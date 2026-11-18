# Builds "Read so it sticks" (READ_CURRICULUM) in time-tracker.html: 12 sittings on the Reading goal, each one reading
# technique used straight away on the chapter you're reading, inside your daily minutes (14 on weekdays in the round, the
# goal's own 20 at weekends). Written in my words from Justin Sung's videos in the youtube-digest library (priming, reading
# in bursts, highlighting, consume vs digest, PACER, mind maps, retrieval, the memory ladder, choosing books), and from the
# Atomic Habits chapter notes on your bookshelf for the habit itself.
#   python3 scripts/build-reading-course.py       -> rewrites the block in time-tracker.html
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from course_block import yt, course, check_videos, check_extras, write

JS = "Justin Sung"
FOCUS = yt("4YF3_fw1Jko", JS, "4 Tips to Read Without Losing Focus", "priming a paragraph, then reading for its anchor points, even when tired")
BOOKS = yt("J-9F6YFgeP8", JS, "How I Find The Perfect Book For Any Problem (Blinkist vs Shortform)", "start from your problem, then screen books for it")
FASTER = yt("f1k4eXELEIE", JS, "4 Steps to Read Difficult Texts Faster (Academic Speed Reading Comprehension)", "grouping words, slowing down where it’s dense, and pausing to predict")
HIGHLIGHT = yt("KTRMX2heR5k", JS, "Intelligent People Never Use Highlighters. Here’s Why", "the illusion of fluency, and the highlighter as a gate to thinking")
REMEMBER = yt("okHkUIW46ks", JS, "How to Remember Everything You Read", "consume, then digest, and the five kinds of information")
LADDER = yt("ldaCYNWUW5M", JS, "How to Read Once and Remember Forever - The Memory Ladder framework", "recall the way you’ll use it, and how much to pay for a memory")
MAPBEG = yt("gLHqVR6VDUg", JS, "You’re Not Dumb: How to Mindmap as a Beginner", "delayed note-taking, fewer words, then a first map")
SPACED = yt("KuI_eD1VbqU", JS, "What Everyone Gets WRONG About Spaced Repetition", "why needing many repetitions points back to how you learned it")

CH, OTHER = "the chapter you’re on", "a chapter of another book on your shelf"
AH3 = "Your bookshelf: Atomic Habits, Ch. 4–7 — Make it obvious"
AH5 = "Your bookshelf: Atomic Habits, Ch. 11–14 — Make it easy"
AH6 = "Your bookshelf: Atomic Habits, Ch. 15–17 — Make it satisfying"
L = [
 dict(id="R01", rung="Habit", stage_name="A time and a place", concept="Decide once when and where you read",
  teach="A reading habit usually fails on the cue, not the book. Atomic Habits, on your shelf, gives two tools. An implementation intention: ‘I will read at [time] in [place]’; in one study Clear cites, 91% of people who wrote theirs down exercised at least weekly, against about 35–38% of those who didn’t. And habit stacking: ‘After [something I already do], I read for 20 minutes.’ Then fix the room: the book on your pillow or by the coffee machine, the phone in another room. A cue you can see beats a plan you have to remember. Write the when and where once, in the box on this card, and stop deciding every day.",
  task="Write your reading intention in one line in this card’s ‘+ when & where’: after which habit, at what time, in which place, which book. Then put that book where the cue happens, tonight, and read on in the chapter you’re on until the sitting ends. Judge: what usually stops you reading, and does your line remove it?",
  co="your daily reading", rev="a busy day", read=[AH3]),
 dict(id="R02", rung="Habit", stage_name="Easy to start", concept="Two minutes to start, and never two days off",
  teach="Clear’s third and fourth laws make a habit easy and satisfying. The two-minute rule: scale it down until starting takes two minutes, so ‘read 20 minutes’ begins as ‘open the book and read one page’; most days you’ll keep going. Cut the friction: the book already open, the audiobook downloaded for the commute. Then track it, because seeing progress is its own small reward: the dots on this goal are your paper clips. And the rule for bad days: never miss twice. Missing once is an accident; missing twice starts a new habit, so on a hard day do the two-minute version. A habit has to exist before it can be improved.",
  task="Write your two-minute version of reading, and the one piece of friction you’ll remove this week. Then do the two minutes now, and keep going in the chapter you’re on. Judge: on your worst day this month, what is the smallest version that still counts?",
  co="your daily reading", rev="a day you’re exhausted", read=[AH5, AH6]),
 dict(id="R03", rung="Before", stage_name="Prime first", concept="A minute of skimming gives the reading somewhere to land",
  teach="Justin Sung’s first step happens before you read: priming. Spend a minute skimming what you’re about to read: the headings, first lines, bold words, any summary or figure. Don’t try to understand it; notice the key words and guess what the chapter will argue. Those words become anchors, so when they come back in the text your brain already has somewhere to put them, and reading feels easier without getting shallower. It works even when you’re tired: prime one paragraph, then slow down only where the anchors are. The Prime step of every sitting is the same idea: guess first.",
  task="Before reading on, spend one minute on the next section of your chapter: write five key words and one sentence on what you think it will argue. Then read it. Judge: where was your guess wrong, and did knowing the words make the reading easier?",
  co=CH, rev=OTHER, after=["R02"], watch=[FOCUS]),
 dict(id="R04", rung="Before", stage_name="Read for a problem", concept="Know what you’re reading this for",
  teach="Justin Sung starts every non-fiction book from a problem he is trying to solve, because the brain processes and keeps information far better when it is framed by something that matters to you. A problem also tells you how to read: which chapters to go deep on, which to skim, and when a book isn’t the right one, however highly it’s rated. Your shelf already has a problem behind each book: Atomic Habits for the daily habits in this app, The Mom Test for your customer interviews, $100M Offers for your AI service, Zero to One for the products you build. Name the problem before each chapter, and read as if you had to use the answer tomorrow.",
  task="Write the problem behind the book you’re reading in one line, and the question this chapter should help you answer. Read on with that question in mind, and stop when you have an answer or know the chapter doesn’t have one. Judge: did the question change what you skimmed and what you slowed down for?",
  co=CH, rev=OTHER, after=["R01"], watch=[BOOKS]),
 dict(id="R05", rung="During", stage_name="Sprints and pauses", concept="Hurry through the easy parts, slow down on the dense ones, pause to predict",
  teach="On hard non-fiction, speed is limited less by how fast your eyes move than by how fast you can make sense of it. Justin Sung’s strategy: read easy stretches in quick bursts, taking in two or three words at a glance, and slow down, saying it in your head, where the text is dense or the idea matters. Every paragraph or so, pause for a few seconds: what did that just say, and where is it going next? Predicting makes the next part easier to read. And when you notice you’ve read a page without taking anything in, that is passive reading: stop, go back to the last thing you understood, and pause there.",
  task="Read the next part of your chapter in bursts, and every paragraph or two stop for five seconds: one line on what it said and a guess at what comes next. Judge: where did you slow down, and was that where the important idea was?",
  co=CH, rev=OTHER, after=["R03"], watch=[FASTER, FOCUS]),
 dict(id="R06", rung="During", stage_name="No highlighter without a question", concept="Reading that feels easy isn’t the same as learning",
  teach="Highlighting is one of the most common ways people study, yet in a meta-analysis Justin Sung cites it had essentially no effect, while ten minutes of quiet rest after learning did better. The trap is the illusion of fluency: text that feels smooth feels learned, and colour makes it feel organised, while the hard part, working out how the ideas connect, gets skipped. The opposite trap is believing that effort means it isn’t working. If you want to mark something, make the mark a gate: first ask whether this is really the most important line on the page, and after marking it, ask a why or what-if question about it.",
  task="Read the next pages without marking anything until you’ve asked: is this the most important line on the page? Mark at most one line per page, and write one question beside it. Judge: how many lines would you have highlighted before, and what did choosing one make you think about?",
  co=CH, rev=OTHER, after=["R04"], watch=[HIGHLIGHT]),
 dict(id="R07", rung="After", stage_name="Digest what you consume", concept="Read less, think more about it",
  teach="Justin Sung splits reading into consuming, taking the words in, and digesting, working out what they mean, and says most people only work on the first: faster reading, double-speed audio, more books. What stays is what you digested; he cites studies suggesting most of what is only consumed is soon forgotten. So keep the two in balance. After each section, stop and process it before reading on: say what it argued in your own words, connect it to something you know, decide what you’d do with it. If there’s no time to digest, read less, not faster. Audiobooks need the same pause: they won’t stop to let you think, so you have to.",
  task="Read one section of your chapter, then close the book and spend as long digesting as you spent reading: what it argued in three sentences of your own, one link to something you already know, and one thing you’d do with it. Judge: how much could you say without looking, and what does that tell you about your usual pace?",
  co=CH, rev="a chapter you listened to", after=["R05"], watch=[REMEMBER]),
 dict(id="R08", rung="After", stage_name="Five kinds of information", concept="Each kind needs its own way of being kept",
  teach="Justin Sung sorts what you read into five kinds, PACER, because each needs different handling. Procedural, how to do something: practise it as soon as you can, not later. Analogous, like something you already know: make the analogy, then critique it: where does it hold, and where does it break? Conceptual, the what and why: map it, so you see how the ideas connect. Evidence, the facts and cases behind a concept: store them, and rehearse them later by using them in an explanation. Reference, details you only need to look up: store them, or put them on flashcards if you need them from memory. Memorising reference details while you read is the classic waste.",
  task="Take the section you just read and label each important point P, A, C, E or R. Then handle one of each kind properly: practise a P, critique an A, put a C on a mini map, note down an E or an R. Judge: which kind is most of your chapter, and how were you treating it before?",
  co=CH, rev=OTHER, after=["R06"], watch=[REMEMBER]),
 dict(id="R09", rung="Keep", stage_name="A map, not a list", concept="Notes that show how the ideas connect",
  teach="An expert’s knowledge isn’t a list in the order a book was written; it is a network, which is why they can start anywhere and still solve a problem. Justin Sung’s advice is to build that network as you read, on a mind map. Two habits get you started. Delayed note-taking: read a paragraph or a page first, then write, so your brain does the thinking in the gap. And fewer words: cut sentences down to key words, because long notes usually mean copying, not thinking. Then put the key ideas on one page and draw how they connect, with a word on each line saying how. Moving things around as you read is part of the learning.",
  task="After reading the next part of your chapter, close the book and draw a one-page map of the chapter so far: at most ten key words, lines between the ones that connect, and a word on each line saying how. Judge: which link was hardest to name, and is that where your understanding is thin?",
  co=CH, rev=OTHER, after=["R07", "R08"], watch=[MAPBEG, REMEMBER]),
 dict(id="R10", rung="Keep", stage_name="Recall it the way you’ll use it", concept="Retrieve it later, in the form you’ll need it",
  teach="A memory you can’t get back is as good as gone, and Justin Sung adds a twist: you recall best in the way you practised. Reciting flashcards doesn’t prepare you to use an idea in a decision. So retrieve the way you’ll use it: explain it to someone, apply it to your own work, answer a question you would really face. Space it out: as a loose rule, the next day, a week later and a month later. The revisits in this app do that, ten days after a sitting you nailed and three after a shaky one. Sleep is part of it too: memories consolidate overnight. If something takes many repetitions to stick, look at how you learned it.",
  task="Without the book, answer from memory: what was the main idea of the last chapter you finished, and how would you use it on one of your goals in this app? Then check that chapter’s note on your shelf. Judge: what did you miss, and would you have missed it if you’d had to use it this week?",
  co="the last chapter you finished", rev="a chapter from two weeks ago", after=["R07"], watch=[LADDER, SPACED]),
 dict(id="R11", rung="Use", stage_name="Pay for the memory you need", concept="Spend the most thinking on what you’ll use",
  teach="Justin Sung’s memory ladder asks one question of everything you learn: how much will I pay for this memory, in time and effort? At the bottom, repetition: cheap and short-lived, fine for a name or a figure. In the middle, varied retrieval: questions, summaries, explaining it. At the top, comparing, judging and synthesising: how is this like or unlike what I know, why does it matter, how does it fit the bigger picture, what model can I build from it? That costs more up front and lasts far longer. Two things make any memory stronger: relevance to a problem you have, and a link to who you want to become.",
  task="Pick one idea from your chapter that you’ll really need, and climb the ladder with it: compare it with an idea from another book on your shelf, judge whether it matters more or less than the rest of the chapter, and write one sentence linking it to the person your goal says you’re becoming. Judge: which ideas in this book are worth the top of the ladder, and which only need the bottom?",
  co=CH, rev=OTHER, after=["R09", "R10"], watch=[LADDER]),
 dict(id="R12", rung="Use", stage_name="The next book", concept="Choose the next book by your problem, not its rating",
  teach="Justin Sung screens books before committing to them: start from the problem, gather candidates, and check whether each one really tackles your problem at your level. He finds the highest-rated books aren’t always the right ones, and that summaries help you screen but can miss the details, sometimes even the point, so read the full book when it’s worth learning. When you finish a book, close it properly: what will you do differently, and which ideas earned the top of the ladder? Then pick the next one from a problem you have now. You’re allowed to drop a book that isn’t helping.",
  task="Finish or close the book you’re on with three lines: what you’ll do differently, the idea worth keeping, and one question it left open. Then write down your two biggest problems from your goals in this app and one candidate book for each. Judge: which would you start tomorrow, and why that one?",
  co="your next book", rev="a book for your career", after=["R10"], watch=[BOOKS]),
]
for x in L:
    x["estimateMin"] = 20   # the Reading goal's own 20 minutes
    x["rung"] = "Read better"   # the reading techniques come after the books, as an optional last part
    x.pop("after", None)

# ---- the books: every chapter note on the bookshelf (articles/book-*.md) becomes a sitting ---------------------------
# Guess what the chapter says, read the note (or listen to that chapter), write the idea and one action for tomorrow from
# memory, check it against the chapter's points. The action comes back at the next sitting as "did you do it?".
# A note added later (from the audiobooks on the PC) becomes a sitting the next time this script runs; ids are per book
# and per note number, so a new book never renumbers the sittings you've done.
import glob, json, re
ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "articles")
BOOKS_IN_ORDER = [  # book (as in the note's channel), id letter, what it's for
    ("Atomic Habits", "A", "James Clear: small habits, made obvious, attractive, easy and satisfying"),
    ("Eat That Frog!", "E", "Brian Tracy: the most important task first, every day"),
    ("The Richest Man in Babylon", "Y", "George S. Clason: pay yourself first, and make your money work"),
    ("Zero to One", "Z", "Peter Thiel: start small, own a market, build something new"),
    ("The Mom Test", "M", "Rob Fitzpatrick: ask about their life, not your idea"),
    ("$100M Offers", "O", "Alex Hormozi: an offer so good people feel stupid saying no"),
]
norm = lambda t: re.sub(r"[^a-z0-9$]", "", t.lower())
def plain(t):
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return re.sub(r"\*\*?([^*]+)\*\*?", r"\1", t).replace("`", "").strip()
def item(line):
    m = re.match(r"\*\*(.+?)\*\*\s*(.*)", line)
    return [plain(m.group(1)), plain(m.group(2))] if m and m.group(2) else plain(line)
def parse_note(path):
    raw = open(path, encoding="utf-8").read()
    fm, body = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S).groups()
    meta = dict(re.findall(r"^(\w+):\s*(.*)$", fm, re.M))
    teach, idea, tryit, walk, cur = "", "", "", [], None
    for blk in re.split(r"\n\s*\n", body.strip()):
        lines = [x.rstrip() for x in blk.strip().split("\n") if x.strip()]
        if lines[0].startswith("## "):
            cur = {"h": plain(lines[0][3:]), "l": [], "p": []}; walk.append(cur); lines = lines[1:]
        m = re.match(r"\*\*(.+?)\*\*\s*(.*)", lines[0]) if lines else None
        if m and not lines[0].startswith(("- ", "|")) and len(lines) == 1:
            label, text = m.group(1).rstrip(".").lower(), plain(m.group(2))
            if "idea worth keeping" in label: idea = text; continue
            if label.startswith("try it"): tryit = text; continue
            if not teach and not walk: teach = text; continue
        for ln in lines:
            if cur is None: cur = {"h": "In short", "l": [], "p": []}; walk.append(cur)
            if re.match(r"^\|[\s:-]+\|", ln) and set(ln) <= set("|:- "): continue   # a table's separator row
            if ln.startswith("|"): cur["l"].append(" · ".join(plain(c) for c in ln.strip("|").split("|") if c.strip())); continue
            mm = re.match(r"^(?:- |\d+\. )(.*)", ln)
            cur["l"].append(item(mm.group(1))) if mm else cur["p"].append(plain(ln))
    walk = [{k: v for k, v in w.items() if v} for w in walk]
    return meta, teach, idea, tryit, [w for w in walk if w.get("p") or w.get("l")]
notes = {}
for path in glob.glob(os.path.join(ART, "book-*.md")):
    meta, teach, idea, tryit, walk = parse_note(path)
    notes.setdefault(norm(meta["channel"]), []).append((int(meta["n"]), meta, teach, idea, tryit, walk))
known = {norm(b) for b, _, _ in BOOKS_IN_ORDER}
assert set(notes) <= known, ("a book on the shelf isn't in BOOKS_IN_ORDER", set(notes) - known)
first_sentence = lambda t: re.split(r"(?<=[.!?])\s", t.strip(), 1)[0]
BOOK_L, BOOK_RUNGS, BOOK_DESC = [], [], []
# Building products lives here now: its nine lessons were the Zero to One and Mom Test chapters used on your own idea, so
# each of those chapters carries that lesson's task, worked example, good-answer check and revisit (reading-apply.json).
APPLY = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "reading-apply.json"), encoding="utf-8"))
LISTEN = {"h": "How to listen", "l": ["At a speed you can follow, not double speed: digesting it is what makes it stick.", "Pause after each big idea and say it back in one sentence, out loud or in your head.",
                                       "Link it to something you already know, and say the link.", "Drifted off? Go back 30 seconds rather than pushing on."]}
def bare(h): return re.sub(r"^(?:Chapters?|Ch\.)\s*[\d–-]+:\s*", "", h).strip()
def cap(s): return s[:1].upper() + s[1:]
for book, letter, desc in BOOKS_IN_ORDER:
    ns = sorted(notes.get(norm(book), []), key=lambda x: x[0])
    if not ns: continue
    BOOK_RUNGS.append(book); BOOK_DESC.append(desc)
    for i, (n, meta, teach, idea, tryit, walk) in enumerate(ns):
        lid = "%s%02d" % (letter, n % 100); part = meta.get("part", "") or "this chapter"; title = plain(meta["title"])
        if len(teach) < 150: teach = (teach + " " + idea).strip()
        if len(teach) < 150 and tryit: teach = (teach + " " + tryit).strip()
        pts = []
        for w in walk:
            for it in w.get("l", []):
                pts.append((it[0] + ": " + first_sentence(it[1])) if isinstance(it, list) else first_sentence(it))
        heads = [w["h"] for w in walk if w["h"] != "In short"]
        ap = APPLY.get(lid)
        act = tryit or "Pick the one line of this chapter you’d act on, and do it tomorrow."
        # the brief: listen first, then the work; a chapter that carries a product lesson asks you to use it on your idea
        if ap:
            do, judge = (ap["task"].split(" Judge: ", 1) + [""])[:2]
            task = ("Listen to %s of the audiobook, pausing to say each idea back. Then, from memory: %s End with one action for tomorrow, as ‘After I …, I will …’." % (part, do)
                    + (" Judge: " + judge if judge else ""))
        else:
            task = ("Before you press play, guess what this part says about ‘%s’. Listen to %s of the audiobook, pausing to say each idea back. Then, from memory, write the idea in your own words and one action for tomorrow, as ‘After I …, I will …’. Judge: which line of it would change what you do this week?" % (title, part))
        terms = [it[0].rstrip(".") for w in walk for it in w.get("l", []) if isinstance(it, list)][:5]   # the note's key terms, in bold
        one = len(heads) <= 1
        lw = [{"h": "The map, before you press play", "p": ["%s of %s%s. Keep %s in mind while you listen: %s where each idea will land." % (cap(part), book, "" if one else ", in %d parts" % len(heads), "it" if one else "them", "it’s" if one else "they’re")],
               "l": [cap(bare(h)) for h in heads] or [title]},
              {"h": "Listen for", "l": ["%s: what’s the claim, and the reason or example behind it?" % cap(bare(h)) for h in heads[:3]]
                   + (["These terms, and what each one means: %s." % "; ".join(terms)] if terms else [])}]
        lw[1]["l"] = lw[1]["l"] or ["The one claim this part makes, and the reason behind it."]
        lw += [
              LISTEN,
              {"h": "Can’t listen now? The chapter note", "fold": walk + ([{"h": "The idea worth keeping", "p": [idea]}] if idea else [])}]
        if ap: lw += ap["walk"]
        lw.append({"h": "Your turn: %s" % part, "p": ["Play %s, %s, in the audiobook, with the map above in mind. Then say the idea in one line." % (book, part),
                                                     ("Next, use it on your idea: Intensity Applied, or whichever idea you’d most like to build." if ap else act + " Write it as ‘After I …, I will …’, small enough to do in two minutes.")]})
        key = (ap["key"] if ap else []) + [{"t": "The chapter in short", "l": pts[:6] or [teach]}] + ([{"t": "The idea worth keeping", "l": [idea]}] if idea else [])
        les = dict(id=lid, rung=book, stage_name=meta.get("part", "") or ("Note %d" % n), concept=title, estimateMin=30, teach=teach, task=task, co=book, rev=book,
                   walk=lw, key=key,
                   thread={"n": ("%s%02d · %s" % (letter, ns[i + 1][0] % 100, plain(ns[i + 1][1]["title"]))) if i + 1 < len(ns) else "the next book on your shelf"},
                   rtask=(ap["rtask"][:1].upper() + ap["rtask"][1:]) if ap else "From memory: this chapter’s idea in two lines, and the action you chose. Did it stick?",
                   rkey=ap["rkey"] if ap else [{"t": "Short answer", "l": [idea or teach]}],
                   read=["Listen: %s, %s, in the audiobook" % (book, part), "Or read: the chapter note, under ‘Can’t listen now?’ in step 2"])
        if i: les["thread"]["b"] = "%s%02d · %s" % (letter, ns[i - 1][0] % 100, plain(ns[i - 1][1]["title"]))
        elif BOOK_L: les["thread"]["b"] = "the previous book, %s" % BOOK_L[-1]["co"]
        BOOK_L.append(les)
assert set(APPLY) <= {x["id"] for x in BOOK_L}, "a product lesson's chapter is missing from the shelf"
for x in BOOK_L:   # a chapter keeps to its own book: no pointers to other lessons in what it shows
    for sec in x["walk"] + [s for w in x["walk"] for s in w.get("fold", [])]:
        for t in [sec.get("h", "")] + sec.get("p", []) + [" ".join(q) if isinstance(q, list) else q for q in sec.get("l", [])]:
            assert not re.search(r"\b(?:P|Z|M|O|A|E|Y|B)\d\d\b", t), (x["id"], "points at another lesson", t)
L = BOOK_L + L

C = course({"goal_id": "goal_read", "key": "read", "title": "Your books, one chapter a sitting", "azTitle": "Your books, A → Z",
     "rungs": BOOK_RUNGS + ["Read better"],
     "rungDesc": BOOK_DESC + ["the reading techniques: a time and a place, priming, sprints, PACER, maps, retrieval, the next book"],
     "blurb": "One chapter per sitting, made for the audiobook, in Justin Sung’s four steps: guess what it says and look at its map, listen with the map in mind and pause to say each idea back, write it from memory, then check it. A chapter longer than today’s slot runs in two halves: listen one day, write and check the next. The Zero to One and Mom Test chapters ask you to use them on your own idea (they used to be the Building products course). The reading techniques come last, under Read better.",
     "allDone": "now add the next book to your shelf. 📖",
     "revWord": "the same chapter, a week on",
     "refNote": "Guess first: the map opens in step 2. The chapter notes are in my words, from the books, folded away under ‘Can’t listen now?’; the audiobooks on your PC are the full text."}, L)
check_videos(C)
check_extras(C["lessons"])
write("READ_CURRICULUM", ["Read so it sticks — your books, one chapter a sitting (one per note on the bookshelf, in the order of BOOKS_IN_ORDER),\n     then 12 reading techniques under Read better, in my words from Justin Sung's videos in the youtube-digest",
      "library and the Atomic Habits notes on the bookshelf: a time and a place, the two-minute start, priming, reading for a problem,",
      "sprints and pauses, highlighting, consume vs digest, PACER, mind maps, retrieval, the memory ladder and choosing the next book.",
      "Each runs on the chapter you're reading, at 20 minutes. Built by scripts/build-reading-course.py."], C)
