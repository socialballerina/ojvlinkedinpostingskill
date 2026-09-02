process.env.APP_PASSWORD = "localtest123";
process.env.ANTHROPIC_API_KEY = "sk-ant-not-a-real-key-for-routing-tests";

const gen = (await import("../api/generate.js")).default;
const pho = (await import("../api/photos.js")).default;

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

console.log("=== auth gate ===");
check("no password -> 401", (await call(gen, { method: "POST", body: { step: "ping" } })).status, 401);
check("wrong password -> 401", (await call(gen, { method: "POST", key: "nope", body: { step: "ping" } })).status, 401);
check("GET on POST-only -> 405", (await call(gen, { method: "GET", key: "localtest123" })).status, 405);

console.log("=== generate routing ===");
const ping = await call(gen, { method: "POST", key: "localtest123", body: { step: "ping" } });
check("correct password + ping -> 200", ping.status, 200);
console.log("        week:", ping.body.isoWeek, "| model:", ping.body.model);
console.log("        slots:", (ping.body.slots || []).map(s => `${s.day[0]} ${s.date} ${s.ctaTier}`).join(" | "));
check("unknown step -> 400", (await call(gen, { method: "POST", key: "localtest123", body: { step: "bogus" } })).status, 400);
check("draft with no slot -> 400", (await call(gen, { method: "POST", key: "localtest123", body: { step: "draft" } })).status, 400);
check("draft with bad archetype -> 400",
  (await call(gen, { method: "POST", key: "localtest123", body: { step: "draft", slot: { archetype: "Z" } } })).status, 400);

console.log("=== photos ===");
check("no query -> 400", (await call(pho, { key: "localtest123", query: {} })).status, 400);
check("photos auth enforced -> 401", (await call(pho, { key: "nope", query: { q: "x" } })).status, 401);
const p1 = await call(pho, { key: "localtest123", query: { q: "electronics components market", limit: "4" } });
check("live CC search -> 200", p1.status, 200);
if (p1.status === 200) {
  console.log("        source:", p1.body.source, "| count:", p1.body.count, "| relaxed:", p1.body.relaxed);
  for (const i of p1.body.items) console.log("         -", i.license, "| credit needed:", String(i.attributionRequired).padEnd(5), "|", i.provider, "|", (i.creator || "").slice(0, 20));
  const bad = p1.body.items.filter(i => /nc|nd|sa/i.test(i.license.replace(/^CC /, "").split(" ")[0]));
  check("no NC/ND/SA licences returned", bad.length, 0);
}
const p2 = await call(pho, { key: "localtest123", query: { q: "shenzhen huaqiangbei actuator tray stall", limit: "4" } });
if (p2.status === 200) console.log("        relaxation: asked", JSON.stringify(p2.body.query), "-> used", JSON.stringify(p2.body.usedQuery), "| relaxed:", p2.body.relaxed, "| count:", p2.body.count);

console.log("=== style gate parity with the skill's python gate ===");
const { styleGate } = await import("../api/_lib.js");
const good = ["Unitree closed its first day on the Shanghai exchange up 542%.", "", "x".repeat(1100), "", "#A #B #C"].join("\n");
check("clean post passes", styleGate(good).length, 0);
check("em dash caught", styleGate(good.replace("542%.", "542% — really.")).some(f => f.includes("em dash")), true);
check("banned phrase caught", styleGate("We are thrilled to announce x.\n\n" + "y".repeat(1100) + "\n\n#A #B #C").some(f => f.includes("banned")), true);
check("too many hashtags caught", styleGate(good.replace("#A #B #C", "#A #B #C #D #E #F")).some(f => f.includes("hashtags")), true);
check("question+cta close caught",
  styleGate(["Hook line here.", "", "z".repeat(1050), "", "Comment TREK and we will send it. Ready?", "", "#A #B #C"].join("\n")).some(f => f.includes("both")), true);

const pass = results.filter(Boolean).length;
console.log(`\n${pass}/${results.length} checks passed`);
process.exit(pass === results.length ? 0 : 1);
