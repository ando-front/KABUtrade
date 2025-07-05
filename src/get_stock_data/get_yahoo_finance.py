import os
from dotenv import load_dotenv
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import mplfinance as mpf
from typing import List
from datetime import datetime, timedelta
import time
import random
from typing import Optional
import hashlib

def load_api_key() -> str:
    load_dotenv()
    return os.getenv("API_KEY")

def get_yfinance_stock_data(
    symbol: str, 
    period: str = "max", 
    interval: str = "1d",
    max_retries: int = 5, 
    base_retry_delay: int = 60
) -> Optional[pd.DataFrame]:
    """
    yfinanceを使用して株価データを取得（レート制限対策強化版＋キャッシュ機能）
    
    Args:
        symbol: 株式シンボル
        period: データ期間 ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
        interval: データ間隔 ("1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo")
        max_retries: 最大リトライ回数
        base_retry_delay: リトライ間隔の基準値（秒）
    
    Returns:
        pd.DataFrame: 株価データ（Open, High, Low, Close, Volume列を含む）
    """
    # キャッシュファイル名生成
    cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data_cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_key = f"{symbol}_{period}_{interval}"
    cache_hash = hashlib.md5(cache_key.encode()).hexdigest()
    cache_path = os.path.join(cache_dir, f"{cache_hash}.csv")

    # キャッシュがあれば先に読む
    if os.path.exists(cache_path):
        try:
            print(f"Loading cached data for {symbol} from {cache_path}")
            data = pd.read_csv(cache_path, index_col=0, parse_dates=True)
            if not data.empty:
                return data
        except Exception as e:
            print(f"Failed to load cache for {symbol}: {e}")

    # rate limit回避のための事前待機
    random_delay = random.uniform(2, 8)
    print(f"Pre-request delay: {random_delay:.1f} seconds")
    time.sleep(random_delay)
    
    for attempt in range(max_retries):
        try:
            print(f"Attempting to fetch data for {symbol} (attempt {attempt + 1}/{max_retries})")
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval, auto_adjust=True, prepost=True)
            if not data.empty:
                print(f"Successfully retrieved {len(data)} records for {symbol}")
                # キャッシュ保存
                try:
                    data.to_csv(cache_path)
                    print(f"Saved data to cache: {cache_path}")
                except Exception as e:
                    print(f"Failed to save cache for {symbol}: {e}")
                return data
            else:
                print(f"Attempt {attempt + 1}: No data available for symbol {symbol}")
        except Exception as e:
            error_msg = str(e)
            print(f"Attempt {attempt + 1} failed for {symbol}: {error_msg}")
            
            # レート制限エラーの場合は長めの待機時間
            if "rate limit" in error_msg.lower() or "too many requests" in error_msg.lower():
                if attempt < max_retries - 1:
                    # より保守的な指数バックオフ: 60, 120, 240, 480秒
                    retry_delay = base_retry_delay * (2 ** attempt)
                    print(f"Rate limit detected. Waiting {retry_delay} seconds before retry...")
                    time.sleep(retry_delay)
                continue
        if attempt < max_retries - 1:
            retry_delay = base_retry_delay + (attempt * 30)  # より長い待機時間
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    print(f"Failed to retrieve data for {symbol} after {max_retries} attempts.")
    return None

def get_stock_info(symbol: str) -> dict:
    """
    株式の基本情報を取得
    
    Args:
        symbol: 株式シンボル
    
    Returns:
        dict: 株式の基本情報
    """
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info
    except Exception as e:
        print(f"Error getting info for {symbol}: {e}")
        return {}

def get_stock_data_by_date_range(
    symbol: str, 
    start_date: str, 
    end_date: str,
    max_retries: int = 3
) -> Optional[pd.DataFrame]:
    """
    指定した日付範囲の株価データを取得
    
    Args:
        symbol: 株式シンボル
        start_date: 開始日 (YYYY-MM-DD形式)
        end_date: 終了日 (YYYY-MM-DD形式)
        max_retries: 最大リトライ回数
    
    Returns:
        pd.DataFrame: 株価データ
    """
    for attempt in range(max_retries):
        try:
            data = yf.download(symbol, start=start_date, end=end_date, auto_adjust=True)
            if not data.empty:
                print(f"Successfully retrieved {len(data)} records for {symbol} from {start_date} to {end_date}")
                return data
            else:
                print(f"Attempt {attempt + 1}: No data for {symbol} in date range")
                
        except Exception as e:
            print(f"Attempt {attempt + 1}: Failed to get data for {symbol}. Reason: {e}")
            
        if attempt < max_retries - 1:
            time.sleep(2)  # リトライ間隔
    
    print(f"Failed to retrieve data for {symbol} after {max_retries} attempts.")
    return None

def plot_stock_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    fig = plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(len(symbol), 1, figure=fig)
    all_data = pd.DataFrame()
# TODO
# plot_stock_dataを呼ぶかget_stock_dataを呼ぶか決めて修正数r
# ここで銘柄をリストで渡して繰り返し処理するのではなく、メイン関数で渡して銘柄別の集計がわかるようにする
    # for i, symbol in enumerate(symbols):
    data = get_stock_data(symbol, start, end)
    data['Symbol'] = symbol  # シンボル列を追加
    all_data = pd.concat([all_data, data])
    # ap = mpf.make_addplot(data['Close'].rolling(window=5).mean())  # 5日移動平均
    # mpf.plot(data, type='candle', addplot=ap, title=f'{symbol} Close Price with Moving Averages')

    # plt.tight_layout()
    # plt.show()
    return all_data
