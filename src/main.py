import aibaTradeMethod
import sendEmailForSignal
from dotenv import load_dotenv
import os

# Alpha VantageのAPIキーを設定
load_dotenv()
api_key = os.getenv("API_KEY")


def main():
    kabuData = aibaTradeMethod.get_stock_data('SPY', api_key)
    signalType, signalKind = aibaTradeMethod.main(kabuData)
    sendEmailForSignal.sendEmailForSignal(signalType, signalKind)
    kabuData = aibaTradeMethod.get_stock_data('NVDA', api_key)
    signalType, signalKind = aibaTradeMethod.main(kabuData)
    sendEmailForSignal.sendEmailForSignal(signalType, signalKind)

if __name__ == '__main__':
    main()  # メイン関数を実行