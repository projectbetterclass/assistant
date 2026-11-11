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
    "task": "Value KO in dollars, then in euros, using What you need. Which inputs move together and cancel (currency, default spread, riskfree vs terminal growth)? Defend the claim that choosing inconsistently is the only real error — and find the one pair that does not cancel, and why it’s surfaced. Check the README table.",
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

# ---- checks -------------------------------------------------------------------------------------
def check():
    vids = set()
    if os.path.exists(LIBRARY):
        lib = json.load(open(LIBRARY))
        vids = set((lib.get("videos", lib)).keys())
    for lid, x in L.items():
        for item in x.get("need", []) + x.get("key", []):
            u = item.get("u", "")
            m = re.search(r"v=([\w-]{11})", u)
            if m and vids and m.group(1) not in vids:
                sys.exit("%s: video %s is not in the youtube-digest library" % (lid, m.group(1)))
        for item in x.get("need", []):
            assert item["k"] and item["v"] and (item.get("s") or re.search(r"\(L\d\d|\(assumed\)", item["k"])), (lid, item)   # a source, the earlier lesson it comes from, or marked as an assumption
check()

def block():
    js = json.dumps(L, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return "  var VAL_KO=" + js + ";\n"

def main():
    html = open(HTML, encoding="utf-8").read()
    m = re.search(r"(/\* VAL_KO:start[\s\S]*?\*/\n)([\s\S]*?)(  /\* VAL_KO:end \*/)", html)
    if not m: sys.exit("VAL_KO markers not found")
    new = html[:m.start(2)] + block() + html[m.end(2):]
    if "--check" in sys.argv:
        sys.exit(0 if new == html else "VAL_KO block is out of date")
    open(HTML, "w", encoding="utf-8").write(new)
    print("VAL_KO: %d lessons · KO D/E %.1f%% · levered beta %.2f · rf %.2f%%" % (len(L), DE * 100, BETA_L, RF_NET))

main()
