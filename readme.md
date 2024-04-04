alpha_vantage ライブラリのインストール

```
pip install alpha_vantage
```

Welcome to Alpha Vantage! Your API key is:

- B48ULYVXV9EYZ0M1

. Please record this API key at a safe place for future data access.

```
from alpha_vantage.timeseries import TimeSeries

# あなたのAPIキーを設定します
api_key = 'YOUR_API_KEY'

ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT', interval='1min', outputsize='full')

print(data)
```

このコードは、Microsoft の株価データを 1 分間隔で取得します。get_intraday メソッドのパラメータを変更することで、異なる銘柄、時間間隔、またはデータ量のデータを取得することができます。

以下のコマンドを使用して pandas ライブラリをインストールしてください：

```
pip install pandas
```

Python の実行

```
.\kabu.py
```

```
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries

# あなたのAPIキーを設定します
api_key = 'YOUR_API_KEY'

ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_daily(symbol='MSFT', outputsize='full')

# 移動平均線を計算します
data['5_day_sma'] = data['4. close'].rolling(window=5).mean()
data['20_day_sma'] = data['4. close'].rolling(window=20).mean()
data['40_day_sma'] = data['4. close'].rolling(window=40).mean()

# グラフを描画します
plt.figure(figsize=(12,6))
plt.plot(data['4. close'], label='Close Price')
plt.plot(data['5_day_sma'], label='5 Day SMA')
plt.plot(data['20_day_sma'], label='20 Day SMA')
plt.plot(data['40_day_sma'], label='40 Day SMA')
plt.title('Microsoft Close Price with Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
```

## 環境変数

AlphaVantage API キーを環境変数として設定する必要があります。GitHub Actions では、Secrets を使用して環境変数を設定できます。

以下の手順で設定を行ってください：

GitHub リポジトリの設定ページに移動します。
左側のメニューから"Secrets"を選択します。
"New repository secret"をクリックします。
"Name"フィールドに ALPHAVANTAGE_API_KEY と入力し、"Value"フィールドに API キーを入力します。
"Add secret"をクリックします。
これで、API キーはリポジトリの Secrets に保存され、ワークフローから参照できます。

次に、ワークフローファイル（daily_exec.yaml）を更新して、この Secret を環境変数として使用します：

```
jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.x"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r ${{ github.workspace }}/requirements.txt

      - name: Run script
        run: python src/main.py
        env:
          ALPHAVANTAGE_API_KEY: ${{ secrets.ALPHAVANTAGE_API_KEY }}
```
