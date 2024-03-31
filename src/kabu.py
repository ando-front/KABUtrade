from alpha_vantage.timeseries import TimeSeries
from datetime import datetime, timedelta
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import mplfinance as mpf
import os

load_dotenv()

api_key = os.getenv("API_KEY")

ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_daily(symbol='MSFT', outputsize='full')

# カラム名を変更します
data.rename(columns={
    '1. open': 'Open',
    '2. high': 'High',
    '3. low': 'Low',
    '4. close': 'Close',
    '5. volume': 'Volume'
}, inplace=True)

# 移動平均線を計算します
sma_periods = [5, 20, 60, 100, 200, 300]
for period in sma_periods:
    data[f'{period}_day_sma'] = data['Close'].rolling(window=period).mean()

# 現在の日付から2年前の日付を計算します
two_years_ago = datetime.now() - timedelta(days=2*365)

# 過去2年分のデータをフィルタリングします
data = data[data.index >= two_years_ago]

# 移動平均線のデータを作成します
apdict = [mpf.make_addplot(data[f'{period}_day_sma']) for period in [5, 20, 60, 100, 200, 300]]

# グラフを描画します
mpf.plot(data, type='candle', addplot=apdict, volume=True, title='Microsoft Close Price with Moving Averages', ylabel='Price ($)')