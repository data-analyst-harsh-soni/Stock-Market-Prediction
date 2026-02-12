import pandas as pd
import numpy as np
import os
import random
from datetime import datetime

# reproducibility
np.random.seed(42)
random.seed(42)

# base directory
base_dir = "stock_market_dataset"

# folders
folders = [
    "raw_data",
    "company_data",
    "macro_data",
    "news_sentiment",
    "trading_data",
    "metadata",
    "logs"
]

# create folders
for folder in folders:
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

# date range (business days only)
start_date = datetime(2015, 1, 1)
end_date = datetime(2026, 2, 1)

dates = pd.date_range(
    start=start_date,
    end=end_date,
    freq="B"
)

# companies list
companies = [
    "HDFC", "HDFCBANK", "ICICIBANK", "SBIN", "AXISBANK",
    "KOTAKBANK", "INDUSINDBK", "BANKBARODA", "PNB", "CANBK",

    "RELIANCE", "ONGC", "IOC", "BPCL", "HPCL",
    "TATAPOWER", "ADANIPOWER", "NTPC", "POWERGRID", "COALINDIA",

    "TCS", "INFY", "WIPRO", "HCLTECH", "TECHM",
    "LTIM", "PERSISTENT", "MPHASIS", "COFORGE", "OFSS",

    "SUNPHARMA", "DRREDDY", "CIPLA", "DIVISLAB", "BIOCON",
    "LUPIN", "AUROPHARMA", "TORNTPHARM", "ALKEM", "GLENMARK",

    "TATASTEEL", "JSWSTEEL", "HINDALCO", "VEDL", "SAIL",

    "MARUTI", "TATAMOTORS", "M&M", "BAJAJ-AUTO", "HEROMOTOCO"
]

# sector mapping
company_sector_map = {

    "HDFC": "Finance",
    "HDFCBANK": "Finance",
    "ICICIBANK": "Finance",
    "SBIN": "Finance",
    "AXISBANK": "Finance",
    "KOTAKBANK": "Finance",
    "INDUSINDBK": "Finance",
    "BANKBARODA": "Finance",
    "PNB": "Finance",
    "CANBK": "Finance",

    "RELIANCE": "Energy",
    "ONGC": "Energy",
    "IOC": "Energy",
    "BPCL": "Energy",
    "HPCL": "Energy",
    "TATAPOWER": "Energy",
    "ADANIPOWER": "Energy",
    "NTPC": "Energy",
    "POWERGRID": "Energy",
    "COALINDIA": "Energy",

    "TCS": "IT",
    "INFY": "IT",
    "WIPRO": "IT",
    "HCLTECH": "IT",
    "TECHM": "IT",
    "LTIM": "IT",
    "PERSISTENT": "IT",
    "MPHASIS": "IT",
    "COFORGE": "IT",
    "OFSS": "IT",

    "SUNPHARMA": "Pharma",
    "DRREDDY": "Pharma",
    "CIPLA": "Pharma",
    "DIVISLAB": "Pharma",
    "BIOCON": "Pharma",
    "LUPIN": "Pharma",
    "AUROPHARMA": "Pharma",
    "TORNTPHARM": "Pharma",
    "ALKEM": "Pharma",
    "GLENMARK": "Pharma",

    "TATASTEEL": "Metal",
    "JSWSTEEL": "Metal",
    "HINDALCO": "Metal",
    "VEDL": "Metal",
    "SAIL": "Metal",

    "MARUTI": "Auto",
    "TATAMOTORS": "Auto",
    "M&M": "Auto",
    "BAJAJ-AUTO": "Auto",
    "HEROMOTOCO": "Auto"
}

# sector volatility
sector_volatility = {

    "Finance": 0.012,
    "IT": 0.015,
    "Energy": 0.018,
    "Pharma": 0.017,
    "Metal": 0.022,
    "Auto": 0.016
}

# sector annual growth
sector_growth = {

    "Finance": 0.10,
    "IT": 0.14,
    "Energy": 0.09,
    "Pharma": 0.11,
    "Metal": 0.08,
    "Auto": 0.10
}

trading_days = 252


# stock price generator
def generate_stock_prices(market):

    data = []

    for company in companies:

        sector = company_sector_map[company]

        volatility = sector_volatility[sector]

        annual_growth = sector_growth[sector]

        daily_growth = annual_growth / trading_days

        price = random.uniform(100, 2500)

        for date in dates:

            drift = price * daily_growth

            shock = price * np.random.normal(0, volatility)

            open_price = price + shock

            close_price = open_price + price * np.random.normal(0, volatility)

            high_price = max(open_price, close_price) * random.uniform(1.001, 1.02)

            low_price = min(open_price, close_price) * random.uniform(0.98, 0.999)

            # avoid negative price
            open_price = max(open_price, 5)
            close_price = max(close_price, 5)
            high_price = max(high_price, open_price, close_price)
            low_price = max(min(low_price, open_price, close_price), 5)

            data.append([
             date,
             market,
             company,
             round(open_price, 2),
             round(high_price, 2),
             round(low_price, 2),
             round(close_price, 2)
            ])


            price = close_price + drift

    df = pd.DataFrame(
        data,
        columns=[
                  "date",
                  "market",
                  "company",
                  "open",
                  "high",
                  "low",
                  "close"
                ])

    return df


# generate NSE data
nse = generate_stock_prices("NSE")

# generate BSE data
bse = generate_stock_prices("BSE")


# save datasets
nse.to_csv(
    f"{base_dir}/raw_data/nse_prices.csv",
    index=False
)

bse.to_csv(
    f"{base_dir}/raw_data/bse_prices.csv",
    index=False
)

print("✅ NSE and BSE datasets generated successfully")


# ----------- REALISTIC GLOBAL INDICES GENERATION -----------

index_config = {
    "SENSEX": {
        "start": (20000, 26000),
        "daily_volatility": 120,
        "annual_growth": 0.10
    },
    "NIFTY50": {
        "start": (6000, 9000),
        "daily_volatility": 80,
        "annual_growth": 0.11
    },
    "NASDAQ": {
        "start": (4000, 6000),
        "daily_volatility": 150,
        "annual_growth": 0.13
    },
    "DOWJONES": {
        "start": (15000, 20000),
        "daily_volatility": 130,
        "annual_growth": 0.09
    }
}

global_data = []

trading_days_per_year = 252

for idx, cfg in index_config.items():

    value = random.uniform(cfg["start"][0], cfg["start"][1])

    daily_growth = cfg["annual_growth"] / trading_days_per_year

    for i, date in enumerate(dates):

        # market movement
        noise = np.random.normal(0, cfg["daily_volatility"])

        # long-term growth
        growth = value * daily_growth

        value = value + noise + growth

        global_data.append([
            date,
            idx,
            round(value, 2)
        ])

pd.DataFrame(
    global_data,
    columns=["date", "index", "value"]
).to_csv(
    f"{base_dir}/raw_data/global_indices.csv",
    index=False
)

print("✅ Realistic Global Indices Generated Successfully")


# ----------- REALISTIC FUNDAMENTALS GENERATION -----------

sector_pe_range = {
    "Finance": (10, 25),
    "IT": (20, 45),
    "Energy": (8, 20),
    "Pharma": (18, 35),
    "Metal": (6, 15),
    "Auto": (15, 30)
}

sector_de_range = {
    "Finance": (1.5, 4.0),
    "IT": (0.1, 0.8),
    "Energy": (1.0, 3.5),
    "Pharma": (0.2, 1.2),
    "Metal": (0.5, 2.5),
    "Auto": (0.5, 2.0)
}

sector_roe_range = {
    "Finance": (10, 20),
    "IT": (15, 30),
    "Energy": (8, 18),
    "Pharma": (12, 25),
    "Metal": (8, 16),
    "Auto": (10, 22)
}

fundamentals = []

for company in companies:

    sector = company_sector_map[company]

    pe_low, pe_high = sector_pe_range[sector]
    de_low, de_high = sector_de_range[sector]
    roe_low, roe_high = sector_roe_range[sector]

    pe = round(random.uniform(pe_low, pe_high), 2)
    de = round(random.uniform(de_low, de_high), 2)
    roe = round(random.uniform(roe_low, roe_high), 2)

    fundamentals.append([
        company,
        sector,
        pe,
        de,
        roe
    ])

fundamentals_df = pd.DataFrame(
    fundamentals,
    columns=[
        "company",
        "sector",
        "pe_ratio",
        "debt_equity",
        "roe"
    ]
)

fundamentals_df.to_csv(
    f"{base_dir}/company_data/company_fundamentals.csv",
    index=False
)

print("✅ Realistic Fundamentals Generated Successfully")


# ----------- FIXED REALISTIC SENTIMENT GENERATION -----------

# sector sentiment bias (stronger realistic bias)
sector_sentiment_bias = {
    "Finance": 0.15,
    "IT": 0.20,
    "Energy": 0.10,
    "Pharma": 0.12,
    "Metal": 0.05,
    "Auto": 0.08
}

# company-specific bias (large companies more positive)
company_sentiment_bias = {
    "RELIANCE": 0.25,
    "TCS": 0.22,
    "HDFCBANK": 0.20,
    "INFY": 0.18,
    "ICICIBANK": 0.19,
    "SBIN": 0.17
}

sentiment = []

for company in companies:

    sector = company_sector_map[company]

    # base bias
    sector_bias = sector_sentiment_bias[sector]

    # company bias (if exists)
    company_bias = company_sentiment_bias.get(company, random.uniform(0.02, 0.10))

    # overall bias
    base_bias = sector_bias + company_bias

    for i, date in enumerate(dates):

        # market cycle (bull/bear cycle)
        cycle = 0.15 * np.sin(i / 250)

        # small random noise
        noise = random.uniform(-0.15, 0.15)

        # occasional big news spike
        spike = 0
        if random.random() < 0.04:
            spike = random.uniform(-0.4, 0.6)

        sentiment_score = (
            base_bias +
            cycle +
            noise +
            spike
        )

        # clamp between -1 and +1
        sentiment_score = max(-1, min(1, sentiment_score))

        sentiment.append([
            date,
            company,
            round(sentiment_score, 3)
        ])


sentiment_df = pd.DataFrame(
    sentiment,
    columns=["date", "company", "sentiment_score"]
)

sentiment_df.to_csv(
    f"{base_dir}/news_sentiment/daily_sentiment.csv",
    index=False
)

print("✅ Fixed Realistic Sentiment Generated Successfully")

# ----------- FIXED REALISTIC VOLUME GENERATION -----------

# define company size categories
large_caps = ["RELIANCE", "HDFCBANK", "ICICIBANK", "TCS", "INFY", "SBIN"]
mid_caps = ["AXISBANK", "KOTAKBANK", "NTPC", "POWERGRID", "HCLTECH", "WIPRO"]
small_caps = list(set(companies) - set(large_caps) - set(mid_caps))

# assign base volume based on company size
company_base_volume = {}

for company in companies:

    if company in large_caps:
        company_base_volume[company] = random.randint(8000000, 15000000)

    elif company in mid_caps:
        company_base_volume[company] = random.randint(3000000, 7000000)

    else:
        company_base_volume[company] = random.randint(500000, 2500000)


# sector multipliers
sector_multiplier = {
    "Finance": 1.5,
    "Energy": 1.4,
    "IT": 1.2,
    "Pharma": 1.1,
    "Metal": 1.3,
    "Auto": 1.0
}


# generate volume
volume = []

for company in companies:

    base = company_base_volume[company]

    sector = company_sector_map[company]

    multiplier = sector_multiplier[sector]

    for i, date in enumerate(dates):

        seasonal = 1 + 0.2 * np.sin(i / 200)

        noise = random.uniform(0.7, 1.3)

        spike = 1
        if random.random() < 0.02:
            spike = random.uniform(1.5, 4)

        daily_volume = int(
            base *
            multiplier *
            seasonal *
            noise *
            spike
        )

        volume.append([
            date,
            company,
            daily_volume
        ])


# save file
volume_df = pd.DataFrame(
    volume,
    columns=["date", "company", "volume"]
)

volume_df.to_csv(
    f"{base_dir}/trading_data/volumes.csv",
    index=False
)

print("✅ Realistic Volume Generated Successfully")


pd.DataFrame({
    "column": ["open","close","sentiment_score","inflation"],
    "description": [
        "Opening price of stock",
        "Closing price of stock",
        "News sentiment score (-1 to 1)",
        "Inflation percentage"
    ]
}).to_csv(f"{base_dir}/metadata/data_dictionary.csv", index=False)

with open(f"{base_dir}/logs/generation_log.txt", "w") as f:
    f.write("Stock Market Dataset Generated Successfully")

print("✅ Dataset Generated Successfully")

# ----------- REALISTIC MACRO ECONOMIC DATA GENERATION -----------

macro_data = []

inflation = 5.5
interest_rate = 6.5

for i, date in enumerate(dates):

    # inflation slow movement
    inflation += np.random.normal(0, 0.02)

    # interest rate slower movement
    interest_rate += np.random.normal(0, 0.015)

    # keep within realistic bounds
    inflation = max(2.5, min(inflation, 9))
    interest_rate = max(3.5, min(interest_rate, 10))

    macro_data.append([
        date,
        round(inflation, 2),
        round(interest_rate, 2)
    ])

macro_df = pd.DataFrame(
    macro_data,
    columns=[
        "date",
        "inflation",
        "interest_rate"
    ]
)

macro_df.to_csv(
    f"{base_dir}/macro_data/inflation_interest.csv",
    index=False
)

print("✅ Realistic Macro Data Generated Successfully")
