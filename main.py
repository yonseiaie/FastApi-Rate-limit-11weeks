"""
FastAPI Rate Limit Test Project
SlowAPI를 활용한 Rate Limit 기능 구현
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# FastAPI 애플리케이션 초기화
app = FastAPI(
    title="Rate Limit Test API",
    description="SlowAPI를 사용한 Rate Limit 기능 구현 테스트",
    version="1.0.0"
)

# SlowAPI Limiter 초기화
# get_remote_address를 사용하여 클라이언트의 IP 주소를 식별
limiter = Limiter(key_func=get_remote_address)

# FastAPI 앱에 Limiter 등록
app.state.limiter = limiter

# RateLimitExceeded 예외 핸들러 등록
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """
    Rate Limit 초과 시 에러 응답을 반환하는 핸들러
    429 Too Many Requests 상태코드를 반환
    """
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Rate limit exceeded. Please try again later.",
            "message": "Too Many Requests"
        }
    )


@app.get("/hello")
@limiter.limit("10/minute")  # 1분에 10번까지 요청 허용
async def hello(request: Request):
    """
    hello 엔드포인트
    1분에 10번까지 요청을 허용하고, 초과하면 429 에러를 반환
    """
    return {
        "message": "Hello World"
    }


@app.get("/")
async def root():
    """
    루트 경로로의 요청을 처리합니다
    """
    return {
        "message": "FastAPI Rate Limit Test Server",
        "endpoints": ["/hello"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)