from alpha_vantage.timeseries import TimeSeries
import pandas as pd

# Alpha VantageのAPIを使用して株価データを取得

def get_stock_data(symbol: str, api_key: str) -> pd.DataFrame:
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
    return data.sort_index(ascending=True)
