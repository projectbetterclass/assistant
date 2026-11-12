#!/usr/bin/env python3
"""The investing course's lessons (L01–L34): what each task needs, and a worked answer to check against.

L03–L14 build one valuation of KO; the rest reuse it, and add his own NVIDIA, Paytm and Tesla spreadsheets
(from the youtube-digest library), SEC filings for JPMorgan, NVIDIA, Intel and Tesla, and his history pages.

Every number comes from a place named on the lesson itself:
  * annual reports (Form 10-K) read from SEC EDGAR: KO 2025 (filed 20 Feb 2026), JPMorgan, NVIDIA, Intel, Tesla;
  * Aswath Damodaran's own words and slides, from the youtube-digest library (his 2026 Data Updates and lectures);
  * his January 2026 data pages, where the digest has no copy (marked as such, with the link).
Derived numbers are computed here, not typed, so a change to an input flows through.

Writes the VAL_KO block in time-tracker.html between the VAL_KO:start / VAL_KO:end markers.
    python3 scripts/build-invest-ko.py            # rewrite the block
    python3 scripts/build-invest-ko.py --check    # exit 1 if the block is out of date
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "..", "time-tracker.html")
LIBRARY = os.path.join(HERE, "..", "..", "youtube-digest", "data", "library.json")

def yt(vid): return "https://www.youtube.com/watch?v=" + vid
TENK = "https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm"
BETAS = "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html"
DU2_2026 = ("Damodaran · Data Update 2 for 2026", "BzG8M74BfrY")
DU7_2026 = ("Damodaran · Data Update 7 for 2026: Debt and Taxes", "3X6rah8r4Do")
S12 = ("Damodaran · Session 12: Cracking the Currency Code!", "FXbXksS4kNs")
S6_BETA = ("Damodaran · Session 6: Bottom Up Betas", "AtWeS8b9Igw")

# ---- inputs (each with where it was read) -------------------------------------------------------
# KO 10-K 2025 (XBRL, accession 0001628280-26-010047)
KO_SHARES_M = 4300.723069        # dei:EntityCommonStockSharesOutstanding, 18 Feb 2026 (cover page)
KO_PRICE = 69.91                 # closing price 31 Dec 2025 (Yahoo Finance)
KO_NOTES = 1551                  # us-gaap:NotesAndLoansPayable, $M
KO_LTD = 43941                   # us-gaap:LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities, $M
KO_LTD_FAIR = 39385              # us-gaap:LongTermDebtFairValue, $M
KO_LEASES = 1722                 # us-gaap:OperatingLeaseLiability, $M
# Damodaran, start of 2026 (Data Update 2 for 2026, spoken)
TBOND = 4.18                     # 10-year US Treasury, 1 Jan 2026
US_SPREAD = 0.23                 # default spread for an Aa1 rating (Moody's cut the US from Aaa in 2025)
ERP_GROSS, ERP_NET = 4.23, 4.46  # implied ERP against 4.18%, and against 3.95%
# Damodaran, Data Update 7 for 2026 (spoken): US marginal tax rate "about 25%"
TAX_US = 25.0
# Damodaran, Betas by sector (US), data as of January 2026: Beverage (Soft)
BEV_FIRMS, BEV_BETA, BEV_UNLEV_CASH = 27, 0.64, 0.58
# KO regression beta: 60 monthly returns Jan 2021–Dec 2025 against the S&P 500 (Yahoo adjusted closes)
REG_BETA, REG_SE = 0.39, 0.137

# ---- derived ------------------------------------------------------------------------------------
RF_NET = round(TBOND - US_SPREAD, 2)                       # 3.95
E_M = KO_SHARES_M * KO_PRICE                               # market value of equity, $M
D_M = KO_NOTES + KO_LTD + KO_LEASES                        # debt incl. leases (book), $M
DE = D_M / E_M
BETA_L = BEV_UNLEV_CASH * (1 + (1 - TAX_US / 100) * DE)
assert abs(RF_NET - 3.95) < 1e-9 and abs(ERP_NET - (8.41 - 3.95)) < 0.006 and abs(ERP_GROSS - (8.41 - 4.18)) < 0.006
def b(x): return "$%.1f billion" % (x / 1000)
def pct(x, d=1): return ("%." + str(d) + "f%%") % x

def src(name_vid):
    return {"s": name_vid[0], "u": yt(name_vid[1])}

def M(x): return ("−" if x < 0 else "") + "$" + format(abs(int(round(x))), ",") + " M"
DAM = "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/"
CTRY = "https://pages.stern.nyu.edu/~adamodar/pc/datasets/ctryprem.xlsx"
S5 = ("Damodaran · Session 5: Accounting Inconsistencies", "un6-H_wOizM")
S9 = ("Damodaran · Session 9: Analyst Estimates of Growth & Fundamentals", "LhkalvrWdUU")
S6B = ("Damodaran · Session 6B: Monte Carlo Simulations", "eXhCXobViJc")
CR2018 = ("Damodaran · Country Risk 2018: A Mid-Year Update", "GRPDgtQ_yFY")
S10_DEBT = ("Damodaran · Session 10: Debt and the Cost of Debt", "RNeCC28qbVI")
S11_LOOSE = ("Damodaran · Session 11: Loose Ends in Valuation", "C5ZDAEqQkvA")
S9_TV = ("Damodaran · Session 9: Terminal Value", "83yR6EFEl5Y")
S7_CF = ("Damodaran · Session 7: Estimating Cash Flows", "8gYT3Xgs6NE")

# KO 10-K 2025, income statement and notes ($M)
REV, EBIT, INT_EXP = 47941, 13762, 1654
CHARGES, IMPAIR, PRODUCTIVITY, FAIRLIFE_REMEAS = 1261, 960, 97, 47       # other operating charges and its items
CHARGES_2024, FAIRLIFE_2024, IMPAIR_2024 = 4163, 3109, 760
PRETAX, TAXES, EFF_2024 = 15998, 2861, 18.6
ADVERTISING_B = 5.4
SEG = [  # third-party revenue by operating segment, and the region of Damodaran's table it is matched to
    ("North America", 19579, "North America", "his North America average (US 4.46%, Canada 4.23%)"),
    ("Europe, Middle East & Africa", 10833, "EMEA", "his Western Europe, Eastern Europe, Middle East and Africa averages, weighted by GDP: KO doesn’t split EMEA by country"),
    ("Latin America", 6331, "Central and South America", "his Central and South America average (Mexico 6.69%, Brazil 7.47%)"),
    ("Asia Pacific", 5328, "Asia", "his Asia average"),
    ("Bottling Investments", 5726, "India", "mostly India after the 2024 sales of its Philippines and Bangladesh bottlers; India’s premium"),
]
SEG_TOTAL = 47797
# cash flow and balance sheet ($M)
CAPEX, DA, ACQ, WC_LINE, FAIRLIFE_PAID = 2112, 1050, 461, 7208, 6100
CASH_ST = 13872                    # cash, cash equivalents and short-term investments
LISTED_MKT, LISTED_BOOK, EQM_BOOK = 34286, 13999, 20235
UNLISTED_BOOK = EQM_BOOK - LISTED_BOOK
MINORITY, EQUITY_BOOK = 2106, 32169
OPTIONS_M, OPTIONS_STRIKE = 27, 55.74
RATING_SP, RATING_MOODY = "A+", "A1"
# Damodaran, January 2026 (his data pages and ctryprem.xlsx)
REGION_ERP = {"North America": 4.4465, "Western Europe": 5.2665, "Eastern Europe": 7.5777, "Middle East": 6.2367,
              "Africa": 11.9493, "Central and South America": 8.4628, "Asia": 5.7223, "India": 7.0754}
REGION_GDP = {"Western Europe": 23561725.6, "Eastern Europe": 3491477.2, "Middle East": 3565018.3, "Africa": 2340875.2}
MATURE_ERP = round(ERP_NET - US_SPREAD, 2)                 # 4.23: ERP for the US less its default spread (his 2026 note)
RATINGS = [(8.5, "Aaa/AAA", 0.40), (6.5, "Aa2/AA", 0.55), (5.5, "A1/A+", 0.70), (4.25, "A2/A", 0.78), (3.0, "A3/A-", 0.89)]
BEV_WACC, BEV_COE, BEV_ROC, BEV_RR, BEV_G = 6.33, 6.81, 29.03, 33.93, 9.85
BEV_S2C, BEV_NETCAPEX_S, BEV_MARGIN, BEV_TAX = 1.54, 4.69, 20.63, 19.75

# ---- derived for L04–L14 --------------------------------------------------------------------------
ws = sum(REGION_GDP.values())
REGION_ERP["EMEA"] = sum(REGION_ERP[k] * v for k, v in REGION_GDP.items()) / ws
assert sum(s[1] for s in SEG) == SEG_TOTAL
KO_ERP = sum(r * REGION_ERP[reg] for _, r, reg, _ in SEG) / SEG_TOTAL
COE = RF_NET + BETA_L * KO_ERP
COV = EBIT / INT_EXP
def rate(cov):
    for lo, name, sp in RATINGS:
        if cov >= lo: return name, sp
SYN_RATING, SYN_SPREAD = rate(COV)
ACT_SPREAD = [sp for lo, n, sp in RATINGS if n.endswith("/" + RATING_SP)][0]
KD = RF_NET + SYN_SPREAD
KD_AT = KD * (1 - TAX_US / 100)
WE, WD = E_M / (E_M + D_M), D_M / (E_M + D_M)
WACC = WE * COE + WD * KD_AT
def wacc_with(spread=None, debt=None):
    d = D_M if debt is None else debt
    kd = (RF_NET + (SYN_SPREAD if spread is None else spread)) * (1 - TAX_US / 100)
    bl = BEV_UNLEV_CASH * (1 + (1 - TAX_US / 100) * d / E_M)
    return (E_M * (RF_NET + bl * KO_ERP) + d * kd) / (E_M + d)
WACC_ACT = wacc_with(spread=ACT_SPREAD)
WACC_NOLEASE = wacc_with(debt=D_M - KO_LEASES)
WBE = EQUITY_BOOK / (EQUITY_BOOK + D_M)
WACC_BOOK = WBE * COE + (1 - WBE) * KD_AT
EBIT_CLEAN = EBIT + IMPAIR + FAIRLIFE_REMEAS
EFF = TAXES / PRETAX * 100
EBIT_AT = EBIT_CLEAN * (1 - EFF / 100)
NETCAPEX = CAPEX - DA + ACQ
RR = NETCAPEX / EBIT_AT
IC = EQUITY_BOOK + MINORITY + D_M - CASH_ST - EQM_BOOK
ROC = EBIT_AT / IC
G = RR * ROC                                         # fundamental growth, a fraction
REINV_S2C = (REV - 47061) / BEV_S2C

def dcf(g=None, roc_term=None, wacc=None, taxpath=True, clean=True):
    """Ten years at growth g with reinvestment g/ROC, the tax rate walking from the effective rate (years 1–5) to the
    marginal rate by year 10, then a terminal value with growth g and return on capital roc_term. Returns (value, tv share)."""
    g = G if g is None else g; roc_term = ROC if roc_term is None else roc_term; w = (WACC if wacc is None else wacc) / 100
    e = EBIT_CLEAN if clean else EBIT
    pv, ebit = 0.0, e
    for y in range(1, 11):
        ebit *= 1 + g
        t = EFF if (y <= 5 or not taxpath) else EFF + (TAX_US - EFF) * (y - 5) / 5
        fcff = ebit * (1 - t / 100) * (1 - g / ROC)
        pv += fcff / (1 + w) ** y
    t_term = TAX_US if taxpath else EFF
    fcff11 = ebit * (1 + g) * (1 - t_term / 100) * (1 - g / roc_term)
    tv = fcff11 / (w - g)
    pvtv = tv / (1 + w) ** 10
    return pv + pvtv, pvtv / (pv + pvtv)
OPS_MOAT, TVS_MOAT = dcf()                                    # return on capital stays at today's
OPS_NOMOAT, TVS_NOMOAT = dcf(roc_term=WACC / 100)            # return on capital falls to the cost of capital
OPS_FLAT, _ = dcf(taxpath=False)
OPS_RAW, _ = dcf(clean=False)
OPTIONS_VAL = OPTIONS_M * (KO_PRICE - OPTIONS_STRIKE)
CROSS = LISTED_MKT + UNLISTED_BOOK
def per_share(ops):
    return (ops + CASH_ST + CROSS - D_M - MINORITY - OPTIONS_VAL) / KO_SHARES_M
VPS_MOAT, VPS_NOMOAT = per_share(OPS_MOAT), per_share(OPS_NOMOAT)
SENS = {   # value per share when one input moves, the rest at the moat case
    "growth ±1 point": (per_share(dcf(g=G - 0.01)[0]), per_share(dcf(g=G + 0.01)[0])),
    "return on capital forever: cost of capital vs today’s": (VPS_NOMOAT, VPS_MOAT),
    "cost of capital ±0.5 point": (per_share(dcf(wacc=WACC + 0.5)[0]), per_share(dcf(wacc=WACC - 0.5)[0])),
}
def usd(x): return "$%.2f" % x

L = {}
L["L03"] = {
    "teach": "Currency is a unit of measurement, not a bet. Value a company in dollars or in euros and, done consistently, you get the same answer, because inflation enters both the cash flows and the discount rate. So pick the currency you have clean data for and stay in it. A riskfree rate needs two things: no default risk and no reinvestment risk, with a duration that fits the cash flows. For a going concern in dollars that is today’s 10-year Treasury rate, not an average or a ‘normal’ rate. Since Moody’s cut the US to Aa1 in 2025, he nets the US default spread out too: at the start of 2026, %s less %s, which leaves %s. When the government can default, its bond rate is not riskfree: subtract the sovereign default spread, taken from a dollar bond, the credit default swap or the rating. Aswath’s Brazil example: a 12.3%% government bond less a 2.82%% spread leaves 9.48%%." % (pct(TBOND, 2), pct(US_SPREAD, 2), pct(RF_NET, 2)),
    "task": "KO reports in dollars and sells in about 200 countries. Using the numbers in What you need, pick the currency and the riskfree rate for a KO valuation, and say what you’d do in a currency whose government isn’t default-free. Then judge: which choice could move the value more — the currency or the rate? Check D-02–D-04.",
    "need": [
        {"k": "The currency KO reports in", "v": "US dollars", "n": "Its 2025 annual report is in dollars, so its cash flows are.", "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "10-year US Treasury rate, 1 Jan 2026", "v": pct(TBOND, 2), **src(DU2_2026)},
        {"k": "Default spread of the US (Moody’s Aa1)", "v": pct(US_SPREAD, 2), "n": "Moody’s took the US’s last AAA away in 2025.", **src(DU2_2026)},
        {"k": "Riskfree rate in dollars, spread netted out", "v": pct(RF_NET, 2), "n": "%s − %s. His choice for 2026." % (pct(TBOND, 2), pct(US_SPREAD, 2)), **src(DU2_2026)},
    ],
    "needNote": "Every KO lesson uses these same numbers, so each answer can be checked.",
    "key": [
        {"t": "Worked answer: his method, KO’s numbers",
         "l": ["Currency: US dollars, the currency KO reports in. Inflation is then the same in the cash flows and the discount rate.",
               "Riskfree rate: %s, the %s Treasury rate less the US’s %s default spread, as he did for 2026. If you use %s instead, that’s defensible too, but pair it with his %s risk premium, not %s (lesson L04)." % (pct(RF_NET, 2), pct(TBOND, 2), pct(US_SPREAD, 2), pct(TBOND, 2), pct(ERP_GROSS, 2), pct(ERP_NET, 2)),
               "Today’s rate, not an average: the valuation is as of today.",
               "A currency whose government can default: take its local 10-year bond rate and subtract the sovereign default spread (Brazil in his example: 12.3% − 2.82% = 9.48%).",
               "Which moves value more: the rate. A consistent currency choice cancels out; a wrong riskfree rate doesn’t."],
         **src(DU2_2026)},
        {"t": "His own test question (Session 12)",
         "l": ["Q: One company borrows for the same project in two currencies at different rates. What is the biggest reason the rates differ?",
               "His answer: expected inflation. Same company, same project, same risk, so inflation is all that’s left. That is why the currency doesn’t change the value."],
         **src(S12)},
    ],
}
L["L05"] = {
    "task": "Using the numbers in What you need, build KO’s bottom-up beta: its business, that industry’s unlevered beta, KO’s debt-to-equity and the tax rate. Then set it beside KO’s regression beta, decide which you’d trust, and name the one situation where the regression would be defensible. Check D-09–D-12.",
    "need": [
        {"k": "KO’s business", "v": "Soft drinks", "n": "One business: Damodaran’s ‘Beverage (Soft)’ industry.", "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Unlevered beta, soft drinks (corrected for cash)", "v": "%.2f" % BEV_UNLEV_CASH, "n": "%d US companies; their average levered beta is %.2f. Data as of January 2026." % (BEV_FIRMS, BEV_BETA), "s": "Damodaran · Betas by sector, January 2026", "u": BETAS},
        {"k": "KO’s equity, market value (31 Dec 2025)", "v": b(E_M), "n": "%s million shares × $%.2f." % (format(round(KO_SHARES_M, 1), ",.1f"), KO_PRICE), "s": "KO 10-K cover (shares) · closing price 31 Dec 2025", "u": TENK},
        {"k": "KO’s debt, leases included", "v": b(D_M), "n": "Loans and notes $%s M + long-term debt $%s M + operating leases $%s M. (The bonds’ market value is $%s M.)" % (format(KO_NOTES, ","), format(KO_LTD, ","), format(KO_LEASES, ","), format(KO_LTD_FAIR, ",")), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Marginal tax rate, US", "v": pct(TAX_US, 0), **src(DU7_2026)},
        {"k": "KO’s regression beta (5 years, monthly)", "v": "%.2f" % REG_BETA, "n": "Against the S&P 500, 2021–2025. Standard error %.2f." % REG_SE, "s": "Computed from Yahoo Finance prices", "u": "https://finance.yahoo.com/quote/KO/history/"},
    ],
    "key": [
        {"t": "Worked answer: his method, KO’s numbers",
         "l": ["Business: soft drinks, so start from the industry’s unlevered beta, %.2f." % BEV_UNLEV_CASH,
               "Debt-to-equity: %s ÷ %s = %s." % (b(D_M), b(E_M), pct(DE * 100, 1)),
               "Relever: %.2f × (1 + (1 − %.2f) × %.3f) = %.2f." % (BEV_UNLEV_CASH, TAX_US / 100, DE, BETA_L),
               "Regression beta: %.2f, but with a standard error of %.2f the true value could be anywhere from about %.2f to %.2f. Use the bottom-up %.2f." % (REG_BETA, REG_SE, REG_BETA - 2 * REG_SE, REG_BETA + 2 * REG_SE, BETA_L),
               "When a regression is defensible: a company with no comparable firms to average and a long, stable history in one business, and even then check it against a bottom-up beta."],
         "s": "His method: " + S6_BETA[0], "u": yt(S6_BETA[1])},
        {"t": "His own example (movie studios)",
         "l": ["Average regression beta of movie companies: 1.24. Median debt-to-equity: 27% (the average, 129%, was skewed by one firm near bankruptcy).",
               "Unlevered: 1.03. Movie companies hold about 3% cash, so 1.03 ÷ 0.97 ≈ 1.06 for the movie business alone."],
         **src(S6_BETA)},
    ],
}

L["L04"] = {
    "teach": "The equity risk premium is the extra return investors want for owning stocks instead of the riskfree asset. Start from the implied premium, the return that makes the index’s expected cash flows worth today’s level, not a historical average, which depends on the years you pick and looks backward. At the start of 2026 the S&P 500 priced in an expected return of 8.41%%: %s above his %s riskfree rate. Because the US itself now carries a %s default spread, he takes the mature-market premium as %s less %s, which is %s. A market that isn’t mature adds a country risk premium on top. A company’s exposure comes from where it does business, not where it is incorporated, so weight the premiums by where its revenue comes from. Coca-Cola is based in Atlanta, but most of what it sells is sold outside the US." % (pct(ERP_NET, 2), pct(RF_NET, 2), pct(US_SPREAD, 2), pct(ERP_NET, 2), pct(US_SPREAD, 2), pct(MATURE_ERP, 2)),
    "task": "Using the numbers in What you need, give KO an equity risk premium: start from the mature-market premium, then add country risk by where KO sells, not where it is based. Then judge: which of these inputs would you fight hardest to get right, and why? Check D-05–D-08.",
    "need": [
        {"k": "Implied premium, US (1 Jan 2026)", "v": pct(ERP_NET, 2), "n": "8.41%% expected return on the S&P 500, less the %s riskfree rate." % pct(RF_NET, 2), **src(DU2_2026)},
        {"k": "Mature-market premium", "v": pct(MATURE_ERP, 2), "n": "The US premium less the US default spread (%s). What a country with no default risk adds." % pct(US_SPREAD, 2), "s": "Damodaran · Country risk premiums, January 2026", "u": DAM + "ctryprem.html"},
    ] + [
        {"k": "%s (%d%% of revenue)" % (name, round(r / SEG_TOTAL * 100)), "v": pct(REGION_ERP[reg], 2), "n": "%s of 2025 revenue; %s." % (M(r), why), "s": "KO 10-K 2025 · Damodaran’s regional premiums, January 2026", "u": CTRY}
        for name, r, reg, why in SEG
    ],
    "needNote": "Premiums are his GDP-weighted regional averages from his January 2026 country-risk spreadsheet. Each region’s premium already includes the mature %s." % pct(MATURE_ERP, 2),
    "key": [
        {"t": "Worked answer: his method, KO’s numbers",
         "l": ["Weight each region’s premium by its share of KO’s revenue: %s." % " + ".join("%d%% × %s" % (round(r / SEG_TOTAL * 100), pct(REGION_ERP[reg], 2)) for _, r, reg, _ in SEG),
               "KO’s equity risk premium: %s. Using Atlanta alone would give %s, too low for a company that sells %d%% of its drinks outside North America." % (pct(KO_ERP, 2), pct(ERP_NET, 2), round((1 - SEG[0][1] / SEG_TOTAL) * 100)),
               "Fight hardest for the mature-market premium: it sits under every dollar of revenue. A 0.5-point change in it moves KO’s premium by 0.5 points; re-labelling one region (say Latin America at Mexico’s 6.69%% instead of %s) moves it by only %s." % (pct(REGION_ERP["Central and South America"], 2), pct((REGION_ERP["Central and South America"] - 6.6950) * SEG[2][1] / SEG_TOTAL, 2)),
               "Then the regional mix, because it changes as KO sells more in riskier places."],
         "s": "Damodaran · Country risk premiums, January 2026", "u": CTRY},
        {"t": "His own Coca-Cola example (2018 numbers)",
         "l": ["Coca-Cola’s beta 0.80, riskfree 3%. A project in Nigeria: 3% + 0.80 × 13.15% = 13.52%. In Chile: 3% + 0.80 × 6.22% = 7.98%. In the US: 3% + 0.80 × 5.37% = 7.30%.",
               "Same business, same currency, different country risk, different hurdle rate. Using one rate everywhere would make Coca-Cola over-invest in its riskiest markets."],
         **src(CR2018)},
    ],
}
L["L06"] = {
    "task": "Using the numbers in What you need, give KO a cost of debt from a synthetic rating (interest coverage), check it against KO’s actual rating, add its leases to debt, and decide whether a country default burden applies. Judge: does the rating or the leases move KO’s cost of capital more? Check D-13–D-15.",
    "need": [
        {"k": "Operating income 2025", "v": M(EBIT), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Interest expense 2025", "v": M(INT_EXP), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "His table, large companies: coverage above 8.50", "v": "AAA · 0.40%", "s": "Damodaran · Ratings and spreads, January 2026", "u": DAM + "ratings.html"},
        {"k": "Coverage 6.50 to 8.50", "v": "AA · 0.55%", "s": "Damodaran · Ratings and spreads, January 2026", "u": DAM + "ratings.html"},
        {"k": "Coverage 5.50 to 6.50", "v": "A+ · 0.70%", "s": "Damodaran · Ratings and spreads, January 2026", "u": DAM + "ratings.html"},
        {"k": "KO’s actual rating", "v": "%s (S&P) · %s (Moody’s)" % (RATING_SP, RATING_MOODY), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Riskfree rate (from L03)", "v": pct(RF_NET, 2), **src(DU2_2026)},
        {"k": "Operating leases", "v": M(KO_LEASES), "n": "Already on KO’s balance sheet, discounted at 3.9%.", "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Marginal tax rate", "v": pct(TAX_US, 0), **src(DU7_2026)},
    ],
    "key": [
        {"t": "Worked answer: his method, KO’s numbers",
         "l": ["Interest coverage: %s ÷ %s = %.2f, which his table rates %s, a %s default spread." % (M(EBIT), M(INT_EXP), COV, SYN_RATING.split("/")[1], pct(SYN_SPREAD, 2)),
               "Pre-tax cost of debt: %s + %s = %s. After tax: %s × (1 − 0.25) = %s." % (pct(RF_NET, 2), pct(SYN_SPREAD, 2), pct(KD, 2), pct(KD, 2), pct(KD_AT, 2)),
               "Check: KO’s actual %s rating carries %s, so %s before tax. He prefers an actual rating when one exists; the two are close here.%s" % (RATING_SP, pct(ACT_SPREAD, 2), pct(RF_NET + ACT_SPREAD, 2), " With the one-off charges added back (L08), coverage is %.2f, an AAA." % (EBIT_CLEAN / INT_EXP)),
               "Leases: add the %s to debt, so debt is %s." % (M(KO_LEASES), b(D_M)),
               "No country default burden: KO borrows in dollars as a US company, with earnings spread over many countries.",
               "Which moves the cost of capital more: the rating. AA versus A+ moves it by %.3f points; leaving the leases out moves it by %.3f. Both are tiny for KO, because debt is only %s of its capital." % (abs(WACC_ACT - WACC), abs(WACC_NOLEASE - WACC), pct(WD * 100, 1))],
         "s": "His method: " + S10_DEBT[0], "u": yt(S10_DEBT[1])},
        {"t": "His own test question (Session 5)",
         "l": ["Q: To convert leases to debt, which rate do you discount the lease commitments at?",
               "His answer: the pre-tax cost of debt. The commitments are pre-tax and are debt commitments."],
         **src(S5)},
    ],
}
L["L07"] = {
    "task": "Using the numbers in What you need, weight KO’s equity and debt at market values and put its cost of capital together. Set it beside book-value weights and his soft-drinks average. Judge: would one company-wide number be wrong for a company with very different businesses — and is KO one of those? Check D-16–D-18.",
    "need": [
        {"k": "Cost of equity (L03–L05)", "v": pct(COE, 2), "n": "%s + %.2f × %s." % (pct(RF_NET, 2), BETA_L, pct(KO_ERP, 2))},
        {"k": "After-tax cost of debt (L06)", "v": pct(KD_AT, 2)},
        {"k": "Equity at market value", "v": b(E_M), "s": "KO 10-K cover (shares) · closing price 31 Dec 2025", "u": TENK},
        {"k": "Debt, leases included", "v": b(D_M), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Equity at book value", "v": b(EQUITY_BOOK), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "His soft-drinks cost of capital", "v": pct(BEV_WACC, 2), "n": "27 US companies, January 2026, with the US premium for all of them.", "s": "Damodaran · Cost of capital by sector, January 2026", "u": DAM + "wacc.html"},
    ],
    "key": [
        {"t": "Worked answer: his method, KO’s numbers",
         "l": ["Weights at market value: equity %s, debt %s." % (pct(WE * 100, 1), pct(WD * 100, 1)),
               "Cost of capital: %s × %s + %s × %s = %s." % (pct(WE * 100, 1), pct(COE, 2), pct(WD * 100, 1), pct(KD_AT, 2), pct(WACC, 2)),
               "At book weights (equity %s) it would be %s: book equity is an accounting leftover that says nothing about what investors own today." % (pct(WBE * 100, 1), pct(WACC_BOOK, 2)),
               "Higher than his soft-drinks %s because KO sells far outside the US: its premium is %s, not %s." % (pct(BEV_WACC, 2), pct(KO_ERP, 2), pct(ERP_NET, 2)),
               "One number is right for KO: it is one business, selling drinks. Bottling Investments (%d%% of revenue) is the one part with a different risk and margin; you’d give it its own rate only if you valued it separately." % round(SEG[4][1] / SEG_TOTAL * 100)],
         "s": "Damodaran · Cost of capital by sector, January 2026", "u": DAM + "wacc.html"},
    ],
}
L["L08"] = {
    "task": "Using the numbers in What you need, clean KO’s 2025 operating income: one-off charges, anything to capitalise, anything to normalise. Judge: which cleanup moves KO’s base year most — and which would matter more for a company with negative earnings? Check D-19–D-22.",
    "need": [
        {"k": "Operating income 2025, as reported", "v": M(EBIT), "n": "On revenue of %s: a %s margin." % (M(REV), pct(EBIT / REV * 100, 1)), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Other operating charges 2025", "v": M(CHARGES), "n": "Inside it: %s impairment of the BodyArmor brand (%s in 2024 too), %s for the productivity programme (it runs every year), %s re-valuing what KO still owed for fairlife, and smaller items." % (M(IMPAIR), M(IMPAIR_2024), M(PRODUCTIVITY), M(FAIRLIFE_REMEAS)), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "The same charges in 2024", "v": M(CHARGES_2024), "n": "%s of it re-valuing the fairlife payment." % M(FAIRLIFE_2024), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Research and development", "v": "not reported", "n": "KO has no R&D line. Its big brand spend is advertising: $%.1f billion in 2025." % ADVERTISING_B, "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "His soft-drinks operating margin", "v": pct(BEV_MARGIN, 2), "n": "Pre-tax, lease-adjusted, January 2026.", "s": "Damodaran · Margins by sector, January 2026", "u": DAM + "margin.html"},
    ],
    "key": [
        {"t": "Worked answer: his method, KO’s numbers",
         "l": ["Add back the %s BodyArmor impairment: writing down a past acquisition is a loss of capital, not this year’s cost of running the business, even when it happens two years running." % M(IMPAIR),
               "Add back the %s fairlife re-valuation: it is about the price of an acquisition, not operations." % M(FAIRLIFE_REMEAS),
               "Keep the %s productivity charge: it comes back every year, so it is a cost." % M(PRODUCTIVITY),
               "Nothing to capitalise: no R&D. Advertising builds the brand, but he doesn’t capitalise it by default. Leases are already on the balance sheet.",
               "Clean operating income: %s, a %s margin, against %s for soft drinks as a whole." % (M(EBIT_CLEAN), pct(EBIT_CLEAN / REV * 100, 1), pct(BEV_MARGIN, 2)),
               "Biggest mover: the impairment (+%s of the base year). For a company with negative earnings, normalising matters far more: you’d replace this year’s loss with a target margin." % pct(IMPAIR / EBIT * 100, 1)],
         "s": "His method: " + S5[0], "u": yt(S5[1])},
        {"t": "His own test question (Session 5)",
         "l": ["Q: Why does accounting treat R&D as an operating expense rather than a capital expense?",
               "His answer: because the benefits are too uncertain. He disagrees: R&D builds an asset, so in a valuation he capitalises it."],
         **src(S5)},
    ],
}
L["L09"] = {
    "task": "Using the numbers in What you need, choose KO’s tax rate now and at the end, and say how they converge. Does KO have losses carried forward to use up? Judge: does the tax path or the base-year cleanup move KO’s value more? Check D-23–D-25.",
    "need": [
        {"k": "Effective tax rate 2025", "v": pct(EFF, 1), "n": "Taxes %s ÷ profit before tax %s. It was %s in 2024." % (M(TAXES), M(PRETAX), pct(EFF_2024, 1)), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "US federal statutory rate", "v": "21%", "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Marginal tax rate, US", "v": pct(TAX_US, 0), "n": "Federal plus state.", **src(DU7_2026)},
        {"k": "His soft-drinks effective rate", "v": pct(BEV_TAX, 2), "n": "Money-making companies, aggregate, January 2026.", "s": "Damodaran · Tax rates by sector, January 2026", "u": DAM + "taxrate.html"},
    ],
    "key": [
        {"t": "Worked answer: his method, KO’s numbers",
         "l": ["Years 1–5: the effective %s. Years 6–10: up in five equal steps of %.2f points to %s. Forever after: %s." % (pct(EFF, 1), (TAX_US - EFF) / 5, pct(TAX_US, 0), pct(TAX_US, 0)),
               "Tax the operating income as if KO had no debt; the interest saving is already in the after-tax cost of debt.",
               "No losses carried forward that matter, so no tax holiday in the early years.",
               "In the worked KO model (L12): the tax path takes %s off the operating value compared with %s forever; the base-year cleanup adds %s. Close, but the cleanup moves it a little more." % (pct((1 - OPS_MOAT / OPS_FLAT) * 100, 1), pct(EFF, 1), pct((OPS_MOAT / OPS_RAW - 1) * 100, 1))],
         **src(DU7_2026)},
    ],
}
L["L10"] = {
    "task": "Using the numbers in What you need, build KO’s reinvestment from net capex, acquisitions and working capital. Then do it the other way, from sales-to-capital. Decide which fits KO — and when you’d switch, with NVIDIA in mind. Check D-26–D-29.",
    "need": [
        {"k": "Capital expenditure 2025", "v": M(CAPEX), "s": "KO cash flow statement 2025", "u": TENK},
        {"k": "Depreciation and amortisation", "v": M(DA), "s": "KO cash flow statement 2025", "u": TENK},
        {"k": "Acquisitions", "v": M(ACQ), "n": "Businesses, equity stakes and other investments bought.", "s": "KO cash flow statement 2025", "u": TENK},
        {"k": "Working capital line 2025", "v": M(-WC_LINE), "n": "Distorted: it includes about $6.1 billion KO paid for fairlife in March 2025, a one-off.", "s": "KO cash flow statement 2025", "u": TENK},
        {"k": "Revenue growth 2025", "v": M(REV - 47061), "n": "From %s to %s." % (M(47061), M(REV)), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "His soft-drinks sales-to-capital", "v": "%.2f" % BEV_S2C, "n": "Each dollar of capital supports $%.2f of revenue. January 2026." % BEV_S2C, "s": "Damodaran · Capital expenditures by sector, January 2026", "u": DAM + "capex.html"},
    ],
    "key": [
        {"t": "Worked answer: his method, KO’s numbers",
         "l": ["Net capex: %s − %s + %s = %s." % (M(CAPEX), M(DA), M(ACQ), M(NETCAPEX)),
               "Working capital: leave 2025’s line out; the fairlife payment swamps it. For a mature company, small and in line with revenue.",
               "Reinvestment ≈ %s, %s of after-tax operating income (%s)." % (M(NETCAPEX), pct(RR * 100, 1), M(EBIT_AT)),
               "From sales-to-capital: %s of extra revenue ÷ %.2f = %s." % (M(REV - 47061), BEV_S2C, M(REINV_S2C)),
               "For KO, the net-capex route fits: it is mature, and its past spending is a fair guide. For a young company like NVIDIA, whose growth ahead dwarfs anything behind it, switch to sales-to-capital and tie the spending to the growth you assume."],
         "s": "His method: " + S7_CF[0], "u": yt(S7_CF[1])},
    ],
}
L["L11"] = {
    "task": "Using the numbers in What you need, derive KO’s growth from reinvestment rate × return on capital. Set it beside his soft-drinks figure and decide which goes in the model — and why analysts’ forecasts aren’t an input. Judge: how fast should KO’s growth fade, and what decides that? Check D-30–D-32.",
    "need": [
        {"k": "After-tax operating income (L08, L09)", "v": M(EBIT_AT), "n": "%s × (1 − %s)." % (M(EBIT_CLEAN), pct(EFF, 1))},
        {"k": "Reinvestment (L10)", "v": M(NETCAPEX)},
        {"k": "Invested capital", "v": M(IC), "n": "Equity %s + minority %s + debt %s − cash %s − equity stakes %s (their income isn’t in operating income)." % (M(EQUITY_BOOK), M(MINORITY), M(D_M), M(CASH_ST), M(EQM_BOOK)), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "His soft-drinks numbers", "v": "%s × %s = %s" % (pct(BEV_RR, 1), pct(BEV_ROC, 1), pct(BEV_G, 2)), "n": "Reinvestment rate × return on capital = expected growth, January 2026.", "s": "Damodaran · Fundamental growth by sector, January 2026", "u": DAM + "fundgrEB.html"},
    ],
    "key": [
        {"t": "Worked answer: his method, KO’s numbers",
         "l": ["Return on capital: %s ÷ %s = %s." % (M(EBIT_AT), M(IC), pct(ROC * 100, 1)),
               "Reinvestment rate: %s ÷ %s = %s." % (M(NETCAPEX), M(EBIT_AT), pct(RR * 100, 1)),
               "Growth: %s × %s = %s a year." % (pct(RR * 100, 1), pct(ROC * 100, 1), pct(G * 100, 2)),
               "That, not the industry’s %s: KO reinvests far less than the average soft-drinks company. Analysts’ forecasts are a cross-check only: they look a few years out, follow each other and echo management." % pct(BEV_G, 2),
               "Fade: KO is already growing at about the riskfree rate (%s), so there is almost nothing to fade. A company growing at 20%% would step down over years 6–10." % pct(RF_NET, 2)],
         "s": "Damodaran · Fundamental growth by sector, January 2026", "u": DAM + "fundgrEB.html"},
        {"t": "His own test question (Session 9)",
         "l": ["Q: A toy company earns $50 M after tax on $400 M of equity plus $250 M of debt, less $150 M of cash. It spends $75 M on capex against $30 M of depreciation, and working capital falls by $5 M. Expected growth?",
               "His answer: 8%. Return on capital 50 ÷ (400 + 250 − 150) = 10%; reinvestment (75 − 30 − 5) ÷ 50 = 80%; 10% × 80% = 8%."],
         **src(S9)},
    ],
}
L["L12"] = {
    "task": "Using the numbers in What you need, set KO’s growth forever and its return on capital forever under his two caps (growth no higher than the riskfree rate; return on capital falls to the cost of capital unless KO has a moat). Judge: what share of KO’s value sits in the terminal value — and why that number deserves most of your care? Check D-33–D-35.",
    "need": [
        {"k": "Riskfree rate: the cap on growth (L03)", "v": pct(RF_NET, 2), **src(DU2_2026)},
        {"k": "KO’s growth (L11)", "v": pct(G * 100, 2)},
        {"k": "Cost of capital (L07)", "v": pct(WACC, 2)},
        {"k": "Return on capital today (L11)", "v": pct(ROC * 100, 1)},
        {"k": "Tax path (L09)", "v": "%s → %s" % (pct(EFF, 1), pct(TAX_US, 0))},
    ],
    "needNote": "The worked model in the answer uses only these numbers: ten years at KO’s growth, then growth forever at the same rate. One defensible set of choices, not a forecast.",
    "key": [
        {"t": "Worked answer: his method, KO’s numbers",
         "l": ["Growth forever: %s, KO’s own growth, already under the %s cap." % (pct(G * 100, 2), pct(RF_NET, 2)),
               "Return on capital forever, two cases. With a moat (the brand holds it at %s): reinvest %s ÷ %s = %s of earnings. Without one (it falls to %s): reinvest %s." % (pct(ROC * 100, 1), pct(G * 100, 2), pct(ROC * 100, 1), pct(G / ROC * 100, 1), pct(WACC, 2), pct(G / (WACC / 100) * 100, 1)),
               "Operating value: %s with the moat, %s without." % (b(OPS_MOAT), b(OPS_NOMOAT)),
               "Terminal value’s share: %s with the moat, %s without. Most of KO’s value is in the years after year 10." % (pct(TVS_MOAT * 100, 0), pct(TVS_NOMOAT * 100, 0)),
               "Why it deserves the most care: growth forever and return on capital forever set most of the value, so each needs a written reason. The moat question alone is worth %s a share." % usd(VPS_MOAT - VPS_NOMOAT)],
         "s": "His method: " + S9_TV[0], "u": yt(S9_TV[1])},
    ],
}
L["L13"] = {
    "task": "Using the numbers in What you need, go from KO’s operating value to its equity: cash, cross-holdings, all of its debt, the minority interest and employee options. Decide how each enters, then judge which loose end moves KO’s value per share most. Check D-36–D-40.",
    "need": [
        {"k": "Cash and short-term investments", "v": M(CASH_ST), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Listed stakes, at market prices", "v": M(LISTED_MKT), "n": "Monster, Coca-Cola Europacific, FEMSA, HBC, Bottlers Japan, İçecek, Andina. On KO’s books at %s." % M(LISTED_BOOK), "s": "KO annual report 2025 (10-K), equity method note", "u": TENK},
        {"k": "Other equity stakes, at book", "v": M(UNLISTED_BOOK), "n": "No market price for these.", "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Debt, leases included", "v": M(D_M), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Minority interest (book)", "v": M(MINORITY), "n": "Outsiders’ share of subsidiaries KO consolidates.", "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Employee options", "v": "%d M at $%.2f" % (OPTIONS_M, OPTIONS_STRIKE), "n": "Average exercise price; the share price was $%.2f." % KO_PRICE, "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Shares outstanding", "v": "%s M" % format(round(KO_SHARES_M, 1), ",.1f"), "s": "KO 10-K cover", "u": TENK},
    ],
    "key": [
        {"t": "Worked answer: his method, KO’s numbers",
         "l": ["Add cash at face value: %s (%s a share). Cash is cash." % (M(CASH_ST), usd(CASH_ST / KO_SHARES_M)),
               "Add the stakes at market where there is a price: %s + %s = %s (%s a share). Their income isn’t in operating income, so they’re valued separately." % (M(LISTED_MKT), M(UNLISTED_BOOK), M(CROSS), usd(CROSS / KO_SHARES_M)),
               "Subtract all the debt: %s (%s a share), and the minority interest: %s." % (M(D_M), usd(D_M / KO_SHARES_M), M(MINORITY)),
               "Subtract the options: at least their exercise value, %d M × ($%.2f − $%.2f) = %s. He’d value them as options, a little more. Then divide by the actual %s M shares, not a diluted count." % (OPTIONS_M, KO_PRICE, OPTIONS_STRIKE, M(OPTIONS_VAL), format(round(KO_SHARES_M), ",")),
               "Biggest judgement: the stakes. At market they add %s a share; at book (%s) only %s. Control: no value here, since nobody expects KO to be run very differently."
               % (usd(CROSS / KO_SHARES_M), M(EQM_BOOK), usd(EQM_BOOK / KO_SHARES_M))],
         "s": "His method: " + S11_LOOSE[0], "u": yt(S11_LOOSE[1])},
    ],
}
L["L14"] = {
    "task": "Using the numbers in What you need, turn the KO inputs into a value per share — then into a range, not a point. Decide which three inputs drive the spread. Compare with KO’s price and name the game you’re playing: valuing, or pricing? Check D-41–D-42.",
    "need": [
        {"k": "Operating value (L12)", "v": "%s or %s" % (b(OPS_MOAT), b(OPS_NOMOAT)), "n": "With and without a moat."},
        {"k": "Cash + stakes − debt − minority − options (L13)", "v": b(CASH_ST + CROSS - D_M - MINORITY - OPTIONS_VAL)},
        {"k": "Shares outstanding", "v": "%s M" % format(round(KO_SHARES_M, 1), ",.1f"), "s": "KO 10-K cover", "u": TENK},
        {"k": "KO’s price, 31 Dec 2025", "v": "$%.2f" % KO_PRICE, "s": "Yahoo Finance", "u": "https://finance.yahoo.com/quote/KO/history/"},
    ],
    "key": [
        {"t": "Worked answer: his method, KO’s numbers",
         "l": ["Value per share: %s with the moat, %s without, against a price of $%.2f." % (usd(VPS_MOAT), usd(VPS_NOMOAT), KO_PRICE)]
              + ["%s: %s to %s a share." % (k[0].upper() + k[1:], usd(lo), usd(hi)) for k, (lo, hi) in SENS.items()]
              + ["Those three drive the spread: growth, return on capital forever and the cost of capital. Put ranges on them and let a simulation run, rather than trusting one number.",
                 "On these numbers the market pays more than the value. For the market to be right, KO would have to grow faster than its reinvestment supports, or deserve a lower cost of capital. Valuing is asking what it is worth; pricing is asking what others pay for similar drinks companies. Know which game you’re in."],
         "s": "His method: " + S6B[0], "u": yt(S6B[1])},
        {"t": "His own test question (Session 6B)",
         "l": ["Q: Which inputs should you give distributions to in a simulation?",
               "His answer: the ones that move the output most when they change, and where you are most uncertain about the future."],
         **src(S6B)},
    ],
}

# =================================================================================================
# The rest of the course: L01, L02 and L15–L34. Same rule: every number is read from a named source
# or computed here from one.
# =================================================================================================
def edgar(cik): return "https://www.sec.gov/edgar/browse/?CIK=%d" % cik
def yahoo(t): return "https://finance.yahoo.com/quote/%s/history/" % t
def B(x, d=1): return ("−" if x < 0 else "") + "$" + format(round(abs(x) / 1000, d), ",." + str(d) + "f") + " billion"
def spct(x, d=0): return ("−" if x < 0 else "+") + pct(abs(x), d)
BLOG = "https://pages.stern.nyu.edu/~adamodar/pc/blog/"
DECLINE = ("Damodaran · Dealing with Decline: Intel, Walgreens and Starbucks", "g3VT_cclr4U")
BANKS = ("Damodaran · Good (Bad) Banks and Good (Bad) Investments", "CdhTVs36z4c")
NARRATIVE = ("Damodaran · Narrative and Numbers: A number cruncher learns to tell stories", "5DEhvVjWOEc")
S5_IMPL = ("Damodaran · Session 5: Implied Equity Risk Premiums", "Q7Yaw7gSIXY")
DRM1 = ("Damodaran · Discount Rate Myth 1: If you don't like betas…", "_uIowZm1DsY")
DRM2 = ("Damodaran · Discount Rate Myth 2: It's all about D in a DCF", "FbjJqlCo1iM")
NV2023 = ("Damodaran · AI Winners, Losers and Wannabes: NVIDIA (June 2023)", "2N0IDShsTyc")
DEEPSEEK = ("Damodaran · DeepSeek crashes the AI Party (January 2025)", "fx5jnE5HnhE")
TSLA_DIY = ("Damodaran · A Do-it-Yourself (DIY) Valuation of Tesla (February 2020)", "BVc6CfAjAbM")
PAYTM_V = ("Damodaran · Paytm’s ‘Coming of Age’ IPO (2021)", "Y0U-XsjQdD4")
TV_MYTH5 = ("Damodaran · Terminal Value Myth 5: The Terminal value ate my DCF!", "3T5sAeswybo")
S14_REL = ("Damodaran · Session 14: Relative Valuation - First Principles", "WDZwqSierZ4")
S8_GROWTH = ("Damodaran · Session 8: Estimating Growth", "fRNcP9xjk-8")
LIGHT = ("Damodaran · Narrative and Numbers: Light in the Darkness", "f4skDr1Lqjc")
NV25_XLS = BLOG + "NvidiaJan2025.xlsx"
NV24_XLS = BLOG + "Nvidia2024.xlsx"
PAYTM_XLS = BLOG.replace("pages.stern.nyu.edu", "www.stern.nyu.edu") + "Paytm2021.xlsx"
TSLA_XLS = "https://www.stern.nyu.edu/~adamodar/pc/blog/TeslaJan2020DIY.xlsx"

# ---- SEC EDGAR company facts (10-K, by fiscal year), $M --------------------------------------------
KO_REV_2024, KO_GROSS, KO_NI, KO_DIL_SHARES = 47061, 29544, 13107, 4313
KO_CONC, KO_FIN, KO_US, KO_INTL = 28462, 19479, 19127, 28814          # revenue by line of business / place (Note 3)
KO_CASES, KO_CASES_2024 = 33.8, 33.7                                   # unit cases, billions
KO_SERVINGS, WORLD_SERVINGS = 2.2, 65                                  # billions a day
JPM = {"cik": 19617, "assets": 4424900, "deposits": 2559320, "equity": 362438, "equity_2024": 344758,
       "ni": 57048, "rev": 182447, "nii": 95443, "price": 322.22}
NVDA = {"cik": 1045810, "rev": {"FY2023": 26974, "FY2024": 60922, "FY2025": 130497, "FY2026": 215938},
        "opinc": 130387, "rnd": 18497, "capex": 6042, "da": 2843, "price": 186.50, "shares": 24300}
INTC = {"cik": 50863, "rev": {2021: 79024, 2024: 53101, 2025: 52853}, "opinc": {2024: -11678, 2025: -2214},
        "capex": 14646, "dep": 10757, "price": 36.90}
TSLA = {"cik": 1318605, "rev": {2022: 81462, 2024: 97690, 2025: 94827}, "opinc": 4355, "ni": 3794, "eps": 1.08,
        "debt": 6584 + 1569, "leases": 6343, "cash": 16513 + 27546, "shares": 3752.4, "price": 449.72}
# regression betas: 60 monthly returns, Jan 2021–Dec 2025, against the S&P 500 (Yahoo adjusted closes)
TSLA_REG, TSLA_SE, TSLA_R2 = 1.83, 0.46, 0.21
# ---- Damodaran, January 2026 data pages ---------------------------------------------------------
AUTO = {"n": 33, "beta": 1.46, "unlev": 1.31, "evs": 3.88, "margin": 2.38, "roc": 2.25, "wacc": 9.38}
SOFTW = {"n": 309, "beta": 1.28, "unlev": 1.25, "evs": 11.41, "margin": 33.21, "roc": 29.32, "wacc": 9.34}
SEMI = {"n": 66, "unlev": 1.50, "s2c": 1.21, "roc": 27.23, "growth": 22.88, "wacc": 10.55, "margin": 35.31}
BEV_PE_TRAIL, BEV_PE_AGG, BEV_EVS = 47.76, 26.92, 4.16
HIST = {"1928–2025": (7.03, 5.48, 2.10), "1976–2025": (6.57, 5.79, 2.62), "2016–2025": (14.53, 13.79, 3.76)}  # arithmetic, geometric, standard error
IMPLIED = {"end of 1999": 2.05, "end of 2008": 6.43, "end of 2021": 4.24, "end of 2022": 5.94, "end of 2025": 4.23}
HISTRET, HISTIMPL = DAM + "histretSP.html", DAM + "histimpl.html"

# ---- KO extras, all from the L03–L14 model -------------------------------------------------------
def wacc_gen(ko_erp=None, beta_add=0.0, rf=None):
    erp = KO_ERP if ko_erp is None else ko_erp
    r = RF_NET if rf is None else rf
    bl = BETA_L + beta_add
    kd = (r + SYN_SPREAD) * (1 - TAX_US / 100)
    return (E_M * (r + bl * erp) + D_M * kd) / (E_M + D_M)
assert abs(wacc_gen() - WACC) < 1e-9
def dcf_rows(g=None, wacc=None, ebit=None):
    """The same model as dcf(), year by year: (year, EBIT, tax rate, after-tax EBIT, reinvestment, FCFF, PV)."""
    g = G if g is None else g; w = (WACC if wacc is None else wacc) / 100
    e, rows = (EBIT_CLEAN if ebit is None else ebit), []
    for y in range(1, 11):
        e *= 1 + g
        t = EFF if y <= 5 else EFF + (TAX_US - EFF) * (y - 5) / 5
        at = e * (1 - t / 100); re = at * g / ROC; f = at - re
        rows.append((y, e, t, at, re, f, f / (1 + w) ** y))
    return rows
def vps(**kw):
    w = kw.pop("wacc", None)
    return per_share(dcf(wacc=w, **kw)[0])
def dcf_ebit(scale):   # operating value with the base-year margin moved, the rest unchanged
    g, w = G, WACC / 100
    pv, e = 0.0, EBIT_CLEAN * scale
    for y in range(1, 11):
        e *= 1 + g
        t = EFF if y <= 5 else EFF + (TAX_US - EFF) * (y - 5) / 5
        pv += e * (1 - t / 100) * (1 - g / ROC) / (1 + w) ** y
    tv = e * (1 + g) * (1 - TAX_US / 100) * (1 - g / ROC) / (w - g)
    return pv + tv / (1 + w) ** 10
assert abs(dcf_ebit(1) - OPS_MOAT) < 1e-6
assert abs(sum(r[6] for r in dcf_rows()) + 0 - (OPS_MOAT * (1 - TVS_MOAT))) < 1e-3
CLEAN_MARGIN = EBIT_CLEAN / REV * 100
KO_EPS = KO_NI / KO_DIL_SHARES
KO_PE = KO_PRICE / KO_EPS
KO_EV = E_M + D_M - CASH_ST
KO_EVS = KO_EV / REV

# L15: the historical average in place of the implied premium (shift every region by the same amount)
WACC_HIST_A = wacc_gen(KO_ERP + HIST["1928–2025"][0] - ERP_GROSS)
WACC_HIST_G = wacc_gen(KO_ERP + HIST["1928–2025"][1] - ERP_GROSS)
VPS_HIST_A, VPS_HIST_G = vps(wacc=WACC_HIST_A), vps(wacc=WACC_HIST_G)
# L17: the same valuation in euros. Expected inflation is an assumption for the exercise: any pair gives the same answer.
INF_USD, INF_EUR = 2.5, 2.0
K = (1 + INF_EUR / 100) / (1 + INF_USD / 100)
WACC_EUR = ((1 + WACC / 100) * K - 1) * 100
G_EUR = (1 + G) * K - 1
def eur_value(cf_eur=True, rate_eur=True):
    """Value (in dollars at today's exchange rate) of KO's cash flows, in euros or dollars, at a euro or dollar rate."""
    rows = dcf_rows(); w = (WACC_EUR if rate_eur else WACC) / 100; k = K if cf_eur else 1.0
    g = G_EUR if cf_eur else G
    pv = sum(f * k ** y / (1 + w) ** y for y, _, _, _, _, f, _ in rows)
    f11 = rows[-1][3] * (1 + G) / (1 - rows[-1][2] / 100) * (1 - TAX_US / 100) * (1 - G / ROC) * k ** 11
    return pv + f11 / (w - g) / (1 + w) ** 10
EUR_OK, EUR_A, EUR_B = eur_value(True, True), eur_value(True, False), eur_value(False, True)
assert abs(EUR_OK - OPS_MOAT) / OPS_MOAT < 1e-9 and abs(per_share(OPS_MOAT) - VPS_MOAT) < 1e-9
# L30: one input at a time
SENS30 = [
    ("Beta ±0.2", vps(wacc=wacc_gen(beta_add=+0.2)), vps(wacc=wacc_gen(beta_add=-0.2)), "discount rate"),
    ("Cost of capital ±0.5 point", vps(wacc=WACC + 0.5), vps(wacc=WACC - 0.5), "discount rate"),
    ("Operating margin ±2 points", per_share(dcf_ebit((CLEAN_MARGIN - 2) / CLEAN_MARGIN)), per_share(dcf_ebit((CLEAN_MARGIN + 2) / CLEAN_MARGIN)), "cash flow"),
    ("Growth ±1 point", vps(g=G - 0.01), vps(g=G + 0.01), "cash flow"),
    ("Moat (return on capital forever at the cost of capital, or at today’s)", VPS_NOMOAT, VPS_MOAT, "cash flow"),
]
SENS30_TOP = sorted(SENS30, key=lambda r: -abs(r[2] - r[1]))
# L31: country risk by where KO sells vs where it is based
WACC_US_ONLY = wacc_gen(ERP_NET)
VPS_US_ONLY = vps(wacc=WACC_US_ONLY)
# L32: what growth would the price need (moat case)?
def solve(f, lo, hi, target):
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) < target else (lo, mid)
    return (lo + hi) / 2
G_IMPLIED = solve(lambda g: vps(g=g), 0.0, 0.06, KO_PRICE)
WACC_IMPLIED = solve(lambda w: -vps(wacc=w), 4.0, 9.0, -KO_PRICE)

# ---- his NVIDIA model, January 2025 (NvidiaJan2025.xlsx, from the youtube-digest library) -----------
# Three businesses; his FCFF for the 'rest' and 'auto' parts as he printed them, and the AI part rebuilt
# (market × share × margin, tax 13.5% → 25%, reinvestment = revenue change three years on ÷ 2.5).
NV_BASE_REV, NV_YR1_REV, NV_YR10_REV = 113269, 55279.35 + 82992 + 3036, 357271.69
NV_VPS_2025, NV_PRICE_2025, NV_VPS_2024, NV_PRICE_2024 = 77.51, 123, 86.68, 106
NV_R0, NV_R0_2024, NV_RS, NV_G, NV_ROC_T, NV_S2C = 0.11793732266471768, 0.1051547270453094, 0.085, 0.047, 0.20, 2.5
NV_REST_F = [26694.398115, 29598.775164, 34202.891976, 39608.949694, 45907.424980, 51602.597798, 56851.946302, 60157.032021, 62339.565988, 63237.176326]
NV_AUTO_F = [454.191, 1464.8148, 3241.3452, 4738.3104, 6405.3, 7443.7056, 8515.7208, 10531.6032, 11703.9024, 12881.738124]
NV_REST_EAT, NV_AUTO_EAT = 69387.05477240021, 14134.5          # after-tax operating income in the terminal year
NV_CASH, NV_NONOP, NV_DEBT, NV_SHARES = 38487, 2237, 10225, 24490
NV_TAX = [0.135] * 5 + [0.158, 0.181, 0.204, 0.227, 0.25]
NV_MARGIN = [0.65, 0.63, 0.62, 0.61, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]
def nv_ai_rev(m10):
    m5 = 80000 + 0.6 * (m10 - 80000)
    mk = [80000 + (m5 - 80000) * t / 5 for t in range(1, 6)] + [m5 + (m10 - m5) * t / 5 for t in range(1, 6)]
    return [m * (0.8 - 0.02 * t) for t, m in enumerate(mk, 1)]
def nv_value(m10=300000, r0=NV_R0, roc_t=NV_ROC_T):
    rates = [r0] * 5 + [r0 + (NV_RS - r0) * t / 5 for t in range(1, 6)]
    df, d = [], 1.0
    for r in rates: d /= 1 + r; df.append(d)
    rev = nv_ai_rev(m10); ext = rev + [rev[-1] * (1 + NV_G) ** k for k in range(1, 4)]
    ai = [r * m * (1 - t) - (ext[i + 3] - ext[i + 2]) / NV_S2C for i, (r, m, t) in enumerate(zip(rev, NV_MARGIN, NV_TAX))]
    tv_term = lambda eat: eat * (1 - NV_G / roc_t) / (NV_RS - NV_G)
    ai_eat = rev[-1] * (1 + NV_G) * 0.6 * 0.75
    pv = sum((a + b_ + c) * x for a, b_, c, x in zip(NV_REST_F, ai, NV_AUTO_F, df))
    tv = (tv_term(NV_REST_EAT) + tv_term(ai_eat) + tv_term(NV_AUTO_EAT)) * df[-1]
    ops = pv + tv
    return (ops + NV_CASH + NV_NONOP - NV_DEBT) / NV_SHARES, ops, tv / ops
NV_CHECK, NV_OPS, NV_TVS = nv_value()
assert abs(NV_CHECK - NV_VPS_2025) < 0.01, NV_CHECK            # reproduces his $77.51
NV_MKT500 = nv_value(m10=500000)[0]
NV_R2024 = nv_value(r0=NV_R0_2024)[0]
NV_NOMOAT, NV_NOMOAT_OPS, NV_NOMOAT_TVS = nv_value(roc_t=NV_RS)
NV_WHICH = ("The story moved it more." if abs(NV_MKT500 - NV_VPS_2025) > abs(NV_R2024 - NV_VPS_2025) else "Here the discount rate moved it more.")
NV_FY26_GROWTH = NVDA["rev"]["FY2026"] - NVDA["rev"]["FY2025"]
NV_NETCAPEX = NVDA["capex"] - NVDA["da"]
# ---- his Paytm IPO model, September 2021 (Paytm2021.xlsx), ₹ million ---------------------------------
PAYTM = {"rev": 31868, "ebit": -15614, "gmv_g": 40, "margin10": 30, "s2c": 2.45, "r0": 10.44, "rs": 8.91, "roc_t": 15,
         "fail": 5, "pv10": 36169.5, "pvtv": 1377090.7, "vps": 2190, "price": 2950}
# ---- Tesla ------------------------------------------------------------------------------------------
TSLA_E = TSLA["price"] * TSLA["shares"]
TSLA_D = TSLA["debt"] + TSLA["leases"]
TSLA_DE = TSLA_D / TSLA_E
def relever(bu, de): return bu * (1 + (1 - TAX_US / 100) * de)
TSLA_BETA_AUTO, TSLA_BETA_SOFT = relever(AUTO["unlev"], TSLA_DE), relever(SOFTW["unlev"], TSLA_DE)
TSLA_EVS = (TSLA_E + TSLA_D - TSLA["cash"]) / TSLA["rev"][2025]
TSLA_PE = TSLA["price"] / TSLA["eps"]
TSLA_MARGIN = TSLA["opinc"] / TSLA["rev"][2025] * 100

def gr(a, b_): return (a / b_ - 1) * 100
L["L01"] = {
    "task": "Four companies, four routes: KO, JPMorgan, NVIDIA and Intel. Using the numbers in What you need, route each (mature, financial, young/high-growth, declining) and name the one thing the route changes in the model. Then judge: what would it cost to route Intel as mature instead? Check D-43/D-44.",
    "need": [
        {"k": "KO: revenue 2025, and growth", "v": "%s · %s" % (B(REV), pct(gr(REV, KO_REV_2024), 1)), "n": "Operating margin %s (before one-off charges)." % pct(CLEAN_MARGIN, 1), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "JPMorgan: assets, and how they are paid for", "v": B(JPM["assets"], 0), "n": "Deposits %s; shareholders’ equity only %s (%s of assets). It lends out what it borrows." % (B(JPM["deposits"], 0), B(JPM["equity"], 0), pct(JPM["equity"] / JPM["assets"] * 100, 1)), "s": "JPMorgan annual report 2025 (10-K, SEC EDGAR)", "u": edgar(JPM["cik"])},
        {"k": "JPMorgan: net income 2025", "v": B(JPM["ni"]), "n": "A return on equity of about %s." % pct(JPM["ni"] / ((JPM["equity"] + JPM["equity_2024"]) / 2) * 100, 0), "s": "JPMorgan annual report 2025 (10-K, SEC EDGAR)", "u": edgar(JPM["cik"])},
        {"k": "NVIDIA: revenue, year to Jan 2023 → Jan 2026", "v": "%s → %s" % (B(NVDA["rev"]["FY2023"]), B(NVDA["rev"]["FY2026"])), "n": "%.0f× in three years; operating margin %s." % (NVDA["rev"]["FY2026"] / NVDA["rev"]["FY2023"], pct(NVDA["opinc"] / NVDA["rev"]["FY2026"] * 100, 0)), "s": "NVIDIA annual reports (10-K, SEC EDGAR)", "u": edgar(NVDA["cik"])},
        {"k": "Intel: revenue 2021 → 2025", "v": "%s → %s" % (B(INTC["rev"][2021]), B(INTC["rev"][2025])), "n": "Down %s. Operating loss: %s in 2024, %s in 2025." % (pct(-gr(INTC["rev"][2025], INTC["rev"][2021]), 0), B(INTC["opinc"][2024]), B(INTC["opinc"][2025])), "s": "Intel annual reports (10-K, SEC EDGAR)", "u": edgar(INTC["cik"])},
        {"k": "Intel: capital spending 2025", "v": B(INTC["capex"]), "n": "Against %s of depreciation: still spending to grow (its chip factories)." % B(INTC["dep"]), "s": "Intel annual report 2025 (10-K, SEC EDGAR)", "u": edgar(INTC["cik"])},
        {"k": "His Intel call, 2024", "v": "≈ $23.70 vs $18.89", "n": "Value at just 3%% revenue growth and a 25%% margin, against the price; he bought. Intel closed 2025 at $%.2f." % INTC["price"], **src(DECLINE)},
    ],
    "key": [
        {"t": "Worked answer: his routes, these numbers",
         "l": ["KO: mature. Growth of %s and a steady %s margin. The default path: today’s operating income, net-capex reinvestment, all 13 stages (L03–L14)." % (pct(gr(REV, KO_REV_2024), 1), pct(CLEAN_MARGIN, 0)),
               "JPMorgan: financial. Debt is its raw material, not its financing: %s of deposits fund %s of assets. Value the equity: net income less what it must keep back as regulatory capital, discounted at the cost of equity. Book equity matters, because the regulator watches it." % (B(JPM["deposits"], 0), B(JPM["assets"], 0)),
               "NVIDIA: high growth (not young, but growing like it). Revenue drives the model, and reinvestment is charged through sales-to-capital (L19). Last year’s operating income tells you little about year 5.",
               "Intel: declining. Revenue down %s in four years, operating losses. The route flips the inputs: revenue can shrink, reinvestment can turn negative as assets are sold, margins can improve as the worst parts go, and the chance of failure becomes its own input, never a higher discount rate." % pct(-gr(INTC["rev"][2025], INTC["rev"][2021]), 0),
               "The cost of routing Intel as mature: you’d assume it grows forever and reinvests to do so, with no chance of failure. That is a bet that the decline ends, hidden inside a default.",
               "His own Intel call (2024) shows the honest version: he priced in very little, 3%% growth and a 25%% margin, below its own history, and still got ≈ $23.70 against $18.89. Intel then spent %s in 2025, %s more than depreciation, the ‘trying too hard’ he warned about." % (B(INTC["capex"]), B(INTC["capex"] - INTC["dep"]))],
         **src(DECLINE)},
        {"t": "His own words on banks",
         "l": ["‘When a bank borrows money at three percent it hopes to make money by lending that out at four percent… if debt is raw material we can no longer think of it as a source of capital.’",
               "So a bank is always an equity valuation: cash flows to equity at the cost of equity, priced with PE or price-to-book, never EV/EBITDA."],
         **src(BANKS)},
    ],
}
# the Learn step of the first lesson: what a valuation is, before what kind of company changes it
L["L01"]["walk"] = [
    {"h": "First, what a valuation is",
     "p": ["A company is worth the cash it will make for its owners over its whole life, counted in today’s money. Damodaran builds that from four parts, and L03–L14 build each one for KO:"],
     "l": [["Cash from the business today.", "Operating income: what it earns from its products after the costs of running it, before interest and tax. You clean it and tax it in L08–L09."],
           ["Reinvestment.", "What it must spend on factories, equipment, research and acquisitions to keep growing (L10). Growth is never free."],
           ["Growth.", "How fast that cash grows: for ten years, then forever at a modest rate (L11–L12)."],
           ["The discount rate.", "The return investors want for the risk they take. It turns cash in year 10 into its value today: the riskier the cash, the less it is worth now (L03–L07)."]],
     "p2": ["Added up year by year, that is a discounted cash flow valuation, a DCF. Some companies need a fifth part: the chance they fail before the cash arrives."]},
    {"h": "Four kinds of company, and what each changes",
     "p": ["The parts stay. What changes is where the value comes from, and which numbers you can trust."],
     "l": [["Mature.", "The default. Today’s operating income is a fair starting point, growth is slow and reinvestment modest. This is the route you’ll build on KO."],
           ["Financial: banks and insurers.", "Borrowing is what a bank sells, not how it pays for itself: it takes in deposits and lends them out at a higher rate. So its debt can’t be split off from the business. You value only the owners’ share: the profit left for them, net income, minus the capital the regulator makes the bank keep as a cushion, discounted at the return owners want, the cost of equity (L05–L07)."],
           ["High growth.", "Last year’s operating income says little about year 5. Start from revenue instead: how big can it get, at what margin, and how much must it reinvest for each extra dollar of sales (sales-to-capital, L10 and L19)."],
           ["Declining.", "The default run backward. Revenue can shrink, reinvestment can turn negative as assets are sold, the margin can improve as the worst parts close, and the chance of failure becomes its own input. Keep that chance separate rather than raising the discount rate: a discount rate measures how uncertain the cash is, not whether the company will be there to pay it."]]},
    {"h": "How to tell the kind from the numbers",
     "p": ["Don’t go by the industry’s name. Look at four signals:"],
     "l": [["Growth.", "A few percent a year, around the pace of the economy, is mature. Several times bigger in a few years is high growth. Shrinking several years running is decline."],
           ["Profit.", "A steady margin, or one that swings and turns into losses? Losses on falling revenue are the mark of decline."],
           ["Who pays for its assets.", "Most companies are funded mainly by their owners and long-term lenders. A bank’s owners put up less than a tenth of its assets, and depositors fund the rest. That, not the name, makes it a financial."],
           ["What it spends to grow.", "Capital spending, against its size and against depreciation, the yearly wear on what it already owns. Heavy spending means it is still building; spending below depreciation means it is letting its base shrink."]]},
    {"h": "Worked: KO",
     "p": ["Revenue of %s in 2025, up %s. An operating margin of %s before one-off charges (L08). Capital spending of %s, about %s of revenue. Slow, steady, very profitable, and spending little to grow: mature, the default route." % (B(REV), pct(gr(REV, KO_REV_2024), 1), pct(CLEAN_MARGIN, 1), B(CAPEX), pct(CAPEX / REV * 100, 0)),
           "Now read JPMorgan, NVIDIA and Intel the same way, with the numbers below. One of them sends mixed signals: that is where the judgement is."]},
]
L["L02"] = {
    "task": "Tell KO’s story in two sentences, using What you need: what it sells, to whom, where it’s heading. Run it through his 3P test: possible, plausible, probable? Then judge: which one number in a KO valuation does this story pin down most? Check D-01.",
    "need": [
        {"k": "What KO sells, and to whom", "v": "%s concentrate · %s finished drinks" % (pct(KO_CONC / REV * 100, 0), pct(KO_FIN / REV * 100, 0)), "n": "Concentrate goes to bottlers, who make, bottle and deliver the drinks. Finished drinks come mostly from the bottlers KO owns.", "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Where it sells", "v": "200+ countries", "n": "%s of revenue outside the US." % pct(KO_INTL / REV * 100, 0), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "How much of the world’s drinking", "v": "%.1f of %d billion" % (KO_SERVINGS, WORLD_SERVINGS), "n": "Servings a day: %s of all drinks." % pct(KO_SERVINGS / WORLD_SERVINGS * 100, 1), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Volume growth 2025", "v": "%.1f vs %.1f billion cases" % (KO_CASES, KO_CASES_2024), "n": "Under 1%% more drinks; revenue grew %s." % pct(gr(REV, KO_REV_2024), 1), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Margins 2025", "v": "gross %s · operating %s" % (pct(KO_GROSS / REV * 100, 0), pct(CLEAN_MARGIN, 0)), "n": "Operating margin before one-off charges (L08). His soft-drinks average: %s." % pct(BEV_MARGIN, 1), "s": "KO annual report 2025 (10-K) · Damodaran margins, January 2026", "u": DAM + "margin.html"},
        {"k": "Advertising 2025", "v": "$%.1f billion" % ADVERTISING_B, "n": "What keeps the brand worth paying for.", "s": "KO annual report 2025 (10-K)", "u": TENK},
    ],
    "key": [
        {"t": "Worked answer: one way to tell it",
         "l": ["Story: KO sells the brands and the concentrate, and lets bottlers carry the factories and trucks; it grows with population, prices and new drinks in poorer countries, not with volume in rich ones.",
               "Possible: yes. Plausible: yes, it has done exactly this for decades. Probable: the slow growth, yes (under 1% more cases in 2025). The pricing power is the claim to test: revenue grew faster than volume.",
               "The number it pins down most: the operating margin, and with it the return on capital. A brand owner that lets others do the heavy lifting earns %s on sales against %s for the average soft-drinks company, on little capital (L11: %s return on capital)." % (pct(CLEAN_MARGIN, 0), pct(BEV_MARGIN, 0), pct(ROC * 100, 0)),
               "What it doesn’t pin down: the discount rate. The story is about cash flows; risk comes later (L03–L07)."],
         **src(NARRATIVE)},
        {"t": "His 3P test, in his words",
         "l": ["Possible: could it happen at all? Plausible: has something like it happened before? Probable: is it likely? Only probable things go in the base case; plausible ones go in a range.",
               "Then every number must agree with the story. If the story says ‘brand owner, few factories’, the model can’t have heavy reinvestment."],
         **src(NARRATIVE)},
    ],
}

L["L15"] = {
    "task": "Using the numbers in What you need, defend his implied ERP against the historical average, out loud, as if to a sceptic: what breaks in your KO valuation if you use the average instead? Only then check D-06.",
    "need": [
        {"k": "Implied premium, start of 2026", "v": pct(ERP_GROSS, 2), "n": "Against the %s Treasury rate; %s against %s (L03, L04)." % (pct(TBOND, 2), pct(ERP_NET, 2), pct(RF_NET, 2)), "s": "Damodaran · Implied ERP by year", "u": HISTIMPL},
    ] + [
        {"k": "Historical: stocks over T-bonds, %s" % k, "v": "%s arithmetic · %s geometric" % (pct(a, 2), pct(g_, 2)), "n": "Standard error %s." % pct(se, 2), "s": "Damodaran · Historical returns 1928–2025 (computed from his yearly returns)", "u": HISTRET}
        for k, (a, g_, se) in HIST.items()
    ] + [
        {"k": "Implied premium over time", "v": " · ".join("%s %s" % (k.replace("end of ", ""), pct(v, 2)) for k, v in IMPLIED.items()), "n": "End of each year.", "s": "Damodaran · Implied ERP by year", "u": HISTIMPL},
        {"k": "KO with his implied premium (L14)", "v": "%s a share" % usd(VPS_MOAT), "n": "Cost of capital %s." % pct(WACC, 2)},
    ],
    "key": [
        {"t": "Worked answer: KO with the historical average",
         "l": ["Swap his %s for the 1928–2025 arithmetic average, %s: every region’s premium rises %s points, KO’s cost of capital goes from %s to %s, and the value falls from %s to %s a share." % (pct(ERP_GROSS, 2), pct(HIST["1928–2025"][0], 2), "%.2f" % (HIST["1928–2025"][0] - ERP_GROSS), pct(WACC, 2), pct(WACC_HIST_A, 2), usd(VPS_MOAT), usd(VPS_HIST_A)),
               "With the geometric average (%s) instead: %s, and %s a share. So ‘the historical premium’ isn’t one number; it is a choice of years and averaging." % (pct(HIST["1928–2025"][1], 2), pct(WACC_HIST_G, 2), usd(VPS_HIST_G)),
               "And it is noisy: a standard error of %s on 98 years means the true premium could be 3 to 11 percent. Over the last ten years, %s." % (pct(HIST["1928–2025"][2], 2), pct(HIST["2016–2025"][0], 2)),
               "What breaks: the valuation stops being about today. The implied premium uses today’s index level and today’s expected cash flows, so it moves when the market does (%s at the end of 2008, %s at the end of 1999). The average still says roughly 7%% whatever happens." % (pct(IMPLIED["end of 2008"], 2), pct(IMPLIED["end of 1999"], 2)),
               "When the sceptic wins: if you think the market as a whole is mispriced, the implied premium carries that mistake in. Then you are a market timer, not a stock picker; say so."],
         "s": "Damodaran · Historical returns and implied ERP pages", "u": HISTIMPL},
        {"t": "His own test (Session 5)",
         "l": ["Q: The S&P 500 is at 4,000; expected cash returned next year is 4% of the index, growing 5% a year for five years, then at the riskfree rate of 3%. What return makes that the price?",
               "His method: solve for the rate, then subtract the riskfree rate. That difference is the implied premium: what investors demand today, not what they got in the past."],
         **src(S5_IMPL)},
    ],
}
L["L16"] = {
    "task": "Tesla: an auto company or a software company? His own call hinged on it. Using the numbers in What you need, build a bottom-up beta for each story, set them against Tesla’s regression beta, and name the one case where the regression wins. Check D-09, D-12.",
    "need": [
        {"k": "Auto & Truck, unlevered beta (cash-corrected)", "v": "%.2f" % AUTO["unlev"], "n": "%d US companies; levered %.2f." % (AUTO["n"], AUTO["beta"]), "s": "Damodaran · Betas by sector, January 2026", "u": BETAS},
        {"k": "Software (System & Application), unlevered", "v": "%.2f" % SOFTW["unlev"], "n": "%d US companies; levered %.2f." % (SOFTW["n"], SOFTW["beta"]), "s": "Damodaran · Betas by sector, January 2026", "u": BETAS},
        {"k": "Tesla’s debt, leases included", "v": B(TSLA_D), "n": "Debt %s + operating leases %s." % (B(TSLA["debt"]), B(TSLA["leases"])), "s": "Tesla annual report 2025 (10-K, SEC EDGAR)", "u": edgar(TSLA["cik"])},
        {"k": "Tesla’s equity, market value", "v": "$%s billion" % format(round(TSLA_E / 1000), ","), "n": "%s M shares × $%.2f (31 Dec 2025). The share count includes the 2025 CEO award’s restricted shares." % (format(round(TSLA["shares"]), ","), TSLA["price"]), "s": "Tesla 10-K cover · Yahoo Finance", "u": yahoo("TSLA")},
        {"k": "Marginal tax rate, US", "v": pct(TAX_US, 0), **src(DU7_2026)},
        {"k": "Tesla’s regression beta (5 years, monthly)", "v": "%.2f" % TSLA_REG, "n": "Against the S&P 500, 2021–2025. Standard error %.2f; R² %.2f." % (TSLA_SE, TSLA_R2), "s": "Computed from Yahoo Finance prices", "u": yahoo("TSLA")},
        {"k": "His 2020 Tesla model: cost of capital", "v": "auto 6.94% · tech 8.86%", "n": "The two medians his do-it-yourself sheet offered, January 2020.", "s": "Damodaran · TeslaJan2020DIY.xlsx", "u": TSLA_XLS},
    ],
    "key": [
        {"t": "Worked answer: his method, Tesla’s numbers",
         "l": ["Debt-to-equity: %s ÷ $%s billion = %s. Tiny, so relevering barely moves anything." % (B(TSLA_D), format(round(TSLA_E / 1000), ","), pct(TSLA_DE * 100, 2)),
               "Auto story: %.2f × (1 + 0.75 × %.4f) = %.2f. Software story: %.2f → %.2f." % (AUTO["unlev"], TSLA_DE, TSLA_BETA_AUTO, SOFTW["unlev"], TSLA_BETA_SOFT),
               "Surprise: in 2026 the two stories give almost the same beta. In 2020 they didn’t (his sheet: 6.94%% vs 8.86%% cost of capital). The auto-or-software question now lives in the margin (auto %s, software %s) and the sales-to-capital, not in the beta." % (pct(AUTO["margin"], 1), pct(SOFTW["margin"], 1)),
               "Regression: %.2f, but ± 2 standard errors runs from %.2f to %.2f, and the S&P 500 explains only %d%% of Tesla’s moves. It also measures 2021–2025 Tesla against one index. Use a bottom-up beta." % (TSLA_REG, TSLA_REG - 2 * TSLA_SE, TSLA_REG + 2 * TSLA_SE, round(TSLA_R2 * 100)),
               "When the regression wins: almost never; only a company that is truly its own industry, with no business to borrow from. Even then use it as a check. Its one fair use here: a regression far above both bottom-up betas says the peer set may be missing something (here, perhaps, robotaxis and AI)."],
         **src(DRM1)},
        {"t": "His rule (D-12), in his words",
         "l": ["‘If you’re saying I’m using a regression beta because I have only five companies, guess what: the square root of five is still going to give you a more precise beta than any single regression beta.’",
               "‘You pick a different index, you get a different number.’"],
         **src(DRM1)},
    ],
}
L["L17"] = {
    "task": "Value KO in dollars, then in euros, using What you need. Which inputs move together and cancel (currency, default spread, riskfree vs terminal growth)? Defend the claim that choosing inconsistently is the only real error — and find the one pair that does not cancel, and why it’s surfaced. Then check the note on inputs that cancel out, under Want more.",
    "need": [
        {"k": "KO’s cost of capital in dollars (L07)", "v": pct(WACC, 2)},
        {"k": "KO’s growth in dollars (L11)", "v": pct(G * 100, 2)},
        {"k": "KO’s value per share in dollars (L14)", "v": usd(VPS_MOAT)},
        {"k": "Expected inflation: dollars · euros (assumed)", "v": "%s · %s" % (pct(INF_USD, 1), pct(INF_EUR, 1)), "n": "An assumption for this exercise. Any pair works; watch what happens to the value."},
        {"k": "How to convert a rate", "v": "(1 + r$) × (1 + π€) ÷ (1 + π$) − 1", "n": "His Session 12 rule: the gap between two currencies’ rates is expected inflation.", **src(S12)},
    ],
    "key": [
        {"t": "Worked answer: KO in euros",
         "l": ["Cost of capital in euros: 1.%s × 1.020 ÷ 1.025 − 1 = %s. Growth in euros: %s." % (("%.4f" % (WACC / 100))[2:], pct(WACC_EUR, 2), pct(G_EUR * 100, 2)),
               "Cash flows in euros: each year’s dollar cash flow × today’s exchange rate × (1.020 ÷ 1.025) to the power of the year, the exchange rate expected from the inflation gap.",
               "Value: exactly the same, %s a share at today’s exchange rate. Inflation sits in both the cash flows and the rate, so it cancels." % usd(per_share(EUR_OK)),
               "The real error, mixing: euro cash flows at the dollar rate give %s a share (%s); dollar cash flows at the euro rate give %s (%s)." % (usd(per_share(EUR_A)), spct((per_share(EUR_A) / VPS_MOAT - 1) * 100), usd(per_share(EUR_B)), spct((per_share(EUR_B) / VPS_MOAT - 1) * 100)),
               "The other two pairs: a default spread left in the riskfree rate makes the premium lower (L03, L04), and a higher riskfree rate raises terminal growth too: ‘what one hand gives you, the other hand takes away’.",
               "The pair that doesn’t cancel: his three ways of measuring country risk (rating spread, CDS, relative volatility) gave Brazil 7.16% to 8.58% on the same day. Nothing on the other side offsets that choice, so it is shown, not hidden."],
         **src(S12)},
    ],
}
L["L18"] = {
    "task": "He says ~80% of the effort goes on discount rates while valuations fail on cash flows and growth. Using his own NVIDIA model in What you need, flip one cash-flow input and one discount-rate input and see which moves value more. Which would you spend your hour on? Then judge what that changes about the 14 KO inputs you just did. Check D-19, D-35.",
    "need": [
        {"k": "His NVIDIA value, Sept 2024", "v": "$%.2f vs $%d price" % (NV_VPS_2024, NV_PRICE_2024), "n": "AI chip market $500 billion by year 10; starting cost of capital %s." % pct(NV_R0_2024 * 100, 2), "s": "Damodaran · Nvidia2024.xlsx", "u": NV24_XLS},
        {"k": "His NVIDIA value, Jan 2025 (after DeepSeek)", "v": "$%.2f vs $%d price" % (NV_VPS_2025, NV_PRICE_2025), "n": "He cut the AI market to $300 billion; starting cost of capital %s." % pct(NV_R0 * 100, 2), "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "Its story inputs (Jan 2025)", "v": "AI share 80% → 60%", "n": "Margin 65%% → 60%%; sales-to-capital %.1f; cost of capital %s → %s after year 10." % (NV_S2C, pct(NV_R0 * 100, 1), pct(NV_RS * 100, 1)), "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "His year-1 revenue forecast (Jan 2025)", "v": B(NV_YR1_REV, 0), "n": "From %s in the year before." % B(NV_BASE_REV, 0), "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "What NVIDIA then reported (year to Jan 2026)", "v": B(NVDA["rev"]["FY2026"], 0), "s": "NVIDIA annual report (10-K, SEC EDGAR)", "u": edgar(NVDA["cik"])},
    ],
    "needNote": "The flips below come from his January 2025 spreadsheet, rebuilt input by input; it reproduces his $77.51.",
    "key": [
        {"t": "Worked answer: flip one input at a time in his model",
         "l": ["Cash-flow input: put the AI market back to $500 billion (his September 2024 story) and the value goes from $%.2f to %s a share." % (NV_VPS_2025, usd(NV_MKT500)),
               "Discount-rate input: put the starting cost of capital back to %s (September 2024) and it goes to %s." % (pct(NV_R0_2024 * 100, 2), usd(NV_R2024)),
               "%s And the story is where he was most wrong: his first forecast year (roughly 2025) had revenue of %s; NVIDIA reported %s, %s more. No discount rate fixes a revenue miss that size." % (NV_WHICH, B(NV_YR1_REV, 0), B(NVDA["rev"]["FY2026"], 0), pct(gr(NVDA["rev"]["FY2026"], NV_YR1_REV), 0)),
               "Spend the hour on the AI market size, NVIDIA’s share of it and the margin. Take the cost of capital from his industry table and move on.",
               "For your 14 KO inputs: L03–L07 (riskfree to cost of capital) were mostly table look-ups; L08–L12 (earnings, tax, reinvestment, growth, terminal value) are where KO’s value can really go wrong. L30 tests this on KO."],
         **src(DEEPSEEK)},
        {"t": "His own words",
         "l": ["‘When I’ve screwed up on a valuation, it’s almost never because I got the discount rate wrong, it’s because I’ve got the cash flow wrong.’",
               "In January 2025 he re-told the story, cut the AI market from $500 to $300 billion, found NVIDIA ‘more overvalued’, and sold half of the half he still held."],
         **src(DEEPSEEK)},
    ],
}
L["L19"] = {
    "task": "His NVIDIA models chose a sales-to-capital ratio: 1.15 in June 2023, 2.5 in January 2025. Using What you need, defend revenue-driven reinvestment for a high-growth firm against capex-minus-depreciation, with NVIDIA’s real numbers and his sector figure. Check D-29.",
    "need": [
        {"k": "NVIDIA revenue growth, year to Jan 2026", "v": B(NV_FY26_GROWTH), "n": "From %s to %s." % (B(NVDA["rev"]["FY2025"]), B(NVDA["rev"]["FY2026"])), "s": "NVIDIA annual report (10-K, SEC EDGAR)", "u": edgar(NVDA["cik"])},
        {"k": "Capital spending · depreciation", "v": "%s · %s" % (B(NVDA["capex"]), B(NVDA["da"])), "s": "NVIDIA annual report (10-K, SEC EDGAR)", "u": edgar(NVDA["cik"])},
        {"k": "Research and development", "v": B(NVDA["rnd"]), "n": "NVIDIA designs chips; others make them. R&D is its real investment.", "s": "NVIDIA annual report (10-K, SEC EDGAR)", "u": edgar(NVDA["cik"])},
        {"k": "Semiconductors: sales-to-capital", "v": "%.2f" % SEMI["s2c"], "n": "US industry, January 2026 (%d companies)." % SEMI["n"], "s": "Damodaran · Capital expenditures by sector, January 2026", "u": DAM + "capex.html"},
        {"k": "His June 2023 choice", "v": "1.15", "n": "NVIDIA had made only $0.65 of revenue per dollar of capital (R&D included) in 2022; he moved it toward the global industry median, 1.15.", **src(NV2023)},
        {"k": "His January 2025 choice", "v": "%.1f" % NV_S2C, "n": "By then NVIDIA’s extra revenue per extra dollar of capital was 5.46.", "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
    ],
    "key": [
        {"t": "Worked answer: two ways to charge NVIDIA for its growth",
         "l": ["Capex minus depreciation: %s − %s = %s, against %s of new revenue. That says each dollar invested brought %.0f dollars of sales, which nobody believes: it misses R&D (%s) and the money tied up in chips and customers." % (B(NVDA["capex"]), B(NVDA["da"]), B(NV_NETCAPEX), B(NV_FY26_GROWTH), NV_FY26_GROWTH / NV_NETCAPEX, B(NVDA["rnd"])),
               "Sales-to-capital at his %.1f: %s ÷ %.1f = %s of reinvestment for that year’s growth. At the industry’s %.2f: %s." % (NV_S2C, B(NV_FY26_GROWTH), NV_S2C, B(NV_FY26_GROWTH / NV_S2C), SEMI["s2c"], B(NV_FY26_GROWTH / SEMI["s2c"])),
               "Why revenue-driven wins: the bill is tied to the growth you assume. Double the growth story and the reinvestment doubles; capex-minus-depreciation looks backward and can’t do that.",
               "Why his number moved from 1.15 to 2.5: he sets it between the company’s own ratio and the industry’s, and NVIDIA’s own ratio had jumped. Choosing it is a judgement; writing down why is the discipline."],
         "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
    ],
    "example": "",
}
NV_ROIC_NOW = 0.4726
L["L20"] = {
    "task": "Growth is earned: reinvestment rate × return on capital. Using What you need, defend that against plugging in an analyst’s growth number — why is the analyst number circular? Try both on NVIDIA and compare what each implies it must reinvest. Check D-30, D-31.",
    "need": [
        {"k": "Analysts’ expected growth, semiconductors", "v": pct(SEMI["growth"], 2), "n": "Next 5 years, earnings, January 2026.", "s": "Damodaran · PE and growth by sector, January 2026", "u": DAM + "pedata.html"},
        {"k": "NVIDIA’s return on capital", "v": pct(NV_ROIC_NOW * 100, 1), "n": "Most recent year, in his January 2025 model.", "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "Semiconductors: return on capital", "v": pct(SEMI["roc"], 2), "n": "Reinvestment rate 35.29% → expected growth 9.61%.", "s": "Damodaran · Fundamental growth by sector, January 2026", "u": DAM + "fundgrEB.html"},
        {"k": "His return on capital after year 10", "v": pct(NV_ROC_T * 100, 0), "n": "He let NVIDIA keep a moat, but a smaller one.", "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
    ],
    "key": [
        {"t": "Worked answer: what %s growth costs NVIDIA" % pct(SEMI["growth"], 1),
         "l": ["Reinvestment rate = growth ÷ return on capital.",
               "At NVIDIA’s %s: %s ÷ %s = %s of after-tax operating income ploughed back." % (pct(NV_ROIC_NOW * 100, 0), pct(SEMI["growth"], 2), pct(NV_ROIC_NOW * 100, 1), pct(SEMI["growth"] / NV_ROIC_NOW, 0)),
               "At the industry’s %s: %s. At his long-run %s: %s, more than everything it earns." % (pct(SEMI["roc"], 1), pct(SEMI["growth"] / SEMI["roc"] * 100, 0), pct(NV_ROC_T * 100, 0), pct(SEMI["growth"] / (NV_ROC_T * 100) * 100, 0)),
               "So the same growth number means very different companies. The analyst number comes with no bill attached; the identity forces you to say which company you mean.",
               "Why it is circular: analysts follow the price, management guidance and each other. Use their number in a valuation and you price the stock with the market’s own mood. Use it as a cross-check of the first few years only."],
         **src(S9)},
    ],
}
L["L21"] = {
    "task": "Terminal value is usually most of the value. Using his NVIDIA model in What you need, defend the growth cap and the return-on-capital convergence as what keeps it honest, where a story of many times today’s revenue still has to settle somewhere. Check D-33–D-35.",
    "need": [
        {"k": "His revenue path (Jan 2025)", "v": "%s → %s" % (B(NV_BASE_REV, 0), B(NV_YR10_REV, 0)), "n": "Base year to year 10.", "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "Growth forever", "v": pct(NV_G * 100, 1), "n": "Equal to the riskfree rate he used, %s." % pct(NV_G * 100, 1), "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "Cost of capital forever", "v": pct(NV_RS * 100, 1), "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "Return on capital forever", "v": pct(NV_ROC_T * 100, 0), "n": "He overrode his own default (return = cost of capital) to give NVIDIA a lasting edge.", "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "His operating value · per share", "v": "%s · $%.2f" % (B(NV_OPS, 0), NV_VPS_2025), "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
    ],
    "key": [
        {"t": "Worked answer: his NVIDIA terminal value",
         "l": ["Terminal value’s share of operating value: %s. Most of NVIDIA’s value is after year 10, even in a model that already grows revenue %.0f× by then." % (pct(NV_TVS * 100, 0), NV_YR10_REV / NV_BASE_REV),
               "The growth cap: %s forever, no more than the riskfree rate. A company can’t outgrow the economy forever; above it, the terminal value has no ceiling." % pct(NV_G * 100, 1),
               "The return-on-capital cap: at %s forever, NVIDIA reinvests %s ÷ %s = %s of its income to grow %s. If its edge fades to the cost of capital (%s), it must reinvest %s, and the value drops to %s a share (terminal share %s)." % (pct(NV_ROC_T * 100, 0), pct(NV_G * 100, 1), pct(NV_ROC_T * 100, 0), pct(NV_G / NV_ROC_T * 100, 1), pct(NV_G * 100, 1), pct(NV_RS * 100, 1), pct(NV_G / NV_RS * 100, 0), usd(NV_NOMOAT), pct(NV_NOMOAT_TVS * 100, 0)),
               "That one judgement, a lasting moat or not, is worth %s a share. Defend it with a named advantage (NVIDIA’s software and its lead in AI chips), or don’t use it." % usd(NV_VPS_2025 - NV_NOMOAT)],
         **src(TV_MYTH5)},
    ],
}
L["L22"] = {
    "task": "He bought Tesla as undervalued and sold it as overvalued: “I have to play the game I came to play.” Defend valuing and pricing as two different games, using What you need, and name when each is the right tool. Check D-42, D-45.",
    "need": [
        {"k": "His Tesla value, February 2020", "v": "≈ $430 vs $640", "n": "Before Tesla’s 15-for-1 of splits: about $29 vs $43 today. An auto company reaching about $125 billion of revenue by 2030, with a 10% chance of failure. He sold.", **src(TSLA_DIY)},
        {"k": "Tesla 2025: revenue · operating margin", "v": "%s · %s" % (B(TSLA["rev"][2025]), pct(TSLA_MARGIN, 1)), "n": "Revenue fell from %s in 2024." % B(TSLA["rev"][2024]), "s": "Tesla annual report 2025 (10-K, SEC EDGAR)", "u": edgar(TSLA["cik"])},
        {"k": "Tesla’s price, 31 Dec 2025 · earnings per share", "v": "$%.2f · $%.2f" % (TSLA["price"], TSLA["eps"]), "n": "A PE of %.0f." % TSLA_PE, "s": "Yahoo Finance · Tesla 10-K", "u": yahoo("TSLA")},
        {"k": "Tesla’s EV/Sales", "v": "%.1f" % TSLA_EVS, "n": "Market value of equity + debt − cash, over 2025 revenue.", "s": "Computed: Tesla 10-K and Yahoo Finance", "u": edgar(TSLA["cik"])},
        {"k": "His sector EV/Sales, January 2026", "v": "auto %.2f · software %.2f" % (AUTO["evs"], SOFTW["evs"]), "n": "Pre-tax operating margins: auto %s, software %s." % (pct(AUTO["margin"], 1), pct(SOFTW["margin"], 1)), "s": "Damodaran · Price and value to sales by sector", "u": DAM + "psdata.html"},
    ],
    "key": [
        {"t": "Worked answer: two games, Tesla’s numbers",
         "l": ["Valuing asks what the cash flows are worth. In 2020 his story (a very good auto company) gave ≈ $430 against $640, so the value game said sell, and he did, and kept to it as the price ran to $900.",
               "Pricing asks what the market pays for similar companies. Today Tesla trades at %.1f times sales; auto companies at %.2f, software companies at %.2f. Priced as either, it looks expensive; priced as ‘Tesla’, nothing is comparable." % (TSLA_EVS, AUTO["evs"], SOFTW["evs"]),
               "Different questions, different tools: a value gap closes when the market comes round to the cash flows; a pricing gap closes when the peer relationship returns. Neither tells you when.",
               "Use valuing when you can hold on until value wins, and can say what the business is. Use pricing when you must act relative to peers (a fund benchmarked to its sector) or when the cash flows can’t yet be estimated.",
               "The mistake is switching games mid-way: buying on value and then holding because ‘the momentum is good’. That is what he refused to do."],
         **src(TSLA_DIY)},
        {"t": "His own words",
         "l": ["‘I bought Tesla because I thought it was undervalued; I sold because I thought it was overvalued. I have to play the game I came to play.’"],
         **src(TSLA_DIY)},
    ],
}

# ---- L23–L34: the run, compare, judge and produce rungs, on the KO model you built -------------------
KO_CHAIN = [  # (stage, number, computed or chosen, the reason)
    ("Story (L02)", "brand owner, slow growth", "chosen", "it sets the margin and the reinvestment"),
    ("Riskfree rate (L03)", pct(RF_NET, 2), "chosen", "net of the US default spread"),
    ("Equity risk premium (L04)", pct(KO_ERP, 2), "computed", "from a choice: weight regions by revenue"),
    ("Beta (L05)", "%.2f" % BETA_L, "computed", "from a choice: the soft-drinks industry"),
    ("Cost of debt (L06)", pct(KD, 2), "computed", "synthetic rating from interest coverage"),
    ("Cost of capital (L07)", pct(WACC, 2), "computed", "market-value weights"),
    ("Base-year operating income (L08)", M(EBIT_CLEAN), "chosen", "which charges are one-offs"),
    ("Tax path (L09)", "%s → %s" % (pct(EFF, 1), pct(TAX_US, 0)), "chosen", "effective now, marginal by year 10"),
    ("Reinvestment rate (L10)", pct(RR * 100, 1), "computed", "net capex, fairlife left out"),
    ("Return on capital · growth (L11)", "%s · %s" % (pct(ROC * 100, 1), pct(G * 100, 2)), "computed", "growth = reinvestment rate × return on capital"),
    ("Return on capital forever (L12)", "%s or %s" % (pct(ROC * 100, 1), pct(WACC, 2)), "chosen", "a lasting moat, or not"),
    ("Equity stakes (L13)", "at market", "chosen", "a price exists for the listed ones"),
    ("Value per share (L14)", "%s / %s" % (usd(VPS_MOAT), usd(VPS_NOMOAT)), "computed", "with and without the moat"),
]
L["L23"] = {
    "task": "Read the whole KO valuation you built in L03–L14, stage by stage, using What you need. For each number, say whether it was computed or chosen, and open its doctrine card to confirm why. Note any you would choose differently.",
    "need": [{"k": s, "v": v} for s, v, _, _ in KO_CHAIN],
    "needNote": "Each number comes from the lesson in brackets, where its sources are.",
    "key": [
        {"t": "Worked answer: computed or chosen",
         "l": ["%s — %s: %s." % (s, c, why) for s, v, c, why in KO_CHAIN if c == "chosen"]
              + ["Everything else is arithmetic on those choices and on KO’s reported numbers, so it can be checked, not argued.",
                 "The choices that matter most, by what they move: the moat (%s vs %s a share) and where country risk comes from (%s if KO is priced as a US company, L31). The discount-rate pieces were mostly look-ups with data behind them; the chosen cash-flow pieces are where you can be argued with." % (usd(VPS_MOAT), usd(VPS_NOMOAT), usd(VPS_US_ONLY))],
         "s": "His method: " + S11_LOOSE[0], "u": yt(S11_LOOSE[1])},
    ],
    "example": "",
}
L["L24"] = {
    "task": "Build KO’s cost of capital in one go: riskfree, risk premium, bottom-up beta, cost of debt and market-value weights, using What you need. Check each against his soft-drinks sector figure and explain every gap. Each number: computed or chosen (with a reason).",
    "need": [
        {"k": "Riskfree rate (L03)", "v": pct(RF_NET, 2), **src(DU2_2026)},
        {"k": "KO’s equity risk premium (L04)", "v": pct(KO_ERP, 2), "s": "Damodaran · Country risk premiums, January 2026", "u": CTRY},
        {"k": "Bottom-up beta (L05)", "v": "%.2f" % BETA_L, "s": "Damodaran · Betas by sector, January 2026", "u": BETAS},
        {"k": "Pre-tax cost of debt (L06)", "v": pct(KD, 2), "s": "Damodaran · Ratings and spreads, January 2026", "u": DAM + "ratings.html"},
        {"k": "Equity (market) · debt (book, leases included)", "v": "%s · %s" % (b(E_M), b(D_M)), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "His soft-drinks sector, January 2026", "v": "cost of equity %s · cost of capital %s" % (pct(BEV_COE, 2), pct(BEV_WACC, 2)), "n": "Beta %.2f; debt 17%% of capital." % BEV_BETA, "s": "Damodaran · Cost of capital by sector, January 2026", "u": DAM + "wacc.html"},
    ],
    "key": [
        {"t": "Worked answer: KO end to end",
         "l": ["Cost of equity: %s + %.2f × %s = %s." % (pct(RF_NET, 2), BETA_L, pct(KO_ERP, 2), pct(COE, 2)),
               "Cost of debt after tax: %s × 0.75 = %s." % (pct(KD, 2), pct(KD_AT, 2)),
               "Weights: equity %s, debt %s. Cost of capital: %s." % (pct(WE * 100, 1), pct(WD * 100, 1), pct(WACC, 2)),
               "Against his sector: %s vs %s cost of equity. Nearly all of the gap is the premium: his sector table uses the US premium (%s) for every company; KO sells %s outside North America, so it gets %s. That is a choice, and the right one for KO." % (pct(COE, 2), pct(BEV_COE, 2), pct(ERP_NET, 2), pct((1 - SEG[0][1] / SEG_TOTAL) * 100, 0), pct(KO_ERP, 2)),
               "Computed: the beta (from the industry), the cost of debt (from coverage), the weights. Chosen: the riskfree rate net of the default spread, the regional weights, leases as debt."],
         "s": "Damodaran · Cost of capital by sector, January 2026", "u": DAM + "wacc.html"},
    ],
    "example": "",
}
R1, R5, R10 = dcf_rows()[0], dcf_rows()[4], dcf_rows()[9]
L["L25"] = {
    "task": "For KO, using What you need: normalise base-year earnings, pick a tax path and build reinvestment. Then compare your structure with how he built NVIDIA (January 2025): what does he drive from revenue that you drove from earnings, and why?",
    "need": [
        {"k": "KO’s cleaned operating income (L08)", "v": M(EBIT_CLEAN), "n": "%s reported + %s impairments + %s fairlife remeasurement." % (M(EBIT), M(IMPAIR), M(FAIRLIFE_REMEAS))},
        {"k": "Tax: effective · marginal (L09)", "v": "%s · %s" % (pct(EFF, 1), pct(TAX_US, 0))},
        {"k": "Reinvestment rate · growth (L10, L11)", "v": "%s · %s" % (pct(RR * 100, 1), pct(G * 100, 2))},
        {"k": "His NVIDIA structure (Jan 2025)", "v": "revenue × margin", "n": "Three businesses’ revenue; margin 65%% → 60%% by year 5; tax 13.5%% → 25%% over years 6–10; reinvestment = revenue change ÷ %.1f, three years ahead." % NV_S2C, "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
    ],
    "key": [
        {"t": "Worked answer: KO’s year 1",
         "l": ["Operating income: %s × (1 + %s) = %s." % (M(EBIT_CLEAN), pct(G * 100, 2), M(R1[1])),
               "After tax at %s: %s." % (pct(R1[2], 1), M(R1[3])),
               "Reinvestment at %s: %s. Free cash flow: %s." % (pct(RR * 100, 1), M(R1[4]), M(R1[5])),
               "Year 10, tax now %s: free cash flow %s." % (pct(R10[2], 0), M(R10[5])),
               "The difference from NVIDIA: KO’s model runs on earnings and grows them at a rate earned from reinvestment; NVIDIA’s runs on revenue, because its future revenue is the whole question, and charges reinvestment for each dollar of it. Mature company, earnings first; growth company, revenue first."],
         "s": "His method: " + S7_CF[0], "u": yt(S7_CF[1])},
    ],
    "example": "",
}
L["L26"] = {
    "task": "Extend KO’s cash flows with fundamental growth and a disciplined terminal value (growth ≤ riskfree, return on capital → cost of capital unless you can name the moat), using What you need. What share of value is terminal? Is that defensible?",
    "need": [
        {"k": "Year-1 free cash flow (L25)", "v": M(R1[5])},
        {"k": "Growth, years 1–10 and forever (L11)", "v": pct(G * 100, 2), "n": "Below the riskfree rate (%s), so it can run forever." % pct(RF_NET, 2)},
        {"k": "Cost of capital (L07)", "v": pct(WACC, 2)},
        {"k": "Return on capital today (L11)", "v": pct(ROC * 100, 1)},
    ],
    "key": [
        {"t": "Worked answer: KO, ten years and a terminal value",
         "l": ["Present value of years 1–10: %s." % b(sum(r[6] for r in dcf_rows())),
               "Year 5 free cash flow %s; year 10 %s (the tax walks from %s to %s over years 6–10)." % (M(R5[5]), M(R10[5]), pct(EFF, 1), pct(TAX_US, 0)),
               "Terminal value with the moat: present value %s, %s of the total %s." % (b(OPS_MOAT * TVS_MOAT), pct(TVS_MOAT * 100, 0), b(OPS_MOAT)),
               "Without it (return on capital → %s): total %s, terminal share %s." % (pct(WACC, 2), b(OPS_NOMOAT), pct(TVS_NOMOAT * 100, 0)),
               "Defensible: yes, for a company growing at about the riskfree rate, most of the value is always after year 10. Compare Paytm (L28), where it was 97%. The share isn’t the problem; an undisciplined terminal value is."],
         **src(S9_TV)},
    ],
    "example": "",
}
L["L27"] = {
    "task": "Open his real NVIDIA spreadsheet (January 2025, in What you need). Trace every major input — story, growth, reinvestment, terminal — back to the stage it belongs to. Where did he make a judgement, and where a computation?",
    "need": [
        {"k": "His spreadsheet", "v": "NvidiaJan2025.xlsx", "n": "Value $%.2f a share against a $%d price." % (NV_VPS_2025, NV_PRICE_2025), "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "Story", "v": "three businesses", "n": "AI chips (market $80 → $300 billion, share 80% → 60%), auto chips ($20 → $200 billion, 6% → 15%), the rest growing 15% a year.", "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "Margin", "v": "65% → 60%", "n": "Reached by year 5.", "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "Sales-to-capital", "v": "%.1f" % NV_S2C, "n": "Years 1–10.", "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "Cost of capital", "v": "%s → %s" % (pct(NV_R0 * 100, 2), pct(NV_RS * 100, 1)), "n": "Fixed for years 1–5, then stepping down.", "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "Terminal", "v": "growth %s · return %s" % (pct(NV_G * 100, 1), pct(NV_ROC_T * 100, 0)), "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
    ],
    "key": [
        {"t": "Worked answer: judgement or computation",
         "l": ["Judgements (the story): the AI market size and NVIDIA’s share of it, the auto market, 15%% growth for the rest, the 60%% target margin, sales-to-capital %.1f, a 20%% return on capital forever, and 8.5%% cost of capital forever." % NV_S2C,
               "Computations: revenue (market × share), operating income (revenue × margin), tax walking 13.5%% → 25%%, reinvestment (revenue change ÷ %.1f), the starting cost of capital (%s, from his betas and premiums), discounting, and the bridge from operating value to $%.2f a share." % (NV_S2C, pct(NV_R0 * 100, 2), NV_VPS_2025),
               "His own overrides are judgements too: he switched off two defaults, ‘return on capital = cost of capital after year 10’ and ‘cost of capital = riskfree + 4.5%’, and wrote down why.",
               "The tell: every judgement is a story claim you could argue with; every computation follows from them. That is what the doctrine cards mean by ‘chosen’ and ‘computed’."],
         **src(DEEPSEEK)},
    ],
    "co": "NVDA",
    "example": "",
}
L["L28"] = {
    "task": "Put two of his models side by side: KO (the mature model you built) and his Paytm IPO (young, losing money), in What you need. List the concrete ways the young-growth model differs and tie each difference to a routing decision.",
    "need": [
        {"k": "Paytm, base year (₹ million)", "v": "revenue %s · operating loss %s" % (format(PAYTM["rev"], ","), format(-PAYTM["ebit"], ",")), "n": "An operating margin of −49%.", "s": "Damodaran · Paytm2021.xlsx", "u": PAYTM_XLS},
        {"k": "Paytm: growth and margin", "v": "payments +%d%% a year · margin → %d%%" % (PAYTM["gmv_g"], PAYTM["margin10"]), "n": "Payment volume grows 40% a year for 5 years; revenue as a share of it doubles; the margin reaches 30% in year 10.", "s": "Damodaran · Paytm2021.xlsx", "u": PAYTM_XLS},
        {"k": "Paytm: reinvestment · risk", "v": "sales-to-capital %.2f · %s → %s" % (PAYTM["s2c"], pct(PAYTM["r0"], 2), pct(PAYTM["rs"], 2)), "n": "Return on capital after year 10: 15%%. Chance of failure: %d%%." % PAYTM["fail"], "s": "Damodaran · Paytm2021.xlsx", "u": PAYTM_XLS},
        {"k": "Paytm: value", "v": "₹%s vs ₹%s IPO price" % (format(PAYTM["vps"], ","), format(PAYTM["price"], ",")), "n": "Years 1–10 worth ₹%s M; the terminal value ₹%s M." % (format(round(PAYTM["pv10"]), ","), format(round(PAYTM["pvtv"]), ",")), "s": "Damodaran · Paytm2021.xlsx", "u": PAYTM_XLS},
        {"k": "KO (L14)", "v": "%s a share" % usd(VPS_MOAT), "n": "Growth %s; margin %s; terminal share %s." % (pct(G * 100, 2), pct(CLEAN_MARGIN, 0), pct(TVS_MOAT * 100, 0))},
    ],
    "key": [
        {"t": "Worked answer: what the route changes",
         "l": ["Starting point: KO starts from today’s earnings; Paytm starts from revenue, because its earnings are negative and mean nothing yet. (Route: young → revenue-driven.)",
               "Margin: KO’s is held; Paytm’s climbs from −49% to 30% over ten years. The target margin is Paytm’s biggest judgement. (Route: young → margin convergence.)",
               "Reinvestment: KO’s from net capex; Paytm’s from sales-to-capital (%.2f), charged for growth that hasn’t happened. (Route: young → D-29.)" % PAYTM["s2c"],
               "Survival: KO none; Paytm a %d%% chance of failure, its own input, not a higher discount rate. (D-44.)" % PAYTM["fail"],
               "Where the value is: Paytm’s first ten years are worth only %s of the total; %s is terminal value. KO’s is %s. A young company is a bet on the far future, so the terminal discipline matters even more." % (pct(PAYTM["pv10"] / (PAYTM["pv10"] + PAYTM["pvtv"]) * 100, 1), pct(PAYTM["pvtv"] / (PAYTM["pv10"] + PAYTM["pvtv"]) * 100, 0), pct(TVS_MOAT * 100, 0))],
         **src(PAYTM_V)},
    ],
    "co": "KO vs Paytm",
    "example": "",
}
L["L29"] = {
    "task": "In his NVIDIA model (What you need), trace the three convergences: effective → marginal tax, high → terminal growth, excess → competitive returns. Why is ‘it’s a path, not a constant’ the resolution each time — and where did he break the rule?",
    "need": [
        {"k": "Tax rate, years 1–10", "v": "13.5% → 25%", "n": "13.5% for years 1–5, then 15.8, 18.1, 20.4, 22.7, 25.0.", "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "Growth of ‘the rest’, years 1–10", "v": "15% → 4.7%", "n": "15% for years 1–5, then 12.9, 10.9, 8.8, 6.8, 4.7.", "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "Cost of capital, years 1–10", "v": "%s → %s" % (pct(NV_R0 * 100, 2), pct(NV_RS * 100, 1)), "n": "Fixed for years 1–5, then equal steps.", "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
        {"k": "Return on capital: year 10 → forever", "v": "114% → 20%", "n": "Implied by his sales-to-capital and margin in year 10, then his override.", "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
    ],
    "key": [
        {"t": "Worked answer: three paths, one jump",
         "l": ["Tax: the effective rate is right now (deferrals and credits), the marginal rate is right eventually (deferrals run out). A path lets both be right.",
               "Growth: high growth is right now, growth at or below the riskfree rate is right forever. A five-year step-down stops a cliff in year 11.",
               "Returns: an edge is right now, competition is right eventually. Here he broke his own default: return on capital falls from 114% to 20%, not to the 8.5% cost of capital. That is a jump, and it is a judgement he had to defend (L21).",
               "The pattern: where two camps argue over a constant, both are usually right at different times, so the input becomes a path. KO’s model does the same with its tax rate (L09)."],
         **src(DEEPSEEK)},
    ],
    "co": "NVDA",
    "example": "",
}
L["L30"] = {
    "task": "Flip KO’s inputs one at a time (beta, cost of capital, margin, growth, terminal return on capital) and record how far the value per share moves, using What you need. Does his claim hold for KO: do the cash-flow and growth inputs dominate the discount-rate inputs?",
    "need": [
        {"k": "KO value per share (L14)", "v": usd(VPS_MOAT), "n": "With the moat; price $%.2f." % KO_PRICE},
        {"k": "Beta (L05) · cost of capital (L07)", "v": "%.2f · %s" % (BETA_L, pct(WACC, 2))},
        {"k": "Operating margin, cleaned (L08)", "v": pct(CLEAN_MARGIN, 1)},
        {"k": "Growth (L11) · return on capital", "v": "%s · %s" % (pct(G * 100, 2), pct(ROC * 100, 1))},
    ],
    "key": [
        {"t": "Worked answer: KO, one input at a time",
         "l": ["%s: %s to %s a share (a spread of %s, %s)." % (k, usd(min(lo, hi)), usd(max(lo, hi)), usd(abs(hi - lo)), kind) for k, lo, hi, kind in SENS30]
              + ["Biggest swings: %s, then %s. So for KO the claim fails on swings: a discount-rate input moves the value most. But ±0.2 is a big move for a 0.65 beta (about a third), and the beta has the most data behind it (%d soft-drinks companies), while growth, the margin and the moat are guesses about the future." % (SENS30_TOP[0][0].split(" ±")[0].lower(), SENS30_TOP[1][0].split(" ±")[0].lower(), BEV_FIRMS),
                 "So spend the effort where the uncertainty is, not where the swing is: the moat and the growth. Then give those inputs ranges in a simulation (L14)."],
         **src(S6B)},
    ],
    "example": "",
}
L["L31"] = {
    "task": "Pick one of KO’s high-uncertainty judgements — the moat (terminal return on capital) or the country-risk method. Using What you need, choose your own value and defend it in writing with its sensitivity: why your number, and what it costs if you’re wrong.",
    "need": [
        {"k": "Moat: return on capital forever (L12)", "v": "%s or %s" % (pct(ROC * 100, 1), pct(WACC, 2)), "n": "Value %s or %s a share." % (usd(VPS_MOAT), usd(VPS_NOMOAT))},
        {"k": "His soft-drinks sector: return on capital vs cost of capital", "v": "%s vs %s" % (pct(BEV_ROC, 2), pct(BEV_WACC, 2)), "n": "January 2026.", "s": "Damodaran · EVA by sector, January 2026", "u": DAM + "EVA.html"},
        {"k": "Country risk: by where KO sells (L04)", "v": pct(KO_ERP, 2), "n": "Cost of capital %s; value %s." % (pct(WACC, 2), usd(VPS_MOAT))},
        {"k": "Country risk: by where KO is based, the US (L04)", "v": pct(ERP_NET, 2), "n": "Cost of capital %s; value %s." % (pct(WACC_US_ONLY, 2), usd(VPS_US_ONLY))},
    ],
    "key": [
        {"t": "Worked answer: defending the moat",
         "l": ["My number: KO keeps an excess return forever, but a smaller one. Evidence: the soft-drinks industry earns %s on capital against a %s cost, and KO earns %s; brands and the bottler system are hard to copy." % (pct(BEV_ROC, 0), pct(BEV_WACC, 2), pct(ROC * 100, 0)),
               "What it costs if I’m wrong: %s a share (%s vs %s), %s of the value." % (usd(VPS_MOAT - VPS_NOMOAT), usd(VPS_MOAT), usd(VPS_NOMOAT), pct((VPS_MOAT / VPS_NOMOAT - 1) * 100, 0)),
               "The other judgement, for contrast: valuing KO as a US company (%s premium) instead of by where it sells (%s) adds %s a share. Almost as big, but easier to defend: %s of revenue is outside North America." % (pct(ERP_NET, 2), pct(KO_ERP, 2), usd(VPS_US_ONLY - VPS_MOAT), pct((1 - SEG[0][1] / SEG_TOTAL) * 100, 0)),
               "The format: the choice, the evidence, the default you’re overriding, and the value with and without it. A defended choice beats a default; an undefended one doesn’t."],
         **src(LIGHT)},
    ],
    "co": "KO",
    "example": "",
}
L["L32"] = {
    "task": "Deliver a value-vs-price verdict on KO using What you need. State the 2–3 assumptions it hangs on, check it against pricing (PE, EV/Sales vs peers), and say what would have to be true for the market to be right instead of you.",
    "need": [
        {"k": "KO’s value (L14)", "v": "%s to %s" % (usd(VPS_NOMOAT), usd(VPS_MOAT)), "n": "Without and with the moat."},
        {"k": "KO’s price, 31 Dec 2025", "v": "$%.2f" % KO_PRICE, "s": "Yahoo Finance", "u": yahoo("KO")},
        {"k": "KO’s PE", "v": "%.1f" % KO_PE, "n": "Price ÷ earnings per share ($%.2f: %s ÷ %s M diluted shares)." % (KO_EPS, M(KO_NI), format(KO_DIL_SHARES, ",")), "s": "KO annual report 2025 (10-K)", "u": TENK},
        {"k": "Soft-drinks PE, January 2026", "v": "%.2f aggregate · %.2f average trailing" % (BEV_PE_AGG, BEV_PE_TRAIL), "s": "Damodaran · PE by sector, January 2026", "u": DAM + "pedata.html"},
        {"k": "KO’s EV/Sales · sector", "v": "%.2f · %.2f" % (KO_EVS, BEV_EVS), "n": "KO’s operating margin %s; the sector’s %s." % (pct(CLEAN_MARGIN, 0), pct(BEV_MARGIN, 0)), "s": "Damodaran · Price and value to sales by sector", "u": DAM + "psdata.html"},
    ],
    "key": [
        {"t": "Worked answer: KO’s verdict",
         "l": ["Value: %s to %s against $%.2f. On my numbers the market pays %s to %s more than the value: expensive." % (usd(VPS_NOMOAT), usd(VPS_MOAT), KO_PRICE, pct((KO_PRICE / VPS_MOAT - 1) * 100, 0), pct((KO_PRICE / VPS_NOMOAT - 1) * 100, 0)),
               "Pricing: a PE of %.1f against %.1f for the sector, so KO is cheap or fair against its peers. EV/Sales %.2f vs %.2f looks dear, but KO’s margin is higher, so that is fair too." % (KO_PE, BEV_PE_AGG, KO_EVS, BEV_EVS),
               "Together: expensive on value, not on price. His third case (D-49): the whole sector is priced richly, and KO is a good house on an expensive street.",
               "It hangs on: growth (%s), the moat, and the cost of capital (%s). And on one choice inside it: priced as a US company (L31), KO is worth %s, above the price. The verdict flips on where country risk comes from, so say which you chose and why." % (pct(G * 100, 2), pct(WACC, 2), usd(VPS_US_ONLY)),
               "For the market to be right, with the moat: growth of %s a year instead of %s, or a cost of capital of %s instead of %s." % (pct(G_IMPLIED * 100, 2), pct(G * 100, 2), pct(WACC_IMPLIED, 2), pct(WACC, 2))],
         **src(S14_REL)},
    ],
    "co": "KO",
    "example": "",
}
L["L33"] = {
    "task": "Pick a company you actually care about. Write its story first (D-01), then build the full valuation, producing your own input at every stage, using What you need. The KO build is your worked example. This is the produce-not-consume milestone.",
    "need": [
        {"k": "Its annual report (10-K)", "v": "SEC EDGAR", "n": "Revenue, operating income, tax, capex, debt, leases, cash, shares. European companies: their annual report.", "s": "SEC EDGAR company search", "u": "https://www.sec.gov/edgar/search/"},
        {"k": "Industry beta, margin, sales-to-capital, cost of capital", "v": "his sector tables", "n": "January 2026, US and global.", "s": "Damodaran · Data pages", "u": "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/data.html"},
        {"k": "Risk premiums by country", "v": "ctryprem.xlsx", "s": "Damodaran · Country risk premiums, January 2026", "u": CTRY},
        {"k": "Riskfree rate · implied premium", "v": "%s · %s" % (pct(RF_NET, 2), pct(ERP_NET, 2)), "n": "In dollars, start of 2026.", **src(DU2_2026)},
        {"k": "The price", "v": "Yahoo Finance", "s": "Yahoo Finance", "u": "https://finance.yahoo.com/"},
        {"k": "A model to fill in", "v": "his NVIDIA sheet", "n": "Same template he uses for every company; change the inputs.", "s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS},
    ],
    "key": [
        {"t": "Check your build against these rules",
         "l": ["Story first: two sentences, graded possible, plausible, probable (L02). Every number must agree with it.",
               "Route it (L01): mature, financial, high-growth or declining. That decides whether you start from earnings or revenue.",
               "Currency and riskfree rate together; premium by where it sells; bottom-up beta; synthetic rating; market weights (L03–L07).",
               "Clean the base year, walk the tax rate, charge reinvestment for the growth (L08–L10). Growth = reinvestment rate × return on capital (L11).",
               "Terminal: growth ≤ riskfree rate; return on capital → cost of capital unless you name the moat; check the terminal share (L12).",
               "Cash, stakes, debt, options, then per share; a range, not a point; value vs price, and pricing vs peers (L13, L14, L32).",
               "Worked example of every step: the KO build, L03–L14."],
         "s": "His method: " + S11_LOOSE[0], "u": yt(S11_LOOSE[1])},
    ],
    "co": "your company",
    "example": "",
}
L["L34"] = {
    "task": "Turn your valuation into a short memo, using What you need: the story, the key judgements (each cited to a doctrine rule with its sensitivity), a range, and the value-vs-price verdict. Compare with the KO memo in Check your answer. Then GRINDE-map the method so it sticks.",
    "need": [
        {"k": "Your story (L33)", "v": "two sentences"},
        {"k": "Your three biggest judgements (L31)", "v": "each with a sensitivity", "n": "Like L31: the choice, the evidence, the value with and without it."},
        {"k": "Your range (L30)", "v": "low · base · high", "n": "From the inputs that move value most (L30)."},
        {"k": "Your verdict (L32)", "v": "value vs price, and pricing vs peers", "n": "Like L32."},
    ],
    "key": [
        {"t": "A worked memo: Coca-Cola, start of 2026",
         "l": ["Story: KO owns the brands and sells concentrate; bottlers carry the factories. It grows slowly (%s in 2025) and earns a high margin (%s) on little capital. Possible, plausible, probable. (D-01)" % (pct(gr(REV, KO_REV_2024), 1), pct(CLEAN_MARGIN, 0)),
               "Judgement 1, the moat: return on capital stays at %s forever, not %s. Worth %s a share. (D-34)" % (pct(ROC * 100, 1), pct(WACC, 2), usd(VPS_MOAT - VPS_NOMOAT)),
               "Judgement 2, growth: %s a year, earned from a %s reinvestment rate. ±1 point moves the value from %s to %s. (D-30)" % (pct(G * 100, 2), pct(RR * 100, 1), usd(SENS["growth ±1 point"][0]), usd(SENS["growth ±1 point"][1])),
               "Judgement 3, country risk: by where KO sells, a %s premium, not %s. Worth %s a share. (D-07)" % (pct(KO_ERP, 2), pct(ERP_NET, 2), usd(VPS_US_ONLY - VPS_MOAT)),
               "Range: %s to %s a share; base case %s." % (usd(VPS_NOMOAT), usd(max(VPS_MOAT, SENS["growth ±1 point"][1])), usd(VPS_MOAT)),
               "Verdict: at $%.2f KO is expensive on value but fair against its peers (PE %.1f vs %.1f). The market needs %s growth to be right. I wouldn’t buy at this price; I’d look again below %s. (D-42, D-49)" % (KO_PRICE, KO_PE, BEV_PE_AGG, pct(G_IMPLIED * 100, 2), usd(VPS_MOAT)),
               "Not financial advice: a worked example of the method."],
         "s": "His method: " + LIGHT[0], "u": yt(LIGHT[1])},
    ],
    "co": "your company",
    "example": "",
}

# =================================================================================================
# Revisits: ten days later, the same question on a new company, with that company's numbers and a
# short answer to check against. KO's lessons revisit on PepsiCo, NVIDIA's on AMD, Tesla's on BYD.
# =================================================================================================
def model(c):
    """A company through the same chain as KO's (L03–L14). c holds the inputs; returns them with the results."""
    m = dict(c)
    m["E"] = c["shares"] * c["price"]
    m["DE"] = c["debt"] / m["E"]
    m["beta"] = c["unlev"] * (1 + (1 - TAX_US / 100) * m["DE"])
    m["coe"] = RF_NET + m["beta"] * c["erp"]
    m["kd"] = RF_NET + c["spread"]
    m["kd_at"] = m["kd"] * (1 - TAX_US / 100)
    m["we"] = m["E"] / (m["E"] + c["debt"])
    m["wacc"] = m["we"] * m["coe"] + (1 - m["we"]) * m["kd_at"]
    m["ebit_at"] = c["ebit"] * (1 - c["eff"] / 100)
    m["rr"] = c["netcapex"] / m["ebit_at"]
    m["roc"] = m["ebit_at"] / c["ic"]
    m["g"] = m["rr"] * m["roc"]
    return m
def mdcf(m, g=None, roc_term=None, wacc=None, ebit=None, taxpath=True):
    """Same as dcf(): ten years at g, tax walking to 25% over years 6–10, then growth forever. (value, tv share, pv of 1–10)"""
    g = m["g"] if g is None else g; roc_term = m["roc"] if roc_term is None else roc_term
    w = (m["wacc"] if wacc is None else wacc) / 100; e = m["ebit"] if ebit is None else ebit
    pv = 0.0
    for y in range(1, 11):
        e *= 1 + g
        t = m["eff"] if (y <= 5 or not taxpath) else m["eff"] + (TAX_US - m["eff"]) * (y - 5) / 5
        pv += e * (1 - t / 100) * (1 - g / m["roc"]) / (1 + w) ** y
    tv = e * (1 + g) * (1 - (TAX_US if taxpath else m["eff"]) / 100) * (1 - g / roc_term) / (w - g)
    pvtv = tv / (1 + w) ** 10
    return pv + pvtv, pvtv / (pv + pvtv), pv
def mps(m, ops): return (ops + m["cash"] + m["cross"] - m["debt"] - m["minority"] - m["options"]) / m["shares"]
def mvps(m, **kw): return mps(m, mdcf(m, **kw)[0])
# the general chain must give KO's own answers before it is trusted with anyone else
_ko = model(dict(shares=KO_SHARES_M, price=KO_PRICE, debt=D_M, unlev=BEV_UNLEV_CASH, erp=KO_ERP, spread=SYN_SPREAD, ebit=EBIT_CLEAN,
                 eff=EFF, netcapex=NETCAPEX, ic=IC, cash=CASH_ST, cross=CROSS, minority=MINORITY, options=OPTIONS_VAL))
assert abs(_ko["wacc"] - WACC) < 1e-9 and abs(mvps(_ko) - VPS_MOAT) < 1e-9 and abs(mvps(_ko, roc_term=WACC / 100) - VPS_NOMOAT) < 1e-9

# ---- PepsiCo: annual report 2025 (10-K, filed 3 Feb 2026), $M ----------------------------------
PEP10K = "https://www.sec.gov/Archives/edgar/data/77476/000007747626000007/pep-20251227.htm"
PEP_SRC = {"s": "PepsiCo annual report 2025 (10-K)", "u": PEP10K}
PEP_REV, PEP_REV24, PEP_EBIT, PEP_INT, PEP_PRETAX, PEP_TAX, PEP_EPS = 93925, 91854, 11498, 1840, 10244, 1949, 6.00
PEP_IMP = {2023: 1230, 2024: 714, 2025: 1946}            # "impairment and other charges", by segment table
PEP_RESTR = {2023: 446, 2024: 698, 2025: 964}            # 2019 Productivity Plan, every year since
PEP_CORE = 14912                                          # the company's own "core" operating profit
PEP_CAPEX, PEP_DA = 4415, 3451
PEP_ACQ = {2023: 314, 2024: 256, 2025: 3391}             # acquisitions and investments (poppi, Siete in 2025)
PEP_DEBT_LT, PEP_DEBT_CUR, PEP_LEASES = 42321, 6861, 3846
PEP_CASH, PEP_EQM, PEP_EQUITY, PEP_MIN = 9159 + 371, 2038, 20406, 141
PEP_SHARES, PEP_PRICE = 1366.649053, 143.52              # 10-K cover (23 Jan 2026); close 31 Dec 2025 (Yahoo)
PEP_FOOD = 0.58                                           # convenient foods' share of revenue (beverages 42%)
PEP_SEG = [("North America (foods and drinks)", 27528 + 28197, "North America"), ("Europe, Middle East & Africa", 18025, "EMEA"),
           ("Latin America", 10549, "Central and South America"), ("Asia Pacific, Australia, NZ & China", 4629, "Asia")]
PEP_IBF = 4997                                            # international beverage franchise, sold across the regions above
PEP_US, PEP_MEX, PEP_RUS = 52228, 6947, 4768
PEP_REG, PEP_REG_SE = 0.42, 0.12
RUSSIA_ERP, MEXICO_ERP = 8.13, 6.69                       # his January 2026 file: Russia unrated, from its political-risk score
FOOD = {"n": 78, "unlev": 0.47, "evs": 1.47, "margin": 10.77, "s2c": 1.71, "roc": 15.95, "rr": 32.77, "g": 5.23, "wacc": 5.79, "pe": 16.78}
BEV_EVS_ = BEV_EVS

PEP_DEBT = PEP_DEBT_LT + PEP_DEBT_CUR + PEP_LEASES
_food, _bev = PEP_FOOD * PEP_REV, (1 - PEP_FOOD) * PEP_REV
PEP_W_FOOD = _food * FOOD["evs"] / (_food * FOOD["evs"] + _bev * BEV_EVS)
PEP_UNLEV = PEP_W_FOOD * FOOD["unlev"] + (1 - PEP_W_FOOD) * BEV_UNLEV_CASH
_intl = [s for s in PEP_SEG if s[2] != "North America"]
PEP_INTL_ERP = sum(r * REGION_ERP[k] for _, r, k in _intl) / sum(r for _, r, _ in _intl)
PEP_ERP = (sum(r * REGION_ERP[k] for _, r, k in PEP_SEG) + PEP_IBF * PEP_INTL_ERP) / PEP_REV
PEP_COV = PEP_EBIT / PEP_INT
PEP_RATING, PEP_SPREAD = rate(PEP_COV)
PEP_IMP_AVG = sum(PEP_IMP.values()) / len(PEP_IMP)
PEP_EBIT_CLEAN = PEP_EBIT + PEP_IMP[2025] - PEP_IMP_AVG
PEP_EFF = PEP_TAX / PEP_PRETAX * 100
PEP_ACQ_AVG = sum(PEP_ACQ.values()) / len(PEP_ACQ)
PEP_NETCAPEX = PEP_CAPEX - PEP_DA + PEP_ACQ_AVG
PEP_NETCAPEX_25 = PEP_CAPEX - PEP_DA + PEP_ACQ[2025]
PEP_IC = PEP_EQUITY + PEP_MIN + PEP_DEBT - PEP_CASH - PEP_EQM
PEP_IN = dict(shares=PEP_SHARES, price=PEP_PRICE, debt=PEP_DEBT, unlev=PEP_UNLEV, erp=PEP_ERP, spread=PEP_SPREAD, ebit=PEP_EBIT_CLEAN,
              eff=PEP_EFF, netcapex=PEP_NETCAPEX, ic=PEP_IC, cash=PEP_CASH, cross=PEP_EQM, minority=PEP_MIN, options=0.0)
P = model(PEP_IN)
assert P["g"] < RF_NET / 100, "PepsiCo's growth forever must stay under the riskfree rate"
P_OPS, P_TVS, P_PV10 = mdcf(P)
P_OPS0, P_TVS0, _ = mdcf(P, roc_term=P["wacc"] / 100)
P_VPS, P_VPS0 = mps(P, P_OPS), mps(P, P_OPS0)
P_VPS_FLAT = mps(P, mdcf(P, taxpath=False)[0])
P_HIST = model(dict(PEP_IN, erp=PEP_ERP + HIST["1928–2025"][0] - ERP_GROSS))
P_VPS_HIST = mvps(P_HIST)
P_US = model(dict(PEP_IN, erp=ERP_NET)); P_VPS_US = mvps(P_US)
P_WEUR = ((1 + P["wacc"] / 100) * K - 1) * 100; P_GEUR = (1 + P["g"]) * K - 1
P_MARGIN = PEP_EBIT_CLEAN / PEP_REV * 100
P_SENS = [
    ("Beta ±0.2", mvps(model(dict(PEP_IN, unlev=PEP_UNLEV + 0.2 / (1 + 0.75 * P["DE"])))), mvps(model(dict(PEP_IN, unlev=PEP_UNLEV - 0.2 / (1 + 0.75 * P["DE"]))))),
    ("Cost of capital ±0.5 point", mvps(P, wacc=P["wacc"] + 0.5), mvps(P, wacc=P["wacc"] - 0.5)),
    ("Operating margin ±2 points", mvps(P, ebit=PEP_EBIT_CLEAN * (P_MARGIN - 2) / P_MARGIN), mvps(P, ebit=PEP_EBIT_CLEAN * (P_MARGIN + 2) / P_MARGIN)),
    ("Growth ±1 point", mvps(P, g=P["g"] - 0.01), mvps(P, g=P["g"] + 0.01)),
    ("Moat (return forever at the cost of capital, or at today’s)", P_VPS0, P_VPS),
]
P_SENS_TOP = sorted(P_SENS, key=lambda r: -abs(r[2] - r[1]))
P_G_IMPLIED = solve(lambda g: mvps(P, g=g), 0.0, 0.06, PEP_PRICE)
P_PE = PEP_PRICE / PEP_EPS
P_EVS = (P["E"] + PEP_DEBT - PEP_CASH) / PEP_REV
_r1 = P["ebit"] * (1 + P["g"]); _r1at = _r1 * (1 - P["eff"] / 100); _r1re = _r1at * P["g"] / P["roc"]
P_Y1 = (_r1, _r1at, _r1re, _r1at - _r1re)
assert abs(_ko["g"] - G) < 1e-12

# ---- AMD: annual report 2025 (10-K, filed 4 Feb 2026), $M ------------------------------------------
AMD10K = "https://www.sec.gov/Archives/edgar/data/2488/000000248826000018/amd-20251227.htm"
AMD_SRC = {"s": "AMD annual report 2025 (10-K)", "u": AMD10K}
AMD_REV = {2022: 23601, 2023: 22680, 2024: 25785, 2025: 34639}
AMD_DC = {2024: 12579, 2025: 16635}
AMD_EBIT, AMD_AMORT, AMD_RND, AMD_CAPEX, AMD_DEP = 3694, 1031 + 1223, 8091, 974, 521
AMD_PRETAX, AMD_TAX = 4166, -103
AMD_EQUITY, AMD_GW, AMD_INTANG = 62999, 25126, 16705
AMD_DEBT = 2348 + 874 + 784                                # debt and operating leases
AMD_CASH = 5539 + 5013
AMD_SHARES, AMD_PRICE = 1630.410843, 214.16
AMD_REG, AMD_REG_SE = 1.95, 0.42
AMD_EBITA = AMD_EBIT + AMD_AMORT                          # before amortizing what it paid for Xilinx
AMD_IC = AMD_EQUITY + AMD_DEBT - AMD_CASH
AMD_ROC = AMD_EBIT * (1 - TAX_US / 100) / AMD_IC
AMD_ROC_A = AMD_EBITA * (1 - TAX_US / 100) / AMD_IC
AMD_ROC_X = AMD_EBITA * (1 - TAX_US / 100) / (AMD_IC - AMD_GW - AMD_INTANG)
AMD_GROWTH = AMD_REV[2025] - AMD_REV[2024]
AMD_NETCAPEX = AMD_CAPEX - AMD_DEP
AMD_E = AMD_SHARES * AMD_PRICE
G_FOREVER, R_MATURE, ROC_EDGE = RF_NET / 100, NV_RS, 0.15   # riskfree growth; his mature cost of capital in the NVIDIA model; his usual 15% edge
def tv_mult(roc): return (1 - G_FOREVER / roc) / (R_MATURE - G_FOREVER)

# ---- BYD: Hong Kong-listed, reports in renminbi (CNY M); Yahoo Finance's figures for 2025 -----------
BYD_SRC = {"s": "BYD annual figures 2025 (Yahoo Finance)", "u": "https://finance.yahoo.com/quote/1211.HK/financials/"}
BYD_REV = {2023: 602315.4, 2024: 777102.5, 2025: 803965.0}
BYD_EBIT, BYD_NI, BYD_EPS = 38516.9, 32619.0, 3.58
BYD_DEBT, BYD_CASH = 119120.6, 75424.7 + 54532.5
BYD_CAPEX, BYD_DA, BYD_RND = 156807.9, 78570.6, 57978.1
BYD_SHARES, BYD_PRICE_HKD, HKD_CNY = 9117.2, 97.75, 0.8899   # shares after the 3-for-1 split of June 2025
BYD_REG, BYD_REG_SE, BYD_R2 = 0.92, 0.19, 0.29          # 2021–2025, monthly, against the Hang Seng
TAX_CN = 25.0
G_AUTO = {"n": 165, "unlev": 1.15, "evs": 1.50, "margin": 4.33, "wacc": 9.48}       # his global tables, January 2026
G_ELEC = {"n": 1158, "unlev": 1.34, "evs": 2.77, "margin": 8.40}
GLOBAL_SRC = {"s": "Damodaran · global industry tables, January 2026", "u": "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/data.html"}
BYD_E = BYD_SHARES * BYD_PRICE_HKD * HKD_CNY
BYD_DE = BYD_DEBT / BYD_E
BYD_B_AUTO = G_AUTO["unlev"] * (1 + (1 - TAX_CN / 100) * BYD_DE)
BYD_B_ELEC = G_ELEC["unlev"] * (1 + (1 - TAX_CN / 100) * BYD_DE)
BYD_PE = BYD_PRICE_HKD * HKD_CNY / BYD_EPS
BYD_EVS = (BYD_E + BYD_DEBT - BYD_CASH) / BYD_REV[2025]
BYD_MARGIN = BYD_EBIT / BYD_REV[2025] * 100

# ---- Wells Fargo and IBM, for the routing revisit -------------------------------------------------
WFC = {"cik": 72971, "assets": 2148631, "deposits": 1426207, "equity": 181117, "ni": 21338}
IBM_ = {"cik": 51143, "rev": {2011: 106916, 2018: 79591, 2021: 57350, 2024: 62753, 2025: 67535}, "acq": 8294}

def need(k, v, n=None, s=None):
    d = {"k": k, "v": v}
    if n: d["n"] = n
    if s: d.update(s)
    return d
def nb(x): return "%.1f" % x
P_ROWS = [  # the PepsiCo chain, for the revisits that use it
    ("Riskfree rate", pct(RF_NET, 2)), ("Equity risk premium", pct(PEP_ERP, 2)), ("Beta", "%.2f" % P["beta"]),
    ("Cost of capital", pct(P["wacc"], 2)), ("Clean operating income", M(PEP_EBIT_CLEAN)), ("Tax now → later", "%s → 25%%" % pct(PEP_EFF, 1)),
    ("Return on capital · growth", "%s · %s" % (pct(P["roc"] * 100, 1), pct(P["g"] * 100, 2))),
]
REV = {}
REV["L01"] = {"rev": "PEP, WFC, AMD, IBM",
    "rtask": "Route four new companies: PepsiCo, Wells Fargo, AMD and IBM. Name each one’s route and the one thing it changes in the model. Which of the four is the trap, and why?",
    "rneed": [need("PepsiCo: revenue 2025, growth", "%s · %s" % (B(PEP_REV), pct(gr(PEP_REV, PEP_REV24), 1)), "Operating margin %s." % pct(PEP_EBIT / PEP_REV * 100, 1), PEP_SRC),
              need("Wells Fargo: assets · deposits", "%s · %s" % (B(WFC["assets"], 0), B(WFC["deposits"], 0)), "Equity %s, %s of assets." % (B(WFC["equity"], 0), pct(WFC["equity"] / WFC["assets"] * 100, 1)), {"s": "Wells Fargo annual report 2025 (SEC EDGAR)", "u": edgar(WFC["cik"])}),
              need("AMD: revenue 2023 → 2025", "%s → %s" % (B(AMD_REV[2023]), B(AMD_REV[2025])), "Up %s in 2025; R&D is %s of revenue." % (pct(gr(AMD_REV[2025], AMD_REV[2024]), 0), pct(AMD_RND / AMD_REV[2025] * 100, 0)), AMD_SRC),
              need("IBM: revenue 2011 → 2021 → 2025", "%s → %s → %s" % (B(IBM_["rev"][2011], 0), B(IBM_["rev"][2021], 0), B(IBM_["rev"][2025], 0)), "Up %s in 2025; %s spent buying companies." % (pct(gr(IBM_["rev"][2025], IBM_["rev"][2024]), 1), B(IBM_["acq"])), {"s": "IBM annual reports (SEC EDGAR)", "u": edgar(IBM_["cik"])})],
    "rkey": [{"t": "Short answer", "l": [
        "PepsiCo: mature. Earnings-first, net-capex reinvestment, the default path.",
        "Wells Fargo: financial. Deposits are its raw material; value the equity, with reinvestment in regulatory capital.",
        "AMD: high growth. Revenue drives the model; reinvestment through sales-to-capital.",
        "IBM is the trap. Its revenue roughly halved from 2011 to 2021, which looks like decline, but much of the drop came from selling businesses and, in 2021, spinning off Kyndryl. It grew %s in 2025 and is buying companies: mature, not declining. Route by the business today, not the long chart." % pct(gr(IBM_["rev"][2025], IBM_["rev"][2024]), 1)],
        **src(DECLINE)}]}
REV["L02"] = {"rev": "PEP",
    "rtask": "Tell PepsiCo’s story in two sentences: what it sells, to whom, where it’s heading. Grade it possible, plausible, probable, and name the one number in a PepsiCo valuation the story pins down most.",
    "rneed": [need("What it sells", "58% snacks · 42% drinks", "Frito-Lay, Quaker; Pepsi, Gatorade. About 36% of revenue comes from bottling it does itself.", PEP_SRC),
              need("Where", "%s from the US" % pct(PEP_US / PEP_REV * 100, 0), "Mexico %s, Russia %s, Canada, China." % (B(PEP_MEX), B(PEP_RUS)), PEP_SRC),
              need("Growth 2025", pct(gr(PEP_REV, PEP_REV24), 1), "North American snack volume fell 3%.", PEP_SRC),
              need("Operating margin 2025", pct(PEP_EBIT / PEP_REV * 100, 1), "KO: %s. His industries: soft drinks %s, food processing %s." % (pct(CLEAN_MARGIN, 0), pct(BEV_MARGIN, 1), pct(FOOD["margin"], 1)), PEP_SRC)],
    "rkey": [{"t": "Short answer", "l": [
        "Story: PepsiCo owns snack and drink brands and, unlike KO, makes and delivers much of it itself; it grows on price and new products while snack volumes slip.",
        "Possible and plausible, yes. Probable: the slow growth, yes; the pricing is the claim to test, since volume is falling.",
        "The number it pins down: the operating margin again, but here it sits near food makers’ (%s) rather than KO’s (%s), because PepsiCo carries the factories and trucks. So its reinvestment matters more than KO’s." % (pct(PEP_EBIT / PEP_REV * 100, 0), pct(CLEAN_MARGIN, 0))],
        **src(NARRATIVE)}]}
REV["L03"] = {"rev": "PEP",
    "rtask": "Pick PepsiCo’s currency and riskfree rate. Then say what changes if you value it in Mexican pesos instead (Mexico is its second-biggest country).",
    "rneed": [need("PepsiCo reports in", "US dollars", "%s of revenue from the US; Mexico %s." % (pct(PEP_US / PEP_REV * 100, 0), B(PEP_MEX)), PEP_SRC),
              need("10-year Treasury · US default spread", "%s · %s" % (pct(TBOND, 2), pct(US_SPREAD, 2)), None, src(DU2_2026)),
              need("Mexico’s default spread (Baa2)", "1.62%", "His January 2026 table.", {"s": "Damodaran · Country risk premiums, January 2026", "u": CTRY})],
    "rkey": [{"t": "Short answer", "l": [
        "Dollars, at %s − %s = %s." % (pct(TBOND, 2), pct(US_SPREAD, 2), pct(RF_NET, 2)),
        "In pesos: Mexico’s 10-year bond rate less its 1.62% default spread, and peso cash flows with Mexico’s inflation in them. Done consistently, the value is the same; only mixing them changes it."],
        **src(S12)}]}
REV["L04"] = {"rev": "PEP",
    "rtask": "Give PepsiCo an equity risk premium by where it sells. Which country inside its regions would you worry about?",
    "rneed": [need("%s (%d%%)" % (n, round(r / PEP_REV * 100)), pct(REGION_ERP[k], 2), M(r), {"s": "PepsiCo 10-K · Damodaran’s regional premiums", "u": CTRY}) for n, r, k in PEP_SEG]
             + [need("International beverage franchise (%d%%)" % round(PEP_IBF / PEP_REV * 100), "across the regions", M(PEP_IBF), PEP_SRC),
                need("Russia, inside EMEA", pct(RUSSIA_ERP, 2), "%s of revenue. No credit rating; his premium comes from a political-risk score." % B(PEP_RUS), {"s": "Damodaran · Country risk premiums, January 2026", "u": CTRY})],
    "rkey": [{"t": "Short answer", "l": [
        "Weighted by revenue (the franchise spread like the other international revenue): %s, against %s for the US alone." % (pct(PEP_ERP, 2), pct(ERP_NET, 2)),
        "Lower than KO’s %s: PepsiCo sells %s of its revenue in North America." % (pct(KO_ERP, 2), pct(PEP_SEG[0][1] / PEP_REV * 100, 0)),
        "The worry: Russia, %s at %s, is averaged into EMEA at %s. Country by country, that slice would carry more." % (B(PEP_RUS), pct(RUSSIA_ERP, 2), pct(REGION_ERP["EMEA"], 2))],
        "s": "Damodaran · Country risk premiums, January 2026", "u": CTRY}]}
REV["L05"] = {"rev": "PEP",
    "rtask": "Build PepsiCo’s bottom-up beta. It is in two businesses: weight them by value, not by sales. Then set it beside its regression beta.",
    "rneed": [need("Snacks · drinks, share of revenue", "58% · 42%", None, PEP_SRC),
              need("Food processing: unlevered beta · EV/Sales", "%.2f · %.2f" % (FOOD["unlev"], FOOD["evs"]), "%d US companies." % FOOD["n"], {"s": "Damodaran · Betas and EV/Sales by sector, January 2026", "u": BETAS}),
              need("Soft drinks: unlevered beta · EV/Sales", "%.2f · %.2f" % (BEV_UNLEV_CASH, BEV_EVS), None, {"s": "Damodaran · Betas and EV/Sales by sector, January 2026", "u": BETAS}),
              need("PepsiCo equity · debt (leases included)", "%s · %s" % (b(P["E"]), b(PEP_DEBT)), "%s M shares × $%.2f." % (format(round(PEP_SHARES), ","), PEP_PRICE), PEP_SRC),
              need("Regression beta (5 years, monthly)", "%.2f" % PEP_REG, "Standard error %.2f." % PEP_REG_SE, {"s": "Computed from Yahoo Finance prices", "u": yahoo("PEP")})],
    "rkey": [{"t": "Short answer", "l": [
        "Value weights: snacks %s × %.2f, drinks %s × %.2f → %s snacks, %s drinks. The drinks are 42%% of sales but two thirds of the value." % (b(_food), FOOD["evs"], b(_bev), BEV_EVS, pct(PEP_W_FOOD * 100, 0), pct((1 - PEP_W_FOOD) * 100, 0)),
        "Unlevered: %s × %.2f + %s × %.2f = %.2f. Debt-to-equity %s; levered %.2f." % (pct(PEP_W_FOOD * 100, 0), FOOD["unlev"], pct((1 - PEP_W_FOOD) * 100, 0), BEV_UNLEV_CASH, PEP_UNLEV, pct(P["DE"] * 100, 1), P["beta"]),
        "Regression %.2f ± %.2f: use the bottom-up %.2f." % (PEP_REG, 2 * PEP_REG_SE, P["beta"])], **src(S6_BETA)}]}
REV["L06"] = {"rev": "PEP",
    "rtask": "Give PepsiCo a cost of debt from a synthetic rating, and add its leases to its debt.",
    "rneed": [need("Operating income · interest expense", "%s · %s" % (M(PEP_EBIT), M(PEP_INT)), None, PEP_SRC),
              need("His table: coverage 5.50 to 6.50 · 6.50 to 8.50", "A+ 0.70% · AA 0.55%", None, {"s": "Damodaran · Ratings and spreads, January 2026", "u": DAM + "ratings.html"}),
              need("Riskfree rate · marginal tax", "%s · 25%%" % pct(RF_NET, 2)),
              need("Debt · operating leases", "%s · %s" % (M(PEP_DEBT_LT + PEP_DEBT_CUR), M(PEP_LEASES)), None, PEP_SRC)],
    "rkey": [{"t": "Short answer", "l": [
        "Coverage %s ÷ %s = %.2f → %s, a %s spread." % (M(PEP_EBIT), M(PEP_INT), PEP_COV, PEP_RATING.split("/")[1], pct(PEP_SPREAD, 2)),
        "Cost of debt %s; after tax %s." % (pct(P["kd"], 2), pct(P["kd_at"], 2)),
        "Leases: %s more debt, %s in all. A weaker rating than KO’s AA: more debt for its earnings." % (M(PEP_LEASES), M(PEP_DEBT))], **src(S10_DEBT)}]}
REV["L07"] = {"rev": "PEP",
    "rtask": "Put PepsiCo’s cost of capital together at market weights. Compare it with book weights and with its two industries.",
    "rneed": [need("Cost of equity (L04, L05 numbers)", pct(P["coe"], 2), "%s + %.2f × %s." % (pct(RF_NET, 2), P["beta"], pct(PEP_ERP, 2))),
              need("After-tax cost of debt (L06 numbers)", pct(P["kd_at"], 2)),
              need("Equity: market · book", "%s · %s" % (b(P["E"]), b(PEP_EQUITY)), None, PEP_SRC),
              need("Debt, leases included", b(PEP_DEBT), None, PEP_SRC),
              need("His industries’ cost of capital", "food %s · soft drinks %s" % (pct(FOOD["wacc"], 2), pct(BEV_WACC, 2)), None, {"s": "Damodaran · Cost of capital by sector, January 2026", "u": DAM + "wacc.html"})],
    "rkey": [{"t": "Short answer", "l": [
        "Market weights %s equity, %s debt: cost of capital %s." % (pct(P["we"] * 100, 0), pct((1 - P["we"]) * 100, 0), pct(P["wacc"], 2)),
        "Book weights would put debt at %s and give %s: too low, because book equity is history." % (pct(PEP_DEBT / (PEP_DEBT + PEP_EQUITY) * 100, 0), pct(PEP_EQUITY / (PEP_DEBT + PEP_EQUITY) * P["coe"] + PEP_DEBT / (PEP_DEBT + PEP_EQUITY) * P["kd_at"], 2)),
        "Above both industries, which use the US premium for every company; PepsiCo’s %s carries its foreign sales." % pct(PEP_ERP, 2)], "s": "Damodaran · Cost of capital by sector, January 2026", "u": DAM + "wacc.html"}]}
REV["L08"] = {"rev": "PEP",
    "rtask": "Clean PepsiCo’s 2025 operating income. Which of its “one-off” charges really are one-off?",
    "rneed": [need("Reported operating income 2025", M(PEP_EBIT), "The company’s own “core” figure adds everything back: %s." % M(PEP_CORE), PEP_SRC),
              need("Restructuring, 2023 · 2024 · 2025", " · ".join(M(v) for v in PEP_RESTR.values()), "Its productivity plan, running every year since 2019.", PEP_SRC),
              need("Impairments and other charges, 2023 · 2024 · 2025", " · ".join(M(v) for v in PEP_IMP.values()), "2025: mostly the Rockstar energy-drink brand.", PEP_SRC)],
    "rkey": [{"t": "Short answer", "l": [
        "Restructuring comes every year: it’s a running cost. Leave it in.",
        "Impairments come every year too, in different sizes: spread them. Average %s; add back only 2025’s excess, %s − %s = %s." % (M(PEP_IMP_AVG), M(PEP_IMP[2025]), M(PEP_IMP_AVG), M(PEP_IMP[2025] - PEP_IMP_AVG)),
        "Clean operating income: %s (a %s margin), not the company’s %s. Adding back recurring charges is how “core” earnings flatter." % (M(PEP_EBIT_CLEAN), pct(P_MARGIN, 1), M(PEP_CORE))], **src(S5)}]}
REV["L09"] = {"rev": "PEP",
    "rtask": "Choose PepsiCo’s tax rate now and at the end of the forecast, and say how they meet.",
    "rneed": [need("Tax · profit before tax, 2025", "%s · %s" % (M(PEP_TAX), M(PEP_PRETAX)), "2024’s rate: 19.4%.", PEP_SRC),
              need("US marginal rate", "25%", None, src(DU7_2026))],
    "rkey": [{"t": "Short answer", "l": [
        "Effective %s ÷ %s = %s: hold it for years 1–5, then step to 25%% by year 10." % (M(PEP_TAX), M(PEP_PRETAX), pct(PEP_EFF, 1)),
        "The path is worth %s a share less than keeping %s forever (%s against %s)." % (usd(P_VPS_FLAT - P_VPS), pct(PEP_EFF, 1), usd(P_VPS), usd(P_VPS_FLAT))], **src(DU7_2026)}]}
REV["L10"] = {"rev": "PEP",
    "rtask": "Build PepsiCo’s reinvestment from capex and acquisitions, then from sales-to-capital. What does 2025 alone get wrong?",
    "rneed": [need("Capex · depreciation and amortisation", "%s · %s" % (M(PEP_CAPEX), M(PEP_DA)), None, PEP_SRC),
              need("Acquisitions, 2023 · 2024 · 2025", " · ".join(M(v) for v in PEP_ACQ.values()), "2025: poppi and Siete.", PEP_SRC),
              need("Revenue growth 2025", M(PEP_REV - PEP_REV24), None, PEP_SRC),
              need("His sales-to-capital: food · soft drinks", "%.2f · %.2f" % (FOOD["s2c"], BEV_S2C), None, {"s": "Damodaran · Capital expenditures by sector, January 2026", "u": DAM + "capex.html"})],
    "rkey": [{"t": "Short answer", "l": [
        "2025 alone: %s − %s + %s = %s, %s of after-tax operating income. Two deals in one year inflate it." % (M(PEP_CAPEX), M(PEP_DA), M(PEP_ACQ[2025]), M(PEP_NETCAPEX_25), pct(PEP_NETCAPEX_25 / P["ebit_at"] * 100, 0)),
        "Average the acquisitions (%s a year): %s, a %s reinvestment rate." % (M(PEP_ACQ_AVG), M(PEP_NETCAPEX), pct(P["rr"] * 100, 1)),
        "From sales-to-capital at about 1.6: %s ÷ 1.6 = %s. The averaged net capex is the better guide for a mature company." % (M(PEP_REV - PEP_REV24), M((PEP_REV - PEP_REV24) / 1.6))], **src(S7_CF)}]}
REV["L11"] = {"rev": "PEP",
    "rtask": "Derive PepsiCo’s growth from reinvestment and return on capital, and set it beside its two industries.",
    "rneed": [need("After-tax operating income", M(P["ebit_at"]), "%s × (1 − %s)." % (M(PEP_EBIT_CLEAN), pct(PEP_EFF, 1))),
              need("Reinvestment (acquisitions averaged)", M(PEP_NETCAPEX)),
              need("Invested capital", M(PEP_IC), "Equity + minority + debt − cash − equity stakes.", PEP_SRC),
              need("His industries: return × reinvestment = growth", "food %s × %s = %s" % (pct(FOOD["roc"], 1), pct(FOOD["rr"], 1), pct(FOOD["g"], 2)), "Soft drinks %s." % pct(BEV_G, 2), {"s": "Damodaran · Fundamental growth by sector, January 2026", "u": DAM + "fundgrEB.html"})],
    "rkey": [{"t": "Short answer", "l": [
        "Return on capital %s ÷ %s = %s; reinvestment rate %s." % (M(P["ebit_at"]), M(PEP_IC), pct(P["roc"] * 100, 1), pct(P["rr"] * 100, 1)),
        "Growth %s × %s = %s a year, just under the %s riskfree rate." % (pct(P["rr"] * 100, 1), pct(P["roc"] * 100, 1), pct(P["g"] * 100, 2), pct(RF_NET, 2)),
        "Well below KO’s %s: the factories and trucks." % pct(ROC * 100, 0)], **src(S9)}]}
REV["L12"] = {"rev": "PEP",
    "rtask": "Set PepsiCo’s growth and return on capital forever under his two caps. What share of its value is terminal, with and without a moat?",
    "rneed": [need("Growth (L11 numbers)", pct(P["g"] * 100, 2)), need("Cost of capital (L07 numbers)", pct(P["wacc"], 2)),
              need("Return on capital today", pct(P["roc"] * 100, 1)), need("Riskfree rate", pct(RF_NET, 2), None, src(DU2_2026))],
    "rkey": [{"t": "Short answer", "l": [
        "Growth %s, under the cap. With the moat (%s forever): operating value %s, %s of it terminal." % (pct(P["g"] * 100, 2), pct(P["roc"] * 100, 1), b(P_OPS), pct(P_TVS * 100, 0)),
        "Without it (return falls to %s): %s, %s terminal. The brands argue for an edge; a 16%% return is a smaller one than KO’s." % (pct(P["wacc"], 2), b(P_OPS0), pct(P_TVS0 * 100, 0))], **src(S9_TV)}]}
REV["L13"] = {"rev": "PEP",
    "rtask": "Go from PepsiCo’s operating value to value per share: cash, stakes, debt, minority interest, shares.",
    "rneed": [need("Operating value (moat)", b(P_OPS)), need("Cash and short-term investments", M(PEP_CASH), None, PEP_SRC),
              need("Equity stakes (book)", M(PEP_EQM), None, PEP_SRC), need("Debt, leases included", M(PEP_DEBT), None, PEP_SRC),
              need("Minority interest", M(PEP_MIN), None, PEP_SRC), need("Shares", "%s M" % format(round(PEP_SHARES, 1), ",.1f"), None, PEP_SRC)],
    "rkey": [{"t": "Short answer", "l": [
        "%s + %s + %s − %s − %s = %s of equity." % (b(P_OPS), M(PEP_CASH), M(PEP_EQM), M(PEP_DEBT), M(PEP_MIN), b(P_OPS + PEP_CASH + PEP_EQM - PEP_DEBT - PEP_MIN)),
        "÷ %s M shares = %s a share (options left out: small)." % (format(round(PEP_SHARES), ","), usd(P_VPS)),
        "The biggest loose end is the debt: %s a share, against KO’s $10.98." % usd(PEP_DEBT / PEP_SHARES)], "s": "His method: " + S11_LOOSE[0], "u": yt(S11_LOOSE[1])}]}
REV["L14"] = {"rev": "PEP",
    "rtask": "Turn PepsiCo into a value per share and a range, then set it against the price. Which three inputs drive the spread?",
    "rneed": [need("Value per share, moat · no moat", "%s · %s" % (usd(P_VPS), usd(P_VPS0))),
              need("PepsiCo’s price, 31 Dec 2025", "$%.2f" % PEP_PRICE, None, {"s": "Yahoo Finance", "u": yahoo("PEP")})],
    "rkey": [{"t": "Short answer", "l": ["Value %s with the moat, %s without, against $%.2f." % (usd(P_VPS), usd(P_VPS0), PEP_PRICE)]
              + ["%s: %s to %s." % (k, usd(min(lo, hi)), usd(max(lo, hi))) for k, lo, hi in P_SENS if k.startswith(("Growth", "Cost", "Moat"))]
              + ["For the price to be right: growth of %s a year instead of %s." % (pct(P_G_IMPLIED * 100, 2), pct(P["g"] * 100, 2))], **src(S6B)}]}
REV["L15"] = {"rev": "PEP",
    "rtask": "Value PepsiCo with his implied premium, then with the historical average. What breaks?",
    "rneed": [need("Implied premium · 1928–2025 average", "%s · %s" % (pct(ERP_GROSS, 2), pct(HIST["1928–2025"][0], 2)), None, {"s": "Damodaran · Implied ERP and historical returns", "u": HISTIMPL}),
              need("PepsiCo’s cost of capital and value (implied)", "%s · %s" % (pct(P["wacc"], 2), usd(P_VPS)))],
    "rkey": [{"t": "Short answer", "l": [
        "With the average, every premium rises %.2f points: cost of capital %s, value %s a share (from %s)." % (HIST["1928–2025"][0] - ERP_GROSS, pct(P_HIST["wacc"], 2), usd(P_VPS_HIST), usd(P_VPS)),
        "What breaks: the valuation stops being about today’s market, and the average itself is uncertain by ±4 points."], "s": "Damodaran · Implied ERP by year", "u": HISTIMPL}]}
REV["L17"] = {"rev": "PEP",
    "rtask": "Value PepsiCo in euros instead of dollars. What cancels, and what would be the real error?",
    "rneed": [need("Cost of capital · growth, in dollars", "%s · %s" % (pct(P["wacc"], 2), pct(P["g"] * 100, 2))),
              need("Expected inflation: dollars · euros (assumed)", "%s · %s" % (pct(INF_USD, 1), pct(INF_EUR, 1)))],
    "rkey": [{"t": "Short answer", "l": [
        "In euros: cost of capital %s, growth %s, same value at today’s exchange rate (%s)." % (pct(P_WEUR, 2), pct(P_GEUR * 100, 2), usd(P_VPS)),
        "The error is mixing: euro cash flows at the dollar rate, or the reverse."], **src(S12)}]}
REV["L23"] = {"rev": "PEP",
    "rtask": "Lay out PepsiCo’s valuation stage by stage. Which numbers were chosen, and which computed?",
    "rneed": [need(k, v) for k, v in P_ROWS],
    "rkey": [{"t": "Short answer", "l": [
        "Chosen: the story; the riskfree rate net of the default spread; weighting the two businesses by value; averaging the impairments and the acquisitions; the tax path; the moat.",
        "Computed: the premium (from where it sells), the beta (from its industries), the cost of debt (coverage), the weights, the return and growth.",
        "The PepsiCo-specific choices, impairments and acquisitions, move its base year most."], "s": "His method: " + S11_LOOSE[0], "u": yt(S11_LOOSE[1])}]}
REV["L24"] = {"rev": "PEP",
    "rtask": "Build PepsiCo’s cost of capital in one go and explain each gap to its industries.",
    "rneed": [need("Riskfree · premium · beta", "%s · %s · %.2f" % (pct(RF_NET, 2), pct(PEP_ERP, 2), P["beta"])),
              need("Cost of debt after tax", pct(P["kd_at"], 2)), need("Weights, market", "%s equity" % pct(P["we"] * 100, 0)),
              need("His industries", "food %s · soft drinks %s" % (pct(FOOD["wacc"], 2), pct(BEV_WACC, 2)), None, {"s": "Damodaran · Cost of capital by sector", "u": DAM + "wacc.html"})],
    "rkey": [{"t": "Short answer", "l": [
        "Cost of equity %s; cost of capital %s." % (pct(P["coe"], 2), pct(P["wacc"], 2)),
        "Above both industries mostly because of the premium (%s vs the US %s); the beta, %.2f, is in between food and drinks." % (pct(PEP_ERP, 2), pct(ERP_NET, 2), P["beta"])], "s": "Damodaran · Cost of capital by sector", "u": DAM + "wacc.html"}]}
REV["L25"] = {"rev": "PEP",
    "rtask": "Work out PepsiCo’s year-1 free cash flow from its clean operating income.",
    "rneed": [need("Clean operating income", M(PEP_EBIT_CLEAN)), need("Growth · tax", "%s · %s" % (pct(P["g"] * 100, 2), pct(PEP_EFF, 1))),
              need("Reinvestment rate", pct(P["rr"] * 100, 1))],
    "rkey": [{"t": "Short answer", "l": [
        "Operating income %s × 1.%s = %s; after tax %s." % (M(PEP_EBIT_CLEAN), ("%.4f" % P["g"])[2:], M(P_Y1[0]), M(P_Y1[1])),
        "Reinvestment %s; free cash flow %s." % (M(P_Y1[2]), M(P_Y1[3]))], **src(S7_CF)}]}
REV["L26"] = {"rev": "PEP",
    "rtask": "Close PepsiCo’s valuation: ten years, then a terminal value. What share is terminal, and is that defensible?",
    "rneed": [need("Year-1 free cash flow", M(P_Y1[3])), need("Growth · cost of capital · return", "%s · %s · %s" % (pct(P["g"] * 100, 2), pct(P["wacc"], 2), pct(P["roc"] * 100, 1)))],
    "rkey": [{"t": "Short answer", "l": [
        "Years 1–10 are worth %s; the terminal value %s: %s of %s." % (b(P_PV10), b(P_OPS - P_PV10), pct(P_TVS * 100, 0), b(P_OPS)),
        "Defensible for a company growing near the riskfree rate."], **src(S9_TV)}]}
REV["L30"] = {"rev": "PEP",
    "rtask": "Flip PepsiCo’s inputs one at a time. Which move its value most?",
    "rneed": [need("Value per share", usd(P_VPS)), need("Beta · cost of capital", "%.2f · %s" % (P["beta"], pct(P["wacc"], 2))),
              need("Margin · growth · return", "%s · %s · %s" % (pct(P_MARGIN, 1), pct(P["g"] * 100, 2), pct(P["roc"] * 100, 1)))],
    "rkey": [{"t": "Short answer", "l": ["%s: %s to %s." % (k, usd(min(lo, hi)), usd(max(lo, hi))) for k, lo, hi in P_SENS]
              + ["Biggest: %s, then %s." % (P_SENS_TOP[0][0].split(" ±")[0].split(" (")[0].lower(), P_SENS_TOP[1][0].split(" ±")[0].split(" (")[0].lower())], **src(S6B)}]}
REV["L31"] = {"rev": "PEP",
    "rtask": "Pick one of PepsiCo’s judgements, the moat or the country risk, and defend your choice with its price.",
    "rneed": [need("Moat: return forever %s or %s" % (pct(P["roc"] * 100, 1), pct(P["wacc"], 2)), "%s or %s" % (usd(P_VPS), usd(P_VPS0))),
              need("Country risk: by where it sells · the US", "%s or %s" % (usd(P_VPS), usd(P_VPS_US))),
              need("His industries’ return vs cost", "food %s vs %s" % (pct(FOOD["roc"], 1), pct(FOOD["wacc"], 2)), None, {"s": "Damodaran · EVA by sector", "u": DAM + "EVA.html"})],
    "rkey": [{"t": "Short answer", "l": [
        "The moat is worth %s a share; food makers as a group earn %s against a %s cost, so a modest edge is defensible." % (usd(P_VPS - P_VPS0), pct(FOOD["roc"], 0), pct(FOOD["wacc"], 2)),
        "Country risk is worth %s a share, %s KO’s %s, though PepsiCo sells %s of its revenue in North America. Its cost of capital sits closer to its growth (%s against %s, KO %s against %s), so each step in the discount rate moves its value more." % (usd(P_VPS_US - P_VPS), "more than" if P_VPS_US - P_VPS > VPS_US_ONLY - VPS_MOAT else "less than", usd(VPS_US_ONLY - VPS_MOAT), pct(PEP_SEG[0][1] / PEP_REV * 100, 0), pct(P["wacc"], 2), pct(P["g"] * 100, 2), pct(WACC, 2), pct(G * 100, 2))], **src(LIGHT)}]}
REV["L32"] = {"rev": "PEP",
    "rtask": "Give a value-vs-price verdict on PepsiCo, and check it against its peers.",
    "rneed": [need("Value · price", "%s to %s · $%.2f" % (usd(P_VPS0), usd(P_VPS), PEP_PRICE)),
              need("PepsiCo PE · EV/Sales", "%.1f · %.2f" % (P_PE, P_EVS), "Earnings per share $%.2f." % PEP_EPS, PEP_SRC),
              need("Food processing PE · EV/Sales", "%.2f · %.2f" % (FOOD["pe"], FOOD["evs"]), None, {"s": "Damodaran · PE and EV/Sales by sector", "u": DAM + "pedata.html"}),
              need("Soft drinks PE · EV/Sales", "%.2f · %.2f" % (BEV_PE_AGG, BEV_EVS), None, {"s": "Damodaran · PE and EV/Sales by sector", "u": DAM + "pedata.html"})],
    "rkey": [{"t": "Short answer", "l": [
        "Value %s to %s against $%.2f: %s." % (usd(P_VPS0), usd(P_VPS), PEP_PRICE, "expensive" if PEP_PRICE > P_VPS * 1.1 else ("cheap" if PEP_PRICE < P_VPS0 * 0.9 else "about fair, inside the range")),
        "Against peers: a PE of %.1f sits between food makers (%.1f) and soft drinks (%.1f); so does EV/Sales (%.2f). Priced like the mix it is." % (P_PE, FOOD["pe"], BEV_PE_AGG, P_EVS),
        "For the market to be right with the moat: growth of %s a year." % pct(P_G_IMPLIED * 100, 2)], **src(S14_REL)}]}

# NVIDIA's lessons, ten days later on AMD
REV["L18"] = {"rev": "AMD",
    "rtask": "AMD: which inputs would you spend your hour on, and which would you take from a table? Use the numbers, three lines.",
    "rneed": [need("Revenue 2024 → 2025", "%s → %s" % (B(AMD_REV[2024]), B(AMD_REV[2025])), "Data center %s → %s (+%s)." % (B(AMD_DC[2024]), B(AMD_DC[2025]), pct(gr(AMD_DC[2025], AMD_DC[2024]), 0)), AMD_SRC),
              need("Operating margin", pct(AMD_EBIT / AMD_REV[2025] * 100, 1), "%s before amortising what it paid for Xilinx." % pct(AMD_EBITA / AMD_REV[2025] * 100, 1), AMD_SRC),
              need("Semiconductors: margin · cost of capital", "%s · %s" % (pct(SEMI["margin"], 1), pct(SEMI["wacc"], 2)), None, {"s": "Damodaran · Margins and cost of capital by sector", "u": DAM + "wacc.html"})],
    "rkey": [{"t": "Short answer", "l": [
        "The hour goes on data-center growth and the margin. Closing a third of the gap to the industry’s margin (%s → %s) adds about %s of operating income a year." % (pct(AMD_EBITA / AMD_REV[2025] * 100, 0), pct((AMD_EBITA / AMD_REV[2025] * 100 * 2 + SEMI["margin"]) / 3, 0), B(AMD_REV[2025] * (SEMI["margin"] - AMD_EBITA / AMD_REV[2025] * 100) / 3 / 100)),
        "The cost of capital: take his industry’s %s and move on." % pct(SEMI["wacc"], 2)], **src(DEEPSEEK)}]}
REV["L19"] = {"rev": "AMD",
    "rtask": "Charge AMD for its 2025 growth two ways: capex minus depreciation, and sales-to-capital. Which do you believe?",
    "rneed": [need("Revenue growth 2025", B(AMD_GROWTH), None, AMD_SRC), need("Capex · depreciation", "%s · %s" % (M(AMD_CAPEX), M(AMD_DEP)), None, AMD_SRC),
              need("R&D", B(AMD_RND), None, AMD_SRC), need("Semiconductors: sales-to-capital", "%.2f" % SEMI["s2c"], None, {"s": "Damodaran · Capital expenditures by sector", "u": DAM + "capex.html"})],
    "rkey": [{"t": "Short answer", "l": [
        "Capex − depreciation: %s for %s of new revenue, a ratio of %.0f. Not believable: it misses R&D (%s)." % (M(AMD_NETCAPEX), B(AMD_GROWTH), AMD_GROWTH / AMD_NETCAPEX, B(AMD_RND)),
        "At the industry’s %.2f: %s of reinvestment; at 2.5, %s." % (SEMI["s2c"], B(AMD_GROWTH / SEMI["s2c"]), B(AMD_GROWTH / 2.5))], **src(NV2023)}]}
REV["L20"] = {"rev": "AMD",
    "rtask": "AMD: what return on capital does it earn, and what would analysts’ growth cost it? Why does buying Xilinx matter here?",
    "rneed": [need("Operating income · before Xilinx amortisation", "%s · %s" % (M(AMD_EBIT), M(AMD_EBITA)), None, AMD_SRC),
              need("Invested capital", M(AMD_IC), "Of which goodwill %s and intangibles %s, from buying Xilinx (2022)." % (B(AMD_GW), B(AMD_INTANG)), AMD_SRC),
              need("Analysts’ growth, semiconductors", pct(SEMI["growth"], 2), None, {"s": "Damodaran · PE and growth by sector", "u": DAM + "pedata.html"})],
    "rkey": [{"t": "Short answer", "l": [
        "On all its capital: %s after tax (%s before the amortisation). At that return, %s growth needs %s of earnings reinvested: impossible." % (pct(AMD_ROC * 100, 1), pct(AMD_ROC_A * 100, 1), pct(SEMI["growth"], 1), pct(SEMI["growth"] / (AMD_ROC_A * 100) * 100, 0)),
        "Without the Xilinx price: %s, needing %s. The acquisition is capital too (D-28): the growth story only works if new money earns far more than the old." % (pct(AMD_ROC_X * 100, 0), pct(SEMI["growth"] / (AMD_ROC_X * 100) * 100, 0))], **src(S9)}]}
REV["L21"] = {"rev": "AMD",
    "rtask": "AMD’s terminal value: growth capped at the riskfree rate, return on capital forever with or without an edge. What does the edge cost to assume?",
    "rneed": [need("Growth forever (riskfree)", pct(RF_NET, 2), None, src(DU2_2026)), need("Cost of capital forever", pct(R_MATURE * 100, 1), "His mature rate in the NVIDIA model.", {"s": "Damodaran · NvidiaJan2025.xlsx", "u": NV25_XLS}),
              need("Return forever: an edge · none", "%s · %s" % (pct(ROC_EDGE * 100, 0), pct(R_MATURE * 100, 1)), "15%: his figure for the big tech companies in 2024 (12% is his most common).")],
    "rkey": [{"t": "Short answer", "l": [
        "With a 15%% edge it reinvests %s of its income forever; with none, %s." % (pct(G_FOREVER / ROC_EDGE * 100, 0), pct(G_FOREVER / R_MATURE * 100, 0)),
        "Each dollar of year-11 income is then worth %.1f or %.1f dollars: the edge adds %s to the terminal value. Assume it only with a named advantage." % (tv_mult(ROC_EDGE), tv_mult(R_MATURE), pct((tv_mult(ROC_EDGE) / tv_mult(R_MATURE) - 1) * 100, 0))], **src(TV_MYTH5)}]}
REV["L27"] = {"rev": "AMD",
    "rtask": "If you built AMD a model like his NVIDIA one, which inputs would be judgements and which computations?",
    "rneed": [need("Segments 2025", "data center %s · client and gaming %s · embedded %s" % (B(AMD_DC[2025]), B(10640 + 3910), B(3454)), None, AMD_SRC),
              need("Margin · R&D share", "%s · %s" % (pct(AMD_EBITA / AMD_REV[2025] * 100, 1), pct(AMD_RND / AMD_REV[2025] * 100, 0)), None, AMD_SRC)],
    "rkey": [{"t": "Short answer", "l": [
        "Judgements: the AI-chip market and AMD’s share of it, the target margin, sales-to-capital, the cost of capital forever, any edge forever.",
        "Computations: revenue, operating income, tax path, reinvestment, discounting, the bridge to a share price."], **src(DEEPSEEK)}]}
REV["L29"] = {"rev": "AMD",
    "rtask": "Trace AMD’s three paths: tax, growth and return on capital. Where does each start, and where must it end?",
    "rneed": [need("Tax 2025", "%s on %s of profit" % (M(AMD_TAX), M(AMD_PRETAX)), "A tax credit, not a charge.", AMD_SRC),
              need("Revenue growth 2025", pct(gr(AMD_REV[2025], AMD_REV[2024]), 0), None, AMD_SRC),
              need("Return on capital", pct(AMD_ROC_A * 100, 1), "All capital, before Xilinx amortisation.")],
    "rkey": [{"t": "Short answer", "l": [
        "Tax: a negative rate can’t be carried: start at the 25% marginal rate (D-23).",
        "Growth: %s now, down to the riskfree rate by year 10." % pct(gr(AMD_REV[2025], AMD_REV[2024]), 0),
        "Return: %s today is below the cost of capital, so this path rises, if the new money earns more: the reverse of NVIDIA’s." % pct(AMD_ROC_A * 100, 1)], **src(DEEPSEEK)}]}
REV["L28"] = {"rev": "PEP vs AMD",
    "rtask": "Put PepsiCo (mature) next to AMD (high growth). Name three ways their models must differ.",
    "rneed": [need("PepsiCo: growth · margin", "%s · %s" % (pct(gr(PEP_REV, PEP_REV24), 1), pct(P_MARGIN, 1)), None, PEP_SRC),
              need("AMD: growth · margin", "%s · %s" % (pct(gr(AMD_REV[2025], AMD_REV[2024]), 0), pct(AMD_EBITA / AMD_REV[2025] * 100, 1)), None, AMD_SRC)],
    "rkey": [{"t": "Short answer", "l": [
        "Start: PepsiCo from today’s earnings; AMD from revenue, with a margin path to a target.",
        "Reinvestment: PepsiCo from net capex; AMD from sales-to-capital, R&D counted.",
        "Where the value sits: PepsiCo’s is already %s terminal at %s growth; for AMD the growth story, and how long it lasts, would carry even more of it." % (pct(P_TVS * 100, 0), pct(P["g"] * 100, 1))], **src(PAYTM_V)}]}

# Tesla's lessons, ten days later on BYD
REV["L16"] = {"rev": "BYD",
    "rtask": "BYD: a car maker, or a battery-and-electrics company? Build its bottom-up beta for each and set them beside its regression.",
    "rneed": [need("Car makers, global: unlevered beta", "%.2f" % G_AUTO["unlev"], "%d companies." % G_AUTO["n"], GLOBAL_SRC),
              need("Electrical equipment, global: unlevered beta", "%.2f" % G_ELEC["unlev"], "%s companies." % format(G_ELEC["n"], ","), GLOBAL_SRC),
              need("BYD debt · market value of equity", "CNY %s B · CNY %s B" % (format(round(BYD_DEBT / 1000), ","), format(round(BYD_E / 1000), ",")), "%s M shares × HK$%.2f × %.4f CNY per HKD." % (format(round(BYD_SHARES), ","), BYD_PRICE_HKD, HKD_CNY), BYD_SRC),
              need("China’s tax rate", "25%", None, {"s": "Damodaran · Country tax rates, January 2026", "u": CTRY}),
              need("Regression beta vs the Hang Seng", "%.2f" % BYD_REG, "Standard error %.2f; R² %.2f." % (BYD_REG_SE, BYD_R2), {"s": "Computed from Yahoo Finance prices", "u": yahoo("1211.HK")})],
    "rkey": [{"t": "Short answer", "l": [
        "Global tables: BYD is based outside the US, so his rule uses the global industries.",
        "Debt-to-equity %s. Car maker: %.2f; electrical equipment: %.2f." % (pct(BYD_DE * 100, 1), BYD_B_AUTO, BYD_B_ELEC),
        "Regression %.2f ± %.2f, against Hong Kong’s index, not the world’s. Use bottom-up." % (BYD_REG, 2 * BYD_REG_SE)], **src(DRM1)}]}
REV["L22"] = {"rev": "BYD",
    "rtask": "Is BYD cheap? Answer as a pricer against car makers, then say what a valuer would still need to know.",
    "rneed": [need("Revenue 2024 → 2025", "CNY %s B → %s B" % (format(round(BYD_REV[2024] / 1000), ","), format(round(BYD_REV[2025] / 1000), ",")), "Up %s, after +%s in 2024." % (pct(gr(BYD_REV[2025], BYD_REV[2024]), 1), pct(gr(BYD_REV[2024], BYD_REV[2023]), 0)), BYD_SRC),
              need("Operating margin · PE · EV/Sales", "%s · %.1f · %.2f" % (pct(BYD_MARGIN, 1), BYD_PE, BYD_EVS), "Price HK$%.2f; earnings CNY %.2f a share." % (BYD_PRICE_HKD, BYD_EPS), BYD_SRC),
              need("Car makers, global: EV/Sales · margin", "%.2f · %s" % (G_AUTO["evs"], pct(G_AUTO["margin"], 1)), None, GLOBAL_SRC),
              need("Capex · depreciation 2025", "CNY %s B · %s B" % (format(round(BYD_CAPEX / 1000), ","), format(round(BYD_DA / 1000), ",")), None, BYD_SRC)],
    "rkey": [{"t": "Short answer", "l": [
        "As a pricer: EV/Sales %.2f against %.2f for car makers, with a slightly higher margin. Cheap against its peers." % (BYD_EVS, G_AUTO["evs"]),
        "As a valuer you’d still need the story: does growth come back after 2025’s slowdown, and does capex of %s of revenue pay off? Pricing can’t answer that." % pct(BYD_CAPEX / BYD_REV[2025] * 100, 0)], **src(TSLA_DIY)}]}

# the produce lessons: no new company, the method from memory
REV["L33"] = {"rev": "your next company",
    "rtask": "From memory: the order you build a valuation in, with one rule for each step. Then name the step you’d most likely get wrong on your own company.",
    "rkey": [{"t": "Short answer", "l": [
        "Story (3P) → route → currency and riskfree rate → premium by where it sells → bottom-up beta → synthetic rating → market-weighted cost of capital.",
        "Clean base year → tax path → reinvestment (net capex or sales-to-capital) → growth = reinvestment × return → terminal (growth ≤ riskfree; return → cost of capital unless a moat).",
        "Cash, stakes, all debt, options → per share → a range → value vs price, and pricing vs peers."], "s": "His method: " + S11_LOOSE[0], "u": yt(S11_LOOSE[1])}]}
REV["L34"] = {"rev": "your next company",
    "rtask": "From memory: the parts of a valuation memo, and what each must contain.",
    "rkey": [{"t": "Short answer", "l": [
        "The story, graded. Three judgements, each with its rule and what it’s worth. A range, not a point. The verdict: value vs price, and pricing vs peers. What would have to be true for the market to be right."], **src(LIGHT)}]}

for lid, r in REV.items():
    L.setdefault(lid, {}).update(r)

# ---- walk-throughs for L02–L14: the method, then his own worked example, then your turn on KO ------
# One worked company throughout: his Alphabet valuation of March 2018 (blog post and spreadsheet), so the
# example never gives away a KO answer, a revisit company (PepsiCo, AMD, BYD) or a later lesson's case.
ALPHA_XLSX = "https://pages.stern.nyu.edu/~adamodar/pc/blog/AlphabetApr2018.xlsx"
ALPHA_PDF = "https://pages.stern.nyu.edu/~adamodar/pdfiles/blog/Google2018.pdf"
A_SRC = {"s": "Damodaran · Alphabet valuation, March 2018 (spreadsheet)", "u": ALPHA_XLSX}
A_BLOG = {"s": "Damodaran · Alphabet Soup: Mostly Google, but Lots of Bets! (2018)", "u": ALPHA_PDF}
EGP_SRC = {"s": "Damodaran · Session 12: Currencies & Exchange Rates (slides)", "u": "https://pages.stern.nyu.edu/~adamodar/pdfiles/FoundationsOnline/slides/session12.pdf"}
# his spreadsheet, $ million unless marked
A = dict(rev=110855, rev_prev=90272, ebit=26146, rd=16625, rd_amort=12020.67, rd_asset=30017.67, lease_adj=147.44,
         lease_debt=7620.50, debt_book=3969, debt_mkt=3601.69, eff=24.3, marg=25.0, s2c=2.030311, rf=2.75,
         regions=[("North America", 52449, 5.08), ("Europe", 36046, 6.0058), ("Asia", 16235, 6.05), ("Latin America", 6125, 8.7505)],
         biz=[("Advertising", 109652, 1.568262, 0.969156), ("Diversified", 1203, 1.688909, 0.758014)],
         shares=703, price=1050, ebit_cov=26293.44, int_cov=250.71, spread=0.54, wacc_t=8.0, roc_t=12.0, g5=12.0,
         rev1=124157.6, ebit1_at=26196.37, reinv1=6552.0, ebitT_at=57270.70, df10=0.4554548525, pv_cf=213889.62,
         cash=101871, trapped=60000, trapped_tax=15.0, roic=25.36, mroic=56.59, sim_median=957, sim_price=1030, p_over=65, limit=950)
A_REV_W = sum(r for _, r, _ in A["regions"])
A_ERP = sum(r * e for _, r, e in A["regions"]) / A_REV_W
A_VAL = [(n, r * m, b_) for n, r, m, b_ in A["biz"]]
A_BU = sum(v * b_ for _, v, b_ in A_VAL) / sum(v for _, v, _ in A_VAL)
A_E = A["shares"] * A["price"]
A_D = A["debt_mkt"] + A["lease_debt"]
A_DE = A_D / A_E
A_BL = A_BU * (1 + (1 - A["marg"] / 100) * A_DE)
A_COE = A["rf"] + A_BL * A_ERP
A_COV = A["ebit_cov"] / A["int_cov"]
A_KD = A["rf"] + A["spread"]
A_KD_AT = A_KD * (1 - A["marg"] / 100)
A_WE = A_E / (A_E + A_D)
A_WACC = A_WE * A_COE + (1 - A_WE) * A_KD_AT
A_RD_ADJ = A["rd"] - A["rd_amort"]
A_EBIT_ADJ = A["ebit"] + A_RD_ADJ + A["lease_adj"]
A_RIR_T = A["rf"] / A["roc_t"]
A_TFCF = A["ebitT_at"] * (1 - A_RIR_T)
A_TV = A_TFCF / ((A["wacc_t"] - A["rf"]) / 100)
A_PV_TV = A_TV * A["df10"]
A_OPS = A_PV_TV + A["pv_cf"]
A_TV0 = A["ebitT_at"] * (1 - A["rf"] / A["wacc_t"]) / ((A["wacc_t"] - A["rf"]) / 100)
A_MOAT_PS = (A_PV_TV - A_TV0 * A["df10"]) / A["shares"]
A_CASH = A["cash"] - A["trapped"] * (A["marg"] - A["trapped_tax"]) / 100
A_DEBT_OUT = A["debt_book"] + A["lease_debt"]
A_EQ = A_OPS - A_DEBT_OUT + A_CASH
A_VPS = A_EQ / A["shares"]
A_RR1 = A["reinv1"] / A["ebit1_at"]
# his own numbers come back: premium, beta, cost of equity and capital, base year, reinvestment, terminal value, value per share
for got, want, tol in ((A_ERP, 5.7259, 1e-3), (A_BU, 0.96669, 1e-4), (A_BL, 0.97771, 1e-4), (A_COE, 8.3483, 1e-3),
                       (A_COV, 104.874, 1e-2), (A_WACC, 8.2602, 1e-3), (A_EBIT_ADJ, 30897.77, 0.05),
                       ((A["rev1"] - A["rev"]) / A["s2c"], A["reinv1"], 0.05), (A_TFCF, 44146.16, 0.05), (A_TV, 840879.33, 1),
                       (A_PV_TV, 382982.57, 1), (A_CASH, 95871, 0.5), (A_VPS, 968.92, 0.01)):
    assert abs(got - want) < tol, (got, want)

def a_b(x): return B(x)          # Alphabet figures in billions, like KO's
WALK = {}
WALK["L02"] = [
    {"h": "Why the story comes first",
     "p": ["A spreadsheet will take any number you type. The story is what stops you typing nonsense: it says what the business is, so you can ask of every number whether it fits. Aswath’s warning cuts both ways. Number people hide behind precision; storytellers hide behind a big vision. You need both, and each keeps the other honest."]},
    {"h": "How he does it",
     "l": [["Tell it short.", "What the company sells, to whom, why they buy, who it competes with, where it is heading. Two or three sentences."],
           ["Grade it.", "Possible (could it happen at all?), plausible (has something like it happened?), probable (is it likely?). Only the probable part goes into the base case; plausible upsides go into a range."],
           ["Turn each part into an input.", "How big the market is and what share the company takes sets revenue. The business model sets the margin it settles at. How it grows sets reinvestment (L10). Whether it has a lasting edge sets the return on capital forever (L11–L12). How cyclical it is feeds risk (L03–L07)."],
           ["Check the loop.", "If a number doesn’t fit the story, one of them has to change."]]},
    {"h": "Where it goes wrong",
     "l": ["A story with no numbers attached, so nothing can be checked.",
           "Numbers that contradict the story: a ‘mature, steady’ story with 20% growth; a ‘light, asset-free’ story with heavy reinvestment.",
           "Putting a plausible upside into the base case because it is exciting."]},
    {"h": "Worked: his Alphabet, March 2018",
     "p": ["The facts he started from: digital ads were $228.4 billion of the $584 billion spent on advertising in 2017; Google took 42.2% of digital, Facebook 20.9%. His story: Google keeps taking share of a digital ad market that is slowing, privacy rules dull its edge, its other businesses add little for now, and it stays a low-cost, high-margin business."],
     "l": [["Revenue.", "12% a year for five years, below the 15% of the past five, because digital ads were already a large slice of all ads and privacy rules could bite."],
           ["Margin.", "Kept at %s, the margin it earned in 2017 once R&D is counted as an investment (L08): ‘business stays a low cost, high margin one’." % pct(A_EBIT_ADJ / A["rev"] * 100, 2)],
           ["Lasting edge.", "A return on capital of 12% forever, above its cost of capital (L07, L11–L12): ‘strong competitive advantages’."],
           ["Graded.", "YouTube taking on Spotify and Netflix was plausible, not probable, so he left it out of the base case and called it the upside."]],
     "p2": ["The one number he said the value hangs on: revenue growth, not the margin."],
     **A_BLOG},
    {"h": "Your turn: KO",
     "p": ["Use the numbers below: what KO sells and to whom, where, how much of the world’s drinking it already has, volume against revenue, its margins and its advertising. Write the story in two sentences, grade it, then decide which single number in KO’s valuation the story pins down most."]},
]
WALK["L03"] = [
    {"h": "Why the currency doesn’t matter, and consistency does",
     "p": ["A currency is a unit of measurement. Value a company in dollars and again in euros and you should get the same answer, because inflation shows up twice: in the cash flows (higher-inflation currencies have faster-growing numbers) and in the discount rate (their interest rates are higher too). Mix them, dollar cash flows with a euro rate, and the answer is meaningless."]},
    {"h": "How he picks the riskfree rate",
     "l": [["Same currency as the cash flows.", "Dollar cash flows, a dollar rate."],
           ["Long-term.", "A going business lasts decades, so use the 10-year government bond rate today, not an average and not a ‘normal’ rate."],
           ["Truly free of default.", "If the government can default, its bond rate includes a default spread. Subtract it."],
           ["No trustworthy bond?", "Build the rate from the dollar rate and the difference in expected inflation."]]},
    {"h": "Where it goes wrong",
     "l": ["Swapping in a rate you think of as ‘normal’ because today’s looks low or high: you are then betting on rates, not valuing a company.",
           "Taking a risky government’s bond rate as riskfree and counting the same risk again later, in the premium (L04)."]},
    {"h": "Worked: his examples",
     "l": [["Alphabet, March 2018.", "Dollars throughout; the 10-year US Treasury rate, 2.75%. The US was rated Aaa then, so there was nothing to take out."],
           ["The Egyptian pound, December 2015.", "No usable bond rate, so he built one: the dollar rate 2.27%, US inflation 1.5%, Egyptian inflation 9.7%. Riskfree rate in pounds = 1.0227 × (1.097 ÷ 1.015) − 1 = 10.53%. The extra 8 points is inflation, not risk."]],
     **EGP_SRC},
    {"h": "Your turn: KO",
     "p": ["KO reports in dollars. Take the 10-year Treasury rate below and decide what to do about the US default spread, the one problem his 2018 Alphabet valuation didn’t have. Then weigh which choice could move KO’s value more: the currency or the rate."]},
]
WALK["L04"] = [
    {"h": "What the premium is",
     "p": ["The equity risk premium is the extra return investors want for owning stocks rather than the riskfree bond. It is one number for the whole market, set by investors today, and it applies to every company before you adjust for how risky that company is (L05)."]},
    {"h": "How he does it",
     "l": [["Start from the implied premium.", "The return that makes the index’s expected cash payouts (dividends and buybacks) worth today’s index level, minus the riskfree rate. It is today’s price of risk, not a historical average."],
           ["Add country risk where the company operates.", "Riskier markets carry an extra premium. What counts is where the company sells, not where it is incorporated."],
           ["Weight by revenue.", "Multiply each region’s premium by its share of the company’s revenue and add up."]]},
    {"h": "Where it goes wrong",
     "l": ["Using the premium of the country of incorporation: a US company that sells half its products in emerging markets is not a pure US risk.",
           "Using a historical average, which depends on the years you pick (L15)."]},
    {"h": "Worked: his Alphabet, March 2018",
     "p": ["The US premium then was %s. Alphabet’s revenue by region, each with its premium:" % pct(A["regions"][0][2], 2)],
     "l": ["%s: %s of revenue at %s" % (n, pct(r / A_REV_W * 100, 1), pct(e, 2)) for n, r, e in A["regions"]],
     "p2": ["Weighted: %s. Higher than the US premium alone, because half of Alphabet’s revenue comes from outside North America. That is the number that goes into its cost of equity (L05)." % pct(A_ERP, 2)],
     **A_SRC},
    {"h": "Your turn: KO",
     "p": ["KO’s numbers below give each operating segment’s share of revenue and premium. Weight them the same way. Then judge which input you would fight hardest to get right."]},
]
WALK["L05"] = [
    {"h": "What beta measures",
     "p": ["Beta is how much a company’s stock moves with the market. A beta of 1 is average risk; 0.6 moves about 60% as much as the market; 1.5 moves 50% more. Multiply it by the risk premium (L04) and you have the company’s extra return over the riskfree rate: cost of equity = riskfree rate + beta × premium."]},
    {"h": "Why not the regression",
     "p": ["The obvious way, regressing the stock’s returns on the market’s, gives a number with a wide margin of error, set by the past five years and by the company’s old debt and old businesses. Averaging across many companies in the same business cancels most of that noise."]},
    {"h": "How he builds it bottom-up",
     "l": [["Name the businesses.", "By how the company makes money."],
           ["Take each business’s unlevered beta.", "The average for many companies in that business, with their debt taken out, from his industry tables."],
           ["Weight by value.", "Revenue × what investors pay for each dollar of that business’s sales (EV/Sales, more in L22)."],
           ["Put this company’s debt back in.", "Levered beta = unlevered beta × (1 + (1 − tax rate) × debt-to-equity), with debt and equity at market value."]]},
    {"h": "Worked: his Alphabet, March 2018",
     "l": ["%s: revenue %s × %.2f = %s of value, unlevered beta %.2f" % (n, M(r), m, a_b(r * m), b_) for n, r, m, b_ in A["biz"]],
     "p2": ["Weighted by value: %.4f. Debt (leases included, L06) of %s against equity of %s: a debt-to-equity of %s. Levered beta = %.4f × (1 + 0.75 × %.4f) = %.2f. Cost of equity = %s + %.2f × %s = %s." % (A_BU, a_b(A_D), a_b(A_E), pct(A_DE * 100, 2), A_BU, A_DE, A_BL, pct(A["rf"], 2), A_BL, pct(A_ERP, 2), pct(A_COE, 2))],
     **A_SRC},
    {"h": "Your turn: KO",
     "p": ["KO is one business, so there is nothing to weight: take the soft-drinks unlevered beta and put KO’s own debt back in. Then set the result beside KO’s regression beta and decide which you’d trust, and when the regression would be the better number."]},
]
WALK["L06"] = [
    {"h": "What the cost of debt is",
     "p": ["What the company would pay to borrow long-term today. Not the coupon on bonds it issued years ago, and not interest expense divided by debt: both look backward. It is the riskfree rate plus a default spread for how likely the company is to fail to pay."]},
    {"h": "How he does it",
     "l": [["Get a rating.", "Use the actual one if it has one. Either way, also make a synthetic one: interest coverage = operating income ÷ interest expense, then read the rating and its default spread off his table. Safer coverage, smaller spread."],
           ["Add it up.", "Pre-tax cost of debt = riskfree rate + default spread (+ part of the country’s spread, if the company carries that risk)."],
           ["Count all the debt.", "Leases and other fixed commitments are debt: discount the future lease payments at the pre-tax cost of debt and add the result to debt."],
           ["Take the tax off.", "Interest saves tax at the rate on the last dollar of profit, the marginal tax rate (L09): after-tax cost = pre-tax × (1 − marginal rate)."]]},
    {"h": "Where it goes wrong",
     "l": ["Leaving leases out, which understates debt and makes the company look safer than it is.",
           "Using the effective tax rate (L09) for the tax saving."]},
    {"h": "Worked: his Alphabet, March 2018",
     "p": ["Alphabet barely borrowed: its only interest was the interest built into its leases. Its lease commitments, discounted at the pre-tax cost of debt, were worth %s, against %s of ordinary debt. Coverage: operating income %s ÷ interest %s = %.0f times, far above his top band (8.5): AAA, a %s spread. Pre-tax cost of debt %s + %s = %s; after tax at 25%%, %s. Its actual rating was AA; he used the synthetic one." % (a_b(A["lease_debt"]), a_b(A["debt_book"]), M(A["ebit_cov"]), M(A["int_cov"]), A_COV, pct(A["spread"], 2), pct(A["rf"], 2), pct(A["spread"], 2), pct(A_KD, 2), pct(A_KD_AT, 2))],
     **A_SRC},
    {"h": "Your turn: KO",
     "p": ["KO does borrow. Work out its coverage from the numbers below, read off the rating and spread, and compare with KO’s actual rating. Then add the leases and decide which moves KO’s cost of capital (L07) more: the rating or the leases."]},
]
WALK["L07"] = [
    {"h": "What the cost of capital is",
     "p": ["A company is paid for by its owners and its lenders, and each wants a return. The cost of capital is the blend: cost of equity × the equity’s share + after-tax cost of debt × the debt’s share. It is the rate that turns the company’s future cash into today’s value."]},
    {"h": "How he weights it",
     "l": [["Market values, never book.", "Equity at shares × price; debt at its market value, leases included. Book equity is an accounting leftover; investors want a return on what the company is worth today."],
           ["One number for the whole company.", "Built from its business mix and its debt. For a single division or a new project, use that thing’s own risk instead."]]},
    {"h": "Where it goes wrong",
     "l": ["Book-value weights. For a company whose market value is far above its book value, they make debt look much bigger than it is.",
           "Using the company-wide number for a division that is riskier or safer than the average."]},
    {"h": "Worked: his Alphabet, March 2018",
     "p": ["Equity %s (703 million shares × $1,050), debt %s: %s equity, %s debt. Cost of capital = %s × %s + %s × %s = %s. With so little debt, it is nearly the cost of equity." % (a_b(A_E), a_b(A_D), pct(A_WE * 100, 1), pct((1 - A_WE) * 100, 1), pct(A_WE * 100, 1), pct(A_COE, 2), pct((1 - A_WE) * 100, 1), pct(A_KD_AT, 2), pct(A_WACC, 2))],
     **A_SRC},
    {"h": "Your turn: KO",
     "p": ["KO carries real debt. Weight its cost of equity and after-tax cost of debt by market values, then redo it with book values and see how far the answer moves. Compare with his soft-drinks average."]},
]
WALK["L08"] = [
    {"h": "Why the base year needs cleaning",
     "p": ["Every forecast grows from this year’s operating income, so an error here carries into every year after it. Accounting puts some spending in the wrong place, in directions you can predict, and the job is to put it back."]},
    {"h": "How he does it",
     "l": [["Three boxes.", "Every expense is operating (it helps this year), capital (it helps for years) or financing (it comes from borrowing). Move anything in the wrong box."],
           ["R&D is capital.", "It builds an asset. Add this year’s R&D back to operating income, subtract the amortisation of past years’ R&D, and count the research asset as invested capital."],
           ["One-offs: genuine or recurring?", "Add back a charge that won’t return. A ‘one-off’ that comes back every few years is a cost: spread it over the years instead."],
           ["Negative earnings: ask why first.", "A one-off, a cycle (average the margin over it), a young company (aim at what mature peers earn) or a broken business (a story and a real chance of failure)."]]},
    {"h": "Worked: his Alphabet, March 2018",
     "p": ["Reported operating income %s on revenue of %s: a %s margin. R&D: %s this year, spread over three years; amortisation of the past three years’ R&D %s. Adjustment: %s. Leases moved to debt (L06) add %s more. Clean operating income: %s, a margin of %s. The research asset, %s, joins invested capital." % (M(A["ebit"]), M(A["rev"]), pct(A["ebit"] / A["rev"] * 100, 1), M(A["rd"]), M(A["rd_amort"]), "+" + M(A_RD_ADJ), M(A["lease_adj"]), M(A_EBIT_ADJ), pct(A_EBIT_ADJ / A["rev"] * 100, 1), M(A["rd_asset"]))],
     **A_SRC},
    {"h": "Your turn: KO",
     "p": ["KO reports no R&D, so the cleanup that mattered most for Alphabet doesn’t apply. KO’s question is its ‘other operating charges’: look at 2025 and 2024 side by side and decide whether they are one-off or a recurring cost of doing business."]},
]
WALK["L09"] = [
    {"h": "Two rates, two jobs",
     "l": [["Effective rate.", "The income tax in the accounts ÷ profit before tax, for the same year. What the company really pays now, after credits, deferrals and lower rates abroad. Use it to tax operating income at the start."],
           ["Marginal rate.", "The legal rate on the last dollar of profit. Use it for the tax that interest saves (L06), and as the rate the forecast ends at, because breaks and deferrals don’t last forever."]]},
    {"h": "How he does it",
     "l": [["The path.", "Hold the effective rate for years 1–5, step it to the marginal rate in equal steps over years 6–10, and use the marginal rate after year 10, in the terminal value (L12)."],
           ["Tax as if there were no debt.", "Operating income × (1 − tax rate). The interest saving is already in the after-tax cost of debt; counting it here too counts it twice."],
           ["Losses carried forward.", "Keep a running balance: income they shelter pays no tax until they are used up."]]},
    {"h": "Worked: his Alphabet, March 2018",
     "p": ["Effective rate %s for years 1–5; then %s, %s, %s, %s; %s in year 10 and after. The tax saving on its debt used 25%%. No losses carried forward." % (pct(A["eff"], 1), pct(24.44, 2), pct(24.58, 2), pct(24.72, 2), pct(24.86, 2), pct(A["marg"], 0))],
     **A_SRC},
    {"h": "Your turn: KO",
     "p": ["KO’s effective rate is well below the marginal rate. Set its path, check for losses carried forward, then weigh whether the tax path or the base-year cleanup (L08) moves KO’s value more."]},
]
WALK["L10"] = [
    {"h": "Why reinvestment is the bill for growth",
     "p": ["A company can’t grow without spending: plants, equipment, research, acquisitions, stock on the shelves. Reinvestment is everything it spends to grow, net of what simply replaces what wears out. Forget it and you have assumed growth for free."]},
    {"h": "Two ways to measure it",
     "l": [["From the accounts.", "Net capex = capital spending − depreciation + R&D that you capitalised (L08) + acquisitions, including ones paid in stock + leases. Add the change in non-cash working capital: operating current assets minus non-debt current liabilities."],
           ["From the growth.", "For a fast-growing or young company the past is a poor guide, so tie reinvestment to the growth you forecast with a sales-to-capital ratio: reinvestment = the extra revenue ÷ the ratio. A ratio of 3 means each $1 of new capital brings $3 of new revenue."]]},
    {"h": "Where it goes wrong",
     "l": ["Growth with no reinvestment behind it.", "Using one lumpy year of capital spending as if it were normal."]},
    {"h": "Worked: his Alphabet, March 2018",
     "p": ["He drove it from revenue, using Alphabet’s own sales-to-capital ratio, %.2f, for all ten years. Year 1: revenue grows from %s to %s, so reinvestment = %s ÷ %.2f = %s. As growth slows after year 5, the bill shrinks with it. His reason, in the story sheet: ‘reinvestment will be in technology and in occasional acquisitions’." % (A["s2c"], M(A["rev"]), M(A["rev1"]), M(A["rev1"] - A["rev"]), A["s2c"], M(A["reinv1"]))],
     **A_SRC},
    {"h": "Your turn: KO",
     "p": ["Build KO’s reinvestment both ways: from capital spending, depreciation, acquisitions and working capital, then from his soft-drinks sales-to-capital and KO’s revenue growth. Decide which fits a company like KO, and when you would switch to the other."]},
]
WALK["L11"] = [
    {"h": "Growth has to be paid for",
     "p": ["The identity: growth in operating income = reinvestment rate × return on capital. Reinvestment rate = reinvestment ÷ after-tax operating income; return on capital = after-tax operating income ÷ invested capital. A company that reinvests half its after-tax income at 12% grows about 6% a year."]},
    {"h": "How he uses it",
     "l": [["As the growth, for a steady company.", "Measure the two parts and multiply."],
           ["As a check, for a changing one.", "When margins are still moving, choose revenue growth from the story and charge it through sales-to-capital (L10); then ask what return on new capital that growth needs."],
           ["Analysts as a cross-check only.", "Their forecasts look a few years ahead, follow each other and echo the company."],
           ["The shape.", "Years 2–5 at the chosen growth, years 6–10 stepping down in five equal steps, growth forever from year 11 (L12)."]]},
    {"h": "Worked: his Alphabet, March 2018",
     "p": ["He chose 12%% revenue growth for five years, against 15%% over the past five and %s in the latest year, then stepped it down to 2.75%% by year 10. The check: in year 1 Alphabet reinvests %s of %s after-tax operating income, a reinvestment rate of %s. To grow 12%% on that, each new dollar must earn about %s (12 ÷ %.2f). His story sheet shows the return on new capital the forecast implies, %s, against %s on existing capital. That high bar is the price of the growth he assumed." % (pct((A["rev"] / A["rev_prev"] - 1) * 100, 1), M(A["reinv1"]), M(A["ebit1_at"]), pct(A_RR1 * 100, 0), pct(12 / A_RR1, 0), A_RR1, pct(A["mroic"], 1), pct(A["roic"], 1))],
     **A_SRC},
    {"h": "Your turn: KO",
     "p": ["Measure KO’s reinvestment rate and return on capital from the numbers below and multiply. Set the result beside his soft-drinks figure, decide which goes in the model, then judge how fast KO’s growth needs to fade."]},
]
WALK["L12"] = [
    {"h": "Why a terminal value",
     "p": ["You can’t forecast forever, so after year 10 one number captures all the years after: the terminal value. It is usually most of the value, which is why it needs the most care."]},
    {"h": "His two caps",
     "l": [["Growth forever ≤ the riskfree rate.", "No company can outgrow the economy forever, and the riskfree rate is his stand-in for the economy’s long-run growth."],
           ["Return on capital forever → the cost of capital.", "Competition wears down excess returns. Keep them above the cost of capital only if you can name the moat that protects them."],
           ["Reinvestment follows.", "Reinvestment rate = growth ÷ return on capital. Year 11 cash flow = after-tax operating income × (1 − reinvestment rate). Terminal value = that cash flow ÷ (cost of capital − growth)."],
           ["Never end on a multiple.", "Ending with ‘ten times earnings’ is pricing, what the market pays for similar companies (L22), dressed up as a DCF."]]},
    {"h": "Worked: his Alphabet, March 2018",
     "p": ["Growth forever 2.75%%, the riskfree rate. Cost of capital after year 10: 8%%. Return on capital forever: 12%%, above 8%%, for ‘strong competitive advantages’. Reinvestment rate = 2.75 ÷ 12 = %s. Year 11: %s × (1 − %s) = %s. Terminal value = %s ÷ (8%% − 2.75%%) = %s, worth %s today: %s of the operating value." % (pct(A_RIR_T * 100, 1), M(A["ebitT_at"]), pct(A_RIR_T * 100, 1), M(A_TFCF), M(A_TFCF), a_b(A_TV), a_b(A_PV_TV), pct(A_PV_TV / A_OPS * 100, 0)),
           "What the moat was worth: with the return falling to 8%%, reinvestment rises to %s and the value drops by about $%.0f a share." % (pct(A["rf"] / A["wacc_t"] * 100, 1), A_MOAT_PS)],
     **A_SRC},
    {"h": "Your turn: KO",
     "p": ["Set KO’s growth forever under the cap and choose its return on capital forever: can you name KO’s moat? Then find what share of KO’s value sits in the terminal value."]},
]
WALK["L13"] = [
    {"h": "From the business to the shares",
     "p": ["The DCF values the operating business. The shareholders own that, plus everything outside it, minus every other claim ahead of them."]},
    {"h": "How he does it",
     "l": [["Add cash.", "At face value: ‘cash is cash’. Less any tax still due to bring it home."],
           ["Add stakes in other companies.", "Their income isn’t in operating income, so value them separately: listed ones at market price."],
           ["Subtract all the debt.", "Borrowings, leases, unfunded pensions. And the minority interest: the outsiders’ share of subsidiaries counted at 100%."],
           ["Subtract employee options.", "Value them as options and subtract; then divide by the shares actually outstanding."]]},
    {"h": "Worked: his Alphabet, March 2018",
     "p": ["Operating value %s. Minus debt, leases included: %s. Plus cash: %s, less the extra US tax on the %s held abroad, %s × (25%% − 15%%) = %s, leaving %s. No stakes, no minority interest, no options outstanding. Equity: %s. Per share: ÷ 703 million = %s." % (a_b(A_OPS), a_b(A_DEBT_OUT), a_b(A["cash"]), a_b(A["trapped"]), a_b(A["trapped"]), a_b(A["cash"] - A_CASH), a_b(A_CASH), a_b(A_EQ), usd(A_VPS))],
     **A_SRC},
    {"h": "Your turn: KO",
     "p": ["KO has more loose ends than Alphabet: listed stakes in its bottlers, a minority interest, employee options. Walk from operating value to equity with the numbers below, and find which loose end moves KO’s value per share most."]},
]
WALK["L14"] = [
    {"h": "From a value to a verdict",
     "p": ["A single value per share pretends to know more than you do. The honest output is a range, and a comparison with the price that says what would have to be true for the market to be right."]},
    {"h": "How he does it",
     "l": [["Point value.", "Equity ÷ shares."],
           ["A range.", "Give the uncertain inputs, growth, margin and reinvestment, a distribution and run the valuation thousands of times: a simulation. The spread of results shows how much you really know."],
           ["Against the price.", "If they differ, either you are right and the market is wrong, or the other way round. Name the inputs the gap depends on."]]},
    {"h": "Worked: his Alphabet, March 2018",
     "p": ["His point value: %s a share, against $%s when he built the spreadsheet. His simulation: a median of $%d; at a price of $%s, a %d%% chance the stock was overvalued, with more room above than below. The input it hinged on: revenue growth. His verdict: the closest he had come to owning it, with an order to buy at $%d." % (usd(A_VPS), format(A["price"], ","), A["sim_median"], format(A["sim_price"], ","), A["p_over"], A["limit"])],
     **A_BLOG},
    {"h": "Your turn: KO",
     "p": ["Divide KO’s equity by its shares, once with a moat and once without, and set both against the price. Name the three inputs that drive the spread, and say what would have to be true for the market to be right."]},
]
IDEA = {
    "L02": "A valuation is a bridge between a story and numbers. Tell the story first, grade it possible, plausible or probable, and let only the probable part set the numbers. When a number and the story disagree, one of them has to change.",
    "L03": "Value the company in one currency and keep everything in it, cash flows and discount rate alike. The riskfree rate is today’s long-term government bond rate in that currency, with any government default spread taken out.",
    "L04": "The equity risk premium is the extra return investors demand for owning stocks: use today’s implied premium, not a historical average. Add country risk for where the company sells, weighted by its revenue there.",
    "L05": "Beta measures how much a company moves with the market. Build it bottom-up from the businesses the company is in, then put its own debt back in; one company’s regression beta is too noisy to trust.",
    "L06": "The cost of debt is what the company would pay to borrow long-term today: the riskfree rate plus a default spread from its rating, real or synthetic. Leases are debt, and the tax saving uses the marginal rate (L09).",
    "L07": "The cost of capital blends the cost of equity and the after-tax cost of debt, weighted by market values, never book values. One number for the company as a whole; a division or a project gets its own.",
    "L08": "Clean the base year before you forecast from it: put every expense in the right box, capitalise R&D, and add back only true one-offs. Every later year grows from this number.",
    "L09": "Tax operating income at the effective rate now and walk it to the marginal rate by year 10. The marginal rate also sets the tax that interest saves, and losses carried forward shelter income until they run out.",
    "L10": "Reinvestment is the bill for growth: net capital spending, acquisitions and working capital. For a fast-growing company, tie it to the growth with a sales-to-capital ratio instead of trusting the past.",
    "L11": "Growth has to be earned: growth = reinvestment rate × return on capital. It is the growth for a steady company and the check on the growth you chose for a changing one; analysts’ forecasts are a cross-check, never the input.",
    "L12": "After year 10 a terminal value closes the model, and it is usually most of the value. Growth forever no higher than the riskfree rate, return on capital forever at the cost of capital unless you can name a moat, and reinvestment that follows from the two.",
    "L13": "The DCF values the operating business. To reach the shares, add cash and stakes in other companies, subtract all the debt, the minority interest and employee options, and divide by the shares outstanding.",
    "L14": "A value per share is a range, not a point: simulate the uncertain inputs and see how wide the range is. Then set it against the price and say what would have to be true for the market to be right.",
}
for lid, w in WALK.items():
    L.setdefault(lid, {})["walk"] = w
for lid in ("L03", "L04"):
    L[lid]["teach"] = IDEA[lid]


# ---- the thread: what each lesson builds on (with the number it carries in) and where its result goes --
# Shown at the top of the Learn step. "b" never states today's answer: only numbers from lessons already done.
THREAD = {
    "L01": {"n": "L02 · KO’s story. Then L03–L14 build KO’s valuation on the route you pick here, one part per lesson; L28 comes back to routing once you’ve built one"},
    "L02": {"b": "L01 · KO routes as mature: today’s operating income is a fair start",
            "n": "L03–L14 · every number in KO’s valuation has to agree with this story"},
    "L03": {"b": "L02 · KO sells in about 200 countries and reports in dollars",
            "n": "L04–L07 · the riskfree rate is the floor under every return in KO’s cost of capital"},
    "L04": {"b": "L03 · KO’s riskfree rate, %s after the US default spread" % pct(RF_NET, 2),
            "n": "L05 · beta scales this premium to KO; L07 · the cost of capital; L15 · you defend it"},
    "L05": {"b": "L03–L04 · riskfree rate %s; KO’s premium %s, weighted by where it sells" % (pct(RF_NET, 2), pct(KO_ERP, 2)),
            "n": "L07 · cost of equity = %s + beta × %s; L16 · you defend bottom-up against regression" % (pct(RF_NET, 2), pct(KO_ERP, 2))},
    "L06": {"b": "L03 · riskfree rate %s; L05 · KO’s debt %s, a debt-to-equity of %s" % (pct(RF_NET, 2), B(D_M), pct(DE * 100, 1)),
            "n": "L07 · the debt side of KO’s cost of capital"},
    "L07": {"b": "L05 · cost of equity %s (%s + %.2f × %s); L06 · after-tax cost of debt %s" % (pct(COE, 2), pct(RF_NET, 2), BETA_L, pct(KO_ERP, 2), pct(KD_AT, 2)),
            "n": "L12–L14 · the rate that turns KO’s future cash into today’s value"},
    "L08": {"b": "L02 · the story says KO’s margin is its key number",
            "n": "L09 · you tax it; L10–L11 · KO reinvests and grows from it"},
    "L09": {"b": "L08 · KO’s clean operating income, %s" % B(EBIT_CLEAN),
            "n": "L10–L12 · KO reinvests and grows from its after-tax operating income"},
    "L10": {"b": "L09 · KO’s after-tax operating income, %s at a %s effective tax rate" % (B(EBIT_AT), pct(EFF, 1)),
            "n": "L11 · growth = reinvestment rate × return on capital"},
    "L11": {"b": "L10 · KO reinvests %s of its after-tax operating income" % pct(RR * 100, 1),
            "n": "L12 · growth fades to growth forever; L20 · you defend earned growth"},
    "L12": {"b": "L07 · cost of capital %s; L11 · growth %s, from %s reinvested at a %s return on capital" % (pct(WACC, 2), pct(G * 100, 1), pct(RR * 100, 1), pct(ROC * 100, 1)),
            "n": "L13 · from operating value to equity; L21 · you defend the caps"},
    "L13": {"b": "L12 · KO’s operating value, %s with a moat" % B(OPS_MOAT),
            "n": "L14 · value per share, against the price"},
    "L14": {"b": "L12–L13 · KO’s operating value, then cash, stakes, debt and options",
            "n": "L22 · value and price as two games; L30–L32 · what moves it, and your verdict"},
    "L15": {"b": "L04 · his implied premium: %s over the riskfree rate, %s once the US default spread is out" % (pct(ERP_NET, 2), pct(MATURE_ERP, 2)),
            "n": "L24 · you rebuild KO’s cost of capital in one go"},
    "L16": {"b": "L05 · KO’s bottom-up beta %.2f, against its regression beta %.2f" % (BETA_L, REG_BETA),
            "n": "L24 · KO’s cost of capital end to end"},
    "L17": {"b": "L03 · currency and riskfree rate; L12 · growth forever capped at the riskfree rate",
            "n": "L24 · one consistent set of inputs"},
    "L18": {"b": "L03–L14 · KO’s inputs: the discount rate (L03–L07) and the cash flows (L08–L12)",
            "n": "L25 · where your hour goes on KO; L30 · you test the claim on KO"},
    "L19": {"b": "L10 · KO’s reinvestment from net capex, %s" % B(NETCAPEX),
            "n": "L25–L26 · reinvestment in a full run; L28 · how the route changes it"},
    "L20": {"b": "L11 · KO’s growth, earned: %s × %s ≈ %s" % (pct(RR * 100, 1), pct(ROC * 100, 1), pct(G * 100, 1)),
            "n": "L26 · growing KO’s cash flows"},
    "L21": {"b": "L12 · %s of KO’s operating value sits in the terminal value" % pct(TVS_MOAT * 100, 0),
            "n": "L26 · closing out the model"},
    "L22": {"b": "L14 · KO’s value, %s a share with a moat, against a price of %s" % (usd(VPS_MOAT), usd(KO_PRICE)),
            "n": "L32 · your verdict holds both halves"},
    "L23": {"b": "L03–L14 · KO’s whole valuation, %s a share" % usd(VPS_MOAT),
            "n": "L24–L27 · you run each part end to end"},
    "L24": {"b": "L03–L07 · the pieces; L15–L17 · their defences",
            "n": "L33 · your own company’s cost of capital"},
    "L25": {"b": "L08–L10 · base year, tax and reinvestment; L18–L19 · where valuations fail",
            "n": "L33 · your own company’s cash flows"},
    "L26": {"b": "L11–L12 · growth and terminal value; L20–L21 · their defences",
            "n": "L33 · closing out your own valuation"},
    "L27": {"b": "L23–L26 · your own end-to-end run on KO",
            "n": "L28–L29 · comparing models"},
    "L28": {"b": "L01 · the four routes; L23–L27 · KO’s mature model, end to end",
            "n": "L33 · route your own company first"},
    "L29": {"b": "L09, L11, L12 · KO’s tax, growth and return on capital",
            "n": "L33 · paths, not constants, in your own model"},
    "L30": {"b": "L14 · KO’s value, %s a share" % usd(VPS_MOAT),
            "n": "L31 · you defend the input that moves it most"},
    "L31": {"b": "L30 · the inputs that move KO’s value most",
            "n": "L32 · the verdict rests on it"},
    "L32": {"b": "L22 · valuing vs pricing; L30–L31 · what moves KO’s value, and your defended choice",
            "n": "L34 · the memo’s verdict"},
    "L33": {"b": "L01–L32 · the whole method, with KO as your worked example",
            "n": "L34 · writing it up"},
    "L34": {"b": "L33 · your own valuation",
            "n": "the next company, which goes faster"},
}
for lid, th in THREAD.items():
    L.setdefault(lid, {})["thread"] = th

# ---- terms before they're taught ------------------------------------------------------------------
# Each term and the lesson that teaches it. Learn text (the idea, the walk-through, the thread) may use a
# term from a later lesson only with a pointer to that lesson in the same sentence, e.g. "(L05–L07)".
GLOSSARY = [
    (3, "riskfree rate", r"risk-?free rate"),
    (3, "default spread", r"default spread"),
    (4, "equity risk premium", r"risk premium|implied premium|(?-i:\bERP\b)"),
    (4, "country risk", r"country risk"),
    (5, "beta", r"\bbetas?\b"),
    (5, "unlevered / relevered", r"\b(?:un|re)lever"),
    (5, "debt-to-equity", r"debt-to-equity|(?-i:\bD/E\b)"),
    (5, "cost of equity", r"cost of equity"),
    (6, "cost of debt", r"cost of debt"),
    (6, "synthetic rating", r"synthetic rating|interest coverage"),
    (6, "leases as debt", r"\bleases?\b"),
    (7, "cost of capital", r"cost of capital|(?-i:\bWACC\b)"),
    (7, "market-value weights", r"market[- ]value weights"),
    (8, "one-off charges", r"one-off"),
    (8, "capitalising", r"capitali[sz]"),
    (8, "normalising", r"normali[sz]"),
    (9, "effective tax rate", r"effective (?:tax )?rate"),
    (9, "marginal tax rate", r"marginal (?:tax )?rate"),
    (9, "losses carried forward", r"carried forward|carry[- ]?forward|(?-i:\bNOLs?\b)"),
    (10, "net capex", r"net capex|capital expenditure"),
    (10, "working capital", r"working capital"),
    (10, "sales-to-capital", r"sales[- ]to[- ]capital"),
    (11, "return on capital", r"return on capital|(?-i:\bROIC\b)"),
    (11, "reinvestment rate", r"reinvestment rate"),
    (12, "terminal value", r"\bterminal\b"),
    (12, "growth forever", r"growth forever|stable growth"),
    (12, "moat", r"\bmoats?\b"),
    (12, "excess returns", r"excess returns?"),
    (13, "minority interest", r"minority (?:interest|stake)"),
    (13, "cross-holdings", r"cross-holding"),
    (13, "employee options", r"\boptions\b"),
    (13, "value per share", r"value per share"),
    (14, "simulation", r"monte carlo|simulation"),
    (22, "pricing", r"\bpricing\b"),
    (22, "multiples", r"\bmultiples\b|(?-i:\bPE\b)|EV/Sales|price-to-book"),
]
POINTER = re.compile(r"\bL(\d\d)(?:\s*[–-]\s*L(\d\d))?")

def learn_texts(html):
    """The investing Learn step, lesson by lesson: the idea (VAL_KO's, else VAL_TEACH's), the walk-through, the thread."""
    i = html.index("var VAL_TEACH=")
    teach = json.loads(html[i + len("var VAL_TEACH="):html.index("\n  };", i) + 4])
    out = {}
    for n in range(1, 35):
        lid = "L%02d" % n
        x = L.get(lid, {})
        parts = [("idea", x.get("teach") or teach.get(lid, {}).get("teach", ""))]
        for s in x.get("walk", []):
            parts += [("walk", s["h"])] + [("walk", q) for q in s.get("p", []) + s.get("p2", [])]
            parts += [("walk", " ".join(it) if isinstance(it, list) else it) for it in s.get("l", [])]
        parts += [("thread", x["thread"][k]) for k in ("b", "n") if x.get("thread", {}).get(k)]
        out[lid] = parts
    return out

def term_order(html):
    flags = []
    for lid, parts in learn_texts(html).items():
        n = int(lid[1:])
        for where, text in parts:
            for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z‘“(])", text):
                ptrs = [(int(a), int(b or a)) for a, b in POINTER.findall(sent)]
                for intro, name, rx in GLOSSARY:
                    if intro > n and re.search(rx, sent, re.I) and not any(a <= intro <= b for a, b in ptrs):
                        flags.append("%s %s: “%s” is taught in L%02d — %s" % (lid, where, name, intro, sent[:110]))
    return flags

# ---- checks -------------------------------------------------------------------------------------
def check():
    vids = set()
    if os.path.exists(LIBRARY):
        lib = json.load(open(LIBRARY))
        vids = set((lib.get("videos", lib)).keys())
    for lid, x in L.items():
        for item in x.get("need", []) + x.get("key", []) + x.get("rneed", []) + x.get("rkey", []):
            u = item.get("u", "")
            m = re.search(r"v=([\w-]{11})", u)
            if m and vids and m.group(1) not in vids:
                sys.exit("%s: video %s is not in the youtube-digest library" % (lid, m.group(1)))
        for item in x.get("need", []):
            assert item["k"] and item["v"] and (item.get("s") or re.search(r"\(L\d\d|\(assumed\)", item["k"])), (lid, item)   # a source, the earlier lesson it comes from, or marked as an assumption
        for item in x.get("rneed", []):
            assert item["k"] and item["v"], (lid, item)
        if "rtask" in x:
            assert x.get("rev") and x.get("rkey") and "What you need" not in x["rtask"], lid   # a revisit names its company and has an answer
check()

def block():
    js = json.dumps(L, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return "  var VAL_KO=" + js + ";\n"

def main():
    html = open(HTML, encoding="utf-8").read()
    m = re.search(r"(/\* VAL_KO:start[\s\S]*?\*/\n)([\s\S]*?)(  /\* VAL_KO:end \*/)", html)
    if not m: sys.exit("VAL_KO markers not found")
    new = html[:m.start(2)] + block() + html[m.end(2):]
    flags = term_order(new)
    if flags:
        sys.exit("Learn text uses a term before the lesson that teaches it, with no pointer:\n  " + "\n  ".join(flags))
    if "--check" in sys.argv:
        sys.exit(0 if new == html else "VAL_KO block is out of date")
    open(HTML, "w", encoding="utf-8").write(new)
    print("VAL_KO: %d lessons · KO D/E %.1f%% · levered beta %.2f · rf %.2f%%" % (len(L), DE * 100, BETA_L, RF_NET))

main()
