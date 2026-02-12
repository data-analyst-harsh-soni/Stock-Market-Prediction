-- 🔹 SECTION 1: Data Understanding & Basic Analysis

-- 1️⃣ Company Coverage Check
-- Find how many unique companies are present in the database.
SELECT 
      COUNT(company_name)
FROM company_fundamentals;

--Insight:
--The database contains 500 unique companies, indicating broad market coverage. This ensures that the analysis represents a diverse and comprehensive view of the market.

--Business Value:
--A large number of companies improves the reliability and accuracy of market insights.


-- 2️⃣ Latest Price Snapshot
-- For each company, get the most recent trading date and its closing price.
SELECT DISTINCT ON (company) company,
       trade_date,
	   close
FROM base_price
ORDER BY company, trade_date DESC;

-- Insight:
-- The most recent closing price for each company provides a current snapshot of stock valuations and helps identify which companies are currently performing well.

-- Business Value:
-- Useful for monitoring current market leaders and making timely investment decisions.


-- 3️⃣ Data Availability Trend
-- Find the date on which the maximum number of companies had price data available.
-- 3.1 Peak Data Availability Date
SELECT trade_date, company_count
FROM (
    SELECT trade_date,
    COUNT(DISTINCT company) AS company_count,
    RANK() OVER (ORDER BY COUNT(DISTINCT company) DESC) AS rnk
    FROM volumes
    GROUP BY trade_date
) t
WHERE rnk = 1;
-- Insight:
-- Certain trading days had price data available for all 500 companies, indicating full market participation.

--Business Value:
--These days represent complete and reliable market activity.

-- 3.2 Frequency of Peak & Partial Coverage
SELECT company_count, COUNT(*) AS days
FROM (
    SELECT trade_date,
    COUNT(DISTINCT company) AS company_count
    FROM volumes
    GROUP BY trade_date
) t
GROUP BY company_count
ORDER BY company_count DESC;
--Insight:
--Most trading days have near-complete company coverage, with only a few days showing slightly reduced participation.

--Business Value:
--Confirms overall high data quality and consistency.
-- 3.3 Company-wise Data Availability
SELECT company,
       COUNT(DISTINCT trade_date) AS available_days
FROM volumes
GROUP BY company
ORDER BY available_days ASC;
--Insight:
--Some companies have fewer trading records, possibly due to later listing dates or temporary inactivity.

--Business Value:
--Helps identify newer or less active companies.
--3.4 Year-wise Average Coverage Trend
SELECT EXTRACT(YEAR FROM trade_date) AS year,
       ROUND(AVG(company_count), 2) AS avg_coverage,
       ROUND(AVG(company_count) * 100.0 / 500, 2) AS coverage_pct
FROM (
    SELECT trade_date,
    COUNT(DISTINCT company) AS company_count
    FROM volumes
    GROUP BY trade_date
) t
GROUP BY year
ORDER BY year;
-- Insight:
-- Coverage remained consistently high over the years, close to full market coverage.

-- Business Value:
-- The dataset is reliable for long-term trend and time-series analysis.


-- 4️⃣ Sentiment Distribution
-- Count how many records have Positive, Negative, and Neutral sentiment.
SELECT sentiment_label,
       COUNT(*) FROM daily_sentiment
GROUP BY 1;
--Insight:
--The dataset shows a strong presence of both positive and negative sentiment, with fewer neutral sentiments.

--Business Value:
--Indicates that market sentiment is dynamic and responsive to events and news.


-- 5️⃣ Trading Activity Check
-- Find the top 5 trading days with the highest total traded volume across all companies.
SELECT trade_date,
       SUM(volume) AS total_traded_volume,
       RANK() OVER (ORDER BY SUM(volume) DESC) AS activity_rank
FROM volumes
GROUP BY trade_date
ORDER BY total_traded_volume DESC
LIMIT 5;
--Insight:
--Certain trading days experienced exceptionally high trading volumes, likely driven by major news or economic events.

--Business Value:
--High-volume days often indicate strong investor participation and market volatility.


-- 6️⃣ Average Stock Price
-- Calculate the average closing price for each company.
SELECT company,
       ROUND(AVG(close)::numeric, 2) AS avg_close
FROM base_price
GROUP BY 1;
--Insight:
--There is significant variation in average stock prices across companies, reflecting differences in company valuation and market perception.

--Business Value:
--Helps distinguish between high-value and low-value stocks.


-- 7️⃣ Best Performing Companies
-- List companies whose average closing price is higher than the overall market average.
SELECT company,
       ROUND(AVG(close)::numeric, 2) AS avg_close
FROM base_price
GROUP BY company
HAVING AVG(close) > (SELECT AVG(close) FROM base_price)
ORDER BY avg_close DESC;
--Insight:
--Companies with average closing prices above the market average can be considered strong performers.

--Business Value:
--These companies may represent stable and attractive investment opportunities.


-- 8️⃣ Price Extremes
-- For each company, find the highest closing price and the date on which it occurred.
SELECT company,
       trade_date,
       close AS highest_close
FROM (
    SELECT company,
           trade_date,
           close,
           ROW_NUMBER() OVER (PARTITION BY company ORDER BY close DESC) AS rn
    FROM base_price
) t
WHERE rn = 1
ORDER BY highest_close DESC;
--Insight:
--The highest closing price for each company reveals peak performance periods.

--Business Value:
--Helps evaluate growth potential and historical performance strength.


-- 9️⃣ Consistency Analysis
--Identify companies that have price data available for every trading day in the dataset.
--🔹 9.1 Identify Fully Consistent Companies
SELECT company
FROM base_price
GROUP BY company
HAVING COUNT(DISTINCT trade_date) = (
    SELECT COUNT(DISTINCT trade_date)
    FROM base_price
);
--Insight:
--Some companies have price data available for every trading day.

--Business Value:
--Indicates stable and continuously traded companies.

--🔹 9.2 Find Companies with Highest Data Availability
SELECT company,
       COUNT(DISTINCT trade_date) AS available_days
FROM base_price
GROUP BY company
ORDER BY available_days DESC
LIMIT 10;
-- 🔹 9.3 Calculate Missing Trading Days for Each Company
SELECT company,
       COUNT(DISTINCT trade_date) AS available_days,
       (SELECT COUNT(DISTINCT trade_date)FROM base_price) - COUNT(DISTINCT trade_date) AS missing_days
FROM base_price
GROUP BY company
ORDER BY missing_days ASC
LIMIT 10; 
--Insight:
--Some companies missed a few trading days, possibly due to operational or listing factors.

--Business Value:
--Helps identify less consistent or newer stocks.


-- 🔟 Sector-Level Performance
-- Find the average closing price for each business sector.
SELECT c.business_sector,
       ROUND(AVG(b.close)::numeric, 2) AS avg_close
FROM base_price b
JOIN company_fundamentals c
ON b.company = c.company_name
GROUP BY 1
ORDER BY 2;
--Insight:
--Different sectors show varying average stock prices, indicating sector-specific performance differences.

--Business Value:
--Sector selection plays an important role in investment strategy.

-- 🔹 SECTION 3: Sentiment & Market Behavior

-- 1️⃣1️⃣ Sentiment Impact Check
-- Calculate the average closing price on days with Positive sentiment versus Negative sentiment.
SELECT d.sentiment_label,
       ROUND(AVG(b.close)::numeric, 2) AS avg_close
FROM base_price b
JOIN daily_sentiment d
ON b.company = d.company
AND b.trade_date = d.trade_date
GROUP BY d.sentiment_label
ORDER BY avg_close DESC;
--Insight:
--Stock prices tend to be higher on days with positive sentiment compared to negative sentiment days.

--Business Value:
--Market sentiment directly influences stock performance.


-- 1️⃣2️⃣ Company Sentiment Score
-- Find the average sentiment score for each company.
SELECT company,
       ROUND(AVG(sentiment_score)::numeric, 4) AS avg_sentiment_score
FROM daily_sentiment
GROUP BY company
ORDER BY avg_sentiment_score DESC;
--Insight:
--Some companies consistently receive higher sentiment scores, indicating strong investor confidence.

--Business Value:
--These companies may be more attractive to investors.


-- 1️⃣3️⃣ Sentiment vs Volume
-- Identify days where Negative sentiment was followed by high trading volume.
SELECT company,
       trade_date,
       volume,
       prev_sentiment
FROM (
    SELECT v.company,
           v.trade_date,
           v.volume,
           LAG(d.sentiment_label) OVER ( PARTITION BY v.company ORDER BY v.trade_date) AS prev_sentiment
    FROM volumes v
    JOIN daily_sentiment d
    ON v.company = d.company
    AND v.trade_date = d.trade_date
) t
WHERE prev_sentiment = 'Negative'
AND volume > (
    SELECT AVG(volume)
    FROM volumes
)
ORDER BY 3 DESC;
--Insight:
--Negative sentiment is often followed by increased trading volume, indicating strong market reactions.

--Business Value:
--Negative news can trigger high trading activity.


-- 1️⃣4️⃣ Strong Market Confidence
-- Find companies that have more than 50% of their sentiment records marked as Positive.
SELECT company,
       COUNT(*) AS total_records,
       SUM(CASE 
               WHEN sentiment_label = 'Positive' THEN 1 
               ELSE 0 
           END) AS positive_records,
       ROUND((
           SUM(CASE 
                   WHEN sentiment_label = 'Positive' THEN 1 
                   ELSE 0 
               END)::numeric/ COUNT(*) )* 100, 2) AS positive_percentage
FROM daily_sentiment
GROUP BY company
HAVING 
    SUM(CASE 
            WHEN sentiment_label = 'Positive' THEN 1 
            ELSE 0 
        END)::numeric/ COUNT(*) > 0.50
ORDER BY positive_percentage DESC;
--Insight:
--Companies with more than 50% positive sentiment show strong overall investor confidence.

--Business Value:
--These companies may represent stable investment options.


-- 1️⃣5️⃣ Sentiment & Price Movement
--Find trading days where sentiment was Positive and the closing price increased compared to the previous day.
SELECT trade_date,
       sentiment_label,
       open,
       close,
       prev_close
FROM (
    SELECT b.trade_date,
           d.sentiment_label,
           b.open,
           b.close,
           LAG(b.close) OVER (PARTITION BY b.company ORDER BY b.trade_date) AS prev_close
    FROM base_price b
    JOIN daily_sentiment d
    ON b.company = d.company
    AND b.trade_date = d.trade_date
) t
WHERE sentiment_label = 'Positive'
AND close > prev_close;
--Insight:
--Positive sentiment is often associated with stock price increases compared to previous days.

--Business Value:
--Sentiment can serve as a predictive indicator of price movement.

--🔹 SECTION 4: Macro & Market Analysis

-- 1️⃣6️⃣ Macro Environment Effect
-- Calculate the average market index return for each macro environment (Loose, Tight, etc.).
SELECT Market_Volatility_Level,
       ROUND(AVG(index_daily_return_pct)::numeric, 6) AS avg_market_return,
       COUNT(*) AS total_days
FROM global_indices
GROUP BY Market_Volatility_Level
ORDER BY avg_market_return DESC;
--Insight:
--Market returns vary depending on volatility levels, with moderate volatility often producing better returns.

--Business Value:
--Market conditions significantly impact investment performance.


-- 1️⃣7️⃣ Inflation Impact
-- Compare the average market index return during high inflation_rate periods and low inflation_rate periods.
SELECT 
    CASE 
        WHEN i.inflation_rate >= 6 THEN 'High Inflation'
        ELSE 'Low Inflation'
    END AS inflation_level,
    ROUND(AVG(g.index_daily_return_pct)::numeric * 100, 4) 
    AS avg_market_return_pct,
    COUNT(*) AS total_days
FROM inflation_interest i
JOIN global_indices g
ON i.trade_date = g.trade_date
GROUP BY inflation_level
ORDER BY avg_market_return_pct DESC;
--Insight:
--Market returns differ between high-inflation and low-inflation periods.

--Business Value:
--Inflation plays a key role in influencing stock market returns.


-- 1️⃣8️⃣ Volatility Analysis
-- For each Market_Volatility_Level , calculate the average market return and number of trading days.
SELECT Market_Volatility_Level,
       ROUND(AVG(index_daily_return_pct)::numeric * 100, 4) AS avg_market_return_pct,
       COUNT(*) AS trading_days
FROM global_indices
GROUP BY Market_Volatility_Level
ORDER BY avg_market_return_pct DESC;
--Insight:
--Higher volatility periods are often associated with lower or more unstable returns.

--Business Value:
--Volatility increases investment risk.


-- 1️⃣9️⃣ Interest Rate Sensitivity
--Find how stock prices behaved on days when interest rates were rising.
SELECT b.trade_date,
       b.company,
       i.interest_rate_trend,
       (b.close - b.open) AS price_change,
       CASE 
           WHEN b.close > b.open THEN 'Increased'
           WHEN b.close < b.open THEN 'Decreased'
           ELSE 'No Change'
       END AS price_behavior
FROM base_price b
JOIN inflation_interest i
ON b.trade_date = i.trade_date
WHERE i.interest_rate_trend > 0
ORDER BY price_change DESC;
--Insight:
--Rising interest rates influence stock price movements, sometimes negatively impacting stock growth.

--Business Value:
--Interest rate changes affect stock market performance.


-- 2️⃣0️⃣ Market Condition Summary (⭐ End-to-End Question)
-- Create a query that produces a summary table with:
-- Company name, Average closing price, Average sentiment score, Average trading volume,
-- Dominant macro environment (Use data from the last one year only.)
SELECT c.company_name,
       ROUND(AVG(b.close)::numeric, 2) AS avg_close,
       ROUND(AVG(s.sentiment_score)::numeric, 4) AS avg_sentiment,
       ROUND(AVG(v.volume)::numeric, 0) AS avg_volume
       FROM company_fundamentals c
JOIN base_price b
ON c.company_name = b.company
JOIN daily_sentiment s
ON b.company = s.company
AND b.trade_date = s.trade_date
JOIN volumes v
ON b.company = v.company
AND b.trade_date = v.trade_date
JOIN inflation_interest i
ON b.trade_date = i.trade_date
WHERE b.trade_date >= (SELECT MAX(trade_date) - INTERVAL '1 year' FROM base_price)
GROUP BY c.company_name;
--Insight:
--Combining stock prices, sentiment, volume, and macroeconomic conditions provides a complete view of company performance over the past year.

--Business Value:
--This enables comprehensive and informed investment analysis.