#!/usr/bin/env node
// Feedback-quality scorer. Turns "is the feedback slop?" into numbers:
// Cohen's kappa vs your labels, a confusion matrix, false-accept / false-reject
// on the "fully addressed?" gate, and an adversarial catch-rate.
//
//   node evals/score.mjs [runFile]      # score a run (default: runs/example.json)
//   node evals/score.mjs --template [name]   # write a blank run to fill in
//
// A "run" is { "<caseId>": "yes|partial|no", ... } — the verdict the feedback
// system gave for each gold case (recorded from the app's grader / a /review pass).
import fs from "node:fs";
import path from "node:path";

const HERE = path.dirname(new URL(import.meta.url).pathname);
const CLASSES = ["yes", "partial", "no"];
const KAPPA_BAR = 0.70; // Landis & Koch "substantial"; below this, recalibrate before trusting it

function norm(v) {
  v = String(v == null ? "" : v).trim().toLowerCase();
  if (v.startsWith("part")) return "partial";
  if (v === "y" || v.startsWith("yes") || v.includes("address")) return "yes";
  if (v === "n" || v.startsWith("no")) return "no";
  return v || null;
}
function loadJSON(p) { return JSON.parse(fs.readFileSync(p, "utf8")); }

const gold = loadJSON(path.join(HERE, "gold.json"));

// --template: emit a blank run for the current gold set, then exit.
if (process.argv[2] === "--template") {
  const name = process.argv[3] || "mine";
  const blank = {}; gold.forEach(c => { blank[c.id] = ""; });
  const out = path.join(HERE, "runs", name + ".json");
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, JSON.stringify(blank, null, 2) + "\n");
  console.log("Wrote blank run: " + path.relative(process.cwd(), out));
  console.log("Fill each case with the verdict your feedback system gave (yes | partial | no), then:");
  console.log("  node evals/score.mjs " + path.relative(process.cwd(), out));
  process.exit(0);
}

const runFile = process.argv[2] || path.join(HERE, "runs", "example.json");
const run = loadJSON(runFile);

// Pair up gold labels with system verdicts for covered cases only.
const rows = [];
const missing = [];
for (const c of gold) {
  const sys = norm(run[c.id]);
  if (!sys) { missing.push(c.id); continue; }
  rows.push({ id: c.id, repo: c.repo, adversarial: !!c.adversarial, gold: norm(c.label), sys, note: c.note });
}
const N = rows.length;
if (!N) { console.error("No scorable cases (run covers none of the gold cases)."); process.exit(2); }

// Cohen's kappa (multi-class).
const agree = rows.filter(r => r.gold === r.sys).length;
const po = agree / N;
const pGold = {}, pSys = {};
CLASSES.forEach(k => { pGold[k] = rows.filter(r => r.gold === k).length / N; pSys[k] = rows.filter(r => r.sys === k).length / N; });
const pe = CLASSES.reduce((s, k) => s + pGold[k] * pSys[k], 0);
const kappa = pe >= 1 ? 1 : (po - pe) / (1 - pe);
const band = kappa < 0 ? "poor (worse than chance)" : kappa <= 0.20 ? "slight" : kappa <= 0.40 ? "fair"
  : kappa <= 0.60 ? "moderate" : kappa <= 0.80 ? "substantial" : "almost perfect";

// Confusion matrix gold(row) x sys(col).
const conf = {}; CLASSES.forEach(g => { conf[g] = { yes: 0, partial: 0, no: 0 }; });
rows.forEach(r => { conf[r.gold][r.sys]++; });

// "Fully addressed?" gate: addressed = yes; not-fully = partial|no.
const addr = v => v === "yes";
let FA = 0, FR = 0, goldNotYes = 0, goldYes = 0;
rows.forEach(r => {
  if (r.gold === "yes") goldYes++; else goldNotYes++;
  if (addr(r.sys) && !addr(r.gold)) FA++;   // system said done, it wasn't -> rubber-stamp
  if (!addr(r.sys) && addr(r.gold)) FR++;   // system said not-done, it was -> over-strict
});

// Adversarial catch-rate.
const adv = rows.filter(r => r.adversarial);
const advCaught = adv.filter(r => r.gold === r.sys).length;

// ---- report ----
const pct = (n, d) => d ? (100 * n / d).toFixed(0) + "%" : "n/a";
const L = [];
L.push("FEEDBACK-QUALITY EVAL  ·  run: " + path.relative(process.cwd(), runFile));
L.push("=".repeat(58));
L.push(`Cases scored: ${N}/${gold.length}` + (missing.length ? `  (missing verdicts: ${missing.join(", ")})` : ""));
L.push(`Gold labels — yes:${gold.filter(c=>norm(c.label)==="yes").length}  partial:${gold.filter(c=>norm(c.label)==="partial").length}  no:${gold.filter(c=>norm(c.label)==="no").length}`);
L.push("");
L.push(`Raw agreement:  ${pct(agree, N)}  (${agree}/${N})`);
L.push(`Cohen's kappa:  ${kappa.toFixed(2)}  — ${band}`);
L.push(`Go / no-go:     ${kappa >= KAPPA_BAR ? "PASS — agreement is substantial; safe to lean on" : "FAIL — below " + KAPPA_BAR + "; read the disagreements, fix the rubric, re-run"}`);
L.push("");
L.push("Confusion (rows = your label, cols = system verdict):");
L.push("            yes  partial  no");
CLASSES.forEach(g => { L.push(`   ${g.padEnd(8)}  ${String(conf[g].yes).padStart(3)}   ${String(conf[g].partial).padStart(5)}   ${String(conf[g].no).padStart(2)}`); });
L.push("");
L.push('"Fully addressed?" gate  (addressed = yes; partial/no = not fully):');
L.push(`   False ACCEPT (rubber-stamped a not-done change): ${FA}  (${pct(FA, goldNotYes)} of the ${goldNotYes} not-yes cases)`);
L.push(`   False REJECT (killed a genuinely-done change):    ${FR}  (${pct(FR, goldYes)} of the ${goldYes} yes cases)`);
L.push("   For a merge gate, a false ACCEPT is the dangerous one.");
L.push("");
L.push(`Adversarial catch-rate: ${advCaught}/${adv.length}  (${pct(advCaught, adv.length)}) — the trick cases it got right`);
L.push("");
const dis = rows.filter(r => r.gold !== r.sys);
if (dis.length) {
  L.push("Disagreements to review (this is your to-fix list):");
  dis.forEach(r => { L.push(`   [${r.adversarial ? "adv" : "   "}] ${r.id}: you=${r.gold}  system=${r.sys}`); if (r.note) L.push(`         ${r.note}`); });
} else {
  L.push("No disagreements on covered cases.");
}
console.log(L.join("\n"));
process.exit(kappa >= KAPPA_BAR ? 0 : 1);
