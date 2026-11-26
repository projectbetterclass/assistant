// lessons in two halves: part 1 learn it (guess, read, the idea in one line, Done), part 2 next time do it (recall, write, check).
// A part counts when you press its Done, however long it took: the clock stops and the day plan shows it done.
import fs from "fs";
import { launch, openPage, check, summary, noHScroll } from "./harness.mjs";
const browser = await launch();
const TMP = new URL("./part-next.html", import.meta.url).pathname;   // the saved page after day 1 (holds your data: never committed)
const D1 = new Date(2026, 10, 18, 17, 0).getTime(), D2 = new Date(2026, 10, 19, 17, 0).getTime(), SAT = new Date(2026, 10, 21, 11, 0).getTime();
const txt = (p, s) => p.$eval(s, e => e.innerText.replace(/\s+/g, " ").trim()).catch(() => "");
const start = async (page, gid, lid) => { await page.evaluate(({ gid, lid }) => { const b = document.createElement("button"); b.setAttribute("data-action", "cur-start"); b.setAttribute("data-id", gid); b.setAttribute("data-lid", lid); document.getElementById("root").appendChild(b); b.click(); }, { gid, lid }); await page.clock.runFor(80); };
const lastState = page => page.evaluate(() => { const h = window.__pub[window.__pub.length - 1] || ""; const m = h.match(/<script id="app-state"[^>]*>([\s\S]*?)<\/script>/); return m ? JSON.parse(m[1]) : null; });
const tile = (page, name) => page.$$eval(".nowc-card", (els, name) => { const e = els.find(x => x.dataset.name === name); return e ? e.querySelector(".nowc-m").innerText.replace(/\s+/g, " ") : ""; }, name);

for (const w of [402, 900]) {
  // day 1: FIRE plan, part 1, done early
  let { page, errors, ctx } = await openPage(browser, { width: w, time: D1 });
  await start(page, "goal_fire", "F01");
  let brief = await txt(page, ".ses-brief");
  check(`${w} part 1 says what it is`, /Part 1 of 2: learn it/.test(brief) && /however long it took/.test(brief), brief.slice(0, 300));
  check(`${w} part 1 has two steps`, (await page.$$(".ses-pills .ses-pill")).length === 2 && /1 Guess/.test(await txt(page, ".ses-pills")) && /2 Learn/.test(await txt(page, ".ses-pills")));
  await page.fill("#ses-guess", "a guess");
  await page.click('.dec-nav [data-i="1"]'); await page.clock.runFor(40);
  check(`${w} Learn ends with the one line and Done`, !!(await page.$("#ses-gist")) && /Done · part 1 of 2/.test(await txt(page, ".ses")), (await txt(page, ".ses")).slice(-300));
  check(`${w} no Write or Check in part 1`, !(await page.$('.ses-pills [data-i="2"]')) && !(await page.$("#ses-answer")));
  await page.clock.runFor(4 * 60000);
  await page.fill("#ses-gist", "copy a known product, but for a narrow group it fails");
  await page.click('[data-action="ses-done1"]'); await page.clock.runFor(3000);
  check(`${w} Done stops the clock`, !(await page.$(".now-active")) && /Part 1 done ✓/.test(await txt(page, "#toast")), await txt(page, "#toast"));
  check(`${w} the day plan counts it done, early`, /✓ done · \d+ min/.test(await tile(page, "FIRE plan")), await tile(page, "FIRE plan"));
  let st = await lastState(page), t = st && st.tasks.find(x => x.id === "lesson_goal_fire_F01");
  check(`${w} saved: part 1 done today, with the one line`, t && t.p1 === "2026-11-18" && (t.fin || []).includes("2026-11-18") && t.study.slice(-1)[0].gist === "copy a known product, but for a narrow group it fails", JSON.stringify(t && { p1: t.p1, fin: t.fin }));
  check(`${w} no sideways scroll (day 1)`, await noHScroll(page));
  fs.writeFileSync(TMP, (await page.evaluate(() => window.__pub[window.__pub.length - 1])));
  check(`${w} no errors (day 1)`, errors.length === 0, errors.join(" | "));
  await ctx.close();

  // day 2: part 2 of the same lesson
  ({ page, errors, ctx } = await openPage(browser, { width: w, time: D2, file: TMP }));
  check(`${w} next day the plan is open again`, !/✓/.test(await tile(page, "FIRE plan")), await tile(page, "FIRE plan"));
  await start(page, "goal_fire", "F01");
  brief = await txt(page, ".ses-brief");
  check(`${w} part 2 says what it is`, /Part 2 of 2: do it/.test(brief), brief.slice(0, 300));
  const pills = await txt(page, ".ses-pills");
  check(`${w} part 2 has recall, write, check`, /1 Recall/.test(pills) && /2 Write/.test(pills) && /3 Check/.test(pills) && !/Learn/.test(pills), pills);
  await page.fill("#ses-guess", "narrow group, known product");
  await page.click('.dec-nav [data-i="2"]'); await page.clock.runFor(40);
  check(`${w} Write can open the idea again`, /Stuck\? Open the idea/.test(await txt(page, ".ses-back summary")));
  await page.fill("#ses-answer", "1 to n");
  await page.click('.dec-nav [data-i="3"]'); await page.clock.runFor(40);
  const chk = await txt(page, ".ses");
  check(`${w} Check shows part 1's one line`, /Part 1, in one line/i.test(chk) && /narrow group it fails/.test(chk), chk.slice(0, 400));
  await page.click('[data-action="cur-nailed"] >> nth=0'); await page.clock.runFor(3000);
  st = await lastState(page); t = st && st.tasks.find(x => x.id === "lesson_goal_fire_F01");
  check(`${w} nailed: lesson done, day counted`, st && st.goals.find(g => g.id === "goal_fire").curr.done.F01 === true && (t.fin || []).includes("2026-11-19"));
  check(`${w} the day plan shows it done`, /✓/.test(await tile(page, "FIRE plan")), await tile(page, "FIRE plan"));
  check(`${w} no errors (day 2)`, errors.length === 0, errors.join(" | "));
  await ctx.close();

  // a lesson begun before parts worked this way, with most of its time logged: it goes straight to part 2
  ({ page, errors, ctx } = await openPage(browser, { width: w, time: D1 }));
  await start(page, "goal_invest", "L01");
  check(`${w} the 88-minute lesson is at part 2`, /Part 2 of 2: do it/.test(await txt(page, ".ses-brief")), (await txt(page, ".ses-brief")).slice(0, 200));
  // going on to part 2 the same day
  await page.click('[data-action="stop"]').catch(() => {}); await page.clock.runFor(40);
  await start(page, "goal_biz", "B01");
  await page.click('.dec-nav [data-i="1"]'); await page.clock.runFor(40);
  await page.click('[data-action="ses-go2"]'); await page.clock.runFor(60);
  const s2 = await txt(page, ".ses");
  check(`${w} go on to part 2: write step, clock still running`, !!(await page.$("#ses-answer")) && /Part 2 of 2/.test(s2) && !!(await page.$(".now-active")), s2.slice(0, 200));
  check(`${w} going on counts the day`, /✓/.test(await tile(page, "Business")), await tile(page, "Business"));
  await page.click('.dec-nav [data-i="3"]'); await page.clock.runFor(40);
  await page.click('.curr-btns [data-action="ses-stop"]'); await page.clock.runFor(3000);
  check(`${w} not yet: stops the clock, counted`, !(await page.$(".now-active")) && /Counted for today ✓/.test(await txt(page, "#toast")), await txt(page, "#toast"));
  check(`${w} no errors (old lesson, go on)`, errors.length === 0, errors.join(" | "));
  await ctx.close();

  // a weekend: the slot is longer, so the whole lesson fits one sitting with all four steps
  ({ page, errors, ctx } = await openPage(browser, { width: w, time: SAT }));
  await start(page, "goal_biz", "B01");
  const wk = await txt(page, ".ses-pills");
  check(`${w} weekend: one sitting, four steps`, /1 Guess/.test(wk) && /4 Check/.test(wk) && !/Part \d of 2/.test(await txt(page, ".ses-brief")), wk);
  check(`${w} no errors (weekend)`, errors.length === 0, errors.join(" | "));
  await ctx.close();
}
// a big lesson (L33, about 120 minutes): part 2 carries over, a sitting at a time, and shows where you stopped
{
  const D3 = new Date(2026, 10, 20, 17, 0).getTime();
  let { page, errors, ctx } = await openPage(browser, { width: 402, time: D1 });
  await start(page, "goal_invest", "L33");
  await page.click('.dec-nav [data-i="1"]'); await page.clock.runFor(40);
  await page.click('[data-action="ses-done1"]'); await page.clock.runFor(3000);
  fs.writeFileSync(TMP, (await page.evaluate(() => window.__pub[window.__pub.length - 1])));
  await ctx.close();
  ({ page, errors, ctx } = await openPage(browser, { width: 402, time: D2, file: TMP }));
  await start(page, "goal_invest", "L33");
  const brief = await txt(page, ".ses-brief");
  check("L33 part 2 says it's a big one", /Part 2 of 2: do it/.test(brief) && /a big one, about 120 minutes/.test(brief) && /keeps your place/.test(brief), brief.slice(0, 400));
  await page.click('.dec-nav [data-i="2"]'); await page.clock.runFor(40);
  await page.fill("#ses-answer", "Picked ASML; story written, revenue growth next");
  await page.click('.dec-nav [data-i="3"]'); await page.clock.runFor(40);
  await page.click('.curr-btns [data-action="ses-stop"]'); await page.clock.runFor(3000);
  check("L33 not yet: counted, the clock stopped", !(await page.$(".now-active")) && /Counted for today ✓/.test(await txt(page, "#toast")));
  fs.writeFileSync(TMP, (await page.evaluate(() => window.__pub[window.__pub.length - 1])));
  check("no errors (L33 day 2)", errors.length === 0, errors.join(" | "));
  await ctx.close();
  ({ page, errors, ctx } = await openPage(browser, { width: 402, time: D3, file: TMP }));
  await start(page, "goal_invest", "L33");
  check("L33 day 3: still part 2", /Part 2 of 2/.test(await txt(page, ".ses-brief")));
  await page.click('.dec-nav [data-i="2"]'); await page.clock.runFor(40);
  const prev = await txt(page, ".ses-prev");
  check("L33 day 3: Write shows where you stopped", /Where you stopped last time/.test(prev) && /Picked ASML/.test(prev), prev);
  check("no errors (L33 day 3)", errors.length === 0, errors.join(" | "));
  await ctx.close();
}
try { fs.unlinkSync(TMP); } catch (e) {}
await browser.close();
process.exit(summary("parts in two") ? 1 : 0);
