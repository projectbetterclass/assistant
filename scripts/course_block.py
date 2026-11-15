# Shared by the course scripts (build-*-course.py): write one course into time-tracker.html as its own block, and
# add it to CURRICULA. A block starts with a comment line that names it and ends with "var <NAME>={...};".
import json, os, re

HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "time-tracker.html")
LIBRARY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "youtube-digest", "data", "library.json")
KEYS = ["id", "order", "rung", "stage_name", "concept", "estimateMin", "teach", "task", "co", "rev", "after", "watch", "read",
        "walk", "thread", "need", "needNote", "key", "rtask", "rneed", "rkey"]


def yt(vid, channel, title, why):
    return {"t": channel + " · " + title, "u": "https://www.youtube.com/watch?v=" + vid, "w": why}


def course(meta, lessons):
    """Number the lessons, check them, and return the curriculum object."""
    ids = [x["id"] for x in lessons]
    assert len(ids) == len(set(ids)), "duplicate lesson ids"
    for i, x in enumerate(lessons):
        x.setdefault("estimateMin", 30)
        x["order"] = i + 1
        assert x["rung"] in meta["rungs"], (x["id"], x["rung"])
        assert 150 < len(x["teach"]) < 1100, (x["id"], len(x["teach"]))   # a short idea, or a paragraph; never empty
        for a in x.get("after", []):
            assert meta["rungs"].index(next(y for y in lessons if y["id"] == a)["rung"]) == meta["rungs"].index(x["rung"]) - 1, (x["id"], "after", a)
    assert len(meta["rungDesc"]) == len(meta["rungs"])
    return dict(meta, lessons=[{k: x[k] for k in KEYS if k in x} for x in lessons])


def lesson_texts(x):
    """Everything a lesson shows, as (where, text) pairs: the idea, walk-through, thread, task, numbers box, worked answer."""
    out = [("idea", x.get("teach", ""))]
    for sec in x.get("walk", []):
        out += [("walk", sec["h"])] + [("walk", q) for q in sec.get("p", []) + sec.get("p2", [])]
        out += [("walk", " ".join(it) if isinstance(it, list) else it) for it in sec.get("l", [])]
    out += [("thread", x["thread"][k]) for k in ("b", "n") if x.get("thread", {}).get(k)]
    out += [("task", x.get("task", ""))] + ([("needNote", x["needNote"])] if x.get("needNote") else [])
    for it in x.get("need", []):
        out += [("need", it["k"])] + ([("need", it["n"])] if it.get("n") else [])
    for b in x.get("key", []):
        out += ([("answer", b["t"])] if b.get("t") else []) + [("answer", q) for q in b.get("l", [])]
    return out


def term_order(lessons, glossary, prefix):
    """A term may be used before the lesson that teaches it only with a pointer to that lesson in the same sentence,
    e.g. "(X07)" or "X03–X05". glossary: [(lesson number, name, regex)]. Returns the offending sentences."""
    ptr = re.compile(r"\b%s(\d\d)(?:\s*[–-]\s*%s(\d\d))?" % (prefix, prefix))
    flags = []
    for x in lessons:
        n = int(x["id"][1:])
        for where, text in lesson_texts(x):
            for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z‘“(€$])", text):
                ps = [(int(a), int(b or a)) for a, b in ptr.findall(sent)]
                for intro, name, rx in glossary:
                    if intro > n and re.search(rx, sent, re.I) and not any(a <= intro <= b for a, b in ps):
                        flags.append("%s %s: “%s” is taught in %s%02d — %s" % (x["id"], where, name, prefix, intro, sent[:110]))
    return flags


def check_extras(lessons):
    """The numbers box, worked answer, walk-through and revisit fields have the shapes the app renders."""
    for x in lessons:
        for it in x.get("need", []) + x.get("rneed", []):
            assert it.get("k") and it.get("v"), (x["id"], it)
        for b in x.get("key", []) + x.get("rkey", []):
            assert b.get("l") and all(isinstance(q, str) and q for q in b["l"]), (x["id"], b)
        for sec in x.get("walk", []):
            assert sec.get("h") and (sec.get("p") or sec.get("l")), (x["id"], sec)
        if "rtask" in x:
            assert (x.get("rev") or "{idea}" in x["rtask"]) and x.get("rkey"), (x["id"], "a revisit needs its company (or {idea}) and an answer")
        if "thread" in x:
            assert x["thread"].get("n"), (x["id"], "a thread says where the lesson leads")


def check_videos(cur, library=LIBRARY):
    """Every watch link must be a video in the youtube-digest library, under the title shown."""
    if not os.path.exists(library):
        print("  (library not found at %s: video ids not checked)" % library)
        return
    lib = json.load(open(library, encoding="utf-8"))["videos"]
    n = 0
    for l in cur["lessons"]:
        for v in l.get("watch", []):
            vid = v["u"].rsplit("=", 1)[1]
            x = lib.get(vid)
            assert x, (l["id"], vid, "not in the library")
            assert v["t"] == x["channel"] + " · " + x["title"].replace("::", ":"), (l["id"], v["t"], x["channel"], x["title"])
            n += 1
    print("  %d videos checked against the library" % n)


def write(name, comment, cur):
    html = open(HTML, encoding="utf-8").read()
    js = json.dumps(cur, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    block = "".join("  " + ("/* " if i == 0 else "   ") + line + ("\n" if i < len(comment) - 1 else " */\n") for i, line in enumerate(comment)) + "  var " + name + "=" + js + ";\n"
    first = re.escape("  /* " + comment[0].split(" — ")[0])
    old = re.search(first + r"[\s\S]*?\n  var " + name + r"=\{[\s\S]*?\};\n", html)
    if old:
        html = html[:old.start()] + block + html[old.end():]
    else:
        anchor = "  var CURRICULA=["
        assert html.count(anchor) == 1
        html = html.replace(anchor, block + anchor)
    m = re.search(r"  var CURRICULA=\[([^\]]*)\];", html)
    names = [s.strip() for s in m.group(1).split(",")]
    if name not in names:
        html = html[:m.start(1)] + ",".join(names + [name]) + html[m.end(1):]
    open(HTML, "w", encoding="utf-8").write(html)
    print("%s: %d lessons written into time-tracker.html" % (name, len(cur["lessons"])))
