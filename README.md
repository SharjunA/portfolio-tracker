# Portfolio Tracker

A Python portfolio analytics backend that derives current positions from a PostgreSQL transaction ledger, fetches live NSE prices, calculates P&L, and generates terminal and Excel reports.

## Source of truth

PostgreSQL is the application source of truth:

- `transactions` contains buys and sells.
- `instruments` contains display names, categories, and market-data symbols.
- `db/portfolio_repository.py` reads both tables and returns domain `Holding` objects.
- `core/position_calculator.py` contains the database-independent weighted-average cost calculation.

`config/holdings.py` remains as an explicit compatibility fallback during the migration. It is not used by default.

## Setup

1. Create a local environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

   Set `DB_USER` and `DB_PASSWORD` to the values you want PostgreSQL to use.

2. Start PostgreSQL:

   ```powershell
   docker compose up -d database
   ```

3. Apply the schema and seed data in this order. The instrument seed must be loaded before transactions because the schema enforces the foreign key.

   ```powershell
   Get-Content db/migrations/001_initial_schema.sql | docker exec -i portfolio_tracker_db psql -U $env:DB_USER -d $env:DB_NAME
   Get-Content db/migrations/002_instruments.sql | docker exec -i portfolio_tracker_db psql -U $env:DB_USER -d $env:DB_NAME
   Get-Content db/seed/instruments.sql | docker exec -i portfolio_tracker_db psql -U $env:DB_USER -d $env:DB_NAME
   Get-Content db/seed/transactions.sql | docker exec -i portfolio_tracker_db psql -U $env:DB_USER -d $env:DB_NAME
   ```

   The commands above assume the same connection values are available in the current PowerShell session. Alternatively, run the SQL with your preferred PostgreSQL client.

4. Install Python dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

## Running reports

The PostgreSQL-backed path is the default:

```powershell
python main.py --report terminal
python main.py --report all --no-cache
```

For the scheduled runner:

```powershell
python scheduler/auto_report.py --source db
python scheduler/auto_report.py --loop --interval 30 --source db
```

Use `--source static` only while PostgreSQL is unavailable and you intentionally want the compatibility holdings list.

## Project structure

```text
portfolio_tracker/
|-- config/
|   |-- settings.py
|   `-- holdings.py                 # temporary compatibility fallback
|-- core/
|   |-- models.py                   # domain models and summary calculations
|   |-- fetcher.py                  # live prices and local cache
|   |-- position_calculator.py      # pure transaction aggregation
|   `-- portfolio.py                # refresh orchestration and history
|-- db/
|   |-- connection.py
|   |-- portfolio_repository.py     # PostgreSQL adapter
|   |-- migrations/
|   |   |-- 001_initial_schema.sql
|   |   `-- 002_instruments.sql
|   `-- seed/
|       |-- instruments.sql
|       |-- transactions.sql
|       `-- dividends.sql
|-- reports/
|   |-- terminal.py
|   `-- excel.py
|-- scheduler/
|   |-- auto_report.py
|   `-- alerts.py
|-- tests/
|-- data/                           # local cache, exports, and history
|-- docker-compose.yml
|-- main.py
`-- requirements.txt
```

## Tests

```powershell
python -m pytest -q
```

The repository tests use fake cursors and do not require a running PostgreSQL instance. A live DB check still requires Docker/PostgreSQL to be running and the schema/seeds to be applied.
