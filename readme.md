alpha_vantage ライブラリのインストール

```
pip install alpha_vantage
```

Welcome to Alpha Vantage! Your API key is:

- B48ULYVXV9EYZ0M1

. Please record this API key at a safe place for future data access.

```
from alpha_vantage.timeseries import TimeSeries

# あなたのAPIキーを設定します
api_key = 'YOUR_API_KEY'

ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT', interval='1min', outputsize='full')

print(data)
```

このコードは、Microsoft の株価データを 1 分間隔で取得します。get_intraday メソッドのパラメータを変更することで、異なる銘柄、時間間隔、またはデータ量のデータを取得することができます。

以下のコマンドを使用して pandas ライブラリをインストールしてください：

```
pip install pandas
```

Python の実行

```
.\kabu.py
```

```
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries

# あなたのAPIキーを設定します
api_key = 'YOUR_API_KEY'

ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_daily(symbol='MSFT', outputsize='full')

# 移動平均線を計算します
data['5_day_sma'] = data['4. close'].rolling(window=5).mean()
data['20_day_sma'] = data['4. close'].rolling(window=20).mean()
data['40_day_sma'] = data['4. close'].rolling(window=40).mean()

# グラフを描画します
plt.figure(figsize=(12,6))
plt.plot(data['4. close'], label='Close Price')
plt.plot(data['5_day_sma'], label='5 Day SMA')
plt.plot(data['20_day_sma'], label='20 Day SMA')
plt.plot(data['40_day_sma'], label='40 Day SMA')
plt.title('Microsoft Close Price with Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
```
