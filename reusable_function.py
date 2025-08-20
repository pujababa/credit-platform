import pandas as pd
import matplotlib.pyplot as plt  #type: ignore

def analyze_stock(file, company_name):
    # CSV load karo
    data = pd.read_csv(file, parse_dates=["Date"], index_col="Date")

    # Moving Average
    data["MA7"] = data["Close"].rolling(window=7).mean()

    # Plot
    plt.figure(figsize=(12,6))
    plt.plot(data.index, data["Open"], label="Open Price", color="blue")
    plt.plot(data.index, data["Close"], label="Close Price", color="green")
    plt.plot(data.index, data["MA7"], label="7-Day Moving Average", color="red", linestyle="--")

    # Labels
    plt.title(f"{company_name} Stock Prices (Last 1 Month)")
    plt.xlabel("Date")
    plt.ylabel("Price (INR)")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()
