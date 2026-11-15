# Builds "Building products" (PROD_CURRICULUM) in time-tracker.html: 9 sittings on the Building products goal, from
# Zero to One (Thiel), The Mom Test (Fitzpatrick) and videos in the youtube-digest library, in my words. Every sitting
# runs on the idea you've starred on the idea board ({idea}); the worked examples are real cases from the sources, and
# the good answers use Intensity Applied, your own app, as the example. Market, offer and price used to be lessons here;
# they live in the Business course now (B01, B03, B06), so this course points there instead of repeating them.
#   python3 scripts/build-products-course.py       -> rewrites the PROD_CURRICULUM object in time-tracker.html
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from course_block import yt, course, check_videos, check_extras, term_order, lesson_texts, HTML

SS = "Starter Story"
FASTLANE = yt("BA_fC95p43c", SS, "How This SaaS Hit $69K/Month In Just 2 Months", "2,000 customer calls using the Mom Test, and how they narrowed an all-in-one tool to one job")
CLEO = yt("XifgHi9R5Rc", SS, "How My App Hit $60K/Month in 2 Months", "waitlist first, a paid beta for the list, no public launch")
MAP = yt("jJIOA4GroBw", "Greg Isenberg", "\"Learn AI” Is Bad Advice. Learn This Instead", "the distribution map and the 48-hour loop")
FIRST100 = yt("l4WEqPX52Cg", SS, "How This $250K/Month SaaS Got Its First 100 Users (Steal This Playbook)", "the founder’s three-step playbook")
PERFECT = yt("3fsJFUvA6Ts", "Alex Hormozi", "What Makes The Perfect Business (5 Things)", "the fifth thing, “unique”: capital, know-how and brand as moats")
def src(v): return {"s": v["t"], "u": v["u"]}

# a worked number in P06: an app at €5 a month, kept 6 months, won by hand at 30 minutes and your €40 an hour (Business B07)
PRICE_M, MONTHS, RATE, HOURS = 5, 6, 40, 0.5
LTV = PRICE_M * MONTHS; CAC = RATE * HOURS; RATIO = LTV / CAC

L = [
 dict(id="P01", rung="Find", stage_name="New or copy?", concept="Zero to one, or one to n",
  teach="Going from 0 to 1 makes something new; going from 1 to n copies what already works into more places. Copying is easier to start but crowded. Most solo founders’ first products are 1 to n, a known product done better for a narrow group, and that works if you know which one you’re doing and what you do better.",
  task="Is {idea} a 0-to-1 or a 1-to-n idea? Answer Thiel’s question for its area in one sentence. Judge: if it’s 1 to n, what do you do that the ones you copy don’t? If you can’t name it, that’s the first gap. Try it this week: find the three closest products to {idea} and write what each one gets wrong.",
  read=["Zero to One, ch. 1 (The Challenge of the Future)"],
  walk=[{"h": "Two kinds of progress", "l": [["0 to 1.", "Something new. Thiel calls it vertical progress: technology."], ["1 to n.", "Something known, copied into more places or done better for a narrower group. Horizontal progress: globalisation."]]},
        {"h": "Thiel’s question", "p": ["What important truth do very few people agree with you on? For a product, narrow it: what do you know about these customers that the products they use today miss?"]},
        {"h": "Where it goes wrong", "l": ["Calling a copy new.", "Copying with no reason to win: the same product, for the same people, with a smaller budget."]},
        {"h": "Worked: an app like Intensity Applied", "p": ["An app for lifters who want to build muscle is 1 to n: training apps and logbooks already exist. That’s fine. The work is the gap: a group the big apps serve badly, such as lifters who have stalled for months, and the one thing done for them that the others don’t do."]},
        {"h": "Your turn: {idea}", "p": ["0 to 1 or 1 to n; Thiel’s question in one sentence; the three closest products, and what each gets wrong."]}],
  key=[{"t": "A good answer looks like", "l": ["One word first: ‘1 to n’, for most first products.",
        "One sentence naming a group and a gap, e.g. ‘lifters who’ve stalled for months get generic programmes; nobody shows them which variable to change next’.",
        "Three named competitors, each with one specific miss taken from a user’s complaint (an app review, a forum post), not from your guess."]}],
  thread={"n": "P02 · how small the first market should be"},
  rtask="{idea}: 0 to 1 or 1 to n, and the one thing it would do that the closest product doesn’t.",
  rkey=[{"t": "Short answer", "l": ["Most are 1 to n. The answer is one specific gap for one group, taken from a real complaint about the closest product; if you can’t name one, that’s the finding."]}]),
 dict(id="P02", rung="Find", stage_name="Start small", concept="Own a tiny market first",
  teach="Competition eats profits, so start by owning a small market and only then grow: Amazon started with books, PayPal with eBay’s power sellers, Facebook with one college. ‘We only need 1% of a huge market’ is a trap: you start in a fight with everyone.",
  task="Write {idea}’s smallest real market in one sentence: who, doing what, where. Roughly how many of them are there, and how would you reach the first 100? Judge: is it small enough that you’d be their obvious choice, but big enough to matter? Try it this week: message three people in that group.",
  read=["Zero to One, ch. 3 and ch. 5 (“start small and monopolize”)", "The Mom Test, ch. 7 (Choosing your customers)"],
  walk=[{"h": "Why small", "p": ["A small market you can own beats a big one you share: you become the obvious choice, word travels inside the group, and you learn fast from people who all have the same problem."]},
        {"h": "How small", "l": [["One sentence.", "Who, doing what, where: precise enough that a stranger could find them."], ["Small enough to own.", "You could be their first choice within a year."], ["Big enough to matter.", "Enough of them for your first goal, with the next market next door."], ["One problem.", "If the people you talk to (P03) don’t share the same problem, the group is still too broad."]]},
        {"h": "Where it goes wrong", "l": ["The 1% of a huge market.", "A group so broad that no single place reaches it.", "Skipping the market tests: pain, money, easy to find, growing (Business B01)."]},
        {"h": "Worked: PayPal", "p": ["PayPal didn’t start with everyone who pays online. It started with eBay’s power sellers: a small group who traded every day and talked to each other. Once they used it, the rest of eBay followed. Thiel’s rule: dominate a small market, then expand to the one next to it."]},
        {"h": "Your turn: {idea}", "p": ["Its smallest real market in one sentence, a rough count with where the count comes from, and how you’d reach the first 100."]}],
  key=[{"t": "A good answer looks like", "l": ["Who, doing what, where, e.g. ‘lifters training 3–5 times a week who’ve stalled for six months, in strength-training communities online’.",
        "A rough count with its source, like a community’s member count or an association’s list. A guess with a source beats a big number without one.",
        "A plan for the first 100 that names the place and the message, not ‘social media’."]}],
  thread={"b": "P01 · the gap you’d fill; Business B01–B02 · the four market tests, and the niche", "n": "P03 · asking these people about their lives"},
  rtask="{idea}: its smallest real market in one sentence, and where the first 100 gather.",
  rkey=[{"t": "Short answer", "l": ["Who, doing what, where, in one sentence, plus a named place where they gather. If the place is ‘online’, the group is still too broad."]}]),
 dict(id="P03", rung="Test", stage_name="The Mom Test", concept="Ask about their life, not your idea",
  teach="Ask your mom if your idea is good and she’ll say yes, because she loves you, and everyone else is polite too. Three rules fix it: talk about their life, not your idea; ask about specific things that already happened, not opinions about the future; talk less and listen.",
  task="Write three bad questions and three good ones for {idea}, then rewrite each bad one into a good one. Judge: which good question is most likely to show you you’re wrong? Try it this week: ask it to two real people, and add them to “talked to” on the idea board.",
  read=["The Mom Test, ch. 1 (The Mom Test)"], watch=[FASTLANE],
  walk=[{"h": "The three rules", "l": [["Their life, not your idea.", "Don’t mention the idea until you have to."], ["The past, not the future.", "What they did last time, not what they would do."], ["Listen.", "If you talk more than they do, it’s a pitch."]]},
        {"h": "Bad questions, rewritten", "l": ["‘Would you use this?’ → ‘Walk me through the last time this happened.’", "‘How much would you pay?’ → ‘What does it cost you now, and what have you tried?’", "‘Is this a good idea?’ → ‘Why haven’t you solved it already?’"]},
        {"h": "Where it goes wrong", "l": ["Pitching and calling it research.", "Counting compliments as demand (P04)."]},
        {"h": "Worked: Fastlane", "p": ["Its founders ran about 20 of these calls a week, about 2,000 in all, and found their product in what people already did: they narrowed an all-in-one tool down to one job. It reached $69K a month within two months."], **src(FASTLANE)},
        {"h": "Your turn: {idea}", "p": ["Three bad questions and three good ones, each bad one rewritten; then the one most likely to show you’re wrong."]}],
  key=[{"t": "A good answer looks like", "l": ["Good questions start with ‘the last time’, ‘walk me through’, ‘what have you tried’, ‘what did it cost’. For Intensity Applied: ‘When did your lifts last go up? What did you change after that?’",
        "Bad ones mention the product or ask about the future: ‘Would you pay for an app that…’.",
        "The one most likely to prove you wrong: ‘What have you tried to fix it?’ If the answer is ‘nothing’, the pain may not be real."]}],
  thread={"b": "P02 · the small group to talk to", "n": "P04 · sorting what they tell you"},
  rtask="{idea}: one bad question rewritten into a good one, and the question most likely to prove you wrong.",
  rkey=[{"t": "Short answer", "l": ["The good version asks about a specific past event (‘the last time…’). The riskiest question is usually ‘what have you tried?’: no attempts, no real pain."]}]),
 dict(id="P04", rung="Test", stage_name="Bad data", concept="Compliments, fluff and feature requests",
  teach="Three things feel like progress and aren’t: compliments, fluff and feature requests. Deflect the compliment, anchor the fluff in the last real time it happened, and dig under a feature request by asking why. A chat that felt great but taught you no fact about their life was a pitch.",
  task="Take three reactions you’ve had to {idea} — or typical ones: “Nice!”, “I’d use that”, “It should have X”. Sort each into compliment, fluff or idea, and write the follow-up question that turns it into a fact. Judge: what’s the one fact about your customer you still don’t know? Try it this week: get that fact from one person.",
  read=["The Mom Test, ch. 2 (Avoiding bad data)"],
  walk=[{"h": "The three", "l": [["Compliments.", "‘That’s cool.’ Deflect, and get back to their life."], ["Fluff.", "‘I usually’, ‘I would’, ‘I might’: ask for the last real time."], ["Feature requests.", "‘It should have X’: ask why, and what they do without it today."]]},
        {"h": "Where it goes wrong", "l": ["Leaving on a high with nothing written down.", "Building the requested feature instead of finding the reason behind it."]},
        {"h": "Worked: three reactions, turned into facts", "l": ["‘Nice idea!’ is a compliment: ‘Thanks. How do you handle it today?’", "‘I’d use that every week’ is fluff: ‘When did you last need it? What did you do?’", "‘It should sync with my watch’ is a request: ‘What would that let you do that you can’t now?’"]},
        {"h": "Your turn: {idea}", "p": ["Three reactions you’ve had, or typical ones: sort each, write its follow-up, and name the one fact you still don’t know."]}],
  key=[{"t": "A good answer looks like", "l": ["Each reaction labelled, then followed by a question about the past or about why.",
        "The missing fact is about their life, not your product. For Intensity Applied, e.g.: how many lifters who stall actually change anything, and what.",
        "Getting it from one person this week counts. A survey of opinions doesn’t."]}],
  thread={"b": "P03 · the questions that get facts", "n": "P05 · asking for a commitment"},
  rtask="{idea}: the most common compliment or ‘I would’ you’ve heard, and the question that turns it into a fact.",
  rkey=[{"t": "Short answer", "l": ["Anchor it in the past: ‘When did that last happen? What did you do?’ A fact is something that already happened, with a cost or a time attached."]}]),
 dict(id="P05", rung="Test", stage_name="Commitment", concept="Time, reputation, money",
  teach="A conversation only counts if it ends with a commitment, because a commitment is how people tell you the truth. It comes in three currencies: time, reputation and money. ‘That went well’ with no next step is a zombie lead.",
  task="For {idea}, write the commitment you’ll ask for at each stage: after a first chat, after a demo, and before you build the full product. Judge: what’s the smallest money commitment that would really prove demand? Try it this week: ask one person for it.",
  read=["The Mom Test, ch. 5 (Commitment and advancement)"], watch=[CLEO],
  walk=[{"h": "Three currencies", "l": [["Time.", "A follow-up call, trying the beta, a session with you watching."], ["Reputation.", "An introduction to a friend or colleague, a public testimonial."], ["Money.", "A pre-order, a deposit, a paid pilot."]]},
        {"h": "By stage", "l": ["After a first chat: a second meeting, or an introduction.", "After a demo: using it for a week, with you watching once.", "Before you build the full thing: money, even a small amount."]},
        {"h": "Where it goes wrong", "l": ["Not asking, to keep the meeting pleasant.", "Treating ‘sounds great, keep me posted’ as a yes."]},
        {"h": "Worked: Cleo", "p": ["Cleo built a waitlist from LinkedIn posts and sold its paid beta only to that list: about $30K a month within days, before any public launch. Joining the waitlist cost people time; the paid beta cost money."], **src(CLEO)},
        {"h": "Your turn: {idea}", "p": ["The commitment you’ll ask for after a first chat, after a demo, and before you build; then the smallest money one that would prove demand."]}],
  key=[{"t": "A good answer looks like", "l": ["Three asks, one per stage, each one something they could say no to.",
        "A real, small money ask. For Intensity Applied, e.g.: a founding-member year at a discount, paid before launch, offered only to the waitlist.",
        "The result that would stop you, in numbers, decided now: e.g. fewer than 3 of 10 people who saw the demo pay."]}],
  thread={"b": "P04 · facts, not compliments", "n": "P06 · where to find many more of these people"},
  rtask="{idea}: the smallest money commitment that would prove demand, and the result that would stop you.",
  rkey=[{"t": "Short answer", "l": ["A real payment they could refuse: a pre-order, a deposit, a paid beta. The stopping result is a number decided now, e.g. fewer than 3 of 10."]}]),
 dict(id="P06", rung="Reach", stage_name="Distribution", concept="If you build it, they won’t just come",
  teach="Poor sales, not a poor product, is the most common reason companies fail. A customer has to be worth more over their lifetime than they cost to win, and the trap is the middle: too cheap to sell person to person, too small for ads to pay. Know where your customers’ attention already is before you build.",
  task="Make a distribution map for {idea}: 20 places its customers already pay attention — subreddits, creators, newsletters, groups, search terms, tools they pay for. Pick one channel for the first 100 users. Judge: what will one customer cost you there, and what will they pay you in a year? Try it this week: post or reply once in that channel.",
  read=["Zero to One, ch. 11 (If You Build It, Will They Come?)"], watch=[MAP],
  walk=[{"h": "Thiel’s ladder, by price", "l": [["Big deals.", "Large contracts, sold by the founder one at a time."], ["Personal sales.", "Smaller deals, each worth a salesperson’s time."], ["The doldrums.", "Too cheap to sell by hand, too small for ads to pay."], ["Marketing and viral.", "Cheap products sold to many: ads, word of mouth, sharing built in."]]},
        {"h": "The distribution map", "p": ["Greg Isenberg’s version: before you build, list 20 places your customers already pay attention, and the words they use for their problem there. Then pick one channel for the first 100."], **src(MAP)},
        {"h": "The numbers", "l": ["What a customer is worth: price × months they stay.", "What one costs to win: your hours × your rate, plus any spend, ÷ the customers it brings.", "Healthy: worth at least three times what they cost (Business B13)."]},
        {"h": "Where it goes wrong", "l": ["Posting everywhere instead of doing one channel well.", "A €5-a-month app, sold one person at a time."]},
        {"h": "Worked: an app at €%d a month" % PRICE_M, "p": ["A user who stays %d months is worth €%d. Winning each one by hand, even %d minutes at your €%d an hour, costs €%d: only %.1f times, in the doldrums. So the channel has to be nearly free per user: a community where one post reaches thousands, or users who bring other users." % (MONTHS, LTV, HOURS * 60, RATE, CAC, RATIO)]},
        {"h": "Your turn: {idea}", "p": ["A map of 20 places, one channel picked, what a customer costs you there, and what they pay you in a year."]}],
  need=[{"k": "Your rate (Business B07)", "v": "€%d an hour" % RATE, "n": "What an hour of your time is worth, for working out what a customer costs to win."}],
  key=[{"t": "A good answer looks like", "l": ["20 named places, not categories: that subreddit, that newsletter, that creator, that search phrase.",
        "One channel and why: the group already talks about the problem there, in its own words.",
        "Two numbers: the cost to win one customer there, and a year’s revenue from one. The second should be at least three times the first; at €%d a month that means winning each user for under €%d." % (PRICE_M, PRICE_M * 12 // 3)]}],
  thread={"b": "P05 · people who’ve committed; Business B13 · what a customer is worth against what one costs", "n": "P07 · the first 100, by hand"},
  rtask="{idea}: one channel for the first 100, what a customer costs you there, and what one pays you in a year.",
  rkey=[{"t": "Short answer", "l": ["A year’s revenue should be at least three times what one customer costs to win. At a low monthly price, the channel has to be nearly free per user."]}]),
 dict(id="P07", rung="Reach", stage_name="The first 100", concept="Do things that don’t scale",
  teach="The first 100 users come by hand: catch the people already searching, do things that don’t scale for each early user, and show up where your users already are. Launch early: speed is the one advantage a small founder has.",
  task="Write {idea}’s first-100 plan: who is already searching for a solution, one thing that doesn’t scale you’d do for each early user, and where you’ll show up. Judge: which step gets you the first 10, and how fast? Try it this week: do the unscalable thing for one person.",
  read=["Zero to One, ch. 11 (the sales methods)"], watch=[FIRST100],
  walk=[{"h": "Three steps", "l": [["Catch the searchers.", "Comparison pages and free tools, for people already looking for a fix."], ["Do things that don’t scale.", "Help each early user by hand, in public where others can see it."], ["Show up.", "In the places on your map (P06), as a member first."]]},
        {"h": "Where it goes wrong", "l": ["Waiting for a launch day.", "Automating something before you’ve done it by hand ten times."]},
        {"h": "Worked: Super Demo", "p": ["Its founder talked to more than 100 founders before building, then made free demos for founders who asked on Reddit, in public, so others saw them. It is now at $250K a month."], **src(FIRST100)},
        {"h": "Your turn: {idea}", "p": ["Who is already searching, one unscalable thing for each early user, where you’ll show up; and which of the three gets you the first 10."]}],
  key=[{"t": "A good answer looks like", "l": ["For Intensity Applied, e.g.: lifters searching ‘plateau’ or ‘stalled bench press’ (searchers); a free review of someone’s last eight weeks of training, posted with permission (unscalable, and public); the communities from P06 (show up).",
        "The first 10 usually come from the unscalable step: one person at a time, starting this week.",
        "A date for the first 10, and what you’ll do if they aren’t in by then."]}],
  thread={"b": "P06 · the one channel", "n": "P08 · what keeps it yours once it works"},
  rtask="{idea}: one thing that doesn’t scale you’d do for each of the first 10 users.",
  rkey=[{"t": "Short answer", "l": ["Something personal and visible: a free review, a done-with-you setup, a reply in public. If it takes more than an hour each, make it smaller, not automated."]}]),
 dict(id="P08", rung="Keep", stage_name="Moats", concept="What keeps it yours",
  teach="Four things keep a business yours: technology at least 10 times better at something important, network effects, economies of scale, and brand. A small product rarely has one on day one; the question is which one it could build, starting now.",
  task="Which of the four could {idea} have in five years — honestly? Name it, and what you’d have to do from day one to build it. Judge: if a funded competitor copied {idea} next month, what would they still not have? Try it this week: write that answer as your one-line pitch.",
  read=["Zero to One, ch. 5 (Last Mover Advantage)"], watch=[PERFECT],
  walk=[{"h": "Thiel’s four", "l": [["Proprietary technology.", "10 times better at the thing that matters, not a bit better."], ["Network effects.", "Each user makes it better for the others."], ["Economies of scale.", "Cheaper per customer the bigger you get."], ["Brand.", "Built on the other three, not instead of them."]]},
        {"h": "Hormozi’s fifth thing", "p": ["If anyone can start your business tomorrow, the price falls. The best protection is what only you know how to do: know-how, capital, a name."], **src(PERFECT)},
        {"h": "Where it goes wrong", "l": ["Calling ‘first’ a moat: Thiel argues the last mover wins.", "A brand with nothing underneath it."]},
        {"h": "Worked: an app like Intensity Applied", "l": ["Technology 10 times better is hard: most training logic is public.", "Network effects are weak, unless many lifters’ data makes the advice better for each one.", "Scale: software is cheap to serve, but so is every rival’s.", "So the likeliest moat is that data, built from day one by logging what each lifter changed and what happened next."]},
        {"h": "Your turn: {idea}", "p": ["Which of the four it could have in five years, what you’d do from day one, and what a funded copycat still wouldn’t have next month."]}],
  key=[{"t": "A good answer looks like", "l": ["One moat, chosen honestly. ‘None yet’ is fine if you name the one you’ll build.",
        "A day-one action that starts it: logging the data, starting the community, owning the niche’s name.",
        "The copycat line, written as your one-line pitch: what they’d still lack next month."]}],
  thread={"b": "P07 · the first users", "n": "P09 · scoring every idea against all of this"},
  rtask="{idea}: which moat could it build, and what’s the first step this month?",
  rkey=[{"t": "Short answer", "l": ["One of Thiel’s four, or Hormozi’s know-how, with a concrete first step. ‘None yet’ counts if you name the one you’ll build."]}]),
 dict(id="P09", rung="Decide", stage_name="The seven questions", concept="Score it, pick one, set a kill rule",
  teach="Thiel’s seven questions for any new business: engineering, timing, monopoly, people, distribution, durability and a secret. You don’t need seven yeses, but every ‘no’ is a risk you’re choosing. Score every idea, pick one, and write the result that would make you drop it.",
  task="Score every idea on your idea board on the seven questions. Pick the one to test next, and write the result that would make you drop it — for example, fewer than 3 of 10 people commit. Judge: is your favourite also the best-scoring one? If not, why? Try it this week: run its test.",
  read=["Zero to One, ch. 13 (Seeing Green)"],
  walk=[{"h": "The seven", "l": [["Engineering.", "Clearly better, not a bit better? (P01)"], ["Timing.", "Why now?"], ["Monopoly.", "A big share of a small market? (P02)"], ["People.", "The skills, or the team, to build it?"], ["Distribution.", "A way to reach customers, not just to build? (P06–P07)"], ["Durability.", "Still yours in 10 years? (P08)"], ["Secret.", "Something others don’t see? (P01)"]]},
        {"h": "The kill rule", "p": ["Before you test, write the result that would make you drop the idea: e.g. fewer than 3 of 10 people commit (P05). Decided before, it’s a test; decided after, it’s a story."]},
        {"h": "Where it goes wrong", "l": ["Scoring your favourite generously.", "No kill rule, so nothing ever fails and nothing gets dropped."]},
        {"h": "Worked: the cleantech bust", "p": ["Thiel blames the cleantech crash of the late 2000s on companies that answered few of the seven well: no clearly better technology, bad timing, crowded markets, weak sales, no secret. Solyndra is the main example in the book."]},
        {"h": "Your turn: your idea board", "p": ["Score every idea on the seven, pick the one to test next, and write its kill rule."]}],
  key=[{"t": "A good answer looks like", "l": ["A table of ideas × the seven, yes or no (or 1–5), with the weakest question for each idea named.",
        "The pick, and if it isn’t the top score, the reason in one line.",
        "A kill rule with a number and a date: e.g. ‘fewer than 3 of 10 pay for the founding year within six weeks: drop it’."]}],
  thread={"b": "P01–P08 · each question has a lesson behind it", "n": "your next test, with the kill rule written first"},
  rtask="{idea}: score it on the seven questions and write its kill rule.",
  rkey=[{"t": "Short answer", "l": ["Seven answers with the weakest one named, and a kill rule with a number and a date, written before the test."]}]),
]

GLOSSARY = [
    (3, "the Mom Test", r"Mom Test"), (4, "fluff", r"\bfluff\b"), (5, "zombie lead", r"zombie"),
    (6, "the doldrums", r"doldrums"), (6, "distribution map", r"distribution map"), (7, "things that don’t scale", r"don’t scale|unscalable"),
    (8, "moat", r"\bmoats?\b"), (8, "network effects", r"network effects?"), (9, "kill rule", r"kill rule"), (9, "the seven questions", r"seven questions"),
]

def check():
    e = lambda a, b, tol=0.01: abs(a - b) <= tol or sys.exit(f"bad number: {a} vs {b}")
    e(LTV, 30); e(CAC, 20); e(RATIO, 1.5); e(PRICE_M * 12 // 3, 20)
    for x in L:
        for where, t in lesson_texts(x) + [("concept", x["concept"])]:
            assert not re.search(r"\b(he|him|his|himself)\b", t, re.I), (x["id"], where, "pronoun", t)
check()

C = course({"goal_id": "goal_build", "key": "prod", "title": "Building products", "azTitle": "Building products, A → Z",
    "rungs": ["Find", "Test", "Reach", "Keep", "Decide"],
    "rungDesc": ["new or copy, and how small to start", "find out if people really want it, before you build", "get it to the first 100 people",
                 "what stops others copying it", "score your ideas, pick one, set a kill rule"],
    "blurb": "One real question on one of your own ideas per sitting: the one you’ve starred on the idea board. Market, offer and price are in your Business course (B01, B03, B06); this course is about testing an idea, reaching people and keeping it yours. Each lesson names the chapter of Zero to One or The Mom Test to read if you want more.",
    "allDone": "now pick one idea and test it. 🚀"}, L)
check_videos(C)
check_extras(C["lessons"])
FLAGS = term_order(C["lessons"], GLOSSARY, "P")
if FLAGS:
    sys.exit("A lesson uses a term before the lesson that teaches it, with no pointer:\n  " + "\n  ".join(FLAGS))

# The products object sits between its comment (with THIEL_Q after it) and the line that tags its lessons, so only the
# object itself is replaced here, not the comment block around it.
html = open(HTML, encoding="utf-8").read()
js = json.dumps(C, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/").replace('{"id":', '\n    {"id":')
m = re.search(r"  var PROD_CURRICULUM=\{[\s\S]*?\};\n(?=  PROD_CURRICULUM\.lessons\.forEach)", html)
assert m, "PROD_CURRICULUM object not found"
html = html[:m.start()] + "  var PROD_CURRICULUM=" + js + ";\n" + html[m.end():]
old_c = re.search(r"  /\* Building products — [\s\S]*?\*/\n", html)
assert old_c, "products comment not found"
html = html[:old_c.start()] + ("  /* Building products — 9 sittings, \"an idea a week\": every lesson runs on the idea you've starred on the idea board\n"
    "     ({idea} in a task, a walk-through heading or a worked answer). Sources: Zero to One (Thiel) and The Mom Test (Fitzpatrick),\n"
    "     in my words with the chapter to read, and videos from the youtube-digest library. Market, offer and price live in the\n"
    "     Business course (B01, B03, B06). Built by scripts/build-products-course.py. Only done-flags, revisits and the idea\n"
    "     board are ever saved into app-state. */\n") + html[old_c.end():]
open(HTML, "w", encoding="utf-8").write(html)
print("PROD_CURRICULUM: %d lessons written into time-tracker.html" % len(C["lessons"]))
