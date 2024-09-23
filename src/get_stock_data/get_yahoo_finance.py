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

def get_stock_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    return yf.download(symbol, start=start, end=end)

def plot_stock_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    fig = plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(len(symbol), 1, figure=fig)
    all_data = pd.DataFrame()
# TODO
# plot_stock_dataを呼ぶかget_stock_dataを呼ぶか決めて修正数r
# ここで銘柄をリストで渡して繰り返し処理するのではなく、メイン関数で渡して銘柄別の集計がわかるようにする
    # for i, symbol in enumerate(symbols):
    data = get_stock_data(symbol, start, end)
    data['Symbol'] = symbol  # シンボル列を追加
    all_data = pd.concat([all_data, data])
    # ap = mpf.make_addplot(data['Close'].rolling(window=5).mean())  # 5日移動平均
    # mpf.plot(data, type='candle', addplot=ap, title=f'{symbol} Close Price with Moving Averages')

    # plt.tight_layout()
    # plt.show()
    return all_data

def get_yfinance_stock_data(symbol) -> pd.DataFrame:
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*10)
    KabuData = plot_stock_data(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    return KabuData.sort_index(ascending=True)

if __name__ == '__main__':
    get_yfinance_stock_data()
