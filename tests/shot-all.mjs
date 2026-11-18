import { launch, openPage, check, summary, noHScroll, toStep, SAT } from "./harness.mjs";
import fs from "fs";
const DIR = new URL(".", import.meta.url).pathname;
const html = fs.readFileSync(DIR + "page.html", "utf8");
const B = await launch(); const browser = () => B;
const KO = JSON.parse(html.match(/var VAL_KO=(\{[\s\S]*?\});\n/)[1]);
const IDS = Object.keys(KO).sort();
check("34 lessons carry inputs and a worked answer", IDS.length === 34 && IDS.every(id => KO[id].need && KO[id].need.length && KO[id].key && KO[id].key.length));
const SHOTS = ["L01", "L18", "L28", "L32"];
const SPOT = {   // a number from each new lesson's worked answer, as the page shows it
  L01: /\$4,425 billion/, L02: /59% concentrate/, L15: /\$44\.72/, L16: /1\.83/, L17: /\$54\.74/, L18: /\$101\.58/, L19: /\$34\.2 billion/,
  L20: /114%/, L21: /\$56\.89/, L22: /17\.5 times sales/, L23: /computed or chosen/i, L24: /7\.72%/, L25: /\$10,946 M/, L26: /\$176\.1 billion/,
  L27: /NvidiaJan2025|judgement/i, L28: /97%/, L29: /114% to 20%/, L30: /\$82\.36/, L31: /\$76\.05|\$14\.26/, L32: /\$76\.05/, L33: /L03–L14/, L34: /Not financial advice/,
};
for (const W of [402, 1280]) for (const lid of IDS) {
  const { page, ctx, errors } = await openPage(browser(), { width: W, dsf: W === 402 ? 2 : 1 });
  await page.evaluate(lid => { const b = document.createElement("button"); b.setAttribute("data-action", "cur-start"); b.setAttribute("data-id", "goal_invest"); b.setAttribute("data-lid", lid); document.getElementById("root").appendChild(b); b.click(); }, lid);
  await page.clock.runFor(80);
  const brief = await page.$eval(".ses-brief", e => e.innerText).catch(() => "");
  check(lid + " " + W + ": task mentions What you need", /What you need/.test(brief), brief.slice(0, 120));
  await toStep(page, 1);
  const need = await page.$eval(".ses .need", e => e.innerText).catch(() => "");
  check(lid + " " + W + ": Learn shows What you need", /WHAT YOU NEED/i.test(need), need.slice(0, 80));
  const sesText = await page.$eval(".ses", e => e.innerText);
  check(lid + " " + W + ": no pointer to local files", !/value\.py|damodaran_source_files|Lab \/ example|Valuation Agent repo/i.test(sesText));
  const links = await page.$$eval(".ses .need a", as => as.map(a => a.href));
  check(lid + ": every link is https", links.every(h => /^https:\/\//.test(h)));
  check(lid + " " + W + ": no sideways scroll (Learn)", await noHScroll(page));
  const clash = await page.$$eval(".ses .need-r", rs => rs.map(r => { const d = r.querySelector("dt").getBoundingClientRect(), v = r.querySelector(".need-v").getBoundingClientRect(), w = r.getBoundingClientRect().width;
    return (d.right > v.left + 1 && d.bottom > v.top + 1 && v.bottom > d.top + 1) || d.width < w * 0.3 ? r.querySelector("dt").innerText + " | " + r.querySelector(".need-v").innerText : null; }).filter(Boolean));
  check(lid + " " + W + ": labels and values don't collide", clash.length === 0, clash);
  if (W === 402 && SHOTS.includes(lid)) await page.$eval(".ses .need", e => e.scrollIntoView({ block: "start" })), await page.screenshot({ path: DIR + `inv-${lid}-learn.png` });
  await toStep(page, 2);
  check(lid + ": Write shows What you need, named as in Learn", /WHAT YOU NEED/i.test(await page.$eval(".ses .need-sm", e => e.innerText).catch(() => "")));
  await toStep(page, 3);
  const key = await page.$eval(".ses .hkey", e => e.innerText).catch(() => "");
  check(lid + ": Check shows a worked answer", /CHECK YOUR ANSWER/i.test(key) && key.length > 200, key.slice(0, 120));
  if (SPOT[lid] && W === 402) check(lid + ": spot number " + SPOT[lid], SPOT[lid].test(need + "\n" + key), (need + key).slice(0, 300));
  check(lid + " " + W + ": no sideways scroll (Check)", await noHScroll(page));
  if (W === 402 && SHOTS.includes(lid)) await page.$eval(".ses .hkey", e => e.scrollIntoView({ block: "start" })), await page.screenshot({ path: DIR + `inv-${lid}-check.png` });
  check(lid + " " + W + ": no errors", errors.length === 0, errors);
  await ctx.close();
}
await B.close();
process.exit(summary("invest") ? 1 : 0);
