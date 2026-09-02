/* Shared helpers. No Anthropic SDK: the model runs in GitHub Actions, not here. */

export class HttpError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

export const REPO = process.env.GITHUB_REPO || "socialballerina/ojvlinkedinpostingskill";
export const WORKFLOW = process.env.GITHUB_WORKFLOW_FILE || "generate-week.yml";
export const BRANCH = process.env.GITHUB_BRANCH || "main";

export function ghToken() {
  const t = process.env.GITHUB_TOKEN;
  if (!t) {
    throw new HttpError(500,
      "GITHUB_TOKEN is not set on this deployment. Add a fine-grained token with Actions read and write plus Contents read, in Vercel: Project Settings, Environment Variables.");
  }
  return t;
}

/** Shared-password gate. A public URL that can start a paid job needs one. */
export function requireAuth(req) {
  const expected = process.env.APP_PASSWORD;
  if (!expected) {
    throw new HttpError(500, "APP_PASSWORD is not set on this deployment. Add it in Vercel before use.");
  }
  const given = req.headers["x-ojv-key"] || "";
  if (given.length !== expected.length) throw new HttpError(401, "Wrong password.");
  let diff = 0;
  for (let i = 0; i < expected.length; i++) diff |= given.charCodeAt(i) ^ expected.charCodeAt(i);
  if (diff !== 0) throw new HttpError(401, "Wrong password.");
}

export async function readJsonBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const raw = Buffer.concat(chunks).toString("utf8");
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch {
    throw new HttpError(400, "Body was not valid JSON.");
  }
}

/** Read a file from the public repo with no credential. Only dispatching needs a token. */
export async function publicFile(path) {
  const url = `https://raw.githubusercontent.com/${REPO}/${BRANCH}/${path}`;
  const res = await fetch(url, { headers: { "User-Agent": "ojv-linkedin-tool/2.0" } });
  if (res.status === 404) return null;
  if (!res.ok) throw new HttpError(502, `Could not read ${path} from GitHub (${res.status}).`);
  return await res.text();
}

export async function publicJson(path) {
  const txt = await publicFile(path);
  if (txt === null) return null;
  try { return JSON.parse(txt); } catch { return null; }
}

export async function gh(path, { method = "GET", body, raw = false, token } = {}) {
  const res = await fetch(`https://api.github.com${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${token || ghToken()}`,
      Accept: raw ? "application/vnd.github.raw" : "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "ojv-linkedin-tool/2.0",
      ...(body ? { "Content-Type": "application/json" } : {})
    },
    body: body ? JSON.stringify(body) : undefined
  });
  if (res.status === 404) return null;
  if (res.status === 401 || res.status === 403) {
    throw new HttpError(502, "GitHub rejected the token. Check that GITHUB_TOKEN has Actions read and write plus Contents read on this repository.");
  }
  if (!res.ok) {
    const t = await res.text().catch(() => "");
    throw new HttpError(502, `GitHub returned ${res.status}. ${t.slice(0, 200)}`);
  }
  if (res.status === 204) return { ok: true };
  return raw ? await res.text() : await res.json();
}

/** The same checks as the skill's scripts/style-gate.py, for display only. */
export const BANNED = [
  "thrilled to announce", "excited to announce", "proud to announce",
  "game-changer", "game changer", "in today's fast-paced world",
  "revolutionizing", "revolutionising", "stay tuned",
  "underscores our dedication", "we look forward to supporting"
];

export function styleGate(copy) {
  const body = (copy || "").trim();
  const lines = body.split("\n").map((l) => l.trim()).filter(Boolean);
  const fails = [];
  if (!lines.length) return ["empty copy"];

  const hook = lines[0];
  const tags = body.match(/#\w+/g) || [];

  if (body.includes("—")) fails.push("em dash present");
  for (const b of BANNED) if (body.toLowerCase().includes(b)) fails.push(`banned phrase: ${b}`);
  if (hook.length > 140) fails.push(`hook is ${hook.length} chars, limit 140`);
  if (body.length < 900 || body.length > 1300) fails.push(`length ${body.length} chars, band is 900 to 1300`);
  if (tags.length < 3 || tags.length > 5) fails.push(`${tags.length} hashtags, band is 3 to 5`);
  if (tags.length && !lines[lines.length - 1].startsWith("#")) fails.push("hashtags are not on the final line");
  if (/\w\s#\w+\s+\w/.test(body)) fails.push("hashtag appears mid-sentence");

  const close = lines[lines.length - 1].startsWith("#") ? lines[lines.length - 2] || "" : lines[lines.length - 1];
  if (close.endsWith("?") && /Comment |DM |Enquir|Follow the page|👉/.test(close)) {
    fails.push("close carries both a question and a CTA");
  }
  return fails;
}

export function send(res, status, payload) {
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");
  res.status(status).end(JSON.stringify(payload));
}

export function fail(res, err) {
  const status = err instanceof HttpError ? err.status : 500;
  if (status >= 500) console.error(err);
  send(res, status, { error: err.message || "Something went wrong." });
}
