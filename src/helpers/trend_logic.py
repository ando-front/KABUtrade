
def is_buy_signal(kabuData, period):
    return (
        (kabuData['Down'].rolling(window=period).sum() == period) | 
        ((kabuData['4. close'] > kabuData['SMA_75']) & 
         (kabuData['4. close'].shift(1) < kabuData['SMA_75'].shift(1)) & 
         (kabuData['Up']))
    )

def is_sell_signal(kabuData, period):
    return (
        (kabuData['Up'].rolling(window=period).sum() == period) |
        ((kabuData['4. close'] < kabuData['SMA_75']) & 
         (kabuData['4. close'].shift(1) > kabuData['SMA_75'].shift(1)) & 
         (kabuData['Down']))
    )

def is_pampakapam(row, SMA_PERIODS, is_buy_signal):
    if is_buy_signal:
        return all(row[f'SMA_{SMA_PERIODS[i]}'] > row[f'SMA_{SMA_PERIODS[i+1]}'] for i in range(len(SMA_PERIODS)-1))
    else:
        return all(row[f'SMA_{SMA_PERIODS[i]}'] < row[f'SMA_{SMA_PERIODS[i+1]}'] for i in range(len(SMA_PERIODS)-1))

def is_golden_cross(kabuData, CROSS_PERIODS):
    return (kabuData[f'SMA_{CROSS_PERIODS[0]}'] > kabuData[f'SMA_{CROSS_PERIODS[1]}']) & \
           (kabuData[f'SMA_{CROSS_PERIODS[0]}'].shift(1) < kabuData[f'SMA_{CROSS_PERIODS[1]}'].shift(1))

def is_dead_cross(kabuData, CROSS_PERIODS):
    return (kabuData[f'SMA_{CROSS_PERIODS[0]}'] < kabuData[f'SMA_{CROSS_PERIODS[1]}']) & \
           (kabuData[f'SMA_{CROSS_PERIODS[0]}'].shift(1) > kabuData[f'SMA_{CROSS_PERIODS[1]}'].shift(1))

def is_trend(kabuData, column, direction):
    if direction == 'up':
        return kabuData[column].diff() > 0
    elif direction == 'down':
        return kabuData[column].diff() < 0

def is_break_5d(kabuData):
    return (kabuData['4. close'] > kabuData['SMA_5']) & \
           (kabuData['4. close'] - kabuData['1. open'] > (kabuData['4. close'] - kabuData['SMA_5']) / 2)

def is_break_down_5d(kabuData):
    return (kabuData['4. close'] < kabuData['SMA_5']) & \
           (kabuData['1. open'] - kabuData['4. close'] > (kabuData['SMA_5'] - kabuData['4. close']) / 2)
