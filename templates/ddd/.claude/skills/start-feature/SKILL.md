---
name: start-feature
description: 기능 개발 착수 문서를 작성하고, 합의된 범위대로 구현한다. 범위·구현 순서·레시피 skill 합의가 필요할 때 사용한다.
---

# 기능 착수 (Start Feature)

## 목적

기능 개발 전 `docs/features/`에 kickoff 문서를 작성하고, 합의 후 같은 문서를 기준으로 구현한다.

- **문서 단계**: 범위·레이어 영향·레시피 skill·완료 기준 정리 (코드 작성 금지)
- **구현 단계**: kickoff 문서 + `AGENTS.md` + 레시피 skill로 구현

## 필요한 입력

- 사용자 요청 또는 이슈/티켓
- `AGENTS.md`
- 기존 코드베이스

## Phase A — kickoff 문서 작성

1. 문서 경로를 정한다. 기본: `docs/features/{feature-name}.kickoff.md`
2. `AGENTS.md`를 읽고 레이어·아키텍처 규칙을 확인한다.
3. 요구사항이 복잡하거나 불명확하면 Problem 1-Pager를 먼저 작성하거나 질문한다.
4. `templates/kickoff-template.md`를 복사해 문서를 생성한다.
5. **레시피 skill** 표에 필요한 skill을 Yes/No로 표시한다.
6. 이 단계에서는 코드를 구현하지 않는다.

## Phase B — 구현

kickoff 문서가 합의된 뒤, 사용자가 구현을 요청하면 진행한다.

1. kickoff 문서와 `AGENTS.md`를 읽는다.
2. 문서의 **레시피 skill** 표에서 Yes인 skill의 `SKILL.md` workflow를 먼저 따른다.
3. 일반 적용 순서: `add-config-component` → `add-lifespan-resource` → `create-bounded-context` → `add-error-code` → `add-api-router`
4. 스캐폴드·인프라 wiring 후 kickoff에만 있는 비즈니스 로직·테스트를 구현한다.
5. 개발 순서: domain → repository port/impl → service → router
6. 검증(pytest, lint) 후 구현 요약을 작성한다.
7. `review-code` skill로 마무리 검토를 권장한다.

## 레시피 skill (문서에 표시)

| kickoff 영향 | Skill |
|--------------|-------|
| 새 bounded context / aggregate / repository port | `create-bounded-context` |
| HTTP 엔드포인트 추가 | `add-api-router` |
| API 에러 코드 / 도메인 예외 | `add-error-code` |
| 환경 변수 / 설정 컴포넌트 | `add-config-component` |
| startup·shutdown 리소스 연결 | `add-lifespan-resource` |

아키텍처 원칙·Service/Repository 책임·네이밍은 `CLAUDE.md`를 따른다. skill 본문에 중복 정의하지 않는다.

## 작성 원칙

- kickoff는 **착수·실행 계획** 문서다. 구현 후 회고나 결과 보고서처럼 쓰지 않는다.
- 숨겨진 요구사항을 추가하지 않는다.
- 불명확한 항목은 Open Questions로 남긴다.
- Goal과 Non-Goal, Done Criteria를 반드시 포함한다.

## 넣지 말아야 할 것

- `AGENTS.md`와 중복되는 장문의 아키텍처 설명
- 구현 전에는 의미 없는 확정 응답 예시 나열
- 실행 계획과 무관한 배경 서술

## Problem 1-Pager

복잡하거나 불명확한 경우 코딩 전에 작성한다.

- Background, Problem, Goal, Non-goals, Constraints

## 자산

- `templates/kickoff-template.md` — kickoff 문서 기본 템플릿
