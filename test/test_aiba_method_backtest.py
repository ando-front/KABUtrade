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
from src.get_stock_data.get_yahoo_finance import get_yfinance_stock_data
from src import aiba_trade_method
from src.calculaters.signals import calculate_signals
from src.calculaters.trends import count_trend_days
from src.get_stock_data.get_alpha_vantage import get_stock_data

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
    # プロジェクトルートからsymbolsファイルの絶対パスを取得
    symbols_ny_path = os.path.join(project_root, "src/symbols/symbols_NY.csv")
    symbols_jp_path = os.path.join(project_root, "src/symbols/symbols_JP.csv")

    print("Starting backtest with very conservative rate limiting...")
    print("Pre-emptive wait of 15 minutes to ensure clean start and rate limit reset...")
    print("If this takes too long, you can interrupt with Ctrl+C and try again later.")
    time.sleep(900)  # 15分待機でrate limitリセットを期待
    
    # NYシンボルの処理（最初の1つだけテスト）
    symbols_NY = pd.read_csv(symbols_ny_path)['symbol'].tolist()[:1]  # テスト用に1つに減らす
    for i, symbol in enumerate(symbols_NY):
        print(f"Processing NY symbol {i+1}/{len(symbols_NY)}: {symbol}")
        try:
            # より保守的な待機時間（rate limit対策）
            if i == 0:
                print("Initial wait of 30 seconds to avoid rate limits...")
                time.sleep(30)
            elif i > 0:
                print("Waiting 120 seconds to avoid rate limits...")
                time.sleep(120)
                
            # yfinanceを直接使用してテスト（より保守的な設定）
            print(f"Fetching data directly for {symbol}...")
            kabuData = get_yfinance_stock_data(symbol, period="1y", max_retries=3, base_retry_delay=60)
            
            if kabuData is None or kabuData.empty:
                print(f"Warning: No data retrieved for symbol {symbol}. Skipping...")
                continue
            
            # データの標準化
            kabuData = standardize_headers(kabuData)
                
            # 過去1年間のデータフィルタリング
            x_year_ago = datetime.now() - timedelta(days=365 * 1)
            kabuData.index = pd.to_datetime(kabuData.index)
            kabuData = kabuData[kabuData.index >= x_year_ago.strftime('%Y-%m-%d')]
            
            if kabuData.empty:
                print(f"Warning: No data in specified date range for {symbol}. Skipping...")
                continue
                
            print(f"Data loaded for {symbol}: {len(kabuData)} records")
            print(f"Date range: {kabuData.index.min()} to {kabuData.index.max()}")
            print(f"Columns: {list(kabuData.columns)}")
            
            calculated_kabu_data = backtest_signals(kabuData)
            run_backtest(calculated_kabu_data)
            print(f"Completed analysis for {symbol}")
            
        except Exception as e:
            print(f"Error processing NY symbol {symbol}: {e}")
            import traceback
            traceback.print_exc()
            continue

    print("NY symbols processing completed. Waiting before JP symbols...")
    time.sleep(180)  # 3分待機（より保守的）

    # JPシンボルの処理（最初の1つだけテスト）
    symbols = pd.read_csv(symbols_jp_path)['symbol'].tolist()[:1]  # テスト用に1つに減らす
    for i, symbol in enumerate(symbols):
        print(f"Processing JP symbol {i+1}/{len(symbols)}: {symbol}")
        try:
            # 日本株のシンボル調整
            if ".T" not in symbol:
                symbol = symbol + ".T"
                
            if i == 0:
                print("Initial wait of 30 seconds...")
                time.sleep(30)
            elif i > 0:
                print("Waiting 120 seconds to avoid rate limits...")
                time.sleep(120)
                
            # yfinanceを直接使用してテスト（より保守的な設定）
            print(f"Fetching data directly for {symbol}...")
            kabuData = get_yfinance_stock_data(symbol, period="2y", max_retries=3, base_retry_delay=60)
            
            if kabuData is None or kabuData.empty:
                print(f"Warning: No data retrieved for symbol {symbol}. Skipping...")
                continue
            
            # データの標準化
            kabuData = standardize_headers(kabuData)
                
            # 過去2年間のデータフィルタリング  
            x_year_ago = datetime.now() - timedelta(days=365 * 2)
            kabuData.index = pd.to_datetime(kabuData.index)
            kabuData = kabuData[kabuData.index >= x_year_ago.strftime('%Y-%m-%d')]
            
            if kabuData.empty:
                print(f"Warning: No data in specified date range for {symbol}. Skipping...")
                continue
                
            print(f"Data loaded for {symbol}: {len(kabuData)} records")
            print(f"Date range: {kabuData.index.min()} to {kabuData.index.max()}")
            print(f"Columns: {list(kabuData.columns)}")
            
            calculated_kabu_data = backtest_signals(kabuData)
            run_backtest(calculated_kabu_data)
            print(f"Completed analysis for {symbol}")
            
        except Exception as e:
            print(f"Error processing JP symbol {symbol}: {e}")
            import traceback
            traceback.print_exc()
            continue

if __name__ == '__main__':
    main()
