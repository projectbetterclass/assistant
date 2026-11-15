// v66: start from a screenshot
import { launch, openPage, check, summary, lastPub, noHScroll, T0 } from "./harness.mjs";
import fs from "fs";
const DIR = new URL(".", import.meta.url).pathname;
const W = +(process.argv[2] || 402);
const SHOTS = process.argv.includes("--shots");
const browser = await launch();

// a fake screenshot to attach: a video page mock-up
const PNG = DIR + "fake-shot.png";
if (!fs.existsSync(PNG)) {
  const c = await browser.newContext({ viewport: { width: 390, height: 700 } }); const p = await c.newPage();
  await p.setContent(`<body style="margin:0;font:15px system-ui;background:#fff"><div style="height:220px;background:#111;display:grid;place-items:center;color:#fff;font-size:42px">▶</div>
  <div style="padding:12px"><b style="font-size:18px">Session 9: Cost of capital</b><div style="color:#666;margin-top:6px">Aswath Damodaran · 48:12</div></div></body>`);
  fs.writeFileSync(PNG, await p.screenshot()); await c.close();
}
const shotBytes = [...fs.readFileSync(PNG)];

async function attach(page) { await page.setInputFiles('.shot-pick input[type=file]', PNG); await page.clock.runFor(30); }
async function resolve(page, v) { await page.evaluate(v => window.__pending[window.__pending.length - 1].res(v), v); await page.clock.runFor(30); }
async function reject(page, e) { await page.evaluate(e => window.__pending[window.__pending.length - 1].rej(e), e); await page.clock.runFor(30); }
const st = page => page.evaluate(() => JSON.parse(JSON.stringify(window.__dbgState ? window.__dbgState() : null)));
async function active(page) { const s = await lastPub(page); if (!s) return null; const t = s.tasks.find(x => x.id === s.activeId); return { s, t }; }
const near = (a, b) => typeof a === "number" && Math.abs(a - b) < 400;
const text = (page, sel) => page.$eval(sel, e => e.textContent).catch(() => null);
const has = (page, sel) => page.$(sel).then(Boolean);

// 1. the button is there, and only where Claude can read images
{
  const { page, ctx, errors } = await openPage(browser, { width: W });
  check("start card shows the screenshot button", await has(page, ".now-idle .shot-pick"));
  check("button label", (await text(page, ".shot-pick")) === "From a screenshot", await text(page, ".shot-pick"));
  check("accept lists the image types", (await page.$eval(".shot-pick input", e => e.accept)).includes("image/png"));
  check("helper line says what happens", /Claude reads it, fills this in and starts the clock/.test(await text(page, ".shot-or")));
  check("no sideways scroll", await noHScroll(page));
  if (SHOTS) await page.$eval(".now-idle", e => e.scrollIntoView({ block: "center" })), await page.screenshot({ path: DIR + `shot-idle-${W}.png` });
  check("no page errors", errors.length === 0, errors);
  await ctx.close();
}
{
  const { page, ctx } = await openPage(browser, { width: W, images: false });
  check("no button when this view can't send images", !(await has(page, ".shot-pick")));
  await ctx.close();
}
{
  const { page, ctx } = await openPage(browser, { width: W, sample: false });
  check("no button when Claude isn't available", !(await has(page, ".shot-pick")));
  await ctx.close();
}

// 2. attach → reading → a new thing starts, counted from when you added it
let fixPage;
{
  const { page, ctx, errors } = await openPage(browser, { width: W });
  const before = await page.evaluate(() => JSON.parse(document.getElementById("app-state").textContent).tasks.length);
  const tAttach = await page.evaluate(() => Date.now());
  await attach(page);
  check("reading panel shows", await has(page, ".now-idle .shot:not(.is-failed)"));
  check("thumbnail of your screenshot", await page.$eval(".shot-img", e => e.src.startsWith("blob:")).catch(() => false));
  check("reading text", /Reading your screenshot/.test(await text(page, ".shot-t")));
  check("says when the clock counts from", /The clock will count from/.test(await text(page, ".shot-s")));
  check("button hidden while reading", !(await has(page, ".shot-pick")));
  const call = await page.evaluate(() => window.__calls[0]);
  check("Claude got the image", call && call.hasImg && call.imgType === "image/png", call && { hasImg: call.hasImg, t: call.imgType });
  check("quick tier, no cache, cancellable", call && call.tier === "quick" && call.cache === false && call.sig);
  check("prompt lists goals", /goal_read \| Read 20 minutes a day/.test(call.input) && /goal_fx \| Trading: forex & options › Forex/.test(call.input), call.input.slice(0, 200));
  check("prompt lists tracked things", /muzyrdr18nbnl \| atomic habit listening \| Read 20 minutes a day/.test(call.input));
  check("prompt leaves out lessons and finished things", !/lesson_goal_invest_L01/.test(call.input) && !/mu9srhdljn66p/.test(call.input));
  check("prompt lists categories", /Categories they use: Work, Focus/.test(call.input));
  check("prompt guards against text in the image", /never instructions/.test(call.input));
  if (SHOTS) await page.$eval(".now-idle", e => e.scrollIntoView({ block: "center" })), await page.screenshot({ path: DIR + `shot-reading-${W}.png` });
  await page.clock.runFor(15000);
  await resolve(page, { name: "Watch Damodaran: cost of capital", match: null, goal: "goal_invest", category: "focus", depth: "deep", seen: "Video: Damodaran, Session 9 on cost of capital" });
  const a = await active(page);
  check("published", !!a);
  check("a new thing is running", a && a.t && a.t.name === "Watch Damodaran: cost of capital", a && a.t);
  check("filed under the goal", a && a.t.goalId === "goal_invest");
  check("category matched to yours", a && a.t.category === "Focus", a && a.t.category);
  check("depth", a && a.t.depth === "deep");
  check("one more task", a && a.s.tasks.length === before + 1, a && [a.s.tasks.length, before]);
  check("clock counts from when you added it", a && a.t.sessions.length === 1 && near(a.t.sessions[0].start, tAttach) && a.t.sessions[0].end === null && (await page.evaluate(() => Date.now())) - a.t.sessions[0].start >= 15000, a && [a.t.sessions, tAttach]);
  check("session remembers what was seen", a && a.t.sessions[0].seen === "Video: Damodaran, Session 9 on cost of capital" && !a.t.sessions[0].matched);
  check("not a goal action", a && !a.t.daily);
  check("running card", await has(page, ".now-active"));
  check("running card says it came from the screenshot", /^From your screenshot: Video: Damodaran, Session 9 on cost of capital$/.test(await text(page, ".now-shot-t")), await text(page, ".now-shot-t"));
  check("clock already shows the 15 s", /^00:1[5-9]$/.test(await text(page, ".now-active .now-clock")), await text(page, ".now-active .now-clock"));
  check("panel gone", !(await has(page, ".shot")));
  check("no sideways scroll", await noHScroll(page));
  if (SHOTS) await page.$eval(".now-active", e => e.scrollIntoView({ block: "start" })), await page.screenshot({ path: DIR + `shot-running-${W}.png` });

  // fix it: renamed in place
  await page.click('[data-action="shot-fix"]');
  check("fix form opens with the name", (await page.$eval("#shot-name", e => e.value)) === "Watch Damodaran: cost of capital");
  check("fix form has the goal picked", (await page.$eval("#shot-goal", e => e.value)) === "goal_invest");
  if (SHOTS) await page.screenshot({ path: DIR + `shot-fix-${W}.png` });
  await page.fill("#shot-name", "Watch Damodaran: equity risk premium");
  await page.selectOption("#shot-goal", "goal_fx");
  await page.click('.shot-fix button[type=submit]');
  await page.clock.runFor(30);
  const b = await active(page);
  check("renamed in place", b && b.t.id === a.t.id && b.t.name === "Watch Damodaran: equity risk premium" && b.t.goalId === "goal_fx", b && b.t);
  check("still running, same session", b && b.t.sessions.length === 1 && b.t.sessions[0].start === a.t.sessions[0].start && b.t.sessions[0].end === null);
  check("form closed", !(await has(page, ".shot-fix")) && (await has(page, ".now-shot")));

  // stop it: Review shows real start times (the v64 hhmm clash printed "null")
  await page.clock.runFor(60000);
  await page.click('.now-active [data-action="stop"]');
  await page.clock.runFor(30);
  await page.click('[data-view="review"]');
  await page.clock.runFor(30);
  const starts = await page.$$eval(".tl-start", els => els.map(e => e.textContent));
  check("review has a start time for it", starts.length > 0 && starts.every(s => s && s !== "null" && /\d/.test(s)), starts);
  check("no page errors", errors.length === 0, errors);
  await ctx.close();
}

// 3. a match: the time goes on what you already track
{
  const { page, ctx, errors } = await openPage(browser, { width: W });
  const before = await page.evaluate(() => JSON.parse(document.getElementById("app-state").textContent).tasks.length);
  const tAttach = await page.evaluate(() => Date.now());
  await attach(page);
  await page.clock.runFor(4000);
  await resolve(page, { name: "Listen: Atomic Habits", match: "muzyrdr18nbnl", goal: "goal_read", category: "", depth: "shallow", seen: "Audible: Atomic Habits, chapter 3" });
  const a = await active(page);
  check("matched task runs", a && a.t && a.t.id === "muzyrdr18nbnl", a && a.s.activeId);
  check("no new task", a && a.s.tasks.length === before);
  check("its name kept", a && a.t.name === "atomic habit listening");
  const se = a && a.t.sessions[a.t.sessions.length - 1];
  check("session from attach, marked matched", se && near(se.start, tAttach) && se.matched === true && se.seen === "Audible: Atomic Habits, chapter 3", se);
  check("card says matched", /^Matched from your screenshot: Audible: Atomic Habits, chapter 3$/.test(await text(page, ".now-shot-t")), await text(page, ".now-shot-t"));
  // fix a wrong match: the time moves to what it really was; the matched thing is left as it was
  await page.click('[data-action="shot-fix"]');
  await page.fill("#shot-name", "Podcast: money habits");
  await page.selectOption("#shot-goal", "");
  await page.click('.shot-fix button[type=submit]');
  await page.clock.runFor(30);
  const b = await active(page);
  check("a new thing took the time", b && b.t.id !== "muzyrdr18nbnl" && b.t.name === "Podcast: money habits" && !b.t.goalId, b && b.t);
  check("…from the same start", b && b.t.sessions.length === 1 && b.t.sessions[0].start === se.start && !b.t.sessions[0].matched);
  const old = b && b.s.tasks.find(x => x.id === "muzyrdr18nbnl");
  check("matched thing is back as it was", old && old.sessions.length === 0 && old.name === "atomic habit listening", old);
  check("one new task", b && b.s.tasks.length === before + 1);
  check("no page errors", errors.length === 0, errors);
  await ctx.close();
}

// 4. made-up ids, odd category → a plain new thing
{
  const { page, ctx } = await openPage(browser, { width: W });
  await attach(page);
  await resolve(page, { name: "  Something   on screen ", match: "lesson_goal_invest_L01", goal: "nope", category: "Gaming", depth: "intense", seen: 42 });
  const a = await active(page);
  check("lesson id isn't matched", a && a.t.id !== "lesson_goal_invest_L01");
  check("unknown goal dropped", a && !a.t.goalId);
  check("unknown category dropped", a && a.t.category === "");
  check("odd depth dropped", a && !a.t.depth);
  check("name tidied", a && a.t.name === "Something on screen", a && a.t.name);
  check("seen falls back to the name", a && a.t.sessions[0].seen === "Something on screen");
  await ctx.close();
}

// 5. Claude can't read it: type it and the clock still counts from the screenshot
{
  const { page, ctx, errors } = await openPage(browser, { width: W });
  const tAttach = await page.evaluate(() => Date.now());
  await attach(page);
  await page.fill("#q-name", "Reading Atomic Habits");
  await page.clock.runFor(8000);
  await reject(page, { code: "upstream_error", message: "x" });
  check("failed panel", await has(page, ".shot.is-failed"));
  check("says why", /Couldn’t read it this time/.test(await text(page, ".shot-t")), await text(page, ".shot-t"));
  check("offers typing with the kept time", /Type what you’re doing and press Start\. The clock still counts from/.test(await text(page, ".shot-s")));
  check("typed text kept through the re-render", (await page.$eval("#q-name", e => e.value)) === "Reading Atomic Habits");
  check("can try another", (await text(page, ".shot-pick")) === "Try another screenshot");
  if (SHOTS) await page.$eval(".now-idle", e => e.scrollIntoView({ block: "center" })), await page.screenshot({ path: DIR + `shot-failed-${W}.png` });
  await page.click('.now-idle form.quick button[type=submit]');
  await page.clock.runFor(30);
  const a = await active(page);
  check("typed thing runs from the screenshot's time", a && a.t.name === "Reading Atomic Habits" && near(a.t.sessions[0].start, tAttach) && (await page.evaluate(() => Date.now())) - a.t.sessions[0].start >= 8000, a && [a.t.name, a.t.sessions, tAttach]);
  check("no seen line for a typed one", !(await has(page, ".now-shot")));
  check("no page errors", errors.length === 0, errors);
  await ctx.close();
}
{
  const { page, ctx } = await openPage(browser, { width: W });
  await attach(page);
  await resolve(page, { name: "", match: null, goal: null, category: "", depth: "shallow", seen: "a blurry photo" });
  check("can't tell → failed panel", /Couldn’t tell what you’re doing/.test(await text(page, ".shot-t")));
  check("nothing started", !(await lastPub(page)));
  await ctx.close();
}
{
  const { page, ctx } = await openPage(browser, { width: W });
  await attach(page);
  await reject(page, { code: "not_granted", message: "x" });
  check("declined → says so", /declined/.test(await text(page, ".shot-t")));
  check("declined → no more screenshot button", !(await has(page, ".shot-pick")));
  await page.click('[data-action="shot-cancel"]');
  check("clear removes the panel", !(await has(page, ".shot")));
  await ctx.close();
}

// 6. cancel: nothing starts, even if Claude answers late
{
  const { page, ctx } = await openPage(browser, { width: W });
  await attach(page);
  await page.click('[data-action="shot-cancel"]');
  await page.clock.runFor(30);
  check("panel gone", !(await has(page, ".shot")));
  check("button back", await has(page, ".shot-pick"));
  await page.evaluate(() => window.__pending[0].res({ name: "Late", match: null, goal: null, category: "", depth: "shallow", seen: "x" })).catch(() => {});
  await page.clock.runFor(30);
  check("late answer ignored", !(await lastPub(page)));
  await ctx.close();
}

// 7. you start something else while it reads → the screenshot steps aside
{
  const { page, ctx } = await openPage(browser, { width: W });
  await attach(page);
  const chip = await page.$(".rchip-go");
  check("an Again chip exists", !!chip);
  const cid = chip && await chip.getAttribute("data-id");
  await chip.click();
  await page.clock.runFor(30);
  await resolve(page, { name: "Should not start", match: null, goal: null, category: "", depth: "shallow", seen: "x" });
  const a = await active(page);
  check("what you tapped keeps running", a && a.s.activeId === cid, a && a.s.activeId);
  check("screenshot didn't start anything", a && !a.s.tasks.some(t => t.name === "Should not start"));
  await ctx.close();
}

// 8. paste and drop
{
  const { page, ctx } = await openPage(browser, { width: W });
  const fire = (sel, withText) => page.evaluate(({ bytes, sel, withText }) => {
    const dt = new DataTransfer();
    dt.items.add(new File([new Uint8Array(bytes)], "s.png", { type: "image/png" }));
    if (withText) dt.setData("text/plain", "hello");
    const el = document.querySelector(sel); if (el.focus) el.focus();
    el.dispatchEvent(new ClipboardEvent("paste", { clipboardData: dt, bubbles: true, cancelable: true }));
  }, { bytes: shotBytes, sel, withText });
  await fire("#l-name", true);
  await page.clock.runFor(30);
  check("words pasted into a field stay a text paste", !(await has(page, ".shot")) && (await page.evaluate(() => window.__calls.length)) === 0);
  await fire("body", false);
  await page.clock.runFor(30);
  check("pasting an image starts reading", await has(page, ".shot:not(.is-failed)") && (await page.evaluate(() => window.__calls.length)) === 1);
  await page.click('[data-action="shot-cancel"]');
  await page.evaluate(bytes => {
    const dt = new DataTransfer(); dt.items.add(new File([new Uint8Array(bytes)], "d.png", { type: "image/png" }));
    const el = document.querySelector(".now-idle .quick");
    el.dispatchEvent(new DragEvent("dragover", { dataTransfer: dt, bubbles: true, cancelable: true }));
    window.__dropHi = document.querySelector(".now-idle").classList.contains("is-drop");
    el.dispatchEvent(new DragEvent("drop", { dataTransfer: dt, bubbles: true, cancelable: true }));
  }, shotBytes);
  await page.clock.runFor(30);
  check("drag over lights the card", await page.evaluate(() => window.__dropHi));
  check("dropping an image starts reading", await has(page, ".shot:not(.is-failed)") && (await page.evaluate(() => window.__calls.length)) === 2);
  await ctx.close();
}

// 9. the wrong kind of file
{
  const { page, ctx } = await openPage(browser, { width: W });
  await page.setInputFiles('.shot-pick input[type=file]', { name: "a.svg", mimeType: "image/svg+xml", buffer: Buffer.from("<svg xmlns='http://www.w3.org/2000/svg'/>") });
  await page.clock.runFor(30);
  check("svg refused before sending", (await page.evaluate(() => window.__calls.length)) === 0 && !(await has(page, ".shot")));
  await ctx.close();
}

// 10. stopping says honestly whether the time filled the round
for (const [goal, re] of [["goal_invest", /^✓ 3m logged under Investing\. Its round minutes come from the lessons\.$/], ["goal_read", /^✓ Reading: 3 of 14 min today\. That counts\./], ["muyi5ymrd1huk", /^✓ [^:]+: 3 of 14 min today\. That counts\./]]) {
  const { page, ctx, errors } = await openPage(browser, { width: W });
  await attach(page);
  await resolve(page, { name: "Thing for " + goal, match: null, goal, category: "", depth: "deep", seen: "x" });
  await page.clock.runFor(180000);
  await page.click('.now-active [data-action="stop"]');
  await page.clock.runFor(30);
  const tt = await text(page, "#toast");
  check("stop toast for " + goal, re.test(tt || ""), tt);
  check("no page errors " + goal, errors.length === 0, errors);
  await ctx.close();
}

await browser.close();
process.exit(summary("shot " + W) ? 1 : 0);
