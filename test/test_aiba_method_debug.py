"""
Aibaメソッドのバックテスト（デバッグ版）
シグナル計算の詳細を表示して、なぜシグナルが発生しないかを分析します。
"""

from datetime import datetime, timedelta
import sys
import os
import numpy as np
import pandas as pd

# プロジェクトのルートディレクトリをPYTHONPATHに追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.helpers.trend_logic import standardize_headers
from src import aiba_trade_method
from src.calculaters.signals import calculate_signals
from src.calculaters.trends import count_trend_days

def create_trending_sample_data() -> pd.DataFrame:
    """トレンドのあるサンプルデータを作成（よりシグナルが発生しやすい）"""
    # 200日分のサンプルデータを作成
    start_date = datetime.now() - timedelta(days=200)
    dates = pd.date_range(start=start_date, periods=200, freq='D')
    
    # 基本価格を設定
    base_price = 100
    
    # より明確なトレンドを持つデータを作成
    np.random.seed(42)
    
    # 段階的なトレンドを作成
    trend_periods = [
        (50, -0.005),   # 下降トレンド
        (50, 0.008),    # 上昇トレンド
        (50, -0.003),   # 軽い下降
        (50, 0.006),    # 上昇トレンド
    ]
    
    prices = [base_price]
    for period_length, trend in trend_periods:
        for i in range(period_length):
            # トレンド + ランダムウォーク
            daily_return = trend + np.random.normal(0, 0.015)
            prices.append(prices[-1] * (1 + daily_return))
    
    # 最初の価格を除去して200日分にする
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
    
    # DataFrameを作成
    data = pd.DataFrame({
        '1. open': prices,
        '2. high': highs,
        '3. low': lows,
        '4. close': prices,
        '5. volume': volumes
    }, index=dates)
    
    return data

def debug_signal_calculation(kabuData: pd.DataFrame) -> pd.DataFrame:
    """シグナル計算のデバッグ"""
    print("\n=== シグナル計算デバッグ ===")
    
    # 移動平均を計算
    kabuData = aiba_trade_method.calculate_sma(kabuData, aiba_trade_method.SMA_PERIODS)
    print(f"移動平均計算完了: {aiba_trade_method.SMA_PERIODS}")
    
    # トレンド日数を計算
    kabuData = count_trend_days(kabuData)
    print("トレンド日数計算完了")
    
    # 上昇・下降フラグを計算
    kabuData['Up'] = kabuData['4. close'] > kabuData['1. open']
    kabuData['Down'] = kabuData['4. close'] < kabuData['1. open']
    
    # シグナルを計算
    calculated_kabu_data = calculate_signals(kabuData, aiba_trade_method.UP_DOWN_PERIODS, aiba_trade_method.SMA_PERIODS, aiba_trade_method.CROSS_PERIODS)
    
    # 最新の20日間のデータを表示
    print("\n=== 最新20日間のデータサンプル ===")
    print("利用可能なカラム:", list(calculated_kabu_data.columns))
    
    # 利用可能なカラムで表示
    display_cols = ['4. close', 'Up', 'Down']
    sma_cols = [col for col in calculated_kabu_data.columns if col.startswith('SMA_')]
    display_cols.extend(sma_cols[:3])  # 最初の3つのSMAカラムを追加
    
    sample_data = calculated_kabu_data.tail(20)[display_cols]
    print(sample_data.to_string())
    
    return calculated_kabu_data

def analyze_signal_conditions(kabuData: pd.DataFrame) -> None:
    """シグナル発生条件の詳細分析"""
    print("\n=== シグナル発生条件の詳細分析 ===")
    
    # 最後の50日間を分析
    recent_data = kabuData.tail(50)
    
    for i in range(10, len(recent_data)):
        data_slice = recent_data.iloc[:i+1]
        signalType, signalKind = aiba_trade_method.get_latest_signals(data_slice, aiba_trade_method.UP_DOWN_PERIODS)
        
        if signalType in ['Buy', 'Sell']:
            date = data_slice.index[-1]
            close_price = data_slice['4. close'].iloc[-1]
            print(f"{date}: {signalType} シグナル ({signalKind}) - 終値: {close_price:.2f}")
            
            # シグナル発生時の詳細情報
            latest_row = data_slice.iloc[-1]
            sma_cols = [col for col in data_slice.columns if col.startswith('SMA_')]
            for sma_col in sma_cols[:3]:  # 最初の3つのSMAを表示
                value = latest_row.get(sma_col, None)
                if value is not None and not pd.isna(value):
                    print(f"  {sma_col}: {value:.2f}")
            print(f"  Up: {latest_row.get('Up', False)}")
            print(f"  Down: {latest_row.get('Down', False)}")

def main() -> None:
    """メイン処理"""
    print("=== Aibaメソッドバックテスト（デバッグ版） ===")
    print("トレンドのあるサンプルデータでシグナル発生を分析します。\n")
    
    # トレンドのあるサンプルデータの作成
    print("トレンドのあるサンプルデータを作成しています...")
    kabuData = create_trending_sample_data()
    
    print(f"データ期間: {kabuData.index.min().strftime('%Y-%m-%d')} ～ {kabuData.index.max().strftime('%Y-%m-%d')}")
    print(f"データ数: {len(kabuData)} 日")
    print(f"価格範囲: {kabuData['4. close'].min():.2f} ～ {kabuData['4. close'].max():.2f}")
    
    # 価格トレンドの可視化
    print("\n=== 価格トレンドの概要 ===")
    for i in range(0, len(kabuData), 40):
        end_idx = min(i + 40, len(kabuData))
        period_data = kabuData.iloc[i:end_idx]
        start_price = period_data['4. close'].iloc[0]
        end_price = period_data['4. close'].iloc[-1]
        change = (end_price - start_price) / start_price * 100
        print(f"期間 {i+1}-{end_idx}: {start_price:.2f} → {end_price:.2f} ({change:+.1f}%)")
    
    # シグナル計算（デバッグ付き）
    calculated_kabu_data = debug_signal_calculation(kabuData)
    
    # シグナル発生条件の分析
    analyze_signal_conditions(calculated_kabu_data)
    
    # 全期間でのシグナル分析
    print("\n=== 全期間シグナル分析 ===")
    signal_counts = {}
    for i in range(max(aiba_trade_method.SMA_PERIODS), len(calculated_kabu_data)):
        signalType, signalKind = aiba_trade_method.get_latest_signals(calculated_kabu_data.iloc[:i], aiba_trade_method.UP_DOWN_PERIODS)
        if signalType in ['Buy', 'Sell']:
            key = f"{signalType}_{signalKind}"
            signal_counts[key] = signal_counts.get(key, 0) + 1
    
    print("シグナル発生回数:")
    if signal_counts:
        for signal, count in signal_counts.items():
            print(f"  {signal}: {count} 回")
    else:
        print("  シグナルが発生しませんでした")
    
    # Aibaメソッドのパラメータ確認
    print("\n=== Aibaメソッドパラメータ ===")
    print(f"移動平均期間: {aiba_trade_method.SMA_PERIODS}")
    print(f"上昇下降日数期間: {aiba_trade_method.UP_DOWN_PERIODS}")
    print(f"クロス検証期間: {aiba_trade_method.CROSS_PERIODS}")
    
    print("\nデバッグ分析が完了しました。")

if __name__ == '__main__':
    main()
