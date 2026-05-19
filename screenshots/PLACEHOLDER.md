# Rate Limit Test Screenshots

이 폴더에는 테스트 실행 시의 스크린샷을 저장합니다.

## 테스트 후 스크린샷을 저장하는 방법

1. `uvicorn main:app --reload` 로 서버를 시작
2. 브라우저에서 `http://127.0.0.1:8000/hello` 에 접근
3. 10번까지 요청을 전송 (200 OK)
4. 11번째 요청을 전송 (429 Too Many Requests)
5. 브라우저의 스크린샷 기능을 사용해 저장
6. 이 폴더에 `rate_limit_result.png` 로 저장

## 기대되는 결과

- 1-10번째: 정상적인 JSON 응답 (`{"message": "Hello World"}`)
- 11번째 이후: 에러 응답 (`429 Too Many Requests`)