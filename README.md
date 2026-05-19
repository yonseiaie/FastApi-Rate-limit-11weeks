# FastAPI Rate Limit Test Project

## 프로젝트 소개

본 프로젝트는 FastAPI 프레임워크에서 **Rate Limit (레이트 제한)** 기능을 구현하는 것을 학습하기 위한 샘플 프로젝트입니다.

### FastAPI에서 Rate Limit이 필요한 이유

현대 개발에서 API 서비스는 불특정 다수의 클라이언트로부터 요청을 받습니다. 레이트 제한을 구현하지 않을 경우, 다음과 같은 문제가 발생할 수 있습니다:

- **API 악용 방지**: 악의적인 사용자가 대량 요청을 보내 서비스를 마비시킬 수 있음
- **자원 낭비 방지**: 단일 사용자가 과도한 요청을 하여 다른 사용자의 서비스를 저해
- **서비스 안정성 저하**: 트래픽 급증으로 인해 서버가 크래시 될 수 있음

이러한 문제를 해결하기 위해, **Rate Limit (레이트 제한)** 기능을 구현하는 것이 중요합니다.

---

## 사용 기술

| 기술 | 설명 |
|------|------|
| **FastAPI** | Python의 고성능 웹 프레임워크. 자동 문서 생성 및 타입 추론 기능 제공 |
| **SlowAPI** | FastAPI용 레이트 제한 라이브러리. 설정이매우 간단하고 사용하기 편리함 |
| **Uvicorn** | ASGI 서버. FastAPI 애플리케이션 실행에 사용 |

---

## 선택한 알고리즘

### Fixed Window 방식

본 프로젝트에서는 **Fixed Window (고정 윈도우)** 알고리즘을 사용하고 있습니다.

**동작 원리:**
- 시간을 고정 크기의 윈도우(예: 1분)로 구분
- 각 윈도우 내에서 허용되는 요청 수를 제한
- 윈도우 경계에서 카운터가 리셋

**예시:**
- 10 요청/분 → 1분마다 10번의 요청 허용
- 11번째 요청은 429 에러 반환

### SlowAPI의 내부 동작

SlowAPI는 내부적으로 `limits` 라이브러리를 사용합니다. Fixed Window 알고리즘을 구현하며, 다음과 같은 기능을 제공합니다:

- IP 주소 기반 레이트 제한
- 커스터마이징 가능한 제한 규칙
- 예외 처리 자동화

---

## 시스템 아키텍처

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
  ├── 200 OK (정상)
  └── 429 Too Many Requests (초과)
```

**플로우 설명:**

1. 클라이언트가 서버로 요청을 전송
2. FastAPI가 요청을 받고 SlowAPI Limiter로 전달
3. Limiter가 현재 윈도우 내의 요청 수를 체크
4. 요청 수가 제한 이내면 200 OK, 초과면 429 에러 반환

---

## 실행 방법

### 패키지 설치

```bash
pip install -r requirements.txt
```

### 서버 실행

```bash
uvicorn main:app --reload
```

또는

```bash
python main.py
```

서버가 정상적으로 시작되면, 다음과 같은 메시지가 표시됩니다:

```
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 테스트 방법

### 방법 1 — 브라우저

브라우저에서 다음 URL에 접근:

```
http://127.0.0.1:8000/hello
```

### 방법 2 — curl (반복 요청)

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

## 실행 결과

### 첫 10개의 요청

```json
{
    "message": "Hello World"
}
```

상태 코드: **200 OK**

### 11번째 이후 요청

```json
{
    "detail": "Rate limit exceeded. Please try again later.",
    "message": "Too Many Requests"
}
```

상태 코드: **429 Too Many Requests**

---

## 결과 분석

### Rate Limit의 정상적인 동작

1. **초기 상태**: 요청 카운터는 0
2. **1-10번째**: 요청을 정상적으로 처리하고 200 OK 반환
3. **11번째**: Limiter가 제한을 초과했음을 감지
4. **429 에러**: 클라이언트에게 레이트 제한 초과를 알림

### API 서버 보호 관점

- **DoS 공격 방지**: 악의적인 대량 요청을 차단
- **자원 공정 배분**: 모든 사용자에게 균등한 서비스 제공
- **시스템 안정성**: 트래픽 급증으로 인한 크래시 방지

---

## 느낀 점

본 프로젝트를 통해 API 보안에서 레이트 제한의 중요성을 배웠습니다. FastAPI와 SlowAPI를 조합함으로써매우 간단하고 효과적으로 레이트 제한을 구현할 수 있음을 알게 되었습니다. 특히, 실제 개발 현장에서는 사용자의 부정접근을 예상하고 적절한 제한 설계를 하는 것이 중요하다는 것을 느꼈습니다. 또한, 429 에러 발생 시 사용자에게 올바르게 알리는 UI/UX 설계도 잊지 않도록 합니다. 이 경험을 바탕으로 향후 프로젝트에서는 보안면을 더욱 강화하고 싶습니다.

---

## GitHub 업로드 방법

### 1. 리포지토리 초기화

```bash
git init
```

### 2. 파일 추가

```bash
git add .
```

### 3. 커밋

```bash
git commit -m "Initial commit"
```

### 4. 브랜치 생성

```bash
git branch -M main
```

### 5. 원격 리포지토리 추가

```bash
git remote add origin <리포지토리 URL>
```

**예시:**
```bash
git remote add origin https://github.com/username/operator-api-rate-limit.git
```

### 6. 푸시

```bash
git push -u origin main
```

---

## 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SlowAPI GitHub](https://github.com/laurentS/slowapi)
- [Uvicorn 공식 문서](https://www.uvicorn.org/)

---

## 라이선스

MIT License

---

작성일: 2026년 5월