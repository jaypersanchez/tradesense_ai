-- Run once in psql / pgAdmin
CREATE TABLE IF NOT EXISTS fundamentals_daily (
    id               SERIAL PRIMARY KEY,
    symbol           TEXT,
    day              DATE,            -- e.g. 2025-06-22
    samples          INT,             -- # raw snapshots aggregated
    avg_market_cap   NUMERIC,
    pct_change_mcap  NUMERIC,
    avg_total_volume NUMERIC,
    pct_change_vol   NUMERIC,
    stddev_mcap      NUMERIC,         -- daily intra-day volatility
    stddev_volume    NUMERIC,
    avg_circ_supply  NUMERIC,
    fundamentals_score_mean NUMERIC,
    commit_count_4w_mean     NUMERIC,
    created_at       TIMESTAMP DEFAULT now(),

    UNIQUE(symbol, day)               -- safe to upsert
);


SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'fundamentals_data';

SELECT * FROM fundamentals_daily WHERE symbol = 'XRP_USD' LIMIT 5;

-- How many raw snapshots do we have for XRP on the day?
SELECT
    COUNT(*)                    AS raw_rows,
    COUNT(market_cap)           AS non_null_mcap,
    COUNT(total_volume)         AS non_null_volume
FROM fundamentals_data
WHERE symbol = 'XRP_USD'
  AND timestamp >= '2025-06-21'::date
  AND timestamp <  '2025-06-22'::date;
SELECT *
FROM fundamentals_daily
WHERE symbol = 'XRP_USD';

SELECT DISTINCT symbol
FROM fundamentals_data
ORDER BY symbol;


CREATE TABLE supported_symbols (
    id SERIAL PRIMARY KEY,
    base TEXT NOT NULL,        -- e.g., 'BTC', 'ETH', 'XRP'
    quote TEXT NOT NULL,       -- e.g., 'USDC', 'USD', 'ETH'
    symbol TEXT UNIQUE NOT NULL, -- e.g., 'BTC_USDC', 'ETH_USD'
    coingecko_id TEXT NOT NULL,  -- e.g., 'bitcoin', 'ethereum'
    active BOOLEAN DEFAULT true
);

ALTER TABLE supported_symbols
ADD COLUMN symbol_type TEXT DEFAULT 'spot';

INSERT INTO supported_symbols (base, quote, symbol, coingecko_id, active)
VALUES 
  ('BTC', 'USDC', 'BTC_USDC', 'bitcoin', true),
  ('ETH', 'USDC', 'ETH_USDC', 'ethereum', true),
  ('XRP', 'USDC', 'XRP_USDC', 'ripple', true),
  ('SOL', 'USDC', 'SOL_USDC', 'solana', true),
  ('BTC', 'ETH',  'BTC_ETH',  'bitcoin', true),
  ('ETH', 'BTC',  'ETH_BTC',  'ethereum', true);
  
 INSERT INTO supported_symbols (base, quote, symbol, coingecko_id, active, symbol_type)
VALUES
  ('USDC', 'USD', 'USDC_USD', 'usd-coin', true, 'stable'),
  ('USDT', 'USD', 'USDT_USD', 'tether', true, 'stable'),
  ('DAI',  'USD', 'DAI_USD',  'dai', true, 'stable'),
  ('TUSD', 'USD', 'TUSD_USD', 'true-usd', true, 'stable'),
  ('FRAX', 'USD', 'FRAX_USD', 'frax', true, 'stable');

  
  SELECT * FROM supported_symbols;









