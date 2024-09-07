import pandas as pd


def count_trend_days(kabuData: pd.DataFrame) -> pd.DataFrame:
    kabuData['up_trend_count'] = 0
    kabuData['down_trend_count'] = 0
    kabuData = kabuData.reset_index(drop=True)

    for i in range(2, len(kabuData)):
        kabuData.at[i, 'up_trend_count'] = calculate_up_trend(kabuData, i)
        kabuData.at[i, 'down_trend_count'] = calculate_down_trend(kabuData, i)

    kabuData['is_up_trend'] = kabuData['up_trend_count'] >= 60
    kabuData['is_down_trend'] = kabuData['down_trend_count'] >= 60

    return kabuData

def calculate_up_trend(kabuData: pd.DataFrame, i: int) -> int:
    if kabuData.iloc[i]['SMA_5'] < kabuData.iloc[i]['SMA_20'] and kabuData.iloc[i]['SMA_5'] < kabuData.iloc[i]['4. close']:
        return kabuData.at[i-1, 'up_trend_count'] + 1
    elif kabuData.iloc[i]['SMA_20'] < kabuData.iloc[i]['SMA_5'] and kabuData.iloc[i]['SMA_20'] < kabuData.iloc[i]['4. close'] and kabuData.iloc[i]['SMA_20'] > kabuData.iloc[i-1]['SMA_20']:
        return kabuData.at[i-1, 'up_trend_count'] + 1
    elif kabuData.iloc[i]['SMA_60'] < kabuData.iloc[i]['SMA_5'] and kabuData.iloc[i]['SMA_60'] < kabuData.iloc[i]['4. close'] and kabuData.iloc[i]['SMA_20'] > kabuData.iloc[i-1]['SMA_20'] and kabuData.iloc[i]['SMA_60'] > kabuData.iloc[i-1]['SMA_60']:
        return kabuData.at[i-1, 'up_trend_count'] + 1
    elif kabuData.iloc[i]['SMA_60'] < kabuData.iloc[i]['SMA_5'] and kabuData.iloc[i]['SMA_20'] < kabuData.iloc[i-1]['SMA_20'] and kabuData.iloc[i]['SMA_60'] > kabuData.iloc[i-1]['SMA_60'] and kabuData.iloc[i]['4. close'] > kabuData.iloc[i]['SMA_60']:
        return kabuData.at[i-1, 'up_trend_count']
    else:
        return 0

def calculate_down_trend(kabuData: pd.DataFrame, i: int) -> int:
    if kabuData.loc[i, 'SMA_20'] < kabuData.loc[i, 'SMA_5'] and kabuData.loc[i, '4. close'] < kabuData.loc[i, 'SMA_5']:
        return kabuData.loc[i-1, 'down_trend_count'] + 1
    elif kabuData.loc[i, 'SMA_5'] < kabuData.loc[i, 'SMA_20'] and kabuData.loc[i, 'SMA_20'] < kabuData.loc[i-1, 'SMA_20'] and kabuData.loc[i, '4. close'] < kabuData.loc[i, 'SMA_20']:
        return kabuData.loc[i-1, 'down_trend_count'] + 1
    elif kabuData.loc[i, 'SMA_5'] < kabuData.loc[i, 'SMA_60'] and kabuData.loc[i, 'SMA_20'] < kabuData.loc[i-1, 'SMA_20'] and kabuData.loc[i, 'SMA_60'] < kabuData.loc[i-1, 'SMA_60'] and kabuData.loc[i, '4. close'] < kabuData.loc[i, 'SMA_60']:
        return kabuData.loc[i-1, 'down_trend_count'] + 1
    elif kabuData.loc[i, 'SMA_5'] < kabuData.loc[i, 'SMA_60'] and kabuData.loc[i, 'SMA_20'] > kabuData.loc[i-1, 'SMA_20'] and kabuData.loc[i, 'SMA_60'] < kabuData.loc[i-1, 'SMA_60'] and kabuData.loc[i, '4. close'] < kabuData.loc[i, 'SMA_60']:
        return kabuData.loc[i-1, 'down_trend_count']
    else:
        return 0

