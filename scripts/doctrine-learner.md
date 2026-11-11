# Damodaran's rules, written for learning them

The "Want more" notes in the investing lessons. Rewritten from the Valuation Agent doctrine
(valuation-agent commit 881fafa) for a learner: the rule, why it holds, his example, his own words,
and what to watch out for. The lessons that practise each rule are added by the build script.
Built into time-tracker.html by: python3 scripts/build-doctrine-learner.py

# D-01 · The story
stage: 1 · Story

## The rule
Before you set any number, tell the story of the business: what it sells, who buys it and why, who it competes with, and where it is heading. Then every input has to agree with that story. The story is what turns a list of numbers into one valuation.

## Why
Number people think spreadsheets make them objective; storytellers think a big story deserves a big number. Both are fooling themselves. Asking for a story *and* numbers, and making them agree, keeps each honest.

## His 3P test
Grade every claim in the story:

| Test | What it asks |
|---|---|
| **Possible** | Could it happen at all? The weakest test. |
| **Plausible** | Is there a mechanism, and has something like it happened before? |
| **Probable** | Has the company already pulled it off, at least in a small part of the market? |

Only probable claims go in the base case; plausible ones belong in a range. "It's possible" defends almost nothing.

## In his words
> "Valuation is a bridge between stories and numbers … I'm going to force you to tell that story, because that's what's going to connect your numbers together."

> "A company valuation without a story to bind it together is just numbers on a spreadsheet, and a story that uses no numbers at all is a fairy tale."

## Watch out
- **Changing the story is fine** when the facts change. Changing it to justify a number you wanted is not.
- **A story claim with no number behind it** (it doesn't raise a margin, lengthen growth or cut reinvestment) doesn't belong in the story.
- **Numbers with no story** are the more common mistake: every input should trace to a sentence you could say out loud.
- **Young companies**: the story carries almost all the value, so test it hardest there.

# D-02 · Currency choice
stage: 2 · Currency and riskfree rate

## The rule
Currency is a unit of measurement, not a bet. Value a company in any currency you like: done consistently, the answer comes out the same. Pick the currency you have clean data for, and stay in it.

## Why
A high riskfree rate isn't a penalty; it signals high expected inflation. The same inflation shows up in the cash flows and in the exchange rate. Raise the discount rate for inflation but leave it out of the cash flows, and you get a lower value for no economic reason. That isn't caution, it's a mistake.

## His example
He asks a Brazilian student: value a Brazilian company in reais at a 7.5% riskfree rate, or in dollars at 2.5%. Which gives the higher value? Neither: the answer must be the same, "and thank God for that", or anyone could manufacture a value by switching currencies.

## In his words
> "Inflation is the driver of risk-free rates, the driver of exchange rates."

## Watch out
- **Bad local data** is a good reason to value in dollars or euros instead. It's a data choice; say so.
- **Very high inflation** (40% a year): the maths still works, but forecasting nominal cash flows gets fragile. Use a stable currency, or real terms (then the rate and the growth are both real).
- **Revenue in many currencies** is a question about country risk (D-08), not about which currency to value in.

# D-03 · Riskfree rate
stage: 2 · Currency and riskfree rate

## The rule
A riskfree rate needs two things: **no default risk** and **no reinvestment risk**, with a length that matches the cash flows. For a going concern valued in dollars, that is today's 10-year US Treasury rate, not an average or a "normal" rate.

## Why
The second condition is the one people forget. A one-year bill held for ten years isn't riskfree: next year you reinvest at a rate nobody knows. Use today's rate because it is what you can lock in today, and it is the rate inside the prices you'll compare your value with. If you think rates will move, say that as a forecast; don't quietly reset the base.

## His example
Since Moody's cut the US to Aa1 in 2025, he takes the US default spread off the Treasury rate: 4.18% − 0.23% = **3.95%** at the start of 2026. He called it the biggest change in how he works that year. (Lesson L03 uses these numbers.)

## In his words
> "There can be no default risk and there can be no reinvestment risk."

## Watch out
- **A government that can default**: its bond rate isn't riskfree. Take its default spread off (D-04).
- **No long-term local bond**: build a rate from a stable currency's rate plus the inflation gap, or value in the stable currency (D-02).
- **Negative rates**: take them as they are. A floor at zero is a view about rates, not a fact.
- **Real terms**: rare outside very high inflation ("Honduras or Argentina or Venezuela"). Then the riskfree rate is a real rate (in the US, the TIPS rate) and the cash flows must be real too.

# D-04 · When the government is not default-free
stage: 2 · Currency and riskfree rate

## The rule
If the government can default, its bond rate isn't riskfree. Take out the default spread:

    riskfree rate = government bond rate − sovereign default spread

Three ways to measure the spread, all fine: the gap between the country's dollar bond and a US Treasury; its credit default swap (CDS); or the spread for its credit rating.

## His example
Brazil: a 12.3% government bond. Spreads of 3.17%, 2.82% and 2.83% from the three methods give riskfree rates of 9.13%, 9.48% and about 9.17%.

## Why
Which method you pick barely matters, **as long as you use the same spread again** when you build the country's equity risk premium (D-07). A high spread lowers the riskfree rate and raises the risk premium by the same amount, so the value hardly moves. Using a high spread for one and a low one for the other creates value out of nothing.

## In his words
> "It doesn't matter which of the three you pick, as long as you stay consistent."

> "Don't sit here two hours trying to pick which of these three. Just pick one and keep moving. At least remember which one you picked."

## Watch out
- **No dollar bond**: use a euro bond against a German bond, or the CDS or rating.
- **Local and foreign-currency ratings differ** (they often do): a local-currency bond needs the local-currency rating.
- **A bond rate you don't trust at all**: build the rate from inflation instead, or value in a stable currency.

# D-05 · The mature market premium
stage: 3 · Equity risk premium

## The rule
Every equity risk premium starts from one number: what investors demand for owning stocks in a mature market, in practice the US. Every other market is that number plus a country risk premium (D-07).

## Why
The riskfree rate is the price of time; the equity risk premium is the price of risk. A beta only says how risky a stock is *relative* to the average; it means nothing until you multiply it by that price. Building every market as "mature premium + country premium" keeps them all on one scale, so the judgement sits in one number you can defend and update.

## His example
Start of 2025: 4.33% against a 4.58% Treasury rate. Start of 2026: 4.23% against 4.18%, or 4.46% against his 3.95% riskfree rate (L04).

## In his words
> "When you say beta for a stock is 1.2, you're saying it's 1.2 times as risky as the average stock, and then you've got to tell me what the price of risk looks like in the equity market."

## Watch out
- **A company selling in many markets** gets a premium weighted by where its revenue comes from, not where it is listed (D-08).
- **It moves**, sometimes violently in a crisis (D-06). Note the date of the number you use.

# D-06 · Implied vs historical premium
stage: 3 · Equity risk premium

## The rule
Use the **implied** premium: the return that makes the index's expected cash flows worth today's index level, less the riskfree rate. Don't use an average of past returns, and recompute it rather than reusing an old one.

## Why
A historical average fails on statistics alone. Stock returns swing so much that even a century of data leaves a huge standard error: the true US premium could be anywhere from about 1% to 10%. That isn't an input, it's a shrug. A shorter window feels more current but makes the error bigger.

The implied premium is arithmetic on today's prices, and it moves when the world moves. In March 2020 it nearly doubled in six weeks, while companies' cash flows barely changed. Only the implied premium sees that.

## His example
In six weeks of 2020 the implied premium rose to almost 8%. In L15, swapping his implied 4.23% for the 1928–2025 average of 7.03% takes KO from $61.79 to $44.72 a share.

## In his words
> "Every estimate of an average comes with a standard error … as I go from close to 100 years to 50 to 10, the standard error is getting larger."

> "This is the essence of a crisis: the price of risk just dramatically explodes in a short period, because the earnings and the cash flows can't be changing that dramatically."

## Watch out
- **If you must use a historical number**, use the geometric (compounded) average; the arithmetic one "missed the compounding effect".
- **Markets without good index data**: use the mature premium plus a country premium (D-07).
- **Your own view on the premium** is allowed, but state it as a view; don't swap in an average and call it neutral.

# D-07 · Country risk premium
stage: 3 · Equity risk premium

## The rule
For a market that isn't mature, add a country risk premium to the mature premium (D-05). Three ways to build it. Brazil, January 2025, mature premium 4.33%, default spread 2.83%:

    1. default spread only:        4.33% + 2.83%              = 7.16%
    2. relative equity volatility: 4.33% × (30% ÷ 18%)        = 7.22%
    3. melded:                     4.33% + 2.83% × (30% ÷ 20%) = 8.58%

(30% is the volatility of Brazil's stock market, 18% the S&P 500's, 20% Brazil's government bonds.) The default spread must be the same one you took off the riskfree rate (D-04).

## Why
A credit rating measures the risk of the government defaulting on its debt, and owning shares is riskier than owning that debt. So the default spread alone is too low. The melded method (his preferred) starts from the default spread and scales it up by how much more volatile shares are than bonds in that country.

## In his words
> "Country ratings measure default risk. While default risk premiums and equity risk premiums are highly correlated, one would expect equity spreads to be higher than debt spreads."

## Watch out
- **This choice doesn't cancel out.** 7.16% to 8.58% for the same country on the same day. Unlike D-04, nothing offsets it, so say which method you used and what the others would give.
- **No traded government bond**: use the rating's spread, or method 2.
- **Volatility from a calm year** understates the premium.

# D-08 · Company exposure to country risk
stage: 3 · Equity risk premium

## The rule
A company's country risk comes from **where it does business**, not where it is based or listed. Weight the country premiums by where its revenue comes from:

    company's premium = Σ (country premium × share of revenue)

A refinement, lambda (λ), scales the country premium up or down around 1 for exposure revenue misses.

## Why
He used to give every company in a country the same premium. Halfway through a flight to São Paulo he compared Embraer, an aircraft maker selling worldwide, with Embratel, then Brazil's domestic phone monopoly, and saw that this made no sense: they don't carry Brazil's risk in the same way.

## His example
KO is based in Atlanta, but 59% of its revenue comes from outside North America. Weighted by revenue its premium is 5.81%, against 4.46% for the US alone (L04). In L31 that one choice moves KO's value by $14.26 a share.

## In his words
> "I decided to title that measure lambda. Why? Because attaching a Greek alphabet makes it much more difficult for people to critique you. Sounds like you did a lot of deep thought."

He's joking, and it's a fair warning: the Greek letter doesn't make the estimate better. Lambda is still a judgement.

## Watch out
- **Coarse disclosure**: many companies report regions like "Europe, Middle East & Africa" that are too broad to weight exactly. Say so; don't invent precision.
- **Where it produces matters too**: a company selling worldwide but making everything in one country carries that country's risk in its costs.
- **Hedges** lower the exposure, if you can see them; being a "national interest" company raises it, because the government has a reason to step in.

# D-09 · Bottom-up beta
stage: 4 · Relative risk

## The rule
Don't use the company's own regression beta. Build the beta from its business:

1. **Name the business by how the company makes money**, not by its label.
2. **Average the betas of many companies in that business**, gathered widely (across the supply chain, across the world), and take out their debt and cash. His industry tables have done this for every listed company.
3. **Weight the businesses by value** if there are several (D-10).
4. **Put back this company's own debt** at its marginal tax rate (D-11).

## Why
Every regression beta is noisy. But average many of them and the errors cancel: precision grows with the square root of the number of companies. 66 US chip companies make an average about √66 ≈ 8 times as precise as one regression. Even five companies beat one, and finding enough is never really the problem.

## His example
KO is one business, soft drinks: his January 2026 table gives an unlevered beta of 0.58 (27 companies). Relevered at KO's 15.7% debt-to-equity: 0.58 × (1 + 0.75 × 0.157) = **0.65** (L05).

## In his words
> "In the last 30 years I haven't valued a single company with a regression beta as my beta."

> "An average of 100 regression betas is going to be 10 times more precise."

> "I have never found a company for which I cannot find enough companies to get a beta, if I define comparable widely enough."

## Watch out
- **US or global table**: he publishes each industry twice. He uses the global table for companies based outside the US (more companies to average), the US table for US companies. Tesla is his exception: he used the global table.
- **Average first, then unlever once** (with the median debt ratio if one company distorts the average).
- **No obvious peers**: widen what you call the business before giving up on the method.
- **Banks**: no unlevering or relevering (D-43).
- Beta matters less than the cash flows (but see L30: for KO it swings the value a lot).

# D-10 · Business mix weighting
stage: 4 · Relative risk

## The rule
A company in several businesses gets an average of its businesses' unlevered betas, **weighted by what each business is worth**, not by its sales. Segment values are rarely reported, so estimate each as its revenue × its industry's EV/Sales.

## Why
Risk follows where the value sits. If one segment has a tenth of the sales but half the value (because its margins are much higher), it drives half the risk. Revenue weights would miss that.

## His example
Twitter (2013): "0.9 × 1.44 (advertising) + 0.1 × 1.05 (data services) = 1.40".

Tesla (March 2025, global table): cars $87,604 M × EV/Sales 1.37 = $119.9 billion; energy $10,086 M × 6.99 = $70.5 billion. Weights 63% and 37%, unlevered beta 1.00. Energy is a tenth of the sales but over a third of the value.

## In his words
> "You can use revenues or operating income by business as approximations … or apply multiples to each of these variables … to arrive at value weights."

## Watch out
- **His industries aren't the company's segments**: you have to decide which industry each segment belongs to, and write the reason down.
- **Companies re-cut their segments** from year to year; check which year's split you're using.
- **A business with no listed peers**: use the closest one and say it's an approximation.

# D-11 · Debt-to-equity and levering
stage: 4 · Relative risk

## The rule
Put this company's debt back into the business beta, using market values:

    levered beta = unlevered beta × (1 + (1 − tax rate) × debt ÷ equity)

His example: 2.36 × (1 + 0.6 × 0.1433) = 2.56.

## Why
A business has its own risk; debt magnifies it. So you take the peers' debt out before averaging (each has its own borrowing policy), then load in this company's. Skip that, and the average quietly carries the debt habits of a hundred other firms.

## In his words
> "Take a safe business and make it incredibly risky by borrowing enough money."

> "When you run a regression you get a regression beta. Is the regression beta levered or unlevered? It's levered. But here's my question: how did that even creep in there?"

(It's levered because the stock it was run on belongs to a company with debt.)

## Watch out
- **Market values of equity, not book** (D-16).
- **The marginal tax rate**, not the effective one (D-23).
- **Debt that will change** (a company paying it down): the beta can change over the forecast too.
- **Equity near zero or negative**: the formula breaks. Use a typical debt ratio for the industry and say so.

# D-12 · When regression betas are defensible
stage: 4 · Relative risk

## The rule
Almost never. This rule exists to close the escape route.

## Why
The usual excuse is "there aren't enough comparable companies". But even five companies give a beta about √5 ≈ 2.2 times as precise as one regression; even two beat one. The only sample size where a regression wins is one, and that isn't a sample.

The other excuse is that a regression is "the market's own estimate". It isn't: it's one noisy estimate, over one chosen window, against one chosen index. Change either and the number changes.

## His example
Tesla's regression beta over 2021–2025 is 1.83, but with a standard error of 0.46 the true value could be anywhere from 0.91 to 2.75, and the S&P 500 explains only 21% of its moves. Its bottom-up beta is 1.32 as a car company, or 1.26 as software (L16).

## In his words
> "If you're saying I'm using a regression beta because I have only five companies, guess what: the square root of five is still going to give you a more precise beta than any single regression beta."

> "You pick a different index, you get a different number."

## Watch out
The real exceptions are narrow:
- **A company that truly is its own industry**, with nothing nearby to borrow from. Rare, and usually a failure of imagination about what the business is.
- **As a check**: if a regression and a bottom-up beta differ wildly, look again at the peer group. Use it as a test, never as the input.

# D-13 · Synthetic rating
stage: 5 · Cost of debt

## The rule
The cost of debt is what the company would pay to borrow long term **today**: not the coupon on old bonds, not interest expense ÷ debt. With no traded bond or rating, make a rating from interest coverage:

    interest coverage = operating income ÷ interest expense

then read the rating and its default spread from his table, and add the spread to the riskfree rate. Tax-adjust it at the marginal rate (D-23).

## His table's shape (large companies)

| Coverage | Rating |
|---|---|
| above 8.50 | AAA |
| 6.50 to 8.50 | AA |
| 5.50 to 6.50 | A+ |
| 4.25 to 5.50 | A |
| 3.00 to 4.25 | A− |
| … down to below 0.20 | D |

Small companies need more coverage for the same rating. He updates the spreads every January (his ratings page).

## His example
KO 2025: $13,762 M ÷ $1,654 M = 8.32 → AA, a 0.55% spread. Pre-tax cost of debt 3.95% + 0.55% = 4.50%; after tax 3.38%. Its actual rating is A+ (L06).

## Why
Old interest costs price debt raised in conditions that no longer hold. You're valuing what borrowing costs now. A real rating is better where one exists; the synthetic one is for the many companies without.

## Watch out
- **Operating income near zero or negative**: coverage means nothing. Clean the earnings first (D-19).
- **A rating and coverage that disagree sharply**: investigate, don't average. It usually means the earnings need cleaning.

# D-14 · Country default burden on cost of debt
stage: 5 · Cost of debt

## The rule
A company in a risky country may pay part of that country's default spread when it borrows, on top of its own spread. How much depends on the company:

    cost of debt = riskfree + (burden × country default spread) + company default spread

## His example
Embraer, carrying two thirds of Brazil's spread: 4.29% + ⅔ × 6.01% + 1.00% = **9.29%**. The two thirds came from what other large Brazilian companies actually paid on their traded bonds.

## In his words
> "Companies in countries with low bond ratings and high default risk might bear the burden of country default risk, especially if they are smaller or have all of their revenues within the country."

> "Larger companies that derive a significant portion of their revenues in global markets may be less exposed to country default risk."

## Watch out
- **No local bonds to compare with**: then it's a judgement. Start at the full burden for a company that sells only at home, and justify anything less.
- **Agree with D-08**: a company you said has little country risk in its equity shouldn't carry the full burden in its debt, unless you can say why (it sells abroad but produces at home, say).
- **The country spread is the same one as in D-04.**

# D-15 · Leases and other commitments as debt
stage: 5 · Cost of debt

## The rule
A payment you're contractually bound to make is debt. Take the present value of the commitments, discounted at the pre-tax cost of debt, and add it to debt. That changes the debt-to-equity ratio, the levered beta (D-11) and the weights (D-16).

## Why
The test is the contract, not the accounting line. He applies it beyond leases to anything you can't walk away from: at Netflix, the content commitments next to the leases in the footnotes are debt too.

## His example
KO's operating leases, $1,722 M, are already on its balance sheet, so they are added to its $45.5 billion of loans and bonds: $47.2 billion of debt (L06, L07). In L06 they barely move KO's cost of capital.

## In his words
> "If you look at the Netflix footnotes, they have lease commitments, and right next to it you see content commitments. When I value Netflix, those content commitments become the equivalent of debt, because they are contractual commitments."

## Watch out
- **Since 2019 (IFRS 16, US ASC 842)** most leases are already on the balance sheet. Check before adding them, or you count them twice.
- **Older footnotes** give five years of payments and then a lump sum; spread the lump sum over a sensible number of years before discounting.
- **Commitments you can cancel** for a penalty are worth the penalty, not the full amount.

# D-16 · Market-value weights
stage: 6 · Cost of capital

## The rule
Weight the cost of equity and the after-tax cost of debt by the **market** values of equity and debt, never book values:

    cost of capital = cost of equity × E ÷ (D + E) + after-tax cost of debt × D ÷ (D + E)

## Why
Book equity is history: what shareholders paid in, plus profits kept, minus buybacks. It isn't what the equity is worth, and a forward-looking rate shouldn't be weighted by an accounting leftover. "Let go of your accounting self" comes up again and again in his class; this is its cleanest use. (He almost never says "WACC"; he says "cost of capital".)

## His example
KO: equity $300.7 billion at market, debt $47.2 billion: 86% and 14%. Cost of capital **7.13%**. With book equity ($32.2 billion) the weights flip towards debt and it falls to 5.13% (L07).

## In his words
> "I take a weighted average based on market values, as opposed to what? Let go of your accounting self."

## Watch out
- **Debt is rarely traded**: estimate its market value as if all of it were one bond, discounted at today's cost of debt. (For KO the bonds' market value was $39.4 billion against $43.9 billion on the books.)
- **Leases** count as debt (D-15).
- **A company clearly moving to a different mix** of debt and equity: the weights, and the beta with them, can change over the forecast.

# D-17 · Currency consistency check
stage: 6 · Cost of capital

## The rule
Not a judgement, a test: value the company again in a second currency. The two answers must agree. A real gap means a mistake, not a range.

## Why
Currency can't change value (D-02), so this is the one place in a valuation where you know the right answer without any opinion about the company. What it catches is inflation in the discount rate but not in the cash flows (or the reverse), a mistake that looks fine inside a single-currency model.

## His example
L17: KO in euros. The cost of capital becomes 6.60% and growth 2.71%, and the value is exactly the same, $61.79 a share. Mix them up (euro cash flows at the dollar rate) and you get $54.74; dollar cash flows at the euro rate, $70.98.

## Watch out
- **Small gaps** are normal: real-world inflation numbers aren't perfectly consistent. Allow a band.
- **Very high inflation currencies** can fail the check for reasons other than a mistake; compare with a stable currency.

# D-18 · One cost of capital, or several
stage: 6 · Cost of capital

## The rule
To value a company as a whole: one cost of capital, from its business mix (D-10) and its debt. For anything inside it (a division, a project, an acquisition): the risk of that thing, not the company average.

## Why
One company-wide rate overprices safe projects and underprices risky ones, so over time the company drifts into risky ones while believing it's being consistent. And the rate isn't a preference you get to choose: it's the price the market charges for that risk.

## In his words
> "One of the biggest sins in investing in companies is using what's called a corporate hurdle rate … you come up with a cost of capital for the company and use it for every project. It is a disaster waiting to happen, because you just don't have to think."

> "I'm never going to ask you what you would like as a hurdle rate … you're a market taker when you enter the public markets."

## His example
His Coca-Cola projects (2018 numbers, L04): Nigeria 3% + 0.80 × 13.15% = 13.52%; Chile 7.98%; the US 7.30%. Same company, same business, three hurdle rates. KO as a whole is one business, so one rate is fine for valuing it.

## Watch out
- **Conglomerates**: the company rate describes none of its businesses. Value the pieces.
- **Acquisitions**: use the target's risk, not the buyer's cheaper rate.
- **A division for sale**: its own beta and its own debt.

# D-19 · The three boxes: cleaning up earnings
stage: 7 · Base-year earnings

## The rule
Before an earnings number goes into the model, sort every expense by what it actually does, not where the accountant put it:

| Box | Test | In the model |
|---|---|---|
| **Operating** | benefits this year only | an expense |
| **Capital** | benefits many years | reinvestment, not an expense |
| **Financing** | comes from using debt | part of the cost of capital |

And start from the **latest twelve months**, not the last annual report: the annual report is months old by the time you value the company.

## Why
Accounting gets two big items wrong in known directions: **R&D**, a capital expense booked as an operating one (D-20), and, before 2019, **leases**, debt kept off the books (D-15). Moving them back isn't a trick to flatter the company; it changes earnings and capital together, and often makes the company look worse.

## In his words
> "A professor came in with three cardboard boxes … he labeled them operating expenses, capital expenses and financing expenses, and he said in accounting we're religious about the way we classify expenses. He was lying, but I didn't know."

> "If you have an expense that creates benefits over many years, it goes into the capital expense box, and if an expense is associated with the use of debt, it goes into the financing expense box."

## His example
NVIDIA, January 2025: twelve months of revenue to October 2024 were $113.3 billion, against $60.9 billion in the last annual report. Starting from the annual report would have missed half the company (L27).

## Watch out
- **Mixed expenses** (selling costs that also build a brand): only move what is clearly capital and disclosed, not on suspicion.
- **Leases** are mostly on the balance sheet now: check before adjusting, or you count them twice.
- **Customer acquisition costs** in subscription businesses are capital in spirit, like R&D; usually you can't see them separately.
- **The latest twelve months may be a boom.** Starting from them is fixed; what to do about a boom is a separate judgement (D-22).

# D-20 · R&D as a capital expenditure
stage: 7 · Base-year earnings

## The rule
Treat R&D as an investment. Pick how many years it pays off for (longer for pharma, shorter for software), build a "research asset" from past R&D, then:

- **add back** this year's R&D to operating income;
- **subtract** this year's amortisation of the research asset;
- **add** the research asset to invested capital;
- count R&D spending as **reinvestment** (D-26).

## Why
R&D pays off over many years, so by the three-box test (D-19) it's capital. It often turns a loss-maker into a profitable company, but it also enlarges the capital, so the return on capital *falls*. The point isn't a nicer earnings number: without it, a pharma or chip company appears to reinvest nothing, and growth (reinvestment × return, D-30) can't be estimated at all.

## In his words
> "If 80% of your expenses are R&D and I capitalize it, you were actually making money."

> "When I capitalize R&D their return on capital decreases by about 5% … so be clear on why we're capitalizing."

> "We capitalize R&D because it gives us a much better perspective on what the company's actually doing, and we need that to estimate growth."

## His example
NVIDIA spent $18.5 billion on R&D in the year to January 2026, three times its $6.0 billion of capital spending. Capex minus depreciation alone says it barely reinvests; with R&D counted, it clearly does (L19).

## Watch out
- **The amortisation life** is the main judgement; say what you used.
- **Short R&D history** understates the research asset; say so.
- **Return on capital below the cost of capital after the change** is a finding, not a mistake: the company was destroying value behind good-looking accounting returns.
- **Bought-in R&D** from acquisitions: don't count it twice with acquisitions (D-28).

# D-21 · One-time charges
stage: 7 · Base-year earnings

## The rule
Add back a truly one-off charge, but test it first: **a charge that keeps coming back isn't one-off.** If a "one-time" charge turns up every five years, a fifth of it belongs in every year's costs. And when you add one back, check what it did to invested capital.

## Why
Companies know analysts add back extraordinary items, so some bundle ordinary costs into them to turn real expenses into "free" earnings. The defence is frequency, not the label. The part almost everyone misses: a write-down shrinks invested capital, so return on capital jumps for no real reason, and since growth = reinvestment × return (D-30), the growth is flattered too.

## In his words
> "Companies know we do it, so you know what they've started doing? They've started gaming the system."

> "When a company takes a restructuring charge, think of what they do to your invested capital … right after the restructuring charge, it drops."

## His example
Boeing: "extraordinary" charges that seemed to happen every year, a pattern. KO 2025 (L08): the $960 M impairments and $47 M fairlife remeasurement are added back; the $97 M productivity programme recurs every year, so it stays in. Clean operating income: $14,769 M.

## Watch out
- **Irregular timing**: average over the observed cycle instead of assuming a fixed gap.
- **Truly one-off items exist** (an asset sale, a settlement): the test is whether history shows repetition.
- **Real cash costs** (severance paid out) aren't paper entries: add back the accounting charge but keep the cash effect.

# D-22 · The target margin, money-losing and cyclical companies
stage: 7 · Base-year earnings

## The rule
Every company gets a **target operating margin** (what it keeps from each dollar of sales once it's grown up) and a **year it gets there**, both written down with a reason. Never just carry today's margin forward unexamined.

1. **Pick a benchmark that fits the story, and name it**: the company's own margin, its industry's average, a named rival, or a percentile of the industry. The target can be *below* today's margin.
2. **A margin above its rivals must be earned** by a named advantage (a brand, a patent, a network). Never add a separate "brand premium" on top: it's already in the margin.
3. **Get there in about 5 years**, his median (range 3 to 10).
4. **When earnings are negative or odd, first ask why**:

| Why | Average the history? | What to do |
|---|---|---|
| A one-off charge | Yes | Add it back, after checking (D-21) |
| A cycle or recession | Yes | Average the margin over a whole cycle, **loss years included** |
| A young company, not yet at scale | No | Target what mature companies in the same business earn |
| A broken business | No | A target only with a real story for getting there, and a chance of failure (D-44) |

## Why
Profit = sales × margin, so the margin is what turns a sales forecast into profit. Even when he expects no change, he types it in as a choice: KO in 2024 got 29.7%, its own margin. He fades very high margins down when he expects competition (Facebook 2020: 44% today, 40% target).

## His examples
- Named rival: Sirius (2006) aimed at Clear Channel's 19.6%. Percentile: Tesla (2013) at the 95th percentile of car makers, 12.5%. Industry: Slack (2019) at the software average, 21.3%.
- Slack's walk from −28.4% to 21.3% over 5 years: −18.5%, −8.6%, 1.4%, 11.3%, 21.3%.
- A cycle with its trough: four years of 28.9%, 15.7%, −23.6% and 35.5% average **14.1%**. Leaving out the loss year gives 28.9%, double.

## In his words
> "When I look at a money-losing company, the first question I ask is why."

> "If your margins are 17% and the industry average is 10% … 17% is going to become 10%." (unless an advantage keeps it up)

## Watch out
- **A broken business that looks cyclical** is the most expensive mistake here. Evidence of recovery has to come from outside the earnings history.
- **The "normal" years may all be a boom.** His costliest mistake: Vale in 2013, valued on five years of iron-ore boom profits at $32.44 against a $13.57 price. He bought; it fell to about $5 and he sold, a 63% loss. Show the longest history you can beside your window.
- **Commodity companies**: since Vale he doesn't average; he takes today's commodity price and simulates around it (D-41).
- **Same basis**: if today's margin treats R&D as investment (D-20), the target must too.

# D-23 · Effective vs marginal tax rate
stage: 8 · Tax rate

## The rule
Two tax rates, two jobs:

- The **effective** rate (the tax in the income statement ÷ profit before tax, over the same period) taxes the operating income. The forecast starts from it.
- The **marginal** rate (the legal rate on the last dollar of income) sets the tax saved by interest (the after-tax cost of debt, the levered beta), and it's where the forecast's rate ends (D-24).

Tax the operating income **as if the company had no debt**. Subtracting the tax actually paid counts the tax saving from debt twice, because the cost of capital already holds it.

## His examples
His 2024–25 models start from the rate each company paid in its latest twelve months: NVIDIA 13.5%, Meta 17.6%, Alphabet 13.9%, Apple 14.8%, Coca-Cola 17.5%. KO 2025: $2,861 M ÷ $15,998 M = **17.9%** (L09). The US marginal rate he uses is 25%, never the 21% federal rate alone.

## In his words
> "It is the effective tax rate … that drives after-tax earnings and cash flows, and the marginal tax rate … that determines the corporate after-tax borrowing cost."

> "In one in five discounted cash flow valuations, tax benefits get double counted."

## Watch out
- **A loss year or a negative rate**: start at the marginal rate, and let the losses carried forward shelter the profit (D-25). "Would I use a negative tax rate going forward? Of course not."
- **A one-off that bent the rate** (a big credit or charge): use a multi-year average or a stated normal rate, and write down why.
- **The cash tax rate** isn't a starting point: "you risk double counting".
- **Effective above marginal** is usually one year's catch-up: bring it down quickly.

# D-24 · The tax convergence rule
stage: 8 · Tax rate

## The rule
Start at the effective rate, **hold it for years 1–5, then walk it in equal steps to the marginal rate by year 10**. The terminal value is taxed at the marginal rate.

## Why
A low effective rate usually means taxes paid later, not never, and deferred taxes come due. The marginal rate from year 1 understates the early years; the effective rate forever overstates every later year. A path makes both right: one now, the other eventually. (The same trick as growth fading, D-32, and returns moving to the cost of capital, D-34.)

## His examples
Apple, 2016: 26.49% for five years, then 28.19, 29.90, 31.60, 33.30, 35.00%. NVIDIA, January 2025: 13.5% for five years, then 15.8, 18.1, 20.4, 22.7, 25.0% (L29). KO: 17.9% for five years, then up to 25% (L09); the path takes 5.5% off KO's operating value compared with 17.9% forever.

## In his words
> "By using the marginal tax rate, we tend to understate after-tax operating income in the earlier years … By using the effective tax rate, we tend to overstate … You can have your cake and eat it too, by starting with the effective tax rate, and adjusting towards the marginal tax rate over time."

> "You cannot defer taxes forever."

## Watch out
- **A low rate from *where* the company earns** (low-tax countries), not from deferral, may stay low. He left Amazon's rate alone once for that reason, but his own Amazon 2024 sheet converged anyway. It's an exception you argue for, never a default.
- **Already at the marginal rate**: no path, the rate stays flat.

# D-25 · Net operating losses
stage: 8 · Tax rate

## The rule
Keep a running balance of past losses. While the company has them, it pays no tax on the profit they cover; once they're used up, it pays the rate from D-24.

## Why
A young company, or one after a bad cycle, pays no cash tax in its first profitable years. An average tax rate from year 1 gets the amount wrong and the timing wrong, and value depends on when cash arrives. It goes with D-22: a young company valued off a target margin usually carries exactly the losses that shelter its first profits.

## In his words
> "Year three, I make money, but I still don't pay taxes. How come? I carry my losses. Best way to deal with NOLs in a DCF is to keep track of them and save taxes while you have them. And once you run out of them, you pay."

## His example
His Paytm IPO model (2021) carries losses for its first loss-making years and uses them up in years 5 and 6, before tax starts (L28).

## Watch out
- **Limits**: many countries cap how much you can use each year, or let losses expire.
- **A takeover** can sharply limit the buyer's use of the target's losses.
- **Losses in one country** don't shelter profits in another.

# D-26 · Net capital expenditure
stage: 9 · Reinvestment

## The rule
Reinvestment is everything the company spends to grow, not just what the cash flow statement calls capital expenditure:

    net capex = capex − depreciation
              + R&D treated as capital (D-20)
              + acquisitions (D-28)
              + leases treated as debt (D-15)

## Why
Growth comes from reinvestment × return on capital (D-30). Every dollar of real reinvestment you miss is growth that looks free, and free growth is the most common way a valuation produces an absurd value. And the reverse check: **anything you add to invested capital must also count as reinvestment**, or you've created growth from nothing.

## His example
KO 2025: capex $2,112 M − depreciation $1,050 M + acquisitions $461 M = $1,523 M of net capex, 12.6% of its after-tax operating income (L10).

## In his words
> "We're going to shred those assumptions and look past what you see as capex and depreciation."

## Watch out
- **Depreciation above capex** is fine for a shrinking company: net capex is negative. Don't floor it at zero.
- **One big year** (a new plant): average over several years, but check the average isn't hiding a trend.

# D-27 · Working capital
stage: 9 · Reinvestment

## The rule
Use **non-cash** working capital, and only its change: take out cash, short-term securities and interest-bearing short-term debt.

    reinvestment in working capital = change in (non-cash current assets − non-debt current liabilities)

Forecast it as a share of revenue, not as a level.

## Why
Growing sales usually needs more stock and more unpaid customer bills, and that uses cash even though none of it is capex. Leave it out and growth is partly free again (D-26). Cash comes out because it isn't an operating asset (D-36): a company piling up cash would otherwise look like it's reinvesting heavily. Short-term debt comes out because it's financing (D-19).

## His example
KO's 2025 working-capital line was distorted by about $6.1 billion paid for fairlife, a one-off, so the worked answer leaves it out and treats KO's working capital as small (L10).

## Watch out
- **Negative working capital** is often an advantage: retailers and subscription businesses get paid before they pay. Growth then *releases* cash. Don't floor it at zero.
- **One odd year**: use a normal share of revenue.
- **Ever-improving efficiency** is a real source of value, but it can't go on forever.
- **With sales-to-capital** (D-29), working capital is already inside the ratio: don't add it twice.

# D-28 · Acquisitions as reinvestment
stage: 9 · Reinvestment

## The rule
Acquisitions are reinvestment. Count them in net capex (D-26), **including those paid for in shares**.

## Why
A company that buys its growth and pays in shares shows strong earnings growth and almost no capex. Model it naively and it grows for free, which is worth infinity. The growth was bought; it was just paid in a currency (dilution) that never shows up as capex unless you put it there.

## His examples
GE in 1985–1990: analysts kept overvaluing it by projecting its earnings growth while ignoring that it bought much of that growth, often with shares. Cisco at its peak reinvested **107%** of its earnings, more than it earned, because of its acquisitions.

## In his words
> "GE did a lot of acquisitions, often with shares. They wouldn't count that as part of the capex, so GE's grown with almost nothing reinvested. It's happening, you're just missing it. So we bring in acquisitions."

## Watch out
- **Lumpy history**: average over several years. A serial buyer has a steady rate; an occasional one doesn't.
- **A company that will stop buying**: reinvestment falls *and so does growth*. Both, or neither.
- **The price paid is the reinvestment**, not the goodwill line. A later goodwill write-down is a separate matter (D-21).

# D-29 · Sales-to-capital: what growth costs
stage: 9 · Reinvestment

## The rule
Charge a company for the growth its story assumes, through one ratio: **sales-to-capital**, the dollars of new revenue each dollar invested brings in.

    reinvestment this year = (next year's revenue − this year's revenue) ÷ sales-to-capital

Choose one ratio for years 1–5 and one for years 6–10, set beside the company's own ratio and its industry's. (Not for banks: D-43.)

## Why
A company can't grow for free: to sell more next year it spends now, on factories, servers, software, stock, even acquisitions. He picks the growth from the story, then bills it at this ratio, so a bigger story always comes with a bigger bill. He uses it for every company, mature ones like Walmart and Coca-Cola included, because it moves less from year to year than raw capex.

## His example
"Your revenues grow 300 million with a sales-to-capital ratio of three, you've got to invest 100 million." NVIDIA: 1.15 in June 2023 (it had made only $0.65 per dollar of capital, R&D included, and the industry median was 1.15); 2.5 in January 2025, after its own ratio jumped (L19).

## In his words
> "I'm going to tie the reinvestment to the change in revenues … those are the three big numbers that drive every valuation." (growth, margin and this ratio)

> "This is the one that gives me the most trouble, because it's the most shaky number."

> "Don't take your sales-to-capital ratio of two and make it 17."

## Watch out
- **A lower ratio costs more than a higher one gains.** On a made-up company, halving the ratio from 2 to 1 cut the value 12%; doubling it to 4 added only 6%. Optimism here is cheap to assume and expensive to be wrong about.
- **A high ratio needs a named reason**: spare capacity (Boeing's idle lines, 10 for five years), or past investment to live off (Alibaba 2021). And only for a limited window.
- **Heavy spending (AI capex)** goes into this ratio, never into faster growth.
- **Check the return on new money**: ratio × pre-tax margin = pre-tax return on each new dollar. Growth adds value only if that beats the cost of capital.
- **Falling revenue** gives negative reinvestment: capital coming back.

# D-30 · Fundamental growth
stage: 10 · Growth

## The rule
Growth has to be paid for. It comes from how much of its profit a company puts back, and how well that money earns:

    growth in operating income = reinvestment rate × return on capital
    reinvestment rate = reinvestment ÷ after-tax operating income
    return on capital = after-tax operating income ÷ invested capital

He trusts it to set the growth only for a **steady company** (margins and returns no longer moving), and then on several years' numbers, not one. For everyone else he chooses revenue growth from the story and charges for it through sales-to-capital (D-29). The formula always works for the years after year 10, run backwards (D-34), and as a check.

## Why
It makes the *quality* of growth visible. Two companies both growing 10%: one earns 50% on new money and reinvests 20% of its profit, keeping 80% as cash; the other earns 12.5% and must reinvest 80%. Same growth, four times the cash. If the second earns less than its cost of capital, its growth destroys value.

## His example
Disney, 2013: reinvestment rate 53.93% × return on capital 12.61% = **6.80%** a year. KO 2025: 12.6% × 25.6% = **3.21%** (L11).

## In his words
> "With stable margins, operating income growth can be tied to how much a firm reinvests and the returns it earns. With changing margins, you have to start with revenue growth, forecast margins and estimate reinvestment."

> "One is clearly a winner: 10% growth, very little reinvestment. You can get 80% of your earnings as cash flow and still grow 10% a year."

## Watch out
- **Losses**: the formula breaks. The growth stands on the story.
- **One odd year**: average several, or move toward the industry. He used 5.40% for Deutsche Bank (2003–07 averages), not 2007's 13.04%.
- **A reinvestment rate above 100%** is real (spending more than it earns, with outside money), but never multiply it out into years of growth. Cisco 1999: 107% × 34% ≈ 36% was a warning, not a forecast.
- **A return flattered by accounting** (R&D not capitalised, write-downs) inflates growth too. Clean the accounts first (D-19 to D-21).

# D-31 · Why analyst forecasts are not inputs
stage: 10 · Growth

## The rule
Don't take analysts' consensus growth as your growth. Use it as a cross-check on yours, never as a replacement.

## Why
Three reasons, the last the most serious:

- **It's free growth.** A number from outside comes with no reinvestment behind it, so the company grows without paying for it (D-26, D-28).
- **It's short.** Forecasts run one to five years; a valuation needs a path to a steady state.
- **It's someone else's story without its numbers.** You get the conclusion, not the reinvestment and returns that justified it, so you can't check it against anything else in your model.

## His example
L20: the analysts' 22.88% for semiconductors. At NVIDIA's 47% return on capital it needs 48% of profit reinvested; at the industry's 27%, 84%; at his long-run 20%, 114%, more than everything it earns. Same growth number, very different companies.

## Watch out
- **As a check it's worth doing**: if your growth is far from consensus, one of you is wrong; find out which, rather than adopting theirs.
- **Guidance on a specific event** (a plant opening, a contract) is information about cash flows: use it there.
- **A young company with no history**: use sales-to-capital (D-29), not consensus.

# D-32 · Growth fade
stage: 10 · Growth

## The rule
Every forecast has the same ten-year shape (his standard spreadsheet):

- **Year 1**: next year's growth (the same as years 2–5 unless a named one-off is expected);
- **Years 2–5**: the chosen growth rate, held flat;
- **Years 6–10**: steps down in five equal amounts to growth forever (D-33);
- **Year 11 on**: growth forever.

A mature company keeps the ten years, at growth forever in each of them. Nothing grows fast for more than ten years.

## Why
Fast growth doesn't last: success draws competitors, and a big company can't keep doubling. Most US growth companies stop growing fast within 3 to 5 years; ten years is already rare. So growth glides down instead of falling off a cliff in year 11, and the story is told through the growth numbers, not through a different calendar for each company.

## His example
Airbnb, 2020: 25% in years 2–5, growth forever 2%. Step = (25 − 2) ÷ 5 = 4.6 points: 20.4%, 15.8%, 11.2%, 6.6%, 2.0%. NVIDIA, January 2025, "the rest" of its business: 15% → 12.9, 10.9, 8.8, 6.8, 4.7% (L29).

## The cost of capital fades too
A company that grows up also becomes less risky: its beta moves toward 1 (the average company), so its cost of capital glides to a mature company's by year 10. NVIDIA: 11.79% for years 1–5, then down to 8.5%. For a low-beta company like KO this *raises* the rate later, and holding it flat overvalues it. (His own exception: he held Coca-Cola's rate flat in 2024, close to the global soft-drinks median.)

## In his words
> "You don't go from 50 to two … you create a transition period."

> "If you set your growth period to be much longer than ten years, you are already building in the expectation that your firm is an exceptional firm."

> "I have never done a valuation where my cost of capital stays the same over time."

## Watch out
- **A one-off next year** (Airbnb's +40% COVID recovery, Birkenstock's "Barbie" year) goes in year 1 only.
- **Shrinking companies** can have negative growth in years 2–5 (Boeing 2020: −10%); the glide then climbs.
- **Giving every company a high-growth phase** by default is a common and expensive habit.

# D-33 · Terminal growth capped at the riskfree rate
stage: 11 · Terminal value

## The rule
Growth forever (every year after year 10) can be no higher than the riskfree rate used in the same valuation:

    growth forever ≤ riskfree rate

Equal to it is his usual choice. Below it needs a story (a company that will grow more slowly than the economy, or shrink). Above it: no.

## Why
The riskfree rate is roughly expected inflation plus a real return, which is roughly how fast the whole economy grows in money terms. No company can outgrow the economy forever, or it becomes the economy. And because the same rate sits inside the discount rate, tying the two together keeps them consistent: when rates are high, both are high, so a wrong rate cancels instead of compounding.

## His examples
Equal to the riskfree rate: Twitter 2013 2.7%, Airbnb 2020 2%, Amazon 2024 4.08%, NVIDIA January 2025 4.7%. Below it: Kraft Heinz 2019, 1%. With a negative riskfree rate, growth forever goes negative too (Heineken 2019: −0.5%).

## In his words
> "If you let it exceed the risk free rate, you are on your own in uncharted territory." (his spreadsheet, beside the input)

> "What one hand gives you, the other hand takes away."

> "If you're valuing a Turkish company … 15%, 18% riskfree rate … and use whatever growth rate you want, 3 to 5%, I'll save you the trouble: no Turkish company is ever going to look cheap to you."

## It often matters less than it looks
Growth has to be paid for (D-34). With next year's after-tax profit $100 M and a 10% cost of capital: no growth is worth 100 ÷ 0.10 = $1,000 M. Growth of 2% earning exactly 10% needs 20% reinvested: 80 ÷ 0.08 = $1,000 M, the same. Growth forever only moves the value when the return forever differs from the cost of capital.

## Watch out
- **A growth rate in years 2–5 below growth forever** makes growth *rise* later. Usually growth forever should be lower.
- **Real terms**: the cap is the real riskfree rate.
- **Many countries**: the cap follows the currency of the valuation, not where the company operates.
- He admits the cap is probably a little strict, and keeps it because growth forever is "the easiest place to push a value up".

# D-34 · Return on capital in the terminal year
stage: 11 · Terminal value

## The rule
After year 10 the company earns one return on capital forever. The reinvestment it needs to keep growing follows from it:

    reinvestment rate forever = growth forever ÷ return on capital forever
    terminal value = year-11 after-tax profit × (1 − reinvestment rate) ÷ (cost of capital − growth forever)

- **Default: equal to the cost of capital.** No lasting edge.
- **Above it** (a "moat") only with a named, lasting advantage: a brand, a network, patents, switching costs, a cost edge.
- **Below it** only for badly run firms that won't change.

## Why
If each new dollar earns exactly what it costs, growing adds nothing; above it, growth adds value; below it, growth destroys value. So the big assumption in a terminal value isn't the growth rate, it's the excess return and whether it lasts. Working out the reinvestment from growth and return also closes a loophole: you can't keep growth at the cap and quietly raise the return to cut reinvestment.

## His examples
- Growth 3%, return 12%: reinvest 25%, value $1,071 M; return 8%: reinvest 37.5%, value $893 M (from $100 M of profit, 10% cost of capital).
- His own moats: NVIDIA 20% forever (cost of capital 8.5%); Meta, Alphabet, Apple, Amazon, Microsoft 15%; Coca-Cola 2024, its own return at the time (21.95%). Intel: none.
- KO (L12): keeping today's 25.6% forever, $61.79 a share; no edge, $46.55. NVIDIA (L21): the moat is worth $20.62 a share.

## In his words
> "The big assumption in my terminal value calculation is not my growth assumption, it's my excess return assumption."

> "For 80% of companies I go to the default … set it equal to the cost of capital. For one in five companies, where I think the competitive advantages are large and significant, I will leave the return on capital above the cost of capital by maybe 2 or 3%."

## Watch out
- **His practice is more generous than his teaching**: he kept an edge in 115 of 155 of his models, typically 4 to 9 points. That's partly which companies he writes about (famous platforms and brands).
- **Show the value both ways**, with and without the moat, so its price is visible.
- **He takes it away when a story breaks** (Vale: an edge in 2013, removed by 2015).
- **Zero reinvestment fits only zero growth.**
- **Commodity producers** get no edge.

# D-35 · The terminal value's share of value
stage: 11 · Terminal value

## The rule
Check what share of the total value sits in the terminal value. A high share isn't a mistake; it's normal, and for a growth company unavoidable. But it tells you where your effort should go.

A valuation ends in only three ways: cash flows growing forever (D-33, D-34), cash flows for a fixed number of years, or liquidation. **Never** with an exit multiple (year-10 profit × what similar companies trade at).

## Why
If three quarters of the value is terminal, growth forever and the return forever matter more than every forecast year combined. And it's the cash flows, not the discount rate, that usually go wrong.

## His examples
KO: 67% of its value is terminal with the moat, 57% without (L12, L26). His NVIDIA (January 2025): 65% (L21). His Paytm IPO (2021): **97%**; the first ten years were worth only 2.6% (L28).

## In his words
> "A typical valuation, 80% of the time is spent estimating discount rates, 20% on cash flows … When I've screwed up on a valuation, and I've screwed up on lots of them, it's almost never because I got the discount rate wrong, it's because I've got the cash flow wrong."

> "This is a forward pricing dressed up to look like a discounted cash flow valuation." (on exit multiples)

## No exit multiple
It's the usual banking ending, and it turns the biggest number in the valuation into a guess at what the market will pay in year 10: a pricing (D-45), not a value. Pricing is a fine exercise on its own; hiding one inside something called a DCF isn't. Averaging a growth-forever value with an exit-multiple value doesn't fix it either.

## Watch out
- **Above about 90%**: usually a young company whose forecast years are all losses. Fine, but say plainly that the valuation is really a terminal value with a preamble.
- **Near or above 100%**: the forecast years burn cash. That raises the question of funding.
- **Very low**: a declining company, or a forecast doing work the terminal value should.

# D-36 · Cash and marketable securities
stage: 12 · Loose ends

## The rule
The forecast values the business from what its products earn; interest on cash isn't in operating income. So add cash back at the end, **at face value**: cash plus every marketable security, short- and long-dated. No discount by default, and no "operating cash" held back.

## Why
Cash earning a low, riskless return is fairly priced, so it's worth exactly what it is. The only good reason to mark it down is about people: managers with a record of wasting cash may never give it back. (One study he cites: a dollar of cash priced at about 69 cents in mature companies earning below their cost of capital, and about $1.22 in young ones earning well above it.)

## His example
Apple 2023: $29,965 M cash + $31,590 M short-dated + $100,544 M long-dated securities = $162,099 M. KO 2025: $13,872 M of cash and short-term investments, $3.23 a share (L13).

## In his words
> "Don't mess with cash. Cash is cash: 100 million in cash is worth 100 million."

> "The right reason for discounting cash is because you don't trust management. The wrong reason is cash earns a low rate of return."

## Watch out
- **Trapped cash** (profits abroad that would be taxed coming home): worth face value minus that tax. He stopped using it after the 2017 US tax law.
- **Balance-sheet cash is one day's number** and can be dressed up; at Satyam it didn't exist.
- **Shares in another company** aren't cash: they're a stake (D-37).
- **What working capital took out must come back here**, no more, no less (D-27).

# D-37 · Cross-holdings
stage: 12 · Loose ends

## The rule
Two opposite corrections, depending on whether the company controls the stake:

| Stake | In the accounts | Fix |
|---|---|---|
| **Not controlled** (under about 50%) | its profit sits below operating income, so the forecast has none of it | **Add** the stake's value |
| **Controlled** (consolidated) | 100% of it is in the accounts | **Subtract** the outsiders' share: the minority interest |

    operations + cash + stakes − debt − minority interest = equity

## Why
A forecast built from operating income misses the stakes entirely, so their value has to be added at the end or it's lost. The mirror case: own 60% of a company and the accounts count 100% of it, so the 40% that belongs to others comes off.

## At what value
Best: value each stake on its own. Next: a listed stake at its market price (he calls this cheating, because it imports the market's mistakes, but uses it). A private stake at book × its sector's price-to-book, or at book if nothing else exists.

## His example
KO (L13): its listed bottlers at market, $34.3 billion (book $14.0 billion), plus $6.2 billion of other stakes at book. At market the stakes add $9.42 a share; at book, $4.70. Minority interest: $2,106 M. His own 2024 Coca-Cola sheet used book.

## In his words
> "When you own 60% of a company … accountants ask you to act like you own 100% … minority interest … the value of the 40% that doesn't belong to you."

> "Before you get carried away, check out the liability side: if you see a noncontrolling or minority interest, something's been consolidated somewhere."

## Watch out
- **Never twice**: a stake already inside "marketable securities", or one whose cash flows are already in the forecast, isn't added again.
- **Taxes on a planned sale** come off (Yahoo 2015: $16.3 billion), but only if a sale is planned.

# D-38 · Debt — all of it
stage: 12 · Loose ends

## The rule
Subtract every claim that comes from borrowing: short- and long-term debt, leases and other commitments (D-15), underfunded pensions, and the debt of subsidiaries whose cash flows are in your forecast. Not accounts payable or other operating liabilities: those are working capital.

## Why
The test is D-19's: does it come from using debt? And it must be exactly the same debt you used for the debt-to-equity ratio (D-11), the weights (D-16) and the cost of debt (D-13). Three places use one definition, so it's not a fresh decision at the end. Taking a subsidiary's cash flows without its debt inflates equity directly.

## His example
KO (L13): $47.2 billion of debt, leases included, $10.98 a share.

## Watch out
- **Market or book value**: for a healthy company book is close enough. For a distressed one the gap is big, and that's exactly when it matters.
- **Convertible bonds**: split into a bond and an option; the option goes with D-39.
- **Underfunded pensions** are a real claim ahead of shareholders.

# D-39 · Employee options
stage: 12 · Loose ends

## The rule
Options already granted are a second claim on the equity. Value them with an option pricing model, subtract that value, and divide by the **actual** shares outstanding:

    value per share = (equity value − value of options) ÷ actual shares

Not the diluted share count, not the treasury stock method. And never add stock-based pay back to earnings.

## Why
Stock-based pay is pay: the company bought work and paid in shares instead of cash. Adding it back pretends it was free. Two effects, both needed: **past** grants are a claim on today's equity (subtract them here); **future** grants are an ongoing cost (leave them in expenses).

## His example
KO (L13): 27 M options at an average exercise price of $55.74 against a $69.91 price, worth at least 27 M × $14.17 = $383 M. He'd value them as options, a little more.

## In his words
> "Stock-based compensation is the most mangled aspect of valuation that I see out there."

> "In the cost of goods sold for a software company there will be stock-based compensation, and analysts don't like this, so what do analysts and companies do? They add it back. This is a stupidity."

> "I'm not as valuable as a company if I have to give out 15 full pizzas every day. That's exactly the way to think about employee options: you're giving away pieces of my business."

## Watch out
- **Diluted shares** treat options out of the money as worthless; they aren't.
- **Restricted shares (RSUs)** are effectively shares: count them in shares outstanding.
- **Heavy issuers** have a big outstanding claim *and* a big ongoing cost; capturing only one is the usual half-fix.

# D-40 · Control and voting rights
stage: 12 · Loose ends

## The rule
Control is worth the difference between the company **as it's run** and **as it could be run**:

    value of control = value run well − value as it is

Not a fixed premium. Voting shares are worth more than non-voting ones by the value of control × the chance that control changes hands.

## Why
Control is only worth something where there's something to fix. A well-run company has none; a badly run one has a lot. Value it twice, once as is and once with what a competent manager would achieve, and the gap is the value of control. A flat 20% premium, M&A's habit, overpays for good companies and underpays for bad ones.

## In his words
> "Do you think there's a value of control in NVIDIA? I'd be struggling to find a value of control when you've taken a company that's increased its market cap by 3 trillion."

> "This is embedded in M&A: 20% control premiums."

## His example
KO (L13): no value for control; nobody expects it to be run very differently.

## Watch out
- **Multiply by the chance it can happen**: founders with dual-class shares, government golden shares and family control push it toward zero.
- **"Run well"** must be argued from peers (better margins, reinvestment, debt), not asserted.
- **A minority holder** gets no control value unless someone else takes control and shares the gain.

# D-41 · Simulation over point estimate
stage: 13 · Value per share

## The rule
Report a **range**, not one number. Turn the core inputs (revenue growth, margin, reinvestment) into distributions and run the valuation many times.

## Why
Every judgement before this was a choice within a range. Collapse them all to midpoints and you get one number that looks authoritative and hides how wide the honest answer is. A range also changes the question for the better: not "is it worth $47?" but "in what share of outcomes is it worth more than the price?"

## His example
NVIDIA, June 2023: his simulation gave only about a 5% chance that the stock was worth its $410 price, so he sold half. KO (L14): growth ±1 point gives $51.34 to $79.36; cost of capital ±0.5 point, $55.04 to $70.53.

## In his words
> "You can take your DCF and very quickly make it into a Monte Carlo simulation, where you take your core assumptions (revenue, growth, margins, reinvestment) and make them into distributions."

> "I'm a great believer in Monte Carlo simulations when you feel a lot of uncertainty."

## Watch out
- **Vary the inputs that carry the value** (L30), not all forty.
- **Inputs move together** (margins and growth); treating them as independent understates the extremes.
- **The shape of a distribution** is the biggest unexamined assumption; a low/base/high triangle is rough, and honest about it.
- **Don't report the average as "the answer"**: that undoes the point.
- He doesn't simulate when the answer is obvious: "I'm not running simulations, clearly."

# D-42 · The value-price gap
stage: 13 · Value per share

## The rule
When your value differs from the price, consider both explanations: you're right and the market is wrong, or you're wrong and the market is right. Report the gap, say which explanation your story supports, and name what would have to be true for the market to be right.

## Why
A finished valuation feels earned, and the easy next thought is that the market is mistaken. Often the model is: a wrong margin, a peer group that doesn't fit, a growth period justified by nothing. "My value is 30% above the price, and here's the assumption the market would have to be rejecting" turns the gap into a claim you can test.

## His example
KO (L32): $46.55 to $61.79 against $69.91. For the market to be right, with the moat, KO would need to grow 3.75% a year instead of 3.21%, or deserve a 6.66% cost of capital instead of 7.13%.

## In his words
> "Is it that you're right and the market is wrong? That could be one. Or you're wrong and the market is right."

> "If you can (and very few of us have this capacity) you can be the catalyst to cause the price to move to value."

## Watch out
- **A gap of many times**: check the share count, currency and units first. A value of 1,500 against a price of 150 means "my guess is you got a unit wrong somewhere".
- **Don't tune the inputs until the value matches the price.** The price acts "like a magnet". Change an input only for a reason in the story.
- **A company that has looked cheap for five years**: your method is probably missing something the market prices.
- **No catalyst**: the gap may be real and never close in time. Say so.

# D-43 · Financial service companies
stage: 0 · Routing

## The rule
Banks, insurers and investment banks take a different path. **Value the equity directly**, not the whole firm: debt is a bank's raw material, not its financing.

    cash flow to equity = net income − what it must put into regulatory capital

| | Normal company | Bank |
|---|---|---|
| Cash flow | to the whole firm, at the cost of capital | **to equity, at the cost of equity** |
| Debt | subtracted at the end | **never subtracted: it's inventory** |
| Reinvestment | net capex + working capital | **regulatory capital** |
| Key number | invested capital | **book value of equity** |

## Why
The usual cash flow (net income + depreciation − capex − working capital) can't be computed for a bank. And book equity, an accounting leftover everywhere else, matters here because the regulator watches it: let it fall too far and they shut you down.

What drives the reinvestment: a bank holding less capital than required must put a lot back to keep going, so it's worth less; one holding more can grow without putting much back, so it's worth more. A growing bank needs more capital than a mature one.

## His example
JPMorgan 2025 (L01): $2,559 billion of deposits fund $4,425 billion of assets; equity is only $362 billion, 8.2% of assets. His Citigroup model (2023) runs on its Tier 1 capital ratio (14.8%, target 15%) and return on equity (8.8%, target 9.5%).

## In his words
> "Here's my version of free cash flow to equity for a bank: I start with the net income and then I look at how much you have to reinvest in regulatory capital, and treat that like capex."

> "When a bank borrows money at three percent, it hopes to make money by lending that out at four percent … if debt is raw material, we can no longer think of it as a source of capital."

> "This is one of the places we reward over-capitalization."

## Watch out
- **Price a bank only with equity multiples** (PE, price-to-book), never EV/EBITDA.
- **Rising capital rules** cut cash flow even when nothing else changes.
- **Don't trust the reported numbers blindly**: 2008 showed a bank's assets are valued by models, and loan-loss provisions often need normalising.
- **Insurers aren't banks**: their float works differently from deposits.

# D-44 · Declining and distressed companies
stage: 0 · Routing

## The rule
Two rules:

**1. The chance a company dies is its own input, never a higher discount rate.** Value it as a survivor, say what's recovered if it fails, and weight the two:

    value = going-concern value × (1 − p) + proceeds if it fails × p

**2. A declining company isn't a growth company with smaller numbers.** Four things flip:

| | Normal | Declining |
|---|---|---|
| Revenue | grows | **shrinks, for years** |
| Reinvestment | positive | **negative: assets are sold** |
| Operating margin | roughly stable | ***improves* as the worst parts go** |
| The end | a going concern at scale | **a smaller niche, or liquidation** |

## Why
A valuation quietly assumes the company lives forever. A higher discount rate still assumes cash arrives every year, forever, just smaller; death means no cash after a point, and a rate can't say that. And shrinking is selective: a sensible company closes its worst stores or plants first, so what remains is *better* than the average it started from.

## His examples
- Slack (2019): going-concern value $13,629 M, a 10% chance of failure, half the value recovered if it fails → $12,947 M.
- Walgreens (2024): revenue falling 5% a year, a target margin of 3.5%, an 11.8% chance of failure: $7.53 against an $8.77 price.
- Intel (2024, L01): even at just 3% growth and a 25% margin he got ≈ $23.70 against $18.89, and bought.

## In his words
> "65% of startups don't make it to year two. If I do a DCF of a startup and I don't factor in this failure risk, I'm going to overvalue the startup even if I get every single number right."

> "You don't want a visionary, you don't want Steve Jobs at the top of the company. You want Larry the Liquidator."

## Watch out
- **Decline or just a bad cycle?** The most expensive mistake. Look for evidence outside the earnings (demand, technology, regulation), over three to ten years, not one bad year.
- **Who runs it matters**: here an ambitious manager *subtracts* value with acquisitions; the good outcome is a smaller, better business.
- **Where p comes from changes everything**: Las Vegas Sands (2009) was $5.83 a share using its bond rating, $1.90 using its bond price, against a $4.25 price. Show both.
- **Liquidation is almost never at book value.**
- **Don't count failure twice**: if p is above zero, don't also raise the discount rate.
- Decliners "deserve to be cheap": many look cheap and are.

# D-45 · Pricing is not valuing
stage: P · Pricing

## The rule
Valuing asks what a business is worth from its cash flows and risk. Pricing asks what the market pays for similar companies today. Different tools, often different answers. A pricing verdict (cheap or expensive) is always **relative to peers**, never absolute.

## Why
Both can be true at once: a DCF can say $30 while every comparable trades at a price implying $90. They're different bets: a pricing gap pays off if the peer relationship comes back; a value gap pays off if the market comes round to the cash flows.

## His example
Tesla (L22): in 2020 his story (a very good car company) gave ≈ $430 against $640, so he sold, and kept to it as the price ran to $900. In 2026 Tesla trades at 17.5 times sales, against 3.88 for car makers and 11.41 for software: expensive priced as either.

## In his words
> "Whether you base it on your intrinsic valuation or your pricing, to make money … the market has to correct its mistakes."

> "I bought Tesla because I thought it was undervalued; I sold because I thought it was overvalued. I have to play the game I came to play."

## Watch out
- **A whole sector priced richly**: a company can be cheap against its peers and still expensive on its cash flows. That's KO's position (D-49).
- **No real comparables**: then you can't price it. Don't approximate.
- **A multiple the company can't support** (EV/Sales with no revenue) is no multiple at all.

# D-46 · The consistency rule
stage: P · Pricing

## The rule
The top and bottom of a multiple must belong to the same people: **equity** value over an **equity** number, **enterprise** value over a number measured **before debt**.

| On top | Pairs with |
|---|---|
| Price, market value of equity | net income (PE), book equity (P/B) |
| Enterprise value (equity + debt − cash) | operating income (EV/EBIT), EBITDA, revenue (EV/Sales), invested capital |

## Why
Price is what shareholders pay, so it goes with what shareholders get. Mix them (enterprise value over net income) and you compare a part with a whole; across companies with different debt, the number means nothing.

## His example
KO (L32): PE = $69.91 ÷ $3.04 earnings per share = 23.0. EV/Sales = ($300.7 billion equity + $47.2 billion debt − $13.9 billion cash) ÷ $47.9 billion revenue = 6.97.

## In his words
> "What's the earnings that goes with equity? Net income."

> "All you need to do is take earnings and divide it by the denominator of your multiple and you'll get the companion variable."

## Watch out
- **Enterprise value** must match the earnings: adjust for minority interests and stakes the same way as in the DCF (D-37).
- **Negative earnings** make a multiple meaningless, not just large.

# D-47 · The companion variable
stage: P · Pricing

## The rule
Every multiple has one fundamental that drives it, its **companion variable**. Know it before you use the multiple: a high multiple is only expensive if the companion doesn't justify it.

| Multiple | Companion variable |
|---|---|
| PE | expected growth |
| Price to book | return on equity |
| EV/EBIT, EV/invested capital | return on capital (and growth) |
| EV/EBITDA | reinvestment, tax, risk |
| EV/Sales | after-tax operating margin |

## Why
A multiple is shorthand for a DCF, and the companion is whichever input dominates it. Price-to-book is high when return on equity is high, because book equity earning a high return is worth more than book. EV/Sales is high when margins are high, because revenue that turns into profit is worth more per dollar.

## His example
KO (L32): EV/Sales of 6.97 against 4.16 for soft drinks looks dear, but KO's margin is 31% against the sector's 21%, so much of that premium is earned.

## In his words
> "Every multiple has a companion variable … it's the one number you'd like to know before you use that multiple."

> "The companion variable for price to book is return on equity … do you see a pattern here? The banks at the lowest price to book, for the most part, have the lowest return on equity."

## Watch out
- **PEG (PE ÷ growth)** assumes a straight-line link, which isn't true: "a dangerous game to play because of that linearity assumption".
- **Some multiples have several companions** (EV/EBITDA); a regression handles them better (D-48).
- **The companion can change** as a business matures (users → revenue for online advertising).

# D-48 · Controlling for differences
stage: P · Pricing

## The rule
A company is cheap only if it trades below its peers **after allowing for its companion variable** (D-47). A low multiple may be deserved. Two ways to allow for it:

1. **Matched peers**: compare with companies similar on the companion variable.
2. **Regression**: explain the multiple across many companies with the companion variable, and compare the company with its *predicted* multiple.

## Why
Without the control, a pricing verdict is just noticing one number is bigger than another. Narrow peers need little control but give a small sample; broad peers (a whole sector, or the market) give a big sample and let the regression absorb the differences.

## In his words
> "The essence of pricing is to know what to control for, what questions to ask."

> "For the PE ratio for the market, you have to control for interest rates, you have to control for return on equity, you have to control for risk premiums, and you have to control for what the growth is, before you decide stocks are overpriced or underpriced."

## Watch out
- **In a regression, a variable counts only if it's significant**: his rule of thumb, a t-statistic above 2.
- **The intercept isn't a verdict**: it's the sector's starting level.
- **Too few peers**: widen the definition, or price against the whole market.

# D-49 · The pricing verdict, and the value–price synthesis
stage: P · Pricing

## The rule
Report two things side by side, never blended into one number:

1. **The pricing verdict**: cheap or expensive against peers, after the control (D-48).
2. **The value–price gap**: your value against the price (D-42).

| Value says | Pricing says | What it means |
|---|---|---|
| cheap | cheap | both agree: the strongest case to buy |
| expensive | expensive | the strongest case to avoid |
| expensive | **cheap against peers** | the whole sector is priced richly: a good house on an expensive street |
| cheap | expensive against peers | the market likes the sector but not this company: check your story |

## Why
The two answer different questions with different catalysts (D-45), and the useful information is where they disagree.

## His example
KO (L32): expensive on value ($46.55 to $61.79 against $69.91), but a PE of 23.0 against 26.9 for soft drinks (and 47.8 as a simple average), so fair or cheap against its peers. The third row. And note: priced as a US company, its value would be $76.05, so the verdict depends on the country-risk choice (L31).

## Watch out
- **Both lenses agreeing doesn't make them right**: they can share an error, like the same optimistic growth.
- **A pure pricing trade** (buy the cheap peer, sell the dear one) is fine, but say that's the bet.
- **Only one lens available** (no DCF, or no peers): say so, rather than implying a synthesis.

# routes · Routing: what kind of company is it?

Before any number, decide what kind of company it is, because the kind changes the model, not just the inputs.

| Kind | What changes |
|---|---|
| Mature | The default: today's earnings, reinvestment from net capex, all 13 stages |
| Financial (bank, insurer) | Value the equity, not the firm; debt is raw material (D-43) |
| High growth, young | Revenue drives the model; reinvestment through sales-to-capital (D-29); a target margin (D-22) |
| Declining | Revenue can shrink, reinvestment can turn negative, margins can improve; the chance of failure is its own input (D-44) |

Route it wrong and every later step answers the wrong question. L01 routes KO, JPMorgan, NVIDIA and Intel.

# pairs · Inputs that cancel out

He often puts the same number on both sides of a valuation, so choosing it a little wrong costs little, and choosing it *inconsistently* is the only real mistake.

| The pair | Why it cancels |
|---|---|
| Currency: in the rates and in the cash flows (D-02) | inflation is in both |
| Default spread: taken off the riskfree rate, added to the risk premium (D-04, D-07) | a lower rate comes with a higher premium |
| Riskfree rate: in the discount rate and in growth forever (D-33) | "what one hand gives you, the other hand takes away" |

**The one that doesn't cancel:** his three ways of measuring country risk (D-07) gave Brazil 7.16% to 8.58% on the same day. Nothing on the other side offsets that choice, so say which method you used.

L17 tests the first pair on KO: in euros the value is exactly the same, $61.79; mix a euro cash flow with a dollar rate and it moves by over 10%.

# paths · Arguments settled by a path

Where two camps argue over the right number, his answer is usually that one is right now and the other is right eventually, so the input becomes a path over the ten years:

- **Tax**: the effective rate now, the marginal rate by year 10 (D-24).
- **Growth**: the company's high growth now, growth forever by year 10 (D-32).
- **Returns**: an edge now, competition eventually (D-34).
- **Risk**: today's cost of capital now, a mature company's by year 10 (D-32).

L29 traces all of them in his own NVIDIA model, including where he broke the pattern (its return on capital jumps from 114% to 20% instead of falling to the cost of capital).

# effort · Where the effort belongs

> "When I've screwed up on a valuation, and I've screwed up on lots of them, it's almost never because I got the discount rate wrong, it's because I've got the cash flow wrong. We need to shift our focus from discount rates to cash flows."

He estimates a typical valuation spends 80% of its effort on the discount rate (the riskfree rate, the risk premium, beta, the cost of debt) and 20% on the cash flows. But the cash flows (earnings, tax, reinvestment, growth, the terminal value) are where valuations fail.

L18 tests it on his NVIDIA model: putting his old AI market story back moves the value from $77.51 to $101.58 a share; putting his old cost of capital back, only to $83.20. L30 tests it on KO, where the beta turns out to swing the value most, but growth and the moat are the bigger unknowns.
