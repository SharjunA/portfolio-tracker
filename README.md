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
│   ├── settings.py
│   └── holdings.py              # temporary; remove later once DB is source of truth
├── core/
│   ├── models.py
│   ├── fetcher.py
│   └── portfolio.py
├── db/
│   ├── connection.py
│   ├── migrations/
│   │   └── 001_initial_schema.sql
│   └── seed/
│       ├── transactions.sql
│       └── dividends.sql
├── reports/
│   ├── terminal.py
│   └── excel.py
├── data/
│   ├── cache/
│   ├── exports/
│   └── history/
├── tests/
│   ├── test_calculator.py
│   └── test_db.py
├── utils/
│   ├── logger.py
│   └── helpers.py
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── main.py
├── README.md
└── requirements.txt
```

## Updating holdings

Open `config/holdings.py` and edit the `HOLDINGS` list.  
Each entry is a `Holding(name, ticker, qty, avg_buy_price, category)`.

## Running tests

```bash
pytest tests/ -v
```
