// every tab loads with the live data, no errors, no sideways scroll, at phone and desktop width, light and dark
import { launch, openPage, check, summary, noHScroll } from "./harness.mjs";
const browser = await launch();
for (const width of [402, 1280]) for (const dark of [false, true]) for (const view of ["now", "goals", "projects", "review"]) {
  const { page, ctx, errors } = await openPage(browser, { width, dark, view });
  await page.clock.runFor(200);
  const tag = `${view} ${width}${dark ? " dark" : ""}`;
  check(tag + ": renders", await page.$(".view").then(Boolean));
  check(tag + ": no sideways scroll", await noHScroll(page));
  check(tag + ": no errors", errors.length === 0, errors);
  if (view === "review") check(tag + ": no 'null' times", !(await page.$$eval(".tl-start,.tl-time span", els => els.some(e => /null/.test(e.textContent)))));
  await ctx.close();
}
{ // the old page: Review printed null start times
  const { page, ctx } = await openPage(browser, { file: new URL("./test-same.html", import.meta.url).pathname, view: "review", time: new Date("2026-11-08T21:00:00") });
  await page.clock.runFor(200);
  const s = await page.$$eval(".tl-start", els => els.map(e => e.textContent));
  console.log("  v65 review start times on 8 Nov:", JSON.stringify(s.slice(0, 4)));
  await ctx.close();
}
{
  const { page, ctx } = await openPage(browser, { view: "review", time: new Date("2026-11-08T21:00:00") });
  await page.clock.runFor(200);
  const s = await page.$$eval(".tl-start", els => els.map(e => e.textContent));
  console.log("  v66 review start times on 8 Nov:", JSON.stringify(s.slice(0, 4)));
  check("v66 review times are times", s.length === 0 || s.every(x => /\d/.test(x) && !/null/.test(x)), s);
  await ctx.close();
}
{ // touch phone: the helper line drops "paste or drop"
  const { page, ctx, errors } = await openPage(browser, { touch: true });
  check("touch: helper line", await page.$eval(".shot-or", e => e.textContent) === "Claude reads it, fills this in and starts the clock.");
  check("touch: no errors", errors.length === 0, errors);
  await ctx.close();
}
await browser.close();
process.exit(summary("smoke") ? 1 : 0);
