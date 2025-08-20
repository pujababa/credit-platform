import pandas as pd
import matplotlib.pyplot as plt  #type: ignore

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def analyze_multiple_stocks(companies):
    colors = ["blue", "green", "orange", "purple"]
    fig, (ax_price, ax_rsi) = plt.subplots(2, 1, figsize=(16,10), sharex=True,gridspec_kw={'height_ratios':[3,1]})

    for i, (file, name) in enumerate(companies.items()):
        data = pd.read_csv(file)
        data["Date"] = pd.to_datetime(data["Date"])
        data.set_index("Date", inplace=True)
        data["MA20"] = data["Close"].rolling(window=20).mean()
        data["RSI"] = calculate_rsi(data)

        ax_price.plot(data.index, data["Close"], color=colors[i], label=f"{name} Close Price")
        ax_price.plot(data.index, data["MA20"], linestyle="--", color=colors[i], label=f"{name} MA20")
        ax_rsi.plot(data.index, data["RSI"], color=colors[i], label=f"{name} RSI")

        last_rsi = data["RSI"].iloc[-1]
        if last_rsi > 70:
            print(f"{name}: RSI {last_rsi:.2f} → Overbought")
        elif last_rsi < 30:
            print(f"{name}: RSI {last_rsi:.2f} → Oversold")
        else:
            print(f"{name}: RSI {last_rsi:.2f} → Neutral")

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
    plt.savefig("stocks_comparison_pro.png", dpi=300)
    plt.show()
