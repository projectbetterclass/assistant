// rule numbers in a lesson's task open their card under it; ranges are expanded; each lesson's call opens the right card
import { launch, openPage, check, summary, noHScroll } from "./harness.mjs";
const browser = await launch();
const txt = (p, s) => p.$eval(s, e => e.innerText.replace(/\s+/g, " ").trim()).catch(() => "");
const o = await openPage(browser, { width: 402, height: 900, view: "curriculum" });
const { page, errors } = o;
await page.evaluate(() => { localStorage.setItem("wmtw_cv_goal", "goal_invest"); localStorage.setItem("wmtw_cv_mode", "list"); });
await page.reload(); await page.waitForSelector(".top"); await page.clock.runFor(100);
let tapped = 0;
const want = { L10: ["NVDA", "Jan 2025"], L12: ["GOOG", "2018"], L14: ["GOOG", "2018"], L18: ["NVDA", "Jan 2025"], L19: ["NVDA", "Jan 2025"], L20: ["NVDA", "Jan 2025"], L21: ["NVDA", "Jan 2025"], L27: ["NVDA", "Jan 2025"], L29: ["NVDA", "Jan 2025"], L01: ["INTC", "2024"], L02: ["TSLA", "Feb 2020"] };
for (let n = 1; n <= 34; n++) {
  const lid = "L" + String(n).padStart(2, "0");
  await page.click(`[data-action=cur-open][data-id="${lid}"]`); await page.clock.runFor(40);
  const ME = `.ls:has(> .ls-row [data-action=cur-open][data-id="${lid}"])`;
  const copies = await page.$$eval(ME, e => e.length);
  const task = await txt(page, ME + " .ls-det .curr-task");
  const refs = await page.$$eval(ME + " .ls-det .curr-task .dref", b => b.map(x => x.getAttribute("data-k")));
  const raw = (task.match(/D-\d\d/g) || []);
  check(lid + " every rule number in the task is a button", raw.length * copies === refs.length, { raw, refs, copies });
  check(lid + " no unexpanded range left", !/D-\d\d\s*[–-]\s*D-\d\d/.test(task), task);
  for (const k of refs.slice(0, 3)) {
    await page.click(`${ME} .ls-det .curr-task .dref[data-k="${k}"]`); await page.clock.runFor(30);
    const body = await txt(page, ME + " .ls-det .ref-pop .doc-body");
    check(`${lid} ${k} opens its card under the task`, body.length > 80 && /The rule/i.test(body), body.slice(0, 80));
    check(`${lid} ${k} button shows it is open`, await page.$eval(`${ME} .ls-det .curr-task .dref[data-k="${k}"]`, b => b.classList.contains("on") && b.getAttribute("aria-expanded") === "true"));
    check(`${lid} ${k} no sideways scroll`, await noHScroll(page));
    await page.click(`${ME} .ls-det .curr-task .dref[data-k="${k}"]`); await page.clock.runFor(30);
    check(`${lid} ${k} tapping again closes it`, !(await page.$(ME + " .ls-det .ref-pop")));
    tapped++;
  }
  const chips = await page.$$eval(ME + " .ls-det .curr-tags .dref", b => b.length);
  const chipsAll = await page.$$eval(ME + " .ls-det .curr-tags .curr-tag", b => b.length);
  check(lid + " rule chips are buttons", chips === chipsAll, { chips, chipsAll });
  if (want[lid]) {
    const cb = await txt(page, ME + " .ls-det .curr-call");
    check(`${lid} call button names ${want[lid].join(" ")}`, cb.includes(want[lid][0]) && cb.includes("(" + want[lid][1] + ")") && !/NVDA25/.test(cb), cb);
  }
  await page.click(`[data-action=cur-open][data-id="${lid}"]`); await page.clock.runFor(30);
}
console.log("rule buttons tapped:", tapped);
// the January 2025 call opens from L18
await page.click(`[data-action=cur-open][data-id="L18"]`); await page.clock.runFor(40);
await page.click(".ls-det .curr-call"); await page.clock.runFor(100);
const card = await txt(page, '.asw-c.open');
check("L18 opens his January 2025 NVIDIA call", /Jan 2025/.test(card) && /\$77\.51/.test(card) && /sold half of the half/i.test(card) && /\$300 billion/.test(card), card.slice(0, 300));
check("the 2023 card is still there", (await page.$$eval('.asw-call[data-id="NVDA"]', b => b.length)) === 1);
check("no errors", errors.length === 0, errors);
await o.ctx.close(); await browser.close();
process.exit(summary("refs") ? 1 : 0);
