from analyze_stock import analyze_multiple_stocks

companies = {
    "reliance_stock.csv": "Reliance",
    "tcs_stock.csv": "TCS",
    "infosys_stock.csv": "Infosys",
    "hdfc_stock.csv": "HDFC"  # New company
}


analyze_multiple_stocks(companies)
