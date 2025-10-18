from typing import Tuple
import pandas as pd
import aiba_trade_method
from get_stock_data.get_yahoo_finance import get_yfinance_stock_data_batch, load_api_key
from helpers.trend_logic import standardize_headers
import send_mail.send_email_for_signal as send_email_for_signal
import os
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# 共通売買シグナル計算関数（バッチ処理対応 + 緩和レベル対応）
def process_stock_data(symbol: str, kabuData: pd.DataFrame, relaxation_level: str = aiba_trade_method.RelaxationLevel.NONE) -> Tuple[str, str, str]:
    """
    銘柄データを処理してシグナルを生成
    Args:
        symbol: 銘柄コード
        kabuData: 株価データ
        relaxation_level: 緩和レベル
    Returns:
        銘柄、シグナルタイプ、シグナル種類のタプル
    """
    try:
        if kabuData.empty:
            print(f"Warning: No data retrieved for symbol {symbol}. Skipping.")
            return symbol, "No Data", "No Data"

        kabuData = standardize_headers(kabuData)  # 株価のヘッダー名統一
        signalType, signalKind = aiba_trade_method.main(kabuData, relaxation_level)
        return symbol, signalType, signalKind
    except Exception as e:
        print(f"Error processing symbol {symbol}: {e}")
        return symbol, "Error", str(e)

def main():
    """メイン処理（コマンドライン引数対応 + バッチ処理 + 並列処理）"""
    parser = argparse.ArgumentParser(description='KABUtrade - 株式売買シグナル生成システム')
    parser.add_argument('--relaxation',
                       choices=[aiba_trade_method.RelaxationLevel.NONE,
                               aiba_trade_method.RelaxationLevel.MODERATE,
                               aiba_trade_method.RelaxationLevel.HIGH],
                       default=aiba_trade_method.RelaxationLevel.NONE,
                       help='シグナル緩和レベル (none: 厳格版, moderate: 中程度緩和, high: 高度緩和)')
    parser.add_argument('--symbols-only', nargs='+', help='処理対象の銘柄を指定（例: --symbols-only AAPL MSFT）')

    args = parser.parse_args()

    # 銘柄リストの決定
    if args.symbols_only:
        all_symbols = args.symbols_only
        print(f"指定銘柄のみ処理: {all_symbols}")
    else:
        # スクリプトのディレクトリを取得
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # CSVファイルへの絶対パスを構築
        ny_csv_path = os.path.join(script_dir, 'symbols', 'symbols_NY.csv')
        jp_csv_path = os.path.join(script_dir, 'symbols', 'symbols_JP.csv')
        # CSVファイルから銘柄リストを読み込む
        symbols_NY = pd.read_csv(ny_csv_path)['symbol'].tolist()
        symbols_JP = pd.read_csv(jp_csv_path)['symbol'].tolist()
        all_symbols = list(set(symbols_NY + symbols_JP))
        print(f"全銘柄処理: {len(all_symbols)} 銘柄")

    print(f"緩和レベル: {args.relaxation}")
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
            executor.submit(process_stock_data, symbol, stock_data_dict.get(symbol, pd.DataFrame()), args.relaxation): symbol
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

    # シグナル結果の表示
    print("\n=== シグナル結果 ===")
    for symbol, signal_type, signal_kind in signals:
        if signal_type not in [None, "No Signal", "No Data", "Error"]:
            print(f"{symbol}: {signal_type} - {signal_kind}")

    # "No Signal"以外のシグナルをフィルタリング（メール送信用）
    signals_to_send = [s for s in signals if s[1] not in [None, 'No Signal', 'No Data', 'Error']]

    # まとめてシグナルを送信
    print(f"\nFound {len(signals_to_send)} signals to send")
    if signals_to_send:
        send_email_for_signal.sendEmailForSignal(signals_to_send)
    else:
        print("No signals to send.")

if __name__ == '__main__':
    main()  # メイン関数を実行
