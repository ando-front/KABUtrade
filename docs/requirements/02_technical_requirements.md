# 技術要求仕様書 - KABUtrade

## 1. システム概要

### 1.1 システム名
KABUtrade - 株式売買シグナル自動生成・通知システム

### 1.2 技術スタック
- **言語**: Python 3.9.18
- **主要ライブラリ**: 
  - pandas 2.0.3 (データ処理)
  - numpy 1.26.3 (数値計算)
  - yfinance 0.2.57 (株価データ取得)
  - alpha-vantage 3.0.0 (バックアップAPI)
  - matplotlib 3.8.2 (グラフ描画)
  - mplfinance 0.12.10b0 (金融チャート)
  - requests 2.31.0 (HTTP通信)
  - python-dotenv 1.0.1 (環境変数管理)

- **実行環境**: ローカル実行（将来的にGitHub Actions対応）
- **通知システム**: Google Apps Script
- **データ保存**: CSV形式（ローカルキャッシュ）

### 1.3 API仕様
- **Primary**: Yahoo Finance API (yfinance)
- **Secondary**: Alpha Vantage API (フォールバック)
- **通知**: Google Apps Script Web App

## 2. アーキテクチャ設計

### 2.1 システム構成
```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions                            │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                 Daily Execution                         │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │ Data Fetch  │ -> │ Analysis    │ -> │ Notification │  │ │
│  │  │ Module      │    │ Engine      │    │ Service     │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
           │                      │                      │
           v                      v                      v
    ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
    │ Yahoo       │        │ Local Cache │        │ Google Apps │
    │ Finance API │        │ (CSV Files) │        │ Script      │
    └─────────────┘        └─────────────┘        └─────────────┘
```

### 2.2 モジュール構成
```
src/
├── main.py                    # メインエントリーポイント
├── aiba_trade_method.py       # 売買シグナル統合処理
├── calculaters/
│   ├── signals.py             # シグナル計算ロジック
│   └── trends.py              # トレンド判定ロジック
├── get_stock_data/
│   ├── get_yahoo_finance.py   # Yahoo Finance API
│   └── get_alpha_vantage.py   # Alpha Vantage API
├── helpers/
│   └── trend_logic.py         # 共通ヘルパー関数
├── send_mail/
│   └── send_email_for_signal.py # 通知処理
├── symbols/
│   ├── symbols_NY.csv         # 米国株銘柄リスト
│   └── symbols_JP.csv         # 日本株銘柄リスト
└── google_app_scripts/
    └── postMail.js            # GAS通知スクリプト
```

## 3. データ仕様

### 3.1 株価データ構造
```python
DataFrame Columns:
- '1. open'     # 始値
- '2. high'     # 高値
- '3. low'      # 安値
- '4. close'    # 終値
- '5. volume'   # 出来高
- Index: DatetimeIndex (日付)
```

### 3.2 移動平均線データ
```python
Calculated Columns:
- 'SMA_5'      # 5日移動平均
- 'SMA_10'     # 10日移動平均
- 'SMA_20'     # 20日移動平均
- 'SMA_25'     # 25日移動平均
- 'SMA_30'     # 30日移動平均
- 'SMA_60'     # 60日移動平均
- 'SMA_75'     # 75日移動平均
- 'SMA_100'    # 100日移動平均
- 'SMA_200'    # 200日移動平均
- 'SMA_300'    # 300日移動平均
```

### 3.3 シグナルデータ
```python
Signal Columns:
- 'Buy_Signal_9'               # 9日連続陰線買いシグナル
- 'Buy_Signal_13'              # 13日連続陰線買いシグナル
- 'Sell_Signal_9'              # 9日連続陽線売りシグナル
- 'Sell_Signal_13'             # 13日連続陽線売りシグナル
- 'Buy_Signal_MA_PPP'          # パンパカパン買いシグナル
- 'Sell_Signal_MA_reverse_PPP' # パンパカパン売りシグナル
- 'Buy_Signal_golden_cross'    # ゴールデンクロス買いシグナル
- 'Sell_Signal_dead_cross'     # デッドクロス売りシグナル
- 'buy_signal_lower_half'      # 下半身買いシグナル
- 'sell_signal_Reverse_lower_half' # 逆下半身売りシグナル
- 'buy_signal_bird_beak'       # くちばし買いシグナル
- 'sell_signal_reverse_bird_beak' # 逆くちばし売りシグナル
```

### 3.4 トレンドデータ
```python
Trend Columns:
- 'up_trend_count'    # 上昇トレンド継続日数
- 'down_trend_count'  # 下降トレンド継続日数
- 'is_up_trend'       # 上昇トレンド判定(60日以上)
- 'is_down_trend'     # 下降トレンド判定(60日以上)
- 'Up'                # 陽線判定
- 'Down'              # 陰線判定
```

## 4. API仕様

### 4.1 Yahoo Finance API
```python
Function: get_yfinance_stock_data()
Parameters:
- symbol: str           # 銘柄コード
- period: str          # データ期間 ("1y", "2y", "max", etc.)
- interval: str        # データ間隔 ("1d")
- max_retries: int     # 最大リトライ回数
- base_retry_delay: int # リトライ間隔

Returns: pd.DataFrame  # 株価データ
```

### 4.2 Alpha Vantage API
```python
Function: get_stock_data()
Parameters:
- symbol: str          # 銘柄コード
- api_key: str         # APIキー
- period: str          # データ期間
- interval: str        # データ間隔

Returns: pd.DataFrame  # 株価データ
```

### 4.3 Google Apps Script API
```javascript
Function: doPost(e)
Parameters:
- e.postData.contents: JSON {
    "signals": [
        {
            "symbol": "AAPL",
            "signalType": "Buy",
            "signalKind": "Golden Cross"
        }
    ]
}

Returns: "Email sent." | "Error message"
```

## 5. アルゴリズム仕様

### 5.1 移動平均線計算
```python
def calculate_sma(data: pd.DataFrame, periods: List[int]) -> pd.DataFrame:
    """
    移動平均線を計算
    
    Args:
        data: 株価データ
        periods: 移動平均期間のリスト
    
    Returns:
        移動平均線カラムが追加されたDataFrame
    """
    for period in periods:
        data[f'SMA_{period}'] = data['4. close'].rolling(window=period).mean()
    return data
```

### 5.2 トレンド判定アルゴリズム
```python
def calculate_up_trend(kabuData: pd.DataFrame, i: int) -> int:
    """
    上昇トレンドカウント計算
    
    Cases:
    A: SMA_5 < SMA_20 and SMA_5 < Close
    B: SMA_20 < SMA_5 and SMA_20 < Close and SMA_20 > SMA_20_prev
    C: SMA_60 < SMA_5 and SMA_60 < Close and SMA_20 > SMA_20_prev and SMA_60 > SMA_60_prev
    
    Exception: SMA_60 < SMA_5 and SMA_20 < SMA_20_prev and SMA_60 > SMA_60_prev and Close > SMA_60
    """
```

### 5.3 シグナル生成アルゴリズム
```python
def check_cross_signals(latest_data: pd.Series) -> Tuple[Optional[str], Optional[str]]:
    """
    クロスシグナルチェック（優先度1）
    
    Returns:
        (signal_type, signal_kind) or (None, None)
    """

def check_up_down_signals(latest_data: pd.Series, UP_DOWN_PERIODS: List[int]) -> Tuple[Optional[str], Optional[str]]:
    """
    連続陰線・陽線シグナルチェック（優先度2）
    """

def check_other_signals(latest_data: pd.Series) -> Tuple[Optional[str], Optional[str]]:
    """
    その他シグナルチェック（優先度3）
    """
```

## 6. エラーハンドリング

### 6.1 API制限対応
```python
Rate Limit Handling:
- 指数バックオフ: 60, 120, 240, 480秒
- 最大リトライ回数: 5回
- キャッシュ機能: 成功時にCSVファイル保存
- フォールバック: Alpha Vantage API使用
```

### 6.2 データ品質チェック
```python
Data Validation:
- 空データチェック
- 日付範囲チェック
- 異常値検出
- カラム存在チェック
```

### 6.3 通知エラー対応
```python
Notification Error Handling:
- HTTP接続エラー
- GASスクリプトエラー
- メール送信エラー
- レスポンスタイムアウト
```

## 7. パフォーマンス設計

### 7.1 データ取得最適化
```python
Optimization Strategy:
- キャッシュ機能による重複取得回避
- 銘柄別の並列処理（将来拡張）
- API制限を考慮した待機時間設定
- 部分的データ更新（将来拡張）
```

### 7.2 メモリ使用量最適化
```python
Memory Management:
- DataFrameの部分読み込み
- 不要カラムの削除
- ガベージコレクションの活用
- キャッシュサイズの制限
```

## 8. セキュリティ仕様

### 8.1 認証情報管理
```python
Environment Variables:
- API_KEY: Alpha Vantage APIキー
- ALPHAVANTAGE_API_KEY: GitHub Secrets
- GAS_URL: Google Apps Script URL
```

### 8.2 データ保護
```python
Data Protection:
- 個人情報の非保存
- 一時ファイルの自動削除
- ログファイルの機密情報除外
- 通信のHTTPS化
```

## 9. 監視・ログ仕様

### 9.1 ログレベル
```python
Logging Levels:
- DEBUG: 詳細なデバッグ情報
- INFO: 一般的な実行情報
- WARNING: 警告レベルの問題
- ERROR: エラー発生時の情報
- CRITICAL: システム停止レベルの問題
```

### 9.2 監視項目
```python
Monitoring Items:
- API応答時間
- データ取得成功率
- シグナル生成成功率
- メール送信成功率
- システム実行時間
```

## 10. テスト仕様

### 10.1 ユニットテスト
```python
Test Coverage:
- データ取得関数
- シグナル生成関数
- トレンド判定関数
- エラーハンドリング
- データ変換関数
```

### 10.2 統合テスト
```python
Integration Tests:
- API連携テスト
- データフロー テスト
- 通知機能テスト
- エラーシナリオテスト
```

### 10.3 バックテスト
```python
Backtest Framework:
- 過去データでのシグナル検証
- 売買シミュレーション
- パフォーマンス評価
- 戦略の有効性確認
```
