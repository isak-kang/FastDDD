---
name: plan-feature
description: 기능 구현 전 PRD를 작성한다. 코딩 전에 요구사항, 범위, API 영향, DB 영향, 테스트 전략, 완료 기준을 정의할 때 사용한다.
---

# 기능 계획 (Plan Feature)

## 목적

코드 작성 전에 구조화된 PRD를 작성한다.

## 필요한 입력

- 사용자 요청
- 기존 레포지토리 컨텍스트
- AGENTS.md
- 관련 이슈, 티켓, 논의 (있는 경우)

## 진행 순서

1. 요청된 기능을 파악한다.
2. 문제, 목표, 비목표를 정의한다.
3. 영향받는 사용자와 시스템을 파악한다.
4. Clean Architecture 레이어별 영향을 분석한다:
   - **domain**: 새로운 도메인 모델, Repository 인터페이스 필요 여부
   - **application**: 새로운 유스케이스 서비스, DTO 필요 여부
   - **infrastructure**: Repository 구현체, 외부 연동 필요 여부
   - **presentation**: 새로운 라우터, 요청/응답 스키마 필요 여부
5. 아래 **레시피 skill 위임** 표를 기준으로 PRD에 필요한 skill을 식별하고, PRD의 `Implementation Skills` 섹션에 기록한다.
6. API 변경이 있는 경우 `/api/{domain}/{resource}` 경로 패턴으로 엔드포인트를 정의한다.
7. DB 변경이 있는 경우 인덱스 영향을 포함한다.
8. 엣지 케이스와 실패 시나리오를 정의한다.
9. 템플릿을 사용하여 PRD를 작성한다.
10. 이 스킬에서는 코드를 구현하지 않는다.

## 레시피 skill 위임

`implement-feature`가 구현할 때 아래 skill의 `SKILL.md`를 읽고 workflow를 따르도록, PRD에 필요한 skill을 명시한다.

| PRD 영향 | Skill | 해당 여부를 PRD에 표시 |
|----------|-------|------------------------|
| 새 bounded context / aggregate / repository port | `create-bounded-context` | Yes / No / Extend existing |
| HTTP 엔드포인트 추가 | `add-api-router` | Yes / No |
| API 에러 코드 / 도메인 예외 | `add-error-code` | Yes / No |
| 환경 변수 / 설정 컴포넌트 | `add-config-component` | Yes / No |
| startup·shutdown 리소스 연결 | `add-lifespan-resource` | Yes / No |

판단 가이드:

- context 전체가 새로 생기면 `create-bounded-context`를 Yes로 표시한다.
- context는 이미 있고 API만 추가하면 `create-bounded-context`는 No, `add-api-router`는 Yes로 표시한다.
- 외부 리소스 env가 새로 필요하면 `add-config-component`를 Yes로 표시한다.
- 앱 시작 시 클라이언트 연결이 필요하면 `add-lifespan-resource`를 Yes로 표시한다. config가 선행되면 PRD에 그 순서를 적는다.
- 새 API 실패 응답이 필요하면 `add-error-code`를 Yes로 표시한다.

## 출력

다음 경로에 생성 또는 업데이트:

```text
docs/features/{feature-name}.prd.md
```

## 품질 규칙

- 숨겨진 요구사항을 추가하지 않는다.
- 불명확한 요구사항은 Open Questions로 표시한다.
- 목표(Goal)와 비목표(Non-Goal)를 명확히 구분한다.
- 완료 기준(Done Criteria)을 반드시 포함한다.
