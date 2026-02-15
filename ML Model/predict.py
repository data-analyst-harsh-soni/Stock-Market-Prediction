

import pandas as pd
import joblib
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "stock_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "company_encoder.pkl")

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "stock_market_clean_dataset_with_Feature_Eng",
    "nse_prices.csv"
)

print("Loading Model and Encoder...")

model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

print("Model and Encoder Loaded Successfully")



print("Loading Dataset...")

df = pd.read_csv(DATA_PATH, low_memory=False)

df = df[df["company"] != "company"]

df["company"] = df["company"].astype(str).str.strip().str.upper()

numeric_cols = ["open", "high", "low", "close"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["trade_date"] = pd.to_datetime(
    df["trade_date"],
    dayfirst=True,
    errors="coerce"
)

df.dropna(inplace=True)

df.sort_values(["company", "trade_date"], inplace=True)

df.reset_index(drop=True, inplace=True)

print("Dataset Loaded Successfully")


print("Performing Feature Engineering...")

def safe_encode(company):
    if company in encoder.classes_:
        return encoder.transform([company])[0]
    return None

df["company_encoded"] = df["company"].apply(safe_encode)

df.dropna(subset=["company_encoded"], inplace=True)

df["prev_close"] = df.groupby("company")["close"].shift(1)

df["ma_5"] = (
    df.groupby("company")["close"]
    .rolling(5)
    .mean()
    .reset_index(level=0, drop=True)
)

df["ma_10"] = (
    df.groupby("company")["close"]
    .rolling(10)
    .mean()
    .reset_index(level=0, drop=True)
)
df["volatility"] = df["high"] - df["low"]

df.dropna(inplace=True)

print("Feature Engineering Completed")


def predict_company(company_name):

    company_name = company_name.strip().upper()

    if company_name not in encoder.classes_:
        print(f"❌ Company '{company_name}' not found in trained model")
        return None

    company_data = df[df["company"] == company_name]

    if company_data.empty:
        print(f"❌ No dataset data found for {company_name}")
        return None

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

    predicted_price = round(float(prediction), 2)

    print("Predicted Next Day Price:", predicted_price)

    if predicted_price > latest["close"]:
        print("Trend: UP 📈")
    else:
        print("Trend: DOWN 📉")

    print("===============================")

    return predicted_price


if __name__ == "__main__":

    print("\nAvailable Companies:\n")

    companies = sorted(df["company"].unique())

    for comp in companies[:50]:
        print(comp)

    company = input("\nEnter Company Name: ").strip().upper()

    result = predict_company(company)

    if result is not None:
        print("\nPrediction Completed Successfully")
