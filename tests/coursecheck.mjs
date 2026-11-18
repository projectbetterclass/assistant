// one course, every lesson: Learn (thread, idea, walk-through, numbers), Write (numbers again), Check (worked answer), revisit (numbers, closed answer)
import { launch, openPage, check, summary, noHScroll, toStep, SAT } from "./harness.mjs";
const [gid, prefix, n, walkFrom = 1, walkTo = 99] = process.argv.slice(2);
const browser = await launch();
const txt = (p, s) => p.$eval(s, e => e.innerText.replace(/\s+/g, " ").trim()).catch(() => "");
const ids = Array.from({ length: +n }, (_, i) => prefix + String(i + 1).padStart(2, "0"));
for (const w of [402, 900]) {
  const o = await openPage(browser, { width: w, time: SAT });
  const { page, errors } = o;
  for (const lid of ids) {
    const k = +lid.slice(1);
    await page.evaluate(({ gid, lid }) => { const b = document.createElement("button"); b.setAttribute("data-action", "cur-start"); b.setAttribute("data-id", gid); b.setAttribute("data-lid", lid); document.getElementById("root").appendChild(b); b.click(); }, { gid, lid });
    await page.clock.runFor(80);
    await toStep(page, 1);
    const th = await txt(page, ".ses-thread");
    check(`${w} ${lid} thread`, (k === 1 ? /Starts here/i.test(th) : /Builds on/i.test(th)) && /Leads to/i.test(th), th);
    if (k >= +walkFrom && k <= +walkTo) {
      const wt = await txt(page, ".ses-walk");
      check(`${w} ${lid} walk-through ends with your turn`, (await page.$$eval(".ses-walk .walk-s", s => s.length)) >= 4 && /Your turn/i.test(wt), wt.slice(0, 120));
    }
    const idea = await txt(page, ".ses-teach");
    check(`${w} ${lid} short idea`, idea.split(/\s+/).length < 75, idea.length);
    const learn = await txt(page, ".ses");
    check(`${w} ${lid} no raw markup or junk`, !/undefined|NaN|\[object|%%|\*\*/.test(learn), (learn.match(/undefined|NaN|\[object|%%|\*\*/) || [])[0]);
    check(`${w} ${lid} no sideways scroll (Learn)`, await noHScroll(page));
    await toStep(page, 2);
    await toStep(page, 3);
    const key = await txt(page, ".ses .hkey");
    check(`${w} ${lid} Check shows the answer`, /Worked answer|A good answer|Check it|Short answer/i.test(key) && key.length > 60, key.slice(0, 120));
    check(`${w} ${lid} no sideways scroll (Check)`, await noHScroll(page));
    await page.evaluate(() => { const b = document.querySelector("[data-action=ses-stop]"); b && b.click(); }); await page.clock.runFor(80);
    await page.evaluate(({ gid, lid }) => { const b = document.createElement("button"); b.setAttribute("data-action", "rev-start"); b.setAttribute("data-id", gid); b.setAttribute("data-lid", lid); document.getElementById("root").appendChild(b); b.click(); }, { gid, lid });
    await page.clock.runFor(80);
    const rv = await txt(page, ".ses-rev");
    check(`${w} ${lid} revisit has its own task and a closed answer`, rv.length > 50 && (await page.$eval(".ses-rev details.rev-key", d => !d.open).catch(() => false)), rv.slice(0, 160));
    check(`${w} ${lid} revisit no junk`, !/undefined|NaN|%%/.test(rv));
    await page.evaluate(() => { const b = document.querySelector("[data-action=ses-stop]"); b && b.click(); }); await page.clock.runFor(80);
  }
  check(`${w} no errors`, errors.length === 0, errors);
  await o.ctx.close();
}
await browser.close();
process.exit(summary(gid) ? 1 : 0);
