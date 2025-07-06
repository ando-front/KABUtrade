# KABUtrade システムドキュメント インデックス

## ドキュメント構成

### 📋 要件定義書
- **[01_business_requirements.md](requirements/01_business_requirements.md)** - 業務要求仕様書
  - プロジェクト概要
  - 業務要求・機能要求
  - 非機能要求・制約事項
  - 成功基準・リスク管理

- **[02_technical_requirements.md](requirements/02_technical_requirements.md)** - 技術要求仕様書
  - システム概要・技術スタック
  - アーキテクチャ設計
  - データ仕様・API仕様
  - アルゴリズム仕様

### 🏗️ 設計書
- **[01_system_design.md](design/01_system_design.md)** - システム設計書
  - システム構成図・データフロー図
  - クラス設計・API設計
  - アルゴリズム設計・エラーハンドリング
  - パフォーマンス・セキュリティ設計

- **[02_database_design.md](design/02_database_design.md)** - データベース設計書
  - データ構造設計
  - ファイルシステム設計
  - データアクセス層設計
  - データ整合性・品質管理

- **[03_ddd_architecture.md](design/03_ddd_architecture.md)** - ドメイン駆動設計（DDD）アーキテクチャ設計書
  - ドメイン分析・ユビキタス言語
  - 境界付きコンテキスト設計
  - 集約・エンティティ・値オブジェクト設計
  - アプリケーションサービス・ドメインサービス設計

### 🛠️ 開発手順書
- **[01_development_guide.md](development/01_development_guide.md)** - 開発手順書
  - 開発環境構築
  - プロジェクト構造理解
  - 開発ワークフロー
  - 機能開発・テスト・デバッグ手順

- **[02_feature_extension_prompts.md](development/02_feature_extension_prompts.md)** - 機能拡張プロンプトテンプレート集
  - 新機能開発プロンプトテンプレート
  - バグ修正・改善プロンプトテンプレート
  - コードレビュー基準・機能テスト仕様書生成
  - ドキュメント更新プロンプトテンプレート

### 🚀 運用手順書
- **[01_operations_manual.md](operations/01_operations_manual.md)** - 運用手順書
  - 日次・週次・月次運用手順
  - 障害対応手順
  - メンテナンス手順
  - 監視・バックアップ・セキュリティ運用

- **[02_backtest_results.md](operations/02_backtest_results.md)** - バックテスト結果レポート
  - Aibaメソッドの実行結果
  - シグナル生成分析
  - パフォーマンス評価

## システム概要

### プロジェクト名
**KABUtrade - 株式売買シグナル自動生成・通知システム**

### 目的
株式市場における売買のタイミングを自動的に判定し、相場式投資手法に基づく高度な分析アルゴリズムによってメール通知を行う投資判断支援システム

### 主要機能
1. **データ取得機能**
   - Yahoo Finance API / Alpha Vantage API
   - 日本株・米国株対応
   - キャッシュ機能搭載

2. **分析機能**
   - 移動平均線計算（5〜300日）
   - トレンド分析（上昇・下降トレンド判定）
   - 技術的指標計算

3. **シグナル生成機能**
   - 75日線ブレイクアウト
   - ゴールデンクロス・デッドクロス
   - パンパカパン（PPP）
   - 下半身・くちばし（相場式投資手法）
   - 連続陰線・陽線（9日・13日）

4. **通知機能**
   - Google Apps Script経由メール通知
   - シグナル詳細情報付き

5. **バックテスト機能**
   - 過去データでの戦略検証
   - パフォーマンス評価

### 技術スタック
- **言語**: Python 3.9.18
- **主要ライブラリ**: pandas, numpy, yfinance, matplotlib
- **デプロイ**: GitHub Actions (Ubuntu Latest)
- **通知**: Google Apps Script
- **データ保存**: CSV (ローカルキャッシュ)

### 対象銘柄
**米国株（8銘柄）**: SPY, AAPL, TMF, TSLA, T, DHI, SOXL, VTI  
**日本株（11銘柄）**: ^N225, トヨタ, ホンダ, 三菱重工, ニトリ, 神戸物産, ディスコ, アドバンテスト, 日清オイリオ, ツムラ, メニコン

## クイックスタート

### 開発環境構築
```bash
# リポジトリクローン
git clone https://github.com/ando-front/KABUtrade.git
cd KABUtrade

# 仮想環境作成・有効化
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 依存関係インストール
pip install -r requirements.txt

# 環境変数設定
cp .env.example .env
# .envファイルを編集してAPIキーを設定
```

### テスト実行
```bash
# 単体テスト
pytest test/

# バックテスト
python test/test_aiba_method_backtest.py

# 本体実行
python src/main.py
```

### 日次運用確認
```bash
# GitHub Actionsの実行状況確認
# https://github.com/ando-front/KABUtrade/actions

# 実行ログ確認
# "Run script"ステップのログをチェック

# メール通知確認
# シグナル通知メールの受信確認
```

## アーキテクチャ概要

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

## 主要ワークフロー

### データ処理フロー
1. 銘柄リスト読み込み（CSV）
2. 各銘柄のデータ取得（API/キャッシュ）
3. データ標準化・前処理
4. 移動平均線計算
5. トレンド分析
6. シグナル生成
7. 最新シグナル評価
8. 通知送信

### シグナル優先順位
1. **クロスシグナル** - ゴールデンクロス・デッドクロス
2. **連続シグナル** - 9日・13日連続陰線・陽線
3. **その他シグナル** - PPP、下半身、くちばし

## 重要な注意事項

### セキュリティ
- APIキーは環境変数で管理
- GitHub Secretsを使用
- 機密情報のハードコード禁止

### API制限対応
- Yahoo Finance API: レート制限あり
- 指数バックオフリトライ実装
- キャッシュ機能で重複取得回避
- Alpha Vantage APIをフォールバック

### 投資責任
- 本システムは投資助言業務ではない
- 情報提供のみを目的とする
- 投資判断は利用者の責任
- 免責事項の遵守

## 問い合わせ・サポート

### 技術的問題
- GitHubイシューで報告
- 開発手順書を参照
- ログ情報を添付

### 運用問題
- 運用手順書を参照
- 障害対応フローに従う
- 必要に応じてシステム停止

### 機能要望
- GitHubディスカッション
- 要件定義書を参照
- 影響範囲を検討

---

**最終更新**: 2024年7月5日  
**ドキュメントバージョン**: 1.0  
**システムバージョン**: 1.0
