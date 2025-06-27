import pandas as pd
from typing import List, Union

def standardize_headers(kabuData: pd.DataFrame) -> pd.DataFrame:
    # MultiIndexをフラット化し、列名を調整
    if isinstance(kabuData.columns, pd.MultiIndex):
        # 最初のレベルの列名を取得
        kabuData.columns = kabuData.columns.get_level_values(0)

    # ヘッダー名のマッピング
    header_mapping = {
        'Open': '1. open',
        'High': '2. high',
        'Low': '3. low',
        'Close': '4. close',
        'Volume': 'Volume'
    }
    # ヘッダー名を統一
    kabuData = kabuData.rename(columns=header_mapping)

    return kabuData

def is_buy_signal(kabuData: pd.DataFrame, period: int) -> pd.Series:
    return (
        (kabuData['Down'].rolling(window=period).sum() == period) | 
        ((kabuData['4. close'] > kabuData['SMA_75']) & 
         (kabuData['4. close'].shift(1) < kabuData['SMA_75'].shift(1)) & 
         (kabuData['Up']))
    )

def is_sell_signal(kabuData: pd.DataFrame, period: int) -> pd.Series:
    return (
        (kabuData['Up'].rolling(window=period).sum() == period) |
        ((kabuData['4. close'] < kabuData['SMA_75']) & 
         (kabuData['4. close'].shift(1) > kabuData['SMA_75'].shift(1)) & 
         (kabuData['Down']))
    )

def is_pampakapam(row: pd.Series, SMA_PERIODS: List[int], is_buy_signal: bool) -> bool:
    if is_buy_signal:
        return all(row[f'SMA_{SMA_PERIODS[i]}'] > row[f'SMA_{SMA_PERIODS[i+1]}'] for i in range(len(SMA_PERIODS)-1))
    else:
        return all(row[f'SMA_{SMA_PERIODS[i]}'] < row[f'SMA_{SMA_PERIODS[i+1]}'] for i in range(len(SMA_PERIODS)-1))

def is_golden_cross(kabuData: pd.DataFrame, CROSS_PERIODS: List[int]) -> pd.Series:
    return (kabuData[f'SMA_{CROSS_PERIODS[0]}'] > kabuData[f'SMA_{CROSS_PERIODS[1]}']) & \
           (kabuData[f'SMA_{CROSS_PERIODS[0]}'].shift(1) < kabuData[f'SMA_{CROSS_PERIODS[1]}'].shift(1))

def is_dead_cross(kabuData: pd.DataFrame, CROSS_PERIODS: List[int]) -> pd.Series:
    return (kabuData[f'SMA_{CROSS_PERIODS[0]}'] < kabuData[f'SMA_{CROSS_PERIODS[1]}']) & \
           (kabuData[f'SMA_{CROSS_PERIODS[0]}'].shift(1) > kabuData[f'SMA_{CROSS_PERIODS[1]}'].shift(1))

def is_trend(kabuData: pd.DataFrame, column: str, direction: str) -> pd.Series:
    if direction == 'up':
        return kabuData[column].diff() > 0
    elif direction == 'down':
        return kabuData[column].diff() < 0

def is_break_5d(kabuData: pd.DataFrame) -> pd.Series:
    return (kabuData['4. close'] > kabuData['SMA_5']) & \
           (kabuData['4. close'] - kabuData['1. open'] > (kabuData['4. close'] - kabuData['SMA_5']) / 2)

def is_break_down_5d(kabuData: pd.DataFrame) -> pd.Series:
    return (kabuData['4. close'] < kabuData['SMA_5']) & \
           (kabuData['1. open'] - kabuData['4. close'] > (kabuData['SMA_5'] - kabuData['4. close']) / 2)
