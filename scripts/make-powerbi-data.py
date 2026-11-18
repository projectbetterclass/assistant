# Practice data for the Power BI course (build-powerbi-course.py): two years of order lines for Kade Distribution, a
# made-up Dutch wholesaler with three warehouses, four carriers and sixty retail customers. The data is generated with a
# fixed seed, so it is the same every run, and the answers every sitting checks against are computed here from the same
# cleaned rows the learner ends up with in Power BI.
#
# Built into it on purpose:
#   - export mess to clean (Q03): Orders.csv is a Dutch export (";" between fields, "," in decimals, dd-mm-yyyy dates),
#     with 30 rows exported twice and 12 test-order rows; Customers.csv spells countries three ways and pads some names.
#   - open lines: orders not yet delivered on the extract date (31-12-2025) have no ship date, delivered date,
#     shipped quantity or freight.
#   - a story to find (Q10): from July 2025 the Venlo warehouse moved most of its volume to a new, cheaper carrier
#     (Kanaal Freight), which is late more often, worst in the Oct–Dec peak; and the snack supplier Krokant Foods
#     short-shipped in Oct–Dec 2025.
#
#   python3 scripts/make-powerbi-data.py   -> data/powerbi/kade-practice-data.zip, data/powerbi/answers.json
import csv, io, json, math, os, random, zipfile
from datetime import date, timedelta

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "powerbi")
rng = random.Random(20261116)
START, END, EXTRACT = date(2024, 1, 2), date(2025, 12, 31), date(2025, 12, 31)

WAREHOUSES = [("W1", "Rotterdam DC", "Rotterdam"), ("W2", "Venlo DC", "Venlo"), ("W3", "Tilburg DC", "Tilburg")]
CARRIERS = [("K1", "Haven Transport", "2019-03-01"), ("K2", "Brug Logistiek", "2020-06-01"),
            ("K3", "Duin Express", "2018-01-01"), ("K4", "Kanaal Freight", "2025-07-01")]
RATE = {"K1": 0.21, "K2": 0.19, "K3": 0.26, "K4": 0.14}            # € per kg shipped
ONTIME = {"K1": 0.955, "K2": 0.935, "K3": 0.97, "K4": 0.86}         # chance an order arrives by the requested date
SUPPLIERS = [("S01", "Bron Dranken", "Netherlands"), ("S02", "Alpenquell", "Germany"), ("S03", "Krokant Foods", "Belgium"),
             ("S04", "Zoutje & Co", "Netherlands"), ("S05", "Schoon Huis", "Netherlands"), ("S06", "Brillo Werke", "Germany"),
             ("S07", "Zacht Care", "Netherlands"), ("S08", "Fleur Cosmetics", "Belgium")]
SHORT_SUPPLIER = "S03"
CATS = [("Beverages", ["S01", "S02"], ["Sparkling water 6×1.5 L", "Still water 6×1.5 L", "Cola 24×330 ml", "Orange juice 8×1 L",
                                         "Iced tea 12×500 ml", "Energy drink 24×250 ml", "Apple juice 8×1 L", "Tonic 24×200 ml",
                                         "Lemonade syrup 6×750 ml", "Cold brew coffee 12×250 ml"]),
        ("Snacks", ["S03", "S04"], ["Paprika crisps 20×150 g", "Salted crisps 20×150 g", "Tortilla chips 12×200 g", "Pretzels 12×250 g",
                                     "Mixed nuts 12×300 g", "Popcorn 18×90 g", "Rice crackers 16×100 g", "Cheese crackers 12×150 g",
                                     "Chocolate bars 48×50 g", "Stroopwafels 20×250 g"]),
        ("Household", ["S05", "S06"], ["Dish soap 12×500 ml", "All-purpose cleaner 12×1 L", "Laundry liquid 4×2 L", "Dishwasher tabs 6×40",
                                        "Paper towels 8×4 rolls", "Toilet paper 6×9 rolls", "Bin bags 20×30", "Glass cleaner 12×500 ml",
                                        "Sponges 24×5", "Fabric softener 6×1.5 L"]),
        ("Personal care", ["S07", "S08"], ["Shampoo 12×300 ml", "Shower gel 12×250 ml", "Toothpaste 24×75 ml", "Hand soap 12×500 ml",
                                            "Deodorant 12×150 ml", "Body lotion 12×400 ml", "Razors 24×4", "Cotton pads 24×80",
                                            "Sunscreen 12×200 ml", "Lip balm 48×4.8 g"])]
PLACES = {"Netherlands": [("Rotterdam", "W1"), ("Den Haag", "W1"), ("Delft", "W1"), ("Leiden", "W1"), ("Gouda", "W1"), ("Dordrecht", "W1"),
                          ("Utrecht", "W1"), ("Amsterdam", "W1"), ("Breda", "W3"), ("Tilburg", "W3"), ("Eindhoven", "W3"),
                          ("Den Bosch", "W3"), ("Nijmegen", "W2"), ("Arnhem", "W2"), ("Venlo", "W2")],
          "Belgium": [("Antwerpen", "W3"), ("Gent", "W3"), ("Brussel", "W3"), ("Hasselt", "W3"), ("Brugge", "W3")],
          "Germany": [("Düsseldorf", "W2"), ("Köln", "W2"), ("Duisburg", "W2"), ("Essen", "W2"), ("Krefeld", "W2")]}
SPELL = {"Netherlands": ["Netherlands", "NL", "Nederland"], "Belgium": ["Belgium", "BE", "België"], "Germany": ["Germany", "DE", "Deutschland"]}
WORDS = ["De Linde", "Het Anker", "Zuidpunt", "Noorderlicht", "Waterkant", "Molenhoek", "Blauwe Brug", "Groene Hart", "De Vlijt",
         "Zonnehoek", "Kloosterhof", "De Eik", "Havenzicht", "Lindenhof", "De Kroon", "Marktplein", "Sterrenwacht", "De Hoeve",
         "Rozengaard", "Kade Oost", "De Kolk", "Dijkzicht", "Polderweg", "Torenhof", "De Pijl", "Vennehof", "Bergzicht", "Duinrand",
         "Weidegrond", "De Spil"]
KIND = {"Netherlands": ["Supermarkt", "Buurtsuper", "Groothandel", "Online"], "Belgium": ["Supermarché", "Buurtwinkel", "Groothandel", "Online"],
        "Germany": ["Markt", "Frischemarkt", "Großhandel", "Online"]}
CHANNEL = {"Supermarkt": "Supermarket", "Buurtsuper": "Supermarket", "Supermarché": "Supermarket", "Buurtwinkel": "Supermarket",
           "Markt": "Supermarket", "Frischemarkt": "Supermarket", "Groothandel": "Wholesale", "Großhandel": "Wholesale", "Online": "Online"}


def products():
    out, n = [], 0
    for cat, sups, names in CATS:
        for i, name in enumerate(names):
            n += 1
            price = round(rng.uniform(8, 45), 2)
            out.append(dict(ProductID="P%02d" % n, Product=name, Category=cat, SupplierID=sups[i % 2], UnitPriceEUR=price,
                            UnitCostEUR=round(price * rng.uniform(0.68, 0.8), 2), CartonWeightKg=round(rng.uniform(2, 12), 1)))
    return out


def customers():
    out, words = [], WORDS[:]
    rng.shuffle(words)
    plan = [("Netherlands", 30), ("Belgium", 15), ("Germany", 15)]
    n = 0
    for country, k in plan:
        for j in range(k):
            n += 1
            city, wh = rng.choice(PLACES[country])
            kind = rng.choice(KIND[country])
            name = "%s %s" % (kind, words[(n - 1) % len(words)]) + ("" if n <= len(words) else " " + city)
            out.append(dict(CustomerID="C%02d" % n, Customer=name, City=city, Country=country, Channel=CHANNEL[kind], WarehouseID=wh,
                            weight=rng.uniform(0.4, 2.2)))
    return out


def carrier_for(wh, d):
    r = rng.random()
    if wh == "W1":
        return "K1" if r < 0.60 else "K3" if r < 0.85 else "K2"
    if wh == "W3":
        return "K2" if r < 0.55 else "K1" if r < 0.85 else "K3"
    if d < date(2025, 7, 1):
        return "K2" if r < 0.50 else "K1" if r < 0.90 else "K3"
    return "K4" if r < 0.75 else "K1" if r < 0.95 else "K3"


def ontime_p(k, d):
    p = ONTIME[k]
    if k == "K4" and d >= date(2025, 10, 1):
        p = 0.78
    if d.month == 12:
        p -= 0.03
    return p


def lines(prods, custs):
    pmap = {p["ProductID"]: p for p in prods}
    cw = [c["weight"] for c in custs]
    rows, oid, d = [], 0, START
    while d <= END:
        if d.weekday() < 5:
            k = rng.choice([4, 5, 6, 6, 7, 7, 8, 9]) + (1 if d.year == 2025 and rng.random() < 0.5 else 0)
            for _ in range(k):
                oid += 1
                c = rng.choices(custs, weights=cw)[0]
                wh = c["WarehouseID"]
                carr = carrier_for(wh, d)
                req = d + timedelta(days=2 if c["Country"] == "Netherlands" else 3)
                ship = d + timedelta(days=1)
                if rng.random() < ontime_p(carr, d):
                    dlv = req - timedelta(days=rng.choice([0, 0, 0, 1]))
                else:
                    dlv = req + timedelta(days=rng.choice([1, 1, 1, 2, 2, 3, 4]))
                for ln, p in enumerate(rng.sample(prods, rng.choice([1, 2, 2, 3, 3, 4, 5])), 1):
                    q = max(1, min(120, int(rng.lognormvariate(2.6, 0.6))))
                    short = 0.22 if (p["SupplierID"] == SHORT_SUPPLIER and d >= date(2025, 10, 1)) else 0.025
                    qs = q if rng.random() >= short else max(0, q - math.ceil(q * rng.uniform(0.1, 0.6)))
                    row = dict(OrderID="SO%05d" % oid, LineNo=ln, OrderDate=d, CustomerID=c["CustomerID"], WarehouseID=wh, CarrierID=carr,
                               ProductID=p["ProductID"], QtyOrdered=q, QtyShipped=qs, RequestedDate=req, ShipDate=ship, DeliveredDate=dlv,
                               FreightEUR=round(qs * pmap[p["ProductID"]]["CartonWeightKg"] * (RATE[carr] + (0.03 if c["Country"] != "Netherlands" else 0))
                                                * rng.uniform(0.95, 1.05) + 1.2, 2))
                    if dlv > EXTRACT:
                        row.update(QtyShipped=None, ShipDate=None, DeliveredDate=None, FreightEUR=None)
                    rows.append(row)
        d += timedelta(days=1)
    return rows


def nl_date(d): return d.strftime("%d-%m-%Y") if d else ""
def nl_num(x): return ("%.2f" % x).replace(".", ",") if x is not None else ""


def write_zip(prods, custs, clean, dirty):
    files = {}
    b = io.StringIO(); w = csv.writer(b, delimiter=";", lineterminator="\r\n")
    cols = ["OrderID", "LineNo", "OrderDate", "CustomerID", "WarehouseID", "CarrierID", "ProductID", "QtyOrdered", "QtyShipped",
            "RequestedDate", "ShipDate", "DeliveredDate", "FreightEUR"]
    w.writerow(cols)
    for r in dirty:
        w.writerow([r["OrderID"], r["LineNo"], nl_date(r["OrderDate"]), r["CustomerID"], r["WarehouseID"], r["CarrierID"], r["ProductID"],
                    r["QtyOrdered"], "" if r["QtyShipped"] is None else r["QtyShipped"], nl_date(r["RequestedDate"]), nl_date(r["ShipDate"]),
                    nl_date(r["DeliveredDate"]), nl_num(r["FreightEUR"])])
    files["Orders.csv"] = b.getvalue()

    def table(name, cols, rows):
        b = io.StringIO(); w = csv.writer(b, lineterminator="\r\n"); w.writerow(cols)
        for r in rows:
            w.writerow([r[c] for c in cols])
        files[name] = b.getvalue()
    messy = []
    for c in custs:
        m = dict(c)
        m["Country"] = rng.choice(SPELL[c["Country"]]) + rng.choice(["", "", " "])
        m["Customer"] = c["Customer"] + rng.choice(["", "", "", "  "])
        messy.append(m)
    table("Customers.csv", ["CustomerID", "Customer", "City", "Country", "Channel", "WarehouseID"], messy)
    table("Products.csv", ["ProductID", "Product", "Category", "SupplierID", "UnitPriceEUR", "UnitCostEUR", "CartonWeightKg"], prods)
    table("Suppliers.csv", ["SupplierID", "Supplier", "Country"], [dict(SupplierID=a, Supplier=b, Country=c) for a, b, c in SUPPLIERS])
    table("Carriers.csv", ["CarrierID", "Carrier", "Mode", "ContractStart"], [dict(CarrierID=a, Carrier=b, Mode="Road", ContractStart=c) for a, b, c in CARRIERS])
    table("Warehouses.csv", ["WarehouseID", "Warehouse", "City"], [dict(WarehouseID=a, Warehouse=b, City=c) for a, b, c in WAREHOUSES])
    files["README.txt"] = README
    os.makedirs(OUT, exist_ok=True)
    with zipfile.ZipFile(os.path.join(OUT, "kade-practice-data.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for name in ["README.txt", "Orders.csv", "Customers.csv", "Products.csv", "Suppliers.csv", "Carriers.csv", "Warehouses.csv"]:
            info = zipfile.ZipInfo("kade-practice-data/" + name, date_time=(2026, 11, 16, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, files[name].encode("utf-8-sig" if name.endswith(".csv") else "utf-8"))
    return {n: files[n].count("\r\n") - 1 for n in files if n.endswith(".csv")}


README = """Kade Distribution: practice data for the Power BI course
=========================================================
Kade Distribution is a made-up Dutch wholesaler. Everything in these files is generated for practice; no real
company, customer or person is in them. Extracted on 31-12-2025.

Orders.csv      one row per order line, Jan 2024 - Dec 2025. A Dutch export: fields split by ";", decimals with ",",
                dates as dd-mm-yyyy. Some rows came out twice, and a few are test orders (CustomerID TEST).
                Lines not yet delivered on the extract date have no ShipDate, DeliveredDate, QtyShipped or FreightEUR.
Customers.csv   60 customers in the Netherlands, Belgium and Germany, and the warehouse that serves each.
Products.csv    40 products (sold per carton), their category, supplier, price, cost and carton weight.
Suppliers.csv, Carriers.csv, Warehouses.csv   the lookups.

Definitions the course uses
  Delivered line   DeliveredDate is filled in.
  On time          DeliveredDate is on or before RequestedDate.
  In full          QtyShipped is at least QtyOrdered.
  OTIF %           delivered lines that are on time AND in full, divided by delivered lines.
  Fill rate        cartons shipped divided by cartons ordered, on delivered lines.
  Revenue          QtyShipped x UnitPriceEUR.     Kg shipped   QtyShipped x CartonWeightKg.
"""


def answers(prods, custs, clean, dirty, counts, n_dup, n_test):
    P = {p["ProductID"]: p for p in prods}; C = {c["CustomerID"]: c for c in custs}
    WN = {a: c for a, b, c in WAREHOUSES}; KN = {a: b for a, b, c in CARRIERS}; SN = {a: b for a, b, c in SUPPLIERS}
    dl = [r for r in clean if r["DeliveredDate"]]
    def ot(r): return r["DeliveredDate"] <= r["RequestedDate"]
    def inf(r): return r["QtyShipped"] >= r["QtyOrdered"]
    def pct(a, b): return round(100.0 * a / b, 1) if b else None
    def otif(rows): rows = [r for r in rows if r["DeliveredDate"]]; return pct(sum(1 for r in rows if ot(r) and inf(r)), len(rows))
    def fill(rows): rows = [r for r in rows if r["DeliveredDate"]]; return pct(sum(r["QtyShipped"] for r in rows), sum(r["QtyOrdered"] for r in rows))
    def eur(x): return round(x, 2)
    def kg(rows): return sum(r["QtyShipped"] * P[r["ProductID"]]["CartonWeightKg"] for r in rows if r["DeliveredDate"])
    def freight(rows): return sum(r["FreightEUR"] for r in rows if r["DeliveredDate"])
    def rev(rows): return sum(r["QtyShipped"] * P[r["ProductID"]]["UnitPriceEUR"] for r in rows if r["DeliveredDate"])
    yr = lambda y: [r for r in clean if r["OrderDate"].year == y]
    ym = lambda y, m: [r for r in clean if (r["OrderDate"].year, r["OrderDate"].month) == (y, m)]
    A = {}
    A["raw"] = dict(counts, orders_blank_delivered=sum(1 for r in dirty if not r["DeliveredDate"]), orders_dup=n_dup, orders_test=n_test,
                    orders_ids=len({r["OrderID"] for r in clean}))
    A["clean_lines"] = len(clean)
    A["cust_by_country"] = {k: sum(1 for c in custs if c["Country"] == k) for k in ["Netherlands", "Belgium", "Germany"]}
    A["open_lines"] = sum(1 for r in clean if not r["DeliveredDate"])
    A["units_by_cat"] = {cat: sum(r["QtyOrdered"] for r in clean if P[r["ProductID"]]["Category"] == cat) for cat, _, _ in CATS}
    A["lines_by_wh"] = {WN[w]: sum(1 for r in clean if r["WarehouseID"] == w) for w, _, _ in WAREHOUSES}
    A["totals"] = dict(lines=len(clean), delivered=len(dl), units_ordered=sum(r["QtyOrdered"] for r in clean),
                       units_shipped=sum(r["QtyShipped"] for r in dl), revenue=eur(rev(clean)), freight=eur(freight(clean)),
                       freight_pct=pct(freight(clean), rev(clean)), kg=round(kg(clean)), eur_per_kg=round(freight(clean) / kg(clean), 3),
                       fill=fill(clean))
    A["service"] = dict(ontime=pct(sum(1 for r in dl if ot(r)), len(dl)), infull=pct(sum(1 for r in dl if inf(r)), len(dl)), otif=otif(clean),
                        otif_by_wh={WN[w]: otif([r for r in clean if r["WarehouseID"] == w]) for w, _, _ in WAREHOUSES},
                        late_share_by_carrier={KN[k]: pct(sum(1 for r in dl if r["CarrierID"] == k and not ot(r)), sum(1 for r in dl if not ot(r)))
                                               for k, _, _ in CARRIERS})
    A["by_year"] = {y: dict(otif=otif(yr(y)), fill=fill(yr(y)), freight=eur(freight(yr(y))), revenue=eur(rev(yr(y))), lines=len(yr(y)),
                            eur_per_kg=round(freight(yr(y)) / kg(yr(y)), 3),
                            otif_by_wh={WN[w]: otif([r for r in yr(y) if r["WarehouseID"] == w]) for w, _, _ in WAREHOUSES}) for y in (2024, 2025)}
    h = lambda y, mm: [r for r in clean if r["OrderDate"].year == y and r["OrderDate"].month in mm]
    A["ytd_jun"] = {y: eur(freight(h(y, range(1, 7)))) for y in (2024, 2025)}
    A["monthly_otif_2025"] = {m: otif(ym(2025, m)) for m in range(1, 13)}
    def raw_otif(rows): rows = [r for r in rows if r["DeliveredDate"]]; return 100.0 * sum(1 for r in rows if ot(r) and inf(r)) / len(rows)
    mo = {m: raw_otif(ym(2025, m)) for m in range(1, 13)}   # a visual calculation averages the unrounded monthly values
    A["mavg3_2025"] = {m: round((mo[m - 2] + mo[m - 1] + mo[m]) / 3, 1) for m in (10, 11, 12)}
    c25 = {}
    for c in custs:
        rows = [r for r in yr(2025) if r["CustomerID"] == c["CustomerID"] and r["DeliveredDate"]]
        if len(rows) >= 40:
            c25[c["CustomerID"]] = (otif(rows), len(rows))
    low = sorted([(v[0], k) for k, v in c25.items() if v[0] < 85])
    A["low_customers_2025"] = [dict(id=k, name=C[k]["Customer"], country=C[k]["Country"], wh=WN[C[k]["WarehouseID"]], otif=v, lines=c25[k][1]) for v, k in low]
    if low:
        w = low[0][1]
        late = [r for r in yr(2025) if r["CustomerID"] == w and r["DeliveredDate"] and not ot(r)]
        A["worst_late_by_carrier_2025"] = {KN[k]: sum(1 for r in late if r["CarrierID"] == k) for k, _, _ in CARRIERS}
        A["worst_late_h2_share"] = pct(sum(1 for r in late if r["OrderDate"].month >= 7), len(late))
    vh = lambda mm, k=None: [r for r in h(2025, mm) if r["WarehouseID"] == "W2" and (k is None or r["CarrierID"] == k)]
    H1, H2 = range(1, 7), range(7, 13)
    v1, v2 = vh(H1), vh(H2)
    rate1, rate2 = freight(v1) / kg(v1), freight(v2) / kg(v2)
    saving = kg(v2) * (rate1 - rate2)
    d1 = len([r for r in v2 if r["DeliveredDate"]])
    extra_fail = d1 * (otif(v1) - otif(v2)) / 100.0
    A["venlo"] = dict(otif_h1=otif(v1), otif_h2=otif(v2), eur_kg_h1=round(rate1, 3), eur_kg_h2=round(rate2, 3), kg_h2=round(kg(v2)),
                      saving=round(saving), delivered_h2=d1, extra_fail=round(extra_fail), per_fail=round(saving / extra_fail, 2),
                      kanaal_share_h2=pct(len([r for r in v2 if r["CarrierID"] == "K4"]), len(v2)),
                      otif_h2_kanaal=otif(vh(H2, "K4")), otif_h2_other=otif([r for r in v2 if r["CarrierID"] != "K4"]),
                      otif_q4_kanaal=otif([r for r in vh(range(10, 13), "K4")]), otif_q3_kanaal=otif([r for r in vh(range(7, 10), "K4")]),
                      kanaal_eur_kg=round(freight(vh(H2, "K4")) / kg(vh(H2, "K4")), 3))
    q4 = h(2025, range(10, 13))
    A["supplier_q4"] = dict(name=SN[SHORT_SUPPLIER], fill=fill([r for r in q4 if P[r["ProductID"]]["SupplierID"] == SHORT_SUPPLIER]),
                            others=fill([r for r in q4 if P[r["ProductID"]]["SupplierID"] != SHORT_SUPPLIER]),
                            fill_q3=fill([r for r in h(2025, range(7, 10)) if P[r["ProductID"]]["SupplierID"] == SHORT_SUPPLIER]))
    A["rls_venlo"] = dict(lines=sum(1 for r in clean if r["WarehouseID"] == "W2"), otif=otif([r for r in clean if r["WarehouseID"] == "W2"]),
                          customers=len({r["CustomerID"] for r in clean if r["WarehouseID"] == "W2"}))
    A["rls_tilburg"] = dict(lines=sum(1 for r in clean if r["WarehouseID"] == "W3"), otif=otif([r for r in clean if r["WarehouseID"] == "W3"]),
                            customers=len({r["CustomerID"] for r in clean if r["WarehouseID"] == "W3"}))
    A["otif_2024_rotterdam"] = otif([r for r in yr(2024) if r["WarehouseID"] == "W1"])
    A["units_by_cat_2025"] = {cat: sum(r["QtyOrdered"] for r in yr(2025) if P[r["ProductID"]]["Category"] == cat) for cat, _, _ in CATS}
    A["by_carrier_2025"] = {KN[k]: dict(otif=otif([r for r in yr(2025) if r["CarrierID"] == k]),
                                        eur_kg=round(freight([r for r in yr(2025) if r["CarrierID"] == k]) / kg([r for r in yr(2025) if r["CarrierID"] == k]), 3))
                            for k, _, _ in CARRIERS}
    A["revenue_by_channel_2025"] = {ch: eur(rev([r for r in yr(2025) if C[r["CustomerID"]]["Channel"] == ch])) for ch in ["Supermarket", "Wholesale", "Online"]}
    return A


def main():
    prods, custs = products(), customers()
    clean = lines(prods, custs)
    dirty = [dict(r) for r in clean]
    dup_at = sorted(rng.sample(range(len(clean)), 30), reverse=True)
    for i in dup_at:
        dirty.insert(i + 1, dict(clean[i]))
    test_day = date(2025, 1, 15)
    tests = [dict(OrderID="TEST%03d" % i, LineNo=1, OrderDate=test_day, CustomerID="TEST", WarehouseID="W1", CarrierID="K1",
                  ProductID="P%02d" % (i + 1), QtyOrdered=1, QtyShipped=1, RequestedDate=test_day + timedelta(days=2),
                  ShipDate=test_day + timedelta(days=1), DeliveredDate=test_day + timedelta(days=2), FreightEUR=0.0) for i in range(12)]
    pos = next(i for i, r in enumerate(dirty) if r["OrderDate"] > test_day)
    dirty[pos:pos] = tests
    counts = write_zip(prods, custs, clean, dirty)
    A = answers(prods, custs, clean, dirty, counts, 30, len(tests))
    json.dump(A, open(os.path.join(OUT, "answers.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: A[k] for k in ["raw", "clean_lines", "totals", "service", "venlo", "supplier_q4"]}, ensure_ascii=False, default=str, indent=1))


main()
