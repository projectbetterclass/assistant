# Builds "Offers & sales with Hormozi" (BIZ_CURRICULUM) in time-tracker.html: 15 sittings on the Business goal,
# written in my words from Alex Hormozi's videos in the youtube-digest library ($100M Offers, $100M Leads and
# the sales trainings). Each sitting runs on your own AI service (the one your Making money with AI plan pilots with
# small firms), and its revisit on Intensity Applied, so you see the same idea on a service and on an app.
#   python3 scripts/build-business-course.py       -> rewrites the block in time-tracker.html
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from course_block import yt, course, check_videos, write

A = "Alex Hormozi"
CROWD = yt("VBoRLJimVzc", A, "If I Wanted to Become a Millionaire In 2024, This is What I'd Do [FULL BLUEPRINT]", "the starving crowd: why the market beats the product")
BROKE = yt("nIk3DedjxJM", A, "\"I'm Broke, What Business Do I Start?\"", "picking what to sell, and to whom, when you start from nothing")
EQ = yt("5MHQr-Z17Hc", A, "This ONE Equation Will Make You RICH", "the value equation, and the four kinds of guarantee")
OFFERS = yt("neTSqOAMgao", A, "Explaining How Anyone Can Make $100M® Offers", "from the customer's problems to an offer, step by step")
K700 = yt("_qspvJAq34M", A, "How I got 700 people to pay me $40,000 each...no bs..", "an offer built on the value equation, worked through")
KEYNOTE = yt("XwZH-lOKG9c", A, "KEYNOTE: Small To BIG. The Big 4 Customer Acquisition Models.", "scarcity, urgency, bonuses, guarantees and the MAGIC name")
PRICES = yt("Gy-RmpRif-I", A, "How To Raise Your Prices [plus the letter I actually sent to customers]", "raising prices, and the letter to existing customers")
PROFIT = yt("41EvCgwPrDc", A, "Make More Profit than 99% of People", "why the cheapest offer is the hardest business")
FUNDING = yt("DpbXWP8fLbc", A, "How to get unlimited funding to build your business in 30 days...", "client-financed acquisition: customers paying for your growth")
MKT101 = yt("Cr0KdqZ954c", A, "Introduction To Marketing | Business Marketing 101", "gross margin, cost to acquire and 30-day cash")
LEADS = yt("Mst4hreQYl0", A, "Watch This To Generate 1000s of Leads (In Any Niche)", "lead magnets: samples, trials, one step of many")
EASY = yt("Ds_Qp2U5I8U", A, "Business is now on ‘Easy Mode” in 2026 (here’s why)", "the lead magnet that reveals a problem")
SCRATCH = yt("HsQeQM1jUeg", A, "If I Had To Start a Business From Scratch, I'd Do This", "warm outreach and the rule of 100")
MATHS = yt("A_tx40lNpf8", A, "The Mathematics of Business, Explained", "the rule of 100, for 100 days")
MKT13 = yt("reisEL_D7xc", A, "13 Years of Marketing Advice in 85 Mins", "content, ads, and more-better-new")
MKT14 = yt("JDR-R--4HhM", A, "14 Years of Marketing Advice in 35 Minutes", "hooks, proof and giving away the secrets")
FREE = yt("7NMH1oAkgLY", A, "Giving Away Free Stuff Will Make You Rich", "give away the secrets, sell the implementation")
SELL4 = yt("JE2_7elAcxM", A, "How to Sell Better than 99% Of People (4 HOUR ULTIMATE GUIDE)", "the CLOSER framework, and what objections blame")
NOTHING = yt("unshZobTt6Q", A, "How to Start a Business From Nothing (Thank Me Later)", "sell the vacation, not the plane flight")
SALES26 = yt("StVqS0jD7Ls", A, "The Ultimate Sales Training for 2026 [Full Course]", "handling objections without arguing")
LTV = yt("uYds0zcAFWM", A, "I Just Learned This After 14 Years of Business", "lifetime value against cost to acquire, and the 3:1 rule")
NUMBER = yt("jzKpAtzKQ54", A, "Business Owners: You NEED to Know This Number", "the one number that tells you if you can grow")
STAY = yt("-j8_YCWZ05Q", A, "How to Get Your Customers to Stay FOREVER", "churn as a leaky bucket, and the first month")
PERFECT = yt("3fsJFUvA6Ts", A, "What Makes The Perfect Business (5 Things)", "recurring revenue and what makes customers stay")
SCALE = yt("N5MExtki_VI", A, "If I Wanted To Scale A Service Business In 2026, Here's What I'd Do", "growing a service business one constraint at a time")

L = [
 dict(id="B01", rung="Market", stage_name="A starving crowd", concept="Pick the market before the product",
  teach="Hormozi’s order of importance is market first, then the offer, then how well you sell. A great offer to the wrong people fails; an average offer to a starving crowd sells out. A good market has four things: real pain (they lose money, time or sleep over the problem), money to pay, people you can find and reach (a list, a trade group, an industry), and growth. Small firms drowning in weekly admin can score well: the pain shows up as unpaid hours every week, the owner signs the cheques, they cluster by trade, and AI makes the problem newly solvable. A market missing one of the four makes everything after it harder.",
  task="Score the two niches from your Making money with AI plan on the four: pain, money to pay, easy to reach, growing (1–10 each). Judge: which niche wins, and which of the four is its weakest — and can you fix that, or should you switch?",
  co="your AI service", rev="Intensity Applied", watch=[CROWD, BROKE]),
 dict(id="B02", rung="Market", stage_name="Niche until it hurts", concept="One who, one problem, one result",
  teach="The narrower the who, the easier everything gets: the words you use, where you find them, the proof you show, and the price you can charge. ‘AI for small businesses’ competes with everyone; ‘I take the weekly invoicing off independent installers’ hands has no direct rival and sounds like it was made for them. Specialists are paid more than generalists for the same skill, because the buyer believes you have solved exactly their problem before. Niching down feels like turning money away; in practice it is how you find the first ten clients, and you can widen later from strength.",
  task="Write your one-sentence niche for the AI service: who exactly, which recurring task, and the result in their words. Then write it once more, narrower. Judge: which version would make an owner say ‘that’s me’, and what do you lose by choosing it?",
  co="your AI service", rev="Intensity Applied", watch=[BROKE]),
 dict(id="B03", rung="Offer", stage_name="The value equation", concept="Dream outcome × likelihood ÷ (time × effort)",
  teach="Hormozi’s value equation: value = (dream outcome × perceived likelihood of getting it) ÷ (time delay × effort and sacrifice). Most people only push the top left, a bigger promise. The cheaper levers are the others. Raise the likelihood with proof, a guarantee, and results from people like them. Cut the time to the first result: something visible in week one, not month three. Cut the effort: do it for them, make it one call a month, nothing new to learn. A smaller promise that feels certain, fast and effortless is worth more than a big one that feels like work.",
  task="Rate your AI service from the owner’s side, 1–10, on each of the four: the dream outcome, how likely it feels, how soon they see something, and how much effort it asks of them. Write one change for each that would raise the value. Judge: which single change would raise it most, and why?",
  co="your AI service", rev="Intensity Applied", after=["B01", "B02"], watch=[EQ, K700]),
 dict(id="B04", rung="Offer", stage_name="Problems into solutions", concept="List every problem, then solve each one",
  teach="A Grand Slam Offer starts from the buyer’s problems, not your features. Write down everything that stands between the owner and the result, before, during and after: ‘I don’t trust AI with client data’, ‘I don’t have time to explain my process’, ‘it won’t fit my software’, ‘what if it makes mistakes?’. Each problem hides in one of the four parts of the value equation. Then turn every problem into a solution and give it a name: a data agreement, a 30-minute onboarding call, setup in their own tools, a weekly check of everything sent. The list of solutions becomes the offer.",
  task="List ten problems a small firm would have with handing over its weekly admin to you, before, during and after. Turn each into a named solution. Judge: which three problems would stop a sale if you left them out?",
  co="your AI service", rev="Intensity Applied", after=["B02"], watch=[OFFERS]),
 dict(id="B05", rung="Offer", stage_name="Make it irresistible", concept="Scarcity, urgency, bonuses, guarantees and a name",
  teach="Five things make an offer easier to say yes to. Scarcity: real limits, such as three pilot places. Urgency: a real deadline. Bonuses: extras that solve the next problem, worth more than they cost you. A guarantee: you take on the buyer’s risk, because you know the work better than they do. Hormozi names four kinds: unconditional (money back, no questions), conditional (money back if they did their part), anti-guarantee (all sales final, said openly) and implied (you’re paid on results). And a name built with his MAGIC formula: a reason why now, who it’s for, the goal, the time frame, and what they get.",
  task="Write your pilot offer in full: a MAGIC name, the scarcity, the deadline, one bonus and one guarantee. Judge: which guarantee can you honour without going broke if three firms use it — and does it make the yes easier?",
  co="your AI service", rev="Intensity Applied", after=["B01"], watch=[KEYNOTE, EQ]),
 dict(id="B06", rung="Price", stage_name="Price on value", concept="Charge from the value, not from your hours",
  teach="A low price is the hardest business there is: thin margins leave no money to deliver well, to find customers or to fix mistakes, and cheap buyers ask the most. Price from the value you create. Your Making money with AI plan prices the monthly service near half its value: if it saves a firm 10 hours a month at €60 an hour, that is €600 of value, so €300 a month, which is exactly the gate in your plan. A higher price also raises how seriously clients take the work, and lets you over-deliver. When demand outruns your time, raise prices for new clients first.",
  task="For one firm from your interviews: the hours your service saves a month, what an hour of theirs is worth, the value per month, and your price at half of it. Judge: if they push back on price, is that a price problem or a value problem — and how would you tell?",
  co="your AI service", rev="Intensity Applied", after=["B04", "B05"], watch=[PROFIT, PRICES]),
 dict(id="B07", rung="Price", stage_name="Let clients fund growth", concept="Gross margin, cost to acquire, and 30-day cash",
  teach="Three numbers decide whether a business can grow. Gross margin: what is left of a sale after the cost of delivering it. Cost to acquire a customer (CAC): everything you spend, time included, to win one. And 30-day cash: how much gross profit a new client brings in during the first month. When a client’s first 30 days cover what it cost to get them, Hormozi calls it client-financed acquisition: every new client pays for the next, and you can grow without savings or investors. A setup fee, paying up front for three months, or a paid kick-off are the usual ways to get there.",
  task="For your €300-a-month service: estimate your hours per client, the cost of the tools, your gross margin, and what it costs you, in hours and euros, to win one client. Is the first month enough to cover it? Judge: what would you change first, a setup fee, up-front payment, or a cheaper way to win clients?",
  co="your AI service", rev="Intensity Applied", after=["B05"], watch=[FUNDING, MKT101]),
 dict(id="B08", rung="Leads", stage_name="Lead magnets", concept="Something free that solves a small problem and reveals the next",
  teach="A lead magnet is a free thing that makes people put their hand up. Hormozi’s three kinds: one that reveals a problem (an audit showing where the hours go), a sample or trial (a week of the work done for them), and one step of a many-step process (the first workflow set up, the rest for paying clients). A good one solves a narrow problem completely and makes the next problem obvious, so the paid offer is the natural next step. Your plan’s free 60-day pilot is a trial lead magnet; a 30-minute admin audit is a smaller one you can offer to many more owners.",
  task="Design a lead magnet for your niche: which of the three kinds, what exactly they get, how long it takes you, and the next problem it makes them see. Judge: is your 60-day pilot too big to be a first step — what smaller one would come before it?",
  co="your AI service", rev="Intensity Applied", after=["B06"], watch=[LEADS, EASY]),
 dict(id="B09", rung="Leads", stage_name="Warm outreach", concept="The people who already know you, and the rule of 100",
  teach="Hormozi’s core four ways to get leads are warm outreach, posting content, cold outreach and paid ads. Start with warm outreach: people who already know you, and the people they know, contacted one at a time. Tell them what you’re doing and ask who they know who struggles with it; a referral beats a pitch. Then volume: his rule of 100 is 100 actions a day for 100 days on one channel, and most people get a first customer within a few weeks. Your plan does a Dutch version: two real conversations with owners a day, no cold email, because in the Netherlands unsolicited email to businesses needs their consent.",
  task="List 30 people from your plan’s list (family, work, school, second-degree LinkedIn) and write the two-sentence message you’ll send each: what you do, and who they know with the problem. Judge: what number of actions a day will you really keep up for 100 days?",
  co="your AI service", rev="Intensity Applied", after=["B07"], watch=[SCRATCH, MATHS]),
 dict(id="B10", rung="Leads", stage_name="Content and proof", concept="Give away the secrets, sell the implementation",
  teach="Posting content is the one-to-many version of warm outreach: you help people who already follow you, and the ones with the problem come to you. Hormozi’s rule is to give away the secrets and sell the implementation: show exactly how you cut a firm’s invoicing from five hours to one, because most owners still won’t want to do it themselves. Every post needs a hook that stops the scroll, something useful, and proof: real numbers from real clients, with their permission. Your plan’s one note a week on client results is this, done small and steadily. Paid ads only make sense once an offer already sells.",
  task="Write next week’s note: the hook (one line), what you did for a client or in a pilot, the result in hours or euros, and what a reader could copy themselves. Judge: does it give away enough that someone could do it alone — and why is that fine?",
  co="your AI service", rev="Intensity Applied", after=["B07"], watch=[FREE, MKT14]),
 dict(id="B11", rung="Sell", stage_name="The CLOSER call", concept="Clarify, label, overview, sell the vacation, explain, reinforce",
  teach="Hormozi’s sales call has six steps, CLOSER. Clarify why they’re here: ‘what made you take this call?’. Label the problem: ‘so what I’m hearing is…, does that sound right?’. Overview their past: what they tried and why it didn’t work. Sell the vacation, not the plane flight: the life after the result (evenings back, invoices out on time), not the steps in between. Explain away their concerns. Reinforce the decision once they say yes, so it sticks. The owner talks most of the call; your job is to ask until they have said, in their own words, why they need it.",
  task="Write the questions for a CLOSER call with an owner from your interviews: one or two for each letter, in your own words. Then write the vacation for that owner in three sentences. Judge: which step will you be tempted to skip, and what happens to the sale if you do?",
  co="your AI service", rev="Intensity Applied", after=["B08", "B09"], watch=[SELL4, NOTHING]),
 dict(id="B12", rung="Sell", stage_name="Objections", concept="Every objection blames circumstances, other people, or the buyer’s own doubt",
  teach="Objections sound different but come from three places. Circumstances: ‘no time’, ‘no money’, ‘not now’. Other people: ‘I need to ask my partner’, ‘my accountant handles that’. And the buyer’s own doubt: ‘I’m not sure it will work for us’. Don’t argue with the reason; ask about it. ‘If money weren’t an issue, would you do it?’ separates a price problem from a doubt. ‘What would your partner want to know?’ brings the other person into the room. Most ‘I need to think about it’ means a concern you haven’t heard yet, so ask what it is.",
  task="Write your answers, as questions, to the three you’ll hear most: ‘I need to think about it’, ‘it’s too expensive’, and ‘I need to ask my partner’. Say which of the three sources each comes from. Judge: which objection tells you your offer, not your selling, needs work?",
  co="your AI service", rev="Intensity Applied", after=["B10"], watch=[SALES26, SELL4]),
 dict(id="B13", rung="Keep", stage_name="What a client is worth", concept="Lifetime value against the cost to win one",
  teach="Lifetime value (LTV) is the gross profit a client brings in for as long as they stay: monthly gross profit × the months they stay. Set it against the cost to acquire them (CAC). In software the rule of thumb is that LTV should be at least three times CAC; Hormozi adds that it depends on how fast the money comes back. At €300 a month, an 80% margin and clients staying 12 months on average, a client is worth about €2,880 of gross profit; if winning one costs €500, the ratio is nearly 6:1 and you can afford to spend more on finding clients. Every extra month a client stays raises the number you can spend to get the next.",
  task="Work out LTV and LTV:CAC for your service with your own guesses: price, gross margin, months clients stay, and the cost to win one. Then redo it if clients stay 6 months instead of 12. Judge: which lever is easier for you to move, the months they stay or the cost to win them?",
  co="your AI service", rev="Intensity Applied", after=["B11", "B12"], watch=[LTV, NUMBER]),
 dict(id="B14", rung="Keep", stage_name="Churn", concept="A leaky bucket, and the first month",
  teach="Churn is the share of clients who leave each month, and it works like a leaky bucket: you grow only while new clients come in faster than old ones leave. Track joins and cancels every month and call it honestly: growing, flat or shrinking. Churn is highest in the first month and drops the longer clients stay, so the biggest win is a planned first 30 days: a quick visible result, a check-in call, and a clear next step. Ask everyone who leaves why, and look for the pattern every 20 or so; ask your longest clients why they stay, and do more of that.",
  task="Plan the first 30 days for a new client: what they see in week one, the check-in, and the moment they know it works. Then write the two questions you’ll ask a client who cancels, and the one you’ll ask your best client. Judge: what is most likely to make a firm cancel in month two?",
  co="your AI service", rev="Intensity Applied", after=["B12"], watch=[STAY, PERFECT]),
 dict(id="B15", rung="Keep", stage_name="More, better, new", concept="Grow the thing that works before trying a new one",
  teach="When something works, the order is more, then better, then new. More: do more of what already brings clients, such as more conversations and more notes, until it stops scaling. Better: improve the weakest step, such as the share of calls that become clients or the hours each client takes, which in your plan means automating one delivery step at a time towards 1.5 hours a client. New: only then a new channel, a new niche or a new product, such as the software for the industry in your plan’s year two. Most small businesses do the opposite: they jump to new before they have squeezed what works.",
  task="Take your plan’s year: where are you on more, better, new right now? Name the one ‘more’ you’ll do next month, the one ‘better’ you’ll fix after, and the one ‘new’ you are not allowed to start yet. Judge: what tempts you to jump to new, and what would it cost?",
  co="your AI service", rev="Intensity Applied", after=["B11"], watch=[MKT13, SCALE]),
]

def check():
    e = lambda a, b, tol=0.5: abs(a - b) <= tol or sys.exit(f"bad number: {a} vs {b}")
    e(10 * 60, 600); e(600 / 2, 300); e(300 * 0.8 * 12, 2880); e(2880 / 500, 5.76, 0.01)
check()

C = course({"goal_id": "goal_biz", "key": "biz", "title": "Offers & sales with Hormozi", "azTitle": "Offers & sales with Hormozi, A → Z",
     "rungs": ["Market", "Offer", "Price", "Leads", "Sell", "Keep"],
     "rungDesc": ["pick a starving crowd, and narrow it until it hurts", "the value equation, problems into solutions, and the extras that make it a yes",
                  "price on value, and let clients pay for your growth", "lead magnets, warm outreach, and content with proof",
                  "the CLOSER call, and what objections are really about", "what a client is worth, churn, and more-better-new"],
     "blurb": "One question on your own offer per sitting: the AI service your Making money with AI plan pilots with small firms, and the revisit on Intensity Applied. Written in my words from Alex Hormozi’s videos in your library.",
     "allDone": "now make the offer to three firms. 💼",
     "revWord": "another offer",
     "refNote": "The idea opens in step 2 of the sitting — guess first. The videos are Hormozi’s, for when you want more; his revenue figures are his own claims."}, L)
check_videos(C)
write("BIZ_CURRICULUM", ["Offers & sales with Hormozi — 15 sittings on the Business goal, in my words from Alex Hormozi's videos in the",
      "youtube-digest library: market, offer (value equation, problems into solutions, guarantees, MAGIC), price, leads (lead magnets,",
      "warm outreach, the rule of 100, content), the CLOSER call, objections, LTV:CAC and churn. Runs on your AI service; revisits on",
      "Intensity Applied. Built by scripts/build-business-course.py."], C)
