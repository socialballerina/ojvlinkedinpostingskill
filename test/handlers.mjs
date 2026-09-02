/* No API key needed: these exercise routing, auth and the keyless photo search.
   The model itself runs in GitHub Actions, so it is not under test here. */
process.env.APP_PASSWORD = "localtest123";
process.env.GITHUB_TOKEN = "github_pat_not_a_real_token";

const run = (await import("../api/run.js")).default;
const status = (await import("../api/status.js")).default;
const photos = (await import("../api/photos.js")).default;
const { styleGate } = await import("../api/_lib.js");

function mockRes() {
  const r = { _s: 0, _b: "", headers: {} };
  r.setHeader = (k, v) => { r.headers[k] = v; };
  r.status = (s) => { r._s = s; return r; };
  r.end = (b) => { r._b = b; return r; };
  return r;
}
async function call(h, { method = "GET", key, body, query = {} } = {}) {
  const req = { method, headers: {}, query, body };
  if (key !== undefined) req.headers["x-ojv-key"] = key;
  const res = mockRes();
  await h(req, res);
  let parsed; try { parsed = JSON.parse(res._b); } catch { parsed = res._b; }
  return { status: res._s, body: parsed };
}
const results = [];
const check = (name, got, want) => {
  const ok = got === want;
  results.push(ok);
  console.log(`  ${ok ? "PASS" : "FAIL"}  ${name}  (got ${got}, want ${want})`);
};
const KEY = "localtest123";

console.log("=== auth gate ===");
check("run: no password -> 401", (await call(run, { method: "POST", body: {} })).status, 401);
check("run: wrong password -> 401", (await call(run, { method: "POST", key: "no", body: {} })).status, 401);
check("status: wrong password -> 401", (await call(status, { key: "no", query: { runId: "x".repeat(12) } })).status, 401);
check("photos: wrong password -> 401", (await call(photos, { key: "no", query: { q: "x" } })).status, 401);

console.log("=== method guards ===");
check("run: GET -> 405", (await call(run, { method: "GET", key: KEY })).status, 405);
check("status: POST -> 405", (await call(status, { method: "POST", key: KEY })).status, 405);
check("photos: POST -> 405", (await call(photos, { method: "POST", key: KEY })).status, 405);

console.log("=== input validation ===");
check("status: missing runId -> 400", (await call(status, { key: KEY, query: {} })).status, 400);
check("status: junk runId -> 400", (await call(status, { key: KEY, query: { runId: "../../etc/passwd" } })).status, 400);
check("photos: missing q -> 400", (await call(photos, { key: KEY, query: {} })).status, 400);

console.log("=== github failure is reported, not swallowed ===");
const bad = await call(run, { method: "POST", key: KEY, body: {} });
check("run with a bogus token -> 502", bad.status, 502);
console.log("        message:", String(bad.body.error).slice(0, 78));

console.log("=== keyless photo search, live ===");
const p1 = await call(photos, { key: KEY, query: { q: "electronics components market", limit: "4" } });
check("live CC search -> 200", p1.status, 200);
if (p1.status === 200) {
  console.log("        source:", p1.body.source, "| count:", p1.body.count);
  for (const i of p1.body.items) console.log("         -", i.license, "| credit needed:", String(i.attributionRequired).padEnd(5), "|", i.provider);
  check("no NC/ND/SA licences", p1.body.items.filter((i) => /(nc|nd|sa)/i.test(i.license.replace(/^CC /, "").split(" ")[0])).length, 0);
}
const p2 = await call(photos, { key: KEY, query: { q: "shenzhen huaqiangbei actuator tray stall", limit: "4" } });
if (p2.status === 200) console.log("        relaxation:", JSON.stringify(p2.body.query), "->", JSON.stringify(p2.body.usedQuery), "| count:", p2.body.count);

console.log("=== style gate parity with the skill's python gate ===");
const good = ["Unitree closed its first day on the Shanghai exchange up 542%.", "", "x".repeat(1100), "", "#A #B #C"].join("\n");
check("clean post passes", styleGate(good).length, 0);
check("em dash caught", styleGate(good.replace("542%.", "542% — really.")).some((f) => f.includes("em dash")), true);
check("banned phrase caught", styleGate("We are thrilled to announce x.\n\n" + "y".repeat(1100) + "\n\n#A #B #C").some((f) => f.includes("banned")), true);
check("hashtag count caught", styleGate(good.replace("#A #B #C", "#A #B #C #D #E #F")).some((f) => f.includes("hashtags")), true);
check("question+cta close caught",
  styleGate(["Hook line here.", "", "z".repeat(1050), "", "Comment TREK and we will send it. Ready?", "", "#A #B #C"].join("\n")).some((f) => f.includes("both")), true);

const pass = results.filter(Boolean).length;
console.log(`\n${pass}/${results.length} checks passed`);
process.exit(pass === results.length ? 0 : 1);
