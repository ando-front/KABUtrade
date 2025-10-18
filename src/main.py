from typing import Tuple
import pandas as pd
import aiba_trade_method
from get_stock_data.get_yahoo_finance import get_yfinance_stock_data_batch, load_api_key
from helpers.trend_logic import standardize_headers
import send_mail.send_email_for_signal as send_email_for_signal
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# 共通売買シグナル計算関数
def process_stock_data(symbol: str, kabuData: pd.DataFrame) -> Tuple[str, str, str]:
    """
    銘柄データを処理してシグナルを生成
    """
    try:
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
    print(f"Processing {len(all_symbols)} symbols: {all_symbols}")

    # 一括でデータ取得（大幅な高速化）
    # 300日移動平均を計算するため、余裕を持って400日分取得
    print("Fetching stock data in batch mode...")
    stock_data_dict = get_yfinance_stock_data_batch(all_symbols, period_days=400)
    print(f"Successfully fetched data for {len(stock_data_dict)} symbols")

    # 並列でシグナル処理（ThreadPoolExecutorで高速化）
    signals = []
    print("Processing signals in parallel...")

    with ThreadPoolExecutor(max_workers=10) as executor:
        # 各銘柄の処理をスレッドプールに投入
        future_to_symbol = {
            executor.submit(process_stock_data, symbol, stock_data_dict.get(symbol, pd.DataFrame())): symbol
            for symbol in all_symbols
        }

        # 完了した処理から結果を収集
        for future in as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            try:
                result = future.result()
                signals.append(result)
                print(f"Processed: {symbol} -> {result[1]}")
            except Exception as e:
                print(f"Error processing {symbol}: {e}")
                signals.append((symbol, "Error", str(e)))

    # "No Signal"以外のシグナルをフィルタリング
    signals = [s for s in signals if s[1] != 'No Signal']

    # まとめてシグナルを送信
    print(f"Found {len(signals)} signals to send")
    print(signals)
    send_email_for_signal.sendEmailForSignal(signals)

if __name__ == '__main__':
    main()  # メイン関数を実行