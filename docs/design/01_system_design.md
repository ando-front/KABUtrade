# システム設計書 - KABUtrade

## 1. システム概要設計

### 1.1 システム構成図
```
┌─────────────────────────────────────────────────────────────────────────┐
│                           KABUtrade System                              │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      Main Application                           │   │
│  │                                                                 │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │   │
│  │  │   Data      │  │  Signal     │  │   Trend     │  │  Mail   │ │   │
│  │  │  Fetcher    │->│ Calculator  │->│  Analyzer   │->│ Sender  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │   │
│  │                                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ Local Cache │  │  Symbol     │  │ Environment │  │   Backup    │   │
│  │ (CSV Files) │  │  Lists      │  │ Variables   │  │   Systems   │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
┌─────────────────────────────────────────────────────────────────────────┐
│                          External Services                              │
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ Yahoo       │  │ Alpha       │  │ Google Apps │  │ Email       │   │
│  │ Finance API │  │ Vantage API │  │ Script      │  │ Recipients  │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 データフロー図
```
Start
  │
  ├─ Read Symbol Lists (symbols_NY.csv, symbols_JP.csv)
  │
  ├─ For Each Symbol:
  │   │
  │   ├─ Check Cache
  │   │   │
  │   │   ├─ Cache Hit → Load Data
  │   │   │
  │   │   └─ Cache Miss → Fetch from API
  │   │       │
  │   │       ├─ Yahoo Finance API (Primary)
  │   │       │
  │   │       └─ Alpha Vantage API (Fallback)
  │   │
  │   ├─ Data Standardization
  │   │   │
  │   │   └─ Convert to Alpha Vantage Format
  │   │
  │   ├─ Calculate Technical Indicators
  │   │   │
  │   │   ├─ Moving Averages (SMA_5, SMA_10, ..., SMA_300)
  │   │   │
  │   │   ├─ Trend Analysis (Up/Down Trend Counts)
  │   │   │
  │   │   └─ Signal Generation (Buy/Sell Signals)
  │   │
  │   ├─ Signal Evaluation
  │   │   │
  │   │   ├─ Cross Signals (Golden/Dead Cross)
  │   │   │
  │   │   ├─ Consecutive Signals (9/13 Day Patterns)
  │   │   │
  │   │   └─ Aiba Method Signals (Lower Half, Bird Beak)
  │   │
  │   └─ Store Signal Result
  │
  ├─ Consolidate All Signals
  │
  ├─ Send Notification
  │   │
  │   ├─ Prepare Email Content
  │   │
  │   ├─ Send to Google Apps Script
  │   │
  │   └─ GAS Sends Email to Recipients
  │
  └─ End
```

## 2. クラス設計

### 2.1 主要クラス構成
```python
class StockDataFetcher:
    """株価データ取得クラス"""
    
    def __init__(self, cache_dir: str = "data_cache"):
        self.cache_dir = cache_dir
        self.api_retry_count = 3
        self.api_retry_delay = 60
    
    def fetch_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """データ取得メイン処理"""
        pass
    
    def _load_from_cache(self, symbol: str, period: str) -> pd.DataFrame:
        """キャッシュからデータ読み込み"""
        pass
    
    def _save_to_cache(self, symbol: str, period: str, data: pd.DataFrame):
        """キャッシュにデータ保存"""
        pass
    
    def _fetch_from_yahoo(self, symbol: str, period: str) -> pd.DataFrame:
        """Yahoo Finance APIからデータ取得"""
        pass
    
    def _fetch_from_alpha_vantage(self, symbol: str) -> pd.DataFrame:
        """Alpha Vantage APIからデータ取得"""
        pass

class TechnicalAnalyzer:
    """テクニカル分析クラス"""
    
    def __init__(self):
        self.sma_periods = [5, 10, 20, 25, 30, 60, 75, 100, 200, 300]
        self.up_down_periods = [9, 13]
        self.cross_periods = [25, 75]
    
    def calculate_sma(self, data: pd.DataFrame) -> pd.DataFrame:
        """移動平均線計算"""
        pass
    
    def calculate_trends(self, data: pd.DataFrame) -> pd.DataFrame:
        """トレンド分析"""
        pass
    
    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """シグナル生成"""
        pass

class SignalEvaluator:
    """シグナル評価クラス"""
    
    def __init__(self):
        self.signal_priority = [
            'cross_signals',
            'consecutive_signals', 
            'aiba_method_signals'
        ]
    
    def evaluate_latest_signal(self, data: pd.DataFrame) -> Tuple[str, str]:
        """最新シグナル評価"""
        pass
    
    def _check_cross_signals(self, latest_data: pd.Series) -> Tuple[str, str]:
        """クロスシグナルチェック"""
        pass
    
    def _check_consecutive_signals(self, latest_data: pd.Series) -> Tuple[str, str]:
        """連続シグナルチェック"""
        pass
    
    def _check_aiba_signals(self, latest_data: pd.Series) -> Tuple[str, str]:
        """相場式シグナルチェック"""
        pass

class NotificationService:
    """通知サービスクラス"""
    
    def __init__(self, gas_url: str):
        self.gas_url = gas_url
    
    def send_signals(self, signals: List[Tuple[str, str, str]]):
        """シグナル通知送信"""
        pass
    
    def _format_message(self, signals: List[Tuple[str, str, str]]) -> dict:
        """メッセージフォーマット"""
        pass

class MainApplication:
    """メインアプリケーションクラス"""
    
    def __init__(self):
        self.data_fetcher = StockDataFetcher()
        self.analyzer = TechnicalAnalyzer()
        self.evaluator = SignalEvaluator()
        self.notifier = NotificationService(os.getenv("GAS_URL"))
    
    def run(self):
        """メイン実行処理"""
        pass
    
    def _load_symbols(self) -> List[str]:
        """銘柄リスト読み込み"""
        pass
    
    def _process_symbol(self, symbol: str) -> Tuple[str, str, str]:
        """銘柄別処理"""
        pass
```

## 3. データベース設計

### 3.1 キャッシュファイル設計
```
data_cache/
├── <hash_value>.csv              # キャッシュファイル
│   ├── Date (Index)              # 日付インデックス
│   ├── Open                      # 始値
│   ├── High                      # 高値
│   ├── Low                       # 安値
│   ├── Close                     # 終値
│   └── Volume                    # 出来高
```

### 3.2 設定ファイル設計
```
symbols/
├── symbols_NY.csv                # 米国株銘柄
│   ├── symbol                    # 銘柄コード
│   └── company                   # 会社名
│
└── symbols_JP.csv                # 日本株銘柄
    ├── symbol                    # 銘柄コード
    └── company                   # 会社名
```

### 3.3 環境変数設計
```
Environment Variables:
├── API_KEY                       # Alpha Vantage APIキー
├── ALPHAVANTAGE_API_KEY          # GitHub Actions用
└── GAS_URL                       # Google Apps Script URL
```

## 4. API設計

### 4.1 内部API設計
```python
# データ取得API
def get_stock_data(symbol: str, period: str = "max") -> pd.DataFrame:
    """
    株価データ取得
    
    Args:
        symbol: 銘柄コード
        period: データ期間
    
    Returns:
        株価データ
    
    Raises:
        DataFetchError: データ取得失敗
    """

# シグナル生成API
def generate_signals(data: pd.DataFrame) -> pd.DataFrame:
    """
    売買シグナル生成
    
    Args:
        data: 株価データ
    
    Returns:
        シグナル付きデータ
    """

# 通知API
def send_notification(signals: List[Signal]) -> bool:
    """
    通知送信
    
    Args:
        signals: シグナルリスト
    
    Returns:
        送信成功フラグ
    """
```

### 4.2 外部API設計
```python
# Yahoo Finance API
Request:
    GET https://query1.finance.yahoo.com/v8/finance/chart/{symbol}
    
Response:
    {
        "chart": {
            "result": [{
                "timestamp": [...],
                "indicators": {
                    "quote": [{
                        "open": [...],
                        "high": [...],
                        "low": [...],
                        "close": [...],
                        "volume": [...]
                    }]
                }
            }]
        }
    }

# Google Apps Script API
Request:
    POST {GAS_URL}
    Content-Type: application/json
    
    {
        "signals": [
            {
                "symbol": "AAPL",
                "signalType": "Buy",
                "signalKind": "Golden Cross"
            }
        ]
    }

Response:
    "Email sent." | "Error message"
```

## 5. アルゴリズム設計

### 5.1 移動平均線計算アルゴリズム
```python
def calculate_sma(data: pd.DataFrame, periods: List[int]) -> pd.DataFrame:
    """
    Simple Moving Average計算
    
    Formula: SMA = (P1 + P2 + ... + Pn) / n
    
    Implementation:
        data[f'SMA_{period}'] = data['4. close'].rolling(window=period).mean()
    """
```

### 5.2 トレンド判定アルゴリズム
```python
def calculate_up_trend(data: pd.DataFrame, index: int) -> int:
    """
    上昇トレンド判定
    
    Cases:
        A: SMA_5 < SMA_20 AND SMA_5 < Close → count++
        B: SMA_20 < SMA_5 AND SMA_20 < Close AND SMA_20_rising → count++
        C: SMA_60 < SMA_5 AND SMA_60 < Close AND SMA_20_rising AND SMA_60_rising → count++
        
    Exception:
        SMA_60 < SMA_5 AND SMA_20_falling AND SMA_60_rising AND Close > SMA_60 → count (no change)
    
    Returns:
        count if condition met, else 0
    """
```

### 5.3 シグナル生成アルゴリズム
```python
def generate_buy_signals(data: pd.DataFrame) -> pd.DataFrame:
    """
    買いシグナル生成
    
    Signals:
        1. 75-day line breakout (upward) with positive candle
        2. 9 or 13 consecutive negative candles
        3. Golden Cross (25-day > 75-day)
        4. PPP (5 < 20 < 60 < 100 < 200 < 300)
        5. Lower Half pattern
        6. Bird Beak pattern
    """

def generate_sell_signals(data: pd.DataFrame) -> pd.DataFrame:
    """
    売りシグナル生成
    
    Signals:
        1. 75-day line breakdown (downward) with negative candle
        2. 9 or 13 consecutive positive candles
        3. Dead Cross (25-day < 75-day)
        4. Reverse PPP (5 > 20 > 60 > 100 > 200 > 300)
        5. Reverse Lower Half pattern
        6. Reverse Bird Beak pattern
    """
```

## 6. エラーハンドリング設計

### 6.1 例外クラス設計
```python
class KABUTradeException(Exception):
    """基底例外クラス"""
    pass

class DataFetchError(KABUTradeException):
    """データ取得エラー"""
    pass

class APILimitError(KABUTradeException):
    """API制限エラー"""
    pass

class DataValidationError(KABUTradeException):
    """データ検証エラー"""
    pass

class NotificationError(KABUTradeException):
    """通知エラー"""
    pass
```

### 6.2 エラーハンドリングフロー
```python
def handle_api_error(error: Exception, symbol: str, attempt: int) -> bool:
    """
    APIエラーハンドリング
    
    Flow:
        1. エラー種別判定
        2. リトライ可能性判定
        3. 待機時間計算
        4. フォールバック処理
        5. エラーログ記録
    
    Returns:
        should_retry: bool
    """
```

## 7. パフォーマンス設計

### 7.1 キャッシュ戦略
```python
Cache Strategy:
    - File-based caching (CSV format)
    - Cache key: MD5(symbol_period_interval)
    - Cache expiration: 1 day
    - Cache invalidation: On data fetch success
    - Cache size limit: 100MB
```

### 7.2 並列処理設計
```python
# 将来の拡張計画
Parallel Processing:
    - ThreadPoolExecutor for multiple symbols
    - Rate limiting with semaphore
    - Shared cache access with locks
    - Result aggregation
```

### 7.3 メモリ最適化
```python
Memory Optimization:
    - Lazy loading of data
    - Garbage collection after each symbol
    - DataFrame chunking for large datasets
    - Memory profiling and monitoring
```

## 8. セキュリティ設計

### 8.1 認証・認可
```python
Authentication:
    - Environment variable based API key storage
    - No hardcoded credentials
    - GitHub Secrets for CI/CD
    - API key rotation support
```

### 8.2 データ保護
```python
Data Protection:
    - No personal data storage
    - Temporary file cleanup
    - Encrypted communication (HTTPS)
    - Input validation and sanitization
```

### 8.3 監査ログ
```python
Audit Logging:
    - API call logging
    - Error occurrence logging
    - Performance metrics logging
    - Security event logging
```

## 9. テスト設計

### 9.1 テスト戦略
```python
Test Strategy:
    1. Unit Tests (90% coverage target)
    2. Integration Tests (API integration)
    3. System Tests (End-to-end)
    4. Performance Tests (Load testing)
    5. Security Tests (Vulnerability scanning)
```

### 9.2 テストケース設計
```python
Test Cases:
    - Data fetching with various symbols
    - Signal generation with different market conditions
    - Error handling with API failures
    - Cache functionality
    - Notification delivery
```

### 9.3 バックテスト設計
```python
Backtest Framework:
    - Historical data simulation
    - Signal accuracy measurement
    - Performance benchmark
    - Strategy comparison
    - Risk assessment
```

## 10. 監視・運用設計

### 10.1 監視項目
```python
Monitoring Items:
    - System availability
    - API response times
    - Error rates
    - Data quality metrics
    - Notification success rates
```

### 10.2 アラート設計
```python
Alert Configuration:
    - API failure alerts
    - Data quality alerts
    - Performance degradation alerts
    - Security incident alerts
    - System resource alerts
```

### 10.3 運用フロー
```python
Operation Flow:
    1. Daily execution monitoring
    2. Error investigation and resolution
    3. Performance optimization
    4. Security patch application
    5. Feature enhancement deployment
```
