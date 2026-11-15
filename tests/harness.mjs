// shared test harness: the page at https://app.test/ with a stubbed window.claude
import { createRequire } from "module";
const { chromium } = createRequire(import.meta.url)("playwright");
import fs from "fs";
const DIR = new URL(".", import.meta.url).pathname;
export const T0 = new Date("2026-11-09T10:00:00"); // a Monday morning

export async function launch() { return chromium.launch(); }

export async function openPage(browser, opts = {}) {
  const file = opts.file || DIR + "page.html";
  const html = fs.readFileSync(file, "utf8");
  const ctx = await browser.newContext({ viewport: { width: opts.width || 402, height: opts.height || 900 }, deviceScaleFactor: opts.dsf || 1, colorScheme: opts.dark ? "dark" : "light", hasTouch: !!opts.touch });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", e => errors.push(String(e)));
  page.on("console", m => { if (m.type() === "error" && !/fonts\.g|ERR_|Failed to load resource/.test(m.text())) errors.push("console: " + m.text()); });
  await page.route("**/*", r => {
    const u = r.request().url();
    if (u.startsWith("https://app.test/")) return r.fulfill({ status: 200, contentType: "text/html; charset=utf-8", body: html });
    return r.abort();
  });
  await page.clock.install({ time: opts.time || T0 });
  await page.addInitScript(cfg => {
    window.__pub = []; window.__calls = []; window.__pending = [];
    if (cfg.view) try { localStorage.setItem("wmtw_view", cfg.view); } catch (e) {}
    const lim = cfg.images === false ? { maxPromptBytes: 65536 } : { maxPromptBytes: 65536, images: { maxCount: 4, maxInputBytes: 20 * 1024 * 1024, mediaTypes: ["image/jpeg", "image/png", "image/webp", "image/gif"] } };
    const sample = function () { return Promise.reject({ code: "upstream_error", message: "stub" }); };
    sample.json = function (input, o) {
      o = o || {};
      window.__calls.push({ input, hasImg: o.images instanceof Blob, imgType: o.images && o.images.type, tier: o.modelTier, cache: o.cache, sig: !!o.signal });
      return new Promise((res, rej) => {
        window.__pending.push({ res, rej });
        if (o.signal) o.signal.addEventListener("abort", () => rej({ code: "cancelled" }));
      });
    };
    sample.limits = () => Promise.resolve(lim);
    const art = { publish(h) { window.__pub.push(h); return Promise.resolve(); } };
    window.claude = { use(n) { return Promise.resolve(n === "sample" ? (cfg.sample === false ? null : sample) : n === "artifact" ? art : null); } };
  }, { images: opts.images, sample: opts.sample, view: opts.view });
  await page.goto("https://app.test/");
  await page.waitForSelector(".top");
  await page.clock.runFor(50);
  return { ctx, page, errors };
}

export function pubState(html) {
  const m = /<script id="app-state"[^>]*>([\s\S]*?)<\/script>/.exec(html);
  return JSON.parse(m[1]);
}
export async function lastPub(page) { const h = await page.evaluate(() => window.__pub[window.__pub.length - 1]); return h ? pubState(h) : null; }

let pass = 0, fail = 0;
export function check(name, ok, info) {
  if (ok) { pass++; } else { fail++; console.log("  ✗ " + name + (info !== undefined ? "  → " + JSON.stringify(info).slice(0, 400) : "")); }
}
export function summary(label) { console.log(label + ": " + pass + " passed, " + fail + " failed"); return fail; }
export async function noHScroll(page) { return page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1); }
