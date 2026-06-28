CREATE TABLE holdings (
    ticker TEXT PRIMARY KEY,

    name TEXT NOT NULL,

    quantity NUMERIC(20,4) NOT NULL
        CHECK (quantity > 0),

    avg_price NUMERIC(20,2) NOT NULL
        CHECK (avg_price >= 0),

    category TEXT NOT NULL DEFAULT 'stock'
        CHECK (
            category IN (
                'stock',
                'etf',
                'gold',
                'mutual_fund'
            )
        ),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE transactions (
    id BIGSERIAL PRIMARY KEY,

    ticker TEXT NOT NULL,

    transaction_type TEXT NOT NULL 
        CHECK (transaction_type IN ( 'BUY', 'SELL' )),

    quantity NUMERIC(20,4) NOT NULL
        CHECK (quantity > 0),

    price NUMERIC(20,2) NOT NULL
        CHECK (price >= 0),

    charges NUMERIC(20,2) NOT NULL DEFAULT 0
        CHECK (charges >= 0),

    transaction_date TIMESTAMPTZ NOT NULL,

    notes TEXT
);

CREATE INDEX idx_transactions_ticker
ON transactions(ticker);



CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER holdings_updated_at_trigger
BEFORE UPDATE ON holdings
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();



CREATE TABLE dividends (
    id BIGSERIAL PRIMARY KEY,

    ticker TEXT NOT NULL,

    dividend_per_share NUMERIC(20,2) NOT NULL
        CHECK (dividend_per_share >= 0),

    shares_held NUMERIC(20,4) NOT NULL
        CHECK (shares_held > 0),

    record_date DATE NOT NULL
);

CREATE INDEX idx_dividends_ticker_record_date
ON dividends (ticker, record_date);