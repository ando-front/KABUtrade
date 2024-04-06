# 仕様

この Python コードは、Alpha Vantage の API を使用して株価データを取得し、そのデータを基に売買のシグナルを生成するものです。具体的には以下のような処理を行っています。

1. Alpha Vantage の API キーを環境変数から取得します。
2. Alpha Vantage の API を使用して、指定した銘柄（ここでは'SPY'）の日次株価データを取得します。
3. 取得した株価データに対して、移動平均線を計算します。移動平均線の期間は、5, 20, 25, 30, 60, 75, 100, 200 日としています。
4. 陽線と陰線を判定します。陽線は終値が始値より高い日、陰線は終値が始値より低い日を指します。
5. 以下の条件に基づいて売買のシグナルを生成します。

- 買いシグナル：日足が 75 日線を下から上に抜けて陽線で終わる、または陰線が 9 日間または 13 日間連続する
- 売りシグナル：日足が 75 日線を上から下に抜けて陰線で終わる、または陽線が 9 日間または 13 日間連続する
- 移動平均線が 5, 20, 60, 100, 200, 30 日の順番で高い場合は買いシグナル、逆に低い場合は売りシグナルとします。
- ゴールデンクロス（短期の移動平均線が長期の移動平均線を下から上に抜ける現象）が発生した場合は買いシグナル、デッドクロス（短期の移動平均線が長期の移動平均線を上から下に抜ける現象）が発生した場合は売りシグナルとします。
- 下半身：買いシグナルシグナル 5 日線が上昇トレンドで、前日の日足線が 5 日線より下にあり、かつ、当日の日足線が陽線で 5 日線を実体の半分以上突き抜けていれば、買いシグナルとします。逆を逆下半身として売りシグナルとします。
- くちばし:5 日線と 10 日線が上昇トレンドで、前日の 5 日線が 10 日線より下にあり、かつ、当日の 5 日線が 10 日線を上抜けていれば、買いシグナルとします。逆を売りシグナルとします。

6. 最新の日付でのシグナルを出力します。ゴールデンクロスもデッドクロスもない場合、連続上昇日数または連続下落日数に基づくシグナル、移動平均に基づくシグナルをチェックします。
7. 最後に、株価と移動平均線、売買のシグナルをプロットします。
   なお、このコードでは実際の売買注文は行わず、シグナルの生成だけを行っています。

# 手順

alpha_vantage ライブラリのインストール

```
pip install alpha_vantage
```

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
