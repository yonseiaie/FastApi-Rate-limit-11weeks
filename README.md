# FastAPI Rate Limit Test Project

## プロジェクト紹介

本プロジェクトは、FastAPIフレームワークにおける**Rate Limit（レート制限）機能**の実装を学習するためのサンプルプロジェクトです。

### FastAPIでRate Limitが必要な理由

現代の開発において、APIサービスは不特定多数のクライアントからリクエストを受けます。レート制限を実装しない場合、以下の問題が発生する可能性があります：

- **APIの不正利用**: 恶意のあるユーザーが大量のリクエストを送信し、サービスを瘫痪させる
- **リソースの浪費**: 単一のユーザーが過度のリクエストを行い、他のユーザーの足を引っ張る
- **サービス安定性の低下**: トラフィックの急増によりサーバーがクラッシュする可能性がある

このような問題を解決するため、**Rate Limit（レート制限）**機能を実装することが重要です。

---

## 使用技術

| 技術 | 説明 |
|------|------|
| **FastAPI** | Pythonの高性能なWebフレームワーク。自動ドキュメント生成功能和类型推論 |
| **SlowAPI** | FastAPI用のレート制限ライブラリ。Easy to configure and use |
| **Uvicorn** | ASGIサーバー。FastAPIアプリケーションを実行するために使用 |

---

## 選択したアルゴリズム

### Fixed Window方式

本プロジェクトでは**Fixed Window（固定ウィンドウ）**アルゴリズムを使用しています。

**動作原理:**
- 時間を固定サイズのウィンドウ（例：1分）に分割
- 各ウィンドウ内で許可されるリクエスト数を制限
- ウィンドウの境界でカウンターがリセット

**例:**
- 10リクエスト/分 → 1分ごとに10回のリクエストを許可
- 11回目のリクエストは429エラーを返す

### SlowAPIの内部動作

SlowAPIは内部的に`limits`ライブラリを使用しています。Fixed Windowアルゴリズムを実装し、以下の機能を提供します：

- IPアドレスベースのレート制限
- カスタマイズ可能な制限ルール
- 例外処理の自動化

---

## システムアーキテクチャ

```
Client
  │
  │ HTTP Request
  ▼
FastAPI Server
  │
  │ Request Validation
  ▼
SlowAPI Limiter
  │
  │ Check Rate Limit
  │ (10 requests/minute)
  ▼
Response
  │
  ├── 200 OK (正常)
  └── 429 Too Many Requests (超過)
```

**フロー説明:**

1. クライアントがサーバーにリクエストを送信
2. FastAPIがリクエストを受け取り、SlowAPI Limiterに転送
3. Limiterが現在のウィンドウ内のリクエスト数をチェック
4. リクエスト数が制限内であれば200 OK、超過であれば429エラーを返却

---

## 実行方法

### パッケージのインストール

```bash
pip install -r requirements.txt
```

### サーバーの実行

```bash
uvicorn main:app --reload
```

または

```bash
python main.py
```

サーバーが正常に起動すると、以下のメッセージが表示されます：

```
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## テスト方法

### 方法1 — ブラウザ

ブラウザで以下のURLにアクセス:

```
http://127.0.0.1:8000/hello
```

### 方法2 — curl（繰り返しリクエスト）

#### Windows PowerShell:

```powershell
for ($i=1; $i -le 12; $i++) {
    curl http://127.0.0.1:8000/hello
}
```

#### Linux/macOS:

```bash
for i in {1..12}; do curl http://127.0.0.1:8000/hello; done
```

---

## 実行結果

### 最初の10回のリクエスト

```json
{
    "message": "Hello World"
}
```

ステータスコード: **200 OK**

### 11回目以降のリクエスト

```json
{
    "detail": "Rate limit exceeded. Please try again later.",
    "message": "Too Many Requests"
}
```

ステータスコード: **429 Too Many Requests**

---

## 結果分析

### Rate Limitの正常な動作

1. **初期状態**: リクエストカウンターは0
2. **1-10回目**: リクエストを正常に処理し、200 OKを返却
3. **11回目**: Limiterが制限を超過していることを検出
4. **429エラー**: クライアントにレート制限超過を通知

### APIサーバー保護の観点から

- **DoS攻撃の防止**: 恶意のある大量リクエストをブロック
- **リソースの公平な配分**: 全ユーザーに均等のサービスを提供
- **システムの安定性**: トラフィック急増によるクラッシュを防止

---

## 感じた点

本プロジェクトを通じて、APIセキュリティにおけるレート制限の重要性を学びました。FastAPIとSlowAPIを組み合わせることで、简单かつ効果的にレート制限を実装できることがわかりました。特に、実際の開発现场では用户からの不正なアクセスを想定し、適切な限制设計が重要であると思いました。また、429エラー发生时的处理を用户に正しく伝えるUI/UX设计も忘れないようにします。この经验を基に、今後のプロジェクトではセキュリティ面をもっと强化したいと考えています。

---

## GitHubアップロード方法

### 1. リポジトリの初期化

```bash
git init
```

### 2. ファイルの追加

```bash
git add .
```

### 3. コミット

```bash
git commit -m "Initial commit"
```

### 4. ブランチの作成

```bash
git branch -M main
```

### 5. リモートリポジトリの追加

```bash
git remote add origin <あなたのリポジトリURL>
```

**例:**
```bash
git remote add origin https://github.com/username/operator-api-rate-limit.git
```

### 6. プッシュ

```bash
git push -u origin main
```

---

## 参考資料

- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [SlowAPI GitHub](https://github.com/laurentS/slowapi)
- [Uvicorn公式ドキュメント](https://www.uvicorn.org/)

---

## ライセンス

MIT License

---

作成日: 2026年5月