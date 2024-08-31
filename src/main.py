import aiba_trade_method
from get_stock_data.get_alpha_vantage import get_stock_data
import send_mail.send_email_for_signal as send_email_for_signal
from dotenv import load_dotenv
import os

# Alpha VantageのAPIキーを設定
load_dotenv()
api_key = os.getenv("API_KEY")


def main():
    kabuData = get_stock_data('SPY', api_key)
    signalType, signalKind = aiba_trade_method.main(kabuData)
    send_email_for_signal.sendEmailForSignal(signalType, signalKind)
    kabuData = get_stock_data('NVDA', api_key)
    signalType, signalKind = aiba_trade_method.main(kabuData)
    send_email_for_signal.sendEmailForSignal(signalType, signalKind)

if __name__ == '__main__':
    main()  # メイン関数を実行