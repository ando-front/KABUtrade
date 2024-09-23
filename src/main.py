from typing import Tuple
import pandas as pd
import aiba_trade_method
from get_stock_data.get_alpha_vantage import get_stock_data
from get_stock_data.get_yahoo_finance import get_yfinance_stock_data, load_api_key
from helpers.trend_logic import standardize_headers
import send_mail.send_email_for_signal as send_email_for_signal
from dotenv import load_dotenv
import os

# Alpha VantageのAPIキーを設定
load_dotenv()
api_key = os.getenv("API_KEY")

# 共通売買シグナル計算関数
def process_stock_data(symbol: str, api_key: str = None) -> Tuple[str, str, str]:
    if symbol in ['SPY', 'AAPL']:
        kabuData = get_stock_data(symbol, api_key)
    else:
        kabuData = get_yfinance_stock_data(symbol)
    
    kabuData = standardize_headers(kabuData)  # 株価のヘッダー名統一
    signalType, signalKind = aiba_trade_method.main(kabuData)
    return symbol, signalType, signalKind

def main():
    api_key = load_api_key()  # APIキーの読み込み
    # CSVファイルから銘柄リストを読み込む
    symbols_NY = pd.read_csv('./symbols/symbols_NY.csv')['symbol'].tolist()
    symbols_JP = pd.read_csv('./symbols/symbols_JP.csv')['symbol'].tolist()
    all_symbols = list(set(symbols_NY + symbols_JP))
    print(all_symbols)
    signals = []

    for symbol in all_symbols:
        signals.append(process_stock_data(symbol, api_key))

    # まとめてシグナルを送信
    print(signals)
    send_email_for_signal.sendEmailForSignal(signals)
    
if __name__ == '__main__':
    main()  # メイン関数を実行