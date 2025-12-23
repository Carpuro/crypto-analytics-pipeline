-- Create crypto_prices table
CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    coin_id VARCHAR(50) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    current_price DECIMAL(20, 8),
    market_cap BIGINT,
    total_volume BIGINT,
    price_change_24h DECIMAL(20, 8),
    price_change_percentage_24h DECIMAL(10, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX idx_coin_timestamp ON crypto_prices(coin_id, timestamp);
CREATE INDEX idx_timestamp ON crypto_prices(timestamp);

-- View for latest prices
CREATE OR REPLACE VIEW latest_crypto_prices AS
SELECT DISTINCT ON (coin_id)
    coin_id,
    symbol,
    name,
    current_price,
    market_cap,
    total_volume,
    price_change_24h,
    price_change_percentage_24h,
    timestamp
FROM crypto_prices
ORDER BY coin_id, timestamp DESC;