"""
holdings.py — edit this file to update your portfolio.

Each entry: "Display Name": (TICKER.NS, quantity, avg_buy_price, "stock"|"etf")

If avg_buy_price is 0.0, it will show P&L as N/A in reports.
"""

from core.models import Holding

HOLDINGS: list[Holding] = [
    # ── Stocks ────────────────────────────────────────────────────────────────
    Holding("Anant Raj Ltd",            "ANANTRAJ.NS",    5,  513.09, "stock"),
    Holding("Ashok Leyland",            "ASHOKLEY.NS",    4,  124.88, "stock"),
    Holding("Canara Bank",              "CANBK.NS",       1,  126.48, "stock"),
    Holding("Eternal",                  "ETERNAL.NS",     4,  244.89, "stock"),
    Holding("Fischer Medical Ventures", "FISCHER.NS",     6,   43.41, "stock"),
    Holding("HDFC Bank",                "HDFCBANK.NS",   13,  918.28, "stock"),
    Holding("IRCTC",                    "IRCTC.NS",       1,    0.00, "stock"),  # TODO: add avg price
    Holding("ITC",                      "ITC.NS",         1,    0.00, "stock"),  # TODO: add avg price
    Holding("PFC",                      "PFC.NS",         1,    0.00, "stock"),  # TODO: add avg price
    Holding("Power Grid Corporation",   "POWERGRID.NS",   1,    0.00, "stock"),  # TODO: add avg price
    Holding("REC Ltd",                  "RECLTD.NS",      1,    0.00, "stock"),  # TODO: add avg price
    Holding("Tata Power",               "TATAPOWER.NS",   1,    0.00, "stock"),  # TODO: add avg price
    Holding("Wonderla Holidays",        "WONDERLA.NS",    1,    0.00, "stock"),  # TODO: add avg price

    # ── ETFs ──────────────────────────────────────────────────────────────────
    Holding("ICICI Nifty 50 ETF",       "NIFTYIETF.NS",  33,  286.79, "etf"),
    Holding("ICICI Nifty Next 50 ETF",  "NEXT50IETF.NS", 57,   71.78, "etf"),
    Holding("ICICI Midcap 150 ETF",     "MIDCAPIETF.NS", 30,   21.87, "etf"),
    Holding("Mirae Small 250 ETF",      "MOSMALL250.NS",  1,    0.00, "etf"),   # TODO: add avg price
    Holding("GoldBees",                 "GOLDBEES.NS",    1,    0.00, "etf"),   # TODO: add avg price
    Holding("ICICI Silver ETF",         "SILVERIETF.NS",  1,    0.00, "etf"),   # TODO: add avg price
    Holding("Kotak Nifty IT ETF",       "IT.NS", 1,    0.00, "etf"),   # TODO: add avg price
    Holding("Mirae Nasdaq 100 ETF",     "MON100.NS",      1,    0.00, "etf"),   # TODO: add avg price
    Holding("Hang Seng BeES",           "HNGSNGBEES.NS",  1,    0.00, "etf"),   # TODO: add avg price
]
