import sys
import os

# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Current directory: {current_dir}")

# aiba_trade_methodが存在するディレクトリへの相対パスを追加
module_dir = os.path.join(current_dir, '..', 'src')
print(f"Module directory: {module_dir}")
sys.path.append(module_dir)

from dotenv import load_dotenv
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

from aiba_trade_method import CROSS_PERIODS, SMA_PERIODS, UP_DOWN_PERIODS, calculate_sma, get_latest_signals
from calculaters.signals import calculate_signals
from calculaters.trends import count_trend_days
from get_stock_data.get_alpha_vantage import get_stock_data

# Alpha VantageのAPIキーを設定
load_dotenv()
api_key = os.getenv("API_KEY")

# 過去の株価データを取得
kabuData = get_stock_data('SPY', api_key)

# 提供されたコードを使ってシグナルを計算
kabuData = calculate_sma(kabuData.copy(), SMA_PERIODS)
kabuData = count_trend_days(kabuData.copy())
kabuData = calculate_signals(kabuData.copy(), UP_DOWN_PERIODS, SMA_PERIODS, CROSS_PERIODS)

# デバッグ用にカラムを表示
print(kabuData.columns)

# 'Down'カラムが存在するか確認
if 'Down' not in kabuData.columns:
    print("Error: 'Down' column is missing")
    
# バックテストの実行
initial_cash = 1000000  # 初期資金
cash = initial_cash
position = 0  # 保有株数
kabuData['Portfolio Value'] = np.nan

for i in range(1, len(kabuData)):
    signalType, signalKind = get_latest_signals(kabuData.iloc[:i], UP_DOWN_PERIODS)
    
    if signalType == 'Buy' and cash > 0:
        position = cash / kabuData['4. close'].iloc[i]
        cash = 0
        print(f"Buy at {kabuData.index[i]}: {kabuData['4. close'].iloc[i]}")
    elif signalType == 'Sell' and position > 0:
        cash = position * kabuData['4. close'].iloc[i]
        position = 0
        print(f"Sell at {kabuData.index[i]}: {kabuData['4. close'].iloc[i]}")
    
    kabuData['Portfolio Value'].iloc[i] = cash + position * kabuData['4. close'].iloc[i]

# バックテスト結果の表示
final_value = cash + position * kabuData['4. close'].iloc[-1]
print(f"Initial Cash: {initial_cash}")
print(f"Final Portfolio Value: {final_value}")
print(f"Return: {(final_value - initial_cash) / initial_cash * 100:.2f}%")

# ポートフォリオ価値のプロット
plt.figure(figsize=(12, 5))
plt.plot(kabuData.index, kabuData['Portfolio Value'], label='Portfolio Value')
plt.title('Portfolio Value Over Time')
plt.xlabel('Date')
plt.ylabel('Portfolio Value')
plt.legend()
plt.grid()
plt.show()
