/* OJV LinkedIn one-button tool.
   The button starts a GitHub Actions run that executes the ojv-linkedin skill in
   Claude Code. This page only triggers it and renders what comes back. */

const $ = (id) => document.getElementById(id);
const PREF_KEY = "ojv.prefs.v1";
const RUN_KEY = "ojv.activeRun.v1";
const LOG_KEY = "ojv.log.v1";

const state = { runId: null, result: null, timer: null, polls: 0 };

/* ---------- prefs ---------- */
const PREF_FIELDS = ["pw", "ojvnews", "keyword", "enquiry", "offer"];
function savePrefs() {
  const p = {};
  for (const k of PREF_FIELDS) p[k] = $(k).value;
  localStorage.setItem(PREF_KEY, JSON.stringify(p));
}
function loadPrefs() {
  try {
    const p = JSON.parse(localStorage.getItem(PREF_KEY) || "{}");
    for (const k of PREF_FIELDS) if (p[k]) $(k).value = p[k];
  } catch {}
}

/* ---------- scheduled-post log, so the skill can learn from it ---------- */
function loadLog() { try { return JSON.parse(localStorage.getItem(LOG_KEY) || "[]"); } catch { return []; } }
function logPost(p) {
  const l = loadLog().filter((x) => x.postId !== p.postId);
  l.push(p);
  localStorage.setItem(LOG_KEY, JSON.stringify(l.slice(-200)));
}

/* ---------- api ---------- */
async function api(path, opts = {}) {
  const r = await fetch(path, {
    ...opts,
    headers: { "Content-Type": "application/json", "x-ojv-key": $("pw").value, ...(opts.headers || {}) }
  });
  const data = await r.json().catch(() => ({ error: `Server returned ${r.status}.` }));
  if (!r.ok && r.status !== 202) throw new Error(data.error || `Server returned ${r.status}.`);
  return data;
}

/* ---------- progress ---------- */
function setStatus(html, cls = "") {
  $("steps").classList.add("on");
  $("steps").innerHTML = `<div class="step ${cls}"><span class="dot"></span><span>${html}</span></div>`;
}
function showErr(msg, url) {
  $("err").innerHTML = esc(msg) + (url ? ` <a href="${esc(url)}" target="_blank" rel="noopener">Open the run log</a>.` : "");
  $("err").classList.add("on");
}
function clearErr() { $("err").classList.remove("on"); $("err").innerHTML = ""; }

/* ---------- run ---------- */
async function start() {
  clearErr();
  if (!$("pw").value) return showErr("Type the password first.");
  savePrefs();
  $("go").disabled = true;
  $("out").innerHTML = "";
  $("foot").style.display = "none";
  state.result = null;
  state.polls = 0;
  setStatus("Starting the run", "doing");

  try {
    const r = await api("/api/run", {
      method: "POST",
      body: JSON.stringify({
        ojvNews: $("ojvnews").value.trim(),
        keyword: $("keyword").value.trim(),
        enquiryUrl: $("enquiry").value.trim(),
        offer: $("offer").value.trim()
      })
    });
    if (r.error) throw new Error(r.error);
    state.runId = r.runId;
    localStorage.setItem(RUN_KEY, r.runId);
    poll();
  } catch (e) {
    setStatus("Could not start", "err");
    showErr(e.message);
    $("go").disabled = false;
  }
}

async function poll() {
  if (!state.runId) return;
  state.polls++;
  try {
    const s = await api(`/api/status?runId=${encodeURIComponent(state.runId)}`);
    const mins = Math.floor((state.polls * 15) / 60);
    const waited = mins ? ` ${mins} min so far.` : "";

    if (s.state === "done") {
      clearTimeout(state.timer);
      localStorage.removeItem(RUN_KEY);
      state.result = s;
      render(s);
      $("go").disabled = false;
      return;
    }
    if (s.state === "failed") {
      clearTimeout(state.timer);
      localStorage.removeItem(RUN_KEY);
      setStatus("The run failed", "err");
      showErr(s.error || "The run failed.", s.workflowRunUrl);
      $("go").disabled = false;
      return;
    }

    setStatus(
      `${s.state === "running" ? "Claude Code is researching and writing" : "Waiting for a runner"}.${waited} ` +
      `This usually takes 5 to 12 minutes.` +
      (s.workflowRunUrl ? ` <a href="${esc(s.workflowRunUrl)}" target="_blank" rel="noopener">Watch it live</a>.` : "") +
      `<br><span class="sub">You can close this tab. Come back and press the button area to resume.</span>`,
      "doing"
    );

    if (state.polls > 120) {
      setStatus("Given up waiting", "err");
      showErr("This run has taken over 30 minutes, which means something is stuck.", s.workflowRunUrl);
      $("go").disabled = false;
      return;
    }
    state.timer = setTimeout(poll, 15000);
  } catch (e) {
    setStatus("Lost contact, retrying", "doing");
    state.timer = setTimeout(poll, 20000);
  }
}

/* ---------- rendering ---------- */
function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }

function render(r) {
  const n = (r.posts || []).length;
  setStatus(`Done. ${n} post${n === 1 ? "" : "s"} for ${esc(r.week || "this week")}.` +
    (r.workflowRunUrl ? ` <a href="${esc(r.workflowRunUrl)}" target="_blank" rel="noopener">Run log</a>.` : ""), "done");

  if (r.needsFromAuthor && r.needsFromAuthor.length) {
    const d = document.createElement("div");
    d.className = "panel";
    d.innerHTML = `<strong>The run needs something from you</strong>
      <ul class="tight">${r.needsFromAuthor.map((x) => `<li>${esc(x)}</li>`).join("")}</ul>`;
    $("out").appendChild(d);
  }

  for (const p of r.posts || []) renderPost(p);
  if (n) $("foot").style.display = "block";

  // stock photo options, only where the run said a generic scene is honest
  for (const p of r.posts || []) {
    if (p.needsTeamPhoto || !p.photoQuery) continue;
    api(`/api/photos?q=${encodeURIComponent(p.photoQuery)}&limit=6`)
      .then((res) => (res.items && res.items.length) ? renderShots(p, res) : renderNoShots(p, res))
      .catch(() => renderNoShots(p, { query: p.photoQuery }));
  }
}

function renderPost(p) {
  const gateOk = !p.styleGate || p.styleGate.length === 0;
  const el = document.createElement("div");
  el.className = "post";
  el.innerHTML = `
    <div class="phead">
      <h2>${esc(p.day)} ${esc(p.date)}, 09:00 HKT</h2>
      <span class="tag">${esc(p.archetype)}. ${esc(p.archetypeName || "")}</span>
      <span class="tag ${p.ctaTier === "hard" ? "hard" : ""}">${esc(p.ctaTier)} CTA</span>
      <span class="tag ${gateOk ? "ok" : "warn"}">${gateOk ? "style ok" : "style: " + esc((p.styleGate || []).join("; "))}</span>
      <span class="tag ${p.verified ? "ok" : "bad"}">${p.verified ? "sources verified" : "NOT verified"}</span>
      <span class="tag">${esc(String(p.charCount || (p.copy || "").length))} chars</span>
    </div>
    <div class="pbody">
      <textarea class="copy" id="copy-${esc(p.postId)}">${esc(p.copy)}</textarea>
      <div class="actions">
        <button class="btn primary" data-act="copy" data-id="${esc(p.postId)}">Copy post text</button>
        ${p.firstComment ? `<button class="btn" data-act="fc" data-id="${esc(p.postId)}">Copy first comment</button>` : ""}
        <a class="btn" style="text-decoration:none;display:inline-block"
           href="https://www.linkedin.com/company/orange-juice-ventures/admin/page-posts/published/"
           target="_blank" rel="noopener">Open the OJV page to schedule</a>
        <button class="btn" data-act="done" data-id="${esc(p.postId)}">Mark scheduled</button>
      </div>
      <div class="meta">
        ${p.whyThisSlot ? `Why this slot: ${esc(p.whyThisSlot)}<br>` : ""}
        ${p.sourceUrl ? `Source${p.sourcePublisher ? " (" + esc(p.sourcePublisher) + ")" : ""}: <a href="${esc(p.sourceUrl)}" target="_blank" rel="noopener">${esc(String(p.sourceUrl).slice(0, 76))}</a><br>` : ""}
        ${p.firstComment ? `First comment: ${esc(p.firstComment)}<br>` : ""}
        ${p.disclosure ? `Disclosure used: "${esc(p.disclosure)}"<br>` : ""}
        ${p.image ? `Image from the library: <code>${esc(p.image)}</code><br>` : ""}
        ${p.altText ? `Alt text: ${esc(p.altText)}` : `Alt text should describe: ${esc(p.photoBrief || "the photo you choose")}`}
      </div>
      ${p.verified ? "" : `<div class="note bad"><strong>Do not schedule this yet</strong>${esc(p.verificationNotes || "The sources could not be confirmed.")}</div>`}
      ${(p.blockers && p.blockers.length) ? `<div class="note"><strong>Fix before scheduling</strong><ul class="tight">${p.blockers.map((b) => `<li>${esc(b)}</li>`).join("")}</ul></div>` : ""}
      ${p.needsTeamPhoto ? teamPhotoBlock(p) : `<div id="shots-${esc(p.postId)}"></div>`}
      <details><summary>What was checked</summary>
        <div class="meta">${esc(p.verificationNotes || "no notes")}</div>
        <div class="meta">Subjects logged: ${esc((p.entities || []).join(", ") || "none")} &middot; hook pattern: ${esc(p.hookPattern || "n/a")}${p.draftPath ? " &middot; draft: " + esc(p.draftPath) : ""}</div>
      </details>
    </div>`;
  $("out").appendChild(el);
  el._post = p;
}

function teamPhotoBlock(p) {
  return `
    <div class="note"><strong>This one needs a photo from the team, not a stock photo</strong>
      ${esc(p.photoBrief || "It is about OJV or a partner, so a stock photo would misrepresent it.")}
      <br><br>Ask in the team chat, or take it yourself. Attach it here to see how it looks, then upload that file to LinkedIn with the post.
    </div>
    <div class="drop" id="drop-${esc(p.postId)}">
      <input type="file" accept="image/*" id="file-${esc(p.postId)}" style="display:none">
      <button class="btn" data-act="pick" data-id="${esc(p.postId)}">Choose a photo</button>
      <div style="margin-top:8px">or tell Naman it still needs shooting</div>
      <div id="prev-${esc(p.postId)}"></div>
    </div>`;
}

function findPost(id) {
  for (const el of $("out").children) if (el._post && el._post.postId === id) return el._post;
  return null;
}

function renderShots(p, r) {
  const box = $("shots-" + p.postId);
  if (!box) return;
  box.innerHTML = `
    <div class="meta" style="margin-top:16px"><strong>Licence-free photo options</strong>
      searched "${esc(r.usedQuery || r.query)}"${r.relaxed ? " (broadened)" : ""} on ${esc(r.source)}.
      Pick one, download it from its source page, then upload it to LinkedIn.</div>
    <div class="shots">
      ${r.items.map((it, i) => `
        <button class="shot" data-act="shot" data-id="${esc(p.postId)}" data-i="${i}">
          <img src="${esc(it.thumb)}" alt="" loading="lazy">
          <div class="lic">${esc(it.license)}${it.attributionRequired ? " &middot; credit needed" : ""}<br>${esc(String(it.creator || "").slice(0, 26))}</div>
        </button>`).join("")}
    </div>
    <div class="meta" id="pick-${esc(p.postId)}"></div>`;
  p.photoOptions = r.items;
}

function renderNoShots(p, r) {
  const box = $("shots-" + p.postId);
  if (!box) return;
  box.innerHTML = `<div class="note"><strong>No licence-free photo matched</strong>
    Nothing usable came back for "${esc(r.query || "")}". Either attach one yourself, or run this post with no image.
    A post with no photo is fine. A photo that contradicts the post is not.
    <div class="drop" id="drop-${esc(p.postId)}" style="margin-top:12px">
      <input type="file" accept="image/*" id="file-${esc(p.postId)}" style="display:none">
      <button class="btn" data-act="pick" data-id="${esc(p.postId)}">Choose a photo</button>
      <div id="prev-${esc(p.postId)}"></div>
    </div></div>`;
}

/* ---------- interactions ---------- */
document.addEventListener("click", (ev) => {
  const b = ev.target.closest("[data-act]");
  if (!b) return;
  const id = b.dataset.id;
  const act = b.dataset.act;
  const p = findPost(id);
  if (!p) return;

  if (act === "copy") {
    navigator.clipboard.writeText($("copy-" + id).value).then(() => {
      b.textContent = "Copied. Now paste it into LinkedIn.";
      setTimeout(() => (b.textContent = "Copy post text"), 2600);
    });
  }
  if (act === "fc") {
    navigator.clipboard.writeText(p.firstComment || "").then(() => {
      b.textContent = "Copied";
      setTimeout(() => (b.textContent = "Copy first comment"), 2000);
    });
  }
  if (act === "done") {
    logPost({
      postId: p.postId, date: p.date, archetype: p.archetype, ctaTier: p.ctaTier,
      hookPattern: p.hookPattern || "", entities: p.entities || [],
      sourceUrl: p.sourceUrl || "", image: p.image || "",
      chars: ($("copy-" + id).value || "").trim().length,
      scheduledAt: new Date().toISOString()
    });
    b.textContent = "Logged";
    b.disabled = true;
  }
  if (act === "pick") {
    const f = $("file-" + id);
    f.onchange = () => {
      const file = f.files && f.files[0];
      if (!file) return;
      $("prev-" + id).innerHTML =
        `<img src="${URL.createObjectURL(file)}" alt=""><div class="meta">${esc(file.name)}. Upload this file to LinkedIn with the post, and write alt text describing ${esc(p.photoBrief || p.altText || "what is in the frame")}.</div>`;
      $("drop-" + id).classList.add("has");
    };
    f.click();
  }
  if (act === "shot") {
    const it = (p.photoOptions || [])[Number(b.dataset.i)];
    if (!it) return;
    b.closest(".shots").querySelectorAll(".shot").forEach((s) => s.classList.remove("sel"));
    b.classList.add("sel");
    $("pick-" + id).innerHTML =
      `Selected. <a href="${esc(it.sourcePage || it.full)}" target="_blank" rel="noopener">Open the source page</a>
       and download the full size, then upload it to LinkedIn. Licence: ${esc(it.license)}.
       ${it.attributionRequired ? `<br><strong>Credit required.</strong> Put this in the first comment: ${esc(it.attribution)}` : "No credit required."}`;
  }
});

$("dl").onclick = () => {
  const rows = [["post_id", "posted_date", "archetype", "cta_tier", "hook_pattern", "entities",
                 "impressions", "reactions", "comments", "reposts", "dm_enquiries", "link_clicks", "notes"]];
  for (const p of loadLog()) {
    rows.push([p.postId, p.date, p.archetype, p.ctaTier, p.hookPattern || "",
               (p.entities || []).join(";"), "", "", "", "", "", "", p.sourceUrl || ""]);
  }
  const csv = rows.map((r) => r.map((c) => /[",;\n]/.test(String(c)) ? `"${String(c).replace(/"/g, '""')}"` : c).join(",")).join("\n");
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
  a.download = `posted-log-${(state.result && state.result.week) || "export"}.csv`;
  a.click();
};

$("forget").onclick = () => {
  if (!confirm("This deletes your record of what has been scheduled. Continue?")) return;
  localStorage.removeItem(LOG_KEY);
  alert("Cleared.");
};

$("go").onclick = start;
PREF_FIELDS.forEach((k) => $(k).addEventListener("change", savePrefs));
loadPrefs();

// resume a run that was going when the tab was closed
const resume = localStorage.getItem(RUN_KEY);
if (resume && $("pw").value) {
  state.runId = resume;
  $("go").disabled = true;
  setStatus("Reconnecting to a run that was already going", "doing");
  poll();
}
$("week").value = "press the button to start a run";
