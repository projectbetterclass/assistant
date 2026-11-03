# Builds "Forex, from the rules up" (FX_CURRICULUM) in time-tracker.html: 12 sittings on the Forex branch of
# Trading. Your library has no forex channel, so these are written from the mechanics (pips, lots, margin) and the EU
# rules for retail traders (ESMA's 2018 measures, applied in the Netherlands by the AFM); the videos are Aswath's on
# currencies and Henry's on risk. Every figure in a lesson is recomputed in check().
#   python3 scripts/build-forex-course.py          -> rewrites the block in time-tracker.html
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from course_block import yt, course, check_videos, write

CURR = yt("FXbXksS4kNs", "Aswath Damodaran", "Session 12: Cracking the Currency Code!", "inflation and interest rates behind a currency")
CURR2 = yt("sx_q72vqIGQ", "Aswath Damodaran", "Data 2017 Update 3: Cracking the Currency Code", "why rates differ between currencies")
TURKEY = yt("IGlMmK06brM", "Aswath Damodaran", "Deja Vu in Turkey: Currency Crisis and Corporate Insanity!", "what a currency crisis looks like from inside")
RISK = yt("X9ibF2v1RKA", "Invest with Henry", "Options vs. Stocks: Which is Safer? (Risk Management Explained)", "sizing so one loss can't sink you")
ADVICE = yt("hiEv_Ra3thg", "Invest with Henry", "12 Years Of Brutal Options Trading Advice In One Course", "the habits that keep a trader in the game")

L = [
 dict(id="X01", rung="Rules", stage_name="Trading money", concept="Money you can lose, kept apart from your FIRE money",
  teach="Trading and investing are different games. Investing for FIRE means owning the world economy for decades; trading means betting on short moves against professionals, and most people lose. When the EU limited leverage for retail traders in 2018, ESMA found that 74–89% of retail accounts trading CFDs, which is how most people trade forex, lost money, and every EU broker must now show its own share. So trading money is a separate pot: an amount you could lose completely without it touching your rent, your emergency fund or your monthly FIRE investing. Treat it as the cost of learning a skill, and decide its size before you open a platform, not after a good week.",
  task="Decide your trading money: a single euro amount, in a separate account, that you could lose without changing anything else in your life. Write why that amount, and what would have to happen before you ever add to it. Judge: what share of your yearly FIRE investing is it, and does that feel right?",
  co="a €2,000 account", rev="a €500 account", watch=[RISK], read=["ESMA product intervention measures for CFDs (2018), applied in the Netherlands by the AFM"]),
 dict(id="X02", rung="Rules", stage_name="Risk per trade", concept="1% a trade, a monthly loss limit, and the maths of losing",
  teach="Losses come in streaks, so the size of each loss decides whether you survive one. Risk at most 1% of the account per trade: ten losses in a row then cost about 9.6% (0.99¹⁰ ≈ 0.904). At 5% a trade the same streak costs about 40%, and climbing back from −40% needs a gain of about 67%; from −50% you need +100%. Add a monthly limit, for example 6%: once you have lost that much in a month, you stop until the next one. Two rules, written down before the first trade, do more for a beginner than any strategy, because they keep you trading long enough to learn whether you have an edge.",
  task="Write your two rules for a €2,000 account: the euros you may lose on one trade at 1%, and your monthly loss limit in euros. Then work out what ten losses in a row would leave at 1% and at 5% a trade. Judge: which rule are you most likely to break, and what will stop you?",
  co="a €2,000 account", rev="a €10,000 account", watch=[RISK]),
 dict(id="X03", rung="Basics", stage_name="Pips, lots, spreads", concept="What a pip is worth, and what the spread costs",
  teach="A currency pair shows how many units of the second currency one unit of the first costs: EUR/USD at 1.0850 means €1 buys $1.0850. A pip is the fourth decimal (0.0001), or the second for yen pairs (0.01). Size comes in lots: a standard lot is 100,000 units of the first currency, a mini lot 10,000, a micro lot 1,000. On EUR/USD a pip is worth $10 a standard lot, $1 a mini and $0.10 a micro, about €0.09 at 1.0850. The spread, the gap between the buy and the sell price, is what you pay on every trade before anything happens: a 1-pip spread on a mini lot costs $1 each time you get in and out, and spreads widen at news and late at night.",
  task="On a demo platform, find EUR/USD and USD/JPY. For each, write the price, the spread in pips, and what one pip is worth on a micro lot, in euros. Judge: a strategy that aims for 10 pips per trade, with a 1-pip spread: what share of each win does the spread take?",
  co="EUR/USD", rev="USD/JPY", after=["X01"]),
 dict(id="X04", rung="Basics", stage_name="Leverage and margin", concept="How a small account controls a big position, and what that does to a loss",
  teach="Leverage lets you open a position much bigger than your money; margin is the deposit the broker holds for it. EU rules cap leverage for retail traders at 30:1 for major pairs (two of USD, EUR, JPY, GBP, CAD and CHF), 20:1 for other pairs and gold, 10:1 for other commodities, 5:1 for single shares and 2:1 for crypto. At 30:1, a mini lot of EUR/USD (€10,000) needs about €333 of margin. Leverage doesn’t change how far the price moves; it changes what the move does to you: with all of a €2,000 account used at 30:1 (€60,000 of positions), a 1% move against you costs €600, 30% of the account. The broker closes your positions when your money falls to half the required margin, and you can’t lose more than your deposit.",
  task="For a €2,000 account: the margin for one mini lot of EUR/USD at 30:1, and what a 100-pip move against it costs you in euros and as a share of the account. Then the same if you used all the leverage the rules allow. Judge: what leverage will you actually use, and why is the cap not a target?",
  co="EUR/USD", rev="gold at 20:1", after=["X02"], read=["ESMA (2018): leverage caps 30:1 / 20:1 / 10:1 / 5:1 / 2:1, margin close-out at 50%, negative balance protection"]),
 dict(id="X05", rung="Drivers", stage_name="What moves currencies", concept="Interest rates, inflation, and fear",
  teach="Over months, currencies follow interest rates and inflation. Money flows towards the currency where it earns more, so when markets come to expect the ECB to raise rates faster than the Fed, the euro tends to rise against the dollar. What moves the price is the change against what was expected, not the rate itself, which is why a hike everyone saw coming can leave the price flat. Over years, high inflation weakens a currency: Turkey’s lira lost most of its value as inflation ran far above everyone else’s. And in a scare, money runs to the dollar, the yen and the Swiss franc. The calendar matters most: central bank decisions, inflation reports and the US jobs report move prices in seconds.",
  task="Find the next ECB and Fed rate decisions and what markets expect from each. Write one sentence on what would make EUR/USD rise, and one on what would make it fall. Judge: if the ECB does exactly what everyone expects, what do you expect the price to do, and why?",
  co="EUR/USD", rev="USD/JPY", after=["X03"], watch=[CURR, TURKEY]),
 dict(id="X06", rung="Drivers", stage_name="Time and cost", concept="Sessions, news and the overnight swap",
  teach="Forex trades around the clock on weekdays, but not evenly. Spreads are tightest when London and New York are both open, roughly 14:00–17:30 Dutch time, and widest around 23:00, when the day rolls over, and in the seconds around big news, such as the US jobs report, usually on the first Friday of the month at 14:30. Hold a position past the rollover and you pay or receive the swap: the interest difference between the two currencies, minus the broker’s cut. Borrowing the low-rate currency to hold the high-rate one, the carry trade, pays a little every night and can lose months of it in a day when fear hits, as in the yen carry unwind of August 2024.",
  task="On your demo platform, write the EUR/USD spread at 15:00 and at 23:00 on the same day, and the overnight swap for a long and a short mini lot. Judge: for a trade you plan to hold three days, which costs more, the spread or the swap?",
  co="EUR/USD", rev="AUD/JPY", after=["X04"], watch=[CURR2]),
 dict(id="X07", rung="Plan", stage_name="Position size", concept="Size every trade from its stop",
  teach="You don’t choose a lot size first; you choose where you are wrong, and the size follows. Put the stop where the idea is proven wrong, count the pips to it, then size = the money you risk ÷ (pips to the stop × value of a pip). €2,000 at 1% is €20 to risk. With a 25-pip stop on EUR/USD and about €0.092 a pip per micro lot, €20 ÷ (25 × €0.092) ≈ 8.7, so you trade 8 micro lots (0.08 lots) and lose about €18 if the stop is hit. A wider stop means a smaller position, never a bigger risk. This is the one calculation to do before every trade.",
  task="Three trades on a €2,000 account at 1%: EUR/USD with a 25-pip stop, EUR/USD with a 60-pip stop, and GBP/USD with a 40-pip stop. Work out the size of each in micro lots, and the loss if each stop is hit. Judge: why does the wider stop not mean more risk?",
  co="EUR/USD", rev="GBP/USD", after=["X05"]),
 dict(id="X08", rung="Plan", stage_name="Expectancy", concept="Win rate, reward-to-risk, and what costs do to them",
  teach="Whether a method makes money depends on two numbers together: how often it wins, and how big the wins are against the losses, measured in R, the amount risked. Expectancy = win rate × average win − loss rate × average loss. Win 40% of the time at 2R, lose 60% at 1R: 0.4 × 2 − 0.6 × 1 = +0.2R a trade. At 2R a win, you break even winning one trade in three. Costs come off every trade: a 1-pip spread on a 25-pip stop is 0.04R, which takes the example to +0.16R. A high win rate means nothing if the losses are bigger than the wins.",
  task="Work out the expectancy, in R and after a 1-pip spread on a 25-pip stop, for three methods: 40% at 2R, 60% at 1R, and 75% at 0.3R. Judge: which would you trade, and which looks good but loses?",
  co="three methods", rev="your own plan", after=["X06"]),
 dict(id="X09", rung="Practice", stage_name="The journal", concept="Why in, why out, what you learned",
  teach="A journal turns trades into data. For every trade write, before you enter: the setup and why, the entry, the stop and the target, the size from the stop, and your risk in R. After you exit: the result in R, whether you followed your rules, and one sentence on what you learned. Add a screenshot of the chart at entry. The rule-following column matters as much as the result: a winning trade that broke your rules is a bad trade, and a loss taken exactly to plan is a good one. Fifty such entries tell you more about yourself than any course.",
  task="Set up your journal now, as a sheet or a notebook, with the columns above, and fill in one example trade on EUR/USD from today’s chart, on paper. Judge: which column will you be most tempted to skip, and why is that the one that matters?",
  co="EUR/USD", rev="GBP/USD", after=["X07", "X08"], watch=[ADVICE]),
 dict(id="X10", rung="Practice", stage_name="Demo, done honestly", concept="Fifty trades on a demo, sized like real money",
  teach="A demo account is only useful if it feels like the real thing. Set the demo balance to your actual trading money, not the €100,000 most brokers start you with, and use the size your 1% rule gives. Trade only your written setups, at the times you could really trade, and journal every one. The goal of fifty trades is not profit but a fair sample of how you trade your own rules, including the losing streaks. Demo fills are kinder than real ones, so if a method only just works on the demo, it won’t work with real money.",
  task="Open a demo with your real trading money as the balance. Write your rules on one card: the pairs, the setup, when you trade, the 1% size rule and your monthly limit. Then place your first demo trade and journal it. Judge: what would make you stop before fifty trades, and is that a good reason?",
  co="a €2,000 demo", rev="a €500 demo", after=["X07"]),
 dict(id="X11", rung="Judge", stage_name="Reading your 50 trades", concept="Win rate, average R, expectancy, and drawdown",
  teach="After fifty trades, count: the win rate, the average win and loss in R, the expectancy, the largest drop from a high point (the drawdown), and the share of trades that followed your rules. Fifty trades is still a small sample: a method that truly wins 40% of the time will show anywhere from about 26% to 54% over fifty trades, just by chance. So look for a positive expectancy after costs, rules followed on nearly every trade, and a drawdown you sat through without breaking them. If the results came from the trades that broke your rules, they are luck, not a method.",
  task="Take your journal (or, until it has fifty trades, a made-up one: 20 wins at 1.8R and 30 losses at 1R, with 6 trades off-plan). Work out the win rate, expectancy and the share of trades on-plan. Judge: is this a method, or not yet? What would you need to see in the next fifty?",
  co="your fifty trades", rev="a friend’s fifty trades", after=["X10"]),
 dict(id="X12", rung="Judge", stage_name="Go, or not yet", concept="When real money is earned, and the claims to ignore",
  teach="Real money is earned by evidence, not by a good week: a positive expectancy after costs over at least fifty journaled trades, nearly all of them on-plan, and a losing streak you sat through calmly. Then start smaller than the demo and keep the same rules. Ignore what sells trading: signal groups, ‘guaranteed’ monthly returns, copy-trading leaderboards and anyone who shows wins but never their account history; the AFM warns about unlicensed brokers regularly. In the Netherlands, a private person’s trading money normally sits in box 3 with your other assets; trading so much that it works like a job can move it to box 1. If it turns out trading isn’t your game, your FIRE plan doesn’t need it.",
  task="Write your go/no-go test: the numbers your fifty trades must show before any real money, and your first real size. Then check your broker in the AFM register. Judge: if your results say ‘not yet’, what will you do: more practice, a different method, or stop?",
  co="your plan", rev="a friend’s plan", after=["X09", "X10"], read=["AFM: register of licensed firms and its warnings about unlicensed brokers"]),
]

def check():
    e = lambda a, b, tol=0.01: abs(a - b) <= tol or sys.exit(f"bad number: {a} vs {b}")
    e(0.99 ** 10, 0.904, 0.001); e(1 - 0.95 ** 10, 0.401, 0.001); e(1 / 0.6 - 1, 0.667, 0.001); e(1 / 0.5 - 1, 1.0)
    pip_micro_eur = 1000 * 0.0001 / 1.0850
    e(pip_micro_eur, 0.092, 0.0005); e(10000 / 30, 333.3, 0.1); e(60000 * 0.01, 600); e(600 / 2000, 0.30)
    size = 20 / (25 * pip_micro_eur); e(size, 8.68, 0.01); e(8 * 25 * pip_micro_eur, 18.4, 0.05)
    e(0.4 * 2 - 0.6 * 1, 0.2); e(1 / (1 + 2), 0.333, 0.001); e(1 / 25, 0.04); e(0.2 - 0.04, 0.16)
    sd = math.sqrt(0.4 * 0.6 / 50); e(0.4 - 2 * sd, 0.26, 0.005); e(0.4 + 2 * sd, 0.54, 0.005)
check()

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
write("FX_CURRICULUM", ["Forex, from the rules up — 12 sittings on the Forex branch of Trading, demo only: trading money and risk rules first (the",
      "Options course leans on them), then pips, leverage under the EU's 2018 retail caps, what moves currencies, sizing from the stop,",
      "expectancy, the journal and a go/no-go test. Built by scripts/build-forex-course.py, which checks every figure."], C)
