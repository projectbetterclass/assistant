// Packs articles/*.md into the <script id="app-articles"> block of time-tracker.html.
// Each article is a markdown file with a small front-matter header (id, channel, date,
// videoMin, title, checked, charts). The app renders the markdown itself; this script
// only collects the files, so adding a batch never touches the app's code or app-state.
//   node scripts/build-articles.mjs            -> rewrites the block in time-tracker.html
//   node scripts/build-articles.mjs --check    -> exits non-zero if the block is out of date
import fs from "node:fs";
import path from "node:path";

const FILE = "time-tracker.html";
const DIR = "articles";
const OPEN = '<script id="app-articles" type="application/json">';

function parse(file) {
  const text = fs.readFileSync(path.join(DIR, file), "utf8");
  const m = text.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!m) throw new Error(file + ": missing front matter");
  const meta = {};
  for (const line of m[1].split("\n")) {
    const i = line.indexOf(":");
    if (i > 0) meta[line.slice(0, i).trim()] = line.slice(i + 1).trim();
  }
  for (const k of ["id", "channel", "date", "title"]) if (!meta[k]) throw new Error(file + ": missing " + k);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(meta.date)) throw new Error(file + ": bad date " + meta.date);
  return {
    id: meta.id,
    channel: meta.channel,
    date: meta.date,
    videoMin: meta.videoMin ? Number(meta.videoMin) : null,
    title: meta.title,
    checked: meta.checked || null,
    charts: meta.charts === "true",
    md: m[2].trim(),
  };
}

const items = fs.readdirSync(DIR).filter((f) => f.endsWith(".md")).sort().map(parse)
  .sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0));
const ids = new Set();
for (const a of items) { if (ids.has(a.id)) throw new Error("duplicate id " + a.id); ids.add(a.id); }

const json = JSON.stringify({ items }).replace(/</g, "\\u003c");
const block = OPEN + json + "</script>";
const html = fs.readFileSync(FILE, "utf8");
const re = /<script id="app-articles" type="application\/json">[\s\S]*?<\/script>/;
let next;
if (re.test(html)) next = html.replace(re, () => block);
else {
  const anchor = html.indexOf('\n<script id="app">');
  if (anchor < 0) throw new Error("could not find the app script to insert before");
  next = html.slice(0, anchor) + "\n" + block + html.slice(anchor);
}

if (process.argv.includes("--check")) {
  if (next !== html) { console.error("✗ app-articles block is out of date — run node scripts/build-articles.mjs"); process.exit(1); }
  console.log("✓ app-articles block matches articles/ (" + items.length + " articles)");
} else {
  fs.writeFileSync(FILE, next);
  console.log("packed " + items.length + " articles (" + Math.round(json.length / 1024) + " KB) into " + FILE);
}
