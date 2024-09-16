from datetime import datetime, timedelta
import sys
import os
import numpy as np
import pandas as pd
import logging
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from helpers.trend_logic import standardize_headers
from get_stock_data.get_yahoo_finance import get_yfinance_stock_data
import aiba_trade_method
from calculaters.signals import calculate_signals
from calculaters.trends import count_trend_days
from get_stock_data.get_alpha_vantage import get_stock_data

# ロギングの設定
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

# Alpha VantageのAPIキーを設定
load_dotenv()
api_key = os.getenv("API_KEY")

def backtest_signals(kabuData: pd.DataFrame) -> pd.DataFrame:
    kabuData = aiba_trade_method.calculate_sma(kabuData, aiba_trade_method.SMA_PERIODS)
    kabuData = count_trend_days(kabuData)
    kabuData['Up'] = kabuData['4. close'] > kabuData['1. open']
    kabuData['Down'] = kabuData['4. close'] < kabuData['1. open']
    calculated_kabu_data = calculate_signals(kabuData, aiba_trade_method.UP_DOWN_PERIODS, aiba_trade_method.SMA_PERIODS, aiba_trade_method.CROSS_PERIODS)
    print("calculated_kabu_data",calculated_kabu_data)  # デバッグ用にシグナルの計算結果を出力
    return calculated_kabu_data

def run_backtest(kabuData: pd.DataFrame) -> None:
    initial_cash = 1000000  # 初期資金
    cash = initial_cash
    position = 0  # 保有株数
    kabuData['Portfolio Value'] = np.nan

    for i in range(1, len(kabuData)):
        signalType, signalKind = aiba_trade_method.get_latest_signals(kabuData.iloc[:i], aiba_trade_method.UP_DOWN_PERIODS)
        
        if signalType == 'Buy' and cash > 0:
            position = cash / kabuData['4. close'].iloc[i]
            cash = 0
            print(f"Buy at {kabuData.index[i]}: {kabuData['4. close'].iloc[i]}")
        elif signalType == 'Sell' and position > 0:
            cash = position * kabuData['4. close'].iloc[i]
            position = 0
            print(f"Sell at {kabuData.index[i]}: {kabuData['4. close'].iloc[i]}")
        
        kabuData.loc[i, 'Portfolio Value'] = cash + position * kabuData['4. close'].iloc[i]

    # バックテスト結果の表示
    final_value = cash + position * kabuData['4. close'].iloc[-1]
    print(f"Initial Cash: {initial_cash}")
    print(f"Final Portfolio Value: {final_value}")
    print(f"Return: {(final_value - initial_cash) / initial_cash * 100:.2f}%")

def main() -> None:
    symbols_NY = ["SPY", "AAPL"]
    for symbol in symbols_NY:
        kabuData: pd.DataFrame = get_stock_data(symbol, api_key)
        kabuData: pd.DataFrame = standardize_headers(kabuData) # 株価のヘッダー名統一
        calculated_kabu_data = backtest_signals(kabuData)
        run_backtest(calculated_kabu_data)

    symbols = ["^N225", "7203.T", "7011.T"]
    for symbol in symbols:
        kabuData: pd.DataFrame = get_yfinance_stock_data(symbol)
        kabuData: pd.DataFrame = standardize_headers(kabuData) # 株価のヘッダー名統一
        calculated_kabu_data = backtest_signals(kabuData)
        run_backtest(calculated_kabu_data)

if __name__ == '__main__':
    main()
