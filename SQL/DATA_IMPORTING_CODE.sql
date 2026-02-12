ALTER USER postgres WITH PASSWORD 'postgres';

DROP TABLE IF EXISTS company_fundamentals;
CREATE TABLE company_fundamentals (
    company_name VARCHAR(20),
    business_sector VARCHAR(50),
    price_earnings_ratio DOUBLE PRECISION,
    debt_to_equity DOUBLE PRECISION,
    return_on_equity DOUBLE PRECISION,
    performance VARCHAR(20),
    valuation_type VARCHAR(20),
    leverage_risk VARCHAR(10),
    profitability_flag INTEGER,
    investment_grade VARCHAR(10)
);
COPY company_fundamentals
FROM 'D:\DATA_ANALYST\FULL_STACK_FROJECT\Stock Market Prediction\stock_market_clean_dataset_with_Feature_Eng/company_fundamentals.csv'
DELIMITER ','
CSV HEADER;
SELECT COUNT(*) FROM company_fundamentals;

DROP TABLE IF EXISTS base_price;
CREATE TABLE base_price (
    company VARCHAR(20),
    trade_date DATE,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION
);
COPY base_price
FROM 'D:\DATA_ANALYST\FULL_STACK_FROJECT\Stock Market Prediction\stock_market_clean_dataset_with_Feature_Eng/base_price.csv'
DELIMITER ','
CSV HEADER;
SELECT COUNT(*) FROM base_price;

DROP TABLE IF EXISTS nse_prices;
CREATE TABLE nse_prices (
    trade_date DATE,
    company VARCHAR(20),
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION
);
COPY nse_prices
FROM 'D:\DATA_ANALYST\FULL_STACK_FROJECT\Stock Market Prediction\stock_market_clean_dataset_with_Feature_Eng/nse_prices.csv'
DELIMITER ','
CSV HEADER;
SELECT COUNT(*) FROM nse_prices;

DROP TABLE IF EXISTS global_indices;
CREATE TABLE global_indices (
    index_name VARCHAR(30),
    trade_date DATE,
    index_price DOUBLE PRECISION,
    index_daily_return_pct DOUBLE PRECISION,
    avg_return_7d DOUBLE PRECISION,
    avg_return_21d DOUBLE PRECISION,
    volatility_7d_pct DOUBLE PRECISION,
    volatility_21d_pct DOUBLE PRECISION,
    moving_avg_7d DOUBLE PRECISION,
    moving_avg_21d DOUBLE PRECISION,
    trend_flag INTEGER,
    return_momentum DOUBLE PRECISION,
    all_time_high_till_date DOUBLE PRECISION,
    drawdown_pct DOUBLE PRECISION,
    Market_Volatility_Level VARCHAR(20)
);
COPY global_indices
FROM 'D:/DATA_ANALYST/FULL_STACK_FROJECT/Stock Market Prediction/stock_market_clean_dataset_with_Feature_Eng/global_indices.csv'
DELIMITER ','
CSV HEADER;
SELECT COUNT(*) FROM global_indices;

DROP TABLE IF EXISTS inflation_interest;
CREATE TABLE inflation_interest (
    trade_date DATE,
    inflation_rate DOUBLE PRECISION,
    interest_rate DOUBLE PRECISION,
    real_interest_rate DOUBLE PRECISION,
    inflation_trend DOUBLE PRECISION,
    interest_rate_trend DOUBLE PRECISION,
    macro_environment VARCHAR(10)
);
COPY inflation_interest
FROM 'D:/DATA_ANALYST/FULL_STACK_FROJECT/Stock Market Prediction/stock_market_clean_dataset_with_Feature_Eng/inflation_interest.csv'
DELIMITER ','
CSV HEADER;
SELECT COUNT(*) FROM inflation_interest;

DROP TABLE IF EXISTS daily_sentiment;
CREATE TABLE daily_sentiment (
    trade_date DATE,
    company VARCHAR(20),
    sentiment_score DOUBLE PRECISION,
    sentiment_label VARCHAR(10)
);
COPY daily_sentiment
FROM 'D:/DATA_ANALYST/FULL_STACK_FROJECT/Stock Market Prediction/stock_market_clean_dataset_with_Feature_Eng/daily_sentiment.csv'
DELIMITER ','
CSV HEADER;
SELECT COUNT(*) FROM daily_sentiment;

DROP TABLE IF EXISTS volumes ;
CREATE TABLE volumes (
    company VARCHAR(20),
    trade_date DATE,
    volume BIGINT,
    avg_volume_7d DOUBLE PRECISION,
    avg_volume_7d_million DOUBLE PRECISION,
    volume_spike BOOLEAN
);
COPY volumes
FROM 'D:/DATA_ANALYST/FULL_STACK_FROJECT/Stock Market Prediction/stock_market_clean_dataset_with_Feature_Eng/volumes.csv'
DELIMITER ','
CSV HEADER;
SELECT COUNT(*) FROM volumes;

DROP TABLE IF EXISTS data_dictionary;
CREATE TABLE data_dictionary (
    feature_name VARCHAR(50),
    feature_description VARCHAR(255)
);
COPY data_dictionary
FROM 'D:/DATA_ANALYST/FULL_STACK_FROJECT/Stock Market Prediction/stock_market_clean_dataset_with_Feature_Eng/data_dictionary.csv'
DELIMITER ','
CSV HEADER;
SELECT COUNT(*) FROM data_dictionary;


ALTER TABLE company_fundamentals
ADD CONSTRAINT pk_company PRIMARY KEY (company_name);
ALTER TABLE base_price
ADD CONSTRAINT pk_base_price PRIMARY KEY (company, trade_date);
ALTER TABLE nse_prices
ADD CONSTRAINT pk_nse_price PRIMARY KEY (company, trade_date);
ALTER TABLE base_price
ADD CONSTRAINT fk_base_price_company
FOREIGN KEY (company)
REFERENCES company_fundamentals(company_name);

ALTER TABLE daily_sentiment
ADD CONSTRAINT fk_sentiment_company
FOREIGN KEY (company)
REFERENCES company_fundamentals(company_name);
