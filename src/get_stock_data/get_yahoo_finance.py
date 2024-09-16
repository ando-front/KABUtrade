import os
from dotenv import load_dotenv
import pandas as pd
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

def plot_stock_data(symbols: List[str], start: str, end: str) -> yf.download:
    fig = plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(len(symbols), 1, figure=fig)
    all_data = pd.DataFrame()

# TODO
# plot_stock_dataを呼ぶかget_stock_dataを呼ぶか決めて修正数r
# ここで銘柄をリストで渡して繰り返し処理するのではなく、メイン関数で渡して銘柄別の集計がわかるようにする
    for i, symbol in enumerate(symbols):
        data = get_stock_data(symbol, start, end)
        all_data = pd.concat([all_data, data], keys=[symbol], names=['Symbol'])
        # ap = mpf.make_addplot(data['Close'].rolling(window=5).mean())  # 5日移動平均
        # mpf.plot(data, type='candle', addplot=ap, title=f'{symbol} Close Price with Moving Averages')

    # plt.tight_layout()
    # plt.show()
    return all_data

def get_yfinance_stock_data() -> pd.DataFrame:
    # api_key = load_api_key()
    # symbols = ["7203.T"]  # 例：トヨタ自動車、ソフトバンク、ソニー
    symbols = ["^N225","7203.T","7011.T","5401.T","8306.T"]
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*10)
    KabuData = plot_stock_data(symbols, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    # KabuData = get_stock_data(symbols, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    return KabuData.sort_index(ascending=True)

if __name__ == '__main__':
    get_yfinance_stock_data()
