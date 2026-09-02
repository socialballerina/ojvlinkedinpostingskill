/* OJV LinkedIn one-button tool. Front end orchestrates 4 short API calls so no
   single serverless request has to hold research plus three drafts. */

const $ = (id) => document.getElementById(id);
const HISTORY_KEY = "ojv.history.v1";
const PREF_KEY = "ojv.prefs.v1";

const state = { week: null, posts: [] };

/* ---------- saved history: this is what stops the tool repeating itself ---------- */
function loadHistory() {
  try {
    const h = JSON.parse(localStorage.getItem(HISTORY_KEY) || "{}");
    return { posts: h.posts || [] };
  } catch { return { posts: [] }; }
}
function daysBetween(a, b) { return Math.round((a - new Date(b)) / 86400000); }

function historyForApi() {
  const h = loadHistory();
  const now = new Date();
  const archetypes = [], entities = [], hookPatterns = [], stories = [];
  const seenEnt = new Map(), seenPat = new Map();
  for (const p of h.posts.slice().sort((x, y) => new Date(y.date) - new Date(x.date))) {
    const age = daysBetween(now, p.date);
    archetypes.push({ key: p.archetype, daysAgo: age });
    if (p.hookPattern && !seenPat.has(p.hookPattern)) { seenPat.set(p.hookPattern, 1); hookPatterns.push({ pattern: p.hookPattern, daysAgo: age }); }
    for (const e of p.entities || []) {
      const k = e.toLowerCase();
      if (!seenEnt.has(k)) { seenEnt.set(k, 1); entities.push({ name: e, daysAgo: age }); }
    }
    if (p.storyKey || p.sourceUrl) stories.push({ key: p.storyKey, url: p.sourceUrl });
  }
  return { archetypes, entities, hookPatterns, stories };
}

function rememberPost(p) {
  const h = loadHistory();
  h.posts = h.posts.filter((x) => x.postId !== p.postId);
  h.posts.push(p);
  h.posts = h.posts.slice(-120);
  localStorage.setItem(HISTORY_KEY, JSON.stringify(h));
}

/* ---------- prefs ---------- */
function savePrefs() {
  const p = { pw: $("pw").value, ojvnews: $("ojvnews").value, keyword: $("keyword").value,
              enquiry: $("enquiry").value, offer: $("offer").value };
  localStorage.setItem(PREF_KEY, JSON.stringify(p));
}
function loadPrefs() {
  try {
    const p = JSON.parse(localStorage.getItem(PREF_KEY) || "{}");
    for (const k of ["pw", "ojvnews", "keyword", "enquiry", "offer"]) if (p[k]) $(k === "pw" ? "pw" : k).value = p[k];
  } catch {}
}

/* ---------- api ---------- */
async function api(path, opts = {}) {
  const r = await fetch(path, {
    ...opts,
    headers: { "Content-Type": "application/json", "x-ojv-key": $("pw").value, ...(opts.headers || {}) }
  });
  const data = await r.json().catch(() => ({ error: `Server returned ${r.status}.` }));
  if (!r.ok) throw new Error(data.error || `Server returned ${r.status}.`);
  return data;
}
const post = (body) => api("/api/generate", { method: "POST", body: JSON.stringify(body) });

/* ---------- progress ---------- */
const STEPS = [
  ["check", "Checking what this week must not repeat"],
  ["research", "Researching and verifying candidate stories"],
  ["d1", "Writing Monday"],
  ["d2", "Writing Wednesday"],
  ["d3", "Writing Friday"],
  ["photos", "Finding licence-free photos"]
];
function renderSteps() {
  $("steps").classList.add("on");
  $("steps").innerHTML = STEPS.map(([k, label]) =>
    `<div class="step" data-k="${k}"><span class="dot"></span><span>${label}</span></div>`).join("");
}
function mark(k, cls, extra) {
  const el = $("steps").querySelector(`[data-k="${k}"]`);
  if (!el) return;
  el.className = "step " + cls;
  if (extra) el.lastElementChild.textContent = extra;
}
function showErr(msg) { $("err").textContent = msg; $("err").classList.add("on"); }
function clearErr() { $("err").classList.remove("on"); $("err").textContent = ""; }

/* ---------- main run ---------- */
async function run() {
  clearErr();
  if (!$("pw").value) return showErr("Type the password first.");
  savePrefs();
  $("go").disabled = true;
  $("out").innerHTML = "";
  $("foot").style.display = "none";
  state.posts = [];
  renderSteps();

  const config = {
    keyword: $("keyword").value.trim(),
    enquiryUrl: $("enquiry").value.trim(),
    offer: $("offer").value.trim()
  };
  const history = historyForApi();

  try {
    mark("check", "doing");
    const blocked = history.entities.filter((e) => e.daysAgo < 90).length;
    mark("check", "done", blocked
      ? `Blocked ${blocked} recent subject${blocked > 1 ? "s" : ""} and ${history.hookPatterns.filter(p => p.daysAgo < 14).length} hook pattern(s)`
      : "Nothing on record yet, so nothing is blocked");

    mark("research", "doing");
    const plan = await post({ step: "research", config, history, ojvNews: $("ojvnews").value.trim() });
    state.week = plan.week;
    mark("research", "done", `Chose ${plan.slots.map((s) => s.archetype).join(", ")} from ${plan.searched} sources read`);

    for (let i = 0; i < plan.slots.length; i++) {
      const key = "d" + (i + 1);
      mark(key, "doing");
      try {
        const res = await post({ step: "draft", slot: plan.slots[i], config, history });
        state.posts.push(res);
        renderPost(res, plan);
        mark(key, "done", `${plan.slots[i].day}: ${res.draft.charCount} chars, archetype ${res.archetype}`);
      } catch (e) {
        mark(key, "err", `${plan.slots[i].day} failed: ${e.message}`);
      }
    }

    mark("photos", "doing");
    let found = 0;
    for (const p of state.posts) {
      if (p.draft.needsTeamPhoto || !p.draft.photoQuery) continue;
      try {
        const r = await api(`/api/photos?q=${encodeURIComponent(p.draft.photoQuery)}&limit=6`);
        if (r.items && r.items.length) { renderShots(p, r); found++; }
        else renderNoShots(p, r);
      } catch { renderNoShots(p, { query: p.draft.photoQuery }); }
    }
    mark("photos", "done", found ? `Photo options for ${found} post(s)` : "No stock photos used this week");

    if (state.posts.length) $("foot").style.display = "block";
    if (!state.posts.length) showErr("Nothing came back. Press the button again.");
  } catch (e) {
    STEPS.forEach(([k]) => { const el = $("steps").querySelector(`[data-k="${k}"]`); if (el && el.className === "step doing") mark(k, "err"); });
    showErr(e.message);
  } finally {
    $("go").disabled = false;
  }
}

/* ---------- rendering ---------- */
function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }

function renderPost(p, plan) {
  const d = p.draft;
  const gateOk = !d.styleGate || d.styleGate.length === 0;
  const el = document.createElement("div");
  el.className = "post";
  el.id = "post-" + p.postId;
  el.innerHTML = `
    <div class="phead">
      <h2>${esc(p.day)} ${esc(p.date)}, 09:00 HKT</h2>
      <span class="tag">${esc(p.archetype)}. ${esc((plan.slots.find((s) => s.postId === p.postId) || {}).archetypeName || "")}</span>
      <span class="tag ${p.ctaTier === "hard" ? "hard" : ""}">${esc(p.ctaTier)} CTA</span>
      <span class="tag ${gateOk ? "ok" : "warn"}">${gateOk ? "style ok" : "style: " + esc(d.styleGate.join("; "))}</span>
      <span class="tag ${d.verified ? "ok" : "bad"}">${d.verified ? "sources verified" : "NOT verified"}</span>
      <span class="tag">${d.charCount} chars</span>
    </div>
    <div class="pbody">
      <textarea class="copy" id="copy-${p.postId}">${esc(d.copy)}</textarea>
      <div class="actions">
        <button class="btn primary" data-act="copy" data-id="${p.postId}">Copy post text</button>
        ${d.firstComment ? `<button class="btn" data-act="fc" data-id="${p.postId}">Copy first comment</button>` : ""}
        <a class="btn" style="text-decoration:none;display:inline-block"
           href="https://www.linkedin.com/company/orange-juice-ventures/admin/page-posts/published/"
           target="_blank" rel="noopener">Open the OJV page to schedule</a>
        <button class="btn" data-act="done" data-id="${p.postId}">Mark scheduled</button>
      </div>
      <div class="meta">
        ${d.sourceUrl ? `Source: <a href="${esc(d.sourceUrl)}" target="_blank" rel="noopener">${esc(d.sourceUrl.slice(0, 76))}</a><br>` : ""}
        ${d.firstComment ? `First comment: ${esc(d.firstComment)}<br>` : ""}
        ${d.disclosure ? `Disclosure line used: "${esc(d.disclosure)}"<br>` : ""}
        Alt text should describe: ${esc(d.altTextHint || "the photo you choose")}
      </div>
      ${d.verified ? "" : `<div class="note bad"><strong>Do not schedule this yet</strong>The sources could not be confirmed. ${esc(d.verificationNotes || "")}</div>`}
      ${(d.blockers && d.blockers.length) ? `<div class="note"><strong>Fix before scheduling</strong><ul class="tight">${d.blockers.map((b) => `<li>${esc(b)}</li>`).join("")}</ul></div>` : ""}
      ${d.needsTeamPhoto ? teamPhotoBlock(p) : `<div id="shots-${p.postId}"></div>`}
      <details><summary>What was checked</summary>
        <div class="meta">${esc(d.verificationNotes || "no notes")}</div>
        <div class="meta">Subjects logged: ${esc((d.entities || []).join(", ") || "none")} &middot; hook pattern: ${esc(d.hookPattern || "n/a")}</div>
      </details>
    </div>`;
  $("out").appendChild(el);
}

function teamPhotoBlock(p) {
  return `
    <div class="note"><strong>This one needs a photo from the team, not a stock photo</strong>
      ${esc(p.draft.photoBrief || "It is about OJV or a partner, so a stock photo would misrepresent it.")}
      <br><br>Ask in the team chat, or take it yourself. Attach it here to check how it looks, then upload it to LinkedIn with the post.
    </div>
    <div class="drop" id="drop-${p.postId}">
      <input type="file" accept="image/*" id="file-${p.postId}" style="display:none">
      <button class="btn" data-act="pick" data-id="${p.postId}">Choose a photo</button>
      <div style="margin-top:8px">or reply to Naman that it still needs shooting</div>
      <div id="prev-${p.postId}"></div>
    </div>`;
}

function renderShots(p, r) {
  const box = $("shots-" + p.postId);
  if (!box) return;
  box.innerHTML = `
    <div class="meta" style="margin-top:16px"><strong>Licence-free photo options</strong>
      searched "${esc(r.usedQuery || r.query)}"${r.relaxed ? " (broadened)" : ""} on ${esc(r.source)}.
      Pick one, then download it from its source page and upload it to LinkedIn.</div>
    <div class="shots">
      ${r.items.map((it, i) => `
        <button class="shot" data-act="shot" data-id="${p.postId}" data-i="${i}">
          <img src="${esc(it.thumb)}" alt="" loading="lazy">
          <div class="lic">${esc(it.license)}${it.attributionRequired ? " &middot; credit needed" : ""}<br>${esc((it.creator || "").slice(0, 26))}</div>
        </button>`).join("")}
    </div>
    <div class="meta" id="pick-${p.postId}"></div>`;
  p.photoOptions = r.items;
}

function renderNoShots(p, r) {
  const box = $("shots-" + p.postId);
  if (!box) return;
  box.innerHTML = `<div class="note"><strong>No licence-free photo matched</strong>
    Nothing usable came back for "${esc(r.query || "")}". Either attach one yourself, or run this post without an image.
    A post with no photo is fine. A photo that contradicts the post is not.
    <div class="drop" id="drop-${p.postId}" style="margin-top:12px">
      <input type="file" accept="image/*" id="file-${p.postId}" style="display:none">
      <button class="btn" data-act="pick" data-id="${p.postId}">Choose a photo</button>
      <div id="prev-${p.postId}"></div>
    </div></div>`;
}

/* ---------- interactions ---------- */
document.addEventListener("click", (ev) => {
  const b = ev.target.closest("[data-act]");
  if (!b) return;
  const id = b.dataset.id;
  const p = state.posts.find((x) => x.postId === id);
  const act = b.dataset.act;

  if (act === "copy") {
    const ta = $("copy-" + id);
    navigator.clipboard.writeText(ta.value).then(() => {
      b.textContent = "Copied. Now paste it into LinkedIn.";
      setTimeout(() => (b.textContent = "Copy post text"), 2600);
    });
  }
  if (act === "fc") {
    navigator.clipboard.writeText(p.draft.firstComment || "").then(() => {
      b.textContent = "Copied";
      setTimeout(() => (b.textContent = "Copy first comment"), 2000);
    });
  }
  if (act === "done") {
    const ta = $("copy-" + id);
    rememberPost({
      postId: p.postId, date: p.date, archetype: p.archetype, ctaTier: p.ctaTier,
      hookPattern: p.draft.hookPattern, entities: p.draft.entities || [],
      storyKey: (p.story && p.story.storyKey) || "", sourceUrl: p.draft.sourceUrl || "",
      chars: (ta.value || "").trim().length, scheduledAt: new Date().toISOString()
    });
    b.textContent = "Logged. Next week will not repeat it.";
    b.disabled = true;
  }
  if (act === "pick") {
    const f = $("file-" + id);
    f.onchange = () => {
      const file = f.files && f.files[0];
      if (!file) return;
      const url = URL.createObjectURL(file);
      $("prev-" + id).innerHTML = `<img src="${url}" alt=""><div class="meta">${esc(file.name)}. Upload this file to LinkedIn with the post, and write alt text describing ${esc(p.draft.altTextHint || "what is in the frame")}.</div>`;
      $("drop-" + id).classList.add("has");
    };
    f.click();
  }
  if (act === "shot") {
    const it = (p.photoOptions || [])[Number(b.dataset.i)];
    if (!it) return;
    b.closest(".shots").querySelectorAll(".shot").forEach((s) => s.classList.remove("sel"));
    b.classList.add("sel");
    $("pick-" + id).innerHTML = `Selected. <a href="${esc(it.sourcePage || it.full)}" target="_blank" rel="noopener">Open the source page</a>
      and download the full size, then upload it to LinkedIn. Licence: ${esc(it.license)}.
      ${it.attributionRequired ? `<br><strong>Credit required.</strong> Put this in the first comment: ${esc(it.attribution)}` : "No credit required."}
      <br>Alt text should describe: ${esc(p.draft.altTextHint || "what is in the frame")}`;
  }
});

$("dl").onclick = () => {
  const rows = [["post_id", "posted_date", "archetype", "cta_tier", "hook_pattern", "entities",
                 "impressions", "reactions", "comments", "reposts", "dm_enquiries", "link_clicks", "notes"]];
  for (const p of loadHistory().posts) {
    rows.push([p.postId, p.date, p.archetype, p.ctaTier, p.hookPattern || "",
               (p.entities || []).join(";"), "", "", "", "", "", "", p.sourceUrl || ""]);
  }
  const csv = rows.map((r) => r.map((c) => /[",;\n]/.test(c) ? `"${String(c).replace(/"/g, '""')}"` : c).join(",")).join("\n");
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
  a.download = `posted-log-${state.week || "export"}.csv`;
  a.click();
};

$("forget").onclick = () => {
  if (!confirm("This deletes the record of what has been posted. The tool will start repeating itself. Continue?")) return;
  localStorage.removeItem(HISTORY_KEY);
  alert("History cleared.");
};

$("go").onclick = run;
["pw", "ojvnews", "keyword", "enquiry", "offer"].forEach((k) => $(k).addEventListener("change", savePrefs));

loadPrefs();
fetch("/api/generate", { method: "POST", headers: { "Content-Type": "application/json", "x-ojv-key": $("pw").value }, body: JSON.stringify({ step: "ping" }) })
  .then((r) => r.json())
  .then((d) => { $("week").value = d.isoWeek ? `${d.isoWeek} (${d.slots.map((s) => s.date.slice(5)).join(" / ")})` : "type the password, then press the button"; })
  .catch(() => { $("week").value = "type the password, then press the button"; });
