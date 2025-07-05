"""
シグナル計算のデバッグ詳細版
各シグナルの計算過程を詳しく分析します。
"""

from datetime import datetime, timedelta
import sys
import os
import numpy as np
import pandas as pd

# プロジェクトのルートディレクトリをPYTHONPATHに追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.helpers.trend_logic import standardize_headers, is_golden_cross, is_dead_cross, is_pampakapam
from src import aiba_trade_method
from src.calculaters.signals import calculate_signals
from src.calculaters.trends import count_trend_days

def create_trending_sample_data() -> pd.DataFrame:
    """トレンドのあるサンプルデータを作成"""
    start_date = datetime.now() - timedelta(days=200)
    dates = pd.date_range(start=start_date, periods=200, freq='D')
    
    base_price = 100
    np.random.seed(42)
    
    # より明確なトレンドを持つデータを作成
    trend_periods = [
        (50, -0.005),   # 下降トレンド
        (50, 0.008),    # 上昇トレンド
        (50, -0.003),   # 軽い下降
        (50, 0.006),    # 上昇トレンド
    ]
    
    prices = [base_price]
    for period_length, trend in trend_periods:
        for i in range(period_length):
            daily_return = trend + np.random.normal(0, 0.015)
            prices.append(prices[-1] * (1 + daily_return))
    
    prices = prices[1:]
    
    # 高値、安値、出来高を生成
    highs = []
    lows = []
    for price in prices:
        high = price * (1 + np.random.uniform(0.005, 0.025))
        low = price * (1 - np.random.uniform(0.005, 0.025))
        highs.append(high)
        lows.append(low)
    
    volumes = [np.random.randint(10000, 100000) for _ in range(200)]
    
    data = pd.DataFrame({
        '1. open': prices,
        '2. high': highs,
        '3. low': lows,
        '4. close': prices,
        '5. volume': volumes
    }, index=dates)
    
    return data

def debug_signal_details(kabuData: pd.DataFrame) -> None:
    """シグナル計算の詳細デバッグ"""
    print("\n=== 詳細シグナルデバッグ ===")
    
    # 最新50日間のデータを詳しく見る
    recent_data = kabuData.tail(50)
    
    print("\n--- ゴールデンクロス・デッドクロス確認 ---")
    cross_data = recent_data[['4. close', 'SMA_25', 'SMA_75', 'Buy_Signal_golden_cross', 'Sell_Signal_dead_cross']].tail(10)
    print(cross_data.to_string())
    
    # ゴールデンクロスの条件確認
    cross_conditions = []
    for i in range(1, len(recent_data)):
        prev_row = recent_data.iloc[i-1]
        curr_row = recent_data.iloc[i]
        
        # 25日線が75日線を上抜けたか
        golden_cross = (prev_row['SMA_25'] <= prev_row['SMA_75'] and 
                       curr_row['SMA_25'] > curr_row['SMA_75'])
        
        # デッドクロス
        dead_cross = (prev_row['SMA_25'] >= prev_row['SMA_75'] and 
                     curr_row['SMA_25'] < curr_row['SMA_75'])
        
        if golden_cross or dead_cross:
            cross_conditions.append({
                'date': curr_row.name,
                'type': 'Golden Cross' if golden_cross else 'Dead Cross',
                'SMA_25_prev': prev_row['SMA_25'],
                'SMA_75_prev': prev_row['SMA_75'],
                'SMA_25_curr': curr_row['SMA_25'],
                'SMA_75_curr': curr_row['SMA_75']
            })
    
    print(f"\n手動検出されたクロス: {len(cross_conditions)} 個")
    for condition in cross_conditions:
        print(f"  {condition['date']}: {condition['type']}")
        print(f"    前日 SMA25: {condition['SMA_25_prev']:.2f}, SMA75: {condition['SMA_75_prev']:.2f}")
        print(f"    当日 SMA25: {condition['SMA_25_curr']:.2f}, SMA75: {condition['SMA_75_curr']:.2f}")
    
    print("\n--- PPPパターン確認 ---")
    ppp_data = recent_data[['4. close'] + [f'SMA_{p}' for p in [5, 20, 60, 100, 200, 300]] + ['Buy_Signal_MA_PPP', 'Sell_Signal_MA_reverse_PPP']].tail(5)
    print(ppp_data.to_string())
    
    # PPPパターンの手動チェック
    print("\n--- PPPパターン手動チェック ---")
    for i in range(-5, 0):
        row = recent_data.iloc[i]
        date = row.name
        
        # PPP条件: SMA_5 > SMA_20 > SMA_60 > SMA_100 > SMA_200 > SMA_300
        sma_values = [row[f'SMA_{p}'] for p in [5, 20, 60, 100, 200, 300] if not pd.isna(row[f'SMA_{p}'])]
        is_ppp = all(sma_values[i] >= sma_values[i+1] for i in range(len(sma_values)-1))
        
        # Reverse PPP条件: SMA_5 < SMA_20 < SMA_60 < SMA_100 < SMA_200 < SMA_300
        is_reverse_ppp = all(sma_values[i] <= sma_values[i+1] for i in range(len(sma_values)-1))
        
        print(f"  {date}: PPP={is_ppp}, Reverse PPP={is_reverse_ppp}")
        print(f"    SMA順序: {' > '.join([f'{v:.1f}' for v in sma_values])}")
    
    print("\n--- 連続上昇/下降日数確認 ---")
    up_down_data = recent_data[['4. close', 'Up', 'Down', 'up_trend_count', 'down_trend_count'] + 
                              [f'Buy_Signal_{p}' for p in aiba_trade_method.UP_DOWN_PERIODS] + 
                              [f'Sell_Signal_{p}' for p in aiba_trade_method.UP_DOWN_PERIODS]].tail(10)
    print(up_down_data.to_string())
    
    print("\n--- トレンド判定確認 ---")
    trend_data = recent_data[['4. close', 'is_up_trend', 'is_down_trend']].tail(10)
    print(trend_data.to_string())

def create_simple_test_data() -> pd.DataFrame:
    """シンプルなテストデータを作成（確実にシグナルが発生するように）"""
    start_date = datetime.now() - timedelta(days=100)
    dates = pd.date_range(start=start_date, periods=100, freq='D')
    
    # 明確なゴールデンクロスが発生するデータを作成
    prices = []
    base_price = 100
    
    # 最初の50日は下降トレンド
    for i in range(50):
        price = base_price - (i * 0.5)  # 徐々に下降
        prices.append(price)
    
    # 次の50日は上昇トレンド（ゴールデンクロスを誘発）
    for i in range(50):
        price = prices[-1] + (i * 0.8)  # 徐々に上昇
        prices.append(price)
    
    # 高値、安値を価格に基づいて設定
    highs = [p * 1.02 for p in prices]
    lows = [p * 0.98 for p in prices]
    opens = prices.copy()
    
    volumes = [50000] * 100
    
    data = pd.DataFrame({
        '1. open': opens,
        '2. high': highs,
        '3. low': lows,
        '4. close': prices,
        '5. volume': volumes
    }, index=dates)
    
    return data

def main() -> None:
    """メイン処理"""
    print("=== シグナル計算詳細デバッグ ===")
    
    # トレンドありサンプルデータでのテスト
    print("\n--- トレンドありサンプルデータ ---")
    kabuData = create_trending_sample_data()
    
    # シグナル計算
    kabuData = aiba_trade_method.calculate_sma(kabuData, aiba_trade_method.SMA_PERIODS)
    kabuData = count_trend_days(kabuData)
    kabuData['Up'] = kabuData['4. close'] > kabuData['1. open']
    kabuData['Down'] = kabuData['4. close'] < kabuData['1. open']
    calculated_kabu_data = calculate_signals(kabuData, aiba_trade_method.UP_DOWN_PERIODS, aiba_trade_method.SMA_PERIODS, aiba_trade_method.CROSS_PERIODS)
    
    debug_signal_details(calculated_kabu_data)
    
    # シンプルなテストデータでのテスト
    print("\n\n--- シンプルテストデータ ---")
    simple_data = create_simple_test_data()
    
    # シグナル計算
    simple_data = aiba_trade_method.calculate_sma(simple_data, aiba_trade_method.SMA_PERIODS)
    simple_data = count_trend_days(simple_data)
    simple_data['Up'] = simple_data['4. close'] > simple_data['1. open']
    simple_data['Down'] = simple_data['4. close'] < simple_data['1. open']
    simple_calculated = calculate_signals(simple_data, aiba_trade_method.UP_DOWN_PERIODS, aiba_trade_method.SMA_PERIODS, aiba_trade_method.CROSS_PERIODS)
    
    debug_signal_details(simple_calculated)
    
    # 価格とSMAの関係を可視化
    print("\n--- 価格とSMAの関係（最新10日） ---")
    display_data = simple_calculated[['4. close', 'SMA_5', 'SMA_25', 'SMA_75']].tail(10)
    print(display_data.to_string())
    
    print("\nデバッグ分析が完了しました。")

if __name__ == '__main__':
    main()
