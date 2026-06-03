---
name: write-api-spec
description: PRD, 라우터 코드, DTO, 에러 정의에서 API 명세 문서를 생성하거나 업데이트한다.
---

# API 명세 작성 (Write API Spec)

## 목적

API 명세 문서를 생성하거나 업데이트한다. 프론트엔드 또는 팀에게 전달하는 문서다.

## 필요한 입력

- PRD 또는 기능 설명
- Router/Controller 구현 (`app/presentation/router/`)
- 요청/응답 DTO (`app/presentation/DTO/`)
- 에러코드 정의 (`docs/errors/`)
- AGENTS.md

## 진행 순서

1. 영향받는 엔드포인트를 파악한다.
2. 실제 코드의 Pydantic DTO에서 요청/응답 필드를 확인한다.
3. 다음 항목을 문서화한다:
   - 경로: `/api/{domain}/{resource}` 패턴
   - HTTP 메서드, 인증 여부, 권한
   - 요청 바디 / 쿼리 파라미터
   - 성공 응답 (`ApiResponse` 래퍼 포함)
   - 에러 응답 (실제 예외 처리 기반)
4. 비즈니스 규칙과 엣지 케이스를 포함한다.
5. 코드에 존재하지 않는 필드를 임의로 만들지 않는다.
6. 예시 값은 실제 DTO와 일치시킨다.
7. 템플릿을 사용하여 저장한다.

## 공통 응답 포맷

모든 API는 아래 포맷을 따른다:

```json
// 성공
{"success": true, "data": {...}}

// 실패
{"success": false, "error": {"code": "ERROR_CODE", "message": "설명"}}
```

## 출력

```text
docs/api/{domain}/{api-name}.api.md
```
