import { requireAuth, send, fail, HttpError } from "./_lib.js";

const UA = "ojv-linkedin-posting-tool/1.0 (+https://github.com/socialballerina/ojvlinkedinpostingskill)";
// Only licences that are safe for a company page to use commercially.
// cc0 and pdm need no attribution. by needs a visible credit, so it is flagged.
const OPENVERSE_LICENCES = "cc0,pdm,by";

function stripTags(s = "") {
  return String(s).replace(/<[^>]*>/g, "").trim();
}

async function getJson(url, timeoutMs = 12000) {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), timeoutMs);
  try {
    const r = await fetch(url, { headers: { "User-Agent": UA, Accept: "application/json" }, signal: ac.signal });
    if (!r.ok) return null;
    return await r.json();
  } catch {
    return null;
  } finally {
    clearTimeout(t);
  }
}

async function openverse(q, limit) {
  const url = `https://api.openverse.org/v1/images/?q=${encodeURIComponent(q)}` +
    `&license=${OPENVERSE_LICENCES}&page_size=${limit}&mature=false`;
  const data = await getJson(url);
  if (!data || !Array.isArray(data.results)) return [];
  return data.results.map((r) => {
    const needsCredit = (r.license || "").toLowerCase() === "by";
    return {
      id: `ov-${r.id}`,
      provider: r.provider || r.source || "openverse",
      title: r.title || "",
      thumb: r.thumbnail || r.url,
      full: r.url,
      sourcePage: r.foreign_landing_url || r.url,
      creator: r.creator || "unknown",
      license: `CC ${String(r.license || "").toUpperCase()}${r.license_version ? " " + r.license_version : ""}`.trim(),
      licenseUrl: r.license_url || "",
      attributionRequired: needsCredit,
      attribution: needsCredit
        ? `Photo: ${r.creator || "unknown"} (${r.provider || "source"}), CC ${String(r.license).toUpperCase()} ${r.license_version || ""}`.trim()
        : ""
    };
  });
}

async function wikimedia(q, limit) {
  const url = "https://commons.wikimedia.org/w/api.php?action=query&format=json&origin=*" +
    "&generator=search&gsrnamespace=6" +
    `&gsrsearch=${encodeURIComponent(q)}&gsrlimit=${limit}` +
    "&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=1200";
  const data = await getJson(url);
  const pages = data && data.query && data.query.pages;
  if (!pages) return [];
  return Object.values(pages).map((p) => {
    const ii = (p.imageinfo || [])[0] || {};
    const meta = ii.extmetadata || {};
    const lic = stripTags(meta.LicenseShortName && meta.LicenseShortName.value) || "see source";
    const artist = stripTags(meta.Artist && meta.Artist.value) || "unknown";
    const free = /^(cc0|public domain|pdm)/i.test(lic);
    return {
      id: `wm-${p.pageid}`,
      provider: "wikimedia commons",
      title: p.title || "",
      thumb: ii.thumburl || ii.url,
      full: ii.url,
      sourcePage: ii.descriptionurl || "",
      creator: artist,
      license: lic,
      licenseUrl: stripTags(meta.LicenseUrl && meta.LicenseUrl.value) || "",
      attributionRequired: !free,
      attribution: free ? "" : `Photo: ${artist} (Wikimedia Commons), ${lic}`
    };
  }).filter((i) => i.thumb);
}

export default async function handler(req, res) {
  try {
    if (req.method !== "GET") throw new HttpError(405, "Use GET.");
    requireAuth(req);
    const q = (req.query && req.query.q ? String(req.query.q) : "").trim();
    if (!q) throw new HttpError(400, "Pass ?q=<search words>.");
    const limit = Math.min(Number(req.query.limit) || 6, 12);

    // Narrow queries routinely return nothing on a CC-only corpus, so relax before giving up.
    const words = q.split(/\s+/).filter(Boolean);
    const attempts = [q];
    if (words.length > 2) attempts.push(words.slice(0, -1).join(" "));
    if (words.length > 3) attempts.push(words.slice(0, 2).join(" "));

    let items = [];
    let usedQuery = q;
    let source = "openverse";
    for (const attempt of attempts) {
      items = await openverse(attempt, limit);
      usedQuery = attempt;
      if (items.length >= 3) break;
    }
    if (items.length < 3) {
      const extra = await wikimedia(q, limit);
      const seen = new Set(items.map((i) => i.full));
      items = items.concat(extra.filter((i) => !seen.has(i.full)));
      source = items.length ? "openverse+wikimedia" : "none";
    }

    return send(res, 200, {
      query: q,
      usedQuery,
      relaxed: usedQuery !== q,
      source,
      count: items.length,
      items: items.slice(0, limit),
      note: "Licences shown are what the provider reports. Anything marked attributionRequired must carry its credit line in the post or the first comment. Check the source page before publishing."
    });
  } catch (err) {
    return fail(res, err);
  }
}
