import pandas as pd
from .get_yahoo_finance import get_yfinance_stock_data
from ..helpers.trend_logic import standardize_headers

def get_stock_data(symbol: str, api_key: str = None) -> pd.DataFrame:
    data = get_yfinance_stock_data(symbol)
    if data is None or data.empty:
        return None
    try:
        return standardize_headers(data)
    except Exception as e:
        print(f"Error standardizing headers for {symbol}: {e}")
        return None
