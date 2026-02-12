# ===============================
# STOCK PRICE PREDICTION SCRIPT
# ===============================

import pandas as pd
import joblib
import os

# ===============================
# PATH SETUP
# ===============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "stock_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "company_encoder.pkl")

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "stock_market_clean_dataset_with_Feature_Eng",
    "nse_prices.csv"
)

# ===============================
# LOAD MODEL AND ENCODER
# ===============================

print("Loading Model and Encoder...")

model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

print("Model and Encoder Loaded Successfully")


# ===============================
# LOAD DATASET
# ===============================

print("Loading Dataset...")

df = pd.read_csv(DATA_PATH)

df.dropna(inplace=True)

df["trade_date"] = pd.to_datetime(df["trade_date"])

df.sort_values(["company", "trade_date"], inplace=True)

print("Dataset Loaded Successfully")


# ===============================
# FEATURE ENGINEERING
# ===============================

print("Performing Feature Engineering...")

# Encode company
df["company_encoded"] = encoder.transform(df["company"])

# Previous close
df["prev_close"] = df.groupby("company")["close"].shift(1)

# Moving averages
df["ma_5"] = (
    df.groupby("company")["close"]
    .rolling(5)
    .mean()
    .reset_index(0, drop=True)
)

df["ma_10"] = (
    df.groupby("company")["close"]
    .rolling(10)
    .mean()
    .reset_index(0, drop=True)
)

# Volatility
df["volatility"] = df["high"] - df["low"]

df.dropna(inplace=True)

print("Feature Engineering Completed")


# ===============================
# FUNCTION: PREDICT FOR COMPANY
# ===============================

def predict_company(company_name):

    company_data = df[df["company"] == company_name]

    if company_data.empty:
        print(f"No data found for {company_name}")
        return

    latest = company_data.iloc[-1]

    print("\n===============================")
    print("Company:", company_name)
    print("Current Price:", latest["close"])

    input_df = pd.DataFrame([{
        "company_encoded": latest["company_encoded"],
        "open": latest["open"],
        "high": latest["high"],
        "low": latest["low"],
        "close": latest["close"],
        "prev_close": latest["prev_close"],
        "ma_5": latest["ma_5"],
        "ma_10": latest["ma_10"],
        "volatility": latest["volatility"]
    }])

    prediction = model.predict(input_df)[0]

    predicted_price = round(prediction, 2)

    print("Predicted Next Day Price:", predicted_price)

    if predicted_price > latest["close"]:
        print("Trend: UP 📈")
    else:
        print("Trend: DOWN 📉")

    print("===============================")

    return predicted_price


# ===============================
# MAIN TERMINAL EXECUTION
# ===============================

if __name__ == "__main__":

    print("\nAvailable Companies:")

    companies = df["company"].unique()

    for i, comp in enumerate(companies[:20]):
        print(comp)

    company = input("\nEnter Company Name: ").strip().upper()

    predict_company(company)

    print("\nPrediction Completed Successfully")
