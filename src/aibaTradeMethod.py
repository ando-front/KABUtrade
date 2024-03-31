from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# import logging
# import http.client

# HTTP接続の詳細をログに記録する
# http.client.HTTPConnection.debuglevel = 1

# ロギングの設定
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


# Constants
SMA_PERIODS = [5, 20, 25, 30, 60, 75, 100, 200]
UP_DOWN_PERIODS = [9, 13]
CROSS_PERIODS = [25, 75]


# Alpha VantageのAPIを使用して株価データを取得し、
# 移動平均線のゴールデンクロスとデッドクロスを売買のシグナルとするPythonコードは以下の通りです。
# ただし、Alpha VantageのAPIを使用するにはAPIキーが必要です。

# Alpha VantageのAPIキーを設定
load_dotenv()

api_key = os.getenv("API_KEY")

# データ取得
ts = TimeSeries(key=api_key, output_format='pandas')
kabuData, meta_data = ts.get_daily(symbol='SPY', outputsize='full')
# kabuData, meta_data = ts.get_daily(symbol='AAPL', outputsize='full')
kabuData = kabuData.sort_index(ascending=True)


# 移動平均線の計算
for period in SMA_PERIODS:
    kabuData[f'SMA_{period}'] = kabuData['4. close'].rolling(window=period).mean()

# 陽線と陰線の判定
kabuData['Up'] = kabuData['4. close'] > kabuData['1. open']
kabuData['Down'] = kabuData['4. close'] < kabuData['1. open']

# シグナルの生成
def calculate_signals(kabuData, UP_DOWN_PERIODS, SMA_PERIODS, CROSS_PERIODS):
    # 買いシグナル：日足が75日線を下から上に抜けて陽線で終わる、または陰線が9日間または13日間連続する
    # 売りシグナル：日足が75日線を上から下に抜けて陰線で終わる、または陽線が9日間または13日間連続する
    for period in UP_DOWN_PERIODS:
        kabuData[f'Buy_Signal_{period}'] = (kabuData['Down'].rolling(window=period).sum() == period)
        kabuData[f'Sell_Signal_{period}'] = (kabuData['Up'].rolling(window=period).sum() == period)

    # パンパカパンと売りシグナルの生成
    # 買いシグナル（パンパカパン）：移動平均線が5, 20, 60, 100, 200, 30日の順番で高い
    # 売りシグナル：移動平均線が5, 20, 60, 100, 200, 30日の順番で安い
    kabuData['Buy_Signal_MA'] = kabuData.apply(lambda row: all(row[f'SMA_{SMA_PERIODS[i]}'] > row[f'SMA_{SMA_PERIODS[i+1]}'] for i in range(len(SMA_PERIODS)-1)), axis=1)
    kabuData['Sell_Signal_MA'] = kabuData.apply(lambda row: all(row[f'SMA_{SMA_PERIODS[i]}'] < row[f'SMA_{SMA_PERIODS[i+1]}'] for i in range(len(SMA_PERIODS)-1)), axis=1)

    # ゴールデンクロスとデッドクロスのシグナル生成
    kabuData['Buy_Signal_golden_cross'] = (kabuData[f'SMA_{CROSS_PERIODS[0]}'] > kabuData[f'SMA_{CROSS_PERIODS[1]}']) & (kabuData[f'SMA_{CROSS_PERIODS[0]}'].shift(1) < kabuData[f'SMA_{CROSS_PERIODS[1]}'].shift(1))
    kabuData['Sell_Signal_dead_cross'] = (kabuData[f'SMA_{CROSS_PERIODS[0]}'] < kabuData[f'SMA_{CROSS_PERIODS[1]}']) & (kabuData[f'SMA_{CROSS_PERIODS[0]}'].shift(1) > kabuData[f'SMA_{CROSS_PERIODS[1]}'].shift(1))

    return kabuData


# 最新の日付でのシグナルを出力
# 最新のデータがゴールデンクロスかデッドクロスのシグナルを持っているかチェック
# ゴールデンクロスもデッドクロスもない場合、連続上昇日数または連続下落日数に基づくシグナル、移動平均に基づくシグナルをチェックします。
# チェックの結果として、シグナルを返却します
def get_latest_signals(kabuData):
    latest_data = kabuData.iloc[-1]
    signal_type = None
    signal_kind = None

    if latest_data['Buy_Signal_golden_cross']:
        signal_type = 'Buy'
        signal_kind = 'Golden Cross'
    elif latest_data['Sell_Signal_dead_cross']:
        signal_type = 'Sell'
        signal_kind = 'Dead Cross'
    else:
        for period in UP_DOWN_PERIODS:
            if latest_data[f'Buy_Signal_{period}']:
                signal_type = 'Buy'
                signal_kind = f'Up for {period} days'
            elif latest_data[f'Sell_Signal_{period}']:
                signal_type = 'Sell'
                signal_kind = f'Down for {period} days'
        if signal_type is None:
            if latest_data['Buy_Signal_MA']:
                signal_type = 'Buy'
                signal_kind = 'Moving Average'
            elif latest_data['Sell_Signal_MA']:
                signal_type = 'Sell'
                signal_kind = 'Moving Average'

    return signal_type, signal_kind


# データのプロット
def create_graph(calculated_data):
    plt.figure(figsize=(12,5))
    colors = ['blue', 'red', 'green', 'violet', 'indigo', 'orange', 'black']
    for period, color in zip(SMA_PERIODS, colors):
        plt.plot(kabuData.index, kabuData[f'SMA_{period}'], label=f'{period} Day SMA', color=color)

    plt.plot(kabuData[kabuData['Buy_Signal_golden_cross']].index, kabuData['SMA_5'][kabuData['Buy_Signal_golden_cross']], '^', markersize=10, color='m', label='buy signal')
    plt.plot(kabuData[kabuData['Sell_Signal_dead_cross']].index, kabuData['SMA_5'][kabuData['Sell_Signal_dead_cross']], 'v', markersize=10, color='k', label='sell signal')

    plt.title('Apple Close Price with Moving Averages and Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.show()

# 注文実行
# このサンプルコードでは、実際の売買注文は行わず、シグナルの生成だけを行います。

def main():
    calculated_kabu_data = calculate_signals(kabuData, UP_DOWN_PERIODS, SMA_PERIODS, CROSS_PERIODS)
    # get_latest_signals関数を呼び出し、結果をsignalTypeとsignalKindに割り当てる
    signalType, signalKind = get_latest_signals(calculated_kabu_data)
    print(f"買いor売りシグナルSignal Typeの結果: {signalType}")
    print(f"移動平均線のシグナルタイプSignal Kindの結果: {signalKind}")
#　データプロット関数を実行すると処理が止まるので、コメントアウトしています
    # create_graph(calculated_kabu_data)
    return signalType, signalKind
