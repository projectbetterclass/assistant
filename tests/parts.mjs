// A lesson bigger than today's slot runs over several sittings: part k of n, recall from part 2, the right buttons.
import { launch, openPage, check, summary, lastPub } from "./harness.mjs";
import fs from "fs";
const browser = await launch();
const txt = (p, s) => p.$eval(s, e => e.innerText.replace(/\s+/g, " ").trim()).catch(() => "");
async function start(page, lid, gid = "goal_invest") {
  await page.evaluate(({ gid, lid }) => { const b = document.createElement("button"); b.setAttribute("data-action", "cur-start"); b.setAttribute("data-id", gid); b.setAttribute("data-lid", lid); document.getElementById("root").appendChild(b); b.click(); }, { gid, lid });
  await page.clock.runFor(80);
}
async function carry(o, opts) {
  const h = await o.page.evaluate(() => window.__pub[window.__pub.length - 1]);
  await o.ctx.close();
  const f = new URL("./parts-tmp.html", import.meta.url).pathname; fs.writeFileSync(f, h);
  return openPage(browser, { ...opts, file: f });
}
const pillsSum = p => p.$$eval(".ses-pills .ses-pill span", s => s.reduce((a, e) => a + parseInt(e.textContent, 10), 0));
const wd = await (async () => { const { page, ctx } = await openPage(browser, {}); const v = await page.evaluate(() => { const s = JSON.parse(document.getElementById("app-state").textContent); return s.dayRound && s.dayRound.weekday; }); await ctx.close(); return v; })();
check("the weekday slot is 14 minutes in this state", wd === 14, wd);

// 1. a 120-minute lesson on a Monday: part 1 of 8, about 15 minutes
let o = await openPage(browser, {}); let { page, errors } = o;
await start(page, "L33");
let brief = await txt(page, ".ses-brief");
check("L33 day 1: part 1 of 8, about 15 minutes", /Part 1 of 8, about 15 minutes/.test(brief) && /about 120 minutes/.test(brief), brief);
check("L33 day 1: done for today, not done when", /Done for today/i.test(brief) && !/Done when/i.test(brief), brief);
check("L33 day 1: the four steps add up to 15", (await pillsSum(page)) === 15);
check("L33 day 1: step 1 is Guess", /Step 1 of 4 · Guess/i.test(await txt(page, ".ses")));
await page.fill("#ses-guess", "story then numbers");
await page.click('.ses-pills [data-i="2"]'); await page.clock.runFor(40);
await page.fill("#ses-answer", "Picked ASML; story half written");
await page.click('.dec-nav [data-i="3"]'); await page.clock.runFor(40);
check("L33 day 1: Check leads with Done for today · part 1 of 8", /Done for today · part 1 of 8/.test(await txt(page, ".ses .curr-btns .btn-primary")));
check("L33 day 1: nailed still there for an early finish", !!(await page.$(".ses [data-action=cur-nailed]")));
await page.clock.runFor(15 * 60000);
await page.click(".ses [data-action=ses-stop]"); await page.clock.runFor(80);
check("L33 day 1: toast says part 1 of 8 done", /Part 1 of 8 done/.test(await txt(page, "#toast")), await txt(page, "#toast"));
let s = await lastPub(page);
check("L33 day 1: clock stopped, lesson not done", !s.activeId && !((s.goals.find(g => g.id === "goal_invest").curr || {}).done || {}).L33);
check("no errors (day 1)", errors.length === 0, errors);

// 2. Tuesday: part 2 of 8, recall first, last time's notes in Learn
o = await carry(o, { time: new Date("2026-11-10T10:00:00") }); ({ page, errors } = o);
await start(page, "L33");
brief = await txt(page, ".ses-brief");
check("L33 day 2: part 2 of 8", /Part 2 of 8/.test(brief), brief);
check("L33 day 2: step 1 is Recall", /Step 1 of 4 · Recall/i.test(await txt(page, ".ses")) && /1 Recall/.test(await txt(page, ".ses-pills")));
await page.fill("#ses-guess", "ASML story");
await page.click('.dec-nav [data-i="1"]'); await page.clock.runFor(40);
const prev = await txt(page, ".ses-prev");
check("L33 day 2: Learn shows where you stopped", /Where you stopped last time/.test(prev) && /Picked ASML/.test(prev), prev);
await page.click('.ses-pills [data-i="3"]'); await page.clock.runFor(40);
check("L33 day 2: Check says You recalled", /You recalled/i.test(await txt(page, ".ses-cmp")));
check("no errors (day 2)", errors.length === 0, errors);
await o.ctx.close();

// 3. a 30-minute lesson: 2 sittings on weekdays, 1 at the weekend; the last part ends on nailed
o = await openPage(browser, {}); ({ page, errors } = o);
await start(page, "L02");
check("L02 Monday: part 1 of 2, about 15 minutes", /Part 1 of 2, about 15 minutes/.test(await txt(page, ".ses-brief")), await txt(page, ".ses-brief"));
await page.clock.runFor(15 * 60000);
await page.click('.ses-pills [data-i="3"]'); await page.clock.runFor(40);
await page.click(".ses [data-action=ses-stop]"); await page.clock.runFor(80);
o = await carry(o, { time: new Date("2026-11-10T09:00:00") }); ({ page, errors } = o);
await start(page, "L02");
brief = await txt(page, ".ses-brief");
check("L02 Tuesday: part 2 of 2, the last part, about 15 minutes", /Part 2 of 2/.test(brief) && /Done when/i.test(brief) && /About 15 minutes/.test(brief), brief);
await page.click('.ses-pills [data-i="3"]'); await page.clock.runFor(40);
check("L02 Tuesday: nailed leads again", /nailed/i.test(await txt(page, ".ses .curr-btns .btn-primary")));
check("no errors (L02)", errors.length === 0, errors);
await o.ctx.close();
o = await openPage(browser, { time: new Date("2026-11-14T10:00:00") }); ({ page, errors } = o);   // a Saturday
await start(page, "L02");
brief = await txt(page, ".ses-brief");
check("L02 Saturday: one sitting, no parts", !/Part \d of/.test(brief) && /About \d+ minutes/.test(brief), brief);
check("no errors (Saturday)", errors.length === 0, errors);
await o.ctx.close();

// 4. the lesson list says how many sittings
o = await openPage(browser, { view: "curriculum" }); ({ page, errors } = o);
await page.evaluate(() => { localStorage.setItem("wmtw_goal", "goal_invest"); localStorage.setItem("wmtw_cv_goal", "goal_invest"); localStorage.setItem("wmtw_cv_mode", "list"); });
await page.reload(); await page.waitForSelector(".top"); await page.clock.runFor(100);
const opener = await page.$('[data-action="cur-open"][data-id="L33"]');
if (opener) { await opener.click(); await page.clock.runFor(60); }
const btn = await txt(page, '.curr-btns [data-action="cur-start"][data-lid="L33"]');
check("L33 in the list: ~120 min · 8 sittings", /~120 min · 8 sittings/.test(btn), btn);
check("no errors (list)", errors.length === 0, errors);
await o.ctx.close();
// 5. your own L01: past its estimate (about 65 of 30 minutes), so one more full sitting, not a scrap
o = await openPage(browser, { time: new Date("2026-11-10T10:00:00") }); ({ page, errors } = o);
await start(page, "L01");
brief = await txt(page, ".ses-brief");
check("L01 past its estimate: a full 14-minute sitting, the last part", /About 14 minutes/.test(brief) && /Done when/i.test(brief), brief);
check("L01: the steps add up to 14", (await pillsSum(page)) === 14);
check("no errors (L01)", errors.length === 0, errors);
await o.ctx.close();
await browser.close();
process.exit(summary("parts") ? 1 : 0);
