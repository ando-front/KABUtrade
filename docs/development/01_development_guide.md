# 開発手順書 - KABUtrade

## 1. 開発環境構築手順

### 1.1 前提条件
- **OS**: macOS / Linux / Windows
- **Python**: 3.9.18以上 (3.11推奨)
- **Git**: 最新版
- **GitHub アカウント**: リポジトリアクセス用

### 1.2 開発環境セットアップ
```bash
# 1. リポジトリのクローン
git clone https://github.com/ando-front/KABUtrade.git
cd KABUtrade

# 2. Python仮想環境の作成
python -m venv venv

# 3. 仮想環境の有効化
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. 依存関係のインストール
pip install --upgrade pip
pip install -r requirements.txt

# 5. 環境変数ファイルの作成
cp .env.example .env
# .envファイルを編集してAPIキーを設定
```

### 1.3 環境変数設定
```bash
# .env ファイルの内容
API_KEY=your_alpha_vantage_api_key_here
ALPHAVANTAGE_API_KEY=your_alpha_vantage_api_key_here
GAS_URL=your_google_apps_script_url_here
```

### 1.4 開発ツールのインストール
```bash
# 開発用追加パッケージ
pip install pytest pytest-cov black flake8 mypy

# VSCode拡張（推奨）
# - Python
# - Python Docstring Generator
# - GitLens
# - Prettier
```

## 2. プロジェクト構造理解

### 2.1 ディレクトリ構造
```
KABUtrade/
├── src/                        # メインソースコード
│   ├── main.py                # エントリーポイント
│   ├── aiba_trade_method.py   # 売買ロジック統合
│   ├── calculaters/           # 計算エンジン
│   │   ├── signals.py         # シグナル計算
│   │   └── trends.py          # トレンド分析
│   ├── get_stock_data/        # データ取得
│   │   ├── get_yahoo_finance.py
│   │   └── get_alpha_vantage.py
│   ├── helpers/               # ヘルパー関数
│   │   └── trend_logic.py
│   ├── send_mail/             # 通知機能
│   │   └── send_email_for_signal.py
│   ├── symbols/               # 銘柄データ
│   │   ├── symbols_NY.csv
│   │   └── symbols_JP.csv
│   └── google_app_scripts/    # GAS関連
│       └── postMail.js
├── test/                      # テストコード
├── data_cache/                # データキャッシュ
├── docs/                      # ドキュメント
├── .github/workflows/         # CI/CD設定
├── requirements.txt           # 依存関係
└── README.md                  # プロジェクト説明
```

### 2.2 主要モジュール概要
```python
# main.py - メインエントリーポイント
def main():
    """
    メイン処理フロー:
    1. 銘柄リスト読み込み
    2. 各銘柄のデータ取得・分析
    3. シグナル生成
    4. 通知送信
    """

# aiba_trade_method.py - 売買ロジック
def main(kabuData: pd.DataFrame) -> Tuple[str, str]:
    """
    相場式投資手法による売買シグナル生成
    Returns: (signalType, signalKind)
    """

# calculaters/signals.py - シグナル計算
def calculate_signals(kabuData: pd.DataFrame, ...) -> pd.DataFrame:
    """
    各種売買シグナルの計算
    - 連続陰線・陽線
    - ゴールデンクロス・デッドクロス
    - パンパカパン
    - 下半身・くちばし
    """

# calculaters/trends.py - トレンド分析
def count_trend_days(kabuData: pd.DataFrame) -> pd.DataFrame:
    """
    上昇・下降トレンドの継続日数カウント
    """
```

## 3. 開発ワークフロー

### 3.1 Git ワークフロー
```bash
# 1. 開発ブランチの作成
git checkout -b feature/new-feature-name

# 2. 開発作業
# コード編集・テスト・デバッグ

# 3. 変更のコミット
git add .
git commit -m "feat: add new feature description"

# 4. プッシュ
git push origin feature/new-feature-name

# 5. プルリクエスト作成
# GitHub上でプルリクエストを作成

# 6. レビュー・マージ
# レビュー後、mainブランチにマージ
```

### 3.2 コミットメッセージ規約
```
コミットタイプ:
- feat: 新機能
- fix: バグ修正
- docs: ドキュメント更新
- style: コードスタイル修正
- refactor: リファクタリング
- test: テスト追加・修正
- chore: その他の変更

例:
feat: add cache functionality to Yahoo Finance API
fix: resolve rate limit error in data fetching
docs: update API documentation
```

### 3.3 コードレビューガイドライン
```
レビューポイント:
1. 機能要件の充足
2. コード品質（可読性・保守性）
3. テストカバレッジ
4. パフォーマンス
5. セキュリティ
6. エラーハンドリング
7. ドキュメント更新
```

## 4. 機能開発手順

### 4.1 新しいシグナル追加手順
```python
# Step 1: calculaters/signals.py にシグナル関数追加
def calculate_new_signal(kabuData: pd.DataFrame) -> pd.Series:
    """
    新しいシグナルの計算ロジック
    
    Args:
        kabuData: 株価データ
    
    Returns:
        シグナル判定結果
    """
    # シグナル計算ロジックを実装
    pass

# Step 2: calculate_signals関数に統合
def calculate_signals(kabuData: pd.DataFrame, ...) -> pd.DataFrame:
    # 既存のシグナル計算
    
    # 新しいシグナル追加
    kabuData['Buy_Signal_new'] = calculate_new_signal(kabuData)
    
    return kabuData

# Step 3: aiba_trade_method.py でシグナル評価追加
def check_other_signals(latest_data: pd.Series) -> Tuple[Optional[str], Optional[str]]:
    # 既存のシグナルチェック
    
    # 新しいシグナルチェック追加
    elif latest_data['Buy_Signal_new']:
        return 'Buy', 'New Signal'
    
    return None, None

# Step 4: テストケース追加
def test_new_signal():
    """新しいシグナルのテスト"""
    # テストデータ準備
    # シグナル計算実行
    # 結果検証
```

### 4.2 新しいデータソース追加手順
```python
# Step 1: get_stock_data/ に新しいモジュール追加
# get_stock_data/get_new_api.py

def get_new_api_stock_data(symbol: str, period: str) -> pd.DataFrame:
    """
    新しいAPIからのデータ取得
    """
    # API呼び出しロジック実装
    pass

# Step 2: get_alpha_vantage.py でフォールバック追加
def get_stock_data(symbol: str, api_key: str = None, period: str = "max") -> pd.DataFrame:
    try:
        # Primary: Yahoo Finance
        data = get_yfinance_stock_data(symbol, period)
        if not data.empty:
            return standardize_headers(data)
        
        # Secondary: Alpha Vantage
        data = get_alpha_vantage_data(symbol, api_key)
        if not data.empty:
            return data
        
        # Tertiary: New API
        data = get_new_api_stock_data(symbol, period)
        return standardize_headers(data)
        
    except Exception as e:
        print(f"Error getting data for {symbol}: {e}")
        return pd.DataFrame()
```

### 4.3 新しい銘柄追加手順
```bash
# Step 1: 銘柄リストファイル編集
# src/symbols/symbols_NY.csv または symbols_JP.csv

# 新しい行を追加
echo "NVDA,NVIDIA" >> src/symbols/symbols_NY.csv

# Step 2: 銘柄の動作確認
python -c "
import pandas as pd
symbols = pd.read_csv('src/symbols/symbols_NY.csv')
print(symbols)
"

# Step 3: テスト実行
python test/test_aiba_method_backtest.py
```

## 5. テスト開発手順

### 5.1 ユニットテスト作成手順
```python
# test/test_signals.py

import pytest
import pandas as pd
import numpy as np
from src.calculaters.signals import calculate_signals

class TestSignalCalculation:
    """シグナル計算テストクラス"""
    
    def setup_method(self):
        """テストデータの準備"""
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        self.test_data = pd.DataFrame({
            '1. open': np.random.uniform(100, 200, 100),
            '2. high': np.random.uniform(150, 250, 100),
            '3. low': np.random.uniform(50, 150, 100),
            '4. close': np.random.uniform(100, 200, 100),
            '5. volume': np.random.randint(1000000, 5000000, 100)
        }, index=dates)
    
    def test_golden_cross_signal(self):
        """ゴールデンクロスシグナルテスト"""
        # テストデータにSMA追加
        self.test_data['SMA_25'] = self.test_data['4. close'].rolling(25).mean()
        self.test_data['SMA_75'] = self.test_data['4. close'].rolling(75).mean()
        
        # シグナル計算
        result = calculate_signals(self.test_data, [9, 13], [5, 10, 20, 25, 30, 60, 75, 100, 200, 300], [25, 75])
        
        # 結果検証
        assert 'Buy_Signal_golden_cross' in result.columns
        assert result['Buy_Signal_golden_cross'].dtype == bool
    
    def test_consecutive_down_signal(self):
        """連続陰線シグナルテスト"""
        # 9日連続陰線のテストデータ作成
        test_data = self.test_data.copy()
        test_data.loc[test_data.index[-9:], 'Down'] = True
        
        # シグナル計算
        result = calculate_signals(test_data, [9, 13], [5, 10, 20, 25, 30, 60, 75, 100, 200, 300], [25, 75])
        
        # 結果検証
        assert result['Buy_Signal_9'].iloc[-1] == True

# テスト実行
pytest test/test_signals.py -v
```

### 5.2 統合テスト作成手順
```python
# test/test_integration.py

import pytest
from unittest.mock import patch, MagicMock
from src.main import main, process_stock_data

class TestIntegration:
    """統合テストクラス"""
    
    @patch('src.main.get_stock_data')
    @patch('src.main.send_email_for_signal.sendEmailForSignal')
    def test_main_workflow(self, mock_email, mock_data):
        """メインワークフローテスト"""
        # モックデータ準備
        mock_data.return_value = self.create_mock_stock_data()
        mock_email.return_value = True
        
        # メイン処理実行
        with patch('src.main.pd.read_csv') as mock_csv:
            mock_csv.return_value = pd.DataFrame({'symbol': ['TEST']})
            main()
        
        # 検証
        assert mock_data.called
        assert mock_email.called
    
    def create_mock_stock_data(self):
        """モック株価データ作成"""
        dates = pd.date_range('2024-01-01', periods=300, freq='D')
        return pd.DataFrame({
            '1. open': np.random.uniform(100, 200, 300),
            '2. high': np.random.uniform(150, 250, 300),
            '3. low': np.random.uniform(50, 150, 300),
            '4. close': np.random.uniform(100, 200, 300),
            '5. volume': np.random.randint(1000000, 5000000, 300)
        }, index=dates)
```

### 5.3 バックテスト開発手順
```python
# test/test_backtest.py

class BacktestFramework:
    """バックテストフレームワーク"""
    
    def __init__(self, initial_capital: float = 1000000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0
        self.trades = []
    
    def run_backtest(self, data: pd.DataFrame, strategy_func) -> dict:
        """バックテスト実行"""
        for i in range(1, len(data)):
            signal_type, signal_kind = strategy_func(data.iloc[:i+1])
            
            if signal_type == 'Buy' and self.capital > 0:
                self.buy(data.iloc[i], i)
            elif signal_type == 'Sell' and self.position > 0:
                self.sell(data.iloc[i], i)
        
        return self.calculate_performance()
    
    def buy(self, row: pd.Series, index: int):
        """買い注文実行"""
        price = row['4. close']
        shares = self.capital / price
        self.position += shares
        self.capital = 0
        self.trades.append({
            'type': 'BUY',
            'date': row.name,
            'price': price,
            'shares': shares
        })
    
    def sell(self, row: pd.Series, index: int):
        """売り注文実行"""
        price = row['4. close']
        self.capital = self.position * price
        self.trades.append({
            'type': 'SELL',
            'date': row.name,
            'price': price,
            'shares': self.position
        })
        self.position = 0
    
    def calculate_performance(self) -> dict:
        """パフォーマンス計算"""
        final_value = self.capital + (self.position * self.trades[-1]['price'] if self.trades else 0)
        return {
            'initial_capital': self.initial_capital,
            'final_value': final_value,
            'total_return': (final_value - self.initial_capital) / self.initial_capital,
            'number_of_trades': len(self.trades),
            'trades': self.trades
        }
```

## 6. デバッグ手順

### 6.1 ログ設定
```python
# ログ設定例
import logging

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kabutrade.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 使用例
def get_stock_data(symbol: str):
    logger.info(f"Fetching data for symbol: {symbol}")
    try:
        # データ取得処理
        logger.info(f"Successfully fetched data for {symbol}")
    except Exception as e:
        logger.error(f"Failed to fetch data for {symbol}: {e}")
```

### 6.2 デバッグ実行
```bash
# デバッグモードでの実行
python -m pdb src/main.py

# 特定の銘柄のみテスト
python -c "
from src.main import process_stock_data
result = process_stock_data('AAPL')
print(result)
"

# VSCodeデバッガー設定（.vscode/launch.json）
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Main",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

### 6.3 パフォーマンス測定
```python
# パフォーマンス測定例
import time
import cProfile

def profile_function(func, *args, **kwargs):
    """関数のプロファイル実行"""
    profiler = cProfile.Profile()
    profiler.enable()
    
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    
    profiler.disable()
    profiler.print_stats(sort='cumulative')
    
    print(f"Execution time: {end_time - start_time:.2f} seconds")
    return result

# 使用例
result = profile_function(process_stock_data, 'AAPL')
```

## 7. 品質保証手順

### 7.1 コード品質チェック
```bash
# フォーマット確認
black --check src/

# リント実行
flake8 src/

# 型チェック
mypy src/

# テストカバレッジ
pytest --cov=src --cov-report=html

# セキュリティチェック
bandit -r src/
```

### 7.2 コードレビューチェックリスト
```
機能性:
□ 要件を満たしているか
□ 期待通りに動作するか
□ エラーハンドリングが適切か

品質:
□ コードが読みやすいか
□ 適切な命名がされているか
□ 重複コードがないか
□ パフォーマンスに問題がないか

テスト:
□ テストケースが十分か
□ エッジケースがカバーされているか
□ テストが実際に機能を検証しているか

ドキュメント:
□ コメントが適切か
□ docstringが記載されているか
□ README/ドキュメントが更新されているか

セキュリティ:
□ 機密情報がハードコードされていないか
□ 入力検証が適切か
□ 権限チェックが実装されているか
```

## 8. リリース手順

### 8.1 リリース準備
```bash
# 1. バージョン更新
# package.json, __init__.py などのバージョン番号更新

# 2. CHANGELOG.md 更新
# 変更内容をCHANGELOG.mdに記載

# 3. 全テスト実行
pytest

# 4. リリースブランチ作成
git checkout -b release/v1.1.0

# 5. 最終確認・修正
# バグ修正、ドキュメント更新など

# 6. プルリクエスト作成・レビュー
# リリースブランチからmainへのPR作成
```

### 8.2 リリース実行
```bash
# 1. mainブランチにマージ
git checkout main
git merge release/v1.1.0

# 2. タグ作成
git tag -a v1.1.0 -m "Release version 1.1.0"

# 3. プッシュ
git push origin main --tags

# 4. GitHub Releases作成
# GitHubでリリースノート作成

# 5. デプロイ確認
# GitHub Actionsでの自動デプロイ確認
```

### 8.3 リリース後確認
```bash
# 1. 本番環境での動作確認
# GitHub Actionsの実行ログ確認

# 2. 通知機能確認
# メール通知が正常に送信されるか確認

# 3. エラー監視
# 新しいエラーが発生していないか監視

# 4. パフォーマンス確認
# 実行時間に問題がないか確認
```

## 9. トラブルシューティング

### 9.1 よくある問題と解決策
```
問題: Rate Limit Error
解決策:
- 待機時間を増やす
- キャッシュを活用する
- 別のAPIを使用する

問題: データ取得失敗
解決策:
- ネットワーク接続を確認
- APIキーの有効性を確認
- シンボル名の正確性を確認

問題: メール送信失敗
解決策:
- GASのURLを確認
- ネットワーク接続を確認
- GASスクリプトの動作を確認

問題: メモリ不足
解決策:
- データの部分読み込み
- 不要なデータの削除
- ガベージコレクション実行
```

### 9.2 ログ分析手順
```bash
# ログレベル別表示
grep "ERROR" kabutrade.log
grep "WARNING" kabutrade.log

# 特定の銘柄のログ抽出
grep "AAPL" kabutrade.log

# 時間範囲指定でログ抽出
grep "2024-01-15" kabutrade.log
```

## 10. 継続的改善

### 10.1 パフォーマンス監視
```python
# パフォーマンスメトリクス収集
class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
    
    def measure_execution_time(self, func_name: str, execution_time: float):
        if func_name not in self.metrics:
            self.metrics[func_name] = []
        self.metrics[func_name].append(execution_time)
    
    def get_average_time(self, func_name: str) -> float:
        if func_name in self.metrics:
            return sum(self.metrics[func_name]) / len(self.metrics[func_name])
        return 0.0
    
    def generate_report(self) -> dict:
        return {
            func: {
                'average_time': self.get_average_time(func),
                'total_calls': len(times),
                'max_time': max(times),
                'min_time': min(times)
            }
            for func, times in self.metrics.items()
        }
```

### 10.2 技術的負債管理
```
技術的負債チェックリスト:
□ 重複コードの削除
□ 複雑な関数の分割
□ ハードコードされた値の設定化
□ 古いライブラリの更新
□ 未使用コードの削除
□ ドキュメントの更新
□ テストカバレッジの向上
```

### 10.3 機能改善提案
```
改善提案プロセス:
1. 問題・改善点の特定
2. 改善案の検討
3. 影響範囲の分析
4. 実装計画の策定
5. レビュー・承認
6. 実装・テスト
7. デプロイ・検証
8. 効果測定
```
