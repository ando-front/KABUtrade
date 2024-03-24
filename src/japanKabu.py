import os
from dotenv import load_dotenv
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import mplfinance as mpf

load_dotenv()

# Alpha VantageのAPIキーと銘柄のリストを設定します
api_key = os.getenv("API_KEY")
symbols = ["7203.T"]  # 例：トヨタ自動車、ソフトバンク、ソニー

# GridSpecを作成します
fig = plt.figure(figsize=(12, 8))
gs = gridspec.GridSpec(len(symbols), 1, figure=fig)

for i, symbol in enumerate(symbols):
    # Yahoo Financeからデータを取得します
    data = yf.download(symbol, start="2020-01-01", end="2022-12-31")

    # チャートを作成します
    ap = mpf.make_addplot(data['Close'].rolling(window=5).mean())  # 5日移動平均
    mpf.plot(data, type='candle', addplot=ap, title=f'{symbol} Close Price with Moving Averages')

plt.tight_layout()
plt.show()