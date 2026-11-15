# Builds "Read so it sticks" (READ_CURRICULUM) in time-tracker.html: 12 sittings on the Reading goal, each one reading
# technique used straight away on the chapter you're reading, inside your daily minutes (14 on weekdays in the round, the
# goal's own 20 at weekends). Written in my words from Justin Sung's videos in the youtube-digest library (priming, reading
# in bursts, highlighting, consume vs digest, PACER, mind maps, retrieval, the memory ladder, choosing books), and from the
# Atomic Habits chapter notes on your bookshelf for the habit itself.
#   python3 scripts/build-reading-course.py       -> rewrites the block in time-tracker.html
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from course_block import yt, course, check_videos, write

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

C = course({"goal_id": "goal_read", "key": "read", "title": "Read so it sticks", "azTitle": "Read so it sticks, A → Z",
     "rungs": ["Habit", "Before", "During", "After", "Keep", "Use"],
     "rungDesc": ["a time and a place, two minutes to start, never miss twice", "prime the chapter, and know the problem you’re reading for",
                  "sprints and pauses, and no highlighter without a question", "digest what you consume, and the five kinds of information",
                  "a map of the ideas, and recall the way you’ll use it", "pay for the memory you need, and choose the next book"],
     "blurb": "One reading technique per sitting, used straight away on the chapter you’re reading, inside your daily minutes. Written in my words from Justin Sung’s videos in your library and the Atomic Habits notes on your shelf; plain reading on its own clock still counts.",
     "allDone": "now just read, with the method. 📖",
     "revWord": "another chapter",
     "refNote": "The idea opens in step 2 of the sitting — guess first. The videos are Justin Sung’s, for when you want more; the notes are on your bookshelf, below on this page."}, L)
check_videos(C)
write("READ_CURRICULUM", ["Read so it sticks — 12 sittings on the Reading goal, in my words from Justin Sung's videos in the youtube-digest",
      "library and the Atomic Habits notes on the bookshelf: a time and a place, the two-minute start, priming, reading for a problem,",
      "sprints and pauses, highlighting, consume vs digest, PACER, mind maps, retrieval, the memory ladder and choosing the next book.",
      "Each runs on the chapter you're reading, at 20 minutes. Built by scripts/build-reading-course.py."], C)
