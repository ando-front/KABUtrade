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
SMA_PERIODS = [5, 10, 20, 25, 30, 60, 75, 100, 200]
UP_DOWN_PERIODS = [9, 13]
CROSS_PERIODS = [25, 75]


# Alpha VantageのAPIを使用して株価データを取得し、
# 移動平均線のゴールデンクロスとデッドクロスを売買のシグナルとするPythonコードは以下の通りです。
# ただし、Alpha VantageのAPIを使用するにはAPIキーが必要です。

def get_stock_data(symbol, api_key):
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
    return data.sort_index(ascending=True)

# 移動平均線の計算(5, 10, 20, 25, 30, 60, 75, 100, 200)
def calculate_sma(data, periods):
    for period in periods:
        data[f'SMA_{period}'] = data['4. close'].rolling(window=period).mean()
    return data

# Alpha VantageのAPIキーを設定
load_dotenv()
api_key = os.getenv("API_KEY")

# データ取得
kabuData = get_stock_data('SPY', api_key)

# 移動平均線の計算
kabuData = calculate_sma(kabuData, SMA_PERIODS)


# 前提条件の追加
# 上昇トレンドの日数をカウントするための新しい列を追加
kabuData['up_trend_count'] = 0
kabuData = kabuData.reset_index(drop=True)
# 上昇トレンドの日数をカウント
for i in range(2, len(kabuData)):
    # ケースA
    if kabuData.iloc[i]['SMA_5'] < kabuData.iloc[i]['SMA_20'] and kabuData.iloc[i]['SMA_5'] < kabuData.iloc[i]['4. close']:
        kabuData.at[i, 'up_trend_count'] = kabuData.at[i-1, 'up_trend_count'] + 1
    # ケースB
    elif kabuData.iloc[i]['SMA_20'] < kabuData.iloc[i]['SMA_5'] and kabuData.iloc[i]['SMA_20'] < kabuData.iloc[i]['4. close'] and kabuData.iloc[i]['SMA_20'] > kabuData.iloc[i-1]['SMA_20']:
        kabuData.at[i, 'up_trend_count'] = kabuData.at[i-1, 'up_trend_count'] + 1
    # ケースC
    elif kabuData.iloc[i]['SMA_30'] < kabuData.iloc[i]['SMA_5'] and kabuData.iloc[i]['SMA_30'] < kabuData.iloc[i]['4. close'] and kabuData.iloc[i]['SMA_20'] > kabuData.iloc[i-1]['SMA_20'] and kabuData.iloc[i]['SMA_30'] > kabuData.iloc[i-1]['SMA_30']:
        kabuData.at[i, 'up_trend_count'] = kabuData.at[i-1, 'up_trend_count'] + 1
    # 上昇トレンドの例外処理
    elif kabuData.iloc[i]['SMA_30'] < kabuData.iloc[i]['SMA_5'] and kabuData.iloc[i]['SMA_20'] < kabuData.iloc[i-1]['SMA_20'] and kabuData.iloc[i]['SMA_30'] > kabuData.iloc[i-1]['SMA_30'] and kabuData.iloc[i]['4. close'] > kabuData.iloc[i]['SMA_30']:
        continue
    else:
        kabuData.at[i, 'up_trend_count'] = 0
# 上昇トレンドが3か月以上続いているかどうかを判定する新しい列を追加
kabuData['is_up_trend'] = kabuData['up_trend_count'] >= 60

# 下降トレンドの日数をカウントするための新しい列を追加
kabuData['down_trend_count'] = 0
# 下降トレンドの日数をカウント
for i in range(1, len(kabuData)):
    # ケースD
    if kabuData.loc[i, 'SMA_20'] < kabuData.loc[i, 'SMA_5'] and kabuData.loc[i, '4. close'] < kabuData.loc[i, 'SMA_5']:
        kabuData.loc[i, 'down_trend_count'] = kabuData.loc[i-1, 'down_trend_count'] + 1
    # ケースE
    elif kabuData.loc[i, 'SMA_5'] < kabuData.loc[i, 'SMA_20'] and kabuData.loc[i, 'SMA_20'] < kabuData.loc[i-1, 'SMA_20'] and kabuData.loc[i, '4. close'] < kabuData.loc[i, 'SMA_20']:
        kabuData.loc[i, 'down_trend_count'] = kabuData.loc[i-1, 'down_trend_count'] + 1
    # ケースF
    elif kabuData.loc[i, 'SMA_5'] < kabuData.loc[i, 'SMA_30'] and kabuData.loc[i, 'SMA_20'] < kabuData.loc[i-1, 'SMA_20'] and kabuData.loc[i, 'SMA_30'] < kabuData.loc[i-1, 'SMA_30'] and kabuData.loc[i, '4. close'] < kabuData.loc[i, 'SMA_30']:
        kabuData.loc[i, 'down_trend_count'] = kabuData.loc[i-1, 'down_trend_count'] + 1
    # 下降トレンドの例外処理
    elif kabuData.loc[i, 'SMA_5'] < kabuData.loc[i, 'SMA_30'] and kabuData.loc[i, 'SMA_20'] > kabuData.loc[i-1, 'SMA_20'] and kabuData.loc[i, 'SMA_30'] < kabuData.loc[i-1, 'SMA_30'] and kabuData.loc[i, '4. close'] < kabuData.loc[i, 'SMA_30']:
        continue
    else:
        kabuData.loc[i, 'down_trend_count'] = 0
# 下降トレンドが3か月以上続いているかどうかを判定する新しい列を追加
kabuData['is_down_trend'] = kabuData['down_trend_count'] >= 60


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
    kabuData['Buy_Signal_MA_PPP'] = kabuData.apply(lambda row: all(row[f'SMA_{SMA_PERIODS[i]}'] > row[f'SMA_{SMA_PERIODS[i+1]}'] for i in range(len(SMA_PERIODS)-1)), axis=1)
    kabuData['Sell_Signal_MA_reverse_PPP'] = kabuData.apply(lambda row: all(row[f'SMA_{SMA_PERIODS[i]}'] < row[f'SMA_{SMA_PERIODS[i+1]}'] for i in range(len(SMA_PERIODS)-1)), axis=1)

    # ゴールデンクロスとデッドクロスのシグナル生成
    kabuData['Buy_Signal_golden_cross'] = (kabuData[f'SMA_{CROSS_PERIODS[0]}'] > kabuData[f'SMA_{CROSS_PERIODS[1]}']) & (kabuData[f'SMA_{CROSS_PERIODS[0]}'].shift(1) < kabuData[f'SMA_{CROSS_PERIODS[1]}'].shift(1))
    kabuData['Sell_Signal_dead_cross'] = (kabuData[f'SMA_{CROSS_PERIODS[0]}'] < kabuData[f'SMA_{CROSS_PERIODS[1]}']) & (kabuData[f'SMA_{CROSS_PERIODS[0]}'].shift(1) > kabuData[f'SMA_{CROSS_PERIODS[1]}'].shift(1))

    # 下半身：買いシグナルシグナル生成
    # 5日線が上昇トレンドで、前日の日足線が5日線より下にあり、かつ、当日の日足線が陽線で5日線を実体の半分以上突き抜けていれば、買いシグナルとします。
    # 5日線の上昇トレンドを判定します。5日線の差分が正（つまり、前日よりも上昇している）であれば、上昇トレンドと判定します。
    # 日足線が5日線より下にあるか判定します。終値が5日線よりも低ければ、その日の日足線は5日線より下にあると判定します。
    # 陽線かつ5日線を実体の半分以上突き抜けたか判定します。終値が5日線よりも高く、かつ、終値と始値の差（実体）が5日線を突き抜けた部分（終値と5日線との差）の半分以上であれば、5日線を実体の半分以上突き抜けたと判定します。
    # 買いシグナル（下半身）を生成します。
    kabuData['5d_trend'] = kabuData['SMA_5'].diff() > 0
    kabuData['below_5d'] = kabuData['4. close'] < kabuData['SMA_5']
    kabuData['break_5d'] = (kabuData['4. close'] > kabuData['SMA_5']) & (kabuData['4. close'] - kabuData['1. open'] > (kabuData['4. close'] - kabuData['SMA_5']) / 2)
    kabuData['buy_signal_lower_harf'] = kabuData['5d_trend'] & kabuData['below_5d'].shift() & kabuData['Up'] & kabuData['break_5d']

    # 売りシグナル（逆下半身）を生成
    kabuData['5d_down_trend'] = kabuData['SMA_5'].diff() < 0
    kabuData['above_5d'] = kabuData['4. close'] > kabuData['SMA_5'] 
    kabuData['break_down_5d'] = (kabuData['4. close'] < kabuData['SMA_5']) & (kabuData['1. open'] - kabuData['4. close'] > (kabuData['SMA_5'] - kabuData['4. close']) / 2)
    kabuData['sell_signal_Reverse_lower_half'] = kabuData['5d_down_trend'] & kabuData['above_5d'].shift() & kabuData['Down'] & kabuData['break_down_5d']

    # 買いシグナル：くちばし
    # 5日線と10日線が上昇トレンドで、前日の5日線が10日線より下にあり、かつ、当日の5日線が10日線を上抜けていれば、買いシグナルとします。
    # 5日線と10日線の上昇トレンドを判定します。5日線と10日線の差分が正（つまり、前日よりも上昇している）であれば、上昇トレンドと判定します。
    # 5日線が10日線より下にあるか判定します。5日線が10日線よりも低ければ、その日の5日線は10日線より下にあると判定します。
    # 5日線が10日線を上抜けたか判定します。5日線が10日線よりも高ければ、5日線は10日線を上抜けたと判定します。
    kabuData['5d_up_trend'] = kabuData['SMA_5'].diff() > 0
    kabuData['10d_up_trend'] = kabuData['SMA_10'].diff() > 0
    kabuData['5d_below_10d'] = kabuData['SMA_5'] < kabuData['SMA_10']
    kabuData['5d_breaks_10d'] = kabuData['SMA_5'] > kabuData['SMA_10']
    kabuData['buy_signal_bird_beak'] = kabuData['5d_up_trend'] & kabuData['10d_up_trend'] & kabuData['5d_below_10d'].shift() & kabuData['5d_breaks_10d']

    # 売りシグナル：逆くちばし
    kabuData['5d_down_trend'] = kabuData['SMA_5'].diff() < 0
    kabuData['10d_down_trend'] = kabuData['SMA_10'].diff() < 0
    kabuData['5d_above_10d'] = kabuData['SMA_5'] > kabuData['SMA_10']
    kabuData['5d_breaks_down_10d'] = kabuData['SMA_5'] < kabuData['SMA_10']
    kabuData['sell_signal_reverse_bird_beak'] = kabuData['5d_down_trend'] & kabuData['10d_down_trend'] & kabuData['5d_above_10d'].shift() & kabuData['5d_breaks_down_10d']

    return kabuData


# 最新の日付でのシグナルを出力
# 最新のデータがゴールデンクロスかデッドクロスのシグナルを持っているかチェック
# ゴールデンクロスもデッドクロスもない場合、連続上昇日数または連続下落日数に基づくシグナル、移動平均に基づくシグナルをチェックします。
# チェックの結果として、シグナルを返却します
def get_latest_signals(kabuData):
    latest_data = kabuData.iloc[-1]
    signal_type = None
    signal_kind = None

    if latest_data['Buy_Signal_golden_cross'] and latest_data['is_up_trend']:
        signal_type = 'Buy'
        signal_kind = 'Golden Cross'
    elif latest_data['Sell_Signal_dead_cross'] and latest_data['is_down_trend']:
        signal_type = 'Sell'
        signal_kind = 'Dead Cross'
    else:
        for period in UP_DOWN_PERIODS:
            if latest_data[f'Buy_Signal_{period}'] and latest_data['is_up_trend']:
                signal_type = 'Buy'
                signal_kind = f'Up for {period} days'
            elif latest_data[f'Sell_Signal_{period}'] and latest_data['is_down_trend']:
                signal_type = 'Sell'
                signal_kind = f'Down for {period} days'
        if signal_type is None:
            if latest_data['Buy_Signal_MA_PPP'] and latest_data['is_up_trend']:
                signal_type = 'Buy'
                signal_kind = 'PPP'
            elif latest_data['Sell_Signal_MA_reverse_PPP'] and latest_data['is_down_trend']:
                signal_type = 'Sell'
                signal_kind = 'Reverse PPP'
            elif latest_data['buy_signal_lower_harf'] and latest_data['is_up_trend']:
                signal_type = 'Buy'
                signal_kind = 'Lower Half'
            elif latest_data['sell_signal_Reverse_lower_half'] and latest_data['is_down_trend']:
                signal_type = 'Sell'
                signal_kind = 'Reverse Lower Half'
            elif latest_data['buy_signal_bird_beak'] and latest_data['is_up_trend']:
                signal_type = 'Buy'
                signal_kind = 'Bird Beak'
            elif latest_data['sell_signal_reverse_bird_beak'] and latest_data['is_down_trend']:
                signal_type = 'Sell'
                signal_kind = 'Reverse Bird Beak'

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
