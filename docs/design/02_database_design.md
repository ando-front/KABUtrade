# データベース設計書 - KABUtrade

## 1. データ構造設計

### 1.1 株価データ構造
```sql
-- 株価データのスキーマ（論理設計）
Table: stock_price_data
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Column Name     │ Data Type       │ Description     │ Sample Value    │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ date            │ DATE (Index)    │ 取引日          │ 2024-01-15      │
│ 1. open         │ DECIMAL(10,2)   │ 始値           │ 150.25          │
│ 2. high         │ DECIMAL(10,2)   │ 高値           │ 152.80          │
│ 3. low          │ DECIMAL(10,2)   │ 安値           │ 149.90          │
│ 4. close        │ DECIMAL(10,2)   │ 終値           │ 151.50          │
│ 5. volume       │ BIGINT          │ 出来高         │ 1250000         │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

### 1.2 移動平均線データ構造
```sql
-- 移動平均線データのスキーマ
Table: moving_averages
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Column Name     │ Data Type       │ Description     │ Sample Value    │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ date            │ DATE (Index)    │ 取引日          │ 2024-01-15      │
│ SMA_5           │ DECIMAL(10,2)   │ 5日移動平均     │ 150.80          │
│ SMA_10          │ DECIMAL(10,2)   │ 10日移動平均    │ 149.20          │
│ SMA_20          │ DECIMAL(10,2)   │ 20日移動平均    │ 148.50          │
│ SMA_25          │ DECIMAL(10,2)   │ 25日移動平均    │ 147.90          │
│ SMA_30          │ DECIMAL(10,2)   │ 30日移動平均    │ 147.30          │
│ SMA_60          │ DECIMAL(10,2)   │ 60日移動平均    │ 145.80          │
│ SMA_75          │ DECIMAL(10,2)   │ 75日移動平均    │ 144.90          │
│ SMA_100         │ DECIMAL(10,2)   │ 100日移動平均   │ 143.50          │
│ SMA_200         │ DECIMAL(10,2)   │ 200日移動平均   │ 140.20          │
│ SMA_300         │ DECIMAL(10,2)   │ 300日移動平均   │ 138.70          │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

### 1.3 シグナルデータ構造
```sql
-- シグナルデータのスキーマ
Table: trading_signals
┌─────────────────────────────────┬─────────────────┬─────────────────────────────────┬─────────────────┐
│ Column Name                     │ Data Type       │ Description                     │ Sample Value    │
├─────────────────────────────────┼─────────────────┼─────────────────────────────────┼─────────────────┤
│ date                            │ DATE (Index)    │ 取引日                          │ 2024-01-15      │
│ Buy_Signal_9                    │ BOOLEAN         │ 9日連続陰線買いシグナル         │ TRUE            │
│ Buy_Signal_13                   │ BOOLEAN         │ 13日連続陰線買いシグナル        │ FALSE           │
│ Sell_Signal_9                   │ BOOLEAN         │ 9日連続陽線売りシグナル         │ FALSE           │
│ Sell_Signal_13                  │ BOOLEAN         │ 13日連続陽線売りシグナル        │ FALSE           │
│ Buy_Signal_MA_PPP               │ BOOLEAN         │ パンパカパン買いシグナル        │ FALSE           │
│ Sell_Signal_MA_reverse_PPP      │ BOOLEAN         │ パンパカパン売りシグナル        │ FALSE           │
│ Buy_Signal_golden_cross         │ BOOLEAN         │ ゴールデンクロス買いシグナル    │ TRUE            │
│ Sell_Signal_dead_cross          │ BOOLEAN         │ デッドクロス売りシグナル        │ FALSE           │
│ buy_signal_lower_half           │ BOOLEAN         │ 下半身買いシグナル              │ FALSE           │
│ sell_signal_Reverse_lower_half  │ BOOLEAN         │ 逆下半身売りシグナル            │ FALSE           │
│ buy_signal_bird_beak            │ BOOLEAN         │ くちばし買いシグナル            │ FALSE           │
│ sell_signal_reverse_bird_beak   │ BOOLEAN         │ 逆くちばし売りシグナル          │ FALSE           │
└─────────────────────────────────┴─────────────────┴─────────────────────────────────┴─────────────────┘
```

### 1.4 トレンドデータ構造
```sql
-- トレンドデータのスキーマ
Table: trend_analysis
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Column Name     │ Data Type       │ Description     │ Sample Value    │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ date            │ DATE (Index)    │ 取引日          │ 2024-01-15      │
│ up_trend_count  │ INTEGER         │ 上昇トレンド日数│ 85              │
│ down_trend_count│ INTEGER         │ 下降トレンド日数│ 0               │
│ is_up_trend     │ BOOLEAN         │ 上昇トレンド判定│ TRUE            │
│ is_down_trend   │ BOOLEAN         │ 下降トレンド判定│ FALSE           │
│ Up              │ BOOLEAN         │ 陽線判定        │ TRUE            │
│ Down            │ BOOLEAN         │ 陰線判定        │ FALSE           │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

## 2. ファイルシステム設計

### 2.1 ディレクトリ構造
```
KABUtrade/
├── data_cache/                 # データキャッシュディレクトリ
│   ├── {hash1}.csv            # 銘柄別キャッシュファイル
│   ├── {hash2}.csv            # 銘柄別キャッシュファイル
│   └── cache_index.json       # キャッシュインデックス（将来拡張）
│
├── src/
│   ├── symbols/               # 銘柄データ
│   │   ├── symbols_NY.csv     # 米国株銘柄リスト
│   │   └── symbols_JP.csv     # 日本株銘柄リスト
│   │
│   └── [application_code]/
│
├── test/                      # テストデータ
│   ├── test_data/             # テスト用データ
│   └── fixtures/              # テストフィクスチャ
│
├── logs/                      # ログファイル（将来拡張）
│   ├── application.log
│   └── error.log
│
└── config/                    # 設定ファイル（将来拡張）
    ├── production.json
    └── development.json
```

### 2.2 キャッシュファイル設計
```csv
# キャッシュファイル形式（CSV）
# ファイル名: {MD5_hash}.csv
# 例: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.csv

Date,Open,High,Low,Close,Volume
2024-01-15,150.25,152.80,149.90,151.50,1250000
2024-01-16,151.50,153.20,150.80,152.10,1180000
2024-01-17,152.10,154.00,151.50,153.75,1320000
...
```

### 2.3 銘柄リストファイル設計
```csv
# symbols_NY.csv (米国株)
symbol,company
SPY,S&P500
AAPL,Apple
TMF,米国債ブル３倍
TSLA,テスラ
T,AT＆T
DHI,DRホートン
SOXL,半導体３倍
VTI,全米

# symbols_JP.csv (日本株)
symbol,company
^N225,nikkei225
7203.T,トヨタ
7267.T,ホンダ
7011.T,三菱重工
9843.T,ニトリ
3038.T,神戸物産
6146.T,ディスコ
6857.T,アドバンテスト
2602.T,日清オイリオ
4540.T,ツムラ
7780.T,メニコン
```

## 3. データアクセス設計

### 3.1 データアクセス層
```python
class DataAccessLayer:
    """データアクセス層の抽象クラス"""
    
    def __init__(self, data_source: str):
        self.data_source = data_source
    
    def read_stock_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """株価データ読み込み"""
        pass
    
    def write_stock_data(self, symbol: str, data: pd.DataFrame) -> bool:
        """株価データ書き込み"""
        pass
    
    def read_symbol_list(self, market: str) -> List[str]:
        """銘柄リスト読み込み"""
        pass
    
    def cache_exists(self, symbol: str, period: str) -> bool:
        """キャッシュ存在チェック"""
        pass

class CSVDataAccess(DataAccessLayer):
    """CSVファイルベースのデータアクセス"""
    
    def __init__(self, cache_dir: str = "data_cache"):
        super().__init__("csv")
        self.cache_dir = cache_dir
    
    def read_stock_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """CSVファイルから株価データ読み込み"""
        cache_file = self._generate_cache_filename(symbol)
        if os.path.exists(cache_file):
            data = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            return data[(data.index >= start_date) & (data.index <= end_date)]
        return pd.DataFrame()
    
    def write_stock_data(self, symbol: str, data: pd.DataFrame) -> bool:
        """CSVファイルに株価データ書き込み"""
        try:
            cache_file = self._generate_cache_filename(symbol)
            data.to_csv(cache_file)
            return True
        except Exception as e:
            print(f"Failed to write data for {symbol}: {e}")
            return False
    
    def _generate_cache_filename(self, symbol: str) -> str:
        """キャッシュファイル名生成"""
        cache_key = f"{symbol}_1y_1d"
        cache_hash = hashlib.md5(cache_key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{cache_hash}.csv")

class APIDataAccess(DataAccessLayer):
    """APIベースのデータアクセス"""
    
    def __init__(self, api_type: str = "yahoo"):
        super().__init__(api_type)
        self.api_type = api_type
    
    def read_stock_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """APIから株価データ読み込み"""
        if self.api_type == "yahoo":
            return self._fetch_from_yahoo(symbol, start_date, end_date)
        elif self.api_type == "alpha_vantage":
            return self._fetch_from_alpha_vantage(symbol)
        return pd.DataFrame()
```

### 3.2 データ変換層
```python
class DataTransformLayer:
    """データ変換層"""
    
    @staticmethod
    def standardize_columns(data: pd.DataFrame) -> pd.DataFrame:
        """カラム名の標準化"""
        column_mapping = {
            'Open': '1. open',
            'High': '2. high',
            'Low': '3. low',
            'Close': '4. close',
            'Volume': '5. volume'
        }
        return data.rename(columns=column_mapping)
    
    @staticmethod
    def validate_data(data: pd.DataFrame) -> bool:
        """データ検証"""
        required_columns = ['1. open', '2. high', '3. low', '4. close', '5. volume']
        return all(col in data.columns for col in required_columns)
    
    @staticmethod
    def clean_data(data: pd.DataFrame) -> pd.DataFrame:
        """データクリーニング"""
        # 重複データの削除
        data = data.drop_duplicates()
        
        # 欠損値の処理
        data = data.dropna()
        
        # 異常値の処理
        for col in ['1. open', '2. high', '3. low', '4. close']:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            data = data[~((data[col] < (Q1 - 1.5 * IQR)) | 
                         (data[col] > (Q3 + 1.5 * IQR)))]
        
        return data
```

## 4. データ整合性設計

### 4.1 データ制約
```python
Data Constraints:
    - 日付: 有効な取引日（平日）
    - 価格: 正の数値
    - 出来高: 非負の整数
    - 高値 >= 始値, 終値, 安値
    - 安値 <= 始値, 終値, 高値
    - 移動平均値: 非負の数値
```

### 4.2 データ検証ルール
```python
class DataValidator:
    """データ検証クラス"""
    
    @staticmethod
    def validate_price_data(data: pd.DataFrame) -> List[str]:
        """価格データの検証"""
        errors = []
        
        # 基本的な価格制約チェック
        if (data['1. open'] <= 0).any():
            errors.append("Invalid open price: must be positive")
        
        if (data['2. high'] < data[['1. open', '3. low', '4. close']].max(axis=1)).any():
            errors.append("Invalid high price: must be highest")
        
        if (data['3. low'] > data[['1. open', '2. high', '4. close']].min(axis=1)).any():
            errors.append("Invalid low price: must be lowest")
        
        if (data['5. volume'] < 0).any():
            errors.append("Invalid volume: must be non-negative")
        
        return errors
    
    @staticmethod
    def validate_moving_averages(data: pd.DataFrame) -> List[str]:
        """移動平均データの検証"""
        errors = []
        
        # 移動平均の順序チェック（一般的な傾向）
        sma_columns = ['SMA_5', 'SMA_10', 'SMA_20', 'SMA_30', 'SMA_60', 'SMA_100', 'SMA_200', 'SMA_300']
        
        for col in sma_columns:
            if col in data.columns:
                if (data[col] <= 0).any():
                    errors.append(f"Invalid {col}: must be positive")
        
        return errors
```

## 5. パフォーマンス最適化

### 5.1 インデックス設計
```python
Index Design:
    - Primary Index: Date (DatetimeIndex)
    - Query Optimization: Date range queries
    - Memory Optimization: Categorical data for symbols
```

### 5.2 キャッシュ戦略
```python
Cache Strategy:
    - Cache Level: File-based (CSV)
    - Cache Key: MD5(symbol_period_interval)
    - Cache Expiration: 24 hours
    - Cache Size: 100MB limit
    - Cache Cleanup: LRU eviction
```

### 5.3 データ圧縮
```python
Data Compression:
    - CSV files: No compression (human-readable)
    - Future enhancement: Parquet format
    - Data types optimization: Float32 for prices
```

## 6. バックアップ・リカバリ設計

### 6.1 バックアップ戦略
```python
Backup Strategy:
    - Daily backup of cache files
    - Configuration files backup
    - Symbol lists backup
    - Version control for code
```

### 6.2 リカバリ手順
```python
Recovery Procedures:
    1. Cache corruption: Re-fetch from API
    2. Configuration loss: Restore from backup
    3. Symbol list corruption: Restore from backup
    4. System failure: Redeploy from Git
```

## 7. データ品質管理

### 7.1 データ品質指標
```python
Data Quality Metrics:
    - Completeness: 完全性（欠損値の割合）
    - Accuracy: 正確性（異常値の検出）
    - Consistency: 一貫性（データ形式の統一）
    - Timeliness: 適時性（データの新鮮度）
    - Validity: 有効性（制約条件の遵守）
```

### 7.2 データ品質監視
```python
class DataQualityMonitor:
    """データ品質監視クラス"""
    
    def __init__(self):
        self.quality_metrics = {}
    
    def check_completeness(self, data: pd.DataFrame) -> float:
        """完全性チェック"""
        total_cells = data.size
        missing_cells = data.isnull().sum().sum()
        return (total_cells - missing_cells) / total_cells
    
    def check_accuracy(self, data: pd.DataFrame) -> float:
        """正確性チェック"""
        # 異常値検出ロジック
        pass
    
    def generate_quality_report(self, data: pd.DataFrame) -> dict:
        """品質レポート生成"""
        return {
            'completeness': self.check_completeness(data),
            'accuracy': self.check_accuracy(data),
            'record_count': len(data),
            'date_range': f"{data.index.min()} to {data.index.max()}",
            'quality_score': self.calculate_quality_score(data)
        }
```

## 8. 将来拡張設計

### 8.1 データベース移行計画
```sql
-- 将来的なデータベース移行（SQLite → PostgreSQL）
CREATE TABLE stock_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    open_price DECIMAL(10,2) NOT NULL,
    high_price DECIMAL(10,2) NOT NULL,
    low_price DECIMAL(10,2) NOT NULL,
    close_price DECIMAL(10,2) NOT NULL,
    volume BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, date)
);

CREATE INDEX idx_stock_data_symbol_date ON stock_data(symbol, date);
CREATE INDEX idx_stock_data_date ON stock_data(date);
```

### 8.2 リアルタイムデータ対応
```python
Real-time Data Design:
    - WebSocket connection for live data
    - Stream processing for real-time signals
    - Event-driven architecture
    - Message queue integration
```

### 8.3 分散処理対応
```python
Distributed Processing:
    - Data partitioning by symbol
    - Distributed computing with Dask
    - Cluster deployment on cloud
    - Load balancing for API calls
```

## 9. ドメイン駆動設計（DDD）との統合

### 9.1 DDDアーキテクチャとデータモデリングの統合
```python
"""
DDDにおけるデータ設計原則:
1. 集約境界とデータ境界の整合性
2. エンティティ識別子による関連管理
3. 値オブジェクトの不変性保証
4. ドメインイベントのデータ整合性
"""

# 集約単位でのデータ設計
class StockPriceAggregate:
    """株価集約のデータ設計"""
    
    # 集約ルート
    stock_price_id: UUID          # エンティティ識別子
    symbol_code: str              # 銘柄コード（値オブジェクト）
    trade_date: date              # 取引日（値オブジェクト）
    
    # OHLCV値オブジェクト
    open_price: Decimal           # 始値
    high_price: Decimal           # 高値
    low_price: Decimal            # 安値
    close_price: Decimal          # 終値
    volume: BigInteger            # 出来高
    
    # 計算値（エンティティ内部状態）
    moving_averages: JSON         # 移動平均値
    technical_indicators: JSON    # テクニカル指標
    
    # メタデータ
    created_at: DateTime
    updated_at: DateTime
    version: Integer              # 楽観的ロック用

class TradingSignalAggregate:
    """売買シグナル集約のデータ設計"""
    
    # 集約ルート
    signal_id: UUID               # エンティティ識別子
    symbol_code: str              # 銘柄コード（外部集約への参照）
    
    # シグナル値オブジェクト
    signal_type: Enum             # Buy/Sell/Hold
    signal_kind: Enum             # GoldenCross/PPP等
    confidence: Decimal           # 信頼度（0-1）
    
    # 状態管理
    status: Enum                  # Active/Expired/Processed
    generated_at: DateTime
    expires_at: DateTime
    
    # ドメインイベント追跡
    domain_events: JSON           # 発生したドメインイベント履歴
    
    # メタデータ
    created_at: DateTime
    updated_at: DateTime
    version: Integer
```

### 9.2 境界付きコンテキスト別データモデル

#### 9.2.1 Market Analysis Context
```sql
-- 市場分析コンテキストのデータモデル
CREATE SCHEMA market_analysis;

-- 株価エンティティテーブル
CREATE TABLE market_analysis.stock_prices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol_code VARCHAR(20) NOT NULL,
    trade_date DATE NOT NULL,
    ohlcv_data JSONB NOT NULL,  -- OHLCV値オブジェクト
    technical_indicators JSONB, -- 計算済み指標
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1,
    UNIQUE(symbol_code, trade_date)
);

-- 移動平均計算結果テーブル
CREATE TABLE market_analysis.moving_averages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stock_price_id UUID REFERENCES market_analysis.stock_prices(id),
    period_type VARCHAR(10) NOT NULL, -- '5d', '10d', etc.
    average_value DECIMAL(10,2) NOT NULL,
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- インデックス設計
CREATE INDEX idx_stock_prices_symbol_date ON market_analysis.stock_prices(symbol_code, trade_date);
CREATE INDEX idx_stock_prices_date ON market_analysis.stock_prices(trade_date);
CREATE INDEX idx_moving_averages_stock_price ON market_analysis.moving_averages(stock_price_id);
```

#### 9.2.2 Signal Generation Context
```sql
-- シグナル生成コンテキストのデータモデル
CREATE SCHEMA signal_generation;

-- 売買シグナルテーブル
CREATE TABLE signal_generation.trading_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol_code VARCHAR(20) NOT NULL,
    signal_type VARCHAR(10) NOT NULL CHECK (signal_type IN ('Buy', 'Sell', 'Hold')),
    signal_kind VARCHAR(50) NOT NULL,
    confidence DECIMAL(3,2) NOT NULL CHECK (confidence BETWEEN 0 AND 1),
    status VARCHAR(20) NOT NULL DEFAULT 'Active',
    generated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB,  -- 追加情報
    domain_events JSONB DEFAULT '[]'::jsonb,  -- ドメインイベント履歴
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- シグナル履歴テーブル（イベントソーシング用）
CREATE TABLE signal_generation.signal_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    signal_id UUID REFERENCES signal_generation.trading_signals(id),
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB NOT NULL,
    occurred_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sequence_number SERIAL
);

-- インデックス設計
CREATE INDEX idx_trading_signals_symbol ON signal_generation.trading_signals(symbol_code);
CREATE INDEX idx_trading_signals_status ON signal_generation.trading_signals(status);
CREATE INDEX idx_trading_signals_generated ON signal_generation.trading_signals(generated_at);
CREATE INDEX idx_signal_events_signal_id ON signal_generation.signal_events(signal_id);
```

#### 9.2.3 Portfolio Management Context
```sql
-- ポートフォリオ管理コンテキストのデータモデル
CREATE SCHEMA portfolio_management;

-- ポートフォリオテーブル
CREATE TABLE portfolio_management.portfolios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    description TEXT,
    risk_profile VARCHAR(20),  -- Conservative/Moderate/Aggressive
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- ポートフォリオ保有銘柄テーブル
CREATE TABLE portfolio_management.portfolio_holdings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID REFERENCES portfolio_management.portfolios(id),
    symbol_code VARCHAR(20) NOT NULL,
    target_allocation DECIMAL(5,4) NOT NULL CHECK (target_allocation > 0 AND target_allocation <= 1),
    current_allocation DECIMAL(5,4),
    quantity INTEGER DEFAULT 0,
    average_cost DECIMAL(10,2),
    added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(portfolio_id, symbol_code)
);

-- ポートフォリオパフォーマンステーブル
CREATE TABLE portfolio_management.portfolio_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID REFERENCES portfolio_management.portfolios(id),
    calculation_date DATE NOT NULL,
    total_value DECIMAL(15,2),
    daily_return DECIMAL(8,6),
    cumulative_return DECIMAL(8,6),
    volatility DECIMAL(8,6),
    sharpe_ratio DECIMAL(8,6),
    max_drawdown DECIMAL(8,6),
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(portfolio_id, calculation_date)
);
```

#### 9.2.4 Notification Service Context
```sql
-- 通知サービスコンテキストのデータモデル
CREATE SCHEMA notification_service;

-- 通知テーブル
CREATE TABLE notification_service.notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipient VARCHAR(255) NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    subject VARCHAR(255),
    message TEXT NOT NULL,
    channel VARCHAR(20) NOT NULL DEFAULT 'email',  -- email/slack/line/push
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    priority VARCHAR(10) NOT NULL DEFAULT 'normal',  -- low/normal/high
    sent_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 通知設定テーブル
CREATE TABLE notification_service.notification_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(100) NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    channel VARCHAR(20) NOT NULL,
    enabled BOOLEAN DEFAULT true,
    frequency_limit INTEGER, -- 1時間あたりの最大通知数
    quiet_hours_start TIME,
    quiet_hours_end TIME,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, notification_type, channel)
);
```

### 9.3 ドメインイベントのデータ設計

#### 9.3.1 イベントストア設計
```sql
-- イベントストアのデータモデル
CREATE SCHEMA event_store;

-- ドメインイベントテーブル
CREATE TABLE event_store.domain_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_id UUID NOT NULL,           -- 集約ID
    aggregate_type VARCHAR(100) NOT NULL, -- 集約タイプ
    event_type VARCHAR(100) NOT NULL,     -- イベントタイプ
    event_version INTEGER NOT NULL,       -- イベントバージョン
    event_data JSONB NOT NULL,            -- イベントデータ
    metadata JSONB,                       -- メタデータ
    occurred_at TIMESTAMP WITH TIME ZONE NOT NULL,
    sequence_number BIGSERIAL,
    causation_id UUID,                    -- 原因となったイベントID
    correlation_id UUID                   -- 関連イベントグループID
);

-- イベント投影テーブル（読み取り専用ビュー）
CREATE TABLE event_store.read_model_signals (
    id UUID PRIMARY KEY,
    symbol_code VARCHAR(20) NOT NULL,
    latest_signal_type VARCHAR(10),
    latest_signal_kind VARCHAR(50),
    signal_count INTEGER DEFAULT 0,
    last_signal_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- インデックス設計
CREATE INDEX idx_domain_events_aggregate ON event_store.domain_events(aggregate_id, aggregate_type);
CREATE INDEX idx_domain_events_type ON event_store.domain_events(event_type);
CREATE INDEX idx_domain_events_occurred ON event_store.domain_events(occurred_at);
CREATE INDEX idx_domain_events_sequence ON event_store.domain_events(sequence_number);
```

#### 9.3.2 イベント処理パターン
```python
class EventStore:
    """イベントストア実装"""
    
    def save_events(self, aggregate_id: UUID, events: List[DomainEvent], 
                   expected_version: int) -> None:
        """イベント保存（楽観的ロック付き）"""
        with self.connection.begin():
            # バージョン確認
            current_version = self._get_current_version(aggregate_id)
            if current_version != expected_version:
                raise ConcurrencyException()
            
            # イベント保存
            for event in events:
                self._insert_event(aggregate_id, event)
    
    def get_events(self, aggregate_id: UUID, from_version: int = 0) -> List[DomainEvent]:
        """イベント取得"""
        return self._select_events(aggregate_id, from_version)

class EventProjector:
    """イベント投影（読み取りモデル更新）"""
    
    def project_signal_events(self, event: DomainEvent) -> None:
        """シグナルイベントの投影"""
        if isinstance(event, SignalGeneratedEvent):
            self._update_signal_read_model(event)
        elif isinstance(event, SignalExpiredEvent):
            self._update_signal_expiry(event)

class EventBus:
    """イベントバス実装"""
    
    def __init__(self):
        self.handlers = {}
    
    def register_handler(self, event_type: type, handler: callable) -> None:
        """イベントハンドラー登録"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
    
    def publish(self, event: DomainEvent) -> None:
        """イベント発行"""
        event_type = type(event)
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    # エラーハンドリング
                    self._handle_event_processing_error(event, handler, e)
```

### 9.4 データ整合性とトランザクション設計

#### 9.4.1 集約トランザクション境界
```python
class AggregateRepository:
    """集約リポジトリ基底クラス"""
    
    def save(self, aggregate: AggregateRoot) -> None:
        """集約保存（トランザクション境界）"""
        with self.unit_of_work.begin():
            # 1. 集約の永続化
            self._persist_aggregate(aggregate)
            
            # 2. ドメインイベントの保存
            for event in aggregate.domain_events:
                self.event_store.save_event(aggregate.id, event)
            
            # 3. イベント発行（コミット後）
            self.unit_of_work.register_post_commit(
                lambda: self._publish_events(aggregate.domain_events)
            )
            
            # 4. 集約のイベントクリア
            aggregate.clear_domain_events()

class UnitOfWork:
    """作業単位パターン実装"""
    
    def __init__(self, connection):
        self.connection = connection
        self.post_commit_callbacks = []
    
    def begin(self):
        return self.connection.begin()
    
    def register_post_commit(self, callback: callable) -> None:
        """コミット後コールバック登録"""
        self.post_commit_callbacks.append(callback)
    
    def commit(self) -> None:
        """コミット実行"""
        self.connection.commit()
        # コミット後処理実行
        for callback in self.post_commit_callbacks:
            try:
                callback()
            except Exception as e:
                # 補償処理やリトライ機能
                self._handle_post_commit_error(callback, e)
```

#### 9.4.2 結果整合性の実装
```python
class EventualConsistencyManager:
    """結果整合性管理"""
    
    def __init__(self, event_bus: EventBus, retry_policy: RetryPolicy):
        self.event_bus = event_bus
        self.retry_policy = retry_policy
    
    def handle_cross_context_consistency(self, event: DomainEvent) -> None:
        """コンテキスト間整合性処理"""
        if isinstance(event, SignalGeneratedEvent):
            # 通知コンテキストへの伝播
            self._propagate_to_notification_context(event)
            
            # ポートフォリオコンテキストへの伝播
            self._propagate_to_portfolio_context(event)
    
    def _propagate_to_notification_context(self, event: SignalGeneratedEvent) -> None:
        """通知コンテキストへの伝播"""
        try:
            notification_command = CreateNotificationCommand(
                signal_id=event.signal_id,
                symbol_code=event.symbol_code,
                signal_type=event.signal_type
            )
            self.command_bus.send(notification_command)
        except Exception as e:
            # リトライ機構
            self.retry_policy.retry(self._propagate_to_notification_context, event)
```

### 9.5 読み取りモデル最適化

#### 9.5.1 CQRS読み取りモデル設計
```sql
-- 読み取り専用ビューの作成
CREATE MATERIALIZED VIEW signal_dashboard AS
SELECT 
    s.symbol_code,
    s.signal_type,
    s.signal_kind,
    s.confidence,
    s.generated_at,
    sp.close_price as current_price,
    ma.sma_5,
    ma.sma_20,
    ma.sma_75
FROM signal_generation.trading_signals s
LEFT JOIN market_analysis.stock_prices sp ON s.symbol_code = sp.symbol_code
LEFT JOIN market_analysis.moving_averages ma ON sp.id = ma.stock_price_id
WHERE s.status = 'Active'
  AND sp.trade_date = (
      SELECT MAX(trade_date) 
      FROM market_analysis.stock_prices sp2 
      WHERE sp2.symbol_code = s.symbol_code
  );

-- インデックス最適化
CREATE INDEX idx_signal_dashboard_symbol ON signal_dashboard(symbol_code);
CREATE INDEX idx_signal_dashboard_type ON signal_dashboard(signal_type);
CREATE INDEX idx_signal_dashboard_generated ON signal_dashboard(generated_at);

-- ビューの定期更新
CREATE OR REPLACE FUNCTION refresh_signal_dashboard()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY signal_dashboard;
END;
$$ LANGUAGE plpgsql;

-- 定期実行ジョブ（例：5分毎）
SELECT cron.schedule('refresh-dashboard', '*/5 * * * *', 'SELECT refresh_signal_dashboard();');
```

### 9.6 DDDデータアクセスパターン

#### 9.6.1 リポジトリパターンの実装
```python
class PostgreSQLStockPriceRepository(StockPriceRepository):
    """PostgreSQL株価リポジトリ実装"""
    
    def __init__(self, connection_factory: ConnectionFactory):
        self.connection_factory = connection_factory
    
    def save(self, stock_price: StockPrice) -> None:
        """株価エンティティ保存"""
        with self.connection_factory.create() as conn:
            # エンティティをデータベーススキーマにマッピング
            query = """
                INSERT INTO market_analysis.stock_prices 
                (id, symbol_code, trade_date, ohlcv_data, technical_indicators, version)
                VALUES (%(id)s, %(symbol_code)s, %(trade_date)s, %(ohlcv_data)s, %(indicators)s, %(version)s)
                ON CONFLICT (symbol_code, trade_date) 
                DO UPDATE SET 
                    ohlcv_data = EXCLUDED.ohlcv_data,
                    technical_indicators = EXCLUDED.technical_indicators,
                    updated_at = NOW(),
                    version = stock_prices.version + 1
            """
            
            params = {
                'id': stock_price.id,
                'symbol_code': stock_price.symbol.symbol_code.value,
                'trade_date': stock_price.date,
                'ohlcv_data': self._serialize_ohlcv(stock_price.ohlcv),
                'indicators': self._serialize_indicators(stock_price.technical_indicators),
                'version': stock_price.version
            }
            
            conn.execute(query, params)
    
    def find_by_symbol_and_date_range(self, symbol: Symbol, 
                                    start_date: datetime, end_date: datetime) -> List[StockPrice]:
        """期間指定株価検索"""
        with self.connection_factory.create() as conn:
            query = """
                SELECT id, symbol_code, trade_date, ohlcv_data, technical_indicators, version
                FROM market_analysis.stock_prices 
                WHERE symbol_code = %(symbol_code)s 
                  AND trade_date BETWEEN %(start_date)s AND %(end_date)s
                ORDER BY trade_date
            """
            
            params = {
                'symbol_code': symbol.symbol_code.value,
                'start_date': start_date.date(),
                'end_date': end_date.date()
            }
            
            results = conn.execute(query, params).fetchall()
            return [self._map_to_entity(row) for row in results]
    
    def _map_to_entity(self, row) -> StockPrice:
        """データベース行をエンティティにマッピング"""
        symbol = Symbol(row['symbol_code'], "", Market.from_symbol(row['symbol_code']))
        ohlcv = self._deserialize_ohlcv(row['ohlcv_data'])
        indicators = self._deserialize_indicators(row['technical_indicators'])
        
        stock_price = StockPrice(symbol, row['trade_date'], ohlcv)
        stock_price.id = row['id']
        stock_price.technical_indicators = indicators
        stock_price.version = row['version']
        
        return stock_price
```

このDDDとデータ設計の統合により、以下の利点が得られます：

1. **ドメインモデルとデータモデルの整合性**: 集約境界とテーブル設計の一致
2. **トランザクション整合性**: 集約内の強整合性と集約間の結果整合性
3. **拡張性**: 新しい境界付きコンテキストの追加が容易
4. **パフォーマンス**: CQRS パターンによる読み取り最適化
5. **可監査性**: イベントソーシングによる変更履歴の完全な追跡

これらの設計原則により、KABUtradeシステムは複雑なドメインロジックを持ちながらも、高いパフォーマンスと拡張性を実現できます。
