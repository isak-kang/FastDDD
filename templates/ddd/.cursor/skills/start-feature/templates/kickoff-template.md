---
doc_id: "{feature-name}-kickoff"
type: "kickoff"
status: "draft"
version: "0.1.0"
---

# Kickoff: {Feature Name}

## 문서 원칙

- 이 문서는 개발 착수 전 kickoff 문서다.
- 범위, 레이어 영향, 레시피 skill, 테스트·완료 기준을 기록한다.
- 상세 아키텍처 규칙은 `AGENTS.md`를 따른다. 여기서는 실행 계획만 적는다.

## 적용 규칙 (본 기능 개발 시 준수)

- `AGENTS.md`와 `.cursor/rules/`의 DDD·레이어 규칙을 준수한다.
- 개발 순서: **domain → repository (port/impl) → service → router**
- router는 제공, `api_router.py`에서 등록한다.
- 에러는 `app/shared/exceptions/domains/{context}/`에 둔다.
- domain 인덱스가 필요하면 `app/domain/{context}/indexes/`에 두고 통합 registry에 등록한다.

---

## 1. Problem 1-Pager

- Background:
- Problem:
- Goal:
- Non-goals:
- Constraints:

## 2. 범위

- 포함:
- 제외:

## 3. 레이어별 영향

| 레이어 | 변경 여부 | 내용 |
|--------|-----------|------|
| domain | Yes / No | |
| application | Yes / No | |
| infrastructure | Yes / No | |
| presentation | Yes / No | |

## 4. 요구사항 → 설계 매핑

| 요구사항/정책 | Domain | Repository | Service | Router |
|---------------|--------|------------|---------|--------|
| | | | | |

## 5. API 영향

- 경로 패턴: `/api/{domain}/{resource}`
- 엔드포인트:
- 인증/권한:

## 6. 데이터 모델

- aggregate / 필드:
- 상태 값·전이:

| 상태 | 설명 | 전이 조건 |
|------|------|-----------|
| | | |

## 7. 외부 시스템·인프라

- DB / Redis / storage / scheduler 영향:

## 8. 엣지 케이스·실패 시나리오

-

## 9. 레시피 skill

구현 시 아래 skill의 `SKILL.md`를 따른다. 해당 없으면 No.

| Skill | Required | Notes |
|-------|----------|-------|
| `create-bounded-context` | Yes / No / Extend | |
| `add-api-router` | Yes / No | |
| `add-error-code` | Yes / No | |
| `add-config-component` | Yes / No | |
| `add-lifespan-resource` | Yes / No | config 선행 여부 |

## 10. 테스트 계획

- 단위:
- 통합/API:
- 수동 확인:

## 11. Done Criteria

-

## 12. Open Questions

-

## 13. 구현 메모 (구현 단계에서 갱신)

| Step | Work | Validation |
|------|------|------------|
| 1 | | |
