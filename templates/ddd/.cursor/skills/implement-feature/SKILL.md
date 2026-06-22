---
name: implement-feature
description: 승인된 PRD를 기반으로 기능을 구현한다. 기존 PRD 문서에서 개발을 시작할 때 사용한다.
---

# 기능 구현 (Implement Feature)

## 목적

승인된 PRD를 기반으로 Clean Architecture 구조에 맞게 기능을 구현한다.

## 필요한 입력

- PRD 마크다운 파일 (`docs/features/{feature-name}.prd.md`)
- AGENTS.md
- 기존 코드베이스
- 기존 테스트 및 컨벤션

## 진행 순서

1. PRD를 먼저 읽는다.
2. AGENTS.md를 읽고 레포지토리 규칙을 따른다.
3. PRD의 `Implementation Skills` 섹션(또는 레이어별 영향)을 보고 필요한 레시피 skill을 식별한다.
4. 아래 **레시피 skill 위임** 표에 해당하는 skill이 있으면, 각 skill의 `SKILL.md`를 읽고 workflow를 먼저 따른다.
5. 기존 폴더 구조를 확인한다. 레시피 skill에 정의되지 않은 파일 위치를 임의로 결정하지 않는다.
6. 레시피 skill 적용 순서는 일반적으로 아래와 같다:
   - `add-config-component`
   - `add-lifespan-resource`
   - `create-bounded-context`
   - `add-error-code`
   - `add-api-router`
7. 스캐폴드·인프라 wiring이 끝난 뒤, PRD에만 있는 비즈니스 로직·DTO·테스트를 채운다.
8. 구현 계획을 수립할 때 레이어 순서를 따른다:
   - **domain**: 도메인 모델, Repository 인터페이스
   - **application**: 유스케이스 서비스, DTO
   - **infrastructure**: Repository 구현체, 의존성 주입
   - **presentation**: 라우터, 요청/응답 스키마
9. 비즈니스 로직은 테스트 우선으로 작성하는 것을 선호한다.
10. API가 변경되는 경우 `/api/{domain}/{resource}` 경로 패턴을 따른다.
11. 한 번에 하나의 논리적 단계씩 구현한다.
12. 여러 시스템이 관여된 경우 데이터 일관성과 부분 실패를 처리한다.
13. 비동기 작업, 외부 호출, 장시간 실행 태스크에 대한 가시성을 추가한다.
14. 검증 단계를 실행하거나 설명한다.
15. 최종 구현 요약을 작성한다. 적용한 레시피 skill 목록을 포함한다.

## 레시피 skill 위임

PRD에 해당 작업이 있으면 `.cursor/skills/{skill-name}/SKILL.md`를 읽고 workflow를 따른다.
레시피 skill이 파일 경로, 클래스명, 등록 위치를 이미 정의하므로 중복 규칙을 만들지 않는다.

| PRD 영향 | Skill |
|----------|-------|
| 새 bounded context / aggregate / repository port | `create-bounded-context` |
| HTTP 엔드포인트 추가 | `add-api-router` |
| API 에러 코드 / 도메인 예외 | `add-error-code` |
| 환경 변수 / 설정 컴포넌트 | `add-config-component` |
| startup·shutdown 리소스 연결 | `add-lifespan-resource` |

판단 가이드:

- PRD에 `Implementation Skills`가 있으면 그 목록을 우선 따른다.
- 없으면 PRD의 레이어별 영향을 보고 위 표에서 skill을 선택한다.
- context 전체가 PRD scope면 `create-bounded-context`를 적용한 뒤, PRD에만 있는 유스케이스·비즈니스 규칙을 구현한다.
- context는 있고 API만 추가하면 `add-api-router`만 적용한다.
- `add-config-component`와 `add-lifespan-resource`가 모두 필요하면 config → lifespan 순서를 따른다.
- 구현이 끝나면 `review-code`로 마무리 검토를 권장한다.

## 아키텍처 규칙

- PRD에 명시되지 않은 기능을 구현하지 않는다.
- 의존성 방향을 반드시 준수한다: `presentation → application → domain`, `infrastructure → domain`
- router/controller는 얇게 유지한다. 비즈니스 로직을 두지 않는다.
- 비즈니스 로직은 application/domain 레이어에만 위치한다.
- DB 및 외부 시스템 접근은 infrastructure 레이어에만 위치한다.
- 요청/응답 모델은 반드시 Pydantic으로 작성한다.
- 응답은 `ApiResponse` 래퍼를 사용한다.
- 생성, 업로드, 실행, 재시도 작업에서 멱등성을 고려한다.

## 네이밍 규칙

- 파일/모듈: snake_case (`user_service.py`)
- 클래스: PascalCase (`UserService`)
- 함수/변수: snake_case (`get_user_by_id`)
- 상수: UPPER_SNAKE_CASE
- 요청/응답 Pydantic 모델: PascalCase (`CreateUserRequest`)

## 출력

- 구현 계획
- 코드 변경 사항 (레이어별)
- 테스트
- 검증 결과
- 잔여 리스크
