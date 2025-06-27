from typing import Tuple
import pandas as pd
import aiba_trade_method
from get_stock_data.get_yahoo_finance import get_yfinance_stock_data, load_api_key
from helpers.trend_logic import standardize_headers
import send_mail.send_email_for_signal as send_email_for_signal
import os

# 共通売買シグナル計算関数
def process_stock_data(symbol: str) -> Tuple[str, str, str]:
    try:
        kabuData = get_yfinance_stock_data(symbol)
        
        if kabuData.empty:
            print(f"Warning: No data retrieved for symbol {symbol}. Skipping.")
            return symbol, "No Data", "No Data"
        
        kabuData = standardize_headers(kabuData)  # 株価のヘッダー名統一
        signalType, signalKind = aiba_trade_method.main(kabuData)
        return symbol, signalType, signalKind
    except Exception as e:
        print(f"Error processing symbol {symbol}: {e}")
        return symbol, "Error", str(e)

def main():
    # CSVファイルから銘柄リストを読み込む
    symbols_NY = pd.read_csv('src/symbols/symbols_NY.csv')['symbol'].tolist()
    symbols_JP = pd.read_csv('src/symbols/symbols_JP.csv')['symbol'].tolist()
    all_symbols = list(set(symbols_NY + symbols_JP))
    print(all_symbols)
    signals = []

    for symbol in all_symbols:
        signals.append(process_stock_data(symbol))

    # まとめてシグナルを送信
    print(signals)
    send_email_for_signal.sendEmailForSignal(signals)
    
if __name__ == '__main__':
    main()  # メイン関数を実行