# Builds "Offers & sales with Hormozi" (BIZ_CURRICULUM) in time-tracker.html: 15 sittings on the Business goal,
# written in my words from Alex Hormozi's videos in the youtube-digest library ($100M Offers, $100M Leads and
# the sales trainings). Each sitting runs on your own AI service (the one your Making money with AI plan pilots with
# small firms), and its revisit on Intensity Applied, so you see the same idea on a service and on an app.
#   python3 scripts/build-business-course.py       -> rewrites the block in time-tracker.html
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from course_block import yt, course, check_videos, write, check_extras, term_order

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
MARKET = yt("LqC-oXjatmA", A, "The Key To Finding a Profitable Market", "the four tests, with the resume-coach and seniors-dating examples")
SCALE = yt("N5MExtki_VI", A, "If I Wanted To Scale A Service Business In 2026, Here's What I'd Do", "growing a service business one constraint at a time")

L = [
 dict(id="B01", rung="Market", stage_name="A starving crowd", concept="Pick the market before the product",
  task="Score the two niches from your Making money with AI plan on the four: pain, money to pay, easy to reach, growing (1–10 each). Judge: which niche wins, and which of the four is its weakest — and can you fix that, or should you switch?",
  co="your AI service", rev="Intensity Applied", watch=[CROWD, MARKET, BROKE], read=["$100M Offers, the “starving crowd” chapter"]),
 dict(id="B02", rung="Market", stage_name="Niche until it hurts", concept="One who, one problem, one result",
  task="Write your one-sentence niche for the AI service: who exactly, which recurring task, and the result in their words. Then write it once more, narrower. Judge: which version would make an owner say ‘that’s me’, and what do you lose by choosing it?",
  co="your AI service", rev="Intensity Applied", watch=[BROKE]),
 dict(id="B03", rung="Offer", stage_name="The value equation", concept="Dream outcome × likelihood ÷ (time × effort)",
  task="Rate your AI service from the owner’s side, 1–10, on each of the four: the dream outcome, how likely it feels, how soon they see something, and how much effort it asks of them. Write one change for each that would raise the value. Judge: which single change would raise it most, and why?",
  co="your AI service", rev="Intensity Applied", after=["B01", "B02"], watch=[EQ, K700], read=["$100M Offers, the “value equation” chapter"]),
 dict(id="B04", rung="Offer", stage_name="Problems into solutions", concept="List every problem, then solve each one",
  task="List ten problems a small firm would have with handing over its weekly admin to you, before, during and after. Turn each into a named solution. Judge: which three problems would stop a sale if you left them out?",
  co="your AI service", rev="Intensity Applied", after=["B02"], watch=[OFFERS]),
 dict(id="B05", rung="Offer", stage_name="Make it irresistible", concept="Scarcity, urgency, bonuses, guarantees and a name",
  task="Write your pilot offer in full: a MAGIC name, the scarcity, the deadline, one bonus and one guarantee. Judge: which guarantee can you honour without going broke if three firms use it — and does it make the yes easier?",
  co="your AI service", rev="Intensity Applied", after=["B01"], watch=[KEYNOTE, EQ]),
 dict(id="B06", rung="Price", stage_name="Price on value", concept="Charge from the value, not from your hours",
  task="For one firm from your interviews: the hours your service saves a month, what an hour of theirs is worth, the value per month, and your price at half of it. Judge: if they push back on price, is that a price problem or a value problem — and how would you tell?",
  co="your AI service", rev="Intensity Applied", after=["B04", "B05"], watch=[PROFIT, PRICES], read=["$100M Offers, the “commodity problem” and pricing chapters"]),
 dict(id="B07", rung="Price", stage_name="Let clients fund growth", concept="Gross margin, cost to acquire, and 30-day cash",
  task="For your €300-a-month service: estimate your hours per client, the cost of the tools, your gross margin, and what it costs you, in hours and euros, to win one client. Is the first month enough to cover it? Judge: what would you change first, a setup fee, up-front payment, or a cheaper way to win clients?",
  co="your AI service", rev="Intensity Applied", after=["B05"], watch=[FUNDING, MKT101]),
 dict(id="B08", rung="Leads", stage_name="Lead magnets", concept="Something free that solves a small problem and reveals the next",
  task="Design a lead magnet for your niche: which of the three kinds, what exactly they get, how long it takes you, and the next problem it makes them see. Judge: is your 60-day pilot too big to be a first step — what smaller one would come before it?",
  co="your AI service", rev="Intensity Applied", after=["B06"], watch=[LEADS, EASY]),
 dict(id="B09", rung="Leads", stage_name="Warm outreach", concept="The people who already know you, and the rule of 100",
  task="List 30 people from your plan’s list (family, work, school, second-degree LinkedIn) and write the two-sentence message you’ll send each: what you do, and who they know with the problem. Judge: what number of actions a day will you really keep up for 100 days?",
  co="your AI service", rev="Intensity Applied", after=["B07"], watch=[SCRATCH, MATHS]),
 dict(id="B10", rung="Leads", stage_name="Content and proof", concept="Give away the secrets, sell the implementation",
  task="Write next week’s note: the hook (one line), what you did for a client or in a pilot, the result in hours or euros, and what a reader could copy themselves. Judge: does it give away enough that someone could do it alone — and why is that fine?",
  co="your AI service", rev="Intensity Applied", after=["B07"], watch=[FREE, MKT14]),
 dict(id="B11", rung="Sell", stage_name="The CLOSER call", concept="Clarify, label, overview, sell the vacation, explain, reinforce",
  task="Write the questions for a CLOSER call with an owner from your interviews: one or two for each letter, in your own words. Then write the vacation for that owner in three sentences. Judge: which step will you be tempted to skip, and what happens to the sale if you do?",
  co="your AI service", rev="Intensity Applied", after=["B08", "B09"], watch=[SELL4, NOTHING]),
 dict(id="B12", rung="Sell", stage_name="Objections", concept="Every objection blames circumstances, other people, or the buyer’s own doubt",
  task="Write your answers, as questions, to the three you’ll hear most: ‘I need to think about it’, ‘it’s too expensive’, and ‘I need to ask my partner’. Say which of the three sources each comes from. Judge: which objection tells you your offer, not your selling, needs work?",
  co="your AI service", rev="Intensity Applied", after=["B10"], watch=[SALES26, SELL4]),
 dict(id="B13", rung="Keep", stage_name="What a client is worth", concept="Lifetime value against the cost to win one",
  task="Work out LTV and LTV:CAC for your service with your own guesses: price, gross margin, months clients stay, and the cost to win one. Then redo it if clients stay 6 months instead of 12. Judge: which lever is easier for you to move, the months they stay or the cost to win them?",
  co="your AI service", rev="Intensity Applied", after=["B11", "B12"], watch=[LTV, NUMBER]),
 dict(id="B14", rung="Keep", stage_name="Churn", concept="A leaky bucket, and the first month",
  task="Plan the first 30 days for a new client: what they see in week one, the check-in, and the moment they know it works. Then write the two questions you’ll ask a client who cancels, and the one you’ll ask your best client. Judge: what is most likely to make a firm cancel in month two?",
  co="your AI service", rev="Intensity Applied", after=["B12"], watch=[STAY, PERFECT]),
 dict(id="B15", rung="Keep", stage_name="More, better, new", concept="Grow the thing that works before trying a new one",
  task="Take your plan’s year: where are you on more, better, new right now? Name the one ‘more’ you’ll do next month, the one ‘better’ you’ll fix after, and the one ‘new’ you are not allowed to start yet. Judge: what tempts you to jump to new, and what would it cost?",
  co="your AI service", rev="Intensity Applied", after=["B11"], watch=[MKT13, SCALE]),
]

# ---- each lesson's idea, walk-through, numbers box, worked answer, thread and revisit -------------------------------
# The numbers are your Making money with AI plan's (€300 a month at half the value of 10 hours at €60, a free 60-day
# pilot for three firms, two conversations a day, towards 1.5 hours a client). Anything the plan doesn't fix is marked
# "assumed" where it is used, so you can put in your own. The figures in Hormozi's videos are Hormozi's own claims.
def eur(x, d=0): return ("−" if x < 0 else "") + "€" + format(abs(x), ",.%df" % d)
def pc(x, d=0): return ("%." + str(d) + "f%%") % x
PRICE, HOURS_SAVED, OWNER_RATE = 300, 10, 60
VALUE = HOURS_SAVED * OWNER_RATE
TOOLS, MY_RATE, HOURS_NOW, HOURS_GOAL = 30, 40, 4, 1.5          # assumed: tools a client a month, what an hour of yours is worth, hours a client
CONV_PER_PILOT, PILOTS_PER_CLIENT, CONV_HOURS, PILOT_MONTHS = 10, 3, 0.5, 2
GP_NOW = PRICE - TOOLS - HOURS_NOW * MY_RATE
GP_GOAL = PRICE - TOOLS - HOURS_GOAL * MY_RATE
CAC_HOURS = CONV_PER_PILOT * PILOTS_PER_CLIENT * CONV_HOURS + PILOTS_PER_CLIENT * PILOT_MONTHS * HOURS_NOW
CAC = CAC_HOURS * MY_RATE
MARGIN_B13, CAC_B13 = 0.80, 500
LTV12, LTV6 = PRICE * MARGIN_B13 * 12, PRICE * MARGIN_B13 * 6
ASSUMED = {"k": "Assumed (put in your own)", "v": "%s tools · %s an hour of yours" % (eur(TOOLS), eur(MY_RATE)), "n": "Tools a client a month, and what an hour of your time is worth; %d hours a client a month at first, %.1f once automated." % (HOURS_NOW, HOURS_GOAL)}
PLAN = {"k": "Your plan’s price", "v": "€300 a month", "n": "Half the value of 10 hours a month at €60 an hour."}

EXTRA = {}
EXTRA["B01"] = dict(
  teach="Market first, then the offer, then how well you sell: an average offer to a starving crowd sells, a great offer to the wrong people doesn’t. A starving crowd has real pain, money to pay, people you can find in one place, and a market that is still growing.",
  walk=[{"h": "Why the market comes first", "p": ["You can fix an offer in a week and your selling in a month. You can’t fix a market that has no money or no pain; you can only leave it."], "p2": ["If you know a market from your own life, start there: you already know its pain, and where its people gather."]},
        {"h": "The four tests", "l": [["Pain.", "They lose money, time or sleep over it, every week. A nice-to-have fails."], ["Money.", "The person with the pain can pay, and signs the cheques."], ["Easy to find.", "A list, a trade group, an industry: somewhere they gather."], ["Growing.", "More of them, or more need, each year."]]},
        {"h": "Where it goes wrong", "l": ["Picking the market you like, not the one that passes.", "Scoring every test 7 to be polite; be harsh with the weakest."]},
        {"h": "Worked: Hormozi’s two failures", "p": ["Unemployed people have the pain but not the money. Newspaper buyers can pay, but the market is shrinking. Each fails one test, and everything after it gets harder. Small firms drowning in weekly admin can pass all four: the hours are lost every week, the owner pays, they cluster by trade, and AI makes the problem newly solvable."]},
        {"h": "Your turn: your AI service", "p": ["Score your plan’s two niches on the four, 1–10 each, and name the weakest test of the winner."]}],
  key=[{"t": "A good answer looks like", "l": ["Two rows of four scores, e.g. independent installers: pain 8, money 7, easy to find 6, growing 6 = 27; a second niche scored the same way.",
        "The winner’s weakest test named, with a fix: ‘easy to find 6: the regional installers’ association and its newsletter’.",
        "Switch if the weakest test can’t be fixed by you: no money or no pain."]}],
  thread={"n": "B02 · narrow the winner until it hurts"},
  rtask="Intensity Applied: score its market, people who lift to build muscle, on the four tests. Which is weakest?",
  rkey=[{"t": "Short answer", "l": ["Pain is the weak one: stalled progress is frustrating, but not lost money. Money and growth are fine; finding them is easy but crowded (gyms, fitness creators).", "So the offer has to make the pain sharper: ‘stalled for six months’, not ‘wants to get bigger’."]}])

EXTRA["B02"] = dict(
  teach="The narrower the who, the easier everything gets: the words you use, where you find them, the proof you show and the price you can charge. One who, one recurring problem, one result in their words; you can widen later from strength.",
  walk=[{"h": "Why narrow wins", "p": ["‘AI for small businesses’ competes with everyone. ‘I take the weekly invoicing off independent installers’ has almost no direct rival and sounds made for them. Specialists are paid more than generalists for the same skill, because the buyer believes you have solved exactly their problem before."]},
        {"h": "How to write it", "l": [["Who, exactly.", "A trade, a size, a place."], ["Which recurring task.", "Weekly, not once a year."], ["The result in their words.", "‘Invoices out every Friday without my evenings’, not ‘workflow automation’."]]},
        {"h": "Where it goes wrong", "l": ["Keeping it broad because narrowing feels like turning money away.", "A result in your words (‘efficiency’), not theirs."]},
        {"h": "Worked: three versions", "l": ["Broad: ‘AI admin help for small businesses.’", "Narrower: ‘I take the weekly invoicing off installers.’", "Narrowest: ‘For independent heat-pump installers: your invoices go out every Friday, and you get your evenings back.’ The last one makes an installer say ‘that’s me’."]},
        {"h": "Your turn: your AI service", "p": ["Write your one-sentence niche, then a narrower one, and say what you give up with the narrower one."]}],
  key=[{"t": "A good answer looks like", "l": ["One who, one weekly task, one result in their words, in under 25 words.", "The narrower version names a trade and a task you could find ten of this month.", "What you lose: the other trades, for now. What you gain: words, proof and referrals that all point the same way."]}],
  thread={"b": "B01 · the niche that passed the four tests", "n": "B03 · the value equation, from this owner’s side"},
  rtask="Intensity Applied: write its niche in one sentence, then narrower.",
  rkey=[{"t": "Short answer", "l": ["Broad: ‘a training app for building muscle.’ Narrower: ‘for lifters who train 3–4 times a week and have stalled: one protocol, and the app tells you which muscles have recovered.’"]}])

EXTRA["B03"] = dict(
  teach="Value = (dream outcome × how likely they believe they’ll get it) ÷ (how long it takes × how much effort it costs them). A bigger promise is the obvious lever; certainty, speed and less effort are the cheaper ones, and usually worth more.",
  walk=[{"h": "The four parts", "l": [["Dream outcome.", "The life after the result, in their words."], ["Likelihood.", "How sure they are it will work for them: proof, results from people like them, a guarantee (B05)."], ["Time delay.", "How soon they see something."], ["Effort.", "What it asks of them: meetings, learning, changing habits."]]},
        {"h": "Where it goes wrong", "l": ["Only raising the promise.", "Rating it from your side, not the owner’s."]},
        {"h": "Worked: Hormozi’s liposuction", "p": ["Liposuction and a $5 weight-loss ebook promise the same outcome. The price gap is the other three parts: a doctor who has done 10,000 surgeries is far more likely to deliver, in an afternoon, with almost no effort from you."]},
        {"h": "Your turn: your AI service", "p": ["Rate it 1–10 on each part from the owner’s side, and write one change for each."]}],
  key=[{"t": "A good answer looks like", "l": ["Ratings from the owner’s side, e.g. outcome 7 (evenings back), likelihood 4 (no proof yet), time 5 (results in month two), effort 6 (they must explain their process).",
        "One change each: a case from the first pilot (likelihood), invoices out in week one (time), a 30-minute onboarding call and you do the rest (effort).",
        "The biggest single change is usually likelihood: before your first three pilots, proof is what you lack."]}],
  thread={"b": "B01–B02 · a starving crowd, narrowed to one who and one task", "n": "B04 · every problem becomes a named solution; B06 · price from the value"},
  rtask="Intensity Applied: rate it on the four parts from a stalled lifter’s side. Which part is weakest?",
  rkey=[{"t": "Short answer", "l": ["Likelihood and time: lifters doubt yet another plan, and muscle shows in months. Make progress visible early (strength logged each session) and show results from people like them."]}])

EXTRA["B04"] = dict(
  teach="A Grand Slam Offer starts from the buyer’s problems, not your features. List everything between the owner and the result, before, during and after; turn each into a named solution; the list of solutions becomes the offer.",
  walk=[{"h": "How to do it", "l": [["List the problems.", "Before (trust, data, time to explain), during (mistakes, fit with their tools), after (what if you stop?)."], ["Sort them by the value equation (B03).", "Each problem lowers likelihood, adds time or adds effort."], ["Name a solution for each.", "A named thing feels real: ‘the Friday check’, not ‘we review things’."]]},
        {"h": "Where it goes wrong", "l": ["Listing features instead of their problems.", "Leaving out the awkward problems (data, mistakes), which are the ones that stop the sale."]},
        {"h": "Worked: four problems, four solutions", "l": ["‘I don’t trust AI with client data’ → a data agreement.", "‘I don’t have time to explain my process’ → a 30-minute onboarding call, and you write it down.", "‘It won’t fit my software’ → setup in their own tools.", "‘What if it makes mistakes?’ → a weekly check of everything sent."]},
        {"h": "Your turn: your AI service", "p": ["Ten problems a small firm would have with handing you its weekly admin, each with a named solution."]}],
  key=[{"t": "A good answer looks like", "l": ["Ten problems in the owner’s words, spread over before, during and after.", "Ten named solutions, each one line.", "The three that stop a sale: data and trust, mistakes going to clients, and the time it takes them to hand it over."]}],
  thread={"b": "B03 · the four parts of value", "n": "B05 · the extras that make it a yes; B11 · these problems come back as questions on the call"},
  rtask="Intensity Applied: five problems a lifter has with trusting a new app, each with a named solution.",
  rkey=[{"t": "Short answer", "l": ["‘Will it work for me?’ → results from people like them. ‘I’ll lose my data’ → local-first storage, said plainly. ‘I don’t have this equipment’ → the equipment filter. ‘I’ll overtrain’ → the recovery lock. ‘Too much to learn’ → one protocol."]}])

EXTRA["B05"] = dict(
  teach="Five things make an offer easier to say yes to: real scarcity, a real deadline, bonuses that solve the next problem, a guarantee that takes on the buyer’s risk, and a name built with Hormozi’s MAGIC formula. Every one of them has to be true.",
  walk=[{"h": "The five", "l": [["Scarcity.", "Real limits: three pilot places."], ["Urgency.", "A real deadline."], ["Bonuses.", "Extras that solve the next problem, worth more to them than they cost you."], ["A guarantee.", "Unconditional (money back), conditional (back if they did their part), anti-guarantee (all sales final, said openly) or implied (paid on results)."], ["A MAGIC name.", "A reason why now, who it’s for, the goal, the time frame, and what they get."]]},
        {"h": "Where it goes wrong", "l": ["Fake scarcity or deadlines: they kill trust the first time someone notices.", "A guarantee you can’t afford if three clients use it."]},
        {"h": "Worked: a pilot offer", "p": ["‘Friday Invoices for Installers: 60 days, three places, closes 1 December. Your invoices go out every Friday; if a week is missed, that month is free. Bonus: a one-page list of your late payers each month.’ The guarantee is conditional and cheap to honour: a missed week costs you one month of one client."]},
        {"h": "Your turn: your AI service", "p": ["Write your pilot offer in full, and check the guarantee against three firms using it at once."]}],
  key=[{"t": "A good answer looks like", "l": ["A name with all five MAGIC parts, three places, a real date, one bonus that solves the next problem, one guarantee.",
        "The guarantee check: if all three firms claim it, what does it cost you? A month free each is %s; money back on a free pilot costs nothing but your hours." % eur(3 * PRICE),
        "It makes the yes easier when it removes the owner’s biggest doubt from B03, usually likelihood."]}],
  thread={"b": "B03–B04 · the value equation and the problems list", "n": "B06 · the price; B08 · the pilot as a lead magnet"},
  rtask="Intensity Applied: write a launch offer with all five, and say which guarantee an app can honour.",
  rkey=[{"t": "Short answer", "l": ["E.g. ‘Break the Stall in 8 Weeks: launch price for the first 500, until the end of the month; if your logged lifts haven’t gone up by week 8, a full refund.’", "A conditional guarantee tied to logged sessions works for an app: the app itself shows whether they did their part."]}])

EXTRA["B06"] = dict(
  teach="Price from the value you create, not from your hours: a low price is the hardest business there is, with no money to deliver well, to find customers or to fix mistakes. Your plan prices the service near half its value, and raises prices for new clients first when demand outruns your time.",
  walk=[{"h": "Why cheap is hard", "p": ["Thin margins leave nothing for delivering well, finding the next client or fixing mistakes, and the cheapest buyers ask the most. A higher price also makes clients take the work more seriously."], "p2": ["Sell what everyone sells and you compete on price, and lose. Make an offer people can’t compare (B05), then charge for the value."]},
        {"h": "The margin maths", "p": ["At a 20%% profit margin, a 20%% price rise doubles your profit: on a %s sale that costs %s to deliver you keep %s; at %s you keep %s. Small price changes move profit far more than they move revenue." % (eur(100), eur(80), eur(20), eur(120), eur(40))]},
        {"h": "How to set it", "l": [["Value per month.", "Hours saved × what an hour of theirs is worth."], ["Price.", "A share of that value, your plan says half: they keep the other half."], ["Raising it.", "When demand outruns your time, raise it for new clients first."]]},
        {"h": "Where it goes wrong", "l": ["Pricing from your hours or your costs.", "Discounting before you’ve heard the real objection (B12)."]},
        {"h": "Worked: Hormozi’s gym", "p": ["When Hormozi tripled the price at the gym, a third of the members left and revenue still doubled: 3 × ⅔ = 2. Fewer clients at a higher price also meant more time and money for each one."]},
        {"h": "Your turn: one firm from your interviews", "p": ["Hours saved a month, what an hour of theirs is worth, the value, and your price at half."]}],
  need=[{"k": "Your plan’s example firm", "v": "10 hours · €60 an hour", "n": "Hours saved a month, and what an hour of the owner’s is worth."}],
  key=[{"t": "Worked answer, with your plan’s numbers", "l": ["Value: 10 hours × €60 = %s a month. Price at half: %s a month, the gate in your plan." % (eur(VALUE), eur(VALUE / 2)),
        "If they push back: ask whether they agree with the 10 hours and the €60. If they doubt the hours, it’s a value problem: more proof (B03). If they agree and still say too much, it’s cash or budget: spread the payment, or start smaller."]}],
  thread={"b": "B03–B05 · value, problems and the offer", "n": "B07 · whether that price can pay for your growth"},
  rtask="Intensity Applied: what’s a month of it worth to a stalled lifter, and what price follows?",
  rkey=[{"t": "Short answer", "l": ["Compare it with what they pay for the alternative: a personal trainer costs more per session than most training apps cost per month. Price it well under a month of coaching, and they keep most of the value."]}])

EXTRA["B07"] = dict(
  teach="Three numbers decide whether a business can grow: gross margin, the cost to acquire a customer (CAC), and the gross profit a new client brings in its first 30 days. When the first month covers what the client cost to win, every client pays for the next.",
  walk=[{"h": "The three numbers", "l": [["Gross margin.", "What’s left of a sale after the cost of delivering it, your hours included."], ["CAC.", "Everything it costs to win one client, time included: the conversations, the pilot."], ["30-day cash.", "The gross profit a new client brings in its first month. When it covers CAC, Hormozi calls it client-financed acquisition."]]},
        {"h": "Ways to get there", "l": ["A setup fee.", "Paying three months up front.", "A paid kick-off instead of a free one.", "A cheaper way to win clients: referrals, a smaller first step (B08)."]},
        {"h": "Where it goes wrong", "l": ["Leaving your own hours out of both numbers.", "A long free pilot that makes CAC bigger than a year of profit."]},
        {"h": "Worked: the same service, two stages", "p": ["At %d hours a client a month, gross profit is €300 − %s tools − %d h × %s = %s, a margin of %s. Automated to %.1f hours: %s, %s." % (HOURS_NOW, eur(TOOLS), HOURS_NOW, eur(MY_RATE), eur(GP_NOW), pc(GP_NOW / PRICE * 100), HOURS_GOAL, eur(GP_GOAL), pc(GP_GOAL / PRICE * 100))]},
        {"h": "Your turn: your €300 service", "p": ["Hours per client, tools, gross margin, the cost to win one client in hours and euros, and whether the first month covers it."]}],
  need=[PLAN, ASSUMED, {"k": "Winning a client (assumed)", "v": "%d conversations → 1 pilot; %d pilots → 1 client" % (CONV_PER_PILOT, PILOTS_PER_CLIENT), "n": "Half an hour a conversation; a free pilot of %d months." % PILOT_MONTHS}],
  key=[{"t": "Worked answer, with the assumed numbers", "l": ["Gross profit a month at %d hours: %s (%s margin); at %.1f hours: %s (%s)." % (HOURS_NOW, eur(GP_NOW), pc(GP_NOW / PRICE * 100), HOURS_GOAL, eur(GP_GOAL), pc(GP_GOAL / PRICE * 100)),
        "CAC: %d conversations × ½ hour + %d pilots × %d months × %d hours = %.0f hours = %s." % (CONV_PER_PILOT * PILOTS_PER_CLIENT, PILOTS_PER_CLIENT, PILOT_MONTHS, HOURS_NOW, CAC_HOURS, eur(CAC)),
        "First month: %s, about %s of CAC. Nowhere near covered." % (eur(GP_NOW), pc(GP_NOW / CAC * 100)),
        "Change first: the free pilots are %.0f of the %.0f hours. A shorter or paid pilot, and three months paid up front (%s), are the first fixes; neither alone covers it, which is why the hours per client matter too (B15)." % (PILOTS_PER_CLIENT * PILOT_MONTHS * HOURS_NOW, CAC_HOURS, eur(3 * PRICE))]}],
  thread={"b": "B06 · €300 a month, half of €600 of value", "n": "B08–B10 · cheaper ways to win clients; B13 · CAC against what a client is worth"},
  rtask="Intensity Applied: what does it cost to win one paying user, and does their first month cover it?",
  rkey=[{"t": "Short answer", "l": ["An app’s gross margin is high (no hours per user), so the question is CAC: store ads or creator posts per paying user, against the first month’s price.", "If a month is a few euros and a paying user costs much more to win, an annual plan paid up front is the app’s version of client-financed acquisition."]}])

EXTRA["B08"] = dict(
  teach="A lead magnet is a free thing that makes the right people put their hand up. It solves a narrow problem completely and makes the next problem obvious, so the paid offer is the natural next step.",
  walk=[{"h": "Three kinds", "l": [["Reveal a problem.", "An audit that shows where the hours go."], ["A sample or trial.", "A week of the work done for them."], ["One step of many.", "The first workflow set up; the rest is for paying clients."]]},
        {"h": "What makes one work", "l": ["Narrow and complete: they get a real result.", "It shows the next problem, which your paid offer solves.", "Cheap for you to deliver to many people."]},
        {"h": "Where it goes wrong", "l": ["Too big to be a first step: a 60-day pilot is a big yes to ask from a stranger.", "Too vague to want: ‘a free consultation’."]},
        {"h": "Worked: the 30-minute admin audit", "p": ["Thirty minutes, one sheet back: where the owner’s admin hours go each week, and which one task you’d take first. It reveals the problem in their own numbers and leads straight to the pilot."]},
        {"h": "Your turn: your niche", "p": ["Design one: which kind, what they get, how long it takes you, and the next problem it reveals."]}],
  key=[{"t": "A good answer looks like", "l": ["One kind, one deliverable, a time cost small enough to do for twenty owners, e.g. the 30-minute audit.", "The next problem it reveals, which is what the pilot solves.", "Yes, the 60-day pilot is too big as the first step: the audit comes before it."]}],
  thread={"b": "B05 · the pilot offer; B07 · winning clients costs too much", "n": "B09 · who you offer it to first"},
  rtask="Intensity Applied: design a lead magnet that makes stalled lifters put their hand up.",
  rkey=[{"t": "Short answer", "l": ["E.g. a free ‘stall check’: log three sessions and see which muscles never recover or never get trained to failure. It reveals the problem, and the app solves the next one."]}])

EXTRA["B09"] = dict(
  teach="Start with warm outreach: the people who already know you, and the people they know, one at a time; ask who they know with the problem rather than pitching. Then volume: Hormozi’s rule of 100 is 100 actions a day for 100 days on one channel.",
  walk=[{"h": "The core four", "p": ["Warm outreach, posting content, cold outreach, paid ads. Start with the first: people who know you answer, and a referral beats a pitch."]},
        {"h": "The message", "l": ["What you do, in one line.", "Who they know who has the problem.", "No pitch to them unless they say it’s them."]},
        {"h": "Volume, the rule of 100", "p": ["100 actions a day for 100 days on one channel; most people get a first customer within weeks. Your plan does a Dutch version: two real conversations with owners a day, and no cold email, because in the Netherlands unsolicited commercial email needs consent."]},
        {"h": "Where it goes wrong", "l": ["Pitching your friends instead of asking for introductions.", "A target you can’t keep up, then stopping after week two."]},
        {"h": "Worked: one message", "p": ["‘I’m taking the weekly invoicing off small installers with AI, so they get their evenings back. Do you know an installer who’s drowning in admin?’ Two sentences, one ask, nothing to buy."]},
        {"h": "Your turn: your plan’s list", "p": ["Thirty names and the message for each; then the number of actions a day you’ll really keep for 100 days."]}],
  key=[{"t": "A good answer looks like", "l": ["Thirty names in groups: family, work, school, second-degree LinkedIn.", "A two-sentence message: what you do, and who they know.", "A daily number you’ll keep: e.g. five messages and your plan’s two conversations, every working day, counted in the app."]}],
  thread={"b": "B07 · cheaper ways to win clients; B08 · the audit to offer", "n": "B10 · content does the same, one to many; B11 · the call when they say yes"},
  rtask="Intensity Applied: who are the first 30 people you’d tell, and what’s the message?",
  rkey=[{"t": "Short answer", "l": ["People you’ve trained with, your gym, and lifters you already talk to online. ‘I built an app for lifters who’ve stalled. Do you know someone stuck on the same weights for months?’"]}])

EXTRA["B10"] = dict(
  teach="Content is warm outreach one-to-many: help the people who follow you, and the ones with the problem come to you. Give away the secrets, sell the implementation: show exactly how you did it, with a hook, something useful and real numbers.",
  walk=[{"h": "Why give it away", "p": ["Most owners who see exactly how you cut a firm’s invoicing from five hours to one still won’t do it themselves; they’ll want you to. The ones who do it alone were never your clients."]},
        {"h": "Every post", "l": [["A hook.", "One line that stops the scroll."], ["Something useful.", "What a reader could copy."], ["Proof.", "Real numbers from a real client, with their permission."]]},
        {"h": "Where it goes wrong", "l": ["Posting opinions without proof.", "Paid ads before an offer already sells."]},
        {"h": "Worked: one note", "p": ["Hook: ‘An installer’s Friday invoicing went from five hours to one.’ What we did: three steps, named. The result: four hours a week back, invoices out the same day. What you can copy: step one, written out."]},
        {"h": "Your turn: next week’s note", "p": ["The hook, what you did, the result in hours or euros, and what a reader could copy."]}],
  key=[{"t": "A good answer looks like", "l": ["A hook with a number in it.", "A result in hours or euros, from a pilot, with permission.", "Enough detail that someone could do it alone. That’s fine: it proves you know how, and most won’t."]}],
  thread={"b": "B07 · cheaper ways to win clients", "n": "B11 · the call when someone puts their hand up"},
  rtask="Intensity Applied: write one post’s hook, the useful part and the proof.",
  rkey=[{"t": "Short answer", "l": ["Hook: ‘Stuck on the same bench for six months? It’s probably recovery, not effort.’ Useful: the 3-day recovery rule. Proof: one user’s logged lifts before and after, with permission."]}])

EXTRA["B11"] = dict(
  teach="Hormozi’s sales call has six steps, CLOSER: clarify why they’re here, label the problem, overview what they tried, sell the vacation, explain away concerns, reinforce the decision. The owner talks most; your job is to ask until they’ve said why they need it.",
  walk=[{"h": "The six steps", "l": [["Clarify.", "‘What made you take this call?’"], ["Label.", "‘So what I’m hearing is…, does that sound right?’"], ["Overview the past.", "What they tried, and why it didn’t work."], ["Sell the vacation.", "The life after the result, not the steps in between."], ["Explain away concerns.", "With questions, not arguments."], ["Reinforce.", "After the yes, so it sticks."]]},
        {"h": "Where it goes wrong", "l": ["Skipping the overview, so you don’t know why the last fix failed.", "Selling the plane flight: the features, the tools, the process."]},
        {"h": "Worked: selling the vacation", "p": ["Plane flight: ‘We connect your invoicing software to an AI that drafts the invoices.’ Vacation: ‘On Friday at five, every invoice is out and you’re home for dinner.’"]},
        {"h": "Your turn: an owner from your interviews", "p": ["One or two questions for each letter, and the vacation in three sentences."]}],
  key=[{"t": "A good answer looks like", "l": ["C: ‘What made you say yes to this call?’ L: ‘So invoicing eats your Friday evenings, right?’ O: ‘What have you tried? Why did it stop?’",
        "S: the vacation in their words. E: ‘What would stop you?’ R: ‘What will you do with the Friday evenings?’",
        "The step most people skip is O, and without it you repeat whatever already failed for them."]}],
  thread={"b": "B04 · their problems; B08–B10 · how they reached the call", "n": "B12 · what the objections are really about"},
  rtask="Intensity Applied: what’s the vacation for a stalled lifter, in three sentences?",
  rkey=[{"t": "Short answer", "l": ["‘In eight weeks your logged lifts are going up again. You train four times a week and know exactly what to do each session. You stop wondering whether it’s working.’"]}])

EXTRA["B12"] = dict(
  teach="Objections sound different but come from three places: circumstances, other people, or the buyer’s own doubt. Don’t argue with the reason; ask about it, and most ‘I need to think about it’ turns out to be a concern you haven’t heard yet.",
  walk=[{"h": "The three sources", "l": [["Circumstances.", "‘No time’, ‘no money’, ‘not now’."], ["Other people.", "‘I need to ask my partner’, ‘my accountant handles that’."], ["Their own doubt.", "‘I’m not sure it will work for us’."]]},
        {"h": "Answer with a question", "l": ["‘If money weren’t an issue, would you do it?’ separates price from doubt.", "‘What would your partner want to know?’ brings them into the room.", "‘What’s the part you’d think about?’ finds the real concern."]},
        {"h": "Where it goes wrong", "l": ["Arguing, or dropping the price at the first objection.", "Taking ‘I’ll think about it’ as a no, or as a yes."]},
        {"h": "Your turn: the three you’ll hear most", "p": ["Your answers, as questions, and the source of each."]}],
  key=[{"t": "A good answer looks like", "l": ["‘I need to think about it’ (doubt): ‘Sure. What’s the part you’d think about?’", "‘It’s too expensive’ (circumstances, or doubt): ‘If it saves the 10 hours, is it still too much?’", "‘I need to ask my partner’ (other people): ‘What would they want to know? Shall we call them together?’",
        "The one that says your offer needs work: doubt that keeps coming back, ‘not sure it works for us’. That’s likelihood (B03): more proof, a stronger guarantee."]}],
  thread={"b": "B11 · the CLOSER call", "n": "B13 · what a client is worth, once they say yes"},
  rtask="Intensity Applied: the three objections a lifter gives before paying, and your question for each.",
  rkey=[{"t": "Short answer", "l": ["‘I can use a free app’ (circumstances): ‘Has the free one got you past the stall?’ ‘My coach does my program’ (other people): ‘Would they mind you logging recovery?’ ‘I’m not sure it’ll work’ (doubt): the refund guarantee and the logged lifts."]}])

EXTRA["B13"] = dict(
  teach="Lifetime value (LTV) is the gross profit a client brings in while they stay: monthly gross profit × the months they stay. Set it against what it cost to win them (CAC); a rule of thumb is at least 3:1, and every extra month a client stays raises what you can spend on finding the next.",
  walk=[{"h": "The two numbers", "l": [["LTV.", "Price × gross margin × months they stay."], ["LTV:CAC.", "How many times a client pays back what they cost to win. At 3:1 or more you can afford to grow; below it, every client is a struggle."]]},
        {"h": "Where it goes wrong", "l": ["Using revenue instead of gross profit.", "Guessing ‘clients stay for years’ before anyone has stayed a year."]},
        {"h": "Worked: the course’s example", "p": ["At €300 a month, an 80%% margin and clients staying 12 months: €300 × 0.8 × 12 = %s. Against a CAC of %s that is %.1f:1, room to spend more on finding clients." % (eur(LTV12), eur(CAC_B13), LTV12 / CAC_B13)]},
        {"h": "Your turn: your service", "p": ["LTV and LTV:CAC with your own guesses, then again with clients staying 6 months."]}],
  need=[PLAN, {"k": "Example guesses", "v": "80%% margin · 12 months · %s CAC" % eur(CAC_B13), "n": "From the course’s example; B07 worked out a CAC of %s with its assumed numbers." % eur(CAC)}],
  key=[{"t": "Worked answer", "l": ["12 months: LTV %s; LTV:CAC %.1f:1 at a %s CAC." % (eur(LTV12), LTV12 / CAC_B13, eur(CAC_B13)),
        "6 months: LTV %s; %.1f:1, just under the 3:1 line." % (eur(LTV6), LTV6 / CAC_B13),
        "With B07’s %s CAC: %.1f:1 at 12 months, %.1f:1 at 6 months; below 1:1, every client loses you money." % (eur(CAC), LTV12 / CAC, LTV6 / CAC),
        "The easier lever is usually the months they stay: a planned first month (B14) costs you hours, cutting CAC needs a new channel."]}],
  thread={"b": "B07 · what a client costs to win", "n": "B14 · keeping them longer"},
  rtask="Intensity Applied: work out LTV for a paying user at a price you choose, staying 4 months, and what you could spend to win one at 3:1.",
  rkey=[{"t": "Check it", "l": ["LTV = monthly price × your margin after store fees × 4. Spend at most LTV ÷ 3 to win one.", "App stores take a cut of each payment, so the margin is what’s left after it."]}])

EXTRA["B14"] = dict(
  teach="Churn is the share of clients who leave each month, a leaky bucket: you grow only while new clients come in faster than old ones leave. It is highest in the first month, so a planned first 30 days is the biggest win, and every cancellation is a question to ask.",
  walk=[{"h": "Why the first month", "p": ["Clients decide early whether it works. A quick visible result, a check-in, and a clear next step in the first 30 days keep more of them than anything you do in month six."]},
        {"h": "Track it", "l": ["Joins and cancels every month: growing, flat or shrinking, said honestly.", "Ask everyone who leaves why; look for the pattern every 20 or so.", "Ask your longest clients why they stay, and do more of that."]},
        {"h": "Where it goes wrong", "l": ["Counting only new clients.", "Not asking why people leave, because it stings."]},
        {"h": "Worked: a first 30 days", "l": ["Week 1: the first invoices go out, and the owner sees them.", "Day 14: a 15-minute check-in: what’s still on your desk?", "Day 30: the hours saved, in numbers, and the next task to take."]},
        {"h": "Your turn: a new client", "p": ["Plan their first 30 days, the two questions for a client who cancels, and the one for your best client."]}],
  key=[{"t": "A good answer looks like", "l": ["A dated plan: something visible in week one, a check-in, a number at day 30.", "For a cancel: ‘What made you decide?’ and ‘What would have made you stay?’ For your best client: ‘Why do you stay?’",
        "Month two’s biggest risk: they stop noticing the result. Show the hours saved every month."]}],
  thread={"b": "B13 · every extra month raises LTV", "n": "B15 · grow what works"},
  rtask="Intensity Applied: what happens in a new user’s first 30 days so they stay?",
  rkey=[{"t": "Short answer", "l": ["Session one: a logged baseline. Week one: the recovery lock shows them which muscles are ready. Day 30: their logged lifts against day one, on one screen."]}])

EXTRA["B15"] = dict(
  teach="When something works, the order is more, then better, then new: do more of what brings clients until it stops scaling, then fix the weakest step, and only then try a new channel, niche or product. Most small businesses jump to new before they’ve squeezed what works.",
  walk=[{"h": "The order", "l": [["More.", "More conversations, more notes, until it stops scaling."], ["Better.", "The weakest step: the share of calls that become clients, or the hours each client takes."], ["New.", "Only then a new channel, niche or product."]]},
        {"h": "Where it goes wrong", "l": ["‘New’ because the current thing got boring, not because it stopped working.", "Fixing something that isn’t the weakest step."]},
        {"h": "Worked: your plan’s year", "l": ["More: two conversations a day becomes three.", "Better: automate one delivery step at a time towards 1.5 hours a client (B07).", "New, not yet: the software for the trade in year two, once ten clients share the same need."]},
        {"h": "Your turn: your plan’s year", "p": ["Where you are on more, better, new; the one ‘more’ next month, the ‘better’ after, and the ‘new’ you’re not allowed to start yet."]}],
  key=[{"t": "A good answer looks like", "l": ["One ‘more’ with a number, one ‘better’ with the step named, and one ‘new’ written down as not yet.", "What tempts you to jump: usually boredom or a shiny idea. The cost: the clients the current thing would have brought."]}],
  thread={"b": "B11–B14 · selling, keeping, and what a client is worth", "n": "the offer to three firms; the course is done"},
  rtask="Intensity Applied: what’s its ‘more’, its ‘better’ and the ‘new’ it isn’t allowed yet?",
  rkey=[{"t": "Short answer", "l": ["More: get it into the store and in front of more lifters. Better: the first-30-days flow (B14). Not yet: new features or a second app."]}])

GLOSSARY = [
    (3, "value equation", r"value equation"), (4, "Grand Slam Offer", r"grand slam"),
    (5, "guarantee", r"\bguarantee"), (5, "scarcity and urgency", r"\bscarcity\b|\burgency\b"), (5, "MAGIC name", r"\bMAGIC\b"),
    (7, "gross margin", r"gross margin|gross profit"), (7, "CAC", r"\bCAC\b|cost to acquire"), (7, "client-financed", r"client-financed|30-day cash"),
    (8, "lead magnet", r"lead magnet"), (9, "rule of 100", r"rule of 100"), (9, "core four", r"core four"),
    (11, "CLOSER", r"\bCLOSER\b"), (11, "sell the vacation", r"sell the vacation"), (12, "objections", r"\bobjections?\b"),
    (13, "LTV", r"\bLTV\b|lifetime value"), (14, "churn", r"\bchurn"), (15, "more, better, new", r"more, better, new|more-better-new"),
]

def check_extra():
    e = lambda a, b, tol=0.5: abs(a - b) <= tol or sys.exit(f"bad number: {a} vs {b}")
    e((120 - 80) / (100 - 80), 2, 0); e(3 * 2 / 3, 2, 1e-9)                      # the margin maths, the gym
    e(VALUE, 600); e(GP_NOW, 110); e(GP_GOAL, 210); e(CAC_HOURS, 39); e(CAC, 1560); e(LTV12, 2880); e(LTV6, 1440)
    for lid, x in EXTRA.items():
        assert 150 < len(x["teach"]) < 1100, (lid, len(x["teach"]))

for x in L:
    x.update(EXTRA[x["id"]])

def check():
    e = lambda a, b, tol=0.5: abs(a - b) <= tol or sys.exit(f"bad number: {a} vs {b}")
    e(10 * 60, 600); e(600 / 2, 300); e(300 * 0.8 * 12, 2880); e(2880 / 500, 5.76, 0.01)
check()
check_extra()

C = course({"goal_id": "goal_biz", "key": "biz", "title": "Offers & sales with Hormozi", "azTitle": "Offers & sales with Hormozi, A → Z",
     "rungs": ["Market", "Offer", "Price", "Leads", "Sell", "Keep"],
     "rungDesc": ["pick a starving crowd, and narrow it until it hurts", "the value equation, problems into solutions, and the extras that make it a yes",
                  "price on value, and let clients pay for your growth", "lead magnets, warm outreach, and content with proof",
                  "the CLOSER call, and what objections are really about", "what a client is worth, churn, and more-better-new"],
     "blurb": "One question on your own offer per sitting: the AI service your Making money with AI plan pilots with small firms, and the revisit on Intensity Applied. Written in my words from Alex Hormozi’s videos in your library.",
     "allDone": "now make the offer to three firms. 💼",
     "revWord": "another offer",
     "refNote": "The idea opens in step 2 of the sitting — guess first. The videos are Hormozi’s, for when you want more; the revenue figures in them are Hormozi’s own claims."}, L)
check_videos(C)
check_extras(C["lessons"])
FLAGS = term_order(C["lessons"], GLOSSARY, "B")
if FLAGS:
    sys.exit("A lesson uses a term before the lesson that teaches it, with no pointer:\n  " + "\n  ".join(FLAGS))
write("BIZ_CURRICULUM", ["Offers & sales with Hormozi — 15 sittings on the Business goal, in my words from Alex Hormozi's videos in the",
      "youtube-digest library: market, offer (value equation, problems into solutions, guarantees, MAGIC), price, leads (lead magnets,",
      "warm outreach, the rule of 100, content), the CLOSER call, objections, LTV:CAC and churn. Runs on your AI service; revisits on",
      "Intensity Applied. Built by scripts/build-business-course.py."], C)
