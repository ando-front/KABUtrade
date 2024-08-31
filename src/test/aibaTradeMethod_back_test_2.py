from aiba_trade_method import calculate_signals
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv
import os

# このコードは、初期資金を設定し、買いシグナルが出たときに全ての資金を使って株を買い、売りシグナルが出たときに全ての株を売るというシンプルな戦略を採用しています。バックテストの結果は、初期資金と最終的なポートフォリオの価値として出力されます。
# ただし、このコードは非常にシンプルなものであり、実際のトレーディングでは、リスク管理のルール、手数料、スリッページ（注文価格と実際の取引価格との差）などを考慮する必要があります。また、バックテストの結果は過去のデータに基づいているため、未来のパフォーマンスを保証するものではありません。

def get_data(api_key, symbol):
    try:
        ts = TimeSeries(key=api_key, output_format='pandas')
        data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
        return data
    except Exception as e:
        print(f"Error occurred while fetching data: {e}")
        return None
    
def check_buy_signals(row):
    return any(row[f'Buy_Signal_{period}'] for period in UP_DOWN_PERIODS) or row['Buy_Signal_MA_PPP'] or row['Buy_Signal_golden_cross'] or row['buy_signal_lower_harf'] or row['buy_signal_bird_beak']

def check_sell_signals(row):
    return any(row[f'Sell_Signal_{period}'] for period in UP_DOWN_PERIODS) or row['Sell_Signal_MA_reverse_PPP'] or row['Sell_Signal_dead_cross'] or row['sell_signal_Reverse_lower_half'] or row['sell_signal_reverse_bird_beak']

# Alpha VantageのAPIキーを設定
load_dotenv()
api_key = os.getenv("API_KEY")
if api_key is None:
    print("API_KEY is not set in the environment variables.")
    exit(1)
    
SYMBOL = 'SPY' # S&P500 ETF
# SYMBOL = 'AAPL'
data = get_data(api_key, SYMBOL)


# 陽線と陰線の判定
data['Up'] = data['4. close'] > data['1. open']
data['Down'] = data['4. close'] < data['1. open']

# Constants
SMA_PERIODS = [5, 10, 20, 25, 30, 60, 75, 100, 200]
UP_DOWN_PERIODS = [9, 13]
CROSS_PERIODS = [25, 75]

for period in SMA_PERIODS:
    data[f'SMA_{period}'] = data['4. close'].rolling(window=period).mean()

# 既存のロジックを使用してシグナルを計算
kabuData = calculate_signals(data, UP_DOWN_PERIODS, SMA_PERIODS, CROSS_PERIODS)

# 資産の初期値を設定
initial_portfolio = 1000000
cash = initial_portfolio
shares = 0
portfolio = []
signal_counts = {}

# シミュレーションの実行
for i in range(len(kabuData)):
    if check_buy_signals(kabuData.iloc[i]):
        shares += cash / kabuData.iloc[i]['4. close']
        cash = 0
        signal_counts['Buy'] = signal_counts.get('Buy', 0) + 1
    elif check_sell_signals(kabuData.iloc[i]):
        cash += shares * kabuData.iloc[i]['4. close']
        shares = 0
        signal_counts['Sell'] = signal_counts.get('Sell', 0) + 1
    portfolio.append(cash + shares * kabuData.iloc[i]['4. close'])

# パフォーマンスの評価
returns = (portfolio[-1] - initial_portfolio) / initial_portfolio
print(f'Returns: {returns * 100}%')
print(f"Initial balance: {initial_portfolio}, Final portfolio: {portfolio[-1]}")

# シグナルの回数を出力
for signal, count in signal_counts.items():
    print(f"{signal} signal was generated {count} times")