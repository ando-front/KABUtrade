"""
Aibaメソッド超シンプル緩和版
トレンド条件を完全に削除してシグナル発生を確認します。
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

def create_simple_trending_data() -> pd.DataFrame:
    """確実にシグナルが発生するシンプルなデータを作成（400日間）"""
    start_date = datetime.now() - timedelta(days=400)
    dates = pd.date_range(start=start_date, periods=400, freq='D')
    
    base_price = 100
    
    # 明確なトレンドを作る
    prices = []
    opens = []
    
    for i in range(400):
        if i < 200:
            # 下降トレンド
            price = base_price - (i * 0.2)
            open_price = price + np.random.uniform(-0.5, 0.5)
        else:
            # 上昇トレンド
            price = prices[199] + ((i - 199) * 0.3)
            open_price = price + np.random.uniform(-0.5, 0.5)
        
        prices.append(price)
        opens.append(open_price)
    
    # 高値、安値を設定
    highs = [max(p, o) * 1.02 for p, o in zip(prices, opens)]
    lows = [min(p, o) * 0.98 for p, o in zip(prices, opens)]
    
    volumes = [50000] * 400
    
    data = pd.DataFrame({
        '1. open': opens,
        '2. high': highs,
        '3. low': lows,
        '4. close': prices,
        '5. volume': volumes
    }, index=dates)
    
    return data

def get_signals_super_relaxed(latest_data: pd.Series) -> Tuple[Optional[str], Optional[str]]:
    """超緩和版シグナル判定（トレンド条件なし）"""
    
    # 1. ゴールデンクロス・デッドクロス（トレンド条件なし）
    if latest_data.get('Buy_Signal_golden_cross', False):
        return 'Buy', 'Golden Cross (No Trend)'
    elif latest_data.get('Sell_Signal_dead_cross', False):
        return 'Sell', 'Dead Cross (No Trend)'
    
    # 2. PPPパターン（トレンド条件なし）
    elif latest_data.get('Buy_Signal_MA_PPP', False):
        return 'Buy', 'PPP (No Trend)'
    elif latest_data.get('Sell_Signal_MA_reverse_PPP', False):
        return 'Sell', 'Reverse PPP (No Trend)'
    
    # 3. 連続上昇下降（トレンド条件なし）
    elif latest_data.get('Buy_Signal_9', False):
        return 'Buy', 'Up 9 days (No Trend)'
    elif latest_data.get('Sell_Signal_9', False):
        return 'Sell', 'Down 9 days (No Trend)'
    elif latest_data.get('Buy_Signal_13', False):
        return 'Buy', 'Up 13 days (No Trend)'
    elif latest_data.get('Sell_Signal_13', False):
        return 'Sell', 'Down 13 days (No Trend)'
    
    # 4. その他のパターン（トレンド条件なし）
    elif latest_data.get('buy_signal_lower_half', False):
        return 'Buy', 'Lower Half (No Trend)'
    elif latest_data.get('sell_signal_Reverse_lower_half', False):
        return 'Sell', 'Reverse Lower Half (No Trend)'
    elif latest_data.get('buy_signal_bird_beak', False):
        return 'Buy', 'Bird Beak (No Trend)'
    elif latest_data.get('sell_signal_reverse_bird_beak', False):
        return 'Sell', 'Reverse Bird Beak (No Trend)'
    
    # 5. シンプルな移動平均クロスオーバー
    elif (latest_data.get('SMA_5', 0) > latest_data.get('SMA_25', 0) and 
          latest_data.get('4. close', 0) > latest_data.get('SMA_5', 0)):
        return 'Buy', 'Simple MA Cross Up'
    elif (latest_data.get('SMA_5', 0) < latest_data.get('SMA_25', 0) and 
          latest_data.get('4. close', 0) < latest_data.get('SMA_5', 0)):
        return 'Sell', 'Simple MA Cross Down'
    
    return None, None

def run_super_relaxed_backtest(kabuData: pd.DataFrame) -> dict:
    """超緩和版バックテスト"""
    initial_cash = 1000000
    cash = initial_cash
    position = 0
    trades = []
    portfolio_values = []
    
    # SMA計算に必要な最小期間を確保
    start_index = max(aiba_trade_method.SMA_PERIODS)
    
    for i in range(start_index, len(kabuData)):
        latest_data = kabuData.iloc[i]
        signalType, signalKind = get_signals_super_relaxed(latest_data)
        
        current_price = latest_data['4. close']
        
        if signalType == 'Buy' and cash > 0:
            position = cash / current_price
            cash = 0
            trades.append({
                'date': latest_data.name,
                'action': 'Buy',
                'price': current_price,
                'signal_kind': signalKind
            })
            print(f"買い注文執行: {latest_data.name} at {current_price:.2f} ({signalKind})")
        elif signalType == 'Sell' and position > 0:
            cash = position * current_price
            position = 0
            trades.append({
                'date': latest_data.name,
                'action': 'Sell',
                'price': current_price,
                'signal_kind': signalKind
            })
            print(f"売り注文執行: {latest_data.name} at {current_price:.2f} ({signalKind})")
        
        # ポートフォリオ価値を記録
        portfolio_value = cash + position * current_price
        portfolio_values.append(portfolio_value)
    
    final_value = cash + position * kabuData['4. close'].iloc[-1]
    return_rate = (final_value - initial_cash) / initial_cash * 100
    
    return {
        'initial_cash': initial_cash,
        'final_value': final_value,
        'return_rate': return_rate,
        'trade_count': len(trades),
        'trades': trades,
        'portfolio_values': portfolio_values
    }

def analyze_all_signals(kabuData: pd.DataFrame) -> None:
    """全シグナルの発生状況を分析"""
    print("\n=== 全シグナル発生状況 ===")
    
    signal_columns = [col for col in kabuData.columns if 'Signal' in col or 'signal' in col]
    
    for col in signal_columns:
        true_count = kabuData[col].sum()
        if true_count > 0:
            print(f"{col}: {true_count} 回発生")
            # 発生日を表示
            signal_dates = kabuData[kabuData[col]].index
            print(f"  発生日: {', '.join([d.strftime('%m-%d') if hasattr(d, 'strftime') else str(d) for d in signal_dates[:5]])}")
            if len(signal_dates) > 5:
                print(f"  ... 他{len(signal_dates)-5}回")

def main() -> None:
    """メイン処理"""
    print("=== Aibaメソッド超シンプル緩和版バックテスト ===")
    print("トレンド条件を完全に削除してシグナル発生を確認します。\n")
    
    # シンプルなテストデータの作成
    kabuData = create_simple_trending_data()
    print(f"データ期間: {kabuData.index.min().strftime('%Y-%m-%d')} ～ {kabuData.index.max().strftime('%Y-%m-%d')}")
    print(f"価格範囲: {kabuData['4. close'].min():.2f} ～ {kabuData['4. close'].max():.2f}")
    
    # 価格トレンドの確認
    start_price = kabuData['4. close'].iloc[0]
    mid_price = kabuData['4. close'].iloc[len(kabuData)//2]
    end_price = kabuData['4. close'].iloc[-1]
    
    print(f"価格推移: 開始{start_price:.1f} → 中間{mid_price:.1f} → 終了{end_price:.1f}")
    print(f"前半変化: {(mid_price-start_price)/start_price*100:+.1f}%")
    print(f"後半変化: {(end_price-mid_price)/mid_price*100:+.1f}%")
    
    # シグナル計算
    print("\nシグナルを計算中...")
    kabuData = aiba_trade_method.calculate_sma(kabuData, aiba_trade_method.SMA_PERIODS)
    kabuData = count_trend_days(kabuData)
    kabuData['Up'] = kabuData['4. close'] > kabuData['1. open']
    kabuData['Down'] = kabuData['4. close'] < kabuData['1. open']
    calculated_kabu_data = calculate_signals(kabuData, aiba_trade_method.UP_DOWN_PERIODS, aiba_trade_method.SMA_PERIODS, aiba_trade_method.CROSS_PERIODS)
    
    # 全シグナルの分析
    analyze_all_signals(calculated_kabu_data)
    
    # 超緩和版バックテスト実行
    print("\n=== 超緩和版バックテスト実行 ===")
    result = run_super_relaxed_backtest(calculated_kabu_data)
    
    print(f"初期資金: {result['initial_cash']:,} 円")
    print(f"最終資産: {result['final_value']:,.2f} 円")
    print(f"収益率: {result['return_rate']:+.2f}%")
    print(f"取引回数: {result['trade_count']} 回")
    
    if result['trades']:
        print("\n=== 取引履歴 ===")
        for trade in result['trades']:
            date_str = trade['date'].strftime('%Y-%m-%d') if hasattr(trade['date'], 'strftime') else str(trade['date'])
            print(f"{date_str}: {trade['action']} at {trade['price']:.2f} ({trade['signal_kind']})")
    
    # シグナル発生頻度の分析
    print("\n=== シグナル発生頻度分析 ===")
    start_index = max(aiba_trade_method.SMA_PERIODS)
    total_days = len(calculated_kabu_data) - start_index
    signal_days = 0
    
    print(f"分析開始インデックス: {start_index}")
    print(f"データ総数: {len(calculated_kabu_data)}")
    
    for i in range(start_index, len(calculated_kabu_data)):
        latest_data = calculated_kabu_data.iloc[i]
        signalType, signalKind = get_signals_super_relaxed(latest_data)
        if signalType:
            signal_days += 1
            print(f"  シグナル発生: {i}日目 - {signalType} ({signalKind})")
    
    print(f"総取引可能日数: {total_days} 日")
    print(f"シグナル発生日数: {signal_days} 日")
    if total_days > 0:
        print(f"シグナル発生率: {signal_days/total_days*100:.1f}%")
    
    print("\n緩和版バックテストが完了しました。")

if __name__ == '__main__':
    main()
