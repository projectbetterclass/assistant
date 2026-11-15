// Lightweight validation for the self-contained artifact `time-tracker.html`.
// Verifies the required blocks exist, the embedded app-state is valid JSON,
// and the inline app script compiles (no JS syntax errors). Exits non-zero on
// any failure so CI turns red.
import fs from "node:fs";
import vm from "node:vm";

const FILE = "time-tracker.html";
let failed = 0;
const fail = (m) => { console.error("✗ " + m); failed++; };
const ok = (m) => console.log("✓ " + m);

const html = fs.readFileSync(FILE, "utf8");

for (const marker of [
  '<style id="app-style">',
  '<script id="app-state" type="application/json">',
  '<script id="app">',
]) {
  if (html.includes(marker)) ok("found " + marker); else fail("missing " + marker);
}

const stateM = html.match(/<script id="app-state" type="application\/json">([\s\S]*?)<\/script>/);
if (!stateM) {
  fail("could not extract the app-state block");
} else {
  try {
    const s = JSON.parse(stateM[1]);
    if (!s || !Array.isArray(s.tasks)) fail("app-state.tasks is not an array");
    else ok("app-state JSON parses (" + s.tasks.length + " tasks, " + ((s.goals || []).length) + " goals)");
  } catch (e) {
    fail("app-state JSON is invalid: " + e.message);
  }
}

const artM = html.match(/<script id="app-articles" type="application\/json">([\s\S]*?)<\/script>/);
if (artM) {
  try {
    const a = JSON.parse(artM[1]);
    if (!a || !Array.isArray(a.items) || a.items.some((x) => !x.id || !x.md || !x.title)) fail("app-articles items are malformed");
    else ok("app-articles JSON parses (" + a.items.length + " articles)");
  } catch (e) {
    fail("app-articles JSON is invalid: " + e.message);
  }
}

const appM = html.match(/<script id="app">([\s\S]*?)<\/script>/);
if (!appM) {
  fail("could not extract the app script");
} else {
  try {
    new vm.Script(appM[1], { filename: "app.js" }); // compiles only; does not run
    ok("app script compiles (no JS syntax errors)");
  } catch (e) {
    fail("app script has a syntax error: " + e.message);
  }
}

if (failed) {
  console.error("\n" + failed + " check(s) failed");
  process.exit(1);
}
console.log("\nAll checks passed");
