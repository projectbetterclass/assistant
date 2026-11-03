# Builds "Your FIRE plan" (FIRE_CURRICULUM) in time-tracker.html: 12 sittings on the user's own numbers (the €5,000 a month
# the FIRE page holds, the costs logged under it) with the Dutch rules of 2026. Every figure in a lesson is recomputed in
# check(), so a typo fails the build.
#   python3 scripts/build-fire-course.py            -> rewrites the block in time-tracker.html
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from course_block import yt, course, check_videos, write

NM_FIRE = yt("klVGlU4-VmQ", "New Money", "Is FIRE actually achievable? Can you retire early? (Financial Independence Retire Early)", "the nest-egg maths, and why retiring at 30 is rare")
ASW_INFL = yt("4UKaQpe1Yfs", "Aswath Damodaran", "Session 10: Inflation, the Hidden Tax", "what inflation is, and how it eats returns")
ASW_INFL2 = yt("lMEyjqXBU4U", "Aswath Damodaran", "Data Update 3 for 2022: The Inflation Effect on Investing", "what higher inflation did to stocks and bonds")
HORM = yt("rnvOwA39dDg", "Alex Hormozi", "How To Retire Early (and be in the top 1%)", "judging every cost against what you earn")
BOGLE = yt("bafSHgye-30", "New Money", "Jack Bogle: Should you buy Index Funds at All-Time Highs?", "own the whole market, keep costs low, keep buying")
BUFF = yt("Qrpj2pSWd7I", "New Money", "Warren Buffett: Should you buy Index Funds at All-Time Highs?", "why Buffett tells most people to index")
DCA = yt("2wU6kb7yyMM", "Invest with Henry", "Dollar Cost Averaging (DETAILED EXPLANATION)", "buying the same amount every month, and why it works")

L = [
 dict(id="F01", rung="Learn", stage_name="The number", concept="Your FIRE number: a year of spending × 25",
  teach="Financial independence is the point where your investments can pay your living costs without your work. The FIRE number is the pot that does it: what you spend in a year ÷ the share you can safely take out each year. At 4% that is 25 × your yearly spending; at 3.5% it is about 28.6 ×. Your FIRE page assumes €5,000 a month: €60,000 a year × 25 = €1,500,000. The number moves with spending, not with income: every €100 a month you don’t need takes €30,000 off it at 4%. That is why spending is the lever you control most. Retiring at 30 usually takes a business that works; for most people the realistic prize is cutting years, often decades, off the usual retirement age.",
  task="Work out your number at €5,000 a month, at 4% and at 3.5%. Then do it for €3,500 a month. Judge: how many euros does each €100 a month of spending add to the number, and which of your monthly costs would you cut first?",
  co="€5,000 a month", rev="€3,000 a month", watch=[NM_FIRE]),
 dict(id="F02", rung="Learn", stage_name="Today’s money", concept="Inflation, and returns above it",
  teach="Prices rise, so a euro buys less every year. At 2% inflation, the ECB’s target, €5,000 a month today costs about €7,430 a month in 20 years and €11,040 in 40; at 3% it is €9,031 and €16,310. Two habits keep the plan honest. Keep every number in today’s money: your spending, your FIRE number and your progress are all in 2026 euros. And use real returns, what investments earn above inflation. A mostly-stock world portfolio has earned roughly 5% a year above inflation over the long run, which is what your FIRE page assumes: an average with bad decades in it, not a promise. Mixing a return before inflation (say 7%) with today’s spending is the classic mistake: it makes the target look closer than it is.",
  task="Your €5,000 a month: what does it cost in 20, 30 and 40 years at 2% and at 3%? Then: your page assumes 5% a year above inflation. If you used 7% with today’s €5,000, would the date look earlier or later than it really is, and why?",
  co="€5,000 a month", rev="€2,500 a month", watch=[ASW_INFL, ASW_INFL2]),
 dict(id="F03", rung="Risk", stage_name="The 4% rule", concept="Where 4% comes from, and why early retirees use 3.5%",
  teach="The 4% rule comes from William Bengen (1994) and the Trinity study (1998). Take 4% of your pot in the first year of retirement, then raise that euro amount with inflation every year. In US market history since 1926, a portfolio of 50–75% stocks lasted through every 30-year period at that rate. Early retirees often use 3–3.5% instead, for three reasons. Your retirement may last 50 years, not 30. The history is the US, one of the best markets of the century. And fees and taxes come out of the same pot. Going from 4% to 3.5% raises the number by a seventh: €1.5M becomes about €1.71M on your €5,000 a month. In the Netherlands, box 3 tax is one of those costs (lesson F05).",
  task="Your number at 4% and at 3.5%, and how many more years of saving the gap costs at €1,000 a month (your FIRE page shows the years for both). Judge: you stop at 40 and live to 90. Which rate do you pick, and what would make you change it?",
  co="a 50-year retirement", rev="a 30-year retirement", after=["F01", "F02"], watch=[NM_FIRE],
  read=["W. Bengen (1994), Determining Withdrawal Rates Using Historical Data", "Cooley, Hubbard & Walz (1998), the Trinity study"]),
 dict(id="F04", rung="Risk", stage_name="Sequence risk", concept="Why a crash right after you stop hurts most",
  teach="Once you are taking money out, the order of returns matters. Two people can earn the same average return and end up very differently. Start with €1,000,000 and take €40,000 a year. If the market falls 30% in the first year, you are left with €672,000, and next year’s €40,000 is already 6% of what’s left: the units you sold low are gone before the recovery. The same fall fifteen years in, after the pot has grown, does far less harm. The first five to ten years decide most of the outcome. The defences: a lower starting rate, one to two years of spending in cash so you don’t have to sell in a crash, spending you can cut in bad years, and some income from work in the early years.",
  task="The day you stop: €1,500,000, taking €60,000 a year. The market falls 30% in year one. What is left, and what share of it is next year’s €60,000? Then plan your defences: how big a cash buffer, and which spending you would cut, by how much. Judge: a buffer or flexible spending, which protects you more?",
  co="a crash in year one", rev="the same crash in year fifteen", after=["F01"]),
 dict(id="F05", rung="Tax", stage_name="Box 3", concept="How investments are taxed in the Netherlands (2026)",
  teach="In the Netherlands your savings and investments are taxed in box 3, not on what they really earn but on an assumed return. For 2026: investments are assumed to earn 6.00%, bank savings 1.28%, and the first €59,357 per person (€118,714 with a fiscal partner) is free. The tax is 36% of the assumed return on the rest. €100,000 in a world index fund, single: (€100,000 − €59,357) × 6% × 36% ≈ €878 a year, about 0.9% of the pot. At €1,500,000 it is about €31,100 a year, roughly 2.1% of the pot every year, on top of what you take out to live on. If your real return in a year was lower than the assumed one, you can ask to be taxed on the real return instead (the tegenbewijsregeling). A system that taxes actual returns is planned for 2028 but isn’t settled, so check the Belastingdienst every year.",
  task="Work out box 3 for 2026 on €50,000, €250,000 and €1,500,000 invested, single; then €1,500,000 with a fiscal partner. Judge: with about 2% a year going to box 3 on a large pot, is 4% still safe for you, or does your number have to grow, and by how much?",
  co="€100,000, single", rev="€400,000 with a fiscal partner", after=["F03"],
  read=["Belastingdienst, box 3 for 2026: 36% on an assumed 6.00% (investments) and 1.28% (savings), above €59,357 per person"]),
 dict(id="F06", rung="Tax", stage_name="The bridge", concept="AOW, pension, and the years in between",
  teach="Stopping early splits your retirement in two. From the day you stop until state pension age, everything comes from your own investments: that is the bridge. From state pension age the AOW and any employer pension pay part of your costs, so the pot has less to do. The AOW age is 67 years and 3 months for people reaching it in 2028–2031, and it rises with life expectancy, so expect it later for you. Employer pension and lijfrente money is taxed in box 1 when it is paid out and stays out of box 3 until then, but it is locked until pension age, so it can’t pay for the bridge. You can see what you have built up on mijnpensioenoverzicht.nl. A realistic plan has two parts: the bridge, and a smaller pot for the years after the AOW starts.",
  task="Suppose the AOW and a small pension will cover €1,500 of your €5,000 a month from 67. How big is the pot for after 67 at 3.5%? If you stop at 45, the bridge adds 22 years of that €1,500 a month: roughly how much extra is that? Then look up your own built-up pension on mijnpensioenoverzicht.nl. Judge: does the AOW change your number more than the withdrawal rate did?",
  co="stopping at 45", rev="stopping at 55", after=["F03", "F04"], read=["mijnpensioenoverzicht.nl: your AOW and pension built up so far"]),
 dict(id="F07", rung="Mine", stage_name="Real spending", concept="Build the number from what you really spend",
  teach="The €5,000 a month on your FIRE page is a guess until you know what you spend. Track everything for a month in What you spend, under the FIRE number: groceries, rent, insurance, transport, subscriptions, going out. Bulk buys and big bills distort a single month, so give each one a ‘how often’: your €210 for 50 kg of chicken, if it lasts about two months, is roughly €105 a month; €120 of petrol every two weeks is about €260 a month. Add the costs that come once a year or less, such as insurance, a phone, a holiday or a car, spread over the months. Build the number from those categories rather than picking a round figure. Every €100 a month you find you don’t need takes €30,000 off the number at 4%, about €34,300 at 3.5%.",
  task="Log every cost for 30 days in What you spend, each with how often it comes back, starting with the chicken and the petrol. Then compare your monthly total with the €5,000 your number assumes. Judge: which category, cut by €200 a month, would hurt least, and how much would that take off your number?",
  co="your own month", rev="a €2,000 month", after=["F05"], watch=[HORM]),
 dict(id="F08", rung="Mine", stage_name="Savings rate", concept="The share you invest sets the years",
  teach="How fast you get there depends mostly on one number: the share of your take-home pay you invest. It works twice: money you invest grows, and money you don’t spend lowers the number you need. Starting from zero, earning 5% above inflation and using the 4% rule: invest 10% of your pay and it takes about 51 years; 25%, about 32; 50%, about 17; 75%, about 7. Income works the same way: a raise you don’t spend goes straight into the rate. Alex Hormozi describes living on about $30,000 a year until the income passed a million, judging every cost against what came in. You don’t need to go that far, but each step up in the rate takes years off.",
  task="Your take-home pay this month and what you invested: what is your savings rate, and roughly how many years does it give? Then compare two moves: €500 a month more income, or €500 a month less spending. Judge: why does the spending cut count twice?",
  co="your pay now", rev="your first full-time salary", after=["F06"], watch=[HORM, NM_FIRE]),
 dict(id="F09", rung="Invest", stage_name="What to buy", concept="One broad, cheap world index fund",
  teach="For most people the core of a FIRE portfolio is one broad, cheap index fund that owns thousands of companies across the world, so you don’t depend on picking winners. In the EU you buy UCITS ETFs, usually based in Ireland; most US-listed funds such as SPY aren’t sold to EU retail investors because they lack the required key information document. Cost is the part you control: a fund charging 0.07% a year instead of 0.50% leaves you about 14% more money after thirty years, and broker fees come on top. Accumulating or distributing (dividends reinvested or paid out) matters little for box 3, which taxes the assumed return either way. Bogle and Buffett give the same advice: own the whole market, keep costs low, keep buying.",
  task="Pick two world index ETFs you could buy here, for example one tracking the FTSE All-World and one the MSCI World, and look up their yearly cost (TER). Over 30 years, how much does the difference cost on your plan? Judge: besides cost, what would make you choose one over the other?",
  co="two world funds", rev="a world fund against a single-country fund", after=["F07", "F08"], watch=[BOGLE, BUFF]),
 dict(id="F10", rung="Invest", stage_name="Every month", concept="An emergency fund first, then automatic monthly buying",
  teach="Order matters. First an emergency fund, three to six months of costs in a savings account, so a broken car or a lost job never forces you to sell investments. Then invest a fixed amount every month, the day after your pay arrives, automatically. Buying every month means you buy more units when prices are low and fewer when they are high, and it takes the guessing out. The hard part is behaviour: in a 30% crash your plan says keep buying, which is exactly when buying pays most. Write down now, while you are calm, what you will do then.",
  task="Set your monthly amount, the day, the fund and the broker, on paper. Then: the market drops 30% three months after you start. Write the three sentences you will read to yourself before you touch anything. Judge: if €20,000 landed tomorrow, would you invest it at once or spread it over months, and why?",
  co="€1,000 a month", rev="€300 a month", after=["F08"], watch=[DCA]),
 dict(id="F11", rung="Keep", stage_name="The yearly review", concept="Four updates, once a year",
  teach="Once a year, on a date you pick, update four things: what you have invested, what you really spent (from your cost log), inflation (raise your monthly number by last year’s inflation, so the plan stays in today’s money), and the rules (box 3 changes nearly every year, and a new system is planned for 2028). Then rebalance if you hold more than one fund, back to the mix you chose. Watch for lifestyle creep: when your pay rises, decide in advance how much of the raise goes into the savings rate. Your FIRE page then shows the new years to go. One honest review a year beats checking the market every day.",
  task="Write your yearly review as a checklist with a date in your calendar: the four updates, your rebalance rule, and one question about lifestyle creep. Then do it now with today’s numbers. Judge: which update is most likely to move your date, and which are you most likely to skip?",
  co="this year", rev="next year", after=["F09", "F10"]),
 dict(id="F12", rung="Keep", stage_name="Milestones", concept="Coast FI, Barista FI, and walk-away money",
  teach="Full FIRE is the last milestone, not the only one. Coast FI: you have invested enough that, with nothing more added, growth alone reaches your number by normal pension age; from then on your pay only has to cover today’s costs. Barista FI: your investments cover part of your costs and part-time or enjoyable work pays the rest, which also softens sequence risk. And walk-away money: enough to leave a bad job and live for a year. Each comes much sooner than the full number, and each changes what risks you can take with your career and your business ideas.",
  task="Work out your Coast FI number: what you’d need invested today for 5% a year above inflation to reach €1.5M by 67 with nothing added. Then your Barista FI number: the pot that covers €5,000 minus €2,000 earned part-time, at 3.5%. Judge: which milestone would change your choices most if you reached it in five years?",
  co="your plan", rev="a plan at €3,500 a month", after=["F10"]),
]

def check():
    e = lambda a, b, tol=0.6: abs(a - b) <= tol or sys.exit(f"bad number: {a} vs {b}")
    e(5000 * 12 * 25, 1_500_000); e(1200 * 25, 30_000); e(5000 * 12 / 0.035, 1_714_285.7)
    e(5000 * 1.02 ** 20, 7_429.7); e(5000 * 1.02 ** 40, 11_040.2); e(5000 * 1.03 ** 20, 9_030.6); e(5000 * 1.03 ** 40, 16_310.2)
    e((1_000_000 - 40_000) * 0.7, 672_000); e(40_000 / 672_000 * 100, 5.95, 0.01)
    e((100_000 - 59_357) * 0.06 * 0.36, 877.9, 0.1); e((1_500_000 - 59_357) * 0.06 * 0.36, 31_117.9, 0.1); e(31_117.9 / 1_500_000 * 100, 2.07, 0.01)
    e(210 / 2, 105); e(120 * 26 / 12, 260); e(1200 / 0.035, 34_285.7)
    n = lambda s: math.log(1 + 1.25 * (1 - s) / s) / math.log(1.05)
    e(n(0.10), 51.4, 0.1); e(n(0.25), 31.9, 0.1); e(n(0.50), 16.6, 0.1); e(n(0.75), 7.1, 0.1)
    e(((1 - 0.0007) / (1 - 0.005)) ** 30, 1.138, 0.001)
check()


C = course({"goal_id": "goal_fire", "key": "fire", "title": "Your FIRE plan", "azTitle": "Your FIRE plan, A → Z",
     "rungs": ["Learn", "Risk", "Tax", "Mine", "Invest", "Keep"],
     "rungDesc": ["the number, and why it lives in today’s money", "the 4% rule, 3.5% for early stops, and sequence risk",
                  "box 3 in 2026, the AOW and the bridge years", "your own spending, and the savings rate that sets the years",
                  "what to buy here, and investing every month on autopilot", "the yearly review, and the milestones on the way"],
     "blurb": "One real question on your own numbers per sitting: €5,000 a month at 4% is what your FIRE page holds now. The Dutch tax figures are 2026’s; they change most years, so check them before you act.",
     "allDone": "now set up the monthly transfer and put the review in your calendar. 🔥",
     "revWord": "another case",
     "refNote": "The idea opens in step 2 of the sitting — guess first. Tax figures are 2026’s and change most years; the videos are for when you want more."}, L)
check_videos(C)
write("FIRE_CURRICULUM", ["Your FIRE plan — 12 sittings on your own numbers (the €5,000 a month your FIRE page holds, the costs you log), with the",
      "Dutch rules of 2026: box 3 at 36% on an assumed 6.00% above €59,357 (Belastingdienst; a new system is planned for 2028",
      "but not settled), AOW at 67 years and 3 months for 2028–2031. Built by scripts/build-fire-course.py, which checks every figure."], C)
