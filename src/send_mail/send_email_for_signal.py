import requests

def sendEmailForSignal(signals):
    # GASアプリのURL
    web_app_url = "https://script.google.com/macros/s/AKfycbx-rRtWXEvNiB6E2JozVRgHbgqsDAq7phKhhrgx3KLhQ8ow3DIFDrp5vihbb14m3zs1tg/exec"
    
    # シグナルデータを整形
    data = {
        'signals': [
            {'symbol': symbol, 'signalType': signalType, 'signalKind': signalKind}
            for symbol, signalType, signalKind in signals
        ]
    }

    response = requests.post(web_app_url, json=data)
    print(response.text)
