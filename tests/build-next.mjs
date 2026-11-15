// node build-next.mjs <prev-code.html> <live-saved.html> <new-code.html> <out.html>
// Asserts the live page still runs prev's code, then writes new code + live's state (byte-identical).
import fs from "fs";
const [prevP, liveP, nextP, outP] = process.argv.slice(2);
const rd = p => fs.readFileSync(p, "utf8");
const prev = rd(prevP), live = rd(liveP), next = rd(nextP);
function block(html, id) {
  const re = id === "app-style"
    ? /<style id="app-style">([\s\S]*?)<\/style>/
    : new RegExp('<script id="' + id + '"[^>]*>([\\s\\S]*?)<\\/script>');
  const m = re.exec(html); return m ? { body: m[1], start: m.index + m[0].indexOf(">") + 1, end: m.index + m[0].length - (id === "app-style" ? 8 : 9) } : null;
}
for (const id of ["app-style", "app-articles", "app-doctrine", "app"]) {
  const a = block(prev, id), b = block(live, id);
  if (!a || !b) { console.error("missing block " + id); process.exit(1); }
  if (a.body !== b.body) { console.error("live " + id + " differs from prev"); process.exit(1); }
}
const ls = block(live, "app-state"), ns = block(next, "app-state");
JSON.parse(ls.body);
const out = next.slice(0, ns.start) + ls.body + next.slice(ns.end);
if (block(out, "app-state").body !== ls.body) { console.error("state splice failed"); process.exit(1); }
fs.writeFileSync(outP, out);
console.log(outP + " " + out.length + " bytes · state untouched (" + ls.body.length + " chars)");
