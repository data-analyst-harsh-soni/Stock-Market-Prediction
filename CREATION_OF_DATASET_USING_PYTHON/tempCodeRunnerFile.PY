import pandas as pd
import numpy as np
from faker import Faker
import os
from datetime import datetime, timedelta
import random

fake = Faker()
np.random.seed(42)

base_dir = "stock_market_dataset"
folders = [
    "raw_data", "company_data", "macro_data",
    "news_sentiment", "trading_data", "metadata", "logs"
]

for folder in folders:
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

start_date = datetime(2015, 1, 1)
end_date = datetime(2025, 1, 1)
dates = pd.date_range(start_date, end_date, freq='B')  

companies = [f"COMP_{i}" for i in range(1, 501)]  
sectors = ["IT", "Finance", "Pharma", "Energy", "FMCG", "Metal", "Auto"]

def generate_stock_prices(market):
    data = []
    for company in companies:
        price = random.uniform(100, 3000)
        for date in dates:
            open_p = price + np.random.normal(0, 10)
            close_p = open_p + np.random.normal(0, 15)
            high = max(open_p, close_p) + abs(np.random.normal(0, 5))
            low = min(open_p, close_p) - abs(np.random.normal(0, 5))

            if random.random() < 0.01:
                close_p = np.nan

            data.append([
                date, company, round(open_p,2),
                round(high,2), round(low,2),
                round(close_p,2)
            ])
            price = close_p if not np.isnan(close_p) else price

    df = pd.DataFrame(data, columns=[
        "date", "company", "open", "high", "low", "close"
    ])
    return df

nse = generate_stock_prices("NSE")
bse = generate_stock_prices("BSE")

nse.to_csv(f"{base_dir}/raw_data/nse_prices.csv", index=False)
bse.to_csv(f"{base_dir}/raw_data/bse_prices.csv", index=False)

indices = ["SENSEX", "NIFTY50", "NASDAQ", "DOWJONES"]
global_data = []

for idx in indices:
    value = random.uniform(20000, 60000)
    for date in dates:
        value += np.random.normal(0, 100)
        global_data.append([date, idx, round(value,2)])

pd.DataFrame(global_data, columns=["date", "index", "value"]) \
    .to_csv(f"{base_dir}/raw_data/global_indices.csv", index=False)

fundamentals = []
for company in companies:
    fundamentals.append([
        company,
        random.choice(sectors),
        round(random.uniform(5, 40),2),   
        round(random.uniform(0.5, 5),2),  
        round(random.uniform(5, 30),2)    
    ])

pd.DataFrame(fundamentals, columns=[
    "company", "sector", "pe_ratio", "debt_equity", "roe"
]).to_csv(f"{base_dir}/company_data/company_fundamentals.csv", index=False)

macro = []
for date in dates:
    macro.append([
        date,
        round(random.uniform(4,8),2),   
        round(random.uniform(5,9),2)    
    ])

pd.DataFrame(macro, columns=[
    "date", "inflation", "interest_rate"
]).to_csv(f"{base_dir}/macro_data/inflation_interest.csv", index=False)

sentiment = []
for company in companies:
    for date in random.sample(list(dates), 1200):
        sentiment.append([
            date, company,
            round(random.uniform(-1,1),2)
        ])

pd.DataFrame(sentiment, columns=[
    "date", "company", "sentiment_score"
]).to_csv(f"{base_dir}/news_sentiment/daily_sentiment.csv", index=False)

volume = []
for company in companies:
    for date in dates:
        volume.append([
            date, company,
            random.randint(10000, 5000000)
        ])

pd.DataFrame(volume, columns=[
    "date", "company", "volume"
]).to_csv(f"{base_dir}/trading_data/volumes.csv", index=False)

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
