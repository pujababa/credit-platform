import yfinance as yf  # type: ignore
import pandas as pd
import matplotlib.pyplot as plt  # type: ignore
from datetime import datetime

# 🔹 Email Function (Console Test)
def send_email(ticker, last_rsi, status, attachment_path=None):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"--- EMAIL ALERT ---")
    print(f"Stock: {ticker}")
    print(f"RSI Value: {last_rsi:.2f}")
    print(f"Status: {status}")
    print(f"Time: {now}")
    if attachment_path:
        print(f"Graph attached: {attachment_path}")
    print("------------------\n")

# 🔹 Companies & CSV
companies = {
    "reliance_stock.csv": "RELIANCE.NS",
    "tcs_stock.csv": "TCS.NS",
    "infosys_stock.csv": "INFY.NS",
    "hdfc_stock.csv": "HDFCBANK.NS"
}

# 🔹 Fetch CSV Files
for filename, ticker in companies.items():
    data = yf.Ticker(ticker).history(period="1mo")
    if data.empty:
        print(f"⚠️ No data found for {ticker}")
        continue
    data.to_csv(filename)
    print(f"{filename} saved successfully ✅")

# 🔹 RSI Function
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# 🔹 Multi-Company Analysis
colors = ["blue", "green", "orange", "purple"]
fig, (ax_price, ax_rsi) = plt.subplots(2, 1, figsize=(16,10), sharex=True, gridspec_kw={'height_ratios':[3,1]})
log_file = r"C:\Users\npuja\OneDrive\Desktop\credit-platform\rsi_log.txt"
graph_file = r"C:\Users\npuja\OneDrive\Desktop\credit-platform\stocks_comparison_pro.png"

for i, (file, ticker) in enumerate(companies.items()):
    try:
        data = pd.read_csv(file)
    except FileNotFoundError:
        print(f"⚠️ {file} not found, skipping...")
        continue

    data["Date"] = pd.to_datetime(data["Date"])
    data.set_index("Date", inplace=True)
    data["MA20"] = data["Close"].rolling(window=20).mean()
    data["RSI"] = calculate_rsi(data)

    # 🔹 Price plot
    ax_price.plot(data.index, data["Close"], color=colors[i], label=f"{ticker} Close Price")
    ax_price.plot(data.index, data["MA20"], linestyle="--", color=colors[i], label=f"{ticker} MA20")

    # 🔹 RSI plot
    ax_rsi.plot(data.index, data["RSI"], color=colors[i], label=f"{ticker} RSI")

    # 🔹 RSI Alerts + Logging + Console Email
    last_rsi = data["RSI"].iloc[-1]
    if last_rsi > 70:
        status = "Overbought"
    elif last_rsi < 30:
        status = "Oversold"
    else:
        status = "Neutral"

    print(f"{ticker}: RSI {last_rsi:.2f} → {status}")

    # Logging
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{now} - {ticker}: RSI {last_rsi:.2f} → {status}\n")

    # Console Email Alert
    if last_rsi > 70 or last_rsi < 30:
        send_email(ticker, last_rsi, status, graph_file)

# 🔹 Formatting plots
ax_price.set_title("Stock Close Price & 20-Day MA Comparison")
ax_price.set_ylabel("Price (INR)")
ax_price.grid(True, linestyle="--", alpha=0.5)
ax_price.legend()

ax_rsi.set_title("RSI (14)")
ax_rsi.set_ylabel("RSI Value")
ax_rsi.set_xlabel("Date")
ax_rsi.grid(True, linestyle="--", alpha=0.5)
ax_rsi.axhline(70, color="red", linestyle="--", alpha=0.5)
ax_rsi.axhline(30, color="green", linestyle="--", alpha=0.5)
ax_rsi.fill_between(data.index, 70, 100, color="red", alpha=0.1)
ax_rsi.fill_between(data.index, 0, 30, color="green", alpha=0.1)
ax_rsi.legend()

plt.tight_layout()
plt.savefig(graph_file, dpi=300)
plt.show()
