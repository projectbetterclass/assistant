// every investing lesson's Learn step: the thread line, L01's walk-through, the box named the same in Learn and Write
import { launch, openPage, check, summary, noHScroll, toStep, SAT } from "./harness.mjs";
const browser = await launch();
const txt = (p, s) => p.$eval(s, e => e.innerText.replace(/\s+/g, " ").trim()).catch(() => "");
const ids = Array.from({ length: 34 }, (_, i) => "L" + String(i + 1).padStart(2, "0"));
for (const w of [402, 900]) {
  const o = await openPage(browser, { width: w, time: SAT });
  const { page, errors } = o;
  for (const lid of ids) {
    await page.evaluate(id => { const b = document.createElement("button"); b.setAttribute("data-action", "cur-start"); b.setAttribute("data-id", "goal_invest"); b.setAttribute("data-lid", id); document.getElementById("root").appendChild(b); b.click(); }, lid);
    await page.clock.runFor(80);
    await toStep(page, 1);
    const th = await txt(page, ".ses-thread");
    check(`${w} ${lid} thread`, (lid === "L01" ? /Starts here the first lesson/i.test(th) : /Builds on L\d\d/i.test(th)) && /Leads to/i.test(th), th);
    if (lid !== "L01") check(`${w} ${lid} thread names an earlier lesson only`, (/Builds on (L\d\d)/i.exec(th) || [])[1] < lid, th);
    const walk = await page.$$eval(".ses-walk .walk-s", s => s.length).catch(() => 0);
    const n = +lid.slice(1);
    const rd = await page.$$eval(".ses .ses-teach, .ses .ses-walk", es => es.map(e => e.innerText).join(" "));
    check(`${w} ${lid} the reading keeps to its own lesson`, !((rd.match(/\b[A-Z]\d\d\b/g) || []).some(x => x !== lid)), (rd.match(/.{0,60}\b[A-Z]\d\d\b.{0,30}/) || [""])[0]);
    check(`${w} ${lid} walk-through`, n <= 14 ? walk >= (lid === "L01" ? 3 : 4) : walk === 0, walk);   // L01 keeps to routing; the course map is in the overview
    if (n >= 2 && n <= 14) {
      const wt = await txt(page, ".ses-walk");
      check(`${w} ${lid} walk: his worked example, sourced, then your turn on KO`, /Worked: his/i.test(wt) && /Your turn: KO/i.test(wt) && await page.$$eval(".ses-walk .walk-src a[href^='https://']", a => a.length) >= 1, wt.slice(0, 160));
      check(`${w} ${lid} idea is short now`, (await txt(page, ".ses-teach")).split(/\s+/).length < 70);
    }
    if (lid === "L01") {
      const wt = await txt(page, ".ses-walk");
      check(`${w} L01 walk: the four parts in a line, no pointers`, /the cash the business makes today, what it must reinvest to grow, how fast that cash grows, and a discount rate/i.test(wt) && !/\bL\d\d\b/.test(wt) && /Worked: KO/i.test(wt) && /\$47\.9 billion/.test(wt) && /about 4% of revenue/.test(wt), wt.slice(0, 200));
      check(`${w} L01 order: thread, idea, walk, numbers`, await page.evaluate(() => { const q = s => document.querySelector(".ses " + s); const a = [q(".ses-thread"), q(".ses-teach"), q(".ses-walk"), q(".need")]; return a.every(Boolean) && a.every((e, i) => !i || (a[i - 1].compareDocumentPosition(e) & 4)); }));
    }
    check(`${w} ${lid} Learn box named What you need`, !(await page.$(".need")) || /What you need/i.test(await txt(page, ".need .need-h")));
    check(`${w} ${lid} no sideways scroll`, await noHScroll(page));
    await toStep(page, 2);
    const wb = await txt(page, ".need-sm .need-h");
    check(`${w} ${lid} Write box named the same`, !(await page.$(".need-sm")) || /What you need/i.test(wb), wb);
    check(`${w} ${lid} no 'Your inputs'`, !/Your inputs/i.test(await txt(page, ".ses")));
    await page.evaluate(() => { const b = document.querySelector("[data-action=ses-stop]"); b && b.click(); }); await page.clock.runFor(80);
  }
  check(`${w} no errors`, errors.length === 0, errors);
  await o.ctx.close();
}
await browser.close();
process.exit(summary("learn") ? 1 : 0);
