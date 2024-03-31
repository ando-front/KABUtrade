import aibaTradeMethod
import sendEmailForSignal


def main():
    signalType, signalKind = aibaTradeMethod.main()
    sendEmailForSignal.sendEmailForSignal(signalType, signalKind)

if __name__ == '__main__':
    main()  # メイン関数を実行