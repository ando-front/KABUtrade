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

# 緩和レベル定義
class RelaxationLevel:
    NONE = "none"           # 従来の厳格版
    MODERATE = "moderate"   # 中程度の緩和（トレンド条件削除）
    HIGH = "high"          # 高度な緩和（簡易MAクロス追加）



# 移動平均線の計算(5, 10, 20, 25, 30, 60, 75, 100, 200)
def calculate_sma(data: pd.DataFrame, periods: List[int]) -> pd.DataFrame:
    for period in periods:
        data[f'SMA_{period}'] = data['4. close'].rolling(window=period).mean()
    return data


# 最新のデータがゴールデンクロスかデッドクロスのシグナルを持っているかチェック
# ゴールデンクロスもデッドクロスもない場合、連続上昇日数または連続下落日数に基づくシグナル、移動平均に基づくシグナルをチェックします。
# チェックの結果として、シグナルを返却します

def check_cross_signals(latest_data: pd.Series, relaxation_level: str = RelaxationLevel.NONE) -> Tuple[Optional[str], Optional[str]]:
    """ゴールデンクロス・デッドクロス判定（緩和対応版）"""
    if relaxation_level == RelaxationLevel.NONE:
        # 従来の厳格版（トレンド条件必須）
        if latest_data['Buy_Signal_golden_cross'] and latest_data['is_up_trend']:
            print('Buy Signal: Golden Cross')
            return 'Buy', 'Golden Cross'
        elif latest_data['Sell_Signal_dead_cross'] and latest_data['is_down_trend']:
            print('Sell Signal: Dead Cross')
            return 'Sell', 'Dead Cross'
    else:
        # 緩和版（トレンド条件なし）
        if latest_data['Buy_Signal_golden_cross']:
            print('Buy Signal: Golden Cross (Relaxed)')
            return 'Buy', 'Golden Cross (Relaxed)'
        elif latest_data['Sell_Signal_dead_cross']:
            print('Sell Signal: Dead Cross (Relaxed)')
            return 'Sell', 'Dead Cross (Relaxed)'
    return None, None

def check_up_down_signals(latest_data: pd.Series, UP_DOWN_PERIODS: List[int], relaxation_level: str = RelaxationLevel.NONE) -> Tuple[Optional[str], Optional[str]]:
    """連続上昇下降日数判定（緩和対応版）"""
    for period in UP_DOWN_PERIODS:
        if relaxation_level == RelaxationLevel.NONE:
            # 従来の厳格版（トレンド条件必須）
            if latest_data[f'Buy_Signal_{period}'] and latest_data['is_up_trend']:
                print(f'Buy Signal: Up for {period} days')
                return 'Buy', f'Up for {period} days'
            elif latest_data[f'Sell_Signal_{period}'] and latest_data['is_down_trend']:
                print(f'Sell Signal: Down for {period} days')
                return 'Sell', f'Down for {period} days'
        else:
            # 緩和版（トレンド条件なし）
            if latest_data[f'Buy_Signal_{period}']:
                print(f'Buy Signal: Up for {period} days (Relaxed)')
                return 'Buy', f'Up for {period} days (Relaxed)'
            elif latest_data[f'Sell_Signal_{period}']:
                print(f'Sell Signal: Down for {period} days (Relaxed)')
                return 'Sell', f'Down for {period} days (Relaxed)'
    return None, None

def check_other_signals(latest_data: pd.Series, relaxation_level: str = RelaxationLevel.NONE) -> Tuple[Optional[str], Optional[str]]:
    """その他シグナル判定（緩和対応版）"""
    if relaxation_level == RelaxationLevel.NONE:
        # 従来の厳格版（トレンド条件必須）
        if latest_data['Buy_Signal_MA_PPP'] and latest_data['is_up_trend']:
            print('Buy Signal: PPP')
            return 'Buy', 'PPP'
        elif latest_data['Sell_Signal_MA_reverse_PPP'] and latest_data['is_down_trend']:
            print('Sell Signal: Reverse PPP')
            return 'Sell', 'Reverse PPP'
        elif latest_data['buy_signal_lower_half'] and latest_data['is_up_trend']:
            print('Buy Signal: Lower Half')
            return 'Buy', 'Lower Half'
        elif latest_data['sell_signal_Reverse_lower_half'] and latest_data['is_down_trend']:
            print('Sell Signal: Reverse Lower Half')
            return 'Sell', 'Reverse Lower Half'
        elif latest_data['buy_signal_bird_beak'] and latest_data['is_up_trend']:
            print('Buy Signal: Bird Beak')
            return 'Buy', 'Bird Beak'
        elif latest_data['sell_signal_reverse_bird_beak'] and latest_data['is_down_trend']:
            print('Sell Signal: Reverse Bird Beak')
            return 'Sell', 'Reverse Bird Beak'
    elif relaxation_level == RelaxationLevel.MODERATE:
        # 中程度の緩和（トレンド条件なし）
        if latest_data['Buy_Signal_MA_PPP']:
            print('Buy Signal: PPP (Relaxed)')
            return 'Buy', 'PPP (Relaxed)'
        elif latest_data['Sell_Signal_MA_reverse_PPP']:
            print('Sell Signal: Reverse PPP (Relaxed)')
            return 'Sell', 'Reverse PPP (Relaxed)'
        elif latest_data['buy_signal_lower_half']:
            print('Buy Signal: Lower Half (Relaxed)')
            return 'Buy', 'Lower Half (Relaxed)'
        elif latest_data['sell_signal_Reverse_lower_half']:
            print('Sell Signal: Reverse Lower Half (Relaxed)')
            return 'Sell', 'Reverse Lower Half (Relaxed)'
        elif latest_data['buy_signal_bird_beak']:
            print('Buy Signal: Bird Beak (Relaxed)')
            return 'Buy', 'Bird Beak (Relaxed)'
        elif latest_data['sell_signal_reverse_bird_beak']:
            print('Sell Signal: Reverse Bird Beak (Relaxed)')
            return 'Sell', 'Reverse Bird Beak (Relaxed)'
    elif relaxation_level == RelaxationLevel.HIGH:
        # 高度な緩和（簡易MAクロス追加）
        # シンプルなMAクロスオーバーを最優先でチェック
        if (latest_data.get('SMA_5', 0) > latest_data.get('SMA_25', 0) and 
            latest_data.get('4. close', 0) > latest_data.get('SMA_5', 0)):
            print('Buy Signal: Simple MA Cross Up')
            return 'Buy', 'Simple MA Cross Up'
        elif (latest_data.get('SMA_5', 0) < latest_data.get('SMA_25', 0) and 
              latest_data.get('4. close', 0) < latest_data.get('SMA_5', 0)):
            print('Sell Signal: Simple MA Cross Down')
            return 'Sell', 'Simple MA Cross Down'
        # 従来シグナルもトレンド条件なしで判定
        elif latest_data['Buy_Signal_MA_PPP']:
            print('Buy Signal: PPP (High Relaxed)')
            return 'Buy', 'PPP (High Relaxed)'
        elif latest_data['Sell_Signal_MA_reverse_PPP']:
            print('Sell Signal: Reverse PPP (High Relaxed)')
            return 'Sell', 'Reverse PPP (High Relaxed)'
        elif latest_data['buy_signal_lower_half']:
            print('Buy Signal: Lower Half (High Relaxed)')
            return 'Buy', 'Lower Half (High Relaxed)'
        elif latest_data['sell_signal_Reverse_lower_half']:
            print('Sell Signal: Reverse Lower Half (High Relaxed)')
            return 'Sell', 'Reverse Lower Half (High Relaxed)'
        elif latest_data['buy_signal_bird_beak']:
            print('Buy Signal: Bird Beak (High Relaxed)')
            return 'Buy', 'Bird Beak (High Relaxed)'
        elif latest_data['sell_signal_reverse_bird_beak']:
            print('Sell Signal: Reverse Bird Beak (High Relaxed)')
            return 'Sell', 'Reverse Bird Beak (High Relaxed)'
    return None, None
    return None, None

def get_latest_signals(kabuData: pd.DataFrame, UP_DOWN_PERIODS: List[int], relaxation_level: str = RelaxationLevel.NONE) -> Tuple[Optional[str], Optional[str]]:
    """最新シグナル取得（緩和レベル対応）
    Args:
        kabuData: 株価データ
        UP_DOWN_PERIODS: 上昇下降日数期間
        relaxation_level: 緩和レベル（NONE, MODERATE, HIGH）
    Returns:
        シグナルタイプとシグナル種類のタプル
    """
    latest_data = kabuData.iloc[-1]
    # 優先順位に従ってシグナルをチェック
    signal_type, signal_kind = check_cross_signals(latest_data, relaxation_level)
    if signal_type is None:
        signal_type, signal_kind = check_up_down_signals(latest_data, UP_DOWN_PERIODS, relaxation_level)
    if signal_type is None:
        signal_type, signal_kind = check_other_signals(latest_data, relaxation_level)
    return signal_type, signal_kind

# 後方互換性のための従来関数（非推奨）
def get_latest_signals_legacy(kabuData: pd.DataFrame, UP_DOWN_PERIODS: List[int]) -> Tuple[Optional[str], Optional[str]]:
    """後方互換性のための従来関数（非推奨）
    
    新しいコードでは get_latest_signals(..., relaxation_level=RelaxationLevel.NONE) を使用してください
    """
    return get_latest_signals(kabuData, UP_DOWN_PERIODS, RelaxationLevel.NONE)

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
def main(kabuData: pd.DataFrame, relaxation_level: str = RelaxationLevel.NONE) -> Tuple[str, str]:
    """メイン処理（緩和レベル対応）
    Args:
        kabuData: 株価データ
        relaxation_level: 緩和レベル（NONE, MODERATE, HIGH）
    Returns:
        シグナルタイプとシグナル種類のタプル
    """
    # 移動平均線の計算
    kabuData = calculate_sma(kabuData, SMA_PERIODS)
    # 上昇トレンドと下降トレンドのカウント
    kabuData = count_trend_days(kabuData)
    # 陽線と陰線の判定
    kabuData['Up'] = kabuData['4. close'] > kabuData['1. open']
    kabuData['Down'] = kabuData['4. close'] < kabuData['1. open']
    calculated_kabu_data = calculate_signals(kabuData, UP_DOWN_PERIODS, SMA_PERIODS, CROSS_PERIODS)
    # get_latest_signals関数を呼び出し、結果をsignalTypeとsignalKindに割り当てる
    signalType, signalKind = get_latest_signals(calculated_kabu_data, UP_DOWN_PERIODS, relaxation_level)
    print(f"緩和レベル: {relaxation_level}")
    print(f"買いor売りシグナルSignal Typeの結果: {signalType}")
    print(f"移動平均線のシグナルタイプSignal Kindの結果: {signalKind}")
    # データプロット関数を実行すると処理が止まるので、コメントアウトしています
    # create_graph(calculated_kabu_data)
    return signalType, signalKind

# 後方互換性のための従来関数
def main_legacy(kabuData: pd.DataFrame) -> Tuple[str, str]:
    """後方互換性のための従来関数（非推奨）
    
    新しいコードでは main(..., relaxation_level=RelaxationLevel.NONE) を使用してください
    """
    return main(kabuData, RelaxationLevel.NONE)
