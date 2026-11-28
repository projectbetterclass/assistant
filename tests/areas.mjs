// the Now page as the four open areas: FIRE, business, reading and trading. Each shows a result, one weekly lever with
// its aim and last four weeks, and the next step from its plan; the one furthest behind is "improve this week".
// Every lever is recorded by the app itself (time from the clocks; book actions from the sittings): nothing to fill in.
// The lesson cards live on the Lessons tab.
import { launch, openPage, check, summary, noHScroll } from "./harness.mjs";
const browser = await launch();
const T = new Date(2026, 10, 27, 19, 30).getTime();   // Friday 27 November
const txt = (p, s) => p.$eval(s, e => e.innerText.replace(/\s+/g, " ").trim()).catch(() => "");
const card = (p, name) => p.$$eval(".ar-card", (es, n) => { const e = es.find(x => x.querySelector(".ar-name").innerText.trim() === n); return e ? e.innerText.replace(/\s+/g, " ").trim() : ""; }, name);
const start = async (page, gid, lid) => { await page.evaluate(({ gid, lid }) => { const b = document.createElement("button"); b.setAttribute("data-action", "cur-start"); b.setAttribute("data-id", gid); b.setAttribute("data-lid", lid); document.getElementById("root").appendChild(b); b.click(); }, { gid, lid }); await page.clock.runFor(80); };
const toNow = async page => { await page.click('.tabbar [data-view="lessons"]'); await page.clock.runFor(40); await page.click('.tabbar [data-view="now"]'); await page.clock.runFor(60); };
for (const w of [402, 1280]) {
  const { page, errors, ctx } = await openPage(browser, { width: w, time: T, view: "now", dsf: w === 1280 ? 2 : 1 });
  const names = await page.$$eval(".ar-card .ar-name", es => es.map(e => e.innerText.trim()));
  check(`${w} four open areas`, names.join("|") === "FIRE plan|Business: AI service|Reading|Trading", names.join(" | "));
  const tabs = await page.$$eval(".tabbar .tab-lbl", es => es.map(e => e.innerText.trim()));
  check(`${w} tabs: Now, Lessons, Goals, Projects, Review`, tabs.join("|") === "Now|Lessons|Goals|Projects|Review", tabs.join(" | "));
  check(`${w} no weekly check-in to fill in`, !(await page.$(".ck")) && !(await page.$("#ck-inv")));
  const imp = await txt(page, ".ar-imp");
  check(`${w} improve this week: FIRE, nothing invested`, /Improve this week · FIRE plan/i.test(imp) && /Nothing is invested yet/.test(imp) && /set up an automatic monthly transfer/.test(imp) && /Open the FIRE plan/.test(imp), imp);
  const fire = await card(page, "FIRE plan");
  check(`${w} FIRE: result, time this week against the day plan, next step with this month's spending`, /Invested, of your €1\.5M number €0/.test(fire) && /Time on it this week 0m of 1h 10m/.test(fire) && /from your clocks/.test(fire) && /Set up an automatic monthly transfer\. €172 of this month’s spending is logged/.test(fire) && /not started/.test(fire), fire);
  const biz = await card(page, "Business: AI service");
  check(`${w} business: the plan's step, time this week, the first open action`, /Your plan step 1 of 4/.test(biz) && /Time on it this week 0m of 1h 10m/.test(biz) && /Next step: Pick my two niches.*\(Discover\)/.test(biz) && /behind/.test(biz), biz);
  const bizBars = await page.$$eval(".ar-card:nth-child(2) .ar-wb i", es => es.map(e => e.style.height));
  check(`${w} business bars: the 5 minutes in the week of 16 November show`, bizBars[2] !== "0%" && bizBars[3] === "0%", bizBars.join(","));
  const rd = await card(page, "Reading");
  check(`${w} reading: the book you're in, every book on the shelf, time against 20 minutes a day`, /Atomic Habits chapter note 1 of 7/.test(rd) && /Your books · 0 of 8 finished/i.test(rd) && /Time on it this week 0m of 2h 20m/.test(rd) && /Next step: Atomic Habits, Intro–Ch\. 1: “Tiny gains compound/.test(rd) && /behind/.test(rd) && !/After I/.test(rd), rd);
  const shelf = await page.$$eval(".ar-book", es => es.map(e => e.querySelector(".ar-bn").innerText + " " + e.querySelector(".ar-bc").innerText + (e.classList.contains("is-cur") ? " *" : "")));
  check(`${w} the shelf: eight books in reading order, Atomic Habits marked as current`, shelf.length === 8 && shelf[0] === "Atomic Habits 0/7 *" && shelf[1] === "Eat That Frog! 0/8" && shelf[7] === "$100M Money Models 0/7", shelf.join(" | "));
  const tr = await card(page, "Trading");
  check(`${w} trading: demo account and the first rule`, /Demo account not opened yet/.test(tr) && /Time on it this week 0m of 1h 10m/.test(tr) && /Next step: Rules before real money\./.test(tr) && /not started/.test(tr), tr);
  check(`${w} the lessons line`, /Today’s lessons: 0 of 7 done/.test(await txt(page, ".ar-les")), await txt(page, ".ar-les"));
  check(`${w} no sideways scroll`, await noHScroll(page));
  if (w === 1280) await page.screenshot({ path: new URL("./areas-1280.png", import.meta.url).pathname, fullPage: true });
  // half an hour on the FIRE plan: its lever moves, and the business becomes the one to improve
  await start(page, "goal_fire", "F01"); await page.clock.fastForward(30 * 60 * 1000); await toNow(page);
  const fire2 = await card(page, "FIRE plan");
  check(`${w} time on FIRE counts, a running clock included`, /Time on it this week 3\dm of 1h 10m/.test(fire2) && /behind/.test(fire2), fire2);
  check(`${w} the lessons line says a clock is running`, /A clock is running/.test(await txt(page, ".ar-les")), await txt(page, ".ar-les"));
  const imp2 = await txt(page, ".ar-imp");
  check(`${w} with FIRE moving, the business is now the one to improve`, /Improve this week · Business: AI service/i.test(imp2) && /No time on the business this week/.test(imp2) && /Pick my two niches/.test(imp2), imp2);
  const fireBar = await page.$$eval(".ar-card:first-child .ar-wb i", es => es.map(e => e.style.height));
  check(`${w} this week's FIRE bar shows it`, fireBar[3] !== "0%", fireBar.join(","));
  // the lesson cards are one tap away
  await page.click(".ar-les"); await page.clock.runFor(60);
  check(`${w} Lessons holds the cards and the running sitting`, (await page.$$(".nowc-card")).length >= 6 && !!(await page.$(".now-active")));
  check(`${w} no errors`, errors.length === 0, errors.join(" | "));
  await ctx.close();
}
await browser.close();
process.exit(summary("open areas") ? 1 : 0);
