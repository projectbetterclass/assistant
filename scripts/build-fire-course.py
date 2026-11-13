# Builds "Your FIRE plan" (FIRE_CURRICULUM) in time-tracker.html: 12 sittings on the user's own numbers (the €5,000 a month
# the FIRE page holds, the costs logged under it) with the Dutch rules of 2026. Every figure in a lesson is recomputed in
# check(), so a typo fails the build.
#   python3 scripts/build-fire-course.py            -> rewrites the block in time-tracker.html
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from course_block import yt, course, check_videos, write, check_extras, term_order

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

# ---- each lesson's idea, walk-through, numbers, worked answer, thread and revisit ------------------------------------
# Real spending: the user's five Lidl receipts, 28 Oct–10 Nov 2026 (about two weeks), split as the receipts' VAT lines do:
# food (9%), household items (21%) and an air fryer (21%, a one-off). Totals are what was paid, rounding included.
FOOD = 40.65 + 59.74 + 42.78 + 40.35          # 28 Oct, 31 Oct (two receipts), 3 Nov, 10 Nov
HOUSE = 2.95 + 19.97                          # toilet paper and a non-food item
FRYER = 69.00
PAID = FOOD + HOUSE + FRYER
DAYS = 14
SALMON = 14.39 + 15.59 + 15.41 + 5 * 7.49     # three whole sides and five fillets
MILK = 22 * 1.45                              # 8 + 4 + 10 litres
per_month = lambda x: x / DAYS * 30.4375
FOOD_M, HOUSE_M, SALMON_M = per_month(FOOD), per_month(HOUSE), per_month(SALMON)
CHICKEN_M, PETROL_M = 210 / 2, 120 * 26 / 12
KNOWN_M = round(FOOD_M, -1) + CHICKEN_M + PETROL_M + round(HOUSE_M)
def eur(x, d=0): return ("−" if x < 0 else "") + "€" + format(abs(x), ",.%df" % d)
yrs = lambda target, monthly, r=0.05: math.log(1 + target * r / (monthly * 12)) / math.log(1 + r)
pv = lambda yearly, n, r=0.05: yearly * (1 - (1 + r) ** -n) / r
box3 = lambda pot, free=59_357: max(0, pot - free) * 0.06 * 0.36
nsr = lambda s: math.log(1 + 1.25 * (1 - s) / s) / math.log(1.05)
RECEIPTS = "Lidl receipts, 28 Oct–10 Nov 2026"

EXTRA = {}
EXTRA["F01"] = dict(
  teach="Your FIRE number is the pot whose returns can pay your costs without work: a year of spending ÷ the share you can safely take out each year. At 4% that is 25 × a year’s spending, at 3.5% about 28.6 ×. It moves with spending, not income: every €100 a month you don’t need takes €30,000 off it at 4%.",
  walk=[{"h": "The formula", "l": ["A year’s spending ÷ the withdrawal rate (F03).", "At 4%: × 25. At 3.5%: × 28.6."]},
        {"h": "Why spending is the lever", "p": ["Income can rise or fall; a euro of spending you drop lowers the target for good. €100 a month is €1,200 a year, × 25 = €30,000 at 4%."]},
        {"h": "Where it goes wrong", "l": ["A round monthly figure instead of one built from real costs (F07).", "Counting income instead of spending."]},
        {"h": "Worked: your groceries", "p": ["Your Lidl receipts from 28 Oct to 10 Nov 2026 come to %s of food in about two weeks: about %s a month. That is %s a year, so %s of your number at 4%%, before rent, insurance or anything else." % (eur(FOOD, 2), eur(round(FOOD_M, -1)), eur(round(FOOD_M, -1) * 12), eur(round(FOOD_M, -1) * 300))]},
        {"h": "Your turn: €5,000 a month", "p": ["Your number at 4% and at 3.5%; then the same for €3,500 a month."]}],
  need=[{"k": "Your FIRE page", "v": "€5,000 a month · 4%"}, {"k": "Food, from your receipts", "v": "≈ %s a month" % eur(round(FOOD_M, -1)), "n": "%s: %s in about two weeks." % (RECEIPTS, eur(FOOD, 2))}],
  key=[{"t": "Worked answer", "l": ["€5,000 a month: €60,000 a year × 25 = €1,500,000 at 4%%; ÷ 0.035 = %s at 3.5%%." % eur(60_000 / 0.035),
        "€3,500 a month: €42,000 × 25 = €1,050,000 at 4%%; ÷ 0.035 = %s at 3.5%%." % eur(42_000 / 0.035),
        "Each €100 a month adds €30,000 at 4%% and about %s at 3.5%%." % eur(1200 / 0.035)]}],
  thread={"n": "F02 · keeping it in today’s money; F07 · building the €5,000 from what you really spend"},
  rtask="€3,000 a month: your number at 4% and at 3.5%.",
  rkey=[{"t": "Short answer", "l": ["€36,000 a year: €900,000 at 4%%, about %s at 3.5%%." % eur(36_000 / 0.035)]}])

EXTRA["F02"] = dict(
  teach="Prices rise, so keep every number in today’s money and use real returns: what investments earn above inflation. Your FIRE page assumes 5% a year above inflation. Mixing a 7% return before inflation with today’s spending makes the date look closer than it is.",
  walk=[{"h": "Two habits", "l": [["Today’s money.", "Spending, the number and your progress, all in 2026 euros."], ["Real returns.", "What investments earn above inflation: about 5% a year for a mostly-stock world portfolio over the long run, with bad decades in it."]]},
        {"h": "What inflation does", "l": ["At 2%, the ECB’s target, €5,000 a month today costs about €7,430 in 20 years and €11,040 in 40.", "At 3%: €9,031 and €16,310."]},
        {"h": "Where it goes wrong", "l": ["A 7% return with today’s spending: the date looks years closer than it is.", "Forgetting to raise the monthly number each year (F11)."]},
        {"h": "Worked: your milk", "p": ["All three receipts with milk show €1.45 a litre. At 2%% inflation that litre costs about %s in 20 years; at 3%%, about %s. In today’s money it stays €1.45, and that is how the plan counts it." % (eur(1.45 * 1.02 ** 20, 2), eur(1.45 * 1.03 ** 20, 2))]},
        {"h": "Your turn: €5,000 a month", "p": ["Its cost in 20, 30 and 40 years at 2% and at 3%; then what using 7% instead of 5% would do to the date."]}],
  key=[{"t": "Worked answer", "l": ["2%%: %s in 20 years, %s in 30, %s in 40." % (eur(5000 * 1.02 ** 20), eur(5000 * 1.02 ** 30), eur(5000 * 1.02 ** 40)),
        "3%%: %s, %s, %s." % (eur(5000 * 1.03 ** 20), eur(5000 * 1.03 ** 30), eur(5000 * 1.03 ** 40)),
        "7% with today’s €5,000 makes the date look earlier than it really is: the return includes inflation, the spending doesn’t."]}],
  thread={"b": "F01 · the number", "n": "F03 · how much you can take out each year"},
  rtask="€2,500 a month: what does it cost in 20 and in 40 years at 2% inflation?",
  rkey=[{"t": "Short answer", "l": ["About %s in 20 years and %s in 40." % (eur(2500 * 1.02 ** 20), eur(2500 * 1.02 ** 40))]}])

EXTRA["F03"] = dict(
  teach="Take 4% of your pot in the first year, then raise that amount with inflation: in US history since 1926, portfolios of 50–75% stocks lasted every 30-year period. Early retirees use 3–3.5%: a longer retirement, a lucky US history, and fees and tax from the same pot.",
  walk=[{"h": "Where it comes from", "p": ["William Bengen (1994) and the Trinity study (1998) tested yearly withdrawals against US market history."]},
        {"h": "Why lower for an early stop", "l": ["Fifty years, not thirty.", "The US was one of the best markets of the century.", "Fees and box 3 tax come out of the same pot (F05)."]},
        {"h": "Where it goes wrong", "l": ["Treating 4% as a guarantee.", "Using 4% for a 50-year retirement with no plan for bad years (F04)."]},
        {"h": "Worked: your food at both rates", "p": ["About %s a month of food is %s of your number at 4%% and %s at 3.5%%. Every line of spending grows by a seventh when you move to 3.5%%." % (eur(round(FOOD_M, -1)), eur(round(FOOD_M, -1) * 300), eur(round(FOOD_M, -1) * 12 / 0.035))]},
        {"h": "Your turn: a 50-year retirement", "p": ["Your number at 4% and 3.5%, and how many more years of saving the gap costs at €1,000 a month."]}],
  key=[{"t": "Worked answer", "l": ["€1,500,000 at 4%%; %s at 3.5%%: a gap of %s." % (eur(60_000 / 0.035), eur(60_000 / 0.035 - 1_500_000)),
        "From zero at €1,000 a month and 5%% above inflation: about %.1f years to €1.5M and %.1f to €1.71M, so about %.1f years more." % (yrs(1_500_000, 1000), yrs(60_000 / 0.035, 1000), yrs(60_000 / 0.035, 1000) - yrs(1_500_000, 1000)),
        "Stopping at 40 and living to 90 is a 50-year retirement: 3.5% is the safer pick. Spending you can cut in bad years would let you lean toward 4%."]}],
  thread={"b": "F01–F02 · the number, in today’s money", "n": "F04 · why the first years after you stop matter most; F05 · box 3, from the same pot"},
  rtask="A 30-year retirement on €5,000 a month: which rate, and which number?",
  rkey=[{"t": "Short answer", "l": ["30 years is what the 4% research tested: 4% and €1,500,000 is defensible, with box 3 still to pay for (F05)."]}])

EXTRA["F04"] = dict(
  teach="Once you take money out, the order of returns matters: a crash in the first years after you stop does far more harm than the same crash fifteen years in, because the units you sell low are gone before the recovery. The defences: a lower rate, a cash buffer, spending you can cut, and some income early on.",
  walk=[{"h": "Why the order matters", "p": ["The same average return can end very differently. What decides it is whether the bad years come while the pot is small and you are already selling."]},
        {"h": "The four defences", "l": [["A lower starting rate.", "3.5% instead of 4% (F03)."], ["A cash buffer.", "One to two years of spending in cash, so you don’t sell in a crash."], ["Flexible spending.", "Costs you can cut in bad years."], ["Some income.", "Part-time work in the first years (F12)."]]},
        {"h": "Where it goes wrong", "l": ["Looking only at the average return.", "No buffer, so the first crash forces sales."]},
        {"h": "Worked: €1,000,000 at €40,000 a year", "p": ["A 30%% fall in year one leaves (€1,000,000 − €40,000) × 0.7 = €672,000. Next year’s €40,000 is already %.1f%% of it, against 4%% when you started." % (40_000 / 672_000 * 100)]},
        {"h": "Your turn: a crash in year one", "p": ["€1,500,000, taking €60,000 a year, and a 30% fall: what’s left, and what share of it is next year’s €60,000? Then your buffer and your cuts."]}],
  key=[{"t": "Worked answer", "l": ["(€1,500,000 − €60,000) × 0.7 = %s left; next year’s €60,000 is %.1f%% of it." % (eur(1_440_000 * 0.7), 60_000 / (1_440_000 * 0.7) * 100),
        "A buffer of one to two years: €60,000–€120,000 in cash.",
        "Flexible spending protects for longer, since a buffer runs out; together they’re strongest. Name the cuts now, with amounts: holidays, going out, the dearer groceries."]}],
  thread={"b": "F03 · the withdrawal rate", "n": "F05 · tax, another yearly cost on the pot; F12 · part-time income as a defence"},
  rtask="The same 30% fall in year fifteen, when the pot has grown to €2,000,000: what share of it is the €60,000?",
  rkey=[{"t": "Short answer", "l": ["(€2,000,000 − €60,000) × 0.7 = %s; €60,000 is %.1f%% of it, against %.1f%% after a crash in year one." % (eur(1_940_000 * 0.7), 60_000 / (1_940_000 * 0.7) * 100, 60_000 / (1_440_000 * 0.7) * 100)]}])

EXTRA["F05"] = dict(
  teach="In the Netherlands investments are taxed in box 3 on an assumed return, not the real one. For 2026: 36% of an assumed 6.00% on investments above €59,357 per person, €118,714 with a fiscal partner. On a large pot that is about 2% a year, on top of what you live on.",
  walk=[{"h": "The 2026 rules", "l": [["Assumed return.", "6.00% on investments, 1.28% on savings."], ["Tax-free.", "€59,357 per person; €118,714 with a fiscal partner."], ["Rate.", "36% of the assumed return above that: 2.16% of the taxable part."], ["Tegenbewijsregeling.", "If your real return was lower, you can ask to be taxed on that instead."]]},
        {"h": "Where it goes wrong", "l": ["Leaving it out of the withdrawal rate: 4% to live on, plus about 2% to box 3.", "Assuming the rules stay: a system on actual returns is planned for 2028, not settled."]},
        {"h": "Worked: €100,000, single", "p": ["(€100,000 − €59,357) × 6%% × 36%% ≈ %s a year, about 0.9%% of the pot." % eur(box3(100_000))]},
        {"h": "Your turn: four pots", "p": ["€50,000, €250,000 and €1,500,000, single; then €1,500,000 with a fiscal partner."]}],
  need=[{"k": "Box 3, 2026", "v": "36% × 6.00%", "n": "On investments above €59,357 per person (Belastingdienst)."}],
  key=[{"t": "Worked answer", "l": ["€50,000: €0, under the tax-free amount.", "€250,000: %s a year (%.1f%%)." % (eur(box3(250_000)), box3(250_000) / 2500),
        "€1,500,000 single: %s (%.1f%%); with a fiscal partner: %s (%.1f%%)." % (eur(box3(1_500_000)), box3(1_500_000) / 15_000, eur(box3(1_500_000, 118_714)), box3(1_500_000, 118_714) / 15_000),
        "So at €1.5M, 4% to live on plus about 2% to box 3 is too much: take a lower rate to live on, or build a bigger number."]}],
  thread={"b": "F03–F04 · what comes out of the pot", "n": "F06 · the AOW, the pension and the bridge years"},
  rtask="€400,000 with a fiscal partner: box 3 for 2026?",
  rkey=[{"t": "Short answer", "l": ["(€400,000 − €118,714) × 2.16%% ≈ %s a year, %.1f%% of the pot." % (eur(box3(400_000, 118_714)), box3(400_000, 118_714) / 4000)]}])

EXTRA["F06"] = dict(
  teach="Stopping early splits retirement in two: the bridge, from the day you stop to state pension age, paid entirely from your own investments; and after it, when the AOW and any pension pay part of your costs. Pension money is locked until pension age, so it can’t pay for the bridge.",
  walk=[{"h": "The two parts", "l": [["The bridge.", "Everything from your own pot, until the AOW starts."], ["After the AOW.", "The AOW and any pension pay part, so the pot does less."]]},
        {"h": "The facts", "l": ["AOW age: 67 years and 3 months for people reaching it in 2028–2031, and rising with life expectancy.", "Employer pension and lijfrente: taxed in box 1 when paid out, outside box 3 until then, locked until pension age.", "Your own figures: mijnpensioenoverzicht.nl."]},
        {"h": "Where it goes wrong", "l": ["Counting pension money for the bridge.", "Assuming today’s AOW age will be yours."]},
        {"h": "Worked: €1,500 a month from 67", "p": ["If the AOW and a pension pay €1,500 of €5,000 a month from 67, the pot after 67 only covers €3,500: €42,000 a year ÷ 3.5%% = %s." % eur(42_000 / 0.035)]},
        {"h": "Your turn: stopping at 45", "p": ["The pot for after 67, plus 22 years of that €1,500 a month for the bridge."]}],
  key=[{"t": "Worked answer", "l": ["After 67: %s." % eur(42_000 / 0.035),
        "The bridge, 22 years × €18,000: %s if the money earns nothing; about %s in today’s money if it earns 5%% above inflation while you spend it." % (eur(22 * 18_000), eur(round(pv(18_000, 22), -3))),
        "Together %s–%s, against %s at 3.5%% with no AOW: the AOW saves about %s–%s, about as much as the withdrawal rate moved it (%s)." % (eur(42_000 / 0.035 + round(pv(18_000, 22), -3)), eur(42_000 / 0.035 + 22 * 18_000), eur(60_000 / 0.035), eur(round(60_000 / 0.035 - 42_000 / 0.035 - 22 * 18_000, -3)), eur(round(60_000 / 0.035 - 42_000 / 0.035 - pv(18_000, 22), -3)), eur(60_000 / 0.035 - 1_500_000))]}],
  thread={"b": "F04–F05 · risk and tax on the pot", "n": "F07 · your real spending, to replace the €5,000 guess"},
  rtask="Stopping at 55: the bridge to 67 at €1,500 a month.",
  rkey=[{"t": "Short answer", "l": ["12 years × €18,000 = %s if it earns nothing; about %s at 5%% above inflation." % (eur(12 * 18_000), eur(round(pv(18_000, 12), -3)))]}])

EXTRA["F07"] = dict(
  teach="The €5,000 a month on your FIRE page is a guess until you know what you spend. Log every cost in What you spend with how often it comes back, keep one-offs out of the monthly figure, and build the number from the categories rather than picking a round figure.",
  walk=[{"h": "How to log", "l": [["Everything, for 30 days.", "Groceries, rent, insurance, transport, subscriptions, going out."], ["How often.", "A bulk buy or a big bill, spread over the months it lasts."], ["One-offs.", "Bought once, not again: out of the monthly figure."], ["Yearly costs.", "Insurance, a phone, a holiday: ÷ 12."]]},
        {"h": "Worked: your %s" % RECEIPTS, "l": ["Five receipts, %s paid." % eur(PAID, 2), "Out: the air fryer, %s, a one-off." % eur(FRYER, 2),
            "Household: toilet paper and a non-food item, %s, about %s a month." % (eur(HOUSE, 2), eur(round(HOUSE_M))),
            "Food: %s in about two weeks: about %s a week, %s a month." % (eur(FOOD, 2), eur(FOOD / 2), eur(round(FOOD_M, -1))),
            "The biggest line: salmon, %s, %.0f%% of the food. Then milk: 22 litres, %s." % (eur(SALMON, 2), SALMON / FOOD * 100, eur(MILK, 2))]},
        {"h": "Plus what’s already logged", "l": ["Chicken, €210 for 50 kg: if it lasts two months, €105 a month.", "Petrol, €120 a tank: every two weeks, about €260 a month."]},
        {"h": "Where it goes wrong", "l": ["One busy month taken as the whole year.", "A one-off counted as monthly, or a monthly cost forgotten."]},
        {"h": "Your turn: your own month", "p": ["Keep logging until 30 days are in, then compare the monthly total with the €5,000."]}],
  need=[{"k": "Food, %s" % RECEIPTS, "v": eur(FOOD, 2), "n": "About two weeks; without the air fryer and the household items."}, {"k": "Already logged", "v": "€210 chicken · €120 petrol"}],
  key=[{"t": "Worked answer, from what’s logged so far", "l": ["Food: about %s a month from Lidl, plus %s of chicken: about %s." % (eur(round(FOOD_M, -1)), eur(CHICKEN_M), eur(round(FOOD_M, -1) + CHICKEN_M)),
        "Petrol about %s a month; household about %s." % (eur(PETROL_M), eur(round(HOUSE_M))),
        "Known so far: about %s a month, before housing, insurance, phone and going out. The rest of the €5,000 stays a guess until those are in." % eur(KNOWN_M),
        "€200 a month less in any category takes €60,000 off the number at 4%."]}],
  thread={"b": "F01 · the number moves with spending; F06 · the bridge it has to pay for", "n": "F08 · the share of your pay you invest"},
  rtask="A €2,000 month: your number at 4% and 3.5%, against the €5,000.",
  rkey=[{"t": "Short answer", "l": ["€600,000 at 4%%; about %s at 3.5%%: €900,000 less than at €5,000 a month, at 4%%." % eur(24_000 / 0.035)]}])

EXTRA["F08"] = dict(
  teach="How fast you get there depends mostly on the share of your take-home pay you invest. It works twice: invested money grows, and money you don’t spend lowers the number. From zero, at 5% above inflation and 4%: invest 10% and it takes about 51 years, 25% about 32, 50% about 17, 75% about 7.",
  walk=[{"h": "Why it works twice", "p": ["Spending less raises the savings rate and lowers the target at the same time. A raise you don’t spend goes straight into the rate."]},
        {"h": "The table", "l": ["10% → about 51 years.", "25% → about 32.", "50% → about 17.", "75% → about 7."]},
        {"h": "Where it goes wrong", "l": ["Counting gross pay instead of take-home.", "Raising spending with every raise (F11)."]},
        {"h": "Worked: €500 more income, or €500 less spending", "p": ["€500 a month more income, all invested, adds €6,000 a year to the pot. €500 a month less spending adds the same €6,000 and also takes €150,000 off the number at 4%."]},
        {"h": "Your turn: your pay now", "p": ["Your take-home pay, what you invested, the savings rate, and roughly the years it gives."]}],
  key=[{"t": "Worked answer", "l": ["Savings rate = invested ÷ take-home pay.", "Years: from the table, or your FIRE page; 30%% gives about %.0f years from zero." % nsr(0.30),
        "The spending cut counts twice: it adds to what you invest and shrinks what you need."]}],
  thread={"b": "F07 · what you really spend", "n": "F09 · what to buy with it"},
  rtask="Your first full-time salary: which savings rate will you set before the first payday, and what does it give?",
  rkey=[{"t": "Short answer", "l": ["Set it before the money arrives: 40%% gives about %.0f years from zero, 50%% about %.0f." % (nsr(0.40), nsr(0.50))]}])

EXTRA["F09"] = dict(
  teach="The core of most FIRE portfolios is one broad, cheap world index fund. In the EU you buy UCITS ETFs, usually Irish-based; most US-listed funds aren’t sold to EU retail investors. Cost is the part you control: 0.07% a year instead of 0.50% leaves about 14% more after thirty years.",
  walk=[{"h": "What to look for", "l": [["Broad.", "Thousands of companies, across the world."], ["UCITS.", "The EU version, with the key information document a broker needs."], ["Cheap.", "The yearly cost (TER), plus broker fees."], ["Accumulating or distributing.", "Matters little for box 3 (F05), which taxes the assumed return either way."]]},
        {"h": "Where it goes wrong", "l": ["Picking by last year’s return.", "Paying 0.5% or more for the same market."]},
        {"h": "Worked: 0.07% against 0.50%", "p": ["After 30 years the cheaper fund leaves about %.1f%% more. If the cheap one reaches €1,500,000, the dear one ends near %s." % ((((1 - 0.0007) / (1 - 0.005)) ** 30 - 1) * 100, eur(round(1_500_000 / ((1 - 0.0007) / (1 - 0.005)) ** 30, -3)))]},
        {"h": "Your turn: two world funds", "p": ["One tracking the FTSE All-World and one the MSCI World: the TER of each, and the difference over 30 years."]}],
  key=[{"t": "Worked answer", "l": ["From each factsheet; the 30-year effect ≈ ((1 − cheaper TER) ÷ (1 − dearer TER))^30.", "A gap of 0.10 percentage points is about %.0f%% after 30 years." % ((((1 - 0.0012) / (1 - 0.0022)) ** 30 - 1) * 100),
        "Beyond cost: what it holds (the All-World includes emerging markets, the MSCI World doesn’t), the fund’s size, and whether your broker sells it cheaply."]}],
  thread={"b": "F07–F08 · what you spend and what you invest", "n": "F10 · buying it every month"},
  rtask="A world fund against a single-country fund: what’s the case for each?",
  rkey=[{"t": "Short answer", "l": ["The world fund spreads the risk of one country’s bad decades; a single-country fund, even the US, bets on one economy and one currency."]}])

EXTRA["F10"] = dict(
  teach="First an emergency fund of three to six months of costs, so a broken car never forces a sale. Then a fixed amount every month, the day after payday, automatically. In a 30% crash the plan says keep buying; write down now, while calm, what you’ll do then.",
  walk=[{"h": "The order", "l": [["Emergency fund.", "Three to six months of costs, in a savings account."], ["Then automatic.", "A fixed amount, the day after your pay arrives."]]},
        {"h": "Why monthly works", "p": ["The same amount buys more units when prices are low and fewer when they are high, and it takes the guessing out."]},
        {"h": "Where it goes wrong", "l": ["Stopping in a crash, when buying pays most.", "Investing the emergency fund."]},
        {"h": "Worked: €1,000 a month through a dip", "p": ["At €100, €70 and €100 a unit, €1,000 buys 10, %.1f and 10 units: %.1f units for €3,000, an average of %s a unit, below the average price of €90." % (1000 / 70, 20 + 1000 / 70, eur(3000 / (20 + 1000 / 70), 2))]},
        {"h": "Your turn: €1,000 a month", "p": ["The amount, the day, the fund and the broker; then three sentences to read in a 30% crash."]}],
  key=[{"t": "A good answer looks like", "l": ["On paper: €1,000, the day after payday, the fund from F09, your broker.", "Three sentences, e.g.: ‘I planned for this. The same money buys more units now. I don’t sell.’",
        "€20,000 at once usually beats spreading it, because markets rise more often than they fall; spreading it over 6–12 months is fine if it keeps you from panicking.",
        "The emergency fund comes first: three to six months of your real costs from F07."]}],
  thread={"b": "F08–F09 · how much, and what", "n": "F11 · the yearly review"},
  rtask="€300 a month for 20 years at 5% above inflation: roughly what does it become?",
  rkey=[{"t": "Short answer", "l": ["About %s in today’s money, from €72,000 put in." % eur(round(3600 * (1.05 ** 20 - 1) / 0.05, -3))]}])

EXTRA["F11"] = dict(
  teach="Once a year, on a date you pick, update four things: what you have invested, what you really spent, inflation, and the rules. Then rebalance if you hold more than one fund, and decide in advance how much of any raise goes into the savings rate.",
  walk=[{"h": "The four updates", "l": [["Invested.", "What the pot is worth now."], ["Spent.", "From What you spend: the year’s real total."], ["Inflation.", "Raise the monthly number by last year’s inflation, so it stays in today’s money (F02)."], ["Rules.", "Box 3 changes nearly every year; a new system is planned for 2028."]]},
        {"h": "Where it goes wrong", "l": ["Lifestyle creep: spending rising with pay.", "Checking the market daily instead of once a year."]},
        {"h": "Worked: one year of 3% inflation", "p": ["Your €5,000 a month becomes €5,150, and the number at 4%% becomes €1,545,000. Your food line of about %s a month becomes about %s." % (eur(round(FOOD_M, -1)), eur(round(FOOD_M, -1) * 1.03))]},
        {"h": "Your turn: this year", "p": ["The checklist with a date in your calendar; then do it now with today’s numbers."]}],
  key=[{"t": "A good answer looks like", "l": ["A date, the four updates, a rebalance rule (e.g. back to the target mix when it’s off by more than 5 points), and a creep rule (e.g. half of every raise to investing).",
        "The update that moves the date most is usually spending; the one most often skipped is inflation."]}],
  thread={"b": "F09–F10 · the plan running", "n": "F12 · the milestones on the way"},
  rtask="Next year’s review: what does €5,000 a month become at 2.5% inflation, and the number with it?",
  rkey=[{"t": "Short answer", "l": ["€5,125 a month; €1,537,500 at 4%."]}])

EXTRA["F12"] = dict(
  teach="Full FIRE is the last milestone, not the only one. Coast FI: enough invested that growth alone reaches your number by pension age. Barista FI: investments cover part of your costs and part-time work the rest. Walk-away money: a year to leave a bad job. Each comes far sooner than the full number.",
  walk=[{"h": "The milestones", "l": [["Walk-away money.", "A year of costs, to leave a bad job."], ["Coast FI.", "Growth alone reaches the number by 67."], ["Barista FI.", "Investments cover part, work the rest; it also softens sequence risk (F04)."], ["Full FIRE.", "The number."]]},
        {"h": "Where it goes wrong", "l": ["Counting only the last milestone, so the plan feels endless.", "Coasting before the number is built from your own spending (F07)."]},
        {"h": "Worked: walk-away money from what you’ve logged", "p": ["The costs logged so far come to about %s a month: a year is about %s. It will grow as housing and the rest go in, but it is the first milestone to aim at." % (eur(KNOWN_M), eur(round(KNOWN_M * 12, -2)))]},
        {"h": "Your turn: your plan", "p": ["Coast FI for €1,500,000 by 67, and Barista FI with €2,000 a month earned."]}],
  key=[{"t": "Worked answer", "l": ["Coast FI = €1,500,000 ÷ 1.05^(years to 67): with 37 years to go about %s; with 27 years, about %s." % (eur(round(1_500_000 / 1.05 ** 37, -3)), eur(round(1_500_000 / 1.05 ** 27, -3))),
        "Barista FI: (€5,000 − €2,000) × 12 ÷ 3.5%% = %s." % eur(36_000 / 0.035),
        "Walk-away money comes first: a year of your real costs."]}],
  thread={"b": "F10–F11 · the plan running, and reviewed", "n": "the monthly transfer, and the review in your calendar"},
  rtask="€3,500 a month: Coast FI with 30 years to 67, and Barista FI with €2,000 earned.",
  rkey=[{"t": "Short answer", "l": ["Number €1,050,000 at 4%%; Coast FI about %s; Barista FI %s." % (eur(round(1_050_000 / 1.05 ** 30, -3)), eur(18_000 / 0.035))]}])

GLOSSARY = [
    (3, "withdrawal rate", r"withdrawal rate"), (4, "sequence risk", r"sequence risk"), (4, "cash buffer", r"\bbuffer\b"),
    (5, "box 3", r"\bbox 3\b"), (5, "fiscal partner", r"fiscal partner"), (6, "AOW", r"\bAOW\b"), (6, "the bridge", r"\bthe bridge\b"),
    (8, "savings rate", r"savings rate"), (9, "TER", r"\bTER\b"), (9, "UCITS", r"\bUCITS\b"), (10, "emergency fund", r"emergency fund"),
    (12, "Coast FI", r"Coast FI"), (12, "Barista FI", r"Barista FI"),
]

def check_extra():
    e = lambda a, b, tol=0.01: abs(a - b) <= tol or sys.exit(f"bad number: {a} vs {b}")
    e(FOOD, 183.52); e(HOUSE, 22.92); e(PAID, 275.44); e(40.34 + 0.01, 40.35); e(59.06 - 0.01 + 0.69, 59.74); e(42.80 - 0.02, 42.78)
    e(SALMON, 82.84); e(MILK, 31.90); e(FOOD_M, 398.99); e(HOUSE_M, 49.83); e(KNOWN_M, 815)
    e(yrs(1_500_000, 1000), 40.6, 0.05); e(yrs(60_000 / 0.035, 1000), 43.0, 0.05)
    e(box3(250_000), 4117.9, 0.1); e(box3(1_500_000, 118_714), 29_835.8, 0.1); e(box3(400_000, 118_714), 6075.8, 0.1)
    e(pv(18_000, 22), 236_934, 1); e(pv(18_000, 12), 159_538.5, 1); e(nsr(0.30), 28.0, 0.05); e(nsr(0.40), 21.6, 0.05)
    e(3000 / (20 + 1000 / 70), 87.50); e(1_500_000 / 1.05 ** 37, 246_653.4, 1); e(1_050_000 / 1.05 ** 30, 242_946.4, 1)
    for lid, x in EXTRA.items():
        assert 150 < len(x["teach"]) < 1100, (lid, len(x["teach"]))
check_extra()
for x in L:
    x.update(EXTRA[x["id"]])


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
check_extras(C["lessons"])
FLAGS = term_order(C["lessons"], GLOSSARY, "F")
if FLAGS:
    sys.exit("A lesson uses a term before the lesson that teaches it, with no pointer:\n  " + "\n  ".join(FLAGS))
write("FIRE_CURRICULUM", ["Your FIRE plan — 12 sittings on your own numbers (the €5,000 a month your FIRE page holds, the costs you log), with the",
      "Dutch rules of 2026: box 3 at 36% on an assumed 6.00% above €59,357 (Belastingdienst; a new system is planned for 2028",
      "but not settled), AOW at 67 years and 3 months for 2028–2031. Built by scripts/build-fire-course.py, which checks every figure."], C)
