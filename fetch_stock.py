import yfinance as yf  # type: ignore

companies = {
    "reliance_stock.csv": "RELIANCE.NS",
    "tcs_stock.csv": "TCS.NS",
    "infosys_stock.csv": "INFY.NS",
    "hdfc_stock.csv": "HDFCBANK.NS"  # Correct ticker
}

for filename, ticker in companies.items():
    data = yf.Ticker(ticker).history(period="1mo")
    if data.empty:
        print(f"⚠️ No data found for {ticker}")
        continue
    data.to_csv(filename)
    print(f"{filename} saved successfully ✅")
