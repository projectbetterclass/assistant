# Builds "Forex, from the rules up" (FX_CURRICULUM) in time-tracker.html: 12 sittings on the Forex branch of
# Trading. Your library has no forex channel, so these are written from the mechanics (pips, lots, margin) and the EU
# rules for retail traders (ESMA's 2018 measures, applied in the Netherlands by the AFM); the videos are Aswath's on
# currencies and Henry's on risk. Every figure in a lesson is recomputed in check().
#   python3 scripts/build-forex-course.py          -> rewrites the block in time-tracker.html
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from course_block import yt, course, check_videos, write, check_extras, term_order

CURR = yt("FXbXksS4kNs", "Aswath Damodaran", "Session 12: Cracking the Currency Code!", "inflation and interest rates behind a currency")
CURR2 = yt("sx_q72vqIGQ", "Aswath Damodaran", "Data 2017 Update 3: Cracking the Currency Code", "why rates differ between currencies")
TURKEY = yt("IGlMmK06brM", "Aswath Damodaran", "Deja Vu in Turkey: Currency Crisis and Corporate Insanity!", "what a currency crisis looks like from inside")
RISK = yt("X9ibF2v1RKA", "Invest with Henry", "Options vs. Stocks: Which is Safer? (Risk Management Explained)", "sizing so one loss can't sink you")
ADVICE = yt("hiEv_Ra3thg", "Invest with Henry", "12 Years Of Brutal Options Trading Advice In One Course", "the habits that keep a trader in the game")

L = [
 dict(id="X01", rung="Rules", stage_name="Trading money", concept="Money you can lose, kept apart from your FIRE money",
  task="Decide your trading money: a single euro amount, in a separate account, that you could lose without changing anything else in your life. Write why that amount, and what would have to happen before you ever add to it. Judge: what share of your yearly FIRE investing is it, and does that feel right?",
  co="a €2,000 account", rev="a €500 account", watch=[RISK], read=["ESMA product intervention measures for CFDs (2018), applied in the Netherlands by the AFM"]),
 dict(id="X02", rung="Rules", stage_name="Risk per trade", concept="1% a trade, a monthly loss limit, and the maths of losing",
  task="Write your two rules for a €2,000 account: the euros you may lose on one trade at 1%, and your monthly loss limit in euros. Then work out what ten losses in a row would leave at 1% and at 5% a trade. Judge: which rule are you most likely to break, and what will stop you?",
  co="a €2,000 account", rev="a €10,000 account", watch=[RISK]),
 dict(id="X03", rung="Basics", stage_name="Pips, lots, spreads", concept="What a pip is worth, and what the spread costs",
  task="On a demo platform, find EUR/USD and USD/JPY. For each, write the price, the spread in pips, and what one pip is worth on a micro lot, in euros. Judge: a strategy that aims for 10 pips per trade, with a 1-pip spread: what share of each win does the spread take?",
  co="EUR/USD", rev="USD/JPY", after=["X01"]),
 dict(id="X04", rung="Basics", stage_name="Leverage and margin", concept="How a small account controls a big position, and what that does to a loss",
  task="For a €2,000 account: the margin for one mini lot of EUR/USD at 30:1, and what a 100-pip move against it costs you in euros and as a share of the account. Then the same if you used all the leverage the rules allow. Judge: what leverage will you actually use, and why is the cap not a target?",
  co="EUR/USD", rev="gold at 20:1", after=["X02"], read=["ESMA (2018): leverage caps 30:1 / 20:1 / 10:1 / 5:1 / 2:1, margin close-out at 50%, negative balance protection"]),
 dict(id="X05", rung="Drivers", stage_name="What moves currencies", concept="Interest rates, inflation, and fear",
  task="Find the next ECB and Fed rate decisions and what markets expect from each. Write one sentence on what would make EUR/USD rise, and one on what would make it fall. Judge: if the ECB does exactly what everyone expects, what do you expect the price to do, and why?",
  co="EUR/USD", rev="USD/JPY", after=["X03"], watch=[CURR, TURKEY]),
 dict(id="X06", rung="Drivers", stage_name="Time and cost", concept="Sessions, news and the overnight swap",
  task="On your demo platform, write the EUR/USD spread at 15:00 and at 23:00 on the same day, and the overnight swap for a long and a short mini lot. Judge: for a trade you plan to hold three days, which costs more, the spread or the swap?",
  co="EUR/USD", rev="AUD/JPY", after=["X04"], watch=[CURR2]),
 dict(id="X07", rung="Plan", stage_name="Position size", concept="Size every trade from its stop",
  task="Three trades on a €2,000 account at 1%: EUR/USD with a 25-pip stop, EUR/USD with a 60-pip stop, and GBP/USD with a 40-pip stop. Work out the size of each in micro lots, and the loss if each stop is hit. Judge: why does the wider stop not mean more risk?",
  co="EUR/USD", rev="GBP/USD", after=["X05"]),
 dict(id="X08", rung="Plan", stage_name="Expectancy", concept="Win rate, reward-to-risk, and what costs do to them",
  task="Work out the expectancy, in R and after a 1-pip spread on a 25-pip stop, for three methods: 40% at 2R, 60% at 1R, and 75% at 0.3R. Judge: which would you trade, and which looks good but loses?",
  co="three methods", rev="your own plan", after=["X06"]),
 dict(id="X09", rung="Practice", stage_name="The journal", concept="Why in, why out, what you learned",
  task="Set up your journal now, as a sheet or a notebook, with the columns above, and fill in one example trade on EUR/USD from today’s chart, on paper. Judge: which column will you be most tempted to skip, and why is that the one that matters?",
  co="EUR/USD", rev="GBP/USD", after=["X07", "X08"], watch=[ADVICE]),
 dict(id="X10", rung="Practice", stage_name="Demo, done honestly", concept="Fifty trades on a demo, sized like real money",
  task="Open a demo with your real trading money as the balance. Write your rules on one card: the pairs, the setup, when you trade, the 1% size rule and your monthly limit. Then place your first demo trade and journal it. Judge: what would make you stop before fifty trades, and is that a good reason?",
  co="a €2,000 demo", rev="a €500 demo", after=["X07"]),
 dict(id="X11", rung="Judge", stage_name="Reading your 50 trades", concept="Win rate, average R, expectancy, and drawdown",
  task="Take your journal (or, until it has fifty trades, a made-up one: 20 wins at 1.8R and 30 losses at 1R, with 6 trades off-plan). Work out the win rate, expectancy and the share of trades on-plan. Judge: is this a method, or not yet? What would you need to see in the next fifty?",
  co="your fifty trades", rev="a friend’s fifty trades", after=["X10"]),
 dict(id="X12", rung="Judge", stage_name="Go, or not yet", concept="When real money is earned, and the claims to ignore",
  task="Write your go/no-go test: the numbers your fifty trades must show before any real money, and your first real size. Then check your broker in the AFM register. Judge: if your results say ‘not yet’, what will you do: more practice, a different method, or stop?",
  co="your plan", rev="a friend’s plan", after=["X09", "X10"], read=["AFM: register of licensed firms and its warnings about unlicensed brokers"]),
]

# ---- each lesson's idea, walk-through, numbers box, worked answer, thread and revisit -------------------------------
# Prices: Yahoo Finance daily closes on 11 November 2026 (EURUSD=X, JPY=X, GBPUSD=X, EURJPY=X, EURGBP=X, AUDJPY=X, GC=F),
# and the history of JPY=X, AUDJPY=X and TRY=X. Every number below is computed from these, and re-checked in check().
ASOF = "11 Nov 2026"
EURUSD, USDJPY, GBPUSD, EURJPY, EURGBP, AUDJPY, GOLD = 1.1169, 158.71, 1.3349, 177.25, 0.8366, 109.02, 4000.50
USDJPY_HI, USDJPY_LO, AUDJPY_HI, AUDJPY_LO = (161.62, "3 Jul 2024"), (144.73, "6 Aug 2024"), (109.11, "10 Jul 2024"), (94.26, "6 Aug 2024")
USDTRY_2018, USDTRY_NOW = 3.79, 50.21
YF = lambda sym: "https://finance.yahoo.com/quote/%s/history/" % sym.replace("=", "%3D")
def yf(sym, what=""): return {"s": "Yahoo Finance · " + (what or sym) + ", close " + ASOF, "u": YF(sym)}
def eur(x, d=2): return ("−" if x < 0 else "") + "€" + format(abs(x), ",.%df" % d)
def pc(x, d=1): return ("%." + str(d) + "f%%") % x
ESMA_TXT = "ESMA product intervention measures for CFDs, 2018 (the EU’s retail rules; the AFM applies them in the Netherlands)"

PIP_MICRO = 0.10 / EURUSD                 # € per pip, one micro lot of EUR/USD (or any …/USD pair)
PIP_MICRO_JPY = 10 / EURJPY               # € per pip, one micro lot of USD/JPY: ¥10
PIP_MICRO_EURGBP = 0.10 / EURGBP          # € per pip, one micro lot of EUR/GBP: £0.10
ACC, RISK = 2000, 20
def size(stop, pip): return int(RISK / (stop * pip))
S25, S60, SG40, SJ30, SG35 = size(25, PIP_MICRO), size(60, PIP_MICRO), size(40, PIP_MICRO), size(30, PIP_MICRO_JPY), size(35, PIP_MICRO)
def E(p, w, c=0.0): return p * w - (1 - p) - c
def breakeven(w, c=0.0): return (1 + c) / (w + 1)

EXTRA = {}
EXTRA["X01"] = dict(
  teach="Trading is a different game from investing: short bets against professionals, and most retail traders lose. So trading money is its own pot, an amount you could lose completely without touching your rent, your emergency fund or your FIRE investing. Decide its size before you open a platform, not after a good week.",
  walk=[{"h": "Why it gets its own pot", "p": ["Investing for FIRE means owning the world economy for decades and letting time do the work. Trading means betting on moves of days or hours, against banks and funds with better data and lower costs. When the EU limited what brokers may offer retail traders in 2018, ESMA found that 74–89% of retail accounts trading CFDs, the way most people trade forex, lost money. Since then every EU broker must print its own share on its website."]},
        {"h": "How to set it", "l": [["One number, decided once.", "An amount you could lose in full and change nothing else in your life."], ["A separate account.", "So a loss can’t leak into your savings, and a win can’t tempt you to top it up from them."], ["A rule for adding to it.", "Only after your demo results pass the test you’ll write in X12, never after a single good week."]]},
        {"h": "Where it goes wrong", "l": ["Sizing the pot after a winning streak.", "Topping it up to win back a loss: that is exactly the money it was meant to protect.", "Counting it as part of your FIRE plan. It is the cost of learning a skill."]},
        {"h": "Worked: one way to size it", "p": ["Someone who invests €12,000 a year for FIRE might set trading money at €2,000: two months of investing, about 17% of a year. If it goes to zero, their FIRE date moves by about two months and nothing else changes. That is the test: what would losing all of it cost you, in time?"]},
        {"h": "Your turn: a €2,000 account", "p": ["Pick your own amount, write why, and what has to happen before you ever add to it. Then put it against your yearly FIRE investing."]}],
  need=[{"k": "Retail CFD accounts that lost money", "v": "74–89%", "n": "ESMA’s finding when it set the EU rules in 2018; every EU broker must now show its own share.", "s": ESMA_TXT},
        {"k": "This course’s example account", "v": "€2,000", "n": "Replace it with your own amount."}],
  key=[{"t": "A good answer looks like", "l": ["One amount, e.g. €2,000, in a separate account, with the reason: ‘I could lose all of it and only my FIRE date moves, by about two months.’",
        "A rule for adding to it: ‘only after fifty demo trades pass my X12 test, and never from my emergency fund or monthly investing.’",
        "The share of a year’s FIRE investing: €2,000 of €12,000 is 17%. If that feels heavy, the pot is too big."]}],
  thread={"n": "X02 · the two risk rules for this pot; the Options course sizes its trades from the same money"},
  rtask="Same question for a €500 account: what does it buy you, and what doesn’t it?",
  rkey=[{"t": "Short answer", "l": ["At 1% a trade you risk €5: on EUR/USD that is about 2 micro lots with a 25-pip stop (X07).", "Enough to learn the routine and the rules; too small to sit through big swings without the size rounding to zero."]}])

EXTRA["X02"] = dict(
  teach="Losses come in streaks, so the size of each loss decides whether you survive one. Risk at most 1% of the account on a trade and stop for the month after a set loss: two rules, written before the first trade, keep you in the game long enough to learn whether you have an edge.",
  walk=[{"h": "Why size beats strategy", "p": ["Even a method that works loses several times in a row now and then. At 1% a trade, ten losses in a row cost about 10%; at 5%, about 40%. And losses compound against you: after −40% you need +67% just to get back, after −50% you need +100%."]},
        {"h": "The two rules", "l": [["1% a trade.", "The most you may lose if the trade goes wrong: 1% of the account. X07 turns it into a position size."], ["A monthly limit.", "For example 6%: once you have lost that much in a month, you stop until the next one. It stops a bad week becoming a bad year."]]},
        {"h": "Where it goes wrong", "l": ["Raising the size after losses to ‘win it back’.", "Moving the limit when you hit it.", "Risking a round number of euros that is really 3–5% of a small account."]},
        {"h": "Worked: an €8,000 account at 2% a trade", "l": ["Risk a trade: €160. Ten losses in a row: €8,000 × 0.98¹⁰ = %s, down %s." % (eur(8000 * 0.98 ** 10), pc((1 - 0.98 ** 10) * 100)), "To get back: %s ÷ %s − 1 = +%s." % (eur(8000, 0), eur(8000 * 0.98 ** 10), pc((1 / 0.98 ** 10 - 1) * 100)), "At 1%% the same streak leaves %s, down %s." % (eur(8000 * 0.99 ** 10), pc((1 - 0.99 ** 10) * 100))]},
        {"h": "Your turn: a €2,000 account", "p": ["Write your two rules in euros, then work out what ten losses leave at 1% and at 5% a trade."]}],
  need=[{"k": "Account", "v": "€2,000", "n": "The course’s example trading money (X01)."}, {"k": "Risk a trade · monthly limit", "v": "1% · 6%", "n": "6% is an example; pick your own and write it down."}],
  key=[{"t": "Worked answer", "l": ["One trade at 1%: €20. A monthly limit of 6%: €120.", "Ten losses at 1%%: €2,000 × 0.99¹⁰ = %s, down %s." % (eur(ACC * 0.99 ** 10), pc((1 - 0.99 ** 10) * 100)),
        "Ten losses at 5%%: €2,000 × 0.95¹⁰ = %s, down %s, and you’d need +%s to get back." % (eur(ACC * 0.95 ** 10), pc((1 - 0.95 ** 10) * 100), pc((1 / 0.95 ** 10 - 1) * 100, 0)),
        "The rule most people break is the monthly limit, right after a loss. What stops you: writing it on the card next to the screen (X10), and closing the platform when it’s hit."]}],
  thread={"b": "X01 · a €2,000 pot, apart from your FIRE money", "n": "X07 · every trade’s size comes from the €20 you set here"},
  rtask="A €10,000 account: your two rules in euros, and what ten losses leave at 1% and at 5%.",
  rneed=[{"k": "Account", "v": "€10,000"}],
  rkey=[{"t": "Short answer", "l": ["1% is €100 a trade; a 6% monthly limit is €600.", "Ten losses: %s at 1%%, %s at 5%%." % (eur(10000 * 0.99 ** 10), eur(10000 * 0.95 ** 10))]}])

EXTRA["X03"] = dict(
  teach="A pair’s price is how much of the second currency one unit of the first costs. A pip is its fourth decimal, the second for yen pairs; size comes in standard, mini and micro lots; and the spread between buy and sell is what every trade costs before anything happens.",
  walk=[{"h": "Reading a quote", "p": ["EUR/USD at %.4f means €1 buys $%.4f. The first currency is the base, the second the quote. A pip is 0.0001, or 0.01 when the yen is the quote currency, because yen prices have two decimals." % (EURUSD, EURUSD)]},
        {"h": "What a pip is worth", "l": [["Lots.", "Standard 100,000 units of the base currency, mini 10,000, micro 1,000."], ["Pip value is in the quote currency.", "On any …/USD pair a pip on a micro lot is $0.10; on USD/JPY it is ¥10; on EUR/GBP it is £0.10. Convert that to euros at today’s rate."]]},
        {"h": "The spread", "p": ["The gap between the price you can buy at and the price you can sell at. You pay it on every round trip, and it widens at big news and late at night (X06)."]},
        {"h": "Where it goes wrong", "l": ["Forgetting that pip value depends on the quote currency, so a yen or pound pair is worth a different amount per pip.", "Ignoring the spread on small targets: on a 5-pip target a 1-pip spread is a fifth of the win."]},
        {"h": "Worked: EUR/GBP, %s" % ASOF, "p": ["EUR/GBP closed at %.4f. The quote currency is the pound, so a pip on a micro lot is £0.10, which is £0.10 ÷ %.4f = %s. A 1-pip spread on a mini lot costs £1, about %s, each round trip." % (EURGBP, EURGBP, eur(PIP_MICRO_EURGBP, 3), eur(10 * PIP_MICRO_EURGBP))], **yf("EURGBP=X", "EUR/GBP")},
        {"h": "Your turn: EUR/USD and USD/JPY", "p": ["Find both on your demo platform: the price, the spread in pips, and a pip on a micro lot in euros. Then the share of a 10-pip win a 1-pip spread takes."]}],
  need=[{"k": "EUR/USD", "v": "%.4f" % EURUSD, **yf("EURUSD=X", "EUR/USD")}, {"k": "USD/JPY", "v": "%.2f" % USDJPY, **yf("JPY=X", "USD/JPY")},
        {"k": "EUR/JPY (to turn yen into euros)", "v": "%.2f" % EURJPY, **yf("EURJPY=X", "EUR/JPY")}, {"k": "A pip · a micro lot", "v": "0.0001 (0.01 for yen) · 1,000 units"}],
  needNote="Your demo platform’s prices will differ from these closes; the method is the same.",
  key=[{"t": "Worked answer, at the %s closes" % ASOF, "l": ["EUR/USD: a pip on a micro lot is $0.10 = $0.10 ÷ %.4f = %s." % (EURUSD, eur(PIP_MICRO, 4)), "USD/JPY: a pip on a micro lot is ¥10 = ¥10 ÷ %.2f = %s." % (EURJPY, eur(PIP_MICRO_JPY, 4)),
        "Spreads: read them off your platform; they are what you pay every round trip.", "A 1-pip spread on a 10-pip target takes 1 ÷ 10 = 10% of every win, and adds to every loss."]}],
  thread={"b": "X02 · €20 at risk a trade, on €2,000", "n": "X04 · leverage and margin on the same lots; X07 · the pip value sizes every trade"},
  rtask="USD/JPY: what is a pip worth on a mini lot, in euros, and what does a 2-pip spread cost you each round trip?",
  rneed=[{"k": "EUR/JPY", "v": "%.2f" % EURJPY, **yf("EURJPY=X", "EUR/JPY")}],
  rkey=[{"t": "Short answer", "l": ["A mini lot of USD/JPY: ¥100 a pip = %s." % eur(10 * PIP_MICRO_JPY, 3), "A 2-pip spread: %s each round trip." % eur(20 * PIP_MICRO_JPY)]}])

M_EU, LOSS100 = 10000 / 30, 100 * 10 * PIP_MICRO
FULL_LOTS = int(ACC * 30 / 10000)
CLOSE_PIPS = (ACC - ACC / 2) / (FULL_LOTS * 10 * PIP_MICRO)
GOLD_EUR = 10 * GOLD / EURUSD
EXTRA["X04"] = dict(
  teach="Leverage lets a small account open a big position; margin is the deposit the broker holds for it. It doesn’t change how far the price moves, only what the move does to your whole account, so the EU’s 30:1 cap on major pairs is a ceiling, never a target.",
  walk=[{"h": "How it works", "p": ["Open €10,000 of EUR/USD with €333 of your money and you are using 30:1. Every pip on that position now counts against your €2,000, not against the €333."]},
        {"h": "The EU’s rules for retail traders", "l": ["Leverage caps: 30:1 on major pairs (two of USD, EUR, JPY, GBP, CAD, CHF), 20:1 other pairs and gold, 10:1 other commodities, 5:1 single shares, 2:1 crypto.", "The broker closes your positions when your money falls to half the margin they need.", "You can’t lose more than your deposit."]},
        {"h": "Where it goes wrong", "l": ["Treating the cap as the size to trade.", "Watching margin instead of the loss: the loss is set by your position size and the stop (X07), not by the margin."]},
        {"h": "Worked: a mini lot of GBP/USD", "p": ["A mini lot is £10,000, which at %.4f EUR/GBP is %s. At 30:1 the margin is %s. A 100-pip move costs $100 (the quote currency is the dollar) = %s. Same pip value as EUR/USD, more margin, because the base currency is the pound." % (EURGBP, eur(10000 / EURGBP, 0), eur(10000 / EURGBP / 30, 0), eur(LOSS100))]},
        {"h": "Your turn: EUR/USD on €2,000", "p": ["The margin for one mini lot, the cost of a 100-pip move, then the same with every bit of leverage the rules allow."]}],
  need=[{"k": "Account · leverage cap, major pairs", "v": "€2,000 · 30:1", "s": ESMA_TXT}, {"k": "EUR/USD", "v": "%.4f" % EURUSD, **yf("EURUSD=X", "EUR/USD")}, {"k": "A pip on a mini lot", "v": "$1 = %s" % eur(10 * PIP_MICRO, 4), "n": "From X03."}],
  key=[{"t": "Worked answer", "l": ["One mini lot is €10,000 of EUR/USD; at 30:1 the margin is %s." % eur(M_EU), "A 100-pip move against it: $100 = %s, %s of the account." % (eur(LOSS100), pc(LOSS100 / ACC * 100)),
        "All the leverage: €2,000 × 30 = €60,000, six mini lots. The same 100 pips: %s, %s of the account." % (eur(FULL_LOTS * LOSS100), pc(FULL_LOTS * LOSS100 / ACC * 100)),
        "And the broker would close you out after %.0f pips against you, when your €2,000 had fallen to €1,000: a move of %s." % (CLOSE_PIPS, pc(CLOSE_PIPS * 0.0001 / EURUSD * 100, 2)),
        "The leverage you use is whatever your 1% rule and stop give (X07), usually far below 30:1."]}],
  thread={"b": "X03 · a pip on a micro lot of EUR/USD is %s" % eur(PIP_MICRO, 4), "n": "X06 · what holding it overnight costs; X07 · sizing from the stop"},
  rtask="Gold at 20:1: ten ounces at $%s. The margin, and what a 1%% move against it costs, on a €2,000 account." % format(GOLD, ",.2f"),
  rneed=[{"k": "Gold, futures", "v": "$%s an ounce" % format(GOLD, ",.2f"), **yf("GC=F", "gold futures")}, {"k": "EUR/USD", "v": "%.4f" % EURUSD}],
  rkey=[{"t": "Short answer", "l": ["Ten ounces: $%s = %s; at 20:1 the margin is %s, almost the whole account." % (format(10 * GOLD, ",.0f"), eur(GOLD_EUR, 0), eur(GOLD_EUR / 20, 0)), "A 1%% move: $%s = %s, %s of the account." % (format(0.1 * GOLD, ",.0f"), eur(0.1 * GOLD / EURUSD, 0), pc(0.1 * GOLD / EURUSD / ACC * 100))]}])

EXTRA["X05"] = dict(
  teach="Over months, currencies follow interest rates and inflation, and in a scare money runs to the dollar, the yen and the franc. What moves a price is the surprise against what was expected, which is why a decision everyone saw coming can leave the price flat.",
  walk=[{"h": "The three forces", "l": [["Interest rates.", "Money flows to where it earns more. When markets come to expect the ECB to raise rates faster than the Fed, the euro tends to rise against the dollar."], ["Inflation, over years.", "A currency that loses value at home loses it abroad too."], ["Fear.", "In a scare, money runs to the dollar, the yen and the Swiss franc."]]},
        {"h": "Expected versus surprise", "p": ["Markets price the decision before it happens. The move comes from what was not expected: a different decision, or a change in what the central bank says about the next ones. The calendar matters most: central bank decisions, inflation reports and the US jobs report move prices in seconds."]},
        {"h": "Where it goes wrong", "l": ["Trading the headline (‘rates up, so the currency goes up’) instead of the surprise.", "Holding through a decision without knowing it’s scheduled."]},
        {"h": "Worked: the Turkish lira", "p": ["With inflation far above everyone else’s for years, the lira went from %.2f per dollar at the start of 2018 to %.2f on %s: it lost %s of its value against the dollar. Aswath’s Turkey video is the inside view of 2018." % (USDTRY_2018, USDTRY_NOW, ASOF, pc((1 - USDTRY_2018 / USDTRY_NOW) * 100, 0))], **yf("TRY=X", "USD/TRY")},
        {"h": "Your turn: EUR/USD", "p": ["Find the next ECB and Fed decisions and what markets expect from each; then write what would make EUR/USD rise, and what would make it fall."]}],
  need=[{"k": "Where to look", "v": "ECB · Fed calendars", "n": "The ECB’s monetary policy calendar (ecb.europa.eu) and the Fed’s FOMC calendar (federalreserve.gov). For what markets expect: CME’s FedWatch for the Fed, and the news around each meeting."},
        {"k": "EUR/USD", "v": "%.4f" % EURUSD, **yf("EURUSD=X", "EUR/USD")}],
  key=[{"t": "A good answer looks like", "l": ["Both dates, and what markets price for each: e.g. ‘ECB: hold expected; Fed: a cut half priced’.",
        "Rise: the ECB more hawkish than expected, or the Fed more dovish. Fall: the reverse, or a scare that sends money to the dollar.",
        "If the ECB does exactly what’s expected, the decision itself barely moves the price; what moves it is anything new in the statement or the press conference about future meetings."]}],
  thread={"b": "X03 · how a pair is quoted", "n": "X06 · around the news, spreads widen; X12 · the claims to ignore"},
  rtask="USD/JPY: what would make it rise, what would make it fall, and why is the yen a ‘scare’ currency?",
  rkey=[{"t": "Short answer", "l": ["Rise: US rates expected higher, or Japanese rates lower, than priced. Fall: the reverse, or a scare.", "Japan’s rates have been far below others for years, so the yen is borrowed to buy higher-yielding assets; in a scare those bets unwind and the yen is bought back (X06)."]}])

EXTRA["X06"] = dict(
  teach="Forex trades all week, but costs change with the hour: spreads are tightest when London and New York overlap and widest at the daily rollover and around big news. Hold past the rollover and you pay or earn the swap, the interest gap between the two currencies minus the broker’s cut.",
  walk=[{"h": "When it’s cheapest", "p": ["Roughly 14:00–17:30 Dutch time, when London and New York are both open. Widest around 23:00, when the trading day rolls over, and in the seconds around big news, such as the US jobs report, usually on the first Friday of the month at 14:30 Dutch time."]},
        {"h": "The swap", "l": [["What it is.", "Holding a position overnight means borrowing one currency to hold the other. You earn the interest on the one you hold and pay it on the one you borrowed, minus the broker’s cut."], ["A rough size.", "If dollar rates were 2 points above euro rates, a long EUR/USD mini lot (€10,000) would pay about 2% × €10,000 ÷ 365 ≈ €0.55 a night before the broker’s cut. Most brokers charge three nights on a Wednesday, for the weekend."], ["The carry trade.", "Borrowing the low-rate currency to hold the high-rate one. It earns a little every night and can lose months of it in days when fear hits."]]},
        {"h": "Where it goes wrong", "l": ["Placing trades at 23:00 because the chart looks quiet.", "Forgetting the triple swap on a trade held over a Wednesday.", "Mistaking a carry trade’s steady nightly income for safety."]},
        {"h": "Worked: the yen carry unwind, 2024", "p": ["Borrowing yen near zero to hold higher-yielding currencies was a crowded trade. When Japan raised rates and fear hit, it unwound: USD/JPY fell from %.2f (%s) to %.2f (%s), %s in five weeks, and AUD/JPY from %.2f to %.2f, %s. Months of nightly swap, gone in days." % (USDJPY_HI[0], USDJPY_HI[1], USDJPY_LO[0], USDJPY_LO[1], pc((1 - USDJPY_LO[0] / USDJPY_HI[0]) * 100), AUDJPY_HI[0], AUDJPY_LO[0], pc((1 - AUDJPY_LO[0] / AUDJPY_HI[0]) * 100))], **{"s": "Yahoo Finance · USD/JPY and AUD/JPY daily closes, 2024", "u": YF("JPY=X")}},
        {"h": "Your turn: EUR/USD", "p": ["On your demo platform: the spread at 15:00 and at 23:00 the same day, and the swap for a long and a short mini lot. Then compare spread and swap for a three-day hold."]}],
  need=[{"k": "Cheapest hours (Dutch time)", "v": "about 14:00–17:30", "n": "London and New York both open."}, {"k": "Widest", "v": "around 23:00", "n": "The daily rollover; also the seconds around big news."}],
  needNote="Spreads and swaps are your broker’s own: read them off your demo platform.",
  key=[{"t": "A good answer looks like", "l": ["Two spreads, e.g. ‘0.8 pips at 15:00, 3 pips at 23:00’: the late one several times wider.", "Two swaps with opposite signs or sizes: one side pays, the other earns less or pays too, because the broker takes a cut on both.",
        "Three-day hold: the spread is paid once; the swap three nights, or five if one is a Wednesday. With a 1-pip spread on a mini lot (about %s) and a swap of about €0.55 a night, the swap costs more from the second night on." % eur(10 * PIP_MICRO)]}],
  thread={"b": "X04 · leverage; X05 · interest rates differ between currencies", "n": "X08 · costs come off every trade’s expectancy"},
  rtask="AUD/JPY: which side earns the swap, why, and what happened to it in August 2024?",
  rneed=[{"k": "AUD/JPY", "v": "%.2f" % AUDJPY, **yf("AUDJPY=X", "AUD/JPY")}],
  rkey=[{"t": "Short answer", "l": ["Long AUD/JPY earns the swap while Australian rates are above Japanese ones, as they have been for years.", "In the 2024 unwind it fell from %.2f to %.2f in under four weeks, %s." % (AUDJPY_HI[0], AUDJPY_LO[0], pc((1 - AUDJPY_LO[0] / AUDJPY_HI[0]) * 100))]}])

EXTRA["X07"] = dict(
  teach="You don’t choose a lot size first; you choose where the idea is proven wrong, and the size follows. Size = the money you risk ÷ (pips to the stop × value of a pip), rounded down, so a wider stop always means a smaller position, never a bigger risk to the account.",
  walk=[{"h": "The one calculation", "l": [["Where are you wrong?", "Put the stop where the idea fails, not where the loss feels small."], ["Count the pips to it.", "From the entry price to the stop."], ["Size it.", "Size in micro lots = euros at risk ÷ (pips to the stop × € per pip on a micro lot). Round down."]]},
        {"h": "Where it goes wrong", "l": ["Picking ‘one mini lot’ and then placing the stop to fit it.", "Rounding up.", "Forgetting the pip value differs for yen or pound pairs (X03)."]},
        {"h": "Worked: USD/JPY with a 30-pip stop", "p": ["€20 at risk. A pip on a micro lot of USD/JPY is ¥10 = %s. Size: €20 ÷ (30 × %s) = %.1f, so %d micro lots, and %s lost if the stop is hit." % (eur(PIP_MICRO_JPY, 4), eur(PIP_MICRO_JPY, 4), RISK / (30 * PIP_MICRO_JPY), SJ30, eur(SJ30 * 30 * PIP_MICRO_JPY))], **yf("EURJPY=X", "EUR/JPY")},
        {"h": "Your turn: three trades on €2,000", "p": ["EUR/USD with a 25-pip and a 60-pip stop, and GBP/USD with a 40-pip stop: the size of each, and the loss if the stop is hit."]}],
  need=[{"k": "At risk a trade", "v": "€20", "n": "1% of €2,000 (X02)."}, {"k": "A pip, micro lot of EUR/USD or GBP/USD", "v": "$0.10 = %s" % eur(PIP_MICRO, 4), "n": "Both quote in dollars, so the same; at EUR/USD %.4f." % EURUSD, **yf("EURUSD=X", "EUR/USD")}],
  key=[{"t": "Worked answer", "l": ["EUR/USD, 25 pips: €20 ÷ (25 × %s) = %.2f → %d micro lots; %s if stopped." % (eur(PIP_MICRO, 4), RISK / (25 * PIP_MICRO), S25, eur(S25 * 25 * PIP_MICRO)),
        "EUR/USD, 60 pips: €20 ÷ (60 × %s) = %.2f → %d micro lots; %s if stopped." % (eur(PIP_MICRO, 4), RISK / (60 * PIP_MICRO), S60, eur(S60 * 60 * PIP_MICRO)),
        "GBP/USD, 40 pips: €20 ÷ (40 × %s) = %.2f → %d micro lots; %s if stopped." % (eur(PIP_MICRO, 4), RISK / (40 * PIP_MICRO), SG40, eur(SG40 * 40 * PIP_MICRO)),
        "The wider stop gets fewer lots, so the loss stays at or under €20 every time."]}],
  thread={"b": "X02 · €20 at risk; X03 · a pip on a micro lot is %s" % eur(PIP_MICRO, 4), "n": "X08 · the €20 becomes 1R; X09 · the size goes in the journal"},
  rtask="GBP/USD with a 35-pip stop, on €2,000 at 1%: the size, and the loss if the stop is hit.",
  rneed=[{"k": "A pip, micro lot of GBP/USD", "v": eur(PIP_MICRO, 4)}],
  rkey=[{"t": "Short answer", "l": ["€20 ÷ (35 × %s) = %.2f → %d micro lots; %s if stopped." % (eur(PIP_MICRO, 4), RISK / (35 * PIP_MICRO), SG35, eur(SG35 * 35 * PIP_MICRO))]}])

C25 = 1 / 25
EXTRA["X08"] = dict(
  teach="Whether a method makes money depends on two numbers together: how often it wins and how big the wins are against the losses, in R, the amount risked. Expectancy = win rate × average win − loss rate × average loss, after costs, and a high win rate means nothing if the losses are bigger than the wins.",
  walk=[{"h": "R, and expectancy", "p": ["1R is what you risk on a trade, the €20 from X07. A win of 2R is €40; a loss is −1R. Expectancy is the average R a trade, across many trades."]},
        {"h": "Costs come off every trade", "p": ["The spread is paid on wins and losses alike. As a share of R it is the spread ÷ the stop: 1 pip on a 25-pip stop is 0.04R. Small stops make costs big."]},
        {"h": "The break-even win rate", "p": ["Win rate needed = (1 + cost) ÷ (average win + 1). At 2R and no costs, one win in three; the smaller the wins, the more often you must be right."]},
        {"h": "Where it goes wrong", "l": ["Judging a method by its win rate alone.", "Leaving costs out.", "Tight stops: they make costs a large share of R."]},
        {"h": "Worked: two methods with a 1-pip spread", "l": ["50%% at 1.5R with a 15-pip stop: the cost is 1/15 = %.3fR; 0.5 × 1.5 − 0.5 − %.3f = %+.3fR a trade." % (1 / 15, 1 / 15, E(0.5, 1.5, 1 / 15)), "55%% at 1R with a 10-pip stop: the cost is 0.1R; 0.55 − 0.45 − 0.1 = %+.2fR. Right more often than not, and the spread eats all of it." % E(0.55, 1, 0.1)]},
        {"h": "Your turn: three methods", "p": ["40% at 2R, 60% at 1R and 75% at 0.3R, each after a 1-pip spread on a 25-pip stop."]}],
  need=[{"k": "Methods", "v": "40% at 2R · 60% at 1R · 75% at 0.3R"}, {"k": "Cost", "v": "1 pip on a 25-pip stop = 0.04R"}],
  key=[{"t": "Worked answer", "l": ["40%% at 2R: 0.4 × 2 − 0.6 − 0.04 = %+.2fR; break-even win rate %s." % (E(0.4, 2, C25), pc(breakeven(2, C25) * 100)),
        "60%% at 1R: 0.6 − 0.4 − 0.04 = %+.2fR; break-even %s." % (E(0.6, 1, C25), pc(breakeven(1, C25) * 100)),
        "75%% at 0.3R: 0.75 × 0.3 − 0.25 − 0.04 = %+.3fR; break-even %s, so it loses even though it wins three times in four." % (E(0.75, 0.3, C25), pc(breakeven(0.3, C25) * 100)),
        "The first two earn the same; the 2R one has longer losing streaks, the 1R one is steadier. The third looks good and loses."]}],
  thread={"b": "X07 · 1R = the €20 you risk a trade", "n": "X11 · you’ll read your own fifty trades the same way"},
  rtask="Your own plan: write your expected win rate, average win in R and cost in R, and its expectancy. What win rate would make it break even?",
  rkey=[{"t": "Check it", "l": ["Expectancy = win rate × average win − loss rate × 1R − cost; break-even win rate = (1 + cost) ÷ (average win + 1).", "If your expected win rate is within a few points of break-even, you don’t have a method yet."]}])

EXTRA["X09"] = dict(
  teach="A journal turns trades into data: why in, the entry, stop, target and size before you trade; the result in R, whether you kept your rules, and one lesson after. The rules column matters as much as the result, because a loss taken to plan is a good trade and a win that broke the rules is a bad one.",
  walk=[{"h": "The columns", "l": [["Before.", "Date and time, pair, the setup and why, entry, stop, target, size (X07), risk in R."], ["After.", "Exit, result in R, rules kept: yes or no, one sentence learned, a screenshot at entry."]]},
        {"h": "Why the rules column", "p": ["Over fifty trades it separates the method from luck. If the profits came from trades that broke your rules, you have found luck, not a method (X11)."]},
        {"h": "Where it goes wrong", "l": ["Filling it in after the trade, when you already know the result.", "Skipping losing trades.", "Writing ‘felt right’ as the reason."]},
        {"h": "Worked: one row, GBP/USD on paper", "p": ["Setup: pullback to yesterday’s low, which held twice. Entry %.4f, stop %.4f (40 pips), target %.4f (2R). Size: %d micro lots (X07), 1R = %s. After: stopped out, −1R. Rules kept: yes. Learned: entered before the candle closed; wait for the close next time." % (GBPUSD, GBPUSD - 0.0040, GBPUSD + 0.0080, SG40, eur(SG40 * 40 * PIP_MICRO))]},
        {"h": "Your turn: EUR/USD", "p": ["Set up your journal and fill in one paper trade from today’s chart."]}],
  key=[{"t": "A good answer looks like", "l": ["Every column above, with the before part filled in before you enter.", "One EUR/USD row: e.g. entry %.4f, a 25-pip stop at %.4f, a 2R target at %.4f, %d micro lots, 1R = %s." % (EURUSD, EURUSD - 0.0025, EURUSD + 0.0050, S25, eur(S25 * 25 * PIP_MICRO)),
        "The column most people skip: ‘rules kept’. It’s the one that tells you, after fifty trades, whether you have a method."]}],
  thread={"b": "X07–X08 · size and R", "n": "X10 · fifty journaled demo trades"},
  rtask="GBP/USD: write one journal row from memory, with every column.",
  rkey=[{"t": "Check it", "l": ["Before: pair, setup and why, entry, stop, target, size, R. After: result in R, rules kept, one lesson, a screenshot."]}])

EXTRA["X10"] = dict(
  teach="A demo only teaches you if it feels real: your actual trading money as the balance, the size your 1% rule gives, only your written setups, at hours you could really trade, every trade journaled. Fifty such trades are a fair sample of how you follow your own rules, losing streaks included.",
  walk=[{"h": "Make it real", "l": ["Balance: your trading money, not the €100,000 most brokers start you with.", "Size: from your stop and 1% rule, every time.", "Setups and hours: only the ones on your card."]},
        {"h": "Why fifty", "p": ["Enough to see your losing streaks and whether you keep your rules through them; still small enough to finish in a few months. Demo fills are kinder than real ones, so a method that only just works here won’t work with real money."]},
        {"h": "Where it goes wrong", "l": ["A big demo balance, so losses don’t sting.", "Stopping after a bad week, or changing the method every ten trades."]},
        {"h": "Worked: a rules card", "l": ["Pairs: EUR/USD, GBP/USD. Setup: pullback to a level that held twice, entry on the candle close.", "Hours: 14:00–17:30 Dutch time, no trades 30 minutes either side of big news.", "Size: 1% from the stop. Monthly limit: 6%. Stop the demo early only if I break the rules three times in a week."]},
        {"h": "Your turn: a €2,000 demo", "p": ["Open it with your real trading money, write your card, place the first trade and journal it."]}],
  key=[{"t": "A good answer looks like", "l": ["A card with pairs, setup, hours, the 1% rule and the monthly limit, short enough to read before every trade.",
        "A good reason to stop before fifty: breaking your own rules again and again, which is a discipline problem to fix first. A bad reason: a losing streak, which the fifty are meant to include."]}],
  thread={"b": "X02, X07, X09 · the rules, the size, the journal", "n": "X11 · reading the fifty"},
  rtask="A €500 demo: what changes on your card, and what doesn’t?",
  rkey=[{"t": "Short answer", "l": ["1R becomes €5; with a 25-pip stop that is %d micro lots of EUR/USD. Everything else on the card stays the same." % int(5 / (25 * PIP_MICRO))]}])

X11_E = 0.4 * 1.8 - 0.6
EXTRA["X11"] = dict(
  teach="After fifty trades, count the win rate, the average win and loss in R, the expectancy, the drawdown and the share of trades on-plan. Fifty is still a small sample, so look for a positive expectancy after costs, rules kept nearly every time, and profits that came from the trades that followed your rules.",
  walk=[{"h": "What to count", "l": ["Win rate; average win and loss in R; expectancy (X08).", "Drawdown: the largest drop from a high point, in R.", "On-plan share: trades where every rule was kept."]},
        {"h": "How much fifty can tell you", "p": ["A method that truly wins 40% of the time will show anywhere from about 26% to 54% over fifty trades, just by chance: 40% ± 2 × √(0.4 × 0.6 ÷ 50)."]},
        {"h": "Where it goes wrong", "l": ["Calling a lucky streak a method.", "Not splitting results into on-plan and off-plan trades."]},
        {"h": "Worked: 22 wins at 1.5R, 28 losses at 1R, 3 off-plan", "p": ["Win rate 44%%; expectancy 0.44 × 1.5 − 0.56 = %+.2fR a trade, %+.0fR in all. On-plan: 47 of 50, 94%%. If its worst run was seven losses in a row, that’s −7R, €140 at €20 a trade: a drawdown to sit through without changing the rules." % (0.44 * 1.5 - 0.56, 50 * (0.44 * 1.5 - 0.56))]},
        {"h": "Your turn: your fifty trades", "p": ["Or until you have them, the made-up journal: 20 wins at 1.8R, 30 losses at 1R, 6 off-plan."]}],
  need=[{"k": "Made-up journal", "v": "20 wins at 1.8R · 30 losses at 1R", "n": "6 of the 50 trades broke the rules."}],
  key=[{"t": "Worked answer", "l": ["Win rate 20/50 = 40%%. Expectancy 0.4 × 1.8 − 0.6 × 1 = %+.2fR a trade, %+.0fR in all (%s at €20 a trade)." % (X11_E, 50 * X11_E, eur(50 * X11_E * RISK, 0)),
        "On-plan 44 of 50 = 88%.", "It hangs on the six off-plan trades: if they were all wins (+10.8R), the 44 on-plan trades lost 4.8R; if all losses, the on-plan trades made +12R.",
        "And 40% over fifty could be anything from 26% to 54%. Not yet a method: in the next fifty, look for a positive expectancy on the on-plan trades alone, and nearly no off-plan ones."]}],
  thread={"b": "X08 · expectancy; X10 · your fifty demo trades", "n": "X12 · go, or not yet"},
  rtask="A friend’s fifty: 35 wins at 0.5R, 15 losses at 1.2R, 12 off-plan. A method, or not?",
  rneed=[{"k": "Their journal", "v": "35 wins at 0.5R · 15 losses at 1.2R", "n": "12 off-plan."}],
  rkey=[{"t": "Short answer", "l": ["Win rate 70%%; expectancy 0.7 × 0.5 − 0.3 × 1.2 = %+.2fR a trade, before costs. On-plan 76%%." % (0.7 * 0.5 - 0.3 * 1.2), "Not a method: a high win rate hiding losses bigger than the wins, and a quarter of the trades off-plan."]}])

EXTRA["X12"] = dict(
  teach="Real money is earned by evidence, not a good week: a positive expectancy after costs over at least fifty journaled trades, nearly all on-plan, and a losing streak sat through calmly. Then start smaller than the demo, with a licensed broker, and ignore anything that sells easy returns.",
  walk=[{"h": "The test", "l": ["A number for each: trades (at least 50), expectancy after costs, the on-plan share, and the worst drawdown you’ll accept.", "Decide it before you look at the results."]},
        {"h": "If it passes", "l": ["Start smaller than the demo, e.g. 0.5% a trade, with the same rules.", "A broker in the AFM’s register; check the AFM’s warnings about unlicensed firms."]},
        {"h": "What to ignore", "p": ["Signal groups, ‘guaranteed’ monthly returns, copy-trading leaderboards and anyone who shows wins but never their account history."]},
        {"h": "Tax, in the Netherlands", "p": ["A private person’s trading money normally sits in box 3 with your other assets; trading so much that it works like a job can move it to box 1. Check with the Belastingdienst or an adviser."]},
        {"h": "Worked: one go/no-go test", "l": ["Go if, over at least 50 trades: expectancy ≥ +0.10R after costs, on-plan ≥ 90%, worst drawdown ≤ 10R with the rules kept.", "Then: real money at 0.5% a trade (€10 on €2,000) for the next fifty."]},
        {"h": "Your turn: your plan", "p": ["Write your own test and your first real size, and check your broker in the AFM register."]}],
  need=[{"k": "Licensed brokers", "v": "AFM register", "n": "afm.nl: the public register of licensed firms, and its warnings about unlicensed ones."}],
  key=[{"t": "A good answer looks like", "l": ["Four numbers written before the results: trades, expectancy after costs, on-plan share, worst drawdown.", "A first real size below the demo’s, and the same card of rules.",
        "If the answer is ‘not yet’: more practice only if the rules were kept and the sample is small; a different method if the on-plan trades lose; stop if trading keeps pulling money or time from your FIRE plan, which doesn’t need it."]}],
  thread={"b": "X11 · what your fifty trades show", "n": "real money, smaller than the demo, or not yet"},
  rtask="A friend’s plan: they want to go live after 30 trades at +0.3R with 20% off-plan. Your advice?",
  rkey=[{"t": "Short answer", "l": ["Not yet: 30 trades is too few, and with a fifth off-plan the +0.3R may come from the broken rules. Fifty more, nearly all on-plan, then the test."]}])

GLOSSARY = [
    (3, "pip", r"\bpips?\b"), (3, "lot sizes", r"\b(?:micro|mini|standard) lots?\b"), (3, "spread", r"\bspreads?\b"),
    (4, "leverage", r"\bleverage\b"), (4, "margin", r"\bmargin\b"),
    (6, "swap", r"\bswaps?\b|\brollover\b"), (6, "carry trade", r"carry trade"),
    (7, "the stop", r"\b\d+-pip stops?\b|\bstop-loss\b|\bthe stop\b|\byour stop\b|\bits stop\b"),
    (8, "expectancy", r"\bexpectancy\b"), (8, "R", r"\b\d+(?:\.\d+)?R\b|\bin R\b|\b1R\b"),
    (9, "journal", r"\bjournal"), (11, "drawdown", r"\bdrawdown"),
]

def check_extra():
    e = lambda a, b, tol=0.01: abs(a - b) <= tol or sys.exit(f"bad number: {a} vs {b}")
    e(USDJPY * EURUSD, EURJPY, 0.05); e(PIP_MICRO, 0.0895, 0.0001); e(PIP_MICRO_JPY, 0.0564, 0.0001)
    e(S25, 8, 0); e(S60, 3, 0); e(SG40, 5, 0); e(SJ30, 11, 0); e(SG35, 6, 0)
    e(E(0.4, 2, C25), 0.16); e(E(0.6, 1, C25), 0.16); e(E(0.75, 0.3, C25), -0.065, 0.0005); e(breakeven(0.3, C25), 0.80, 0.001)
    e(X11_E, 0.12); e(20 * 1.8 - 30, 6); e(14 * 1.8 - 30, -4.8); e(20 * 1.8 - 24, 12)
    e(FULL_LOTS, 6, 0); e(CLOSE_PIPS, 186.2, 0.1); e(M_EU, 333.33)
    for lid, x in EXTRA.items():
        assert 250 < len(x["teach"]) < 1100, (lid, len(x["teach"]))

for x in L:
    x.update(EXTRA[x["id"]])

def check():
    e = lambda a, b, tol=0.01: abs(a - b) <= tol or sys.exit(f"bad number: {a} vs {b}")
    e(0.99 ** 10, 0.904, 0.001); e(1 - 0.95 ** 10, 0.401, 0.001); e(1 / 0.6 - 1, 0.667, 0.001); e(1 / 0.5 - 1, 1.0)
    e(10000 / 30, 333.3, 0.1); e(60000 * 0.01, 600); e(600 / 2000, 0.30)
    e(0.4 * 2 - 0.6 * 1, 0.2); e(1 / (1 + 2), 0.333, 0.001); e(1 / 25, 0.04); e(0.2 - 0.04, 0.16)
    sd = math.sqrt(0.4 * 0.6 / 50); e(0.4 - 2 * sd, 0.26, 0.005); e(0.4 + 2 * sd, 0.54, 0.005)
check()
check_extra()

C = course({"goal_id": "goal_fx", "key": "fx", "title": "Forex, from the rules up", "azTitle": "Forex, from the rules up, A → Z",
     "rungs": ["Rules", "Basics", "Drivers", "Plan", "Practice", "Judge"],
     "rungDesc": ["your trading money, and the two rules that keep you in the game", "pips, lots, spreads, leverage and margin",
                  "what moves a currency, and when trading costs most", "size every trade from its stop, and know your expectancy",
                  "the journal, and fifty honest demo trades", "read your results, and decide: real money, or not yet"],
     "blurb": "One question on a real pair per sitting, demo only. Your library has no forex channel, so these come from the mechanics and the EU rules for retail traders; the first two lessons set the trading money and risk rules your Options course uses too.",
     "allDone": "now take your fifty demo trades through the go/no-go test. 📊",
     "revWord": "another pair",
     "refNote": "The idea opens in step 2 of the sitting — guess first. Demo only until your fifty trades pass your own test; the rules quoted are the EU’s for retail traders (ESMA, applied by the AFM)."}, L)
check_videos(C)
check_extras(C["lessons"])
FLAGS = term_order(C["lessons"], GLOSSARY, "X")
if FLAGS:
    sys.exit("A lesson uses a term before the lesson that teaches it, with no pointer:\n  " + "\n  ".join(FLAGS))
write("FX_CURRICULUM", ["Forex, from the rules up — 12 sittings on the Forex branch of Trading, demo only: trading money and risk rules first (the",
      "Options course leans on them), then pips, leverage under the EU's 2018 retail caps, what moves currencies, sizing from the stop,",
      "expectancy, the journal and a go/no-go test. Built by scripts/build-forex-course.py, which checks every figure."], C)
