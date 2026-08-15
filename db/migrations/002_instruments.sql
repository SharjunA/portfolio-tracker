-- Instruments: per-ticker metadata (name, category, market data symbol).

CREATE TABLE instruments (
    ticker TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL
        CHECK (
            category IN (
                'stock',
                'etf',
                'gold',
                'mutual_fund'
            )
        ),
    market_ticker TEXT
);

CREATE INDEX idx_instruments_category ON instruments (category);

-- A transaction without instrument metadata cannot be rendered correctly.
-- Apply this after 001_initial_schema.sql and before loading transaction data.
ALTER TABLE transactions
    ADD CONSTRAINT transactions_ticker_fkey
    FOREIGN KEY (ticker) REFERENCES instruments (ticker);
