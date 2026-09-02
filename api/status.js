import { requireAuth, send, fail, gh, publicJson, HttpError, REPO, WORKFLOW, styleGate } from "./_lib.js";

const NOT_FINISHED = new Set(["queued", "in_progress", "requested", "waiting", "pending"]);

// The repo is public, so results are readable with no credential. That means the
// page can show a scheduled run's output before anyone sets up GITHUB_TOKEN.
const repoJson = publicJson;

async function workflowRuns() {
  if (!process.env.GITHUB_TOKEN) return [];
  try {
    const r = await gh(`/repos/${REPO}/actions/workflows/${WORKFLOW}/runs?per_page=10`);
    return r?.workflow_runs || [];
  } catch {
    return [];
  }
}

/** Poll a run: report progress, and return the result once the workflow has written it. */
export default async function handler(req, res) {
  try {
    if (req.method !== "GET") throw new HttpError(405, "Use GET.");
    requireAuth(req);
    const q = req.query || {};
    const runId = String(q.runId || "").trim();
    if (!/^[0-9a-zA-Z-]{10,60}$/.test(runId)) throw new HttpError(400, "Pass a valid ?runId=.");
    // How many times the client has polled. Used only to avoid calling a run dead
    // during the window before GitHub has registered the dispatch.
    const attempt = Math.max(1, Math.min(Number(q.attempt) || 1, 1000));

    const result = await repoJson(`runs/${runId}/result.json`);
    if (result) {
      // Recompute the gate here so the UI never simply trusts the run's own claim.
      for (const p of result.posts || []) p.styleGate = styleGate(p.copy);
      return send(res, 200, { ...result, state: "done" });
    }

    const status = await repoJson(`runs/${runId}/status.json`);
    if (status?.state === "failed") {
      return send(res, 200, {
        runId, state: "failed",
        error: status.error || "The run failed.",
        workflowRunUrl: status.workflowRunUrl || null
      });
    }

    const list = await workflowRuns();
    const active = list.filter((r) => NOT_FINISHED.has(r.status));
    const newest = list[0];

    if (status?.state === "running") {
      // The job started. If its workflow run has since ended without a result, say so
      // rather than polling until the client's own timeout.
      const mine = list.find((r) => r.html_url === status.workflowRunUrl);
      if (mine && !NOT_FINISHED.has(mine.status) && mine.conclusion !== "success") {
        return send(res, 200, {
          runId, state: "failed",
          error: `The run ended as "${mine.conclusion}" without producing posts. Open the log to see which step failed.`,
          workflowRunUrl: mine.html_url
        });
      }
      return send(res, 200, {
        runId, state: "running", startedAt: status.startedAt || null,
        workflowRunUrl: status.workflowRunUrl || null,
        workflowStatus: mine ? `${mine.status}${mine.conclusion ? "/" + mine.conclusion : ""}` : null
      });
    }

    // No marker yet. Either a runner has not picked the job up, or the dispatch never
    // became a run. Only call it dead after GitHub has had time to register it.
    if (!active.length && attempt >= 5 && process.env.GITHUB_TOKEN) {
      return send(res, 200, {
        runId, state: "failed",
        error: "No run ever started for this request. GitHub accepted the dispatch but produced no workflow run, which usually means the workflow file on the default branch changed or Actions is disabled.",
        workflowRunUrl: `https://github.com/${REPO}/actions/workflows/${WORKFLOW}`
      });
    }

    return send(res, 200, {
      runId, state: "queued",
      workflowRunUrl: active[0]?.html_url || newest?.html_url || null,
      workflowStatus: active[0] ? active[0].status : null,
      queuePosition: active.length > 1 ? active.length : undefined
    });
  } catch (err) {
    return fail(res, err);
  }
}
