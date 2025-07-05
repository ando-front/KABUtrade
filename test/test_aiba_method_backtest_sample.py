"""
Aibaメソッドのバックテスト（サンプルデータ版）
Yahoo Finance APIのレート制限を回避するために、サンプルデータを使用してバックテストを実行します。
"""

from datetime import datetime, timedelta
import sys
import os
import numpy as np
import pandas as pd
import logging
from dotenv import load_dotenv
import time

# プロジェクトのルートディレクトリをPYTHONPATHに追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.helpers.trend_logic import standardize_headers
from src import aiba_trade_method
from src.calculaters.signals import calculate_signals
from src.calculaters.trends import count_trend_days

def create_sample_data() -> pd.DataFrame:
    """サンプルの株価データを作成"""
    # 200日分のサンプルデータを作成
    start_date = datetime.now() - timedelta(days=200)
    dates = pd.date_range(start=start_date, periods=200, freq='D')
    
    # 基本価格を設定
    base_price = 100
    
    # ランダムウォークで価格を生成
    np.random.seed(42)  # 再現性のため
    returns = np.random.normal(0.001, 0.02, 200)  # 平均0.1%、標準偏差2%の日次リターン
    
    # 価格データを生成
    prices = [base_price]
    for return_rate in returns[1:]:
        prices.append(prices[-1] * (1 + return_rate))
    
    # 高値、安値、出来高を生成
    highs = [price * (1 + np.random.uniform(0, 0.03)) for price in prices]
    lows = [price * (1 - np.random.uniform(0, 0.03)) for price in prices]
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

def backtest_signals(kabuData: pd.DataFrame) -> pd.DataFrame:
    """シグナルの計算"""
    kabuData = aiba_trade_method.calculate_sma(kabuData, aiba_trade_method.SMA_PERIODS)
    kabuData = count_trend_days(kabuData)
    kabuData['Up'] = kabuData['4. close'] > kabuData['1. open']
    kabuData['Down'] = kabuData['4. close'] < kabuData['1. open']
    calculated_kabu_data = calculate_signals(kabuData, aiba_trade_method.UP_DOWN_PERIODS, aiba_trade_method.SMA_PERIODS, aiba_trade_method.CROSS_PERIODS)
    return calculated_kabu_data

def run_backtest(kabuData: pd.DataFrame, symbol: str = "SAMPLE") -> dict:
    """バックテストの実行"""
    initial_cash = 1000000  # 初期資金
    cash = initial_cash
    position = 0  # 保有株数
    trades = []
    
    for i in range(1, len(kabuData)):
        signalType, signalKind = aiba_trade_method.get_latest_signals(kabuData.iloc[:i], aiba_trade_method.UP_DOWN_PERIODS)
        
        if signalType == 'Buy' and cash > 0:
            position = cash / kabuData['4. close'].iloc[i]
            cash = 0
            trades.append({
                'date': kabuData.index[i],
                'action': 'Buy',
                'price': kabuData['4. close'].iloc[i],
                'signal_kind': signalKind
            })
            print(f"Buy at {kabuData.index[i].strftime('%Y-%m-%d')}: {kabuData['4. close'].iloc[i]:.2f} ({signalKind})")
        elif signalType == 'Sell' and position > 0:
            cash = position * kabuData['4. close'].iloc[i]
            position = 0
            trades.append({
                'date': kabuData.index[i],
                'action': 'Sell',
                'price': kabuData['4. close'].iloc[i],
                'signal_kind': signalKind
            })
            print(f"Sell at {kabuData.index[i].strftime('%Y-%m-%d')}: {kabuData['4. close'].iloc[i]:.2f} ({signalKind})")

    # バックテスト結果の計算
    final_value = cash + position * kabuData['4. close'].iloc[-1]
    return_rate = (final_value - initial_cash) / initial_cash * 100
    
    # 結果の表示
    print(f"\n=== バックテスト結果 ({symbol}) ===")
    print(f"初期資金: {initial_cash:,} 円")
    print(f"最終資産: {final_value:,.2f} 円")
    print(f"収益率: {return_rate:.2f}%")
    print(f"取引回数: {len(trades)} 回")
    
    # 取引詳細の表示
    if trades:
        print("\n=== 取引詳細 ===")
        for trade in trades:
            print(f"{trade['date'].strftime('%Y-%m-%d')}: {trade['action']} at {trade['price']:.2f} ({trade['signal_kind']})")
    
    return {
        'symbol': symbol,
        'initial_cash': initial_cash,
        'final_value': final_value,
        'return_rate': return_rate,
        'trade_count': len(trades),
        'trades': trades
    }

def analyze_signals(kabuData: pd.DataFrame) -> None:
    """シグナルの分析"""
    print("\n=== シグナル分析 ===")
    
    # 各シグナルの発生回数を集計
    signal_counts = {}
    for i in range(1, len(kabuData)):
        signalType, signalKind = aiba_trade_method.get_latest_signals(kabuData.iloc[:i], aiba_trade_method.UP_DOWN_PERIODS)
        if signalType in ['Buy', 'Sell']:
            key = f"{signalType}_{signalKind}"
            signal_counts[key] = signal_counts.get(key, 0) + 1
    
    print("シグナル発生回数:")
    for signal, count in signal_counts.items():
        print(f"  {signal}: {count} 回")

def main() -> None:
    """メイン処理"""
    print("=== Aibaメソッドバックテスト（サンプルデータ版） ===")
    print("サンプルデータを使用してバックテストを実行します。\n")
    
    # サンプルデータの作成
    print("サンプルデータを作成しています...")
    kabuData = create_sample_data()
    
    print(f"データ期間: {kabuData.index.min().strftime('%Y-%m-%d')} ～ {kabuData.index.max().strftime('%Y-%m-%d')}")
    print(f"データ数: {len(kabuData)} 日")
    print(f"価格範囲: {kabuData['4. close'].min():.2f} ～ {kabuData['4. close'].max():.2f}")
    
    # シグナルの計算
    print("\nシグナルを計算しています...")
    calculated_kabu_data = backtest_signals(kabuData)
    
    # シグナル分析
    analyze_signals(calculated_kabu_data)
    
    # バックテストの実行
    print("\nバックテストを実行しています...")
    result = run_backtest(calculated_kabu_data, "SAMPLE")
    
    # 統計情報の表示
    print("\n=== 統計情報 ===")
    print(f"移動平均期間: {aiba_trade_method.SMA_PERIODS}")
    print(f"上昇下降日数期間: {aiba_trade_method.UP_DOWN_PERIODS}")
    print(f"クロス検証期間: {aiba_trade_method.CROSS_PERIODS}")
    
    # 移動平均の状況
    if len(calculated_kabu_data) > 0:
        latest_data = calculated_kabu_data.iloc[-1]
        latest_date = calculated_kabu_data.index[-1]
        if hasattr(latest_date, 'strftime'):
            date_str = latest_date.strftime('%Y-%m-%d')
        else:
            date_str = str(latest_date)
        print(f"\n最新データ（{date_str}）:")
        print(f"  終値: {latest_data['4. close']:.2f}")
        for period in aiba_trade_method.SMA_PERIODS:
            sma_col = f'SMA_{period}'
            if sma_col in calculated_kabu_data.columns:
                print(f"  SMA{period}: {latest_data[sma_col]:.2f}")
    
    print("\nバックテストが完了しました。")

if __name__ == '__main__':
    main()
