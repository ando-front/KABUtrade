import os
from dotenv import load_dotenv
import aibaTradeMethod
import sendEmailForSignal

# Alpha VantageのAPIキーを設定
load_dotenv()
api_key = os.getenv("API_KEY")

def main():
    # 必要なデータとパラメータを取得または定義
    # stock_data = aibaTradeMethod.get_stock_data('SPY', api_key)  # 例としてデータ取得
    up_down_periods = [9, 13]  # UP_DOWN_PERIODSの例
    sma_periods = [5, 10, 20, 25, 30, 60, 75, 100, 200, 300]  # SMA_PERIODSの例
    cross_periods = [25, 75]  # CROSS_PERIODSの例

    # データを準備（'Down'および'Up'列を追加）
    stock_data = aibaTradeMethod.prepare_data(up_down_periods, sma_periods, cross_periods)

    # main関数を引数とともに呼び出す
    signalType, signalKind = aibaTradeMethod.main(stock_data, up_down_periods, sma_periods, cross_periods)
    # メールを送信
    sendEmailForSignal.sendEmailForSignal(signalType, signalKind)
    
    # 結果を表示
    print(f"買いor売りシグナルSignal Typeの結果: {signalType}")
    print(f"移動平均線のシグナルタイプSignal Kindの結果: {signalKind}")

    return signalType, signalKind

if __name__ == "__main__":
    main()  # メイン関数を実行
