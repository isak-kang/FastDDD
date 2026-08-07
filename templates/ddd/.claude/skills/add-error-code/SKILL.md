---
name: add-error-code
description: FastAPI DDD 템플릿에 API 에러 코드와 예외를 추가·갱신한다. 새 API 에러, domain failure, exception mapping, 에러 응답 contract 도입 시 사용한다.
---

# 에러 코드 추가 (Add Error Code)

## 목적

공통 또는 도메인별 에러 코드와 예외 클래스를 추가하고 API 응답 contract에 맞게 연결한다.

## 필요한 입력

- `app/shared/exceptions/error_code.py`
- (도메인별일 때) `app/shared/exceptions/domains/{domain}/error_code.py`
- AGENTS.md 에러 응답 규칙

## 진행 순서

1. `app/shared/exceptions/error_code.py`를 읽는다.
2. 도메인별 에러면 `app/shared/exceptions/domains/{domain}/error_code.py`를 읽는다.
3. 새 code 추가 전 기존 이름을 확인한다.
4. 공통 code는 `ErrorCode`, 도메인별 code는 `{Domain}ErrorCode`에 추가한다.
5. 도메인별 error code 값은 `(status_code, code, default_message)` 형식을 사용한다.
6. 도메인별 예외 클래스는 `app/shared/exceptions/domains/{domain}/`에 둔다.
7. FastAPI handler 등록은 `app/shared/exceptions/handlers.py`에서 유지한다.
8. response payload에 대한 test를 추가·갱신한다.

## 응답 contract

```json
{
  "status": 400,
  "code": "ERROR_CODE",
  "message": "message"
}
```

## 규칙

- 제거된 error code를 다른 의미로 재사용하지 않는다.
- 공통 code는 `ErrorCode`, 도메인별 code는 `{Domain}ErrorCode`에 둔다.
- 동작이 다르면 generic message보다 domain-specific code를 우선한다.
- API로 노출된 user-facing message는 안정적으로 유지한다.
- 예외 정의는 `app/shared/exceptions/domains/{domain}/`에 모은다.

## 관련 skill

- `create-bounded-context` — 새 context의 `{Context}Error`, `{Context}ErrorCode` 스캐폴드
- `add-api-router` — endpoint에서 domain error를 raise할 때
