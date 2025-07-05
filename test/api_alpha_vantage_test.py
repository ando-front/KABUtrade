import os
from alpha_vantage.timeseries import TimeSeries
import pandas as pd

# Alpha Vantage APIキーを設定
api_key = os.getenv("API_KEY")  # ご自身のAPIキーをここに設定

symbol = 'SOXL'

def test_alpha_vantage_connection(symbol, api_key):
    ts = TimeSeries(key=api_key, output_format='pandas')

    try:
        # 日次の株価データを取得
        data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')

        # データが空でないことを確認
        if data.empty:
            print(f"[ERROR] No data returned for {symbol}")
        else:
            print(f"[INFO] Successfully fetched data for {symbol}")
            print(data.head())  # 先頭の数行を表示

    except Exception as e:
        print(f"[ERROR] Failed to fetch data for {symbol}: {e}")

# 実行
test_alpha_vantage_connection(symbol, api_key)
