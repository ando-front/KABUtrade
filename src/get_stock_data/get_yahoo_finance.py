import os
from dotenv import load_dotenv
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import mplfinance as mpf
from typing import List
from datetime import datetime, timedelta
import time

def load_api_key() -> str:
    load_dotenv()
    return os.getenv("API_KEY")

def get_stock_data(symbol: str, start: str, end: str, retries: int = 3) -> pd.DataFrame:
    for attempt in range(retries):
        try:
            data = yf.download(symbol, start=start, end=end, auto_adjust=True)
            if not data.empty:
                return data
            print(f"Attempt {attempt + 1}: No data for {symbol}. Retrying...")
        except Exception as e:
            print(f"Attempt {attempt + 1}: Failed to get data for {symbol}. Reason: {e}")
        time.sleep(1)  # リトライ間隔
    print(f"Failed to retrieve data for {symbol} after {retries} attempts.")
    return pd.DataFrame()

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

def get_yfinance_stock_data(symbol: str) -> pd.DataFrame:
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * 10)
        # 銘柄コードのフォーマットを確認
        if not symbol.endswith(".T") and symbol.isdigit():
            symbol += ".T"
        KabuData = get_stock_data(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
        if KabuData.empty:
            print(f"Warning: No data retrieved for symbol {symbol}.")
        return KabuData.sort_index(ascending=True)
    except Exception as e:
        print(f"Failed to get ticker '{symbol}' reason: {e}")
        return pd.DataFrame()

if __name__ == '__main__':
    get_yfinance_stock_data()
