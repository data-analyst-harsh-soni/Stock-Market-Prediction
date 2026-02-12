DROP TABLE IF EXISTS company_summary;

CREATE TABLE company_summary AS
SELECT 
       b.company,

       COUNT(DISTINCT b.trade_date) AS total_trading_days,

       ROUND(AVG(b.close)::numeric, 2) AS avg_close_price,

       ROUND(MIN(b.close)::numeric, 2) AS min_close_price,

       ROUND(MAX(b.close)::numeric, 2) AS max_close_price,

       ROUND(AVG(v.volume)::numeric, 0) AS avg_volume,

       ROUND(MAX(v.volume)::numeric, 0) AS max_volume,

       ROUND(AVG(s.sentiment_score)::numeric, 4) AS avg_sentiment_score

FROM base_price b

LEFT JOIN volumes v 
ON b.company = v.company 
AND b.trade_date = v.trade_date

LEFT JOIN daily_sentiment s 
ON b.company = s.company 
AND b.trade_date = s.trade_date

GROUP BY b.company;

DROP TABLE IF EXISTS market_daily_summary;

CREATE TABLE market_daily_summary AS
SELECT 

       b.trade_date,

       COUNT(DISTINCT b.company) AS total_companies,

       ROUND(AVG(b.close)::numeric, 2) AS market_avg_price,

       ROUND(SUM(v.volume)::numeric, 0) AS total_market_volume,

       ROUND(AVG(s.sentiment_score)::numeric, 4) AS market_sentiment

FROM base_price b

LEFT JOIN volumes v
ON b.company = v.company
AND b.trade_date = v.trade_date

LEFT JOIN daily_sentiment s
ON b.company = s.company
AND b.trade_date = s.trade_date

GROUP BY b.trade_date;

DROP TABLE IF EXISTS volume_summary;

CREATE TABLE volume_summary AS
SELECT 

       company,

       ROUND(AVG(volume)::numeric, 0) AS avg_volume,

       ROUND(MAX(volume)::numeric, 0) AS max_volume,

       COUNT(*) FILTER (WHERE volume_spike = TRUE) AS total_spikes

FROM volumes

GROUP BY company;

DROP TABLE IF EXISTS sentiment_summary;

CREATE TABLE sentiment_summary AS
SELECT 

       company,

       ROUND(AVG(sentiment_score)::numeric, 4) AS avg_sentiment,

       ROUND(MIN(sentiment_score)::numeric, 4) AS min_sentiment,

       ROUND(MAX(sentiment_score)::numeric, 4) AS max_sentiment

FROM daily_sentiment

GROUP BY company;
