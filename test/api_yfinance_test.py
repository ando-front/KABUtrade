import yfinance as yf

tickers = ["9984.T", "6758.T", "8306.T"]  # ソフトバンクG, ソニー, 三菱UFJ
for t in tickers:
    stock = yf.Ticker(t)
    data = stock.history(period="1d")
    print(f"{t} -> data found: {not data.empty}")

ticker = "AAPL"  # Apple Inc
stock = yf.Ticker(ticker)
data = stock.history(period="1d")
print(data)