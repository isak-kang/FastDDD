---
doc_id: "{target-name}-refactoring"
type: "refactoring"
status: "draft"
version: "0.1.0"
---

# Refactoring: {Target Name}

## 문서 원칙

- 이 문서는 리팩토링 착수·실행 계획이다.
- 동작 보존 범위, 책임 분리, 적용 단계, 검증·롤백을 기록한다.
- 상세 아키텍처 규칙은 `AGENTS.md`를 따른다.

## 적용 규칙 (본 리팩토링 시 준수)

- 명시적 요청 없이 외부 동작(API, 에러, DB 스키마)을 변경하지 않는다.
- 구조 변경 전 characterization / 회귀 테스트로 현재 동작을 고정한다.
- 변경은 작고 되돌릴 수 있는 단위로 진행한다.
- 미사용 코드 제거 전 참조 검색(`rg`)으로 영향 범위를 확인한다.

---

## 1. 배경

- 변경 맥락:
- 현재 구조:
- 현재 문제:

## 2. 범위

- In-scope (3~7줄):
- Out-of-scope (기능 변경·범위 밖):

## 3. Goals / Non-Goals

- Goals:
- Non-Goals:

## 4. 동작 보존 기준

- 변경되면 안 되는 API·응답·경로:
- 변경되면 안 되는 부작용 (DB / Redis / storage):
- 예외·에러 코드 보존:

## 5. 사전 고정 테스트

| Case | Input | Current Output | Notes |
|------|-------|----------------|-------|
| | | | |

- 공개 인터페이스 (API, service 시그니처 등):

## 6. 리팩토링 설계

- 책임 분리 포인트 (domain / service / repository / router):
- 정책·컨텍스트 분리 포인트:
- 제거 대상 (중복 / 미사용 / 죽은 분기):

## 7. 적용 단계

| Step | Work | Validation |
|------|------|------------|
| 1 | | |
| 2 | | |
| 3 | | |

## 8. 레시피 skill (구조 이동 시)

| Skill | Required | Notes |
|-------|----------|-------|
| `create-bounded-context` | Yes / No | |
| `add-api-router` | Yes / No | |
| `add-error-code` | Yes / No | |
| `add-config-component` | Yes / No | |
| `add-lifespan-resource` | Yes / No | |

## 9. 검증

- pytest / lint:
- 회귀 테스트 결과:
- 수동 확인 포인트:

## 10. Risks / Rollback

- 주요 리스크:
- 롤백 전략:

## 11. Done Criteria

-

## 12. Open Questions

-

## 13. 변경 로그 (Phase B에서 갱신)

- 변경 파일 목록:
- 핵심 변경 요약:
- 동작 보존 근거 (테스트 / 시나리오):
- 잔여 리스크·후속 작업:
