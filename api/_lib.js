import Anthropic from "@anthropic-ai/sdk";

export const MODEL = process.env.OJV_MODEL || "claude-opus-5";

let cached;
export function client() {
  if (!cached) {
    if (!process.env.ANTHROPIC_API_KEY) {
      throw new HttpError(500, "ANTHROPIC_API_KEY is not set on this deployment. Add it in Vercel: Project Settings, Environment Variables.");
    }
    cached = new Anthropic({ maxRetries: 2 });
  }
  return cached;
}

export class HttpError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

/** Shared-password gate. A public URL that spends API credits needs one. */
export function requireAuth(req) {
  const expected = process.env.APP_PASSWORD;
  if (!expected) {
    throw new HttpError(500, "APP_PASSWORD is not set on this deployment. Add it in Vercel before use.");
  }
  const given = req.headers["x-ojv-key"] || "";
  // constant-ish time compare
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

const WEB_SEARCH = { type: "web_search_20260209", name: "web_search", max_uses: 8 };

/**
 * One Claude turn with web search, resuming pause_turn.
 * Server tools can stop a turn with stop_reason "pause_turn"; if we do not push the
 * paused assistant turn back, the answer comes back silently truncated.
 */
export async function ask({ prompt, system, maxTokens = 16000, effort = "high", maxResumes = 6 }) {
  const c = client();
  const messages = [{ role: "user", content: prompt }];
  let final;

  for (let i = 0; i <= maxResumes; i++) {
    const res = await c.beta.messages.create({
      model: MODEL,
      max_tokens: maxTokens,
      system,
      messages,
      tools: [WEB_SEARCH],
      output_config: { effort },
      // Route around a safety refusal instead of returning nothing to the intern.
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default"
    });
    final = res;
    if (res.stop_reason === "pause_turn") {
      messages.push({ role: "assistant", content: res.content });
      continue;
    }
    break;
  }

  if (final.stop_reason === "refusal") {
    throw new HttpError(502, "The model declined this request. Try a different story or slot.");
  }
  if (final.stop_reason === "pause_turn") {
    throw new HttpError(504, "Research ran long and did not finish. Press the button again.");
  }

  const text = final.content.filter((b) => b.type === "text").map((b) => b.text).join("\n");
  const sources = [];
  for (const block of final.content) {
    if (block.type !== "web_search_tool_result") continue;
    // On success .content is an array of results; on error it is a single error object.
    if (!Array.isArray(block.content)) continue;
    for (const r of block.content) {
      if (r && r.url) sources.push({ url: r.url, title: r.title || r.url });
    }
  }
  return { text, sources, usage: final.usage };
}

/** Pull the first JSON object out of a fenced block, or fall back to brace matching. */
export function extractJson(text) {
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  const candidates = [];
  if (fenced) candidates.push(fenced[1]);
  const start = text.indexOf("{");
  if (start !== -1) {
    let depth = 0, inStr = false, esc = false;
    for (let i = start; i < text.length; i++) {
      const ch = text[i];
      if (inStr) {
        if (esc) esc = false;
        else if (ch === "\\") esc = true;
        else if (ch === '"') inStr = false;
        continue;
      }
      if (ch === '"') inStr = true;
      else if (ch === "{") depth++;
      else if (ch === "}") {
        depth--;
        if (depth === 0) { candidates.push(text.slice(start, i + 1)); break; }
      }
    }
  }
  for (const c of candidates) {
    try { return JSON.parse(c.trim()); } catch { /* try the next one */ }
  }
  throw new HttpError(502, "The model did not return usable JSON. Press the button again.");
}

export const BANNED = [
  "thrilled to announce", "excited to announce", "proud to announce",
  "game-changer", "game changer", "in today's fast-paced world",
  "revolutionizing", "revolutionising", "stay tuned",
  "underscores our dedication", "we look forward to supporting"
];

/** The same checks as skill/scripts/style-gate.py, so the web tool cannot drift from the skill. */
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
  const hasQ = close.endsWith("?");
  const hasCta = /Comment |DM |Enquir|Follow the page|👉/.test(close);
  if (hasQ && hasCta) fails.push("close carries both a question and a CTA");

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
