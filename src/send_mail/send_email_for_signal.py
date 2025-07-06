import requests

def sendEmailForSignal(signals):
    # GASアプリのURL
    web_app_url = "https://script.google.com/macros/s/AKfycbx2yC_gW9lLH9J4NusDbNk34R26F8wr_0GPH9xr7v6IIMrdgehRlri2ZEaho9UtemB25g/exec"

    
    # シグナルデータを整形
    if not signals:
        data = {
            'signals': [
                {'symbol': 'N/A', 'signalType': 'No Signal', 'signalKind': 'No signals were generated today.'}
            ]
        }
    else:
        data = {
            'signals': [
                {'symbol': symbol, 'signalType': signalType, 'signalKind': signalKind}
                for symbol, signalType, signalKind in signals
                if signalType != "No Signal"
            ]
        }
        if not data['signals']:
            data = {
                'signals': [
                    {'symbol': 'N/A', 'signalType': 'No Signal', 'signalKind': 'No signals were generated today.'}
                ]
            }

    print(data)
    response = requests.post(web_app_url, json=data)
    print(response.text)
