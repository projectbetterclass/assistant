// Open every rule note from inside its lessons (Learn → Want more, and Check): renders, no raw markdown, no agent wording.
import { launch, openPage, check, summary, noHScroll, toStep, SAT } from "./harness.mjs";
import fs from "fs";
const DIR = new URL(".", import.meta.url).pathname;
const file = DIR + (process.argv[2] || "page.html");
const html = fs.readFileSync(file, "utf8");
const D = JSON.parse(html.match(/<script id="app-doctrine" type="application\/json">([\s\S]*?)<\/script>/)[1]);
check("49 rules and 4 ideas", Object.keys(D.d).length === 49 && Object.keys(D.x).length === 4);
const B = await launch();
const seen = new Set();
for (const W of [402]) for (const lid of ["L01","L02","L03","L04","L05","L06","L07","L08","L09","L10","L11","L12","L13","L14","L15","L16","L17","L18","L19","L20","L21","L22","L23","L24","L25","L26","L27","L28","L29","L30","L31","L32","L33","L34"]) {
  const { page, ctx, errors } = await openPage(B, { width: W, file, time: SAT });
  await page.evaluate(lid => { const b = document.createElement("button"); b.setAttribute("data-action", "cur-start"); b.setAttribute("data-id", "goal_invest"); b.setAttribute("data-lid", lid); document.getElementById("root").appendChild(b); b.click(); }, lid);
  await page.clock.runFor(80);
  await toStep(page, 1);
  const more = await page.$("details.ses-more");
  if (more) { await page.$eval("details.ses-more", d => { d.open = true; d.dispatchEvent(new Event("toggle")); }); await page.clock.runFor(30); }
  const keys = await page.$$eval(".ses-more .doc-b", bs => bs.map(b => b.getAttribute("data-k")));
  for (const k of keys) {
    await page.click(`.ses-more .doc-b[data-k="${k}"]`); await page.clock.runFor(30);
    const body = await page.$eval(`.ses-more .doc-b[data-k="${k}"]`, b => b.parentElement.querySelector(".doc-body") ? b.parentElement.querySelector(".doc-body").innerText : "");
    const id = k.split(":").pop(); seen.add(id);
    check(`${lid} ${id}: opens with text`, body.length > 150, body.slice(0, 80));
    check(`${lid} ${id}: no raw markdown`, !/(^|\n)#{1,3} |\*\*|\|\s*---|^\s*\|/m.test(body), body.match(/(^|\n)#{1,3} .*|\*\*.*|\|\s*---.*/m));
    check(`${lid} ${id}: no agent wording`, !/\b(engine|rulebook|the agent|Chosen\b)/.test(body), body.match(/.{0,40}\b(engine|rulebook|the agent|Chosen)\b.{0,40}/));
    if (/^D-/.test(id)) check(`${lid} ${id}: starts with The rule`, /^[\s\S]{0,200}THE RULE/i.test(body), body.slice(0, 120));
    if (lid === "L09" && id === "D-24") { await page.$eval(`.ses-more .doc-b[data-k="${k}"]`, b => b.scrollIntoView({ block: "start" })); await page.screenshot({ path: DIR + "doc-D24.png" }); }
    if (lid === "L32" && id === "D-49") { await page.$eval(`.ses-more .doc-b[data-k="${k}"]`, b => b.scrollIntoView({ block: "start" })); await page.screenshot({ path: DIR + "doc-D49.png" }); }
  }
  check(`${lid}: no sideways scroll with notes open`, await noHScroll(page));
  check(`${lid}: no errors`, errors.length === 0, errors);
  await ctx.close();
}
const all = [...Object.keys(D.d), ...Object.keys(D.x)].filter(k => !seen.has(k));
check("every rule cited by a lesson opened somewhere", all.length === 0, all);
await B.close();
process.exit(summary("docs") ? 1 : 0);
