// every investing revisit: start it, check the new company's numbers, the closed short answer, no KO-only wording, no sideways scroll
import { launch, openPage, check, summary, noHScroll } from "./harness.mjs";
const browser = await launch();
const txt = (p, s) => p.$eval(s, e => e.innerText.replace(/\s+/g, " ").trim()).catch(() => "");
const o = await openPage(browser, {});
const { page, errors } = o;
import fs from "fs";
const html = fs.readFileSync(new URL("./page.html", import.meta.url).pathname, "utf8");
const KO = JSON.parse(/var VAL_KO=(\{.*\});/.exec(html)[1]);
const L = Array.from({ length: 34 }, (_, i) => "L" + String(i + 1).padStart(2, "0")).map(id => { const k = KO[id] || {}; return { id, rev: k.rev || null, rneed: (k.rneed || []).length, rkey: (k.rkey || []).length, rtask: !!k.rtask }; });
check("34 lessons", L.length === 34, L.length);
let withNums = 0;
for (const l of L) {
  check(l.id + " has rev + rtask + rkey", l.rev && l.rtask && l.rkey > 0, l);
  await page.evaluate(id => {
    const b = document.createElement("button"); b.setAttribute("data-action", "rev-start"); b.setAttribute("data-id", "goal_invest"); b.setAttribute("data-lid", id); document.getElementById("root").appendChild(b); b.click();
  }, l.id);
  await page.clock.runFor(80);
  const rv = await txt(page, ".ses-rev");
  if (!rv) { check(l.id + " revisit opens", false); continue; }
  check(l.id + " says the company", rv.includes("now on " + l.rev), rv.slice(0, 200));
  check(l.id + " no What you need", !/What you need/.test(rv), rv.slice(0, 300));
  const task = await txt(page, ".ses-rev .ses-task");
  check(l.id + " task not KO-only", !/\bKO’s\b|\bon KO\b|\bfor KO\b/.test(task) || /KO/.test(l.rev), task);
  if (l.rneed) { withNums++; check(l.id + " Numbers for box", /Numbers for /i.test(rv), rv.slice(0, 200)); }
  check(l.id + " closed short answer", await page.$eval(".ses-rev details.rev-key", d => !d.open).catch(() => false));
  check(l.id + " no sideways scroll", await noHScroll(page));
  // open the short answer: it shows, and nothing overflows
  await page.click(".ses-rev details.rev-key summary").catch(() => {}); await page.clock.runFor(20);
  check(l.id + " short answer opens", await page.$eval(".ses-rev details.rev-key", d => d.open && d.querySelector(".hkey-l li")).catch(() => false));
  check(l.id + " still no sideways scroll", await noHScroll(page));
  await page.evaluate(() => { const b = document.querySelector("[data-action=ses-stop]"); b && b.click(); }); await page.clock.runFor(80);
}
console.log("lessons with their own revisit numbers: " + withNums + " of " + L.length);
check("no errors", errors.length === 0, errors);
await o.ctx.close(); await browser.close();
process.exit(summary("revisits") ? 1 : 0);
