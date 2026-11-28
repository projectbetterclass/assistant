// Click everything inside every lesson: the A → Z detail (its doctrine cards, its call button), then the sitting
// (Learn: Want more, every card, the call button; Check: every card). Saves what each click shows.
import { launch, openPage } from "./harness.mjs";
import fs from "fs";
const DIR = new URL(".", import.meta.url).pathname;
const GOALS = process.argv[2] ? [process.argv[2]] : ["goal_invest", "goal_opt", "goal_fx", "goal_fire", "goal_biz", "goal_career", "goal_read"];
const browser = await launch();
async function open(gid) {
  const o = await openPage(browser, { width: 402, height: 900, view: "curriculum" });
  await o.page.evaluate(gid => { localStorage.setItem("wmtw_cv_goal", gid); localStorage.setItem("wmtw_cv_mode", "list"); }, gid);
  await o.page.reload(); await o.page.waitForSelector(".top"); await o.page.clock.runFor(100);
  return o;
}
const T = s => (s || "").replace(/\s+/g, " ").trim();
function lint(text) {
  const f = [];
  if (!text || text.length < 40) f.push("empty or near-empty");
  if (/\*\*|\]\(|```|^\|[-: |]+\|$|&lt;|&amp;|<\/?[a-z]+>/m.test(text)) f.push("raw markup: " + (text.match(/\*\*|\]\(|```|&lt;|&amp;|<\/?[a-z]+>/) || [""])[0]);
  if (/\bundefined\b|\bnull\b|NaN|TODO|TBD|\[object/.test(text)) f.push("junk: " + text.match(/\bundefined\b|\bnull\b|NaN|TODO|TBD|\[object/)[0]);
  return f;
}
async function clickCards(page, scope, where, L, docs) {
  const keys = await page.$$eval(scope + " [data-action=doc-open]", els => els.map(e => e.getAttribute("data-k")));
  for (const k of keys) {
    await page.$eval("details.ses-more", e => e.open = true).catch(() => {});
    const b = await page.$(`[data-action=doc-open][data-k="${k}"]`);
    if (!b) { L.flags.push(where + ": card " + k + " vanished before click"); continue; }
    await b.click(); await page.clock.runFor(30);
    const body = await page.$eval(`[data-k="${k}"]`, e => { const d = e.closest(".doc").querySelector(".doc-body"); return d ? d.innerText : null; }).catch(() => null);
    const id = k.split(":").pop();
    if (body === null) L.flags.push(where + ": card " + id + " opens nothing");
    else { docs[id] = docs[id] || body; lint(body).forEach(x => L.flags.push(where + ": card " + id + " " + x)); }
    L.clicked.push(where + " card " + id + (body ? " (" + body.length + " chars)" : ""));
    const b2 = await page.$(`[data-action=doc-open][data-k="${k}"]`); if (b2) { await b2.click(); await page.clock.runFor(20); }
    if (where === "Learn" && !(await page.$("details.ses-more[open]"))) L.folds = true;   // closing a card folded "Want more" shut
  }
}
async function clickCall(page, scope, where, L, calls) {
  const c = await page.$(scope + " [data-action=asw-go]");
  if (!c) return;
  const id = await c.getAttribute("data-id");
  await c.click(); await page.clock.runFor(80);
  const res = await page.evaluate(id => {
    const el = document.querySelector('.asw-call[data-id="' + id + '"]');
    const box = el && el.closest(".asw-c");
    return { view: localStorage.getItem("wmtw_view"), found: !!el, text: box ? box.innerText : "", running: !!document.querySelector(".now-active") };
  }, id);
  calls[id] = calls[id] || res.text;
  L.clicked.push(where + " call " + id + " → " + (res.found ? "opens the " + id + " call on the goal page" : "NOT FOUND") + (res.text ? " (" + res.text.length + " chars)" : ""));
  if (!res.found) L.flags.push(where + ": call button " + id + " leads nowhere");
  else if (res.text.length < 200) L.flags.push(where + ": call " + id + " shows almost nothing");
  return res;
}

for (const gid of GOALS) {
  let o = await open(gid);
  const lids = [...new Set(await o.page.$$eval(".ls-main[data-action=cur-open]", els => els.map(e => e.getAttribute("data-id"))))];
  await o.ctx.close();
  const out = { gid, lessons: [], docs: {}, calls: {}, labs: [] };
  for (const lid of lids) {
    const L = { lid, flags: [], clicked: [] };
    // 1. the lesson in the A → Z list
    o = await open(gid); let { page, errors } = o;
    const rows = await page.$$(`.ls-main[data-action=cur-open][data-id="${lid}"]`);
    await rows[rows.length - 1].click(); await page.clock.runFor(50);
    const det = await page.$(".ls-det");
    L.detail = det ? T(await det.innerText()) : "";
    if (!det) L.flags.push("A → Z: lesson doesn't open");
    const lab = await page.$eval(".ls-det .curr-ex:not(:has(ul))", e => e.innerText).catch(() => "");
    if (lab) { L.lab = T(lab); out.labs.push(lid + ": " + L.lab); }
    const vids = await page.$$eval(".ls-det a[href]", els => els.map(a => ({ t: a.innerText.trim(), h: a.href })));
    L.videos = vids;
    vids.forEach(v => { if (!/^https:\/\/(www\.)?youtube\.com\/watch\?v=[\w-]{11}$|^https:\/\/youtu\.be\/[\w-]{11}$/.test(v.h)) L.flags.push("odd link " + v.h); });
    await clickCards(page, ".ls-det", "A → Z", L, out.docs);
    await clickCall(page, ".ls-det", "A → Z", L, out.calls);
    if (errors.length) L.flags.push("errors (A → Z): " + errors.join(" | "));
    await o.ctx.close();
    // 2. the sitting
    o = await open(gid); ({ page, errors } = o);
    await page.evaluate(({ gid, lid }) => { const b = document.createElement("button"); b.setAttribute("data-action", "cur-start"); b.setAttribute("data-id", gid); b.setAttribute("data-lid", lid); document.getElementById("root").appendChild(b); b.click(); }, { gid, lid });
    await page.clock.runFor(80);
    if (!(await page.$(".now-active .ses"))) { L.flags.push("sitting doesn't open"); out.lessons.push(L); await o.ctx.close(); continue; }
    await page.click('.ses-pills [data-action=ses-stage][data-i="1"]'); await page.clock.runFor(40);
    const more = await page.$("details.ses-more");
    if (more) { await page.$eval("details.ses-more", e => e.open = true); L.clicked.push("Learn: Want more opened"); }
    await clickCards(page, ".now-active .ses", "Learn", L, out.docs);
    await page.click('.ses-pills [data-action=ses-stage][data-i="3"]'); await page.clock.runFor(40);
    await clickCards(page, ".now-active .ses", "Check", L, out.docs);
    await page.click('.ses-pills [data-action=ses-stage][data-i="1"]'); await page.clock.runFor(40);
    const res = await clickCall(page, ".now-active .ses", "Learn", L, out.calls);
    if (res) {   // the call button took you to the goal page: can you get back to your sitting?
      const back = await page.$('[data-action=set-view][data-view="lessons"]');
      if (back) { await back.click(); await page.clock.runFor(40); }
      const okBack = await page.$(".now-active .ses .ses-pill.on");
      const stage = okBack ? await okBack.innerText() : "";
      L.clicked.push("back to the sitting via Lessons → " + (okBack ? "sitting still there, on " + T(stage) : "SITTING GONE"));
      if (!okBack) L.flags.push("after the call button, the sitting is gone");
    }
    if (errors.length) L.flags.push("errors (sitting): " + errors.join(" | "));
    out.lessons.push(L);
    await o.ctx.close();
  }
  fs.writeFileSync(DIR + "deep-" + gid + ".json", JSON.stringify(out, null, 1));
  const n = out.lessons.reduce((a, l) => a + l.clicked.length, 0), fl = out.lessons.filter(l => l.flags.length);
  console.log(gid + ": " + out.lessons.length + " lessons, " + n + " clicks, " + Object.keys(out.docs).length + " cards, " + Object.keys(out.calls).length + " calls, flagged " + fl.length);
  fl.forEach(l => console.log("   " + l.lid + ": " + [...new Set(l.flags)].join("; ")));
  if (out.labs.length) console.log("   labs: " + out.labs.join(" || "));
}
await browser.close();
