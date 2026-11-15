// the books as daily sittings: the home card, a chapter sitting, tomorrow's action, and "did you do it?" at the next one
import { launch, openPage, check, summary, noHScroll, lastPub } from "./harness.mjs";
const browser = await launch();
const T = new Date(2026, 10, 15, 18, 30).getTime();
const txt = (p, s) => p.$eval(s, e => e.innerText.replace(/\s+/g, " ").trim()).catch(() => "");
for (const w of [402, 900]) {
  const { page, errors, ctx } = await openPage(browser, { width: w, time: T });
  const card = await txt(page, ".home-book");
  check(`${w} home card names the book and chapter`, /Atomic Habits · chapter note 1 of 7/.test(card) && /Tiny gains compound/.test(card), card.slice(0, 160));
  check(`${w} home card says when`, /After I get home · \d+ min/i.test(card), card.slice(0, 60));
  await page.click('.home-book [data-action="cur-start"]'); await page.clock.runFor(80);
  const ses = await txt(page, ".ses"), now = await txt(page, ".now-active");
  check(`${w} the sitting is the chapter`, /A01 · Tiny gains compound/.test(now) && /on Atomic Habits/.test(ses), now.slice(0, 160));
  check(`${w} no action to check yet`, !(await page.$(".act-box")));
  check(`${w} home card hides while the sitting runs`, !(await page.$(".home-book")));
  for (const i of [1, 2, 3]) { await page.click(`.dec-nav [data-i="${i}"]`); await page.clock.runFor(40); }
  const chk = await txt(page, ".ses");
  check(`${w} check step asks for tomorrow's action`, /Your one action for tomorrow/.test(chk) && /The chapter in short/.test(chk), chk.slice(-300));
  await page.fill("#ses-confuse", "After I get home, I will read two pages");
  await page.click('[data-action="cur-nailed"] >> nth=0'); await page.clock.runFor(200);
  const card2 = await txt(page, ".home-book");
  check(`${w} next chapter, with last time's action`, /chapter note 2 of 7/.test(card2) && /Last time’s action: “After I get home, I will read two pages”/.test(card2), card2.slice(0, 220));
  await page.click('.home-book [data-action="cur-start"]'); await page.clock.runFor(80);
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
summary("books"); await browser.close();
