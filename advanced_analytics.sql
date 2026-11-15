-- Create Database
CREATE DATABASE IF NOT EXISTS stock_analytics;
USE stock_analytics;

-- 1. WINDOW FUNCTIONS: Calculate 50-Day & 200-Day Simple Moving Averages (SMA)
CREATE OR REPLACE VIEW stock_moving_averages AS
SELECT 
    Date,
    Ticker,
    Close,
    AVG(Close) OVER (PARTITION BY Ticker ORDER BY Date ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) AS SMA_50,
    AVG(Close) OVER (PARTITION BY Ticker ORDER BY Date ROWS BETWEEN 199 PRECEDING AND CURRENT ROW) AS SMA_200
FROM stock_prices;

-- 2. CTE (Common Table Expressions): Find Top 5 Best Performing Days for Each Stock
-- Wrapped in a VIEW so it acts as a permanent table/asset in the database
CREATE OR REPLACE VIEW top_performing_days AS
WITH RankedReturns AS (
    SELECT 
        Date, 
        Ticker, 
        Daily_Return_Pct,
        RANK() OVER (PARTITION BY Ticker ORDER BY Daily_Return_Pct DESC) as Return_Rank
    FROM stock_prices
    WHERE Daily_Return_Pct IS NOT NULL
)
SELECT * FROM RankedReturns WHERE Return_Rank <= 5;

-- 3. STORED PROCEDURE: Generate Weekly Volatility Report
-- Ensures clean execution without "procedure already exists" error
DROP PROCEDURE IF EXISTS GenerateVolatilityReport;

DELIMITER //
CREATE PROCEDURE GenerateVolatilityReport()
BEGIN
    SELECT 
        Ticker,
        YEAR(Date) as Year,
        WEEK(Date) as Week,
        STDDEV(Close) as Price_Volatility,
        AVG(Volume) as Avg_Weekly_Volume
    FROM stock_prices
    GROUP BY Ticker, YEAR(Date), WEEK(Date)
    ORDER BY Ticker, Year DESC, Week DESC;
END //
DELIMITER ;

-- 4. DATABASE OPTIMIZATION: B-Tree Indexing for High-Frequency Queries
-- Yeh index query speed ko 10x fast kar dega jab data 10GB cross karega
CREATE INDEX idx_ticker_date ON stock_prices(Ticker, Date);
CREATE INDEX idx_returns ON stock_prices(Daily_Return_Pct);