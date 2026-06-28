# Portfolio Tracker

A Python-based portfolio analytics system that fetches live NSE stock and ETF prices, calculates portfolio P&L, and generates terminal and Excel reports.

## Features

- Live price fetching with caching and retry handling
- Portfolio valuation and profit/loss calculation
- Terminal report output
- Excel export
- PostgreSQL-backed persistent storage
- Docker-based local PostgreSQL development environment

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
│   ├── test_alerts.py
|   ├── test_calculator.py
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
