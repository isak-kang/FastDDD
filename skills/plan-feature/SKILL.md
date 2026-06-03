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
5. API 변경이 있는 경우 `/api/{domain}/{resource}` 경로 패턴으로 엔드포인트를 정의한다.
6. DB 변경이 있는 경우 인덱스 영향을 포함한다.
7. 엣지 케이스와 실패 시나리오를 정의한다.
8. 템플릿을 사용하여 PRD를 작성한다.
9. 이 스킬에서는 코드를 구현하지 않는다.

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
