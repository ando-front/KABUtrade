import requests

def sendEmailForSignal(signals):
    # GASアプリのURL
    web_app_url = "https://script.google.com/macros/s/AKfycby-AX2kQeZLDasKS0rAYtJ9rO_WcRAvFQtbYlIY-cqAqiiKb4099fP-F3Mp6BRprIExlQ/exec"

    
    # シグナルデータを整形
    data = {
        'signals': [
            {'symbol': symbol, 'signalType': signalType, 'signalKind': signalKind}
            for symbol, signalType, signalKind in signals
        ]
    }

    print(data)
    response = requests.post(web_app_url, json=data)
    print(response.text)
