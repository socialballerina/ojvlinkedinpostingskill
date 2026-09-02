import { requireAuth, send, fail, gh, HttpError, REPO, WORKFLOW, BRANCH, styleGate } from "./_lib.js";

async function repoJson(path) {
  const txt = await gh(`/repos/${REPO}/contents/${path}?ref=${BRANCH}`, { raw: true });
  if (txt === null) return null;
  try { return JSON.parse(txt); } catch { return null; }
}

/** Poll a run: report progress, and return the result once the workflow has written it. */
export default async function handler(req, res) {
  try {
    if (req.method !== "GET") throw new HttpError(405, "Use GET.");
    requireAuth(req);
    const runId = String((req.query && req.query.runId) || "").trim();
    if (!/^[0-9a-zA-Z-]{10,60}$/.test(runId)) throw new HttpError(400, "Pass a valid ?runId=.");

    const result = await repoJson(`runs/${runId}/result.json`);
    if (result) {
      // recompute the gate here so the UI never trusts the run's own claim
      for (const p of result.posts || []) p.styleGate = styleGate(p.copy);
      return send(res, 200, { ...result, state: "done" });
    }

    const status = await repoJson(`runs/${runId}/status.json`);
    const runs = await gh(`/repos/${REPO}/actions/workflows/${WORKFLOW}/runs?per_page=5`);
    const wf = (runs?.workflow_runs || [])[0];

    if (status?.state === "failed") {
      return send(res, 200, { runId, state: "failed", error: status.error || "The run failed.", workflowRunUrl: status.workflowRunUrl || wf?.html_url });
    }
    if (wf && wf.status === "completed" && wf.conclusion !== "success" && status?.state !== "done") {
      return send(res, 200, {
        runId, state: "failed",
        error: `The workflow ended as "${wf.conclusion}". Open the log to see why.`,
        workflowRunUrl: wf.html_url
      });
    }

    return send(res, 200, {
      runId,
      state: status?.state === "running" ? "running" : "queued",
      startedAt: status?.startedAt || null,
      workflowRunUrl: status?.workflowRunUrl || wf?.html_url || null,
      workflowStatus: wf ? `${wf.status}${wf.conclusion ? "/" + wf.conclusion : ""}` : null,
      pollAfterSeconds: 20
    });
  } catch (err) {
    return fail(res, err);
  }
}
