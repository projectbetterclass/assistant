// the Now page as cards: one per daily thing, saying what today's sitting is without the lesson itself;
// the next one first, the done ones last, arrows and dots to move along, on a phone and on a PC
import { launch, openPage, check, summary, noHScroll } from "./harness.mjs";
const browser = await launch();
const T = new Date(2026, 10, 26, 17, 30).getTime();   // a Thursday
const txt = (p, s) => p.$eval(s, e => e.innerText.replace(/\s+/g, " ").trim()).catch(() => "");
const start = async (page, gid, lid) => { await page.evaluate(({ gid, lid }) => { const b = document.createElement("button"); b.setAttribute("data-action", "cur-start"); b.setAttribute("data-id", gid); b.setAttribute("data-lid", lid); document.getElementById("root").appendChild(b); b.click(); }, { gid, lid }); await page.clock.runFor(80); };
for (const w of [402, 1280]) {
  const { page, errors, ctx } = await openPage(browser, { width: w, time: T });
  const names = await page.$$eval(".nowc-card", es => es.map(e => e.dataset.name));
  check(`${w} one card per daily thing`, names.length === 7 && names.includes("Reading") && names.includes("Buddha"), names.join(", "));
  check(`${w} the first card is the next one`, /Up next/i.test(await txt(page, ".nowc-card:first-child .nowc-k")) && !!(await page.$(".nowc-card:first-child.is-next")));
  check(`${w} progress line`, /0 of 7 done · 0 of \d+ min/.test(await txt(page, ".nowc-prog")), await txt(page, ".nowc-prog"));
  const fire = await txt(page, '.nowc-card[data-name="FIRE plan"]');
  check(`${w} a lesson card: the lesson, the part, today, the end`, /Your FIRE number/.test(fire) && /F01/.test(fire) && /Part 1 of 2 · learn it/.test(fire) && /Today: Guess first/.test(fire) && /You end with: the idea in one line\. Next time: work out your number/.test(fire), fire);
  check(`${w} no lesson text on the card`, !/The idea\.|walk-s|Worked:/.test(await page.$eval('.nowc-card[data-name="FIRE plan"]', e => e.innerHTML)));
  check(`${w} the timer card`, /Just the timer/.test(await txt(page, '.nowc-card[data-name="Buddha"]')) && !!(await page.$('.nowc-card[data-name="Buddha"] [data-action="round-start"]')));
  check(`${w} the book card`, /chapter note \d+ of \d+/.test(await txt(page, '.nowc-card[data-name="Reading"]')) && /Part 1 of 2 · listen/.test(await txt(page, '.nowc-card[data-name="Reading"]')));
  check(`${w} the old day list and book card are gone`, !(await page.$(".day-list")) && !(await page.$(".home-book")));
  check(`${w} "Something else?" is one line`, !!(await page.$(".now-idle.is-compact form.quick #q-name")) && !(await page.$(".now-idle #q-cat")));
  await page.click('[data-action="cards-move"][data-v="1"]'); await new Promise(r => setTimeout(r, 900)); await page.clock.runFor(100);   // smooth scrolling runs on real time
  const at = await page.evaluate(() => [document.querySelector(".nowc-track").scrollLeft, [...document.querySelectorAll(".nowc-dot")].findIndex(d => d.classList.contains("is-at"))]);
  check(`${w} the arrow moves one card, the dot follows`, at[0] > 100 && at[1] === 1, JSON.stringify(at));
  check(`${w} no sideways scroll`, await noHScroll(page));
  // part 1 done early: that card shows done and goes to the end, and says what's next time
  await start(page, "goal_fire", "F01");
  await page.click('.dec-nav [data-i="1"]'); await page.clock.runFor(40);
  await page.click('[data-action="ses-done1"]'); await page.clock.runFor(3000);
  const last = await page.$eval(".nowc-card:last-child", e => e.dataset.name);
  const fd = await txt(page, '.nowc-card[data-name="FIRE plan"]');
  check(`${w} done goes last, with next time`, last === "FIRE plan" && /✓ done/.test(fd) && /Next time: Your FIRE number.*part 2 of 2/i.test(fd), last + " | " + fd.slice(0, 200));
  check(`${w} progress counts it`, /1 of 7 done/.test(await txt(page, ".nowc-prog")), await txt(page, ".nowc-prog"));
  check(`${w} no errors`, errors.length === 0, errors.join(" | "));
  if (w === 402) await (await page.$(".nowc")).screenshot({ path: new URL("./nowcards-402.png", import.meta.url).pathname });
  await ctx.close();
}
await browser.close();
process.exit(summary("now cards") ? 1 : 0);
