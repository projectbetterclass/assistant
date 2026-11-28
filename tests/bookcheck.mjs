// the books as daily sittings: the home card, a chapter sitting, tomorrow's action, and "did you do it?" at the next one
import { launch, openPage, check, summary, noHScroll, lastPub, toStep } from "./harness.mjs";
const browser = await launch();
const T = new Date(2026, 10, 15, 18, 30).getTime();
const txt = (p, s) => p.$eval(s, e => e.innerText.replace(/\s+/g, " ").trim()).catch(() => "");
for (const w of [402, 900]) {
  const { page, errors, ctx } = await openPage(browser, { width: w, time: T });
  const card = await txt(page, '.nowc-card[data-gid="goal_read"]');
  check(`${w} home card names the book and chapter`, /Atomic Habits · chapter note 1 of 7/.test(card) && /Tiny gains compound/.test(card), card.slice(0, 160));
  check(`${w} home card says when`, /After I get home · (\d+ of )?\d+ min/i.test(card), card.slice(0, 60));
  await page.click('.nowc-card[data-gid="goal_read"] [data-action="cur-start"]'); await page.clock.runFor(80);
  const ses = await txt(page, ".ses"), now = await txt(page, ".now-active");
  check(`${w} the sitting is the chapter`, /A01 · Tiny gains compound/.test(now) && /on Atomic Habits/.test(ses), now.slice(0, 160));
  check(`${w} no action to check yet`, !(await page.$(".act-box")));
  check(`${w} its card says it\u2019s running, with Stop`, /Running now/i.test(await txt(page, '.nowc-card[data-gid="goal_read"]')) && !!(await page.$('.nowc-card[data-gid="goal_read"] [data-action="stop"]')));
  for (const i of [1, 2, 3]) await toStep(page, i);
  const chk = await txt(page, ".ses");
  check(`${w} check step asks for tomorrow's action`, /Your one action for tomorrow/.test(chk) && /The chapter in short/.test(chk), chk.slice(-300));
  await page.fill("#ses-confuse", "After I get home, I will read two pages");
  await page.click('[data-action="cur-nailed"] >> nth=0'); await page.clock.runFor(200);
  const card2 = await txt(page, '.nowc-card[data-gid="goal_read"]');
  check(`${w} next chapter, with last time's action`, /chapter note 2 of 7/.test(card2) && /Last time’s action: “After I get home, I will read two pages”/.test(card2), card2.slice(0, 220));
  await page.click('.nowc-card[data-gid="goal_read"] [data-action="cur-start"]'); await page.clock.runFor(80);
  check(`${w} the next sitting asks: did you do it?`, /Did you do it\?/.test(await txt(page, ".act-box")));
  await page.fill("#ses-guess", "a guess typed before answering");
  await page.click('[data-action="act-did"][data-v="1"]'); await page.clock.runFor(2000);
  check(`${w} yes is recorded`, /✓ Done/.test(await txt(page, ".act-box")));
  check(`${w} the guess typed before stays`, (await page.$eval("#ses-guess", e => e.value)) === "a guess typed before answering");
  const st = await page.evaluate(() => { const h = window.__pub[window.__pub.length - 1] || ""; const m = h.match(/<script id="app-state"[^>]*>([\s\S]*?)<\/script>/); return m ? JSON.parse(m[1]).goals.find(g => g.id === "goal_read").curr : null; });
  check(`${w} saved: the action, done, counted`, st && st.carry && st.carry.did === true && st.acts && st.acts.yes === 1, JSON.stringify(st && st.carry));
  check(`${w} no sideways scroll`, await noHScroll(page));
  check(`${w} no errors`, errors.length === 0, errors.join(" | "));
  if (w === 402) await (await page.$(".ses")).screenshot({ path: new URL("./book-402.png", import.meta.url).pathname });
  await ctx.close();
}
// made for the audiobook: part 1 is guess, then listen with the chapter's map; the written note is folded away
const start = async (page, lid) => { await page.evaluate(lid => { const b = document.createElement("button"); b.setAttribute("data-action", "cur-start"); b.setAttribute("data-id", "goal_read"); b.setAttribute("data-lid", lid); document.getElementById("root").appendChild(b); b.click(); }, lid); await page.clock.runFor(80); };
for (const w of [402, 900]) {
  const { page, errors, ctx } = await openPage(browser, { width: w, time: new Date(2026, 10, 18, 18, 30).getTime() });
  await start(page, "A01");
  check(`${w} part 1 is listening`, /Part 1 of 2: listen/.test(await txt(page, ".ses-brief")) && /2 Listen/.test(await txt(page, ".ses-pills")), await txt(page, ".ses-pills"));
  await toStep(page, 1);
  const lw = await txt(page, ".ses-walk");
  check(`${w} the map, what to listen for, how to listen`, /The map, before you press play/.test(lw) && /Listen for/.test(lw) && /How to listen/.test(lw) && /Pause after each big idea/.test(lw), lw.slice(0, 300));
  check(`${w} the note is folded away`, (await page.$eval(".walk-fold", d => !d.open).catch(() => false)) && /Can’t listen now\?/.test(lw));
  check(`${w} the idea waits for the check`, !(await page.$(".ses .ses-teach")));
  await page.click(".walk-fold > summary"); await page.clock.runFor(30);
  check(`${w} the note opens`, (await page.$eval(".walk-fold", d => d.open)) && /The idea worth keeping/.test(await txt(page, ".walk-fold")));
  await page.click('[data-action="stop"]').catch(() => {}); await page.clock.runFor(60);
  // a Zero to One chapter that used to be a Building products lesson: use it on your idea
  await start(page, "Z01");
  const zb = await txt(page, ".ses-brief");
  check(`${w} Z01 asks you to use it on your idea`, /Listen to Preface–Ch\. 2/.test(zb) && /0-to-1 or a 1-to-n idea/.test(zb), zb.slice(0, 300));
  await toStep(page, 1);
  const zw = await txt(page, ".ses-walk");
  check(`${w} Z01 carries the worked example`, /Worked: an app like Intensity Applied/.test(zw) && !/\bP\d\d\b/.test(zw), zw.slice(-300));
  await toStep(page, 3);
  check(`${w} Z01 check: a good answer, then the chapter`, /A good answer looks like/i.test(await txt(page, ".ses .hkey")) && /The chapter in short/i.test(await txt(page, ".ses .hkey")));
  check(`${w} no sideways scroll (listening)`, await noHScroll(page));
  check(`${w} no errors (listening)`, errors.length === 0, errors.join(" | "));
  await ctx.close();
}
// listened away from the app (a podcast on a walk): today's minutes count, a second entry replaces the first, and Done keeps them
{
  const { page, errors, ctx } = await openPage(browser, { width: 402, time: new Date(2026, 10, 18, 18, 30).getTime() });
  const tile = name => page.$$eval(".nowc-card", (els, name) => { const e = els.find(x => x.dataset.name === name); return e ? e.querySelector(".nowc-m").innerText.replace(/\s+/g, " ") : ""; }, name);
  const lastState = () => page.evaluate(() => { const h = window.__pub[window.__pub.length - 1] || ""; const m = h.match(/<script id="app-state"[^>]*>([\s\S]*?)<\/script>/); return m ? JSON.parse(m[1]) : null; });
  await start(page, "A01"); await toStep(page, 1);
  check("the Listen step has the minutes box", /Listened away from the app/.test(await txt(page, ".ses-away")), await txt(page, ".ses-away"));
  await page.fill("#ses-away", "32"); await page.click('[data-action="ses-away"]'); await page.clock.runFor(1500);
  check("32 minutes added", /32 min listened away ✓/.test(await txt(page, ".ses-away")) && /32 min listened away/.test(await txt(page, "#toast")), await txt(page, ".ses-away"));
  await page.fill("#ses-away", "30"); await page.click('[data-action="ses-away"]'); await page.clock.runFor(1500);
  const st = await lastState(), t = st && st.tasks.find(x => x.id === "lesson_goal_read_A01"), aw = ((t && t.sessions) || []).filter(s => s.away);
  const first = ((t && t.sessions) || []).filter(s => !s.away).map(s => s.start).sort()[0];
  check("saved: one entry of 30 minutes, just before the sitting", aw.length === 1 && aw[0].end - aw[0].start === 30 * 60000 && aw[0].end <= first && aw[0].away === "2026-11-18", JSON.stringify(aw));
  await page.click('[data-action="ses-done1"]'); await page.clock.runFor(3000);
  check("Done: the day plan counts the minutes", /✓\D*3\d\b/.test(await tile("Reading")), await tile("Reading"));
  check("no errors (listened away)", errors.length === 0, errors.join(" | "));
  await ctx.close();
}
// $100M Offers is free as podcast parts, not chapters: each sitting names the part to play and where to find it
{
  const { page, errors, ctx } = await openPage(browser, { width: 402, time: new Date(2026, 10, 18, 18, 30).getTime() });
  await start(page, "O02");
  check("O02 names the podcast part", /Listen to \$100M Offers Audiobook Part 2 \(episode 580\), from 16:37 to 42:18/.test(await txt(page, ".ses-brief")), (await txt(page, ".ses-brief")).slice(0, 300));
  await toStep(page, 1);
  check("O02 says where to find it", /search “\$100M Offers Audiobook Part 2”/.test(await txt(page, ".ses-walk")), (await txt(page, ".ses-walk")).slice(-300));
  check("no errors (Offers)", errors.length === 0, errors.join(" | "));
  await ctx.close();
}
// the course map lists the books still to come, with where to listen for free
{
  const { page, errors, ctx } = await openPage(browser, { width: 402, time: new Date(2026, 10, 18, 18, 30).getTime() });
  await page.evaluate(() => { const b = document.createElement("button"); b.setAttribute("data-action", "cv-open"); b.setAttribute("data-id", "goal_read"); document.getElementById("root").appendChild(b); b.click(); });
  await page.clock.runFor(80);
  check("Next on your shelf is gone: every book on the list has its chapter notes", (await page.$$(".cv-soon")).length === 0 && /Eat That Frog!/.test(await txt(page, ".cv")) && /The Richest Man in Babylon/.test(await txt(page, ".cv")), (await txt(page, ".cv")).slice(0, 300));
  check("$100M Leads is a book in the course, 11 chapter notes", (await page.$$eval(".cv-rung", rs => { const r = rs.find(x => /\$100M Leads/.test(x.innerText)); return r ? r.querySelectorAll("[data-lid^=G], .lesson-row, li").length : 0; })) >= 11 || /\$100M Leads[\s\S]*0\/11/.test(await txt(page, ".cv")), (await txt(page, ".cv")).slice(0, 200));
  check("no sideways scroll (course map)", await noHScroll(page));
  check("no errors (course map)", errors.length === 0, errors.join(" | "));
  await ctx.close();
}
// $100M Leads: each sitting names its own podcast part
{
  const { page, errors, ctx } = await openPage(browser, { width: 402, time: new Date(2026, 10, 18, 18, 30).getTime() });
  await start(page, "G03");
  check("G03 names its podcast part", /Listen to \$100M Leads Audiobook Part 3 \(episode 588\)/.test(await txt(page, ".ses-brief")), (await txt(page, ".ses-brief")).slice(0, 300));
  await toStep(page, 1);
  const gw = await txt(page, ".ses-walk");
  check("G03 map and where to find it", /Warm outreach in ten steps/.test(gw) && /search “\$100M Leads Audiobook Part 3”/.test(gw), gw.slice(0, 300));
  check("no errors (Leads)", errors.length === 0, errors.join(" | "));
  await ctx.close();
}
// $100M Money Models: each sitting names its own podcast part
{
  const { page, errors, ctx } = await openPage(browser, { width: 402, time: new Date(2026, 10, 18, 18, 30).getTime() });
  await start(page, "W04");
  check("W04 names its podcast part", /Listen to \$100M Money Models Audiobook Part 5 \(episode 942\)/.test(await txt(page, ".ses-brief")), (await txt(page, ".ses-brief")).slice(0, 300));
  await toStep(page, 1);
  const ww = await txt(page, ".ses-walk");
  check("W04 map and where to find it", /Why upsells make the money/.test(ww) && /search “\$100M Money Models Audiobook Part 5”/.test(ww), ww.slice(0, 300));
  check("no errors (Money Models)", errors.length === 0, errors.join(" | "));
  await ctx.close();
}
// Eat That Frog! and The Richest Man in Babylon: the sitting names the chapters to play in the audiobook
{
  const { page, errors, ctx } = await openPage(browser, { width: 402, time: new Date(2026, 10, 18, 18, 30).getTime() });
  await start(page, "E03");
  check("E03 names its chapters", /Listen to Ch. 4–6 of the audiobook/.test(await txt(page, ".ses-brief")), (await txt(page, ".ses-brief")).slice(0, 300));
  await toStep(page, 1);
  check("E03 map", /The ABCDE method/.test(await txt(page, ".ses-walk")), (await txt(page, ".ses-walk")).slice(0, 300));
  await ctx.close();
  const b = await openPage(browser, { width: 402, time: new Date(2026, 10, 18, 18, 30).getTime() });
  await start(b.page, "Y04");
  check("Y04 names its chapter", /Listen to Ch. 5 of the audiobook/.test(await txt(b.page, ".ses-brief")), (await txt(b.page, ".ses-brief")).slice(0, 300));
  await toStep(b.page, 1);
  check("Y04 map", /The five laws/.test(await txt(b.page, ".ses-walk")), (await txt(b.page, ".ses-walk")).slice(0, 300));
  check("no errors (Frog and Babylon)", errors.length === 0 && b.errors.length === 0, errors.concat(b.errors).join(" | "));
  await b.ctx.close();
  // Zero to One's audiobook doesn't announce its chapters, so the sitting says roughly where they start
  const z = await openPage(browser, { width: 402, time: new Date(2026, 10, 18, 18, 30).getTime() });
  await start(z.page, "Z02");
  check("Z02 says where in the audio its chapters start", /Listen to Ch\. 3–4 \(from 0:29:11\) of the audiobook/.test(await txt(z.page, ".ses-brief")), (await txt(z.page, ".ses-brief")).slice(0, 300));
  check("no errors (Zero to One)", z.errors.length === 0, z.errors.join(" | "));
  await z.ctx.close();
}
// Building products has moved into Reading: no course on its goal, and not in the day plan
{
  const { page, errors, ctx } = await openPage(browser, { width: 402, time: new Date(2026, 10, 18, 18, 30).getTime() });
  const names = await page.$$eval(".nowc-card", es => es.map(e => e.dataset.name));
  check("Products is out of the day plan", !names.includes("Products") && names.includes("Reading"), names.join(", "));
  check("no errors (day plan)", errors.length === 0, errors.join(" | "));
  await ctx.close();
}
summary("books"); await browser.close();
