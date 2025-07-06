# 運用手順書 - KABUtrade

## 1. 日次運用手順

### 1.1 システム実行確認
```bash
# ローカル実行の場合
cd /path/to/KABUtrade
source venv/bin/activate
python src/main.py

# GitHub Actions実行の場合（将来対応）
# URL: https://github.com/ando-front/KABUtrade/actions

# 確認項目:
# ✓ 毎日市場終了後に実行されているか
# ✓ 実行時間が2時間以内に完了しているか
# ✓ エラーが発生していないか
# ✓ 通知メールが送信されているか
```

### 1.2 実行ログ確認手順
```bash
# ローカル実行時のログ確認
# ターミナル出力の確認項目:

# 正常実行時のログ例:
# Processing NY symbol 1/8: SPY
# Loading cached data for SPY from data_cache/xxx.csv
# Successfully retrieved 252 records for SPY
# Buy Signal: Golden Cross (例)
# Processing JP symbol 1/11: ^N225
# Email sent successfully

# エラー発生時の対応:
# - API制限エラー → 待機時間の調整
# - データ取得失敗 → 銘柄の確認、API状態確認
# - 通知失敗 → GAS設定確認
```

### 1.3 シグナル確認手順
```bash
# メール通知内容の確認
# 件名: シグナル通知
# 本文例:
# 賢二さん、AAPLの買いシグナル（Golden Cross）が出ましたので、買い注文を入れてください。

# シグナル種別:
# - Golden Cross / Dead Cross
# - PPP / Reverse PPP  
# - Lower Half / Reverse Lower Half
# - Bird Beak / Reverse Bird Beak
# - Up for 9 days / Down for 9 days
# - Up for 13 days / Down for 13 days
```

## 2. 週次運用手順

### 2.1 システム状態確認
```bash
# 1. GitHub Actionsの実行履歴確認（過去7日間）
# 実行成功率: 目標 95%以上
# 平均実行時間: 目標 20分以内

# 2. API使用状況確認
# Yahoo Finance API: レート制限状況
# Alpha Vantage API: 月間使用量確認

# 3. キャッシュサイズ確認
# data_cache/ ディレクトリサイズ
# 目標: 100MB以下維持
```

### 2.2 パフォーマンス分析
```bash
# 実行時間分析
# - データ取得時間
# - シグナル計算時間
# - 通知送信時間

# メモリ使用量分析
# - ピーク時メモリ使用量
# - メモリリーク検出

# エラー率分析
# - API エラー率
# - データ品質エラー率
# - 通知失敗率
```

### 2.3 週次レポート作成
```markdown
# KABUtrade 週次レポート（YYYY-MM-DD週）

## 実行サマリー
- 実行回数: X/7回
- 成功率: XX.X%
- 平均実行時間: XX分XX秒

## シグナル発生状況
- 総シグナル数: XX件
- 買いシグナル: XX件
- 売りシグナル: XX件
- 主要銘柄のシグナル:
  - AAPL: Golden Cross
  - SPY: No Signal
  - ...

## 問題・課題
- エラー発生状況
- パフォーマンス問題
- 改善提案

## 来週の予定
- 予定メンテナンス
- システム改善
```

## 3. 月次運用手順

### 3.1 システム点検
```bash
# 1. 依存ライブラリ更新確認
pip list --outdated

# 2. セキュリティアップデート確認
# GitHub Dependabotアラート確認

# 3. API制限状況確認
# Alpha Vantage月間使用量確認
# 必要に応じてプラン見直し

# 4. データ品質確認
# キャッシュデータの整合性チェック
# 異常値検出・修正
```

### 3.2 バックテスト実行
```bash
# 月次パフォーマンス検証
cd test/
python test_aiba_method_backtest.py

# バックテスト結果分析:
# - 勝率
# - 収益率
# - 最大ドローダウン
# - シャープレシオ
```

### 3.3 設定見直し
```bash
# 1. 銘柄リスト見直し
# 追加候補銘柄の検討
# 削除対象銘柄の確認

# 2. シグナルパラメータ調整
# 移動平均期間の最適化
# トレンド判定基準の調整

# 3. 通知設定確認
# メール配信リストの更新
# 通知内容の改善
```

## 4. 障害対応手順

### 4.1 緊急度分類
```
【緊急度 高】
- システム完全停止
- データ取得完全失敗
- 通知機能完全停止
- セキュリティインシデント

【緊急度 中】
- 一部銘柄のデータ取得失敗
- 一部通知失敗
- パフォーマンス著しい低下

【緊急度 低】
- 軽微なエラー
- ログ出力問題
- ドキュメント不備
```

### 4.2 障害対応フロー
```bash
# Step 1: 障害状況確認
# - エラーログの確認
# - 影響範囲の特定
# - 原因の初期分析

# Step 2: 緊急対応
# - サービス復旧（可能な場合）
# - 代替手段の実施
# - 利害関係者への連絡

# Step 3: 根本原因分析
# - 詳細ログ分析
# - コードレビュー
# - テスト環境での再現

# Step 4: 恒久対策
# - コード修正
# - テスト実施
# - デプロイ・検証

# Step 5: 再発防止策
# - 監視強化
# - プロセス改善
# - ドキュメント更新
```

### 4.3 よくある障害と対処法

#### 4.3.1 API制限エラー
```bash
# 症状: Rate Limit Error
# 原因: API呼び出し頻度が制限を超過

# 対処法:
# 1. 待機時間の増加
# - base_retry_delay を60秒→120秒に変更
# - 実行間隔を24時間→48時間に変更（一時的）

# 2. キャッシュ活用
# - 既存キャッシュの確認・利用
# - キャッシュ有効期限の延長

# 3. 代替API使用
# - Alpha Vantage APIへの切り替え
# - 手動データ投入（緊急時）
```

#### 4.3.2 データ品質問題
```bash
# 症状: 異常な株価データ
# 原因: APIからの不正データ、ネットワーク問題

# 対処法:
# 1. データ検証強化
# - 価格範囲チェック
# - 前日比変動率チェック
# - 出来高妥当性チェック

# 2. データクリーニング
# - 異常値の除去・補正
# - 欠損値の補間
# - データソースの変更

# 3. 手動確認・修正
# - 信頼できるソースとの照合
# - 手動データ修正
# - 再実行
```

#### 4.3.3 通知障害
```bash
# 症状: メール通知が送信されない
# 原因: GAS設定問題、ネットワーク問題

# 対処法:
# 1. GAS動作確認
# - GASのログ確認
# - 手動実行テスト
# - 権限設定確認

# 2. ネットワーク確認
# - GAS URLの接続確認
# - DNS解決確認
# - プロキシ設定確認

# 3. 代替通知手段
# - 別メールアドレスでのテスト
# - Slack通知の追加（将来）
# - 手動通知（緊急時）
```

## 5. メンテナンス手順

### 5.1 定期メンテナンス
```bash
# 毎月第1土曜日実施

# 1. システム停止
# GitHub Actionsのワークフロー無効化
# .github/workflows/daily_exec.yaml の schedule をコメントアウト

# 2. バックアップ作成
# 設定ファイルのバックアップ
# キャッシュデータのバックアップ

# 3. ライブラリ更新
pip list --outdated
pip install --upgrade package_name

# 4. セキュリティアップデート
# dependabotの推奨アップデート適用

# 5. テスト実行
pytest test/

# 6. システム復旧
# ワークフローの有効化
# 動作確認テスト
```

### 5.2 緊急メンテナンス
```bash
# セキュリティインシデント・重大障害時

# 1. 即座にシステム停止
# GitHub Actionsの緊急停止

# 2. 影響範囲調査
# ログ分析
# セキュリティスキャン

# 3. 修正・パッチ適用
# 脆弱性修正
# 緊急パッチ適用

# 4. テスト・検証
# セキュリティテスト
# 機能テスト

# 5. 段階的復旧
# テスト環境での確認
# 本番環境復旧
# 監視強化
```

## 6. 監視・アラート設定

### 6.1 監視項目
```yaml
# GitHub Actions監視
monitors:
  - workflow_execution_status
  - execution_duration
  - error_rate
  - success_rate

# システムリソース監視  
resources:
  - memory_usage
  - disk_usage
  - network_latency
  - api_response_time

# ビジネスメトリクス監視
business:
  - signal_generation_count
  - notification_delivery_rate
  - data_quality_score
  - user_engagement
```

### 6.2 アラート設定
```yaml
# アラート条件
alerts:
  critical:
    - workflow_failure: 即座
    - api_down: 5分以内
    - security_breach: 即座
    
  warning:
    - execution_time > 30min: 1時間後
    - error_rate > 10%: 2時間後
    - data_quality < 90%: 4時間後
    
  info:
    - new_signal_generated: 日次サマリー
    - performance_report: 週次サマリー
```

### 6.3 通知チャネル
```yaml
# 通知先設定
notification_channels:
  email:
    - admin@example.com
    - operator@example.com
    
  slack: # 将来実装
    - #kabutrade-alerts
    - #kabutrade-reports
    
  sms: # 緊急時のみ
    - +81-xxx-xxxx-xxxx
```

## 7. バックアップ・復旧手順

### 7.1 定期バックアップ
```bash
# 日次バックアップ（自動）
#!/bin/bash
BACKUP_DIR="backups/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# 設定ファイル
cp -r src/symbols/ $BACKUP_DIR/
cp requirements.txt $BACKUP_DIR/
cp .github/workflows/ $BACKUP_DIR/ -r

# キャッシュデータ（選択的）
cp data_cache/*.csv $BACKUP_DIR/ 2>/dev/null || true

# ログファイル
cp *.log $BACKUP_DIR/ 2>/dev/null || true

# 圧縮・保存
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR/
rm -rf $BACKUP_DIR/

# 古いバックアップ削除（30日以上）
find backups/ -name "*.tar.gz" -mtime +30 -delete
```

### 7.2 復旧手順
```bash
# 1. 障害状況確認
# 影響範囲の特定
# データ損失状況の確認

# 2. バックアップからの復旧
RESTORE_DATE="20240115"
tar -xzf backups/$RESTORE_DATE.tar.gz

# 設定ファイル復旧
cp $RESTORE_DATE/symbols/* src/symbols/
cp $RESTORE_DATE/requirements.txt .
cp $RESTORE_DATE/workflows/* .github/workflows/

# 3. 動作確認
python src/main.py --test-mode

# 4. 段階的復旧
# テスト環境での確認
# 一部機能の先行復旧
# 全機能の復旧確認
```

## 8. 容量管理

### 8.1 ディスク使用量監視
```bash
# キャッシュディレクトリサイズ確認
du -sh data_cache/

# 目標: 100MB以下
# 警告: 80MB以上
# 緊急: 150MB以上

# 古いキャッシュファイル削除
find data_cache/ -name "*.csv" -mtime +7 -delete
```

### 8.2 ログローテーション
```bash
# ログファイルサイズ制限
# 日次ログ: 最大10MB
# 月次保存: 最大12ファイル

# logrotate設定例
/path/to/kabutrade.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644
}
```

## 9. セキュリティ運用

### 9.1 定期セキュリティチェック
```bash
# 月次セキュリティ監査

# 1. 依存関係脆弱性チェック
pip audit

# 2. コードセキュリティスキャン
bandit -r src/

# 3. 環境変数確認
# APIキーの有効性確認
# 権限最小化確認

# 4. アクセスログ確認
# 異常なアクセスパターン検出
# 未承認アクセス検出
```

### 9.2 インシデント対応
```bash
# セキュリティインシデント発生時

# 1. 即座の対応
# システム停止
# 影響範囲調査
# 証拠保全

# 2. 影響評価
# データ漏洩有無
# システム改ざん有無
# サービス影響度

# 3. 復旧計画
# セキュリティパッチ適用
# 設定強化
# 監視強化

# 4. 事後対応
# インシデントレポート作成
# 再発防止策実施
# 社内展開・教育
```

## 10. 改善・最適化

### 10.1 継続的改善
```yaml
# 改善サイクル（Plan-Do-Check-Act）

Plan:
  - パフォーマンス指標の設定
  - 改善目標の設定
  - 改善計画の策定

Do:
  - 改善施策の実施
  - テスト・検証
  - デプロイ

Check:
  - 効果測定
  - 副作用確認
  - ユーザーフィードバック収集

Act:
  - 標準化・定着
  - ナレッジ共有
  - 次期改善計画策定
```

### 10.2 最適化項目
```yaml
# パフォーマンス最適化
performance:
  - 実行時間短縮
  - メモリ使用量削減
  - API呼び出し最適化
  - キャッシュ効率化

# 運用効率化
operations:
  - 自動化推進
  - 監視自動化
  - アラート精度向上
  - 手順書整備

# 品質向上
quality:
  - テストカバレッジ向上
  - コード品質向上
  - ドキュメント充実
  - エラーハンドリング強化
```

### 10.3 将来計画
```yaml
# 短期計画（3ヶ月）
short_term:
  - パフォーマンス改善
  - エラーハンドリング強化
  - 監視機能追加

# 中期計画（6ヶ月）
medium_term:
  - 新機能追加
  - UI改善
  - リアルタイム対応

# 長期計画（1年）
long_term:
  - AI/ML導入
  - クラウド移行
  - スケーラビリティ向上
```
