import os
from dotenv import load_dotenv
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import mplfinance as mpf
from typing import List
from datetime import datetime, timedelta

def load_api_key() -> str:
    load_dotenv()
    return os.getenv("API_KEY")

def get_stock_data(symbol: str, start: str, end: str) -> yf.download:
    return yf.download(symbol, start=start, end=end)

def plot_stock_data(symbols: List[str], start: str, end: str) -> None:
    fig = plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(len(symbols), 1, figure=fig)

    for i, symbol in enumerate(symbols):
        data = get_stock_data(symbol, start, end)
        ap = mpf.make_addplot(data['Close'].rolling(window=5).mean())  # 5日移動平均
        mpf.plot(data, type='candle', addplot=ap, title=f'{symbol} Close Price with Moving Averages')

    plt.tight_layout()
    plt.show()

def get_yfinance_stock_data() -> None:
    api_key = load_api_key()
    # symbols = ["7203.T"]  # 例：トヨタ自動車、ソフトバンク、ソニー
    symbols = ["^N225"]
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*10)
    plot_stock_data(symbols, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

if __name__ == '__main__':
    get_yfinance_stock_data()
