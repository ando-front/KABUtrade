# KABUtrade機能拡張プロンプトテンプレート

## 1. 新機能開発プロンプトテンプレート

### 1.1 基本テンプレート
```
# KABUtrade機能拡張要求

## 背景・目的
【現在の課題】
- 既存機能の制限や問題点を記述
- ユーザーのニーズや要求を明確化

【追加したい機能】
- 具体的な機能要求を記述
- 期待される効果・価値を説明

## 技術要件
【アーキテクチャ制約】
- DDD（ドメイン駆動設計）に従った実装
- 既存の境界付きコンテキストとの整合性
- レイヤード アーキテクチャの遵守

【技術スタック】
- Python 3.9+
- pandas, numpy (データ処理)
- yfinance (株価データ取得)
- matplotlib/mplfinance (可視化)

【既存システムとの連携】
- 既存のドメインモデルとの整合性
- データフロー・API設計の一貫性
- 通知システムとの連携

## 実装指針
【ドメインモデリング】
- ユビキタス言語の定義
- エンティティ・値オブジェクトの設計
- 集約境界の明確化
- ドメインサービスの設計

【設計パターン】
- Factory パターンの活用
- Repository パターンの実装
- ドメインイベントの活用
- Strategy パターンの適用

【品質要件】
- 単体テスト: カバレッジ80%以上
- 統合テスト: 主要ユースケースの網羅
- パフォーマンス: 既存処理への影響最小化
- セキュリティ: API キー管理の適切性

## 成果物
【コード】
- ドメイン層の実装
- アプリケーション層の実装
- インフラストラクチャ層の実装
- テストコードの実装

【ドキュメント】
- 設計書の更新
- API仕様書の更新
- 運用手順書の更新

【検証】
- 機能テストの実施
- パフォーマンステストの実施
- セキュリティテストの実施
```

### 1.2 具体的な機能別テンプレート

#### 1.2.1 新しいテクニカル指標追加
```
# 新しいテクニカル指標追加要求

## 指標仕様
【指標名】: [指標名を記入]
【計算式】: [数式または計算ロジックを記入]
【パラメータ】: [期間、閾値等のパラメータを記入]
【シグナル条件】: [買い/売りシグナルの条件を記入]

## ドメインモデリング要求
【値オブジェクト】:
- 指標値を表現する値オブジェクトの設計
- バリデーションルールの定義

【エンティティ】:
- TechnicalIndicator エンティティの拡張
- 計算結果の管理方法

【ドメインサービス】:
- 指標計算ロジックの実装
- 既存指標との組み合わせロジック

【シグナル生成】:
- SignalGenerationService の拡張
- 新しい SignalKind の定義

## 実装要求
```python
# 期待する実装構造
class NewIndicator:
    \"\"\"新指標値オブジェクト\"\"\"
    def __init__(self, value: float, period: int):
        pass
    
    def is_bullish_signal(self) -> bool:
        \"\"\"買いシグナル判定\"\"\"
        pass

class NewIndicatorCalculator:
    \"\"\"新指標計算サービス\"\"\"
    def calculate(self, price_history: List[StockPrice]) -> NewIndicator:
        pass

# テストケース
class TestNewIndicator:
    def test_calculation_accuracy(self):
        pass
    
    def test_signal_detection(self):
        pass
```
```

#### 1.2.2 新しいデータソース追加
```
# 新しいデータソース追加要求

## データソース仕様
【データ提供者】: [API提供者名]
【API種別】: [REST API / WebSocket / その他]
【データ形式】: [JSON / CSV / その他]
【レート制限】: [呼び出し制限の詳細]
【認証方式】: [API Key / OAuth / その他]

## データ仕様
【取得可能データ】:
- 株価データ (OHLCV)
- リアルタイムデータ
- ファンダメンタルデータ
- その他

【データ品質】:
- 更新頻度
- 遅延時間
- データ精度

## 実装要求
【Data Integration Context の拡張】:
```python
class NewDataSource(DataSource):
    \"\"\"新データソース\"\"\"
    def __init__(self, api_key: str, rate_limit: RateLimit):
        pass
    
    def fetch_data(self, symbol: Symbol, date_range: DateRange) -> StockDataResponse:
        pass

class NewApiClient:
    \"\"\"新API クライアント\"\"\"
    def __init__(self, base_url: str, api_key: str):
        pass
    
    def get_stock_data(self, symbol: str) -> Dict:
        pass
```

【フォールバック戦略】:
- 主要データソースとの優先順位
- エラーハンドリング戦略
- キャッシュ戦略
```

#### 1.2.3 ポートフォリオ管理機能
```
# ポートフォリオ管理機能追加要求

## 機能仕様
【基本機能】:
- ポートフォリオ作成・編集・削除
- 銘柄の追加・削除・重み調整
- パフォーマンス計算
- リスク分析

【高度な機能】:
- 自動リバランシング
- リスク制限の設定
- ベンチマークとの比較

## ドメインモデル要求
【Portfolio Context の実装】:
```python
class Portfolio:
    \"\"\"ポートフォリオ集約ルート\"\"\"
    def add_position(self, symbol: Symbol, allocation: Percentage) -> None:
        pass
    
    def rebalance(self, target_allocations: Dict[Symbol, Percentage]) -> RebalanceOrder:
        pass
    
    def calculate_performance(self, period: DateRange) -> PerformanceMetrics:
        pass

class Position:
    \"\"\"ポジションエンティティ\"\"\"
    def __init__(self, symbol: Symbol, quantity: int, average_price: Price):
        pass

class RiskMetrics:
    \"\"\"リスク指標値オブジェクト\"\"\"
    def __init__(self, volatility: float, max_drawdown: float, sharpe_ratio: float):
        pass
```

【ドメインサービス】:
- PortfolioOptimizationService
- RiskCalculationService
- PerformanceAnalysisService
```

#### 1.2.4 アラート・通知機能強化
```
# アラート・通知機能強化要求

## 機能仕様
【アラート条件】:
- 価格閾値アラート
- 指標値アラート
- 出来高アラート
- ニュースアラート

【通知チャネル】:
- Email (既存)
- Slack
- LINE
- プッシュ通知

【通知設定】:
- 通知頻度制限
- 重要度別通知
- 時間帯制限

## 実装要求
【Notification Context の拡張】:
```python
class AlertRule:
    \"\"\"アラートルール集約ルート\"\"\"
    def __init__(self, rule_id: AlertRuleId, condition: AlertCondition, 
                 notification_channels: List[NotificationChannel]):
        pass
    
    def evaluate(self, market_data: MarketData) -> Optional[Alert]:
        pass

class AlertCondition:
    \"\"\"アラート条件値オブジェクト\"\"\"
    def __init__(self, indicator: TechnicalIndicator, operator: ComparisonOperator, 
                 threshold: float):
        pass

class NotificationChannel:
    \"\"\"通知チャネル値オブジェクト\"\"\"
    def __init__(self, channel_type: ChannelType, settings: Dict):
        pass
```

【通知サービス】:
- SlackNotificationService
- LineNotificationService
- PushNotificationService
```

## 2. バグ修正・改善プロンプトテンプレート

### 2.1 バグ修正テンプレート
```
# バグ修正要求

## 現象
【発生条件】: [バグが発生する具体的な条件]
【期待する動作】: [本来あるべき動作]
【実際の動作】: [現在の問題のある動作]
【影響範囲】: [バグによる影響の範囲]

## 技術情報
【エラーメッセージ】:
```
[エラーメッセージをここに貼り付け]
```

【関連ファイル】:
- [問題が発生している可能性のあるファイル一覧]

【実行環境】:
- Python バージョン
- OS
- 依存ライブラリバージョン

## 修正要求
【DDD原則の遵守】:
- ドメインロジックの整合性保持
- 集約境界の保護
- 不変条件の維持

【修正範囲】:
- 最小限の変更で修正
- 既存テストの破綻回避
- 新規テストケースの追加

【検証方法】:
- 単体テストによる検証
- 統合テストによる検証
- 手動テストによる検証
```

### 2.2 パフォーマンス改善テンプレート
```
# パフォーマンス改善要求

## 現状分析
【パフォーマンス問題】:
- 処理時間: [現在の処理時間]
- メモリ使用量: [現在のメモリ使用量]
- ボトルネック: [特定されたボトルネック]

【測定方法】:
- プロファイリングツール
- ベンチマークテスト
- 本番環境での監視結果

## 改善目標
【目標値】:
- 処理時間: [目標処理時間]
- メモリ使用量: [目標メモリ使用量]
- スループット: [目標スループット]

## 改善戦略
【アルゴリズム改善】:
- データ構造の最適化
- 計算アルゴリズムの改良
- キャッシュ戦略の見直し

【アーキテクチャ改善】:
- 並列処理の導入
- バッチ処理の最適化
- I/O処理の非同期化

【コード品質】:
- DDD原則の維持
- 可読性の保持
- テスト可能性の確保
```

## 3. コードレビュー基準プロンプト

### 3.1 DDD準拠チェックリスト
```
# DDDコードレビューチェックリスト

## ドメイン層
□ エンティティは一意識別子を持っているか
□ エンティティは不変条件を適切に保護しているか
□ 値オブジェクトは不変で等価性比較が実装されているか
□ 集約境界が適切に設定されているか
□ 集約ルート以外は外部から直接アクセスされていないか
□ ドメインサービスは状態を持たないか
□ ビジネスロジックがドメイン層に集約されているか

## アプリケーション層
□ ユースケースの調整のみを行っているか
□ ドメインロジックがアプリケーション層に漏れていないか
□ トランザクション境界が適切に設定されているか
□ ドメインイベントが適切に処理されているか

## インフラストラクチャ層
□ リポジトリ実装はドメインインターフェースに準拠しているか
□ 外部API呼び出しが適切に抽象化されているか
□ データ変換が適切に行われているか

## 共通
□ 依存性の方向が適切か（内側が外側に依存していないか）
□ テストが適切に書かれているか
□ 命名がユビキタス言語に準拠しているか
□ エラーハンドリングが適切に実装されているか
```

## 4. 機能テストプロンプトテンプレート

### 4.1 機能テスト仕様書生成
```
# 機能テスト仕様書生成要求

## テスト対象機能
【機能名】: [テスト対象の機能名]
【実装範囲】: [テスト対象の実装範囲]

## テストケース生成要求
【正常系テスト】:
- 基本的な動作テスト
- 境界値テスト
- 異なる条件でのテスト

【異常系テスト】:
- 不正な入力値テスト
- 外部API障害時テスト
- リソース不足時テスト

【統合テスト】:
- 他機能との連携テスト
- エンドツーエンドテスト

## テスト実装要求
【Given-When-Then形式】:
```python
def test_signal_generation_with_golden_cross():
    \"\"\"ゴールデンクロス発生時のシグナル生成テスト\"\"\"
    # Given
    symbol = Symbol("AAPL", "Apple Inc.", Market.US)
    price_history = create_golden_cross_pattern()
    
    # When
    signals = signal_generation_service.generate_signals(symbol, price_history)
    
    # Then
    assert len(signals) == 1
    assert signals[0].signal_type == SignalType.BUY
    assert signals[0].signal_kind == SignalKind.GOLDEN_CROSS
```

【テストデータ生成】:
- 実際の市場データに基づくテストデータ
- エッジケース用の合成データ
- パフォーマンステスト用の大容量データ
```

## 5. ドキュメント更新プロンプトテンプレート

### 5.1 設計書更新テンプレート
```
# 設計書更新要求

## 更新対象
【対象ドキュメント】:
- システム設計書
- DDD アーキテクチャ設計書
- データベース設計書
- API 仕様書

## 更新内容
【新機能の反映】:
- ドメインモデルの追加・変更
- アーキテクチャ図の更新
- データフロー図の更新
- API エンドポイントの追加

【既存機能の修正】:
- 仕様変更の反映
- バグ修正の記録
- パフォーマンス改善の記録

## 品質要求
【一貫性】:
- 既存ドキュメントとの整合性
- 命名規則の統一
- 図表の表現統一

【完全性】:
- 実装との整合性
- 他ドキュメントとの相互参照
- バージョン管理情報
```

このプロンプトテンプレート集を使用することで、KABUtradeシステムの機能拡張を体系的かつ効率的に行うことができます。各テンプレートは既存のDDD設計原則と整合性を保ちながら、高品質な実装を促進します。
