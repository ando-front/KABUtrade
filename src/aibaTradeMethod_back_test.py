import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv
import os

# このコードは、初期資金を設定し、買いシグナルが出たときに全ての資金を使って株を買い、売りシグナルが出たときに全ての株を売るというシンプルな戦略を採用しています。バックテストの結果は、初期資金と最終的なポートフォリオの価値として出力されます。
# ただし、このコードは非常にシンプルなものであり、実際のトレーディングでは、リスク管理のルール、手数料、スリッページ（注文価格と実際の取引価格との差）などを考慮する必要があります。また、バックテストの結果は過去のデータに基づいているため、未来のパフォーマンスを保証するものではありません。

# Alpha VantageのAPIキーを設定
load_dotenv()

api_key = os.getenv("API_KEY")
SYMBOL = 'SPY'
# SYMBOL = 'AAPL'

# データ取得
ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_daily(symbol=SYMBOL, outputsize='full')

# データを降順にソート
data = data.sort_index(ascending=True)

# 移動平均線の計算
data['SMA_75'] = data['4. close'].rolling(window=75).mean()

# 陽線と陰線の判定
data['Up'] = data['4. close'] > data['1. open']
data['Down'] = data['4. close'] < data['1. open']

# シグナルの生成
# Buy_Signal：以下のいずれかの条件が満たされた場合にTrueとなります。
# 現在の終値が75日移動平均（SMA_75）より高く、前日の終値が75日移動平均より低い（つまり、価格が75日移動平均を上回る）場合、かつUpがTrueである。
# 過去9日間にDownがすべてTrue（つまり、9日連続で価格が下落）。
# 過去13日間にDownがすべてTrue（つまり、13日連続で価格が下落）。
# Sell_Signal：以下のいずれかの条件が満たされた場合にTrueとなります。
# 現在の終値が75日移動平均（SMA_75）より低く、前日の終値が75日移動平均より高い（つまり、価格が75日移動平均を下回る）場合、かつDownがTrueである。
# 過去9日間にUpがすべてTrue（つまり、9日連続で価格が上昇）。
# 過去13日間にUpがすべてTrue（つまり、13日連続で価格が上昇）。
data['Buy_Signal'] = ((data['4. close'] > data['SMA_75']) & (data['4. close'].shift(1) < data['SMA_75'].shift(1)) & data['Up']) | (data['Down'].rolling(window=9).sum() == 9) | (data['Down'].rolling(window=13).sum() == 13)
data['Sell_Signal'] = ((data['4. close'] < data['SMA_75']) & (data['4. close'].shift(1) > data['SMA_75'].shift(1)) & data['Down']) | (data['Up'].rolling(window=9).sum() == 9) | (data['Up'].rolling(window=13).sum() == 13)

# バックテスト
initial_balance = 1000000  # 初期資金
balance = initial_balance
shares = 0

for i in range(len(data)):
    # 買いシグナル
    if data['Buy_Signal'].iloc[i] and balance > 0:
        shares = balance / data['4. close'].iloc[i]
        balance = 0
        print(f"Buying on {data.index[i]} at {data['4. close'].iloc[i]}")
    # 売りシグナル
    elif data['Sell_Signal'].iloc[i] and shares > 0:
        balance = shares * data['4. close'].iloc[i]
        shares = 0
        print(f"Selling on {data.index[i]} at {data['4. close'].iloc[i]}")

# 最終的なポートフォリオの価値を計算
final_portfolio = balance + shares * data['4. close'].iloc[-1]
print(f"Initial balance: {initial_balance}, Final portfolio: {final_portfolio}")