// The lesson flows over days: a full sitting graded nailed, its revisit 10 days later; shaky → 3 days; priming; pause mid-sitting; stop for today.
import { launch, openPage, check, summary, lastPub } from "./harness.mjs";
const browser = await launch();
const txt = (p, s) => p.$eval(s, e => e.innerText.replace(/\s+/g, " ").trim()).catch(() => "");
async function startLesson(page, gid, lid) {
  await page.evaluate(({ gid, lid }) => { const b = document.createElement("button"); b.setAttribute("data-action", "cur-start"); b.setAttribute("data-id", gid); b.setAttribute("data-lid", lid); document.getElementById("root").appendChild(b); b.click(); }, { gid, lid });
  await page.clock.runFor(80);
}
// keep the published state between "reloads": load the next page from the last publish, like the real app does
async function carry(o, browser, opts) {
  const h = await o.page.evaluate(() => window.__pub[window.__pub.length - 1]);
  await o.ctx.close();
  const fs = await import("fs"); const f = new URL("./flow-tmp.html", import.meta.url).pathname;
  // the publish is a whole document; the harness serves it as is
  fs.writeFileSync(f, h);
  return openPage(browser, { ...opts, file: f });
}

// 1. a whole sitting, graded nailed; then the revisit 10 days later
{
  let o = await openPage(browser, {});
  let { page, errors } = o;
  await startLesson(page, "goal_invest", "L02");
  check("sitting opens on Guess", /Step 1 of 4 · Guess/i.test(await txt(page, ".ses")));
  await page.fill("#ses-guess", "growth and margin");
  await page.click('.dec-nav [data-i="1"]'); await page.clock.runFor(40);
  await page.click('.dec-nav [data-i="2"]'); await page.clock.runFor(40);
  await page.fill("#ses-answer", "KO sells drinks worldwide through bottlers; the story pins down the target margin.");
  await page.click('.dec-nav [data-i="3"]'); await page.clock.runFor(40);
  const chk = await txt(page, ".ses");
  check("Check shows your guess and your answer", /You guessed\s*growth and margin/i.test(chk) && /You wrote\s*KO sells drinks/i.test(chk), chk.slice(0, 300));
  await page.fill("#ses-confuse", "how the story sets the margin");
  await page.click('[data-action=cur-nailed]'); await page.clock.runFor(80);
  const toast = await txt(page, "#toast");
  check("nailed toast", /comes back once, in 10 days/.test(toast), toast);
  let s = await lastPub(page);
  const g = s.goals.find(x => x.id === "goal_invest");
  check("L02 marked done", g.curr.done.L02 === true);
  check("revisit set for 10 days", g.curr.rev && g.curr.rev.L02 && Math.round((g.curr.rev.L02.due - g.curr.rev.L02.set) / 86400000) === 10, g.curr.rev);
  const t = s.tasks.find(x => x.id === "lesson_goal_invest_L02");
  check("the sitting is saved on the lesson", t && t.study && t.study.at(-1).guess === "growth and margin" && /bottlers/.test(t.study.at(-1).answer));
  check("the open question carries to next time", g.curr.carry && g.curr.carry.q === "how the story sets the margin");
  check("no errors", errors.length === 0, errors);
  // ten days later
  o = await carry(o, browser, { time: new Date(Date.now() + 10 * 86400000 + 3600000) }); ({ page, errors } = o);
  const home = await txt(page, "#root");
  check("home shows the revisit as due", /Revisit due · 5 min · no notes/i.test(home) && /L02 · Narrative before numbers/.test(home), home.slice(0, 400));
  await page.click('.home-next.rev [data-action=rev-start]'); await page.clock.runFor(80);
  const rv = await txt(page, ".ses-rev");
  check("revisit card: new company, no notes", /Revisit · 5 min · no notes/i.test(rv) && /now on /.test(rv), rv.slice(0, 300));
  check("revisit names the company", /now on PEP\b/.test(rv));
  check("revisit task names PepsiCo, not KO", /Tell PepsiCo’s story/.test(rv) && /a PepsiCo valuation/.test(rv) && !/\bKO\b/.test(await txt(page, ".ses-rev .ses-task")), await txt(page, ".ses-rev .ses-task"));
  check("revisit has PepsiCo's own numbers", /Numbers for PEP/i.test(rv) && /PepsiCo/.test(await txt(page, ".ses-rev .need-rev")), (await txt(page, ".ses-rev .need-rev")).slice(0, 300));
  check("revisit has a closed short answer", (await page.$eval(".ses-rev details.rev-key", d => !d.open).catch(() => false)) && /Check your answer \(after you’ve written it\)/i.test(rv));
  check("revisit doesn't say What you need", !/What you need/.test(rv), rv.slice(0, 300));
  await page.fill("#ses-answer", "PEP: snacks plus drinks; story sets growth.");
  await page.click("[data-action=rev-nailed]"); await page.clock.runFor(80);
  s = await lastPub(page);
  const g2 = s.goals.find(x => x.id === "goal_invest");
  check("revisit nailed: off the list", !(g2.curr.rev || {}).L02, g2.curr.rev);
  check("no errors after revisit", errors.length === 0, errors);
  await o.ctx.close();
}

// 2. shaky → back in 3 days, not done
{
  const { page, ctx, errors } = await openPage(browser, {});
  await startLesson(page, "goal_fire", "F01");
  await page.click('.ses-pills [data-i="3"]'); await page.clock.runFor(40);
  await page.click("[data-action=cur-shaky]"); await page.clock.runFor(80);
  const s = await lastPub(page), g = s.goals.find(x => x.id === "goal_fire");
  check("shaky: not done", !g.curr.done || !g.curr.done.F01);
  check("shaky: back in 3 days", g.curr.rev && g.curr.rev.F01 && Math.round((g.curr.rev.F01.due - g.curr.rev.F01.set) / 86400000) === 3, g.curr.rev);
  check("no errors (shaky)", errors.length === 0, errors);
  await ctx.close();
}

// 3. "Not yet — stop for today": clock stops, lesson stays open, notes kept
{
  const { page, ctx, errors } = await openPage(browser, {});
  await startLesson(page, "goal_opt", "H01");
  await page.fill("#ses-guess", "sell the put");
  await page.click('.ses-pills [data-i="3"]'); await page.clock.runFor(40);
  await page.click("[data-action=ses-stop]"); await page.clock.runFor(80);
  const s = await lastPub(page), g = s.goals.find(x => x.id === "goal_opt");
  check("stop for today: clock stopped", !s.activeId);
  check("stop for today: lesson not done", !(g.curr && g.curr.done && g.curr.done.H01));
  check("no errors (stop)", errors.length === 0, errors);
  await ctx.close();
}

// 4. pause in the middle of a sitting, then continue: the step and the notes are still there
{
  const { page, ctx, errors } = await openPage(browser, {});
  await startLesson(page, "goal_read", "R03");
  await page.fill("#ses-guess", "skim first");
  await page.click('.dec-nav [data-i="1"]'); await page.clock.runFor(40);
  await page.click("[data-action=pause]"); await page.clock.runFor(80);
  check("paused card", /Paused/i.test(await txt(page, ".now-paused")));
  await page.clock.runFor(5 * 60000);
  await page.click(".now-paused [data-action=continue]"); await page.clock.runFor(80);
  const ses = await txt(page, ".now-active .ses");
  check("continue: back on Learn", /Step 2 of 4 · Learn/i.test(ses), ses.slice(0, 200));
  await page.click('.ses-pills [data-i="0"]'); await page.clock.runFor(40);
  check("continue: the guess is still there", (await page.$eval("#ses-guess", e => e.value)) === "skim first");
  check("no errors (pause)", errors.length === 0, errors);
  await ctx.close();
}

// 5. priming the night before: the guess waits in the sitting
{
  let o = await openPage(browser, { time: new Date("2026-11-09T21:30:00") });
  let { page, errors } = o;
  const pr = await page.$(".prime-form");
  check("home offers ‘Prime it’", !!pr);
  if (pr) {
    const lid = await page.$eval(".prime-form", f => f.getAttribute("data-lid")), gid = await page.$eval(".prime-form", f => f.getAttribute("data-id"));
    await page.fill("#prime-guess", "my hunch");
    await page.click(".prime-form button[type=submit]"); await page.clock.runFor(80);
    o = await carry(o, browser, { time: new Date("2026-11-10T08:00:00") }); ({ page, errors } = o);
    await startLesson(page, gid, lid);
    check("sitting starts with your primed guess", (await page.$eval("#ses-guess", e => e.value).catch(() => "")) === "my hunch" && /You guessed this ahead/i.test(await txt(page, ".ses")));
  }
  check("no errors (prime)", errors.length === 0, errors);
  await o.ctx.close();
}
await browser.close();
process.exit(summary("flows") ? 1 : 0);
