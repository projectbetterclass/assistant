// the Now page as the four open areas: FIRE, business, reading and trading. Each shows a result, one weekly lever with
// its aim and last four weeks, and the next step from its plan; the one furthest behind is "improve this week".
// The weekly check-in records the levers the app can't see. The lesson cards live on the Lessons tab.
import { launch, openPage, check, summary, noHScroll } from "./harness.mjs";
const browser = await launch();
const T = new Date(2026, 10, 27, 19, 30).getTime();   // Friday 27 November
const txt = (p, s) => p.$eval(s, e => e.innerText.replace(/\s+/g, " ").trim()).catch(() => "");
const card = (p, name) => p.$$eval(".ar-card", (es, n) => { const e = es.find(x => x.querySelector(".ar-name").innerText.trim() === n); return e ? e.innerText.replace(/\s+/g, " ").trim() : ""; }, name);
for (const w of [402, 1280]) {
  const { page, errors, ctx } = await openPage(browser, { width: w, time: T, view: "now", dsf: w === 1280 ? 2 : 1 });
  const names = await page.$$eval(".ar-card .ar-name", es => es.map(e => e.innerText.trim()));
  check(`${w} four open areas`, names.join("|") === "FIRE plan|Business: AI service|Reading|Trading", names.join(" | "));
  const tabs = await page.$$eval(".tabbar .tab-lbl", es => es.map(e => e.innerText.trim()));
  check(`${w} tabs: Now, Lessons, Goals, Projects, Review`, tabs.join("|") === "Now|Lessons|Goals|Projects|Review", tabs.join(" | "));
  const imp = await txt(page, ".ar-imp");
  check(`${w} improve this week: FIRE, nothing invested`, /Improve this week · FIRE plan/i.test(imp) && /Nothing is invested yet/.test(imp) && /set up an automatic monthly transfer/.test(imp) && /Open the FIRE plan/.test(imp), imp);
  const fire = await card(page, "FIRE plan");
  check(`${w} FIRE: result, lever, next step with this month's spending`, /Invested, of your €1\.5M number €0/.test(fire) && /Invested this month €0 · aim: a tenth of pay/.test(fire) && /Set up an automatic monthly transfer\. €172 of this month’s spending is logged/.test(fire) && /not started/.test(fire), fire);
  const biz = await card(page, "Business: AI service");
  check(`${w} business: the plan's step and its weekly talks`, /Your plan step 1 of 4/.test(biz) && /Talks with small firms this week 0 of 3/.test(biz) && /Next step: Pick my two niches.*\(Discover\)/.test(biz), biz);
  const rd = await card(page, "Reading");
  check(`${w} reading: books finished, actions counted from sittings, behind (it has time on it)`, /Books finished, of 8 0/.test(rd) && /Book actions done this week 0 of 3/.test(rd) && /counted from your sittings/.test(rd) && /Atomic Habits: “Tiny gains compound/.test(rd) && /behind/.test(rd), rd);
  const tr = await card(page, "Trading");
  check(`${w} trading: demo account and the first rule`, /Demo account not opened yet/.test(tr) && /Next step: Rules before real money\./.test(tr), tr);
  check(`${w} the lessons line`, /Today’s lessons: 0 of 7 done/.test(await txt(page, ".ar-les")), await txt(page, ".ar-les"));
  check(`${w} no sideways scroll`, await noHScroll(page));
  if (w === 1280) await page.screenshot({ path: new URL("./areas-1280.png", import.meta.url).pathname, fullPage: true });
  // the weekly check-in
  await page.fill("#ck-inv", "250"); await page.fill("#ck-talks", "2"); await page.fill("#ck-trades", "1"); await page.fill("#ck-change", "Message three firms on Monday evening");
  await page.click('.ck-form button[type="submit"]'); await page.clock.runFor(100);
  const sum = await txt(page, ".ck");
  check(`${w} check-in saved and summed up`, /saved for this week/.test(sum) && /€250 invested this month/.test(sum) && /2 talks with small firms/.test(sum) && /1 demo trades written up/.test(sum) && /Next week: “Message three firms/.test(sum), sum);
  const saved = await page.evaluate(() => { const h = window.__pub[window.__pub.length - 1] || ""; const m = /<script id="app-state"[^>]*>([\s\S]*?)<\/script>/.exec(h); return m ? JSON.parse(m[1]).checkins : null; });
  check(`${w} the check-in is in the saved state, by the week's Monday`, saved && saved["2026-11-23"] && saved["2026-11-23"].inv === 250 && saved["2026-11-23"].talks === 2 && saved["2026-11-23"].trades === 1, JSON.stringify(saved));
  const imp2 = await txt(page, ".ar-imp");
  check(`${w} with FIRE and business moving, reading is now the one to improve`, /Improve this week · Reading/i.test(imp2) && /No book actions done this week/.test(imp2), imp2);
  check(`${w} FIRE on track once something is invested (no monthly amount set)`, /on track/.test(await card(page, "FIRE plan")) && /Invested this month €250/.test(await card(page, "FIRE plan")));
  check(`${w} business behind at 2 of 3`, /behind/.test(await card(page, "Business: AI service")) && /2 of 3/.test(await card(page, "Business: AI service")));
  const barH = await page.$$eval(".ar-card:first-child .ar-wb i", es => es.map(e => e.style.height));
  check(`${w} this week's bar shows it, the earlier weeks are empty`, barH[3] === "100%" && barH[0] === "0%", barH.join(","));
  await page.click('[data-action="ck-edit"]'); await page.clock.runFor(40);
  check(`${w} edit brings the numbers back`, (await page.inputValue("#ck-inv")) === "250" && (await page.inputValue("#ck-talks")) === "2");
  await page.click('[data-action="ck-cancel"]'); await page.clock.runFor(40);
  // next week: last week's "one thing" comes back
  await page.clock.fastForward(72 * 3600 * 1000); await page.click('.tabbar [data-view="lessons"]'); await page.clock.runFor(60); await page.click('.tabbar [data-view="now"]'); await page.clock.runFor(60);
  const ck2 = await txt(page, ".ck");
  check(`${w} next week: last week's one thing comes back, and the form is empty`, /Last week you said: “Message three firms on Monday evening”/.test(ck2) && (await page.inputValue("#ck-inv")) === "", ck2.slice(0, 200));
  // the lesson cards are one tap away
  await page.click(".ar-les"); await page.clock.runFor(60);
  check(`${w} Lessons holds the cards`, (await page.$$(".nowc-card")).length === 7);
  check(`${w} no errors`, errors.length === 0, errors.join(" | "));
  await ctx.close();
}
await browser.close();
process.exit(summary("open areas") ? 1 : 0);
