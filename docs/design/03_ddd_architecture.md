# ドメイン駆動設計（DDD）アーキテクチャ設計書 - KABUtrade

## 1. ドメイン分析

### 1.1 ユビキタス言語（Ubiquitous Language）
KABUtradeドメインにおける共通言語の定義

```
【核心概念】
- 銘柄（Symbol）: 取引対象となる株式や金融商品
- 株価（StockPrice）: 銘柄の市場価格情報
- 売買シグナル（TradingSignal）: 投資判断の指標
- 移動平均線（MovingAverage）: テクニカル分析指標
- トレンド（Trend）: 相場の方向性
- ポートフォリオ（Portfolio）: 投資対象の組み合わせ

【テクニカル分析用語】
- パンパカパン（PPP）: 移動平均線の理想的な配置
- ゴールデンクロス（GoldenCross）: 短期線が長期線を上抜く現象
- デッドクロス（DeadCross）: 短期線が長期線を下抜く現象
- 下半身（LowerHalf）: 押し目買いのシグナル
- くちばし（BirdBeak）: 移動平均線のクロスシグナル

【業務プロセス用語】
- 市場監視（MarketMonitoring）: 市場データの継続的な観測
- シグナル検出（SignalDetection）: 売買タイミングの特定
- 通知配信（NotificationDelivery）: シグナル発生時の通知
- バックテスト（Backtesting）: 過去データでの戦略検証
```

### 1.2 ドメインモデル概要
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        KABUtrade ドメインモデル                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    │
│  │   Market        │    │   Portfolio     │    │   Notification  │    │
│  │   Analysis      │    │   Management    │    │   Service       │    │
│  │   Domain        │    │   Domain        │    │   Domain        │    │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘    │
│                                                                         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    │
│  │   Data          │    │   Signal        │    │   Backtesting   │    │
│  │   Integration   │    │   Generation    │    │   Service       │    │
│  │   Domain        │    │   Domain        │    │   Domain        │    │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## 2. 境界付きコンテキスト（Bounded Context）

### 2.1 Market Analysis Context（市場分析コンテキスト）
```python
"""
責任範囲:
- 株価データの取得・管理
- テクニカル指標の計算
- 市場トレンドの分析
- 価格パターンの認識
"""

# エンティティ
class Symbol:
    """銘柄エンティティ"""
    def __init__(self, symbol_code: str, company_name: str, market: Market):
        self.symbol_code = SymbolCode(symbol_code)
        self.company_name = company_name
        self.market = market
        self.created_at = datetime.now()

class StockPrice:
    """株価エンティティ"""
    def __init__(self, symbol: Symbol, date: datetime, ohlcv: OHLCV):
        self.symbol = symbol
        self.date = date
        self.ohlcv = ohlcv
        self.domain_events = []

class TechnicalIndicator:
    """テクニカル指標エンティティ"""
    def __init__(self, symbol: Symbol, date: datetime, indicators: Dict):
        self.symbol = symbol
        self.date = date
        self.moving_averages = MovingAverages(indicators)
        self.trend_analysis = TrendAnalysis(indicators)

# 値オブジェクト
class SymbolCode:
    """銘柄コード値オブジェクト"""
    def __init__(self, code: str):
        self._validate(code)
        self.value = code
    
    def _validate(self, code: str):
        if not code or not isinstance(code, str):
            raise ValueError("Invalid symbol code")

class OHLCV:
    """OHLCV値オブジェクト"""
    def __init__(self, open_price: float, high: float, low: float, close: float, volume: int):
        self._validate(open_price, high, low, close, volume)
        self.open = Price(open_price)
        self.high = Price(high)
        self.low = Price(low)
        self.close = Price(close)
        self.volume = Volume(volume)
    
    def _validate(self, open_price: float, high: float, low: float, close: float, volume: int):
        if high < max(open_price, close, low) or low > min(open_price, close, high):
            raise ValueError("Invalid OHLCV data")

class MovingAverages:
    """移動平均値オブジェクト"""
    def __init__(self, sma_values: Dict[int, float]):
        self.sma_5 = Price(sma_values.get(5, 0))
        self.sma_10 = Price(sma_values.get(10, 0))
        self.sma_20 = Price(sma_values.get(20, 0))
        self.sma_25 = Price(sma_values.get(25, 0))
        self.sma_30 = Price(sma_values.get(30, 0))
        self.sma_60 = Price(sma_values.get(60, 0))
        self.sma_75 = Price(sma_values.get(75, 0))
        self.sma_100 = Price(sma_values.get(100, 0))
        self.sma_200 = Price(sma_values.get(200, 0))
        self.sma_300 = Price(sma_values.get(300, 0))
    
    def is_ppp_formation(self) -> bool:
        """パンパカパン形成の判定"""
        return (self.sma_5.value > self.sma_20.value > self.sma_60.value > 
                self.sma_100.value > self.sma_200.value > self.sma_300.value)

# ドメインサービス
class TechnicalAnalysisService:
    """テクニカル分析ドメインサービス"""
    
    def calculate_moving_averages(self, price_history: List[StockPrice]) -> MovingAverages:
        """移動平均線計算"""
        # 移動平均計算ロジック
        pass
    
    def detect_trend(self, price_history: List[StockPrice]) -> TrendAnalysis:
        """トレンド検出"""
        # トレンド検出ロジック
        pass

# リポジトリインターフェース
class StockPriceRepository:
    """株価リポジトリインターフェース"""
    
    def save(self, stock_price: StockPrice) -> None:
        pass
    
    def find_by_symbol_and_date_range(self, symbol: Symbol, start_date: datetime, end_date: datetime) -> List[StockPrice]:
        pass
    
    def find_latest_by_symbol(self, symbol: Symbol) -> Optional[StockPrice]:
        pass
```

### 2.2 Signal Generation Context（シグナル生成コンテキスト）
```python
"""
責任範囲:
- 売買シグナルの生成
- シグナルの評価・優先順位付け
- シグナルの履歴管理
"""

# 集約ルート
class TradingSignal:
    """売買シグナル集約ルート"""
    def __init__(self, symbol: Symbol, signal_type: SignalType, signal_kind: SignalKind, 
                 confidence: float, generated_at: datetime):
        self.id = SignalId.generate()
        self.symbol = symbol
        self.signal_type = signal_type
        self.signal_kind = signal_kind
        self.confidence = Confidence(confidence)
        self.generated_at = generated_at
        self.status = SignalStatus.ACTIVE
        self.domain_events = []
    
    def evaluate_signal(self, market_condition: MarketCondition) -> None:
        """シグナルの評価"""
        if self.confidence.value < 0.5:
            self.status = SignalStatus.LOW_CONFIDENCE
        
        # ドメインイベント発行
        self.domain_events.append(SignalEvaluatedEvent(self.id, self.confidence))
    
    def expire_signal(self) -> None:
        """シグナルの期限切れ"""
        self.status = SignalStatus.EXPIRED
        self.domain_events.append(SignalExpiredEvent(self.id))

# 値オブジェクト
class SignalType(Enum):
    """シグナル種別"""
    BUY = "Buy"
    SELL = "Sell"
    HOLD = "Hold"

class SignalKind(Enum):
    """シグナル種類"""
    GOLDEN_CROSS = "Golden Cross"
    DEAD_CROSS = "Dead Cross"
    PPP = "PPP"
    REVERSE_PPP = "Reverse PPP"
    LOWER_HALF = "Lower Half"
    REVERSE_LOWER_HALF = "Reverse Lower Half"
    BIRD_BEAK = "Bird Beak"
    REVERSE_BIRD_BEAK = "Reverse Bird Beak"
    CONSECUTIVE_UP_9 = "Up for 9 days"
    CONSECUTIVE_DOWN_9 = "Down for 9 days"
    CONSECUTIVE_UP_13 = "Up for 13 days"
    CONSECUTIVE_DOWN_13 = "Down for 13 days"

class Confidence:
    """信頼度値オブジェクト"""
    def __init__(self, value: float):
        if not 0 <= value <= 1:
            raise ValueError("Confidence must be between 0 and 1")
        self.value = value

# ドメインサービス
class SignalGenerationService:
    """シグナル生成ドメインサービス"""
    
    def generate_cross_signals(self, technical_indicator: TechnicalIndicator) -> List[TradingSignal]:
        """クロスシグナル生成"""
        signals = []
        
        # ゴールデンクロス検出
        if self._is_golden_cross(technical_indicator):
            signal = TradingSignal(
                symbol=technical_indicator.symbol,
                signal_type=SignalType.BUY,
                signal_kind=SignalKind.GOLDEN_CROSS,
                confidence=0.8,
                generated_at=datetime.now()
            )
            signals.append(signal)
        
        return signals
    
    def _is_golden_cross(self, indicator: TechnicalIndicator) -> bool:
        """ゴールデンクロス判定"""
        return (indicator.moving_averages.sma_25.value > indicator.moving_averages.sma_75.value)

# ファクトリー
class SignalFactory:
    """シグナルファクトリー"""
    
    @staticmethod
    def create_ppp_signal(symbol: Symbol, moving_averages: MovingAverages) -> TradingSignal:
        """PPPシグナル生成"""
        if moving_averages.is_ppp_formation():
            return TradingSignal(
                symbol=symbol,
                signal_type=SignalType.BUY,
                signal_kind=SignalKind.PPP,
                confidence=0.9,
                generated_at=datetime.now()
            )
        return None
```

### 2.3 Portfolio Management Context（ポートフォリオ管理コンテキスト）
```python
"""
責任範囲:
- 投資対象銘柄の管理
- ポートフォリオの構成管理
- リスク管理
"""

# 集約ルート
class Portfolio:
    """ポートフォリオ集約ルート"""
    def __init__(self, portfolio_id: PortfolioId, name: str, owner: str):
        self.id = portfolio_id
        self.name = name
        self.owner = owner
        self.holdings = []
        self.created_at = datetime.now()
        self.domain_events = []
    
    def add_symbol(self, symbol: Symbol, allocation: float) -> None:
        """銘柄追加"""
        if allocation <= 0 or allocation > 1:
            raise ValueError("Invalid allocation")
        
        holding = Holding(symbol, allocation)
        self.holdings.append(holding)
        self.domain_events.append(SymbolAddedEvent(self.id, symbol))
    
    def remove_symbol(self, symbol: Symbol) -> None:
        """銘柄削除"""
        self.holdings = [h for h in self.holdings if h.symbol != symbol]
        self.domain_events.append(SymbolRemovedEvent(self.id, symbol))
    
    def rebalance(self) -> None:
        """リバランス"""
        # リバランスロジック
        self.domain_events.append(PortfolioRebalancedEvent(self.id))

class Holding:
    """保有銘柄エンティティ"""
    def __init__(self, symbol: Symbol, allocation: float):
        self.symbol = symbol
        self.allocation = Allocation(allocation)
        self.added_at = datetime.now()

class Allocation:
    """配分値オブジェクト"""
    def __init__(self, percentage: float):
        if not 0 < percentage <= 1:
            raise ValueError("Allocation must be between 0 and 1")
        self.percentage = percentage
```

### 2.4 Notification Service Context（通知サービスコンテキスト）
```python
"""
責任範囲:
- 通知の配信
- 通知履歴の管理
- 通知設定の管理
"""

# 集約ルート
class Notification:
    """通知集約ルート"""
    def __init__(self, notification_id: NotificationId, recipient: str, 
                 message: str, notification_type: NotificationType):
        self.id = notification_id
        self.recipient = EmailAddress(recipient)
        self.message = message
        self.notification_type = notification_type
        self.status = NotificationStatus.PENDING
        self.created_at = datetime.now()
        self.sent_at = None
        self.domain_events = []
    
    def send(self) -> None:
        """通知送信"""
        self.status = NotificationStatus.SENT
        self.sent_at = datetime.now()
        self.domain_events.append(NotificationSentEvent(self.id))
    
    def fail(self, error: str) -> None:
        """送信失敗"""
        self.status = NotificationStatus.FAILED
        self.error_message = error
        self.domain_events.append(NotificationFailedEvent(self.id, error))

class NotificationType(Enum):
    """通知種別"""
    SIGNAL_ALERT = "Signal Alert"
    SYSTEM_NOTIFICATION = "System Notification"
    ERROR_ALERT = "Error Alert"

class NotificationStatus(Enum):
    """通知状態"""
    PENDING = "Pending"
    SENT = "Sent"
    FAILED = "Failed"
    EXPIRED = "Expired"

# ドメインサービス
class NotificationService:
    """通知ドメインサービス"""
    
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository
    
    def send_signal_notification(self, signal: TradingSignal, recipient: str) -> None:
        """シグナル通知送信"""
        message = self._create_signal_message(signal)
        notification = Notification(
            notification_id=NotificationId.generate(),
            recipient=recipient,
            message=message,
            notification_type=NotificationType.SIGNAL_ALERT
        )
        
        self.notification_repository.save(notification)
        notification.send()
    
    def _create_signal_message(self, signal: TradingSignal) -> str:
        """シグナル通知メッセージ作成"""
        return f"{signal.symbol.symbol_code.value}の{signal.signal_type.value}シグナル（{signal.signal_kind.value}）が発生しました。"
```

### 2.5 Data Integration Context（データ統合コンテキスト）
```python
"""
責任範囲:
- 外部APIとの連携
- データの統合・変換
- キャッシュ管理
"""

# 集約ルート
class DataSource:
    """データソース集約ルート"""
    def __init__(self, source_id: DataSourceId, name: str, api_type: ApiType):
        self.id = source_id
        self.name = name
        self.api_type = api_type
        self.status = DataSourceStatus.ACTIVE
        self.rate_limit = RateLimit(requests_per_minute=60)
        self.last_request_at = None
        self.domain_events = []
    
    def fetch_data(self, symbol: Symbol, date_range: DateRange) -> StockDataResponse:
        """データ取得"""
        if not self._can_make_request():
            raise RateLimitExceededException("Rate limit exceeded")
        
        self.last_request_at = datetime.now()
        # データ取得ロジック
        return StockDataResponse(symbol, date_range, [])
    
    def _can_make_request(self) -> bool:
        """リクエスト可能性チェック"""
        if self.last_request_at is None:
            return True
        
        time_since_last = datetime.now() - self.last_request_at
        return time_since_last.total_seconds() >= 60 / self.rate_limit.requests_per_minute

class ApiType(Enum):
    """API種別"""
    YAHOO_FINANCE = "Yahoo Finance"
    ALPHA_VANTAGE = "Alpha Vantage"

class RateLimit:
    """レート制限値オブジェクト"""
    def __init__(self, requests_per_minute: int):
        self.requests_per_minute = requests_per_minute

# ドメインサービス
class DataIntegrationService:
    """データ統合ドメインサービス"""
    
    def __init__(self, data_sources: List[DataSource]):
        self.data_sources = data_sources
        self.primary_source = data_sources[0]
        self.fallback_sources = data_sources[1:]
    
    def fetch_stock_data(self, symbol: Symbol, date_range: DateRange) -> List[StockPrice]:
        """株価データ取得（フォールバック付き）"""
        for source in [self.primary_source] + self.fallback_sources:
            try:
                response = source.fetch_data(symbol, date_range)
                return self._convert_to_stock_prices(response)
            except Exception as e:
                continue
        
        raise DataUnavailableException("No data source available")
    
    def _convert_to_stock_prices(self, response: StockDataResponse) -> List[StockPrice]:
        """レスポンスを株価エンティティに変換"""
        # 変換ロジック
        pass
```

## 3. アプリケーションサービス層

### 3.1 アプリケーションサービス
```python
class MarketAnalysisApplicationService:
    """市場分析アプリケーションサービス"""
    
    def __init__(self, 
                 stock_price_repository: StockPriceRepository,
                 signal_repository: SignalRepository,
                 data_integration_service: DataIntegrationService,
                 signal_generation_service: SignalGenerationService):
        self.stock_price_repository = stock_price_repository
        self.signal_repository = signal_repository
        self.data_integration_service = data_integration_service
        self.signal_generation_service = signal_generation_service
    
    def analyze_market_and_generate_signals(self, symbols: List[Symbol]) -> List[TradingSignal]:
        """市場分析とシグナル生成"""
        all_signals = []
        
        for symbol in symbols:
            # 株価データ取得
            date_range = DateRange(datetime.now() - timedelta(days=365), datetime.now())
            price_history = self.data_integration_service.fetch_stock_data(symbol, date_range)
            
            # 最新価格の保存
            if price_history:
                latest_price = price_history[-1]
                self.stock_price_repository.save(latest_price)
            
            # テクニカル指標計算
            technical_analysis_service = TechnicalAnalysisService()
            moving_averages = technical_analysis_service.calculate_moving_averages(price_history)
            
            # シグナル生成
            signals = self.signal_generation_service.generate_all_signals(symbol, moving_averages)
            
            for signal in signals:
                self.signal_repository.save(signal)
                all_signals.append(signal)
        
        return all_signals

class NotificationApplicationService:
    """通知アプリケーションサービス"""
    
    def __init__(self, 
                 notification_repository: NotificationRepository,
                 notification_service: NotificationService):
        self.notification_repository = notification_repository
        self.notification_service = notification_service
    
    def send_signal_notifications(self, signals: List[TradingSignal], recipients: List[str]) -> None:
        """シグナル通知送信"""
        for signal in signals:
            for recipient in recipients:
                self.notification_service.send_signal_notification(signal, recipient)
```

### 3.2 ドメインイベントハンドラー
```python
class SignalGeneratedEventHandler:
    """シグナル生成イベントハンドラー"""
    
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service
    
    def handle(self, event: SignalGeneratedEvent) -> None:
        """シグナル生成イベント処理"""
        # 通知送信
        self.notification_service.send_signal_notification(event.signal, "investor@example.com")

class MarketDataUpdatedEventHandler:
    """市場データ更新イベントハンドラー"""
    
    def __init__(self, signal_generation_service: SignalGenerationService):
        self.signal_generation_service = signal_generation_service
    
    def handle(self, event: MarketDataUpdatedEvent) -> None:
        """市場データ更新イベント処理"""
        # 新しいシグナルの生成をトリガー
        signals = self.signal_generation_service.generate_all_signals(
            event.symbol, event.technical_indicator
        )
```

## 4. インフラストラクチャ層

### 4.1 リポジトリ実装
```python
class CSVStockPriceRepository(StockPriceRepository):
    """CSV株価リポジトリ実装"""
    
    def __init__(self, cache_directory: str):
        self.cache_directory = cache_directory
    
    def save(self, stock_price: StockPrice) -> None:
        """株価データ保存"""
        # CSV保存実装
        pass
    
    def find_by_symbol_and_date_range(self, symbol: Symbol, start_date: datetime, end_date: datetime) -> List[StockPrice]:
        """期間指定で株価データ取得"""
        # CSV読み込み実装
        pass

class InMemorySignalRepository(SignalRepository):
    """インメモリシグナルリポジトリ実装"""
    
    def __init__(self):
        self.signals = {}
    
    def save(self, signal: TradingSignal) -> None:
        """シグナル保存"""
        self.signals[signal.id] = signal
    
    def find_by_symbol(self, symbol: Symbol) -> List[TradingSignal]:
        """銘柄別シグナル取得"""
        return [s for s in self.signals.values() if s.symbol == symbol]
```

### 4.2 外部API実装
```python
class YahooFinanceApiClient:
    """Yahoo Finance APIクライアント"""
    
    def __init__(self, rate_limiter: RateLimiter):
        self.rate_limiter = rate_limiter
    
    def fetch_stock_data(self, symbol_code: str, period: str) -> Dict:
        """株価データ取得"""
        with self.rate_limiter:
            # Yahoo Finance API呼び出し
            pass

class GoogleAppsScriptNotificationClient:
    """Google Apps Script通知クライアント"""
    
    def __init__(self, gas_url: str):
        self.gas_url = gas_url
    
    def send_notification(self, message: str, recipient: str) -> bool:
        """通知送信"""
        # GAS API呼び出し
        pass
```

## 5. DDDパターンの適用

### 5.1 集約（Aggregate）の設計原則
```python
"""
集約設計原則:
1. 不変条件の保護
2. トランザクション境界の明確化
3. 集約間の参照は IDのみ
4. 集約のサイズは小さく保つ
"""

class TradingSignal:  # 集約ルート
    def __init__(self, ...):
        # 不変条件: 信頼度は0-1の範囲
        self.confidence = Confidence(confidence)
        # 不変条件: 生成日時は現在時刻以前
        if generated_at > datetime.now():
            raise ValueError("Generated time cannot be in the future")
    
    def expire_signal(self):
        # ビジネスルール: アクティブなシグナルのみ期限切れ可能
        if self.status != SignalStatus.ACTIVE:
            raise ValueError("Only active signals can be expired")
        
        self.status = SignalStatus.EXPIRED
        self.domain_events.append(SignalExpiredEvent(self.id))
```

### 5.2 ドメインイベント
```python
class SignalGeneratedEvent:
    """シグナル生成イベント"""
    def __init__(self, signal_id: SignalId, symbol: Symbol, signal_type: SignalType):
        self.signal_id = signal_id
        self.symbol = symbol
        self.signal_type = signal_type
        self.occurred_at = datetime.now()

class MarketDataUpdatedEvent:
    """市場データ更新イベント"""
    def __init__(self, symbol: Symbol, price_data: StockPrice):
        self.symbol = symbol
        self.price_data = price_data
        self.occurred_at = datetime.now()
```

### 5.3 ドメインサービス vs アプリケーションサービス
```python
"""
ドメインサービス:
- 複数の集約にまたがるビジネスロジック
- ドメインの知識を持つ
- 状態を持たない

アプリケーションサービス:
- ユースケースの調整
- トランザクションの管理
- ドメインオブジェクトの協調
"""

# ドメインサービス例
class SignalGenerationService:
    def generate_cross_signals(self, technical_indicator: TechnicalIndicator) -> List[TradingSignal]:
        # 純粋なドメインロジック
        pass

# アプリケーションサービス例
class MarketAnalysisApplicationService:
    def analyze_market_and_generate_signals(self, symbols: List[Symbol]) -> List[TradingSignal]:
        # ユースケースの調整
        # 1. データ取得
        # 2. 分析実行
        # 3. シグナル生成
        # 4. 永続化
        pass
```

## 6. 戦略的設計

### 6.1 コンテキストマップ
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        KABUtrade Context Map                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    │
│  │   Market        │    │   Signal        │    │   Portfolio     │    │
│  │   Analysis      │◄──►│   Generation    │◄──►│   Management    │    │
│  │   Context       │    │   Context       │    │   Context       │    │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘    │
│           │                        │                        │          │
│           │                        │                        │          │
│           ▼                        ▼                        ▼          │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    │
│  │   Data          │    │   Notification  │    │   Backtesting   │    │
│  │   Integration   │◄──►│   Service       │◄──►│   Service       │    │
│  │   Context       │    │   Context       │    │   Context       │    │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

関係性:
- Market Analysis ↔ Signal Generation: 共有カーネル
- Signal Generation ↔ Notification: 顧客・供給者
- Portfolio Management ↔ Backtesting: パートナーシップ
- Data Integration: 汎用サブドメイン
```

### 6.2 アーキテクチャ決定記録（ADR）
```markdown
# ADR-001: ドメイン駆動設計の採用

## 状況
複雑な投資判断ロジックを持つKABUtradeシステムにおいて、
ビジネスロジックとインフラストラクチャの分離が必要。

## 決定
ドメイン駆動設計（DDD）を採用し、以下の構造を採用する:
- 境界付きコンテキストによる責任の分離
- 集約による一貫性の保証
- ドメインイベントによる疎結合

## 結果
- ビジネスロジックの可読性向上
- テストの容易性向上
- 拡張性の向上
- 学習コストの増加
```

## 7. 実装ガイドライン

### 7.1 ディレクトリ構造
```
src/
├── domain/
│   ├── market_analysis/
│   │   ├── entities/
│   │   │   ├── symbol.py
│   │   │   ├── stock_price.py
│   │   │   └── technical_indicator.py
│   │   ├── value_objects/
│   │   │   ├── symbol_code.py
│   │   │   ├── ohlcv.py
│   │   │   └── moving_averages.py
│   │   ├── services/
│   │   │   └── technical_analysis_service.py
│   │   └── repositories/
│   │       └── stock_price_repository.py
│   │
│   ├── signal_generation/
│   │   ├── entities/
│   │   │   └── trading_signal.py
│   │   ├── value_objects/
│   │   │   ├── signal_type.py
│   │   │   └── confidence.py
│   │   ├── services/
│   │   │   └── signal_generation_service.py
│   │   └── repositories/
│   │       └── signal_repository.py
│   │
│   └── shared/
│       ├── value_objects/
│       │   ├── price.py
│       │   └── date_range.py
│       └── events/
│           └── domain_event.py
│
├── application/
│   ├── services/
│   │   ├── market_analysis_application_service.py
│   │   └── notification_application_service.py
│   └── event_handlers/
│       ├── signal_generated_event_handler.py
│       └── market_data_updated_event_handler.py
│
├── infrastructure/
│   ├── repositories/
│   │   ├── csv_stock_price_repository.py
│   │   └── in_memory_signal_repository.py
│   ├── external_apis/
│   │   ├── yahoo_finance_api_client.py
│   │   └── google_apps_script_client.py
│   └── event_bus/
│       └── in_memory_event_bus.py
│
└── presentation/
    ├── cli/
    │   └── main.py
    └── api/
        └── rest_api.py
```

### 7.2 コーディング規約
```python
"""
DDDコーディング規約:

1. エンティティ
   - 一意識別子を持つ
   - ビジネスロジックをメソッドとして実装
   - 不変条件を保護

2. 値オブジェクト
   - 不変
   - 等価性比較を実装
   - バリデーションを含む

3. 集約
   - 集約ルートを通じてのみアクセス
   - 不変条件を保護
   - ドメインイベントを発行

4. ドメインサービス
   - 状態を持たない
   - 複数の集約にまたがるロジック
   - ドメインの知識を持つ

5. リポジトリ
   - 集約の永続化を抽象化
   - コレクションライクなインターフェース
   - ドメイン層でインターフェース定義
"""
```

## 8. テスト戦略

### 8.1 テストピラミッド
```python
"""
テストピラミッド:

1. 単体テスト（多数）
   - ドメインエンティティのテスト
   - 値オブジェクトのテスト
   - ドメインサービスのテスト

2. 統合テスト（中程度）
   - アプリケーションサービスのテスト
   - リポジトリ実装のテスト
   - 外部API連携のテスト

3. E2Eテスト（少数）
   - ユースケース全体のテスト
   - システム間連携のテスト
"""

# ドメインエンティティのテスト例
class TestTradingSignal:
    def test_signal_creation_with_valid_data(self):
        signal = TradingSignal(
            symbol=Symbol("AAPL", "Apple Inc.", Market.US),
            signal_type=SignalType.BUY,
            signal_kind=SignalKind.GOLDEN_CROSS,
            confidence=0.8,
            generated_at=datetime.now()
        )
        
        assert signal.signal_type == SignalType.BUY
        assert signal.status == SignalStatus.ACTIVE
    
    def test_signal_expiration(self):
        signal = TradingSignal(...)
        signal.expire_signal()
        
        assert signal.status == SignalStatus.EXPIRED
        assert len(signal.domain_events) == 1
        assert isinstance(signal.domain_events[0], SignalExpiredEvent)

# アプリケーションサービスのテスト例
class TestMarketAnalysisApplicationService:
    def test_analyze_market_and_generate_signals(self):
        # Arrange
        service = MarketAnalysisApplicationService(...)
        symbols = [Symbol("AAPL", "Apple Inc.", Market.US)]
        
        # Act
        signals = service.analyze_market_and_generate_signals(symbols)
        
        # Assert
        assert len(signals) > 0
        assert all(isinstance(s, TradingSignal) for s in signals)
```

この設計により、KABUtradeシステムは以下の特徴を持ちます：

1. **ドメインロジックの明確化**: ビジネスルールがドメイン層に集約
2. **拡張性**: 新しい機能を境界付きコンテキストとして追加可能
3. **テスト容易性**: 各層が疎結合でテスト可能
4. **保守性**: 責任の分離により変更影響を局所化

これらの設計原則に従うことで、複雑な投資判断システムを持続可能な形で開発・運用できます。
