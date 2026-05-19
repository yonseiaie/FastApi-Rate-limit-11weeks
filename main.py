"""
FastAPI Rate Limit Test Project
SlowAPI를利用したレート制限機能の実装
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# FastAPIアプリケーションの初期化
app = FastAPI(
    title="Rate Limit Test API",
    description="SlowAPIを使用したレート制限機能の実装テスト",
    version="1.0.0"
)

# SlowAPI Limiterの初期化
# get_remote_addressを使用してクライアントのIPアドレスを識別
limiter = Limiter(key_func=get_remote_address)

# FastAPIのアプリにLimiterを登録
app.state.limiter = limiter

# RateLimitExceeded例外ハンドラーの登録
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """
    レート制限超過時のエラーレスポンスを返すハンドラー
    429 Too Many Requestsステータスを返却
    """
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Rate limit exceeded. Please try again later.",
            "message": "Too Many Requests"
        }
    )


@app.get("/hello")
@limiter.limit("10/minute")  # 1分間に10回までのリクエストを許可
async def hello(request: Request):
    """
    helloエンドポイント
    1分間に10回までのリクエストを許可し，超过すると429エラーを返す
    """
    return {
        "message": "Hello World"
    }


@app.get("/")
async def root():
    """
    ルートパスへのリクエストを処理
    """
    return {
        "message": "FastAPI Rate Limit Test Server",
        "endpoints": ["/hello"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)