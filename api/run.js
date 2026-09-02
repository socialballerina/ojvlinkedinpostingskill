import { requireAuth, readJsonBody, send, fail, gh, HttpError, REPO, WORKFLOW, BRANCH } from "./_lib.js";

/** Start a run: dispatch the workflow that runs the skill in Claude Code. */
export default async function handler(req, res) {
  try {
    if (req.method !== "POST") throw new HttpError(405, "Use POST.");
    requireAuth(req);
    const body = await readJsonBody(req);

    // Refuse to queue a second run while one is still going. Best effort: for a few
    // seconds after a dispatch GitHub has not registered the run yet, so a very fast
    // double press can slip through. That is harmless, because the workflow's own
    // concurrency group serialises runs and publish.sh retries a rejected push.
    const recent = await gh(`/repos/${REPO}/actions/workflows/${WORKFLOW}/runs?per_page=10`);
    const active = (recent?.workflow_runs || []).filter(
      (r) => ["queued", "in_progress", "requested", "waiting", "pending"].includes(r.status)
    );
    if (active.length) {
      throw new HttpError(409, `A run is already going. Wait for it to finish. ${active[0].html_url}`);
    }

    const runId = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19) + "-" +
                  Math.random().toString(36).slice(2, 7);

    await gh(`/repos/${REPO}/actions/workflows/${WORKFLOW}/dispatches`, {
      method: "POST",
      body: {
        ref: BRANCH,
        inputs: {
          run_id: runId,
          ojv_news: String(body.ojvNews || "").slice(0, 4000),
          keyword: String(body.keyword || "").slice(0, 40),
          enquiry_url: String(body.enquiryUrl || "").slice(0, 300),
          offer: String(body.offer || "").slice(0, 400),
          dry_run: body.dryRun === true ? "true" : "false"
        }
      }
    });

    return send(res, 202, {
      runId,
      state: "queued",
      pollAfterSeconds: 20,
      actionsUrl: `https://github.com/${REPO}/actions/workflows/${WORKFLOW}`
    });
  } catch (err) {
    return fail(res, err);
  }
}
