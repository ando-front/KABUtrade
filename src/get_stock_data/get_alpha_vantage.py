import pandas as pd
from typing import Optional
from .get_yahoo_finance import get_yfinance_stock_data
from ..helpers.trend_logic import standardize_headers

def get_stock_data(
    symbol: str, 
    api_key: str = None,  # 後方互換性のため保持（使用しない）
    period: str = "max",
    interval: str = "1d"
) -> Optional[pd.DataFrame]:
    """
    yfinanceを使用して株価データを取得（Alpha Vantage APIの代替）
    
    Args:
        symbol: 株式シンボル
        api_key: 非推奨（後方互換性のため保持）
        period: データ期間
        interval: データ間隔
    
    Returns:
        pd.DataFrame: Alpha Vantage形式に標準化された株価データ
    """
    try:
        # yfinanceからデータ取得
        data = get_yfinance_stock_data(symbol, period=period, interval=interval)
        
        if data is None or data.empty:
            print(f"Warning: No data retrieved for symbol {symbol}")
            return pd.DataFrame()
        
        # Alpha Vantage形式のカラム名に標準化
        standardized_data = standardize_headers(data)
        
        print(f"Successfully retrieved {len(standardized_data)} records for {symbol}")
        return standardized_data
        
    except Exception as e:
        print(f"Error getting data for {symbol}: {e}")
        return pd.DataFrame()

# 旧関数名との互換性を保持
def get_alpha_vantage_data(symbol: str, api_key: str = None) -> Optional[pd.DataFrame]:
    """
    非推奨: get_stock_dataを使用してください
    """
    print("Warning: get_alpha_vantage_data is deprecated. Use get_stock_data instead.")
    return get_stock_data(symbol, api_key)
