# Builds the "Options with Henry" course (OPT_CURRICULUM) in time-tracker.html: 18 lessons written from the Invest with Henry
# transcripts in the youtube-digest library. Video titles and links are looked up from that library so none are typed by hand.
#   python3 scripts/build-options-course.py [path/to/youtube-digest/data/library.json]   -> rewrites the block in time-tracker.html
import json, re, sys, os
LIB_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "youtube-digest", "data", "library.json")
LIB = json.load(open(LIB_PATH))["videos"]
def W(vid, why):
    v = LIB[vid]; assert v["channel"] == "Invest with Henry" and v.get("transcript_available"), vid
    return {"t": "Invest with Henry · " + v["title"].strip(), "u": "https://www.youtube.com/watch?v=" + vid, "w": why}

L = []
def lesson(rung, stage, concept, teach, task, co, rev, after, watch):
    n = len(L) + 1
    L.append({"id": "H%02d" % n, "order": n, "rung": rung, "stage_name": stage, "concept": concept, "estimateMin": 30,
              "teach": teach, "task": task, "co": co, "rev": rev, "after": after, "watch": watch, "track": "opt"})

# ---------- I Learn ----------
lesson("Learn", "What an option is", "A right for the buyer, a duty for the seller",
  "One contract covers 100 shares. A call is the right to buy at the strike price until expiry; a put is the right to sell at it. The buyer pays the premium for that right and can lose at most the premium. The seller collects the premium and takes on the duty: to buy the shares (a sold put) or hand them over (a sold call) if the buyer exercises. That gives four positions: buy a call (you think it rises), buy a put (you think it falls), sell a put (you’re fine owning it lower) and sell a call (you’re fine selling it higher). Henry builds almost everything on the two selling ones, because the seller is paid up front and time works for the seller. A bought call breaks even at strike plus premium; a sold put at strike minus premium.",
  "On AAPL’s option chain (your broker or Yahoo Finance), take the call and the put nearest today’s price, about a month out. For each of the four positions write what you pay or collect for one contract (premium × 100), the break-even, and the most you can lose. Judge: if you think AAPL drifts sideways for a month, which of the four would you pick, and why?",
  "AAPL", "MSFT", [],
  [W("SXd-v1z5AY8", "the opening hour: calls, puts, strike, expiry and premium")])
lesson("Learn", "Reading the chain", "Strike, expiry, bid–ask, volume and open interest",
  "The chain lists every strike for each expiry, calls on one side and puts on the other. In the money means it would have value if exercised now: a call with its strike below the stock price, a put with its strike above it. Henry’s three checks before any trade are volume, open interest and the bid–ask spread. A tight spread (cents on a liquid name) means you get filled near a fair price; a wide one costs you on the way in and again on the way out. Henry prefers the monthly expiry, the third Friday, because it keeps managing simple; weeklies work but need watching. Enter with a limit order around the middle of bid and ask.",
  "Open SPY and a small company you know, same monthly expiry. For a strike near the price, write bid, ask, volume and open interest, and work out the spread as a share of the middle price. Judge: above what spread would you skip a trade, and does the small company pass?",
  "SPY", "QQQ", [],
  [W("05MfiNo99T4", "the open interest, volume and bid–ask check, on a live chain")])
lesson("Learn", "Delta, theta and IV", "The three Greeks Henry actually uses",
  "Delta says how much the option moves for a $1 move in the stock, and roughly the chance it ends in the money: 0.30 is about 30%. That’s a model’s estimate, not a promise, but it’s the gauge Henry picks strikes by. Theta is time decay: what the option loses per day, which the seller collects. It speeds up in the last weeks and is biggest near the money, where the chance of assignment is biggest too. Implied volatility (IV) is the move the market expects. High IV means richer premiums, so selling pays more; low IV means cheap options, which favours buying. Before earnings IV rises, and after the report it collapses: the IV crush. Gamma and vega exist, but for selling around 30 delta and 30 days out, Henry barely uses them.",
  "Find SPY’s 30-delta put about 30 days out and write its premium, theta and IV. Do the same on TSLA. Work out each premium as a % of its strike. Judge: why does TSLA pay so much more for the same delta, and what are you being paid to accept?",
  "SPY", "QQQ", [],
  [W("yRTUVGOQmwE", "delta as a risk gauge, theta, vega"), W("L4q9k4J4t9c", "when high IV favours selling and low IV favours buying")])

# ---------- II Sell ----------
lesson("Sell", "Selling a cash-secured put", "Get paid to wait for a price you’d buy at",
  "You sell a put on a stock you’d be happy to own, and keep the cash for 100 shares at the strike. Henry’s defaults: about 30 delta (20–30 when you start), about 30 days out, a strike 5–10% below the price and under support. Your return is the premium divided by the cash you set aside; your break-even is strike minus premium. At 30 delta you keep the premium roughly seven times in ten. The other times you buy the shares, and to Henry owning is not losing. But the maximum loss is real: strike minus premium if the stock collapses. The research Henry quotes is the honest anchor: selling one-month puts on S&P 500 stocks earned about what holding the index did (7.1% against 7.3% a year over ten years) with smaller swings. That’s good, and nowhere near the 50–100% a year a weekly premium seems to promise when you multiply it up.",
  "Paper-sell one KO put at about 30 delta, 30 days out. Write the strike, premium, cash set aside, break-even and return on that cash. Then KO closes 15% lower at expiry: what do you own, at what price, and what is it worth? Judge: is KO a company you’d really hold for a year at that strike?",
  "KO", "PEP", ["H01", "H03"],
  [W("BfZjRQ6k49E", "strikes 5–10% below the price, and why 30 delta"), W("FaeloW8e0-I", "the research: about the index’s return, with smaller drops")])
lesson("Sell", "Choosing the stock and the strike", "A company you’d own, a strike under support, a size you can carry",
  "Henry starts with the business: real revenue and earnings, a sensible price (P/E, or price-to-sales for growth companies), something you’d hold anyway, and no assets without earnings, like crypto. Then the strike: under a support level the stock has bounced from, around 30 delta, with the break-even below support, so an assignment still lands at a price you like. Henry checks volume and the spread, and around earnings goes further out of the money or skips the week. Then size: Henry won’t sell new puts on a stock that’s already about 10% of the portfolio. This is where your investing course meets this one: a sold put is a limit order you get paid for, so the company still has to be worth owning.",
  "Shortlist three US companies you’d own. For each, note the last clear support level, the 30-delta put strike a month out, the next earnings date and the cash one put ties up. Judge: which one fits your trading money, and which would you drop first?",
  "MSFT", "AAPL", ["H02", "H03"],
  [W("u7q-xPaRvoQ", "fundamentals first: revenue, earnings, P/E and P/S"), W("3uqr_tf8fr8", "support levels and Bollinger Bands for picking strikes")])
lesson("Sell", "Covered calls", "Rent out shares you already own",
  "Own 100 shares, sell a call above what you paid, keep the premium. Henry’s default is the same: about 30 delta, about 30 days. The price is the cap: above the strike the gains are the buyer’s. Being called away isn’t a loss if the strike is above your cost; you keep the premium plus the gain. (Henry’s worry about the tax on that sale is an American one; a Dutch private investor’s gains normally sit in box 3, see H17.) Early assignment is rare, because an option with time left is worth more sold than exercised; the risk rises in the last days, deep in the money. Henry’s list of mistakes leads with FOMO: paying to roll up when the stock runs. If it runs and you want to keep the shares, roll up and out, adding time.",
  "Say you own 100 KO at today’s price. Paper-sell a 30-delta call about 30 days out: write the premium, the most you can make if called away, and the price above which you’d have done better without the call. Judge: KO jumps 10% in a week. Let the shares go, or roll?",
  "KO", "PEP", ["H01", "H03"],
  [W("1U9IUZbaYdM", "why early assignment is rare, with a deep in-the-money example"), W("TShirzRDBWU", "assignment, FOMO and support levels")])
lesson("Sell", "The wheel", "Puts until assigned, calls until called away, repeat",
  "The wheel joins the last three lessons: sell puts until you’re assigned, sell covered calls on those shares until they’re called away, start again. Its rule is that you’re never afraid of assignment, which only holds for companies you want. Henry runs it monthly, about 30 delta, 30–40 days out. The weak spot is a hard fall: calls above your cost then pay almost nothing, so you wait. Henry says it plainly: if it drops 20%, you wait and hope it recovers. Henry’s own SPY example earns about 1% a month, 12–15% a year; more only by mixing in spreads. That’s the realistic range, not the headline numbers. One Dutch catch: EU retail investors usually can’t buy US ETFs like SPY (they have no EU key information document), so whether a SPY put assignment works depends on your broker. Wheel a US stock instead.",
  "Run one wheel on paper on KO: the put you’d sell now and, if assigned, the call you’d sell the month after. Write both premiums and what the shares cost you net. Judge: KO falls 20% right after assignment. What do you do for the next three months?",
  "KO", "PEP", ["H03"],
  [W("leI79Bjzd5k", "the full cycle and its rules"), W("O8QsM6gy47k", "monthly expiries, 30 delta, and when 40–50 delta makes sense")])

# ---------- III Manage ----------
lesson("Manage", "Exits", "Decide how you get out before you get in",
  "Henry’s exits differ by trade. A sold put on a stock you like: hold to expiry, take the shares if assigned, roll at most once. A bought option or LEAPS: take profit at 30–50% with a limit order placed the day you buy, and cut at minus 50%; sooner if the stock breaks support or the story changes, which Henry calls admitting defeat. A credit spread: close it if the price reaches your short strike. Write the rules down before you enter, because every rule is easy at the start and hard when the trade is red.",
  "Write exit rules for three paper trades: your KO put, your KO covered call, and a call you’d buy on AAPL. For each: when you take profit, when you cut, and what you do at expiry. Judge: which rule will you be most tempted to break?",
  "AAPL", "MSFT", ["H04", "H06"],
  [W("FxWzFhA8By4", "the 50% rule, and rolling only once"), W("LBLv_254OP8", "managing a 30-delta put from entry to exit")])
lesson("Manage", "Rolling for a credit", "Add time, move the strike your way, get paid for it",
  "Rolling is closing one option and opening another in the same order; most brokers have a roll button that sends it as one spread. Sold puts roll down and out, covered calls up and out. Henry’s rule of thumb, the “DOG” roll: a few dollars down, about 30 days out, and only for a net credit. Time plus volatility is premium, so rolls pay better on higher-IV stocks. The traps: rolling too early or too late, chasing a falling stock down again and again, and paying a debit to roll up out of FOMO. Henry prefers to roll a put once, then take the shares or close. A roll doesn’t remove the risk; it buys time.",
  "Your paper KO put is in the money with a week left. Find a roll: new strike, new expiry, net credit or debit. Compare three choices: roll, let it assign, close for a loss. Judge: which one do your exit rules from H08 pick?",
  "KO", "PEP", ["H04", "H07"],
  [W("jn0w_Ue65uA", "up and out, down and out, for a credit"), W("QG9F2JbthC8", "rolling too early, too late, or when you should close")])

# ---------- IV Spread ----------
lesson("Spread", "Put credit spreads", "Sell a put with a floor under it",
  "Sell a put and buy a lower one with the same expiry. You collect the difference in premium, and your loss is capped at the width minus that credit. Henry uses $5 widths ($1 on small accounts), with the short strike under support at about 15–20 delta. It needs far less cash than a cash-secured put, which is why it suits small accounts. The return on risk looks big, 20–50% in a few weeks, because what you risk is bigger than what you win: one full loss can wipe out several winners. Henry closes when the price reaches the short strike, and sizes each spread at 1–3% of the portfolio, 5% at most. Henry lost heavily on one $200,000 spread, which was about 5% of a $4M portfolio.",
  "Paper a $5-wide SPY put credit spread with the short strike near 15–20 delta, about 30 days out. Write the credit, the max loss, the break-even, and the chance of a full win from delta. Judge: how many full wins pay for one max loss, and is that worth it?",
  "SPY", "QQQ", ["H08", "H09"],
  [W("KaCXI5HCXB8", "$5 widths, sizing, and managing a losing spread"), W("_x8yfPAAgYI", "short strikes under support, and spreading strikes out")])
lesson("Spread", "Call credit and debit spreads", "Bearish income, or a cheaper bullish bet",
  "A call credit spread is the mirror image: sell a call above resistance, buy a higher one, collect a credit. Henry keeps those around 12–15 delta. A bull call (debit) spread buys a call and sells a higher one, so it costs less than the call alone but caps the upside. Break-even is the long strike plus what you paid; the most you can make is the width minus that. Henry uses these when a move is expected soon, often earnings, 1–2 weeks out, and says plainly that selling suits Henry better than buying.",
  "AAPL, same expiry about a month out: compare buying one call near the money with a $5-wide bull call spread. Write the cost, break-even, max profit and max loss of each. Judge: AAPL ends 3% higher. Which did better, and why?",
  "AAPL", "MSFT", ["H08"],
  [W("xBnyH5dJBuI", "break-even and max profit, worked through"), W("--7laF-OZQw", "12–15 delta call credit spreads")])
lesson("Spread", "Iron condors", "Get paid for a stock that goes nowhere",
  "An iron condor is a put credit spread plus a call credit spread. You win if the price stays between the two short strikes until expiry, and the max loss is one side’s width minus the total credit, because only one side can lose. Henry’s setup: short strikes around 12–24 delta, $3–5 wings, about 30 days, never through earnings. Close or adjust a side when the price reaches its short strike. Henry keeps condors at 5–10% of the portfolio altogether; 15% is already risky.",
  "Build a QQQ iron condor on paper: about 30 days out, short strikes near 15 delta, $5 wings. Write the credit, the max loss, the range you need, and the events before expiry (earnings of the biggest holdings, a Fed meeting). Judge: which single event could break it?",
  "QQQ", "SPY", ["H08", "H09"],
  [W("1WPMpVhewds", "why no earnings, and the max-loss maths"), W("GMLZ-xk8Sp8", "12-delta shorts, and sizing at 5–15%")])

# ---------- V Long ----------
lesson("Long", "LEAPS", "A long-dated call instead of 100 shares",
  "A LEAPS is a call with a year or more to run. Henry buys around 0.7 delta, deep in the money, 9–12 months out or longer. It moves about 70 cents for each $1 in the stock, for a fraction of what 100 shares cost, and time decay stays small until the last months. Henry’s list of mistakes: cheap low-delta “LEAPS” (a 10-delta is a lottery ticket), calling a three-month option a LEAPS, buying when IV is pumped up before earnings or hype, and buying too many. Exits: take profit at 30–50%, cut at minus 50% or when support breaks. Delta grows as it wins, so trim to keep the exposure you meant to have.",
  "Compare 100 MSFT shares with one 0.7-delta call 12 months out: the cost, the break-even at expiry, and the gain or loss if MSFT moves 10% up or 10% down in a month. Judge: what’s the worst case for each a year from now?",
  "MSFT", "AAPL", ["H11"],
  [W("J9ohf_y6Qi4", "0.7 delta, and taking profit at 30–50%"), W("CdAoVqJ1lWc", "delta management and the IV crush")])
lesson("Long", "The poor man’s covered call", "Sell monthly calls against a LEAPS",
  "Swap the 100 shares of a covered call for a LEAPS: buy a 0.7-delta call 9–12 months out, then sell 30-delta calls about 30 days out against it, just like Henry’s usual covered calls. Henry’s NVDA example tied up about 85% less capital than shares would. The risks change, though. If the stock jumps past your short call, you manage both legs: roll the short call up and out, or close both. If it falls, the LEAPS loses faster than shares would, with no dividend and its own time decay. Some brokers can’t roll it as one order, so you close one leg and open the next.",
  "Design one on MSFT on paper: the LEAPS you’d buy, the call you’d sell this month, the capital tied up, and the month’s premium as a % of it. Then two scenarios: MSFT +15% in a month, and MSFT −15%. Judge: which hurts more, and what would you do?",
  "MSFT", "AAPL", ["H11"],
  [W("wIUYaUyjwf8", "0.7-delta LEAPS with 30-delta short calls"), W("1jZQ_y0q6xE", "managing and rolling both legs")])
lesson("Long", "Earnings and IV crush", "Why the stock can rise and your option still fall",
  "Before earnings, implied volatility climbs, because a big move is coming. After the report it collapses, so an option bought just before can lose value even when the stock moves your way. Henry’s answers: don’t buy out-of-the-money calls into earnings; sell instead (a covered call, or a put further out of the money that you’d be happy to be assigned on); keep iron condors away from earnings; give LEAPS enough time that one report doesn’t matter. Henry also says research shows buying in-the-money calls before earnings works. The videos don’t show that research, so treat it as unproven.",
  "Look up NVDA’s next earnings date. Compare the IV of an option expiring just after it with one a month later, and price the at-the-money straddle just after earnings: that’s the move the market expects. Judge: NVDA rises 3% on the report. What happens to a call you bought the day before?",
  "NVDA", "AMD", ["H11", "H12"],
  [W("6lfcSLiyjho", "what an IV crush looks like on the chain"), W("6pyIvuT532Y", "what Henry would and wouldn’t do into earnings")])

# ---------- VI Plan ----------
lesson("Plan", "Position sizing", "Small enough that one loss can’t sink you",
  "Henry sizes most trades at 2–5% of the portfolio, spreads at 1–3% and never above 5%, and iron condors at 5–10% together, and stops adding to one stock at about 10%. For a sold put, size by what you’d lose in a crash, not by the margin your broker asks for. Henry argues a tiny account can take bigger bets; that holds for learning money, not for money you need. Your Trading branch already has the rule that matters most: decide your trading money (an amount you can afford to lose, kept apart from your FIRE investments) and risk at most 1% of it on one trade.",
  "With your trading money from the Trading branch, write the most you’d lose on one trade, the most in one stock, and the most in spreads and condors together. Then check each paper trade from this course against those limits, starting with a SPY spread. Judge: which ones would you have to shrink?",
  "SPY", "QQQ", ["H13", "H15"],
  [W("L4q9k4J4t9c", "2–5% per position, and why size depends on the account"), W("X9ibF2v1RKA", "options as a way to control risk, with a collar")])
lesson("Plan", "Your paper-trading plan", "Fifty journaled trades before real money, Dutch rules included",
  "Pull the course into one plan: the strategies you’ll paper trade (start with cash-secured puts and covered calls), Henry’s defaults (30 delta, 30 days, rolls only for a credit, the 50% rule on bought options), your size and exit rules, and a journal: why in, why out, what you learned. Your Options branch already asks for 50 paper trades and a review of win rate against average win and average loss. Two Dutch checks before real money. First, whether your broker offers US options at your level, and what happens on assignment (US ETFs like SPY usually can’t be bought by EU retail investors). Second, tax: a private investor’s options normally fall in box 3 (in 2026, 36% on a fixed return of 7.78% for other assets), but very active trading can count as box 1. Check with the Belastingdienst or an adviser.",
  "Write your one-page plan as if you start with KO puts next month: strategies, defaults, size limits, exit and roll rules, and what you log per trade. Ask your broker in writing how US option assignment works for you. Judge: what result after 50 paper trades would make you stop instead of going live?",
  "KO", "PEP", ["H14"],
  [W("hiEv_Ra3thg", "the whole playbook in one course, from the Greeks to the wheel")])
lesson("Plan", "Judging Henry", "Keep the method, discount the marketing",
  "Henry’s rules are concrete and conservative: cash-secured, about 30 delta, about 30 days, roll for a credit, small sizes. Keep those. Discount the headlines. A weekly 2% multiplied up to 96% a year assumes no losing weeks and no fall in the shares you get assigned. The income figures come from Henry’s own portfolio, and the channel sells a paid Discord and coaching. Henry is also open about losses, like that $200,000 spread. The research Henry cites, put-selling earning about what the index earns with smaller drops, is the fairest expectation. Your FIRE plan assumes 5% a year above inflation; an options plan that needs far more than that needs luck.",
  "Pick one headline from Henry’s titles (say, $8,000 a month selling puts) and rebuild it on SPY: the capital it needs at 2% a month, and what happens to that year if, one month, the market drops 20% and you’re assigned. Judge: what return would you write into your FIRE plan for options, and why?",
  "SPY", "QQQ", ["H13"],
  [W("5BVlq4sTqt8", "small, steady returns, and never a losing month as the goal"), W("L56cWBsbaco", "how a weekly 2% becomes “96% a year”")])

assert len(L) == 18
rungs = ["Learn", "Sell", "Manage", "Spread", "Long", "Plan"]
for l in L:
    assert l["rung"] in rungs
    for a in l["after"]: assert rungs.index(next(x for x in L if x["id"] == a)["rung"]) == rungs.index(l["rung"]) - 1, (l["id"], a)
    for k in ("teach", "task", "concept"):
        assert not re.search(r"\b(he|him|his|himself)\b", l[k], re.I), (l["id"], k, "pronoun")
        assert "<" not in l[k] and '"' not in l[k], (l["id"], k)
course = {
  "goal_id": "goal_opt", "key": "opt", "title": "Options with Henry", "azTitle": "Options with Henry, A → Z",
  "rungs": rungs,
  "rungDesc": ["what an option is, how to read the chain, the Greeks Henry uses",
               "get paid to wait: cash-secured puts, covered calls, the wheel",
               "exit rules, and rolling for a credit",
               "define the risk: credit spreads, debit spreads, iron condors",
               "buy time instead of shares: LEAPS, the poor man’s covered call, earnings",
               "size it, plan 50 paper trades, judge the claims"],
  "blurb": "One options question on a real ticker per sitting, written in my words from the Invest with Henry videos in your library. Paper trade only: Henry’s rules are concrete, the income figures are Henry’s own claims, and your Options branch asks for 50 paper trades before real money.",
  "allDone": "now paper trade your plan. 📈",
  "revWord": "another ticker",
  "refNote": "The idea opens in step 2 of the sitting — guess first. The videos are Henry’s, for when you want more; the income figures in them are Henry’s own claims.",
  "lessons": L,
}
js = json.dumps(course, ensure_ascii=False, indent=None, separators=(",", ":"))
js = js.replace('{"id":', '\n    {"id":')
block = ("  /* Options with Henry — 18 sittings written from the Invest with Henry transcripts in the youtube-digest library (videos up to\n"
         "     15 Oct 2026), in my words. Every lesson runs on a real ticker, on paper; the revisit uses its `rev` ticker. `after` names the\n"
         "     lessons one tier down that it builds on, for the tech tree. Only done-flags and revisits are ever saved into app-state. */\n"
         "  var OPT_CURRICULUM=" + js + ";\n")
FILE = os.path.join(os.path.dirname(__file__), "..", "time-tracker.html")
html = open(FILE, encoding="utf8").read()
m = re.search(r"  /\* Options with Henry — 18 sittings[\s\S]*?\n  var OPT_CURRICULUM=\{[\s\S]*?\};\n", html)
assert m, "OPT_CURRICULUM block not found"
open(FILE, "w", encoding="utf8").write(html[:m.start()] + block + html[m.end():])
print("wrote", len(L), "lessons,", sum(len((l["teach"] + " " + l["task"]).split()) for l in L), "words, into", os.path.normpath(FILE))
