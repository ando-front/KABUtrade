from typing import Tuple
import pandas as pd
import aiba_trade_method
from get_stock_data.get_alpha_vantage import get_stock_data
from get_stock_data.get_yahoo_finance import get_yfinance_stock_data, load_api_key
from helpers.trend_logic import standardize_headers
import send_mail.send_email_for_signal as send_email_for_signal
from dotenv import load_dotenv
import os
import argparse

# Alpha VantageのAPIキーを設定
load_dotenv()
api_key = os.getenv("API_KEY")

# 共通売買シグナル計算関数（緩和レベル対応）
def process_stock_data(symbol: str, api_key: str = None, relaxation_level: str = aiba_trade_method.RelaxationLevel.NONE) -> Tuple[str, str, str]:
    """株価データの処理とシグナル生成
    
    Args:
        symbol: 銘柄コード
        api_key: APIキー
        relaxation_level: 緩和レベル
    
    Returns:
        銘柄、シグナルタイプ、シグナル種類のタプル
    """
    try:
        kabuData = get_stock_data(symbol, api_key)
        
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
    """メイン処理（コマンドライン引数対応）"""
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='KABUtrade - 株式売買シグナル生成システム')
    parser.add_argument('--relaxation', 
                       choices=[aiba_trade_method.RelaxationLevel.NONE, 
                               aiba_trade_method.RelaxationLevel.MODERATE, 
                               aiba_trade_method.RelaxationLevel.HIGH],
                       default=aiba_trade_method.RelaxationLevel.NONE,
                       help='シグナル緩和レベル (none: 厳格版, moderate: 中程度緩和, high: 高度緩和)')
    parser.add_argument('--symbols-only', nargs='+', help='処理対象の銘柄を指定（例: --symbols-only AAPL MSFT）')
    
    args = parser.parse_args()
    
    api_key = load_api_key()  # APIキーの読み込み
    
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
    signals = []

    for symbol in all_symbols:
        signals.append(process_stock_data(symbol, api_key, args.relaxation))

    # シグナル結果の表示
    print("\n=== シグナル結果 ===")
    for symbol, signal_type, signal_kind in signals:
        if signal_type not in [None, "No Data", "Error"]:
            print(f"{symbol}: {signal_type} - {signal_kind}")
    
    # まとめてシグナルを送信
    send_email_for_signal.sendEmailForSignal(signals)
    
if __name__ == '__main__':
    main()  # メイン関数を実行
