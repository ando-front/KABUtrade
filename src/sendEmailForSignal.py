import requests

def sendEmailForSignal(signalType, signalKind):
    # GASアプリのURL
    web_app_url = "https://script.google.com/macros/s/AKfycbx-rRtWXEvNiB6E2JozVRgHbgqsDAq7phKhhrgx3KLhQ8ow3DIFDrp5vihbb14m3zs1tg/exec"
    data = {
      'signalType': signalType,  # 'buy' または 'sell'
      'signalKind': signalKind   # シグナルの種類
    }

    response = requests.post(web_app_url, data=data)
    print(response.text)
