"""
Aibaメソッドの緩和版バックテスト
シグナル発生条件を段階的に緩和して、シグナル発生機会を増やすテストを行います。
"""

from datetime import datetime, timedelta
import sys
import os
import numpy as np
import pandas as pd
from typing import Tuple, Optional, List

# プロジェクトのルートディレクトリをPYTHONPATHに追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.helpers.trend_logic import standardize_headers
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

# 緩和版のシグナル判定関数
def check_cross_signals_relaxed(latest_data: pd.Series, relaxation_level: str = "moderate") -> Tuple[Optional[str], Optional[str]]:
    """クロスシグナル判定（緩和版）"""
    if relaxation_level == "none":
        # 従来の厳格版
        if latest_data['Buy_Signal_golden_cross'] and latest_data['is_up_trend']:
            return 'Buy', 'Golden Cross'
        elif latest_data['Sell_Signal_dead_cross'] and latest_data['is_down_trend']:
            return 'Sell', 'Dead Cross'
    elif relaxation_level == "moderate":
        # 中程度の緩和：トレンド条件を緩和
        if latest_data['Buy_Signal_golden_cross']:
            return 'Buy', 'Golden Cross (Relaxed)'
        elif latest_data['Sell_Signal_dead_cross']:
            return 'Sell', 'Dead Cross (Relaxed)'
    elif relaxation_level == "high":
        # 高度な緩和：追加条件を削除
        if latest_data['Buy_Signal_golden_cross']:
            return 'Buy', 'Golden Cross (High Relaxed)'
        elif latest_data['Sell_Signal_dead_cross']:
            return 'Sell', 'Dead Cross (High Relaxed)'
    
    return None, None

def check_up_down_signals_relaxed(latest_data: pd.Series, UP_DOWN_PERIODS: List[int], relaxation_level: str = "moderate") -> Tuple[Optional[str], Optional[str]]:
    """上昇下降日数シグナル判定（緩和版）"""
    for period in UP_DOWN_PERIODS:
        if relaxation_level == "none":
            # 従来の厳格版
            if latest_data[f'Buy_Signal_{period}'] and latest_data['is_up_trend']:
                return 'Buy', f'Up for {period} days'
            elif latest_data[f'Sell_Signal_{period}'] and latest_data['is_down_trend']:
                return 'Sell', f'Down for {period} days'
        elif relaxation_level == "moderate":
            # 中程度の緩和：トレンド条件を緩和
            if latest_data[f'Buy_Signal_{period}']:
                return 'Buy', f'Up for {period} days (Relaxed)'
            elif latest_data[f'Sell_Signal_{period}']:
                return 'Sell', f'Down for {period} days (Relaxed)'
        elif relaxation_level == "high":
            # 高度な緩和：より短い期間も考慮
            shorter_periods = [max(1, period - 2) for period in UP_DOWN_PERIODS]  # 期間を短縮
            for short_period in shorter_periods:
                period_col = f'Buy_Signal_{period}' if f'Buy_Signal_{period}' in latest_data.index else None
                if period_col and latest_data[period_col]:
                    return 'Buy', f'Up for {period} days (High Relaxed)'
    
    return None, None

def check_other_signals_relaxed(latest_data: pd.Series, relaxation_level: str = "moderate") -> Tuple[Optional[str], Optional[str]]:
    """その他シグナル判定（緩和版）"""
    if relaxation_level == "none":
        # 従来の厳格版
        if latest_data['Buy_Signal_MA_PPP'] and latest_data['is_up_trend']:
            return 'Buy', 'PPP'
        elif latest_data['Sell_Signal_MA_reverse_PPP'] and latest_data['is_down_trend']:
            return 'Sell', 'Reverse PPP'
        elif latest_data['buy_signal_lower_half'] and latest_data['is_up_trend']:
            return 'Buy', 'Lower Half'
        elif latest_data['sell_signal_Reverse_lower_half'] and latest_data['is_down_trend']:
            return 'Sell', 'Reverse Lower Half'
        elif latest_data['buy_signal_bird_beak'] and latest_data['is_up_trend']:
            return 'Buy', 'Bird Beak'
        elif latest_data['sell_signal_reverse_bird_beak'] and latest_data['is_down_trend']:
            return 'Sell', 'Reverse Bird Beak'
    elif relaxation_level == "moderate":
        # 中程度の緩和：トレンド条件を削除
        if latest_data['Buy_Signal_MA_PPP']:
            return 'Buy', 'PPP (Relaxed)'
        elif latest_data['Sell_Signal_MA_reverse_PPP']:
            return 'Sell', 'Reverse PPP (Relaxed)'
        elif latest_data['buy_signal_lower_half']:
            return 'Buy', 'Lower Half (Relaxed)'
        elif latest_data['sell_signal_Reverse_lower_half']:
            return 'Sell', 'Reverse Lower Half (Relaxed)'
        elif latest_data['buy_signal_bird_beak']:
            return 'Buy', 'Bird Beak (Relaxed)'
        elif latest_data['sell_signal_reverse_bird_beak']:
            return 'Sell', 'Reverse Bird Beak (Relaxed)'
    elif relaxation_level == "high":
        # 高度な緩和：さらに条件を緩和
        # 移動平均のシンプルなクロスオーバーも考慮
        if (latest_data['SMA_5'] > latest_data['SMA_25'] and 
            latest_data['4. close'] > latest_data['SMA_5']):
            return 'Buy', 'Simple MA Cross (High Relaxed)'
        elif (latest_data['SMA_5'] < latest_data['SMA_25'] and 
              latest_data['4. close'] < latest_data['SMA_5']):
            return 'Sell', 'Simple MA Cross Down (High Relaxed)'
        # 従来のシグナルもトレンド条件なしで考慮
        elif latest_data['Buy_Signal_MA_PPP']:
            return 'Buy', 'PPP (High Relaxed)'
        elif latest_data['Sell_Signal_MA_reverse_PPP']:
            return 'Sell', 'Reverse PPP (High Relaxed)'
    
    return None, None

def get_latest_signals_relaxed(kabuData: pd.DataFrame, UP_DOWN_PERIODS: List[int], relaxation_level: str = "moderate") -> Tuple[Optional[str], Optional[str]]:
    """緩和版シグナル取得"""
    latest_data = kabuData.iloc[-1]
    
    # 優先順位に従ってシグナルをチェック
    signal_type, signal_kind = check_cross_signals_relaxed(latest_data, relaxation_level)
    if signal_type is None:
        signal_type, signal_kind = check_up_down_signals_relaxed(latest_data, UP_DOWN_PERIODS, relaxation_level)
    if signal_type is None:
        signal_type, signal_kind = check_other_signals_relaxed(latest_data, relaxation_level)
    
    return signal_type, signal_kind

def run_backtest_with_relaxation(kabuData: pd.DataFrame, relaxation_level: str = "moderate") -> dict:
    """緩和版バックテストの実行"""
    initial_cash = 1000000
    cash = initial_cash
    position = 0
    trades = []
    
    for i in range(max(aiba_trade_method.SMA_PERIODS), len(kabuData)):
        signalType, signalKind = get_latest_signals_relaxed(
            kabuData.iloc[:i+1], 
            aiba_trade_method.UP_DOWN_PERIODS, 
            relaxation_level
        )
        
        if signalType == 'Buy' and cash > 0:
            position = cash / kabuData['4. close'].iloc[i]
            cash = 0
            trades.append({
                'date': kabuData.index[i],
                'action': 'Buy',
                'price': kabuData['4. close'].iloc[i],
                'signal_kind': signalKind
            })
        elif signalType == 'Sell' and position > 0:
            cash = position * kabuData['4. close'].iloc[i]
            position = 0
            trades.append({
                'date': kabuData.index[i],
                'action': 'Sell',
                'price': kabuData['4. close'].iloc[i],
                'signal_kind': signalKind
            })

    final_value = cash + position * kabuData['4. close'].iloc[-1]
    return_rate = (final_value - initial_cash) / initial_cash * 100
    
    return {
        'relaxation_level': relaxation_level,
        'initial_cash': initial_cash,
        'final_value': final_value,
        'return_rate': return_rate,
        'trade_count': len(trades),
        'trades': trades
    }

def analyze_signals_with_relaxation(kabuData: pd.DataFrame, relaxation_levels: List[str]) -> None:
    """各緩和レベルでのシグナル分析"""
    print("\n=== 緩和レベル別シグナル分析 ===")
    
    for level in relaxation_levels:
        print(f"\n--- 緩和レベル: {level} ---")
        signal_counts = {}
        
        for i in range(max(aiba_trade_method.SMA_PERIODS), len(kabuData)):
            signalType, signalKind = get_latest_signals_relaxed(
                kabuData.iloc[:i+1], 
                aiba_trade_method.UP_DOWN_PERIODS, 
                level
            )
            if signalType in ['Buy', 'Sell']:
                key = f"{signalType}_{signalKind}"
                signal_counts[key] = signal_counts.get(key, 0) + 1
        
        if signal_counts:
            print(f"シグナル発生回数 ({level}):")
            for signal, count in signal_counts.items():
                print(f"  {signal}: {count} 回")
        else:
            print(f"シグナル発生なし ({level})")

def main() -> None:
    """メイン処理"""
    print("=== Aibaメソッド緩和版バックテスト ===")
    print("シグナル発生条件を段階的に緩和してテストします。\n")
    
    # サンプルデータの作成
    kabuData = create_trending_sample_data()
    print(f"データ期間: {kabuData.index.min().strftime('%Y-%m-%d')} ～ {kabuData.index.max().strftime('%Y-%m-%d')}")
    print(f"価格範囲: {kabuData['4. close'].min():.2f} ～ {kabuData['4. close'].max():.2f}")
    
    # シグナル計算
    kabuData = aiba_trade_method.calculate_sma(kabuData, aiba_trade_method.SMA_PERIODS)
    kabuData = count_trend_days(kabuData)
    kabuData['Up'] = kabuData['4. close'] > kabuData['1. open']
    kabuData['Down'] = kabuData['4. close'] < kabuData['1. open']
    calculated_kabu_data = calculate_signals(kabuData, aiba_trade_method.UP_DOWN_PERIODS, aiba_trade_method.SMA_PERIODS, aiba_trade_method.CROSS_PERIODS)
    
    # 緩和レベル別テスト
    relaxation_levels = ["none", "moderate", "high"]
    
    # シグナル分析
    analyze_signals_with_relaxation(calculated_kabu_data, relaxation_levels)
    
    # バックテスト実行
    results = []
    for level in relaxation_levels:
        print(f"\n=== バックテスト実行 ({level}) ===")
        result = run_backtest_with_relaxation(calculated_kabu_data, level)
        results.append(result)
        
        print(f"緩和レベル: {level}")
        print(f"初期資金: {result['initial_cash']:,} 円")
        print(f"最終資産: {result['final_value']:,.2f} 円")
        print(f"収益率: {result['return_rate']:+.2f}%")
        print(f"取引回数: {result['trade_count']} 回")
        
        if result['trades']:
            print("主な取引:")
            for trade in result['trades'][:5]:  # 最初の5取引を表示
                date_str = trade['date'].strftime('%Y-%m-%d') if hasattr(trade['date'], 'strftime') else str(trade['date'])
                print(f"  {date_str}: {trade['action']} at {trade['price']:.2f} ({trade['signal_kind']})")
    
    # 比較結果
    print("\n=== 緩和レベル別比較結果 ===")
    for result in results:
        print(f"{result['relaxation_level']:>12}: 収益率{result['return_rate']:+6.2f}%, 取引{result['trade_count']:>3}回")
    
    print("\n緩和版バックテストが完了しました。")

if __name__ == '__main__':
    main()
