# Builds the "Options with Henry" course (OPT_CURRICULUM) in time-tracker.html: 18 lessons written from the Invest with Henry
# transcripts in the youtube-digest library. Video titles and links are looked up from that library so none are typed by hand.
#   python3 scripts/build-options-course.py [path/to/youtube-digest/data/library.json]   -> rewrites the block in time-tracker.html
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from course_block import check_extras, term_order, lesson_texts
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
  "Say you own 100 KO at today’s price. Paper-sell a 30-delta call about 30 days out: write the premium, the most you can make if called away, and the price above which you’d have done better without the call. Judge: KO jumps 10% in a week. Let the shares go, or roll (H09)?",
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
  "Pull the course into one plan: the strategies you’ll paper trade (start with cash-secured puts and covered calls), Henry’s defaults (30 delta, 30 days, rolls only for a credit, the 50% rule on bought options), your size and exit rules, and a journal: why in, why out, what you learned. Your Options branch already asks for 50 paper trades and a review of win rate against average win and average loss. Two Dutch checks before real money. First, whether your broker offers US options at your level, and what happens on assignment (US ETFs like SPY usually can’t be bought by EU retail investors). Second, tax: a private investor’s options normally fall in box 3 (in 2026, 36% on a fixed return of 6.00% for other assets), but very active trading can count as box 1. Check with the Belastingdienst or an adviser.",
  "Write your one-page plan as if you start with KO puts next month: strategies, defaults, size limits, exit and roll rules, and what you log per trade. Ask your broker in writing how US option assignment works for you. Judge: what result after 50 paper trades would make you stop instead of going live?",
  "KO", "PEP", ["H14"],
  [W("hiEv_Ra3thg", "the whole playbook in one course, from the Greeks to the wheel")])
lesson("Plan", "Judging Henry", "Keep the method, discount the marketing",
  "Henry’s rules are concrete and conservative: cash-secured, about 30 delta, about 30 days, roll for a credit, small sizes. Keep those. Discount the headlines. A weekly 2% multiplied up to 96% a year assumes no losing weeks and no fall in the shares you get assigned. The income figures come from Henry’s own portfolio, and the channel sells a paid Discord and coaching. Henry is also open about losses, like that $200,000 spread. The research Henry cites, put-selling earning about what the index earns with smaller drops, is the fairest expectation. Your FIRE plan assumes 5% a year above inflation; an options plan that needs far more than that needs luck.",
  "Pick one headline from Henry’s titles (say, $8,000 a month selling puts) and rebuild it on SPY: the capital it needs at 2% a month, and what happens to that year if, one month, the market drops 20% and you’re assigned. Judge: what return would you write into your FIRE plan for options, and why?",
  "SPY", "QQQ", ["H13"],
  [W("5BVlq4sTqt8", "small, steady returns, and never a losing month as the goal"), W("L56cWBsbaco", "how a weekly 2% becomes “96% a year”")])

# ---- each lesson's idea, walk-through, numbers box, worked answer, thread and revisit -------------------------------
# Worked examples are Henry's own, from the videos each lesson cites (round numbers, often undated; labelled as Henry’s).
# Prices: Yahoo Finance closes on 11 Nov 2026. No option quotes: the chain is yours to read on the day, so the
# answers give the method and every number that follows from the stock price alone.
ASOF = "11 Nov 2026"
PX = {"KO": 97.57, "PEP": 143.94, "AAPL": 355.63, "MSFT": 521.13, "SPY": 759.81, "QQQ": 690.38, "NVDA": 173.73, "AMD": 552.90, "TSLA": 390.84}
EURUSD_OPT = 1.1169
def yq(t): return {"s": "Yahoo Finance · %s close, %s" % (t, ASOF), "u": "https://finance.yahoo.com/quote/%s/history/" % t}
def usd(x, d=0): return ("−" if x < 0 else "") + "$" + format(abs(x), ",.%df" % d)
def pq(t): return {"k": "%s, last close" % t, "v": usd(PX[t], 2), **yq(t)}
KO_K = 90                                # a strike about 8% under KO's price
KO_DOWN = round(PX["KO"] * 0.85, 2)
KO_VALUE = 61.79                         # the investing course's KO value per share (2025 data, with a moat)
POT_USD = 2000 * EURUSD_OPT              # the Forex course's €2,000, in dollars
H = lambda *x: list(x)

EXTRA = {}
EXTRA["H01"] = dict(
  teach="One contract covers 100 shares. A call is the right to buy at the strike price until expiry, a put the right to sell at it; the buyer pays the premium and can lose only that, while the seller collects it and takes on the duty. That makes four positions: buy or sell a call, buy or sell a put.",
  walk=[{"h": "The four positions", "l": [["Buy a call.", "You think it rises. Break-even: strike + premium. Most you can lose: the premium."], ["Buy a put.", "You think it falls. Break-even: strike − premium."], ["Sell a put.", "You’re fine owning it lower. Break-even: strike − premium. Most you can lose: (strike − premium) × 100 if it goes to zero."], ["Sell a call.", "You’re fine selling it higher. Without the shares, the loss has no ceiling."]]},
        {"h": "Why Henry sells", "p": ["The seller is paid up front and time works for the seller: every day the option loses some value. Henry builds almost everything on selling puts and selling calls against shares already owned (H06)."]},
        {"h": "Where it goes wrong", "l": ["Forgetting the × 100: a $5 premium is $500.", "Selling calls without owning the shares."]},
        {"h": "Worked: Henry’s round numbers", "l": ["Stock at $100; buy a $105 call for $5: you pay $500, break even at $110, and lose at most $500.", "Stock at $100; sell a $100 put for $1: you collect $100, and if you’re handed the shares your cost is $99."]},
        {"h": "Your turn: AAPL", "p": ["The call and the put nearest today’s price, about a month out: for each of the four positions, the money in or out, the break-even and the most you can lose."]}],
  need=[pq("AAPL"), {"k": "One contract", "v": "100 shares", "n": "Premiums are quoted per share: × 100."}],
  key=[{"t": "Check it", "l": ["Strike nearest %s: about $%d. Premiums are yours to read; then:" % (usd(PX["AAPL"], 2), round(PX["AAPL"] / 5) * 5),
        "Bought call: pay premium × 100; break-even strike + premium; lose at most what you paid. Bought put: break-even strike − premium.",
        "Sold put: collect premium × 100; break-even strike − premium; most you can lose about (strike − premium) × 100, around %s. Sold call without shares: no ceiling." % usd((round(PX["AAPL"] / 5) * 5) * 100),
        "Sideways for a month: the two selling positions, because time decay pays the seller."]}],
  thread={"n": "H02 · reading the chain; H04 and H06 · the two positions Henry sells"},
  rtask="MSFT: the four positions at the strike nearest today’s price. What’s the most each can lose?",
  rneed=[pq("MSFT")],
  rkey=[{"t": "Short answer", "l": ["Bought call or put: the premium. Sold put: about the strike × 100 less the premium, around %s. Sold call without shares: no ceiling." % usd(round(PX["MSFT"] / 5) * 5 * 100)]}])

EXTRA["H02"] = dict(
  teach="The chain lists every strike for each expiry, calls on one side and puts on the other. Before any trade Henry checks three things: volume, open interest and the bid–ask spread; a tight spread means a fair fill, a wide one costs you on the way in and again on the way out.",
  walk=[{"h": "Reading it", "l": [["In the money.", "It would have value if exercised now: a call with its strike below the price, a put with its strike above."], ["Out of the money.", "The rest; what Henry sells."], ["Expiry.", "Henry prefers the monthly one, the third Friday, because it keeps managing simple."]]},
        {"h": "The three checks", "l": ["Volume: how many traded today.", "Open interest: how many contracts are open.", "The spread as a share of the middle price: (ask − bid) ÷ the middle."]},
        {"h": "Where it goes wrong", "l": ["Selling at the bid with a market order on a wide spread.", "Trading strikes nobody else trades."]},
        {"h": "Worked: a spread, in money", "p": ["Bid $2.40, ask $2.60: the middle is $2.50 and the spread is $0.20, 8% of the middle. Selling at the bid instead of the middle costs $10 a contract, and again when you close. Henry enters with a limit order around the middle."]},
        {"h": "Your turn: SPY and a small company", "p": ["Same monthly expiry, a strike near the price: bid, ask, volume, open interest, and the spread as a share of the middle."]}],
  need=[pq("SPY")],
  key=[{"t": "Check it", "l": ["Spread % = (ask − bid) ÷ ((ask + bid) ÷ 2).", "SPY’s near-the-money options usually show a spread of cents on a price of dollars, a small share; a small company’s can be ten times wider.", "A sensible skip line: wider than about 5–10% of the middle, or open interest in the tens rather than the thousands."]}],
  thread={"b": "H01 · strike, expiry, premium", "n": "H03 · the Greeks on the same chain"},
  rtask="QQQ: write bid, ask, volume and open interest for one strike near the price, and the spread as a share of the middle.",
  rneed=[pq("QQQ")],
  rkey=[{"t": "Check it", "l": ["Spread % = (ask − bid) ÷ the middle. QQQ should pass easily; if it doesn’t, check you’re on a monthly expiry near the price."]}])

EXTRA["H03"] = dict(
  teach="Delta is how much the option moves for a $1 move in the stock, and roughly the chance it ends in the money; theta is what time takes from it each day; implied volatility (IV) is the move the market expects. High IV means rich premiums for the seller, and after earnings IV collapses: the IV crush.",
  walk=[{"h": "Delta", "p": ["0.30 moves about 30 cents for a $1 move, and is about a 30% chance of ending in the money. A model’s estimate, not a promise, but it’s the gauge Henry picks strikes by."]},
        {"h": "Theta and IV", "l": [["Theta.", "Time decay, collected by the seller; it speeds up in the last weeks."], ["IV.", "The expected move. High IV: richer premiums, which favour selling. Low IV: cheap options, which favour buying."], ["IV crush.", "Before earnings IV climbs; after the report it collapses."]]},
        {"h": "Where it goes wrong", "l": ["Reading a high premium as free money: it pays for a bigger expected move.", "Treating delta as a promise."]},
        {"h": "Worked: Henry’s Apple and NVIDIA", "p": ["On one chain Apple’s IV read 25.88%; NVIDIA’s, Henry pointed out, was higher, because NVIDIA moves up and down more. Same delta, bigger premium on NVIDIA: the market expects bigger moves."]},
        {"h": "Your turn: SPY and TSLA", "p": ["The 30-delta put about 30 days out on each: premium, theta and IV, and the premium as a % of the strike."]}],
  need=[pq("SPY"), pq("TSLA")],
  key=[{"t": "Check it", "l": ["Premium as % of strike = premium ÷ strike. Expect TSLA’s to be several times SPY’s.", "Why: TSLA’s IV is far higher. Same delta means a similar chance of ending in the money, but when it does, the drop can be much deeper.", "What you’re paid to accept: the bigger, sharper moves."]}],
  thread={"b": "H02 · reading the chain", "n": "H04 · picking a put by delta and days"},
  rtask="QQQ: a 30-delta put about 30 days out. Premium as a % of the strike, and why it’s more than SPY’s.",
  rkey=[{"t": "Short answer", "l": ["Premium ÷ strike. More than SPY’s because QQQ is concentrated in a few large tech companies, so its IV is higher."]}])

EXTRA["H04"] = dict(
  teach="Sell a put on a stock you’d be happy to own and keep the cash for 100 shares at the strike: about 30 delta, about 30 days out. Your return is the premium ÷ the cash, your break-even is strike − premium, and the research Henry quotes puts the long-run return near the index’s, with smaller swings.",
  walk=[{"h": "Henry’s defaults", "l": ["About 30 delta (20–30 when you start), about 30 days out.", "A strike 5–10% under the price, and under a level it has bounced from (H05).", "Cash set aside: strike × 100."]},
        {"h": "The numbers", "l": ["Return on the cash: premium ÷ strike.", "Break-even: strike − premium.", "Most you can lose: (strike − premium) × 100, if it goes to zero."]},
        {"h": "The honest anchor", "p": ["The research Henry quotes: selling one-month puts on S&P 500 stocks earned about what holding the index did, 7.1% against 7.3% a year over ten years, with smaller drops. Good, and nowhere near the 50–100% a year that multiplying one week’s premium seems to promise."]},
        {"h": "Worked: Henry’s NVIDIA", "p": ["NVIDIA at $180; sell the $170 put for $5. You collect $500, set aside $17,000, break even at $165, and earn 2.9% on the cash if it stays above $170. If it falls to $150, you own 100 shares at $170, worth $15,000: down $1,500 after the premium."]},
        {"h": "Your turn: KO", "p": ["One KO put at about 30 delta, 30 days out: strike, premium, cash, break-even, return. Then KO 15% lower at expiry."]}],
  need=[pq("KO"), {"k": "A strike 5–10% under", "v": "%s–%s" % (usd(PX["KO"] * 0.90), usd(PX["KO"] * 0.95))}, {"k": "Your KO value (investing course)", "v": usd(KO_VALUE, 2), "n": "Per share, from 2025 data, with a moat."}],
  key=[{"t": "Check it, with a $%d strike" % KO_K, "l": ["Cash set aside: %s. Break-even: $%d − your premium. Return: premium ÷ $%d." % (usd(KO_K * 100), KO_K, KO_K),
        "KO 15%% lower is %s: you own 100 shares at $%d, worth %s, down %s before the premium you kept." % (usd(KO_DOWN, 2), KO_K, usd(KO_DOWN * 100), usd((KO_K - KO_DOWN) * 100)),
        "Would you hold KO for a year at $%d? Your investing course values it at %s a share: a $%d strike is buying at about %.1f times that value. The put pays you to wait, but the strike is still a price you’re agreeing to." % (KO_K, usd(KO_VALUE, 2), KO_K, KO_K / KO_VALUE)]}],
  thread={"b": "H01 · break-even and max loss; H03 · picking by delta", "n": "H05 · choosing the stock and strike; H07 · what happens after assignment"},
  rtask="PEP: a put about 7% under the price. Cash, break-even, and what a 15% fall leaves you with.",
  rneed=[pq("PEP"), {"k": "Your PEP values (investing revisit)", "v": "$152.06 · $94.84", "n": "With a moat · without."}],
  rkey=[{"t": "Short answer", "l": ["A strike near %s: cash about %s. A 15%% fall to %s leaves 100 shares worth %s against %s paid, less the premium." % (usd(round(PX["PEP"] * 0.93)), usd(round(PX["PEP"] * 0.93) * 100), usd(PX["PEP"] * 0.85, 2), usd(PX["PEP"] * 85), usd(round(PX["PEP"] * 0.93) * 100)), "That strike sits between your no-moat and moat values: a price you could defend."]}])

EXTRA["H05"] = dict(
  teach="Henry starts with the business: real revenue and earnings, a sensible price, something you’d hold anyway. Then the strike: under a level the stock has bounced from, around 30 delta, with the break-even below it. Then the size: no new puts once a stock is about 10% of the portfolio.",
  walk=[{"h": "The order", "l": [["The company.", "Real revenue and earnings, a sensible P/E or price-to-sales; no assets without earnings."], ["The strike.", "Under support, a level the stock bounced from; around 30 delta; break-even below support."], ["The calendar.", "The next earnings date: go further out of the money, or skip that month."], ["The size.", "Cash for one put = strike × 100; stop adding at about 10% of the portfolio in one stock."]]},
        {"h": "Where it goes wrong", "l": ["Choosing the stock for its premium.", "Forgetting how much cash one put ties up."]},
        {"h": "Worked: one put’s cash, %s" % ASOF, "l": ["KO near %s: a put about 8%% under ties up about %s." % (usd(PX["KO"], 2), usd(KO_K * 100)), "AAPL near %s: about %s." % (usd(PX["AAPL"], 2), usd(round(PX["AAPL"] * 0.92) * 100)), "MSFT near %s: about %s." % (usd(PX["MSFT"], 2), usd(round(PX["MSFT"] * 0.92) * 100))], **yq("KO")},
        {"h": "Your turn: three companies you’d own", "p": ["For each: support, the 30-delta put a month out, the next earnings date, the cash one put ties up."]}],
  need=[pq("MSFT"), pq("AAPL"), pq("KO")],
  key=[{"t": "Check it", "l": ["Three rows: support level, strike under it, earnings date, cash = strike × 100.", "Which fits your trading money: with the Forex course’s €2,000 (about %s), none of these as a cash-secured put; one KO put alone is about four times the pot (H16)." % usd(POT_USD), "Drop first: the one with earnings inside the month, or the one you’d least like to own after a 20% fall."]}],
  thread={"b": "H04 · a cash-secured put", "n": "H06 · covered calls on the shares; H16 · sizing against your trading money"},
  rtask="AAPL: where is its support, and how much cash does one put under it tie up?",
  rneed=[pq("AAPL")],
  rkey=[{"t": "Short answer", "l": ["Read support off the chart; a strike about 8%% under the price ties up about %s." % usd(round(PX["AAPL"] * 0.92) * 100)]}])

EXTRA["H06"] = dict(
  teach="Own 100 shares, sell a call above what you paid, keep the premium: about 30 delta, about 30 days. The strike is the cap, since above it the gains are the buyer’s; being called away isn’t a loss if the strike is above your cost.",
  walk=[{"h": "How it works", "l": ["Sell one call per 100 shares, above your cost.", "Above the strike the shares are called away: you keep the premium and the gain up to the strike.", "Below it you keep the premium and the shares."]},
        {"h": "Where it goes wrong", "l": ["FOMO: paying to buy the call back when the stock runs. Henry lists it first among the mistakes.", "A strike below your cost, locking in a loss."]},
        {"h": "Worked: Henry’s Apple", "p": ["Apple at $220; sell the $230 call for $5, $500. If Apple goes to $240, you sell at $230: you keep the $500 and $1,000 of gain, and miss the last $1,000. If Apple drops to $200, the call expires and you keep the $500, against $2,000 lost on the shares."]},
        {"h": "Your turn: 100 KO", "p": ["A 30-delta call about 30 days out: the premium, the most you make if called, and the price above which you’d have done better without the call."]}],
  need=[pq("KO")],
  key=[{"t": "Check it", "l": ["With a strike about 5%% up, say $%.2f: most you make if called = (strike − %s) × 100 + premium × 100 = %s + your premium." % (round(PX["KO"] * 1.05 * 2) / 2, usd(PX["KO"], 2), usd((round(PX["KO"] * 1.05 * 2) / 2 - PX["KO"]) * 100)),
        "You’d have done better without the call above strike + premium.", "KO +10%% in a week (%s): let them go if you’re happy selling at the strike; Henry’s alternative is to roll up and out for a credit (H09), never to pay up out of FOMO." % usd(PX["KO"] * 1.1, 2)]}],
  thread={"b": "H04 · selling puts", "n": "H07 · puts and calls in turn: the wheel"},
  rtask="PEP: 100 shares, a call about 5% up. The most you make if called, and the price above which the call cost you.",
  rneed=[pq("PEP")],
  rkey=[{"t": "Short answer", "l": ["Strike about %s: (strike − %s) × 100 + premium. Above strike + premium you’d have done better without it." % (usd(PX["PEP"] * 1.05), usd(PX["PEP"], 2))]}])

EXTRA["H07"] = dict(
  teach="The wheel joins the last three lessons: sell puts until you’re assigned, sell covered calls on those shares until they’re called away, start again. It only works on companies you’re glad to own, and its weak spot is a hard fall, when calls above your cost pay almost nothing.",
  walk=[{"h": "The cycle", "l": ["Sell a put; if assigned, you own 100 shares at the strike, less the premium.", "Sell calls above that cost until called away.", "Start again. Henry runs it monthly, about 30 delta, 30–40 days out."]},
        {"h": "Realistic returns", "p": ["Henry’s own SPY example earns about 1% a month, 12–15% a year; more only by mixing in spreads. And EU retail investors usually can’t buy US ETFs like SPY, so wheel a US stock."]},
        {"h": "Where it goes wrong", "l": ["A 20% fall after assignment: calls above your cost pay little, so you wait. Henry: ‘you wait and hope it recovers’.", "Wheeling something you don’t want to own."]},
        {"h": "Worked: Henry’s SoFi", "l": ["SoFi at $28; sell the $27 put for about $1: $100. Assigned: your cost is $26 a share.", "Sell the $28 call for $0.70: $70. Called away: $200 of gain plus $70, $270 on $2,700 of cash, 10% in about two months."]},
        {"h": "Your turn: KO", "p": ["The put you’d sell now and, if assigned, the call the month after: both premiums and the net cost of the shares."]}],
  need=[pq("KO")],
  key=[{"t": "Check it", "l": ["Net cost of the shares = put strike − put premium − call premium.", "With a $%d put: $%d − both premiums." % (KO_K, KO_K),
        "KO falls 20%% after assignment (to about %s): calls at or above your cost pay little. Sell small ones and wait, or sell below cost only if you accept locking in the loss when called." % usd(KO_K * 0.8)]}],
  thread={"b": "H04 · puts; H06 · covered calls", "n": "H08 · exits, before you get in"},
  rtask="PEP: one turn of the wheel. Put strike, call strike, and the net cost of the shares.",
  rkey=[{"t": "Check it", "l": ["Net cost = put strike − both premiums. The call strike sits at or above it."]}])

EXTRA["H08"] = dict(
  teach="Decide how you get out before you get in, and write it down. Henry’s exits differ by trade: a sold put on a stock you like is held to expiry, a bought option takes profit at 30–50% and is cut at −50%, and a spread is closed when the price reaches its short strike.",
  walk=[{"h": "By trade", "l": [["A sold put you like.", "Hold to expiry, take the shares if assigned, roll at most once (H09). Or close early when you’ve made half the premium fast."], ["A bought option (or LEAPS, H13).", "Take profit at 30–50% with a limit order placed the day you buy; cut at −50%, or sooner if support breaks."], ["A spread (H10).", "Close when the price reaches your short strike."]]},
        {"h": "Where it goes wrong", "l": ["Rules written after the trade turned red.", "Holding a winner to the last day for the last few dollars."]},
        {"h": "Worked: Henry’s 50% close", "p": ["A $105 put sold 40 days out for $323 was worth $162 seven days later: half the premium in about a sixth of the time. Henry bought it back and freed the cash."]},
        {"h": "Your turn: three trades", "p": ["Exit rules for your KO put, your KO covered call, and a call you’d buy on AAPL."]}],
  key=[{"t": "A good answer looks like", "l": ["KO put: hold to expiry, or close at 50% of the premium if it comes fast; take the shares if assigned.", "KO covered call: let the shares go at the strike, or roll once for a credit (H09).", "AAPL call: sell at +30–50% with a limit order placed today; cut at −50% or if support breaks.", "The rule most people break: the cut at −50% on the bought call."]}],
  thread={"b": "H04, H06, H07 · the trades you’d hold", "n": "H09 · rolling, the one exit that buys time"},
  rtask="MSFT: exit rules for a put you sold and a call you bought.",
  rkey=[{"t": "Short answer", "l": ["Sold put: hold or close at 50%, take the shares if assigned. Bought call: +30–50% limit order on day one, −50% stop."]}])

EXTRA["H09"] = dict(
  teach="Rolling closes one option and opens another in the same order: sold puts roll down and out, covered calls up and out, and only for a net credit. A roll doesn’t remove the risk, it buys time; Henry rolls a put once, then takes the shares or closes.",
  walk=[{"h": "Henry’s ‘DOG’ roll", "l": ["A few dollars Down.", "Out about 30 days.", "Get paid: a net credit, never a debit."]},
        {"h": "Where it goes wrong", "l": ["Rolling too early or too late.", "Chasing a falling stock down again and again.", "Paying a debit to roll up out of FOMO."]},
        {"h": "Worked: Henry’s Nike", "p": ["A $65 put sold; Nike fell to $60. Henry rolled down to $60 and out about a month, for a credit: the new strike meets the stock where it is, and the extra time pays for the move."]},
        {"h": "Your turn: your KO put", "p": ["In the money with a week left: find a roll, then compare roll, take the shares, or close at a loss."]}],
  key=[{"t": "Check it", "l": ["Roll: new strike lower, about 30 days more, net credit = new premium − cost to close the old.", "Take the shares: your cost is the strike − the premium you kept.", "Close: the loss is what it costs to buy back − the premium you got.", "Henry’s rules from H08 pick: roll once if there’s a credit, otherwise take the shares if you still want KO."]}],
  thread={"b": "H08 · exit rules", "n": "H10 · spreads, where the risk is capped from the start"},
  rtask="PEP: your covered call is in the money with a week left. Roll, let it go, or buy it back?",
  rkey=[{"t": "Short answer", "l": ["Let it go if the strike is above your cost. Roll up and out only for a net credit. Buying it back for a debit is the FOMO trade Henry warns against."]}])

EXTRA["H10"] = dict(
  teach="A put credit spread sells a put and buys a lower one with the same expiry: you collect the difference, and your loss is capped at the width minus that credit. It needs far less cash than a cash-secured put, but one full loss can wipe out several winners.",
  walk=[{"h": "The numbers", "l": ["Credit = premium sold − premium bought.", "Max loss = (width − credit) × 100.", "Break-even = short strike − credit.", "Chance of keeping it all ≈ 1 − the short put’s delta."]},
        {"h": "Henry’s rules", "l": ["$5 widths ($1 on small accounts); short strike under support at 15–20 delta.", "Close when the price reaches the short strike.", "1–3% of the portfolio a spread, 5% at most. Henry lost heavily on one $200,000 spread, about 5% of $4M."]},
        {"h": "Where it goes wrong", "l": ["Reading the return on risk as a return on safety: you risk far more than you win.", "No exit at the short strike."]},
        {"h": "Worked: Henry’s SoFi", "p": ["Sell the $11 put for $0.40, buy the $10 put for $0.20: a $0.20 credit, $20. Max loss: ($1 − $0.20) × 100 = $80. Break-even $10.80. It takes four full wins to pay for one full loss."]},
        {"h": "Your turn: SPY", "p": ["A $5-wide put credit spread, short strike near 15–20 delta, 30 days out: credit, max loss, break-even, chance of a full win."]}],
  need=[pq("SPY")],
  key=[{"t": "Check it, with a $1.00 credit as an example", "l": ["Max loss: ($5 − $1) × 100 = $400. Break-even: short strike − $1.", "Full win chance about 80–85% at 15–20 delta.",
        "Full wins needed to pay one max loss: $400 ÷ $100 = 4. At an 80% win rate: 0.8 × $100 − 0.2 × $400 = $0 a trade before costs. The edge has to come from closing losers early."]}],
  thread={"b": "H09 · rolling; H08 · exits", "n": "H11 · call spreads; H12 · two spreads at once"},
  rtask="QQQ: a $5-wide put credit spread for a $0.80 credit. Max loss, and full wins needed per max loss.",
  rkey=[{"t": "Short answer", "l": ["Max loss $420; break-even short strike − $0.80; 5.25 full wins pay for one full loss."]}])

EXTRA["H11"] = dict(
  teach="A call credit spread mirrors the put one, above resistance. A bull call (debit) spread buys a call and sells a higher one: cheaper than the call alone, with the upside capped. Henry uses debit spreads when a move is expected soon, and says plainly that selling suits Henry’s style better than buying.",
  walk=[{"h": "The numbers", "l": ["Bull call spread: debit = long call − short call.", "Break-even: long strike + debit. Max profit: (width − debit) × 100. Max loss: the debit.", "Call credit spread: sell above resistance at 12–15 delta, buy higher."]},
        {"h": "Where it goes wrong", "l": ["Buying calls into a move that’s smaller than the premium paid.", "Forgetting the cap: a big move earns no more than the width."]},
        {"h": "Worked: Henry’s Apple", "p": ["Buy the 165 call for $4.63 ($463), sell the 170 call for $2.69 ($269): a debit of $1.94, $194. Break-even $166.94. Most you can make: ($5 − $1.94) × 100 = $306; most you can lose: $194."]},
        {"h": "Your turn: AAPL", "p": ["About a month out: one call near the money against a $5-wide bull call spread. Cost, break-even, max profit and max loss of each."]}],
  need=[pq("AAPL")],
  key=[{"t": "Check it", "l": ["Call: break-even strike + premium; no cap; lose at most the premium.", "Spread: break-even long strike + debit; cap (5 − debit) × 100.",
        "AAPL +3%% is about %s. A near-the-money call’s premium is mostly time value that a 3%% move barely covers; the spread costs less and pays its full width once AAPL is $5 above the long strike, so for a small move the spread usually does better." % usd(PX["AAPL"] * 1.03, 2)]}],
  thread={"b": "H10 · put credit spreads", "n": "H12 · iron condors; H13 · long calls held a year"},
  rtask="MSFT: a $5-wide bull call spread a month out. Break-even and max profit with your debit.",
  rkey=[{"t": "Check it", "l": ["Break-even = long strike + debit; max profit (5 − debit) × 100; max loss the debit."]}])

EXTRA["H12"] = dict(
  teach="An iron condor is a put credit spread plus a call credit spread: you win if the price stays between the two short strikes. The max loss is one side’s width minus the total credit, because only one side can lose; never hold one through earnings.",
  walk=[{"h": "The numbers", "l": ["Total credit = both spreads’ credits.", "Max loss = (one width − total credit) × 100.", "Break-evens: short put − credit, short call + credit."]},
        {"h": "Henry’s setup", "l": ["Short strikes around 12–24 delta, $3–5 wings, about 30 days, never through earnings.", "Close or adjust a side when the price reaches its short strike.", "5–10% of the portfolio in condors together; 15% is already risky."]},
        {"h": "Worked: Henry’s Facebook condor", "p": ["$5 wings and a total credit of $164: max loss ($5 × 100) − $164 = $336, and a return of 49% on the risk if Facebook stayed inside the range for six weeks."]},
        {"h": "Your turn: QQQ", "p": ["30 days out, short strikes near 15 delta, $5 wings: credit, max loss, the range, and the events before expiry."]}],
  need=[pq("QQQ")],
  key=[{"t": "Check it", "l": ["Max loss = $500 − total credit; range = short put − credit to short call + credit.", "Events: the biggest holdings’ earnings (NVIDIA, Microsoft, Apple and the rest of the top ten) and any Fed meeting before expiry.", "The single event most likely to break it: a top-three holding’s earnings, or a Fed surprise."]}],
  thread={"b": "H10–H11 · put and call spreads", "n": "H15 · why condors stay away from earnings"},
  rtask="SPY: an iron condor with $5 wings for a $1.40 total credit. Max loss, and the return on risk if it works.",
  rkey=[{"t": "Short answer", "l": ["Max loss $360; return on risk $140 ÷ $360 = 39%."]}])

EXTRA["H13"] = dict(
  teach="A LEAPS is a call with a year or more to run. Henry buys around 0.7 delta, 9–12 months out or longer: it moves about 70 cents for each $1 in the stock for a fraction of what 100 shares cost, and time decay stays small until the last months.",
  walk=[{"h": "What to buy", "l": ["About 0.7 delta, deep in the money.", "9–12 months out or longer; a three-month option isn’t a LEAPS.", "Not when IV is pumped up before earnings or hype."]},
        {"h": "Exits", "l": ["Take profit at 30–50%; cut at −50% or when support breaks.", "Delta grows as it wins: trim to keep the exposure you meant to have."]},
        {"h": "Where it goes wrong", "l": ["Cheap low-delta ‘LEAPS’: a 10-delta is a lottery ticket.", "Buying several where you’d have bought 100 shares once."]},
        {"h": "Worked: Henry’s SoFi", "p": ["Instead of $50,000 in shares, Henry controls the same with $10,000–15,000 of LEAPS. Going deeper, a 0.86-delta $10 call cost $8: more like owning the shares, with diminishing returns for the extra cost."]},
        {"h": "Your turn: MSFT", "p": ["100 shares against one 0.7-delta call 12 months out: the cost, the break-even, and a 10% move either way in a month."]}],
  need=[pq("MSFT")],
  key=[{"t": "Check it", "l": ["100 shares: %s. The LEAPS: its premium × 100, a fraction of that; break-even strike + premium at expiry." % usd(PX["MSFT"] * 100),
        "A 10%% move is about %s a share: the shares gain or lose %s; the LEAPS about 0.7 × that, %s, on far less money, so a bigger share of what you put in." % (usd(PX["MSFT"] * 0.1, 2), usd(PX["MSFT"] * 10), usd(PX["MSFT"] * 7)),
        "Worst case in a year: the shares can fall but you still own them; the LEAPS expires worthless below its strike, and you lose all of the premium."]}],
  thread={"b": "H11 · bought calls and their break-even", "n": "H14 · selling calls against a LEAPS"},
  rtask="AAPL: the cost of 100 shares against a 0.7-delta LEAPS, and what each does on a 10% drop.",
  rneed=[pq("AAPL")],
  rkey=[{"t": "Short answer", "l": ["Shares %s, down %s on a 10%% drop; the LEAPS down about 0.7 × that, %s, a bigger share of a smaller stake." % (usd(PX["AAPL"] * 100), usd(PX["AAPL"] * 10), usd(PX["AAPL"] * 7))]}])

EXTRA["H14"] = dict(
  teach="The poor man’s covered call swaps the 100 shares for a LEAPS: buy a 0.7-delta call 9–12 months out, then sell 30-delta calls about 30 days out against it. It ties up far less capital, but if the stock falls the LEAPS loses a bigger share of what you paid than shares would, and a jump past the short call means managing both legs.",
  walk=[{"h": "How it works", "l": ["Long leg: a LEAPS, about 0.7 delta, 9–12 months.", "Short leg: a 30-delta call about 30 days out, sold each month.", "If the stock jumps past the short call: roll it up and out, or close both."]},
        {"h": "Where it goes wrong", "l": ["A fall: the LEAPS loses a bigger share of its cost than shares do, pays no dividend and has its own time decay.", "Brokers that can’t roll it as one order: close one leg, then open the next."]},
        {"h": "Worked: Henry’s NVIDIA", "p": ["NVIDIA at $104: 100 shares would cost $10,400; the LEAPS about a quarter of that. Selling a 30-day call against it collected, in Henry’s example, ‘6–7%’ of the LEAPS’ cost for the month: Henry’s figure, in a strong stock."]},
        {"h": "Your turn: MSFT", "p": ["The LEAPS, this month’s call, the capital tied up, the premium as a % of it; then MSFT ±15% in a month."]}],
  need=[pq("MSFT")],
  key=[{"t": "Check it", "l": ["Capital = the LEAPS’ premium × 100. Month’s return = the short call’s premium ÷ that.",
        "+15%% (about %s): the short call is deep in the money; roll it up and out for a credit, or close both and keep the gain on the LEAPS." % usd(PX["MSFT"] * 1.15, 2),
        "−15%%: the LEAPS loses about 0.7 × %s × 100 = %s, plus time value, while the call premium is small. The fall hurts more." % (usd(PX["MSFT"] * 0.15, 2), usd(PX["MSFT"] * 0.15 * 70))]}],
  thread={"b": "H06 · covered calls; H13 · LEAPS", "n": "H15 · earnings and the IV crush"},
  rtask="AAPL: design one poor man’s covered call. What does a 15% drop do to it?",
  rkey=[{"t": "Short answer", "l": ["LEAPS at about 0.7 delta, monthly 30-delta calls. A 15%% drop costs the LEAPS about 0.7 × %s × 100 = %s, far more than a month’s premium." % (usd(PX["AAPL"] * 0.15, 2), usd(PX["AAPL"] * 0.15 * 70))]}])

EXTRA["H15"] = dict(
  teach="Before earnings implied volatility climbs, and after the report it collapses, so an option bought just before can lose value even when the stock moves your way. Henry sells into earnings rather than buying: a covered call, a put further out of the money, condors kept away, LEAPS with time to spare.",
  walk=[{"h": "The expected move", "p": ["The at-the-money straddle (a call and a put at the same strike) just after the report is roughly the move the market expects. A move smaller than that loses money for the buyer, whichever way it goes."]},
        {"h": "Henry’s answers", "l": ["Don’t buy out-of-the-money calls into earnings.", "Sell instead: a covered call, or a put further out that you’d be happy to be assigned on.", "Keep iron condors away from earnings (H12); give LEAPS enough time that one report doesn’t matter (H13)."]},
        {"h": "What to discount", "p": ["Henry also says research shows buying in-the-money calls before earnings works. The videos don’t show that research, so treat it as unproven."]},
        {"h": "Worked: Henry’s NVIDIA after earnings", "p": ["Assigned at $130, Henry sells covered calls at or above that cost, the $135, and goes further out in time for a lower strike that still pays: about 26 delta."]},
        {"h": "Your turn: NVDA", "p": ["The next earnings date, the IV just after it against a month later, and the straddle price: the expected move."]}],
  need=[pq("NVDA")],
  key=[{"t": "Check it", "l": ["Expected move ≈ the straddle price ÷ the stock price. IV for the expiry just after earnings should be well above the one a month later.", "NVDA +3%%: if the straddle prices a move of, say, 7%% (about %s), the call bought the day before likely loses: its IV collapses by more than the 3%% move adds." % usd(PX["NVDA"] * 0.07, 2)]}],
  thread={"b": "H03 · IV and the crush; H11–H14 · the trades it hits", "n": "H16 · sizing every one of these"},
  rtask="AMD: the expected earnings move from the straddle, and what Henry would sell into it.",
  rneed=[pq("AMD")],
  rkey=[{"t": "Short answer", "l": ["Straddle ÷ price. Henry would sell: a covered call above cost, or a put further out than usual, worth taking assignment on."]}])

PUT_MULT = KO_K * 100 / POT_USD
EXTRA["H16"] = dict(
  teach="Henry sizes most trades at 2–5% of the portfolio, spreads at 1–3% and condors at 5–10% together, and stops adding to a stock at about 10%. Size a sold put by what you’d lose in a crash, not by the margin your broker asks. Your trading branch adds the rule that matters most: 1% of your trading money a trade.",
  walk=[{"h": "Two sets of rules", "l": [["Henry’s.", "2–5% a trade, spreads 1–3% (5% at most), condors 5–10% together, about 10% in one stock."], ["Yours, from Forex X01–X02.", "A trading pot you could lose, and at most 1% of it a trade."]]},
        {"h": "Where it goes wrong", "l": ["Sizing a sold put by the broker’s margin instead of the crash loss.", "Henry’s point that a tiny account can take bigger bets: fine for learning money, not for money you need."]},
        {"h": "Worked: €2,000 against US options", "l": ["€2,000 is about %s." % usd(POT_USD), "One KO cash-secured put at $%d ties up %s, about %.0f times the whole pot." % (KO_K, usd(KO_K * 100), PUT_MULT),
            "A $1-wide spread risks up to about $80, about %.1f%% of the pot; 1%% is about %s." % (80 / POT_USD * 100, usd(POT_USD * 0.01)),
            "So €2,000 can’t trade US options under a 1% rule. Paper-trade at a notional size you’d really use, or set a separate, larger options pot in X01, knowingly."]},
        {"h": "Your turn: your trading money", "p": ["The most on one trade, in one stock, and in spreads and condors together; then check each paper trade from this course against them."]}],
  need=[{"k": "Trading money (Forex X01)", "v": "€2,000 ≈ %s" % usd(POT_USD), "n": "At EUR/USD %.4f, %s." % (EURUSD_OPT, ASOF)}, pq("SPY"), pq("KO")],
  key=[{"t": "Check it, on €2,000", "l": ["1%% a trade: €20, about %s." % usd(POT_USD * 0.01), "One stock (Henry’s 10%%): about %s; spreads and condors together (5–10%%): about %s–%s." % (usd(POT_USD * 0.10), usd(POT_USD * 0.05), usd(POT_USD * 0.10)),
        "Shrink: every cash-secured put and covered call in this course (one KO put alone is about %s), and every $5 spread. Even a $1 spread is several times the 1%% rule." % usd(KO_K * 100),
        "So decide: paper-trade at a notional account size, or a bigger options pot. Not by quietly breaking the rule."]}],
  thread={"b": "H13–H15 · the trades to size; Forex X01–X02 · the trading pot and the 1% rule", "n": "H17 · the paper-trading plan"},
  rtask="QQQ: what notional account would let one $5-wide spread fit Henry’s 1–3%?",
  rkey=[{"t": "Short answer", "l": ["A $5 spread with a $0.50 credit risks $450. At 3% that needs a $15,000 account; at 1%, $45,000."]}])

EXTRA["H17"] = dict(
  teach="Pull the course into one page: the strategies you’ll paper trade, Henry’s defaults, your size and exit rules, and a journal of why in, why out and what you learned. Fifty paper trades before real money, and two Dutch checks: what your broker allows, and how your trading is taxed.",
  walk=[{"h": "The page", "l": ["Strategies: start with cash-secured puts and covered calls.", "Defaults: 30 delta, 30 days, rolls only for a credit, the 50% rule on bought options.", "Size and exits: from H16 and H08.", "The journal: the same columns as the Forex journal, so one journal serves both."]},
        {"h": "The Dutch checks", "l": [["Your broker.", "Whether it offers US options at your level, and what happens on assignment; US ETFs like SPY usually can’t be bought by EU retail investors."], ["Tax.", "A private investor’s options normally fall in box 3 (in 2026, 36% on a fixed return of 6.00% for other assets); very active trading can count as box 1. Check with the Belastingdienst or an adviser."]]},
        {"h": "Where it goes wrong", "l": ["A plan longer than one page.", "Starting live because paper feels slow."]},
        {"h": "Worked: one page, short", "l": ["Strategies: KO and PEP cash-secured puts; covered calls if assigned.", "Rules: 30 delta, 30 days, close at 50% early, roll once for a credit.", "Size: notional $20,000 paper account; no stock above 10%.", "Stop rule: after 50 trades, if on-plan trades lose or I broke the rules more than five times."]},
        {"h": "Your turn: KO puts next month", "p": ["Your one-page plan, and the written question to your broker about US option assignment."]}],
  key=[{"t": "A good answer looks like", "l": ["Every section on one page, with numbers.", "A stop rule decided now: e.g. on-plan trades losing after 50, or more than five rule breaks.", "One journal for Forex and Options, same columns."]}],
  thread={"b": "H16 · sizing; Forex X09–X12 · the journal and the go/no-go test", "n": "H18 · judging the headlines"},
  rtask="PEP: rewrite your one-page plan for PEP puts. What changes?",
  rkey=[{"t": "Short answer", "l": ["The strike and the cash it ties up (PEP is about %s a share); the rules, the journal and the stop rule stay the same." % usd(PX["PEP"], 2)]}])

CAP_8K = 8000 / 0.02
EXTRA["H18"] = dict(
  teach="Keep Henry’s method and discount the marketing. The rules are concrete and conservative: cash-secured, about 30 delta, about 30 days, roll for a credit, small sizes. The headlines multiply one good week into a year and leave out the falls; the research Henry cites, roughly the index’s return with smaller drops, is the fair expectation.",
  walk=[{"h": "What to keep", "p": ["Cash-secured, about 30 delta, about 30 days, roll for a credit, small sizes, and the openness about losses, like the $200,000 spread."]},
        {"h": "What to discount", "l": ["A weekly 2% multiplied to 96% a year: it assumes no losing weeks and no fall in the shares you’re assigned.", "Income figures from Henry’s own portfolio, on a channel that sells a paid Discord and coaching."]},
        {"h": "Worked: Henry’s Microsoft put", "p": ["Sell the $400 put for $5: break-even $395, $500 collected on $40,000 of cash, 1.25% for the month. Multiply by twelve and it looks like 15% a year; one 20% fall while you’re assigned costs $8,000, more than a year of those premiums."]},
        {"h": "Your turn: one headline", "p": ["Rebuild it on SPY: the capital it needs at 2% a month, and the year with one 20% fall while assigned."]}],
  need=[pq("SPY"), {"k": "Your FIRE plan’s return", "v": "5% a year above inflation"}],
  key=[{"t": "Check it: ‘$8,000 a month’", "l": ["At 2%% a month it needs %s of cash: about %d SPY puts at %s." % (usd(CAP_8K), round(CAP_8K / (PX["SPY"] * 100)), usd(PX["SPY"], 2)),
        "Twelve good months: $96,000. One 20%% fall while assigned: −%s. The year nets about %s, %s on the capital: below the index, with more work and the same crash risk." % (usd(CAP_8K * 0.2), usd(96000 - CAP_8K * 0.2), "%.0f%%" % ((96000 - CAP_8K * 0.2) / CAP_8K * 100)),
        "For your FIRE plan: write in no more than the index’s return for options, 5% above inflation; a plan that needs far more needs luck."]}],
  thread={"b": "H17 · your paper-trading plan", "n": "fifty paper trades, then your go/no-go test"},
  rtask="QQQ: ‘1% a week selling puts’. What does a year look like with one 25% fall while assigned?",
  rkey=[{"t": "Short answer", "l": ["52% a year on paper; one 25% fall while assigned takes half of it back, before any other losing week."]}])

GLOSSARY = [
    (2, "in/out of the money", r"in the money|out of the money|at the money"), (2, "open interest", r"open interest"), (2, "bid–ask", r"bid[–-]ask"),
    (3, "delta", r"\bdelta\b|\b\d+-delta\b"), (3, "theta", r"\btheta\b"), (3, "implied volatility", r"implied volatility|\bIV\b"),
    (4, "cash-secured put", r"cash-secured"), (4, "assignment", r"\bassign"), (5, "support", r"\bsupport\b"),
    (6, "covered call", r"covered calls?"), (7, "the wheel", r"\bthe wheel\b|\bwheel\b"), (8, "the 50% close", r"50% (?:rule|close)"),
    (9, "rolling", r"\broll(?:ing|ed|s)?\b"), (10, "credit spread", r"credit spreads?"), (11, "debit spread", r"debit spreads?|bull call spread"),
    (12, "iron condor", r"iron condors?|\bcondors?\b"), (13, "LEAPS", r"\bLEAPS\b"), (14, "poor man’s covered call", r"poor man"),
]

def check_extra():
    e = lambda a, b, tol=0.01: abs(a - b) <= tol or sys.exit(f"bad number: {a} vs {b}")
    e(27 - 1, 26); e((28 - 26) * 100 + 70, 270); e(270 / 2700, 0.10)                 # Henry's SoFi wheel
    e(0.40 - 0.20, 0.20); e((1 - 0.20) * 100, 80); e(4.63 - 2.69, 1.94); e((5 - 1.94) * 100, 306)   # spreads
    e(500 - 164, 336); e(164 / 336, 0.488, 0.001); e(323 / 2, 161.5)                # condor, 50% close
    e(500 / 17000, 0.0294, 0.0001); e(170 - 5, 165)                                  # NVIDIA put
    e(PUT_MULT, 4.03, 0.01); e(CAP_8K, 400000); e(96000 - 80000, 16000)
    for lid, x in EXTRA.items():
        assert 150 < len(x["teach"]) < 1100, (lid, len(x["teach"]))

check_extra()
for x in L:
    x.update(EXTRA[x["id"]])

assert len(L) == 18
rungs = ["Learn", "Sell", "Manage", "Spread", "Long", "Plan"]
for l in L:
    assert l["rung"] in rungs
    for a in l["after"]: assert rungs.index(next(x for x in L if x["id"] == a)["rung"]) == rungs.index(l["rung"]) - 1, (l["id"], a)
    for k, t in lesson_texts(l) + [("concept", l["concept"])] + [("rtask", l.get("rtask", ""))] + \
            [("rkey", q) for b in l.get("rkey", []) for q in [b.get("t", "")] + b.get("l", [])] + \
            [("rneed", it["k"] + " " + it.get("n", "")) for it in l.get("rneed", [])]:
        assert not re.search(r"\b(he|him|his|himself)\b", t, re.I), (l["id"], k, "pronoun", t)
        assert "<" not in t and '"' not in t, (l["id"], k, t)
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
check_extras(L)
FLAGS = term_order(L, GLOSSARY, "H")
if FLAGS:
    sys.exit("A lesson uses a term before the lesson that teaches it, with no pointer:\n  " + "\n  ".join(FLAGS))
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
