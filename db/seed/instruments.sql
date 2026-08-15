-- Instrument metadata for every ticker currently appearing in transactions.
-- The last 7 rows are tickers found in db/seed/transactions.sql that had
-- no equivalent in config/holdings.py — category is a best guess from
-- naming (all look like individual equities, not ETF-pattern names) and
-- should be confirmed/corrected before relying on --source db for these.
INSERT INTO instruments (ticker, name, category, market_ticker) VALUES
('ANANTRAJ',   'Anant Raj Ltd',               'stock', 'ANANTRAJ.NS'),
('ASHOKLEY',   'Ashok Leyland',               'stock', 'ASHOKLEY.NS'),
('CANBK',      'Canara Bank',                 'stock', 'CANBK.NS'),
('ETERNAL',    'Eternal',                     'stock', 'ETERNAL.NS'),
('FISCHER',    'Fischer Medical Ventures',    'stock', 'FISCHER.NS'),
('HDFCBANK',   'HDFC Bank',                   'stock', 'HDFCBANK.NS'),
('IRCTC',      'IRCTC',                       'stock', 'IRCTC.NS'),
('ITC',        'ITC',                         'stock', 'ITC.NS'),
('PFC',        'PFC',                         'stock', 'PFC.NS'),
('POWERGRID',  'Power Grid Corporation',      'stock', 'POWERGRID.NS'),
('RECLTD',     'REC Ltd',                     'stock', 'RECLTD.NS'),
('TATAPOWER',  'Tata Power',                  'stock', 'TATAPOWER.NS'),
('WONDERLA',   'Wonderla Holidays',           'stock', 'WONDERLA.NS'),
('NIFTYIETF',  'ICICI Nifty 50 ETF',          'etf',   'NIFTYIETF.NS'),
('NEXT50IETF', 'ICICI Nifty Next 50 ETF',     'etf',   'NEXT50IETF.NS'),
('MIDCAPIETF', 'ICICI Midcap 150 ETF',        'etf',   'MIDCAPIETF.NS'),
('MOSMALL250', 'Motilal Oswal Small 250 ETF', 'etf',   'MOSMALL250.NS'),
('GOLDBEES',   'Nippon India GoldBees',       'etf',   'GOLDBEES.NS'),
('SILVERIETF', 'ICICI Silver ETF',            'etf',   'SILVERIETF.NS'),
('IT',         'Kotak Nifty IT ETF',          'etf',   'IT.NS'),
('MON100',     'Motilal Oswal Nasdaq 100 ETF','etf',   'MON100.NS'),
('HNGSNGBEES', 'Hang Seng BeES',              'etf',   'HNGSNGBEES.NS'),
-- Needs confirmation — see header note above.
('EIEL',       'EIEL (name TBD)',             'stock', 'EIEL.NS'),
('ITCHOTELS',  'ITC Hotels',                  'stock', 'ITCHOTELS.NS'),
('KPIT',       'KPIT Technologies',           'stock', 'KPIT.NS'),
('LICI',       'LIC India',                   'stock', 'LICI.NS'),
('NTPC',       'NTPC',                        'stock', 'NTPC.NS'),
('RELIANCE',   'Reliance Industries',         'stock', 'RELIANCE.NS'),
('VIKRAMSOLR', 'Vikram Solar',                'stock', 'VIKRAMSOLR.NS');
