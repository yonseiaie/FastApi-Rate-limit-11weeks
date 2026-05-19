# Rate Limit Test Screenshots

このフォルダにはテスト実行時のスクリーンショットを保存します。

## テスト後にスクリーンショットを保存する方法

1. `uvicorn main:app --reload` でサーバーを起動
2. ブラウザで `http://127.0.0.1:8000/hello` にアクセス
3. 10回までリクエストを送信（200 OK）
4. 11回目をリクエスト（429 Too Many Requests）
5. ブラウザのスクリーンショット機能を 사용해保存
6. このフォルダに `rate_limit_result.png` として保存

## 期待される結果

- 1-10回目: 正常なJSONレスポンス (`{"message": "Hello World"}`)
- 11回目以降: エラーレスポンス (`429 Too Many Requests`)