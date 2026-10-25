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
  for (const k of ["id", "channel", "title"]) if (!meta[k]) throw new Error(file + ": missing " + k);
  // a dated video (investing) needs its date; a numbered piece (a book chapter, a reading path) needs its place instead
  if (meta.n == null && !meta.date) throw new Error(file + ": needs a date or an n");
  if (meta.date && !/^\d{4}-\d{2}-\d{2}$/.test(meta.date)) throw new Error(file + ": bad date " + meta.date);
  if (meta.n != null && !/^\d+$/.test(meta.n)) throw new Error(file + ": bad n " + meta.n);
  if (meta.shelf && !["invest", "business", "books", "ai"].includes(meta.shelf)) throw new Error(file + ": unknown shelf " + meta.shelf);
  const item = {
    id: meta.id,
    channel: meta.channel,
    date: meta.date || null,
    videoMin: meta.videoMin ? Number(meta.videoMin) : null,
    title: meta.title,
    checked: meta.checked || null,
    charts: meta.charts === "true",
    md: m[2].trim(),
  };
  if (meta.shelf) item.shelf = meta.shelf;   // invest when left out
  if (meta.n != null) item.n = Number(meta.n);
  if (meta.part) item.part = meta.part;     // "Ch. 3", "Pricing"
  if (meta.by) item.by = meta.by;           // a book's author
  return item;
}

const items = fs.readdirSync(DIR).filter((f) => f.endsWith(".md")).sort().map(parse)
  .sort((a, b) => (a.n != null && b.n != null ? a.n - b.n : (a.date || "") < (b.date || "") ? 1 : (a.date || "") > (b.date || "") ? -1 : 0));
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
