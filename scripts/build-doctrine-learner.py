#!/usr/bin/env python3
"""Put Damodaran's rules, rewritten for a learner, into the app (the "Want more" notes of the investing lessons).

Source: scripts/doctrine-learner.md — one entry per rule (D-01 … D-49) and four big ideas (routes, pairs, paths,
effort), rewritten from the Valuation Agent doctrine (valuation-agent 881fafa) for someone learning the method:
the rule, why, his example, his own words, what to watch out for. This script adds, for each, the lessons that
practise it (from the curriculum's doctrine_ref and the lessons' extra "docs"), checks every cross-reference, and
writes the <script id="app-doctrine" type="application/json"> block of time-tracker.html.

It replaces scripts/build-doctrine.mjs, which copied the agent's own text (an engineering rulebook) into the app.

    python3 scripts/build-doctrine-learner.py            # rewrite the block
    python3 scripts/build-doctrine-learner.py --check    # exit 1 if the block is out of date
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "doctrine-learner.md")
HTML = os.path.join(HERE, "..", "time-tracker.html")
X_KEYS = ("routes", "pairs", "paths", "effort")
FROM = "learner rewrite of valuation-agent 881fafa"


def entries(md):
    """Split the source into (key, title, stage, body) entries; text before the first entry is the file's preamble."""
    out = []
    for block in re.split(r"(?m)^(?=# (?:D-\d\d|" + "|".join(X_KEYS) + r") · )", md)[1:]:
        head, _, rest = block.partition("\n")
        m = re.match(r"# (D-\d\d|" + "|".join(X_KEYS) + r") · (.+)$", head)
        stage = None
        sm = re.match(r"stage: (\S+) · (.+)\n", rest)
        if sm:
            stage, rest = (sm.group(1), sm.group(2).strip()), rest[sm.end():]
        out.append((m.group(1), m.group(2).strip(), stage, rest.strip()))
    return out


def lessons_by_key(html):
    """Which investing lessons cite each rule (doctrine_ref) or big idea (VAL_TEACH docs)."""
    by = {}
    cur = html[html.index("var VAL_CURRICULUM="):html.index("VAL_CURRICULUM.key=")]
    for m in re.finditer(r'\{"id": "(L\d\d)"[^\n]*?"doctrine_ref": \[([^\]]*)\]', cur):
        for k in re.findall(r'"(D-\d\d)"', m.group(2)):
            by.setdefault(k, set()).add(m.group(1))
    teach = html[html.index("var VAL_TEACH={"):html.index("/* VAL_KO:start")]
    for m in re.finditer(r'"(L\d\d)":\{"teach":.*?"docs":\[([^\]]*)\]', teach):
        for k in re.findall(r'"(\w+)"', m.group(2)):
            by.setdefault(k, set()).add(m.group(1))
    return {k: sorted(v) for k, v in by.items()}, set(re.findall(r'\{"id": "(L\d\d)"', cur))


def meta(stage, lessons):
    parts = []
    if stage:
        n, name = stage
        parts.append(name if n in ("0", "P") else "Stage %s · %s" % (n, name))
    if lessons:
        parts.append("practised in " + ", ".join(lessons))
    return " · ".join(parts)


def build(html):
    md = open(SRC, encoding="utf-8").read()
    E = entries(md)
    by, all_lessons = lessons_by_key(html)
    d, x = {}, {}
    for key, title, stage, body in E:
        assert body.startswith("## The rule") or key in X_KEYS, (key, "a rule card starts with its rule")
        rec = {"t": title, "m": meta(stage, by.get(key, [])), "md": body}
        (x if key in X_KEYS else d)[key] = rec
    want = ["D-%02d" % i for i in range(1, 50)]
    assert sorted(d) == want, "expected D-01 … D-49, got %s" % sorted(set(want) ^ set(d))
    assert sorted(x) == sorted(X_KEYS), sorted(x)
    for key, rec in list(d.items()) + list(x.items()):
        for ref in re.findall(r"\bD-\d\d\b", rec["md"]):
            assert ref in d, (key, "cites a rule that doesn't exist", ref)
        for ref in re.findall(r"\bL\d\d\b", rec["md"]):
            assert ref in all_lessons, (key, "cites a lesson that doesn't exist", ref)
        assert not re.search(r"\b(engine|rulebook|the agent)\b", rec["md"], re.I), (key, "agent wording left in")
    js = json.dumps({"from": FROM, "d": d, "x": x}, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    return '<script id="app-doctrine" type="application/json">' + js + "</script>", d, x


def main():
    html = open(HTML, encoding="utf-8").read()
    block, d, x = build(html)
    RE = re.compile(r'<script id="app-doctrine" type="application/json">[\s\S]*?</script>')
    if not RE.search(html):
        sys.exit("no app-doctrine block in time-tracker.html")
    new = RE.sub(lambda m: block, html, count=1)
    if "--check" in sys.argv:
        sys.exit(0 if new == html else "app-doctrine block is out of date")
    open(HTML, "w", encoding="utf-8").write(new)
    words = sum(len(r["md"].split()) for r in list(d.values()) + list(x.values()))
    print("doctrine (learner): %d rules + %d ideas · %d words · %d KB" % (len(d), len(x), words, len(block) // 1024))


main()
