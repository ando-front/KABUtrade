import requests

def sendEmailForSignal(signals):
    # GASアプリのURL
    web_app_url = "https://script.google.com/macros/s/AKfycbx2yC_gW9lLH9J4NusDbNk34R26F8wr_0GPH9xr7v6IIMrdgehRlri2ZEaho9UtemB25g/exec"

    
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
