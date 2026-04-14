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
    Holding("IRCTC",                    "IRCTC.NS",       3,   545.1, "stock"),  # TODO: add avg price
    Holding("ITC",                      "ITC.NS",        21,   374.3, "stock"),  # TODO: add avg price
    Holding("PFC",                      "PFC.NS",        19,  361.42, "stock"),  # TODO: add avg price
    Holding("Power Grid Corporation",   "POWERGRID.NS",   4,  263.88, "stock"),  # TODO: add avg price
    Holding("REC Ltd",                  "RECLTD.NS",     19,   352.8, "stock"),  # TODO: add avg price
    Holding("Tata Power",               "TATAPOWER.NS",   4,  368.47, "stock"),  # TODO: add avg price
    Holding("Wonderla Holidays",        "WONDERLA.NS",    3,   495.9, "stock"),  # TODO: add avg price

    # ── ETFs ──────────────────────────────────────────────────────────────────
    Holding("ICICI Nifty 50 ETF",       "NIFTYIETF.NS",  33,  286.79, "etf"),
    Holding("ICICI Nifty Next 50 ETF",  "NEXT50IETF.NS", 57,   71.78, "etf"),
    Holding("ICICI Midcap 150 ETF",     "MIDCAPIETF.NS", 30,   21.87, "etf"),
    Holding("Motital Oswal Small 250 ETF", "MOSMALL250.NS", 35,   15.63, "etf"),   
    Holding("Nippon India GoldBees",      "GOLDBEES.NS", 53,   103.7, "etf"),   # TODO: add avg price
    Holding("ICICI Silver ETF",         "SILVERIETF.NS",  3,  218.24, "etf"),   # TODO: add avg price
    Holding("Kotak Nifty IT ETF",       "IT.NS",         10,    31.9, "etf"),   # TODO: add avg price
    Holding("Motital Oswal Nasdaq 100 ETF","MON100.NS",   5,  226.22, "etf"),   # TODO: add avg price
    Holding("Hang Seng BeES",           "HNGSNGBEES.NS",  3,  509.44, "etf"),   # TODO: add avg price
]
