import { requireAuth, send, fail, publicJson, HttpError, styleGate } from "./_lib.js";

/** The newest good result, with no run id and no GitHub credential needed. */
export default async function handler(req, res) {
  try {
    if (req.method !== "GET") throw new HttpError(405, "Use GET.");
    requireAuth(req);
    const result = await publicJson("runs/latest.json");
    if (!result) return send(res, 200, { state: "none" });
    for (const p of result.posts || []) p.styleGate = styleGate(p.copy);
    return send(res, 200, { ...result, state: "done" });
  } catch (err) {
    return fail(res, err);
  }
}
