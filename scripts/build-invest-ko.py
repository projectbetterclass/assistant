#!/usr/bin/env python3
"""The KO lessons of the investing course (L03–L14): what each task needs, and a worked answer to check against.

Every number comes from one of three places, named on the lesson itself:
  * KO's annual report for 2025 (Form 10-K, filed 20 Feb 2026), read from SEC EDGAR (XBRL facts + the document);
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
            assert item["k"] and item["v"] and (item.get("s") or re.search(r"\(L\d\d", item["k"])), (lid, item)   # a source, or the earlier lesson it comes from
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
