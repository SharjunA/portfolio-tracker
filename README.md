# Portfolio Tracker

Fetches live NSE stock and ETF prices, calculates P&L, and generates reports.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
# Terminal + Excel report (default)
python main.py

# Force fresh prices (bypass 15-min cache)
python main.py --no-cache

# Terminal only
python main.py --report terminal

# Excel only
python main.py --report excel
```

## Project structure

```
portfolio_tracker/
├── config/
│   ├── holdings.py       ← edit this to update your portfolio
│   └── settings.py       ← paths, cache TTL, colors, etc.
├── core/
│   ├── models.py         ← Holding and PortfolioSummary dataclasses
│   ├── fetcher.py        ← yfinance price fetching with cache + retries
│   └── portfolio.py      ← Portfolio class (orchestrates fetch → summarise)
├── reports/
│   ├── terminal.py       ← coloured terminal table
│   └── excel.py          ← formatted Excel report
├── data/
│   ├── cache/            ← price cache (gitignored)
│   ├── exports/          ← generated Excel files (gitignored)
│   └── history/          ← daily portfolio value snapshots (gitignored)
├── utils/
│   ├── logger.py         ← centralised logging
│   └── helpers.py        ← INR formatting, etc.
├── tests/
│   └── test_calculator.py
├── main.py               ← CLI entrypoint
└── requirements.txt
```

## Updating holdings

Open `config/holdings.py` and edit the `HOLDINGS` list.  
Each entry is a `Holding(name, ticker, qty, avg_buy_price, category)`.

## Running tests

```bash
pytest tests/ -v
```
