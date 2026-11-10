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
            assert item["k"] and item["v"] and item.get("s"), (lid, item)
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
