// SUPERSEDED by scripts/build-doctrine-learner.py, which writes the learner rewrite (scripts/doctrine-learner.md).
// Running this would put the agent's own rulebook text back, so it needs --agent-text to run at all.
// Bring the Valuation Agent doctrine into the app, so a lesson's reading opens inside the sitting.
//   node scripts/build-doctrine.mjs [path/to/valuation-agent/doctrine]
// Reads every D-NN-*.md entry and three passages of the doctrine README, keeps what you learn from
// (the rule, his reasoning, the hard cases, what stays a judgment, the sources) and leaves out what only
// the code needs (the Engine section) and the change logs. Writes the
// <script id="app-doctrine" type="application/json"> block into time-tracker.html, after the articles.
import fs from "node:fs";
if (!process.argv.includes("--agent-text")) { console.error("superseded: run python3 scripts/build-doctrine-learner.py (or pass --agent-text to restore the agent's text)"); process.exit(1); }
process.argv = process.argv.filter((x) => x !== "--agent-text");
import path from "node:path";
import { execFileSync } from "node:child_process";

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const DIR = path.resolve(process.argv[2] || path.join(ROOT, "..", "valuation-agent", "doctrine"));
const HTML = path.join(ROOT, "time-tracker.html");
if (!fs.existsSync(path.join(DIR, "D-01-story.md"))) { console.error("no doctrine at " + DIR); process.exit(1); }

const DROP = /^(Engine|What changed)/;   // code-only, and the change log
const d = {};
for (const f of fs.readdirSync(DIR).filter((x) => /^D-\d\d-.*\.md$/.test(x)).sort()) {
  const src = fs.readFileSync(path.join(DIR, f), "utf8").replace(/\r\n/g, "\n");
  const head = src.match(/^# (D-\d\d) · (.+)\n/);
  if (!head) throw new Error("no title line in " + f);
  const meta = (src.match(/^\*\*Stage:\*\*.*$/m) || [""])[0].replace(/\*\*/g, "").replace(/\s{2,}/g, " · ").trim();
  const parts = src.split(/^(?=## )/m).slice(1).filter((p) => !DROP.test(p.slice(3)));
  if (!parts.length || !/^## Rule\b/.test(parts[0])) throw new Error("no Rule section first in " + f);
  d[head[1]] = { t: head[2].trim(), m: meta, md: parts.join("").trim() };
}
if (Object.keys(d).length < 49) throw new Error("expected 49 entries, found " + Object.keys(d).length);

const readme = fs.readFileSync(path.join(DIR, "README.md"), "utf8").replace(/\r\n/g, "\n");
const between = (from, to) => {
  const i = readme.indexOf(from); if (i < 0) throw new Error("README: missing " + from);
  const j = to ? readme.indexOf(to, i + from.length) : readme.length; if (j < 0) throw new Error("README: missing " + to);
  return readme.slice(i, j).trim();
};
const x = {
  routes: { t: "Stage 0: routing", md: between("Before any stage runs", "## The 13 stages") },
  pairs: { t: "Paired parameters that self-cancel", md: between("**1. Paired parameters that self-cancel.**", "**2. Disputed constants") },
  paths: { t: "Disputed constants become paths", md: between("**2. Disputed constants become paths.**", "## Where the effort belongs") },
  effort: { t: "Where the effort belongs", md: between("> \"when I've screwed up", "## Build order") },
};

let from = "";
try { from = execFileSync("git", ["-C", DIR, "rev-parse", "--short", "HEAD"], { encoding: "utf8" }).trim(); } catch (e) { /* not a git checkout: fine */ }
const json = JSON.stringify({ from, d, x }).replace(/</g, "\\u003c");
const block = '<script id="app-doctrine" type="application/json">' + json + "</script>";

let html = fs.readFileSync(HTML, "utf8");
const RE = /<script id="app-doctrine" type="application\/json">[\s\S]*?<\/script>/;
if (RE.test(html)) html = html.replace(RE, () => block);
else {
  const arts = html.match(/<script id="app-articles" type="application\/json">[\s\S]*?<\/script>\n/);
  if (!arts) throw new Error("no articles block to sit after");
  html = html.replace(arts[0], () => arts[0] + block + "\n");
}
fs.writeFileSync(HTML, html);
console.log(`doctrine: ${Object.keys(d).length} entries + ${Object.keys(x).length} passages, ${Math.round(json.length / 1024)} KB${from ? " · valuation-agent " + from : ""}`);
