from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

import logging
# import http.client

# HTTP接続の詳細をログに記録する
# http.client.HTTPConnection.debuglevel = 1

# ロギングの設定
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# Alpha VantageのAPIキーを設定
load_dotenv()
api_key = os.getenv("API_KEY")

# Constants
# SMA_PERIODS = [5, 10, 20, 25, 30, 60, 75, 100, 200, 300]
# UP_DOWN_PERIODS = [9, 13]
# CROSS_PERIODS = [25, 75]


# Alpha VantageのAPIを使用して株価データを取得し、
# 移動平均線のゴールデンクロスとデッドクロスを売買のシグナルとするPythonコードは以下の通りです。
# ただし、Alpha VantageのAPIを使用するにはAPIキーが必要です。

def get_stock_data(symbol, api_key):
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
    return data.sort_index(ascending=True)

# 移動平均線の計算(5, 10, 20, 25, 30, 60, 75, 100, 200, 300)
def calculate_sma(data, periods):
    for period in periods:
        data[f'SMA_{period}'] = data['4. close'].rolling(window=period).mean()
    return data


# 前提条件の追加
# 上昇トレンドが3か月間継続する場合のみ、売買シグナルの判定を行う
def is_up_trend(row, prev_row):
    """上昇トレンドかどうかを判定する"""
    if row['SMA_5'] < row['SMA_20'] and row['SMA_5'] < row['4. close']:
        return True
    if row['SMA_20'] < row['SMA_5'] and row['SMA_20'] < row['4. close'] and row['SMA_20'] > prev_row['SMA_20']:
        return True
    if row['SMA_60'] < row['SMA_5'] and row['SMA_60'] < row['4. close'] and row['SMA_20'] > prev_row['SMA_20'] and row['SMA_60'] > prev_row['SMA_60']:
        return True
    return False

def is_down_trend(row, prev_row):
    """下降トレンドかどうかを判定する"""
    if row['SMA_20'] < row['SMA_5'] and row['4. close'] < row['SMA_5']:
        return True
    if row['SMA_5'] < row['SMA_20'] and row['SMA_20'] < prev_row['SMA_20'] and row['4. close'] < row['SMA_20']:
        return True
    if row['SMA_5'] < row['SMA_60'] and row['SMA_20'] < prev_row['SMA_20'] and row['SMA_60'] < prev_row['SMA_60'] and row['4. close'] < row['SMA_60']:
        return True
    return False

def calculate_trend_counts(data, trend_func):
    """トレンドのカウントを計算する"""
    trend_count = [0] * len(data)
    for i in range(1, len(data)):
        if trend_func(data.iloc[i], data.iloc[i-1]):
            trend_count[i] = trend_count[i-1] + 1
        else:
            trend_count[i] = 0
    return trend_count


# データ準備
def prepare_data(up_down_periods, sma_periods, cross_periods):
    # 株価データ取得 
    stock_data = get_stock_data('SPY', api_key)
    # 上昇トレンドのカウントと判定
    stock_data['up_trend_count'] = calculate_trend_counts(stock_data, is_up_trend)
    stock_data['is_up_trend'] = stock_data['up_trend_count'] >= 60
    # 下降トレンドのカウントと判定
    stock_data['down_trend_count'] = calculate_trend_counts(stock_data, is_down_trend)
    stock_data['is_down_trend'] = stock_data['down_trend_count'] >= 60
    # 陽線と陰線の判定
    stock_data['Down'] = stock_data['4. close'] < stock_data['1. open']
    stock_data['Up'] = stock_data['4. close'] > stock_data['1. open']
    return stock_data

# シグナル生成
def generate_continuous_signal(data, periods, condition, signal_name):
    """連続した条件に基づくシグナルを生成する"""
    for period in periods:
        data[f'{signal_name}_{period}'] = condition(data, period)
    return data

def down_signal_condition(data, period):
    """陰線の連続条件を判定する"""
    return (data['Down'].rolling(window=period).sum() == period) | (
        (data['4. close'] > data['SMA_75']) & 
        (data['4. close'].shift(1) < data['SMA_75'].shift(1)) & 
        data['Up']
    )

def up_signal_condition(data, period):
    """陽線の連続条件を判定する"""
    return (data['Up'].rolling(window=period).sum() == period) | (
        (data['4. close'] < data['SMA_75']) & 
        (data['4. close'].shift(1) > data['SMA_75'].shift(1)) & 
        data['Down']
    )

def generate_ma_signal(data, periods, signal_name, comparison_func):
    """移動平均線の順序に基づくシグナルを生成する"""
    data[signal_name] = data.apply(
        lambda row: all(comparison_func(row[f'SMA_{periods[i]}'], row[f'SMA_{periods[i+1]}']) for i in range(len(periods) - 1)),
        axis=1
    )
    return data

def cross_signal(data, short_period, long_period, signal_name, comparison_func):
    """ゴールデンクロス/デッドクロスのシグナルを生成する"""
    data[signal_name] = (
        comparison_func(data[f'SMA_{short_period}'], data[f'SMA_{long_period}']) &
        comparison_func(data[f'SMA_{short_period}'].shift(1), data[f'SMA_{long_period}'].shift(1)).shift(-1)
    )
    return data

def lower_half_signal(data):
    """下半身（買いシグナル）を生成する"""
    data['5d_trend'] = data['SMA_5'].diff() > 0
    data['below_5d'] = data['4. close'] < data['SMA_5']
    data['break_5d'] = (
        (data['4. close'] > data['SMA_5']) & 
        (data['4. close'] - data['1. open'] > (data['4. close'] - data['SMA_5']) / 2)
    )
    data['buy_signal_lower_half'] = (
        data['5d_trend'] & data['below_5d'].shift() & data['Up'] & data['break_5d']
    )
    return data

def reverse_lower_half_signal(data):
    """逆下半身（売りシグナル）を生成する"""
    data['5d_down_trend'] = data['SMA_5'].diff() < 0
    data['above_5d'] = data['4. close'] > data['SMA_5']
    data['break_down_5d'] = (
        (data['4. close'] < data['SMA_5']) & 
        (data['1. open'] - data['4. close'] > (data['SMA_5'] - data['4. close']) / 2)
    )
    data['sell_signal_reverse_lower_half'] = (
        data['5d_down_trend'] & data['above_5d'].shift() & data['Down'] & data['break_down_5d']
    )
    return data

def bird_beak_signal(data):
    """くちばし（買いシグナル）を生成する"""
    data['5d_up_trend'] = data['SMA_5'].diff() > 0
    data['10d_up_trend'] = data['SMA_10'].diff() > 0
    data['5d_below_10d'] = data['SMA_5'] < data['SMA_10']
    data['5d_breaks_10d'] = data['SMA_5'] > data['SMA_10']
    data['buy_signal_bird_beak'] = (
        data['5d_up_trend'] & data['10d_up_trend'] & data['5d_below_10d'].shift() & data['5d_breaks_10d']
    )
    return data

def reverse_bird_beak_signal(data):
    """逆くちばし（売りシグナル）を生成する"""
    data['5d_down_trend'] = data['SMA_5'].diff() < 0
    data['10d_down_trend'] = data['SMA_10'].diff() < 0
    data['5d_above_10d'] = data['SMA_5'] > data['SMA_10']
    data['5d_breaks_down_10d'] = data['SMA_5'] < data['SMA_10']
    data['sell_signal_reverse_bird_beak'] = (
        data['5d_down_trend'] & data['10d_down_trend'] & data['5d_above_10d'].shift() & data['5d_breaks_down_10d']
    )
    return data

def calculate_signals(stock_data, up_down_periods, sma_periods, cross_periods):
    """各種シグナルを生成するメイン関数"""
    # 移動平均線の計算
    stock_data = calculate_sma(stock_data, sma_periods)

    # 買い/売りシグナル（連続陰線・陽線）
    # 買いシグナル：陰線が9日間または13日間連続する、または日足が75日線を下から上に抜けて陽線で終わる
    # 売りシグナル：陽線が9日間または13日間連続する、または日足が75日線を上から下に抜けて陰線で終わる
    stock_data = generate_continuous_signal(stock_data, up_down_periods, down_signal_condition, 'Buy_Signal')
    stock_data = generate_continuous_signal(stock_data, up_down_periods, up_signal_condition, 'Sell_Signal')
    
    # パンパカパンシグナル
    # 買いシグナル（パンパカパン）：移動平均線が5, 20, 60, 100, 200, 300日の順番で高い
    # 売りシグナル：移動平均線が5, 20, 60, 100, 200, 300日の順番で安い
    stock_data = generate_ma_signal(stock_data, sma_periods, 'Buy_Signal_MA_PPP', lambda x, y: x > y)
    stock_data = generate_ma_signal(stock_data, sma_periods, 'Sell_Signal_MA_reverse_PPP', lambda x, y: x < y)
    
    # ゴールデンクロス/デッドクロスシグナル
    stock_data = cross_signal(stock_data, cross_periods[0], cross_periods[1], 'Buy_Signal_golden_cross', lambda x, y: x > y)
    stock_data = cross_signal(stock_data, cross_periods[0], cross_periods[1], 'Sell_Signal_dead_cross', lambda x, y: x < y)
    
    # 下半身/逆下半身シグナル
    # 5日線が上昇トレンドで、前日の日足線が5日線より下にあり、かつ、当日の日足線が陽線で5日線を実体の半分以上突き抜けていれば、買いシグナルとします。
    # 5日線の上昇トレンドを判定します。5日線の差分が正（つまり、前日よりも上昇している）であれば、上昇トレンドと判定します。
    # 日足線が5日線より下にあるか判定します。終値が5日線よりも低ければ、その日の日足線は5日線より下にあると判定します。
    # 陽線かつ5日線を実体の半分以上突き抜けたか判定します。終値が5日線よりも高く、かつ、終値と始値の差（実体）が5日線を突き抜けた部分（終値と5日線との差）の半分以上であれば、5日線を実体の半分以上突き抜けたと判定します。
    stock_data = lower_half_signal(stock_data)
    stock_data = reverse_lower_half_signal(stock_data)
    
    # くちばし/逆くちばしシグナル
    # 5日線と10日線が上昇トレンドで、前日の5日線が10日線より下にあり、かつ、当日の5日線が10日線を上抜けていれば、買いシグナルとします。
    # 5日線と10日線の上昇トレンドを判定します。5日線と10日線の差分が正（つまり、前日よりも上昇している）であれば、上昇トレンドと判定します。
    # 5日線が10日線より下にあるか判定します。5日線が10日線よりも低ければ、その日の5日線は10日線より下にあると判定します。
    # 5日線が10日線を上抜けたか判定します。5日線が10日線よりも高ければ、5日線は10日線を上抜けたと判定します。
    stock_data = bird_beak_signal(stock_data)
    stock_data = reverse_bird_beak_signal(stock_data)
    
    return stock_data


# 最新のデータがゴールデンクロスかデッドクロスのシグナルを持っているかチェック
# ゴールデンクロスもデッドクロスもない場合、連続上昇日数または連続下落日数に基づくシグナル、移動平均に基づくシグナルをチェックします。
def check_signal(latest_data, signal_name, trend_name, trend_condition):
    """シグナルとトレンドの組み合わせをチェックし、該当する場合はシグナルを返す"""
    if latest_data[signal_name] and latest_data[trend_condition]:
        signal_type = 'Buy' if 'Buy' in signal_name else 'Sell'
        print(f'{signal_type} Signal: {trend_name}')
        return signal_type, trend_name
    return None, None

def check_cross_signals(latest_data):
    """ゴールデンクロスとデッドクロスのシグナルをチェックする"""
    return (
        check_signal(latest_data, 'Buy_Signal_golden_cross', 'Golden Cross', 'is_up_trend') or
        check_signal(latest_data, 'Sell_Signal_dead_cross', 'Dead Cross', 'is_down_trend')
    )

def check_up_down_signals(latest_data, periods):
    """連続上昇・下降日数に基づくシグナルをチェックする"""
    for period in periods:
        result = check_signal(latest_data, f'Buy_Signal_{period}', f'Up for {period} days', 'is_up_trend')
        if result[0]:  # Buy Signal found
            return result
        
        result = check_signal(latest_data, f'Sell_Signal_{period}', f'Down for {period} days', 'is_down_trend')
        if result[0]:  # Sell Signal found
            return result
            
    return None, None

def check_other_signals(latest_data):
    """その他のシグナルをチェックする"""
    return (
        check_signal(latest_data, 'Buy_Signal_MA_PPP', 'PPP', 'is_up_trend') or
        check_signal(latest_data, 'Sell_Signal_MA_reverse_PPP', 'Reverse PPP', 'is_down_trend') or
        check_signal(latest_data, 'buy_signal_lower_harf', 'Lower Half', 'is_up_trend') or
        check_signal(latest_data, 'sell_signal_Reverse_lower_half', 'Reverse Lower Half', 'is_down_trend') or
        check_signal(latest_data, 'buy_signal_bird_beak', 'Bird Beak', 'is_up_trend') or
        check_signal(latest_data, 'sell_signal_reverse_bird_beak', 'Reverse Bird Beak', 'is_down_trend')
    )

def get_latest_signals(stock_data, up_down_periods):
    """最新の日付でのシグナルを出力する"""
    latest_data = stock_data.iloc[-1]
    signal_type, signal_kind = check_cross_signals(latest_data)
    if signal_type is None:
        signal_type, signal_kind = check_up_down_signals(latest_data, up_down_periods)
    if signal_type is None:
        signal_type, signal_kind = check_other_signals(latest_data)
    return signal_type, signal_kind



# データのプロット
def plot_moving_averages(calculated_data, sma_periods, colors):
    """移動平均線をプロットする"""
    for period, color in zip(sma_periods, colors):
        plt.plot(
            calculated_data.index, 
            calculated_data[f'SMA_{period}'], 
            label=f'{period} Day SMA', 
            color=color
        )

def plot_signals(calculated_data):
    """ゴールデンクロスとデッドクロスのシグナルをプロットする"""
    plt.plot(
        calculated_data[calculated_data['Buy_Signal_golden_cross']].index, 
        calculated_data['SMA_5'][calculated_data['Buy_Signal_golden_cross']], 
        '^', 
        markersize=10, 
        color='m', 
        label='Buy Signal'
    )
    plt.plot(
        calculated_data[calculated_data['Sell_Signal_dead_cross']].index, 
        calculated_data['SMA_5'][calculated_data['Sell_Signal_dead_cross']], 
        'v', 
        markersize=10, 
        color='k', 
        label='Sell Signal'
    )

def create_graph(calculated_data, sma_periods=None, colors=None):
    """グラフを作成し、移動平均線とシグナルをプロットする"""
    if sma_periods is None:
        sma_periods = [5, 20, 60, 100, 200, 300]
    if colors is None:
        colors = ['blue', 'red', 'green', 'violet', 'indigo', 'orange', 'black']
    
    plt.figure(figsize=(12, 5))
    
    plot_moving_averages(calculated_data, sma_periods, colors)
    plot_signals(calculated_data)
    
    plt.title('Close Price with Moving Averages and Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.show()



# 注文実行
# このサンプルコードでは、実際の売買注文は行わず、シグナルの生成だけを行います。
def main(stock_data, up_down_periods, sma_periods, cross_periods):
    """シグナル計算と結果表示のメイン処理"""
    calculated_data = calculate_signals(stock_data, up_down_periods, sma_periods, cross_periods)
    
    # 最新のシグナルを取得
    signal_type, signal_kind = get_latest_signals(calculated_data, up_down_periods)
    
    # シグナルの結果を表示
    print(f"Signal Type: {signal_type}")
    print(f"Signal Kind: {signal_kind}")
    
    # グラフ作成（コメントアウトされたデータプロット）
    # create_graph(calculated_data, sma_periods=sma_periods)
    
    return signal_type, signal_kind
