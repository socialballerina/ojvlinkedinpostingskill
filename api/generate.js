import { ask, extractJson, requireAuth, readJsonBody, send, fail, styleGate, HttpError, MODEL } from "./_lib.js";
import { SYSTEM, ARCHETYPES, CTA_RULES } from "./_voice.js";

const HKT = "Asia/Hong_Kong";

function hkToday() {
  const s = new Date().toLocaleDateString("en-CA", { timeZone: HKT }); // YYYY-MM-DD
  const [y, m, d] = s.split("-").map(Number);
  return new Date(Date.UTC(y, m - 1, d));
}

function isoWeek(date) {
  const t = new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()));
  const day = t.getUTCDay() || 7;
  t.setUTCDate(t.getUTCDate() + 4 - day);
  const yearStart = new Date(Date.UTC(t.getUTCFullYear(), 0, 1));
  const week = Math.ceil(((t - yearStart) / 86400000 + 1) / 7);
  return { year: t.getUTCFullYear(), week };
}

function iso(d) {
  return d.toISOString().slice(0, 10);
}

/** Next Monday strictly after today, in HKT, plus the Wed and Fri of that week. */
export function weekSlots() {
  const today = hkToday();
  const monday = new Date(today);
  const delta = (8 - (today.getUTCDay() || 7)) % 7 || 7;
  monday.setUTCDate(monday.getUTCDate() + delta);
  const wed = new Date(monday); wed.setUTCDate(wed.getUTCDate() + 2);
  const fri = new Date(monday); fri.setUTCDate(fri.getUTCDate() + 4);
  const { year, week } = isoWeek(monday);
  const tag = `${year}${String(week).padStart(2, "0")}`;
  return {
    isoWeek: `${year}-W${String(week).padStart(2, "0")}`,
    slots: [
      { day: "Monday", date: iso(monday), postId: `OJV-${tag}-M`, slot: "awareness", ctaTier: "soft" },
      { day: "Wednesday", date: iso(wed), postId: `OJV-${tag}-W`, slot: "proof", ctaTier: "medium" },
      { day: "Friday", date: iso(fri), postId: `OJV-${tag}-F`, slot: "offer", ctaTier: "hard" }
    ]
  };
}

function archetypeBrief(keys) {
  return keys.map((k) => {
    const a = ARCHETYPES[k];
    return `### ${k}. ${a.name} (native tier: ${a.tier})\nInput trigger: ${a.trigger}\nSkeleton:\n${a.skeleton.map((s) => "  " + s).join("\n")}\nPhoto: ${a.photo}`;
  }).join("\n\n");
}

function historyBlock(h = {}) {
  const stories = h.stories || [];
  const entities = h.entities || [];
  const patterns = h.hookPatterns || [];
  const arch = h.archetypes || [];
  return `## What has already gone out. These are hard blocks, not preferences.

Archetypes used recently (most recent first): ${arch.length ? arch.map((a) => `${a.key} ${a.daysAgo}d ago`).join(", ") : "none on record"}
BLOCKED hook patterns (used within 14 days): ${patterns.filter((p) => p.daysAgo < 14).map((p) => p.pattern).join(", ") || "none"}
BLOCKED subjects (company, person or city used within 90 days, do not build a post around these): ${entities.filter((e) => e.daysAgo < 90).map((e) => e.name).join(", ") || "none"}
Stories already posted, never repeat: ${stories.map((s) => s.key || s.url).join(" | ") || "none"}

If a story you find is about a blocked subject, discard it and find another.`;
}

async function research(body) {
  const { isoWeek: wk, slots } = weekSlots();
  const cfg = body.config || {};
  const ojvNews = (body.ojvNews || "").trim();
  const h = body.history || {};
  const usedArch = new Set((h.archetypes || []).filter((a) => a.daysAgo < 7).map((a) => a.key));

  const prompt = `Plan one week of three LinkedIn posts for the OJV company page.

Slots, fixed:
- ${slots[0].day} ${slots[0].date} 09:00 HKT, awareness, SOFT CTA. Archetype from A, B, C or D.
- ${slots[1].day} ${slots[1].date} 09:00 HKT, proof, MEDIUM CTA. Archetype from B, C or D.
- ${slots[2].day} ${slots[2].date} 09:00 HKT, offer, HARD CTA (the week's only one). Archetype E by default; A instead only if a strong China deep-tech signal is live AND the flagship offer below is inside 8 weeks of ${slots[2].date}.

Three posts, three DIFFERENT archetypes. Archetypes already used this week: ${[...usedArch].join(", ") || "none"}.

## The five archetypes
${archetypeBrief(["A", "B", "C", "D", "E"])}

${historyBlock(h)}

## Flagship offer, for hard CTAs only
${cfg.offer || "China Tech Trek, Hong Kong and Shenzhen, 13 to 17 October 2026, run with ContraVC as official partner"}

## What OJV itself has done lately, the only valid input for archetype E
${ojvNews || "NOTHING SUPPLIED. If you need archetype E, set needsOjvInput true for that slot and leave the story empty, rather than inventing an OJV event."}

## Your job now
Use web search. For each of the three slots, find and verify ONE story. Rules:
- Search for at least three candidates per slot before choosing.
- Open the primary source. A story qualifies only if you can read the specific numbers in it.
- Record each number as a short quote from the source. If you cannot quote it, do not include it.
- Prefer stories published within the last 60 days, except archetype D and archetype B or C case studies, where a well documented older case is better than a thin recent one. Say the publication date.
- Never choose a story about a blocked subject.

Reply with exactly one fenced json block:

\`\`\`json
{
  "week": "${wk}",
  "slots": [
    {
      "postId": "${slots[0].postId}",
      "day": "Monday",
      "date": "${slots[0].date}",
      "slot": "awareness",
      "ctaTier": "soft",
      "archetype": "A|B|C|D",
      "archetypeName": "...",
      "hookPattern": "reframe|by-design|contrarian-bet|local-claim-broken|number-first",
      "why": "one sentence on why this archetype in this slot this week",
      "needsOjvInput": false,
      "story": {
        "title": "...",
        "publisher": "...",
        "published": "YYYY-MM-DD or best known",
        "url": "the primary source URL you actually opened",
        "storyKey": "short-kebab-case-key",
        "summary": "two sentences",
        "verifiedFacts": [ { "fact": "...", "quote": "the sentence from the source that supports it" } ],
        "entities": ["Company", "Person", "City"]
      }
    }
  ],
  "rejected": [ { "storyKey": "...", "url": "...", "reason": "why it was not used" } ]
}
\`\`\`
Include all three slots in order. Keep the postId, day, date, slot and ctaTier values exactly as given above.`;

  const { text, sources, usage } = await ask({ prompt, system: SYSTEM, maxTokens: 16000 });
  const plan = extractJson(text);
  if (!Array.isArray(plan.slots) || plan.slots.length !== 3) {
    throw new HttpError(502, "Research came back without three slots. Press the button again.");
  }
  // never trust the model with the schedule
  plan.slots.forEach((s, i) => Object.assign(s, slots[i]));
  plan.week = wk;
  return { ...plan, searched: sources.length, usage };
}

async function draft(body) {
  const slot = body.slot;
  if (!slot || !slot.archetype) throw new HttpError(400, "No slot supplied to draft.");
  const cfg = body.config || {};
  const a = ARCHETYPES[slot.archetype];
  if (!a) throw new HttpError(400, `Unknown archetype ${slot.archetype}.`);

  const ctaDetail = slot.ctaTier === "hard"
    ? `${CTA_RULES.hard}\nOffer: ${cfg.offer || "China Tech Trek, Hong Kong and Shenzhen, 13 to 17 October 2026, with ContraVC as official partner"}\nDM keyword: ${cfg.keyword || "TODO(config: DM keyword)"}\nEnquiry destination: ${cfg.enquiryUrl || "TODO(config: enquiry destination)"}\nIf either of those is a TODO marker, put the literal TODO marker in the copy where the value belongs. Do not invent a link or a keyword.`
    : CTA_RULES[slot.ctaTier];

  const prompt = `Write the ${slot.day} post.

Archetype ${slot.archetype}: ${a.name}
Funnel slot: ${slot.slot}
${ctaDetail}

Skeleton, follow it in order:
${a.skeleton.map((s) => "  " + s).join("\n")}

Hook pattern to use: ${slot.hookPattern || "pick one that is not blocked"}

## The story
${JSON.stringify(slot.story || {}, null, 2)}

${historyBlock(body.history)}

## Before you write
Use web search to re-open the source URL and confirm every number you are about to use. If a number in the story object above is not in the source, drop it from the post. If the source cannot be opened at all, set "verified" to false and explain.

## Photo
${a.photo}
${slot.archetype === "E"
  ? 'This is archetype E, so the photo MUST come from the team. Set needsTeamPhoto true, and write photoBrief as a specific request: subject, setting, framing, and which partner should be in frame.'
  : 'If a generic, licence-free stock photo could honestly illustrate this post, set needsTeamPhoto false and write photoQuery as 2 to 5 plain English search words for a stock photo library, describing a SCENE and never a person, a named company, a logo or a brand. If the post is about OJV, a partner, an OJV event, or anything where a stock photo would misrepresent what happened, set needsTeamPhoto true instead and write photoBrief as a specific request.'}

Reply with exactly one fenced json block:

\`\`\`json
{
  "copy": "the finished post, real newlines, no markdown, no surrounding quotes",
  "charCount": 0,
  "hookPattern": "...",
  "hook": "the first line",
  "entities": ["Company", "Person", "City"],
  "verified": true,
  "verificationNotes": "which numbers you confirmed, and anything you dropped",
  "sourceUrl": "...",
  "firstComment": "the text for the first comment, usually the source link, or empty string if none",
  "disclosure": "the exact disclosure sentence used, or empty string if not applicable",
  "needsTeamPhoto": false,
  "photoQuery": "",
  "photoBrief": "",
  "altTextHint": "what the alt text should describe once the photo is chosen",
  "blockers": ["anything the author must resolve before scheduling, such as a TODO config value or a promised asset that does not exist"]
}
\`\`\``;

  let { text, usage } = await ask({ prompt, system: SYSTEM, maxTokens: 16000 });
  let out = extractJson(text);
  let fails = styleGate(out.copy);

  // one repair round, because the style gate is mechanical and the fix is mechanical
  if (fails.length) {
    const repair = await ask({
      system: SYSTEM,
      maxTokens: 16000,
      effort: "medium",
      prompt: `This post failed the style gate. Fix ONLY what failed and keep every fact, the disclosure and the CTA tier identical. Do not add or change any number.

Failures:
${fails.map((f) => "- " + f).join("\n")}

Current post:
${out.copy}

Reply with the same json shape as before, fully populated.`
    });
    const repaired = extractJson(repair.text);
    const refails = styleGate(repaired.copy);
    if (refails.length < fails.length) {
      out = { ...out, ...repaired };
      fails = refails;
    }
    usage = { ...usage, repaired: true };
  }

  out.charCount = (out.copy || "").trim().length;
  out.styleGate = fails;
  out.model = MODEL;
  return { ...slot, draft: out, usage };
}

export default async function handler(req, res) {
  try {
    if (req.method !== "POST") throw new HttpError(405, "Use POST.");
    requireAuth(req);
    const body = await readJsonBody(req);
    if (body.step === "research") return send(res, 200, await research(body));
    if (body.step === "draft") return send(res, 200, await draft(body));
    if (body.step === "ping") return send(res, 200, { ok: true, model: MODEL, ...weekSlots() });
    throw new HttpError(400, `Unknown step "${body.step}".`);
  } catch (err) {
    return fail(res, err);
  }
}
