from typing import List
import pandas as pd
from helpers.trend_logic import is_break_5d, is_break_down_5d, is_buy_signal, is_dead_cross, is_golden_cross, is_pampakapam, is_sell_signal, is_trend

# シグナルの生成
def calculate_signals(kabuData: pd.DataFrame, UP_DOWN_PERIODS: List[int], SMA_PERIODS: List[int], CROSS_PERIODS: List[int]) -> pd.DataFrame:
    
    # 買いシグナル：陰線が9日間または13日間連続する、または日足が75日線を下から上に抜けて陽線で終わる
    # 売りシグナル：陽線が9日間または13日間連続する、または日足が75日線を上から下に抜けて陰線で終わる
    for period in UP_DOWN_PERIODS:
        kabuData[f'Buy_Signal_{period}'] = (
            is_buy_signal(kabuData, period)
        )
        kabuData[f'Sell_Signal_{period}'] = (
            is_sell_signal(kabuData, period)
        )

    # パンパカパンと売りシグナルの生成
    # 買いシグナル（パンパカパン）：移動平均線が5, 20, 60, 100, 200, 300日の順番で高い
    # 売りシグナル：移動平均線が5, 20, 60, 100, 200, 300日の順番で安い
    kabuData['Buy_Signal_MA_PPP'] = kabuData.apply(lambda row: is_pampakapam(row, SMA_PERIODS, True), axis=1)
    kabuData['Sell_Signal_MA_reverse_PPP'] = kabuData.apply(lambda row: is_pampakapam(row, SMA_PERIODS, False), axis=1)

    # ゴールデンクロスとデッドクロスのシグナル生成
    kabuData['Buy_Signal_golden_cross'] = is_golden_cross(kabuData, CROSS_PERIODS)
    kabuData['Sell_Signal_dead_cross'] = is_dead_cross(kabuData, CROSS_PERIODS)


    # 下半身：買いシグナルシグナル生成
    # 5日線が上昇トレンドで、前日の日足線が5日線より下にあり、かつ、当日の日足線が陽線で5日線を実体の半分以上突き抜けていれば、買いシグナルとします。
    # 5日線の上昇トレンドを判定します。5日線の差分が正（つまり、前日よりも上昇している）であれば、上昇トレンドと判定します。
    # 日足線が5日線より下にあるか判定します。終値が5日線よりも低ければ、その日の日足線は5日線より下にあると判定します。
    # 陽線かつ5日線を実体の半分以上突き抜けたか判定します。終値が5日線よりも高く、かつ、終値と始値の差（実体）が5日線を突き抜けた部分（終値と5日線との差）の半分以上であれば、5日線を実体の半分以上突き抜けたと判定します。
    # 買いシグナル（下半身）を生成します。
    kabuData['5d_trend'] = is_trend(kabuData, 'SMA_5', 'up')
    kabuData['below_5d'] = kabuData['4. close'] < kabuData['SMA_5']
    kabuData['break_5d'] = is_break_5d(kabuData)
    kabuData['buy_signal_lower_half'] = kabuData['5d_trend'] & kabuData['below_5d'].shift() & kabuData['Up'] & kabuData['break_5d']

    # 売りシグナル（逆下半身）を生成
    kabuData['5d_down_trend'] = is_trend(kabuData, 'SMA_5', 'down')
    kabuData['above_5d'] = kabuData['4. close'] > kabuData['SMA_5']
    kabuData['break_down_5d'] = is_break_down_5d(kabuData)
    kabuData['sell_signal_Reverse_lower_half'] = kabuData['5d_down_trend'] & kabuData['above_5d'].shift() & kabuData['Down'] & kabuData['break_down_5d']


    # 買いシグナル：くちばし
    # 5日線と10日線が上昇トレンドで、前日の5日線が10日線より下にあり、かつ、当日の5日線が10日線を上抜けていれば、買いシグナルとします。
    # 5日線と10日線の上昇トレンドを判定します。5日線と10日線の差分が正（つまり、前日よりも上昇している）であれば、上昇トレンドと判定します。
    # 5日線が10日線より下にあるか判定します。5日線が10日線よりも低ければ、その日の5日線は10日線より下にあると判定します。
    # 5日線が10日線を上抜けたか判定します。5日線が10日線よりも高ければ、5日線は10日線を上抜けたと判定します。
    kabuData['5d_up_trend'] = is_trend(kabuData, 'SMA_5', 'up')
    kabuData['10d_up_trend'] = is_trend(kabuData, 'SMA_10', 'up')
    kabuData['5d_below_10d'] = kabuData['SMA_5'] < kabuData['SMA_10']
    kabuData['5d_breaks_10d'] = kabuData['SMA_5'] > kabuData['SMA_10']
    kabuData['buy_signal_bird_beak'] = kabuData['5d_up_trend'] & kabuData['10d_up_trend'] & kabuData['5d_below_10d'].shift() & kabuData['5d_breaks_10d']

    # 売りシグナル：逆くちばし
    kabuData['5d_down_trend'] = is_trend(kabuData, 'SMA_5', 'down')
    kabuData['10d_down_trend'] = is_trend(kabuData, 'SMA_10', 'down')
    kabuData['5d_above_10d'] = kabuData['SMA_5'] > kabuData['SMA_10']
    kabuData['5d_breaks_down_10d'] = kabuData['SMA_5'] < kabuData['SMA_10']
    kabuData['sell_signal_reverse_bird_beak'] = kabuData['5d_down_trend'] & kabuData['10d_down_trend'] & kabuData['5d_above_10d'].shift() & kabuData['5d_breaks_down_10d']

    return kabuData
