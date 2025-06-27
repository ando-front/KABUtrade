from typing import List, Optional, Tuple
import matplotlib.pyplot as plt

import logging

import pandas as pd

from calculaters.signals import calculate_signals
from calculaters.trends import count_trend_days

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
SMA_PERIODS: List[int] = [5, 10, 20, 25, 30, 60, 75, 100, 200, 300]
UP_DOWN_PERIODS: List[int] = [9, 13]
CROSS_PERIODS: List[int] = [25, 75]



# 移動平均線の計算(5, 10, 20, 25, 30, 60, 75, 100, 200)
def calculate_sma(data: pd.DataFrame, periods: List[int]) -> pd.DataFrame:
    for period in periods:
        data[f'SMA_{period}'] = data['4. close'].rolling(window=period).mean()
    return data


# 最新のデータがゴールデンクロスかデッドクロスのシグナルを持っているかチェック
# ゴールデンクロスもデッドクロスもない場合、連続上昇日数または連続下落日数に基づくシグナル、移動平均に基づくシグナルをチェックします。
# チェックの結果として、シグナルを返却します
def check_cross_signals(latest_data: pd.Series) -> Tuple[Optional[str], Optional[str]]:
    if latest_data['Buy_Signal_golden_cross'].item() and latest_data['is_up_trend'].item():
        print('Buy Signal: Golden Cross')
        return 'Buy', 'Golden Cross'
    elif latest_data['Sell_Signal_dead_cross'].item() and latest_data['is_down_trend'].item():
        print('Sell Signal: Dead Cross')
        return 'Sell', 'Dead Cross'
    return None, None

def check_up_down_signals(latest_data: pd.Series, UP_DOWN_PERIODS: List[int]) -> Tuple[Optional[str], Optional[str]]:
    for period in UP_DOWN_PERIODS:
        if latest_data[f'Buy_Signal_{period}'].item() and latest_data['is_up_trend'].item():
            print(f'Buy Signal: Up for {period} days')
            return 'Buy', f'Up for {period} days'
        elif latest_data[f'Sell_Signal_{period}'].item() and latest_data['is_down_trend'].item():
            print(f'Sell Signal: Down for {period} days')
            return 'Sell', f'Down for {period} days'
    return None, None

def check_other_signals(latest_data: pd.Series) -> Tuple[Optional[str], Optional[str]]:
    if latest_data['Buy_Signal_MA_PPP'].item() and latest_data['is_up_trend'].item():
        print('Buy Signal: PPP')
        return 'Buy', 'PPP'
    elif latest_data['Sell_Signal_MA_reverse_PPP'].item() and latest_data['is_down_trend'].item():
        print('Sell Signal: Reverse PPP')
        return 'Sell', 'Reverse PPP'
    elif latest_data['buy_signal_lower_half'].item() and latest_data['is_up_trend'].item():
        print('Buy Signal: Lower Half')
        return 'Buy', 'Lower Half'
    elif latest_data['sell_signal_Reverse_lower_half'].item() and latest_data['is_down_trend'].item():
        print('Sell Signal: Reverse Lower Half')
        return 'Sell', 'Reverse Lower Half'
    elif latest_data['buy_signal_bird_beak'].item() and latest_data['is_up_trend'].item():
        print('Buy Signal: Bird Beak')
        return 'Buy', 'Bird Beak'
    elif latest_data['sell_signal_reverse_bird_beak'].item() and latest_data['is_down_trend'].item():
        print('Sell Signal: Reverse Bird Beak')
        return 'Sell', 'Reverse Bird Beak'
    return None, None

# 最新の日付でのシグナルを出力
def get_latest_signals(kabuData: pd.DataFrame, UP_DOWN_PERIODS: List[int]) -> Tuple[Optional[str], Optional[str]]:
    latest_data = kabuData.iloc[-1]
    signal_type, signal_kind = check_cross_signals(latest_data)
    if signal_type is None:
        signal_type, signal_kind = check_up_down_signals(latest_data, UP_DOWN_PERIODS)
    if signal_type is None:
        signal_type, signal_kind = check_other_signals(latest_data)
    return signal_type, signal_kind

# # データのプロット
# def create_graph(calculated_data):
#     plt.figure(figsize=(12,5))
#     colors = ['blue', 'red', 'green', 'violet', 'indigo', 'orange', 'black']
#     for period, color in zip(SMA_PERIODS, colors):
#         plt.plot(kabuData.index, kabuData[f'SMA_{period}'], label=f'{period} Day SMA', color=color)

#     plt.plot(kabuData[kabuData['Buy_Signal_golden_cross']].index, kabuData['SMA_5'][kabuData['Buy_Signal_golden_cross']], '^', markersize=10, color='m', label='buy signal')
#     plt.plot(kabuData[kabuData['Sell_Signal_dead_cross']].index, kabuData['SMA_5'][kabuData['Sell_Signal_dead_cross']], 'v', markersize=10, color='k', label='sell signal')

#     plt.title('Apple Close Price with Moving Averages and Signals')
#     plt.xlabel('Date')
#     plt.ylabel('Price')
#     plt.legend()
#     plt.grid()
#     plt.show()




# 注文実行
# このサンプルコードでは、実際の売買注文は行わず、シグナルの生成だけを行います。
def main(kabuData: pd.DataFrame) -> Tuple[str, str]:
    # 移動平均線の計算
    kabuData = calculate_sma(kabuData, SMA_PERIODS)

    # 上昇トレンドと下降トレンドのカウント
    kabuData = count_trend_days(kabuData)

    # 陽線と陰線の判定
    kabuData['Up'] = kabuData['4. close'] > kabuData['1. open']
    kabuData['Down'] = kabuData['4. close'] < kabuData['1. open']

    calculated_kabu_data = calculate_signals(kabuData, UP_DOWN_PERIODS, SMA_PERIODS, CROSS_PERIODS)
    
    # get_latest_signals関数を呼び出し、結果をsignalTypeとsignalKindに割り当てる
    signalType, signalKind = get_latest_signals(calculated_kabu_data, UP_DOWN_PERIODS)
    
    
    # データプロット関数を実行すると処理が止まるので、コメントアウトしています
    # create_graph(calculated_kabu_data)
    
    return signalType, signalKind
