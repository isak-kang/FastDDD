---
name: create-bounded-context
description: FastAPI DDD 템플릿에 bounded context를 추가한다. domain, aggregate, 유스케이스, repository, API router를 새로 만들 때 사용한다.
---

# Bounded Context 추가 (Create Bounded Context)

## 목적

새 bounded context의 domain부터 router까지 표준 레이아웃 스캐폴드를 만든다.

## 필요한 입력

- context 이름 (snake_case, 예: `order`)
- 대표 aggregate 이름 (snake_case, 보통 context와 동일, 예: `order`)
- AGENTS.md
- 기존 `app/` 구조

## 진행 순서

1. `AGENTS.md`를 읽고 기존 `app/` 구조를 확인한다.
2. bounded context 이름을 snake_case로 정한다 (예: `order`).
3. 대표 aggregate 이름을 snake_case로 정한다 (보통 context와 같음, 예: `order`).
4. `app/domain/{context}/{aggregate}.py`에 aggregate를 추가한다.
5. `app/domain/{context}/repository/{aggregate}_repository.py`에 repository port를 `{Aggregate}Repository` (ABC)로 추가한다.
6. `app/application/service/{context}_service.py`에 유스케이스 service를 추가한다.
7. `app/infrastructure/repositories/{aggregate}_repository_impl.py`에 repository 구현체를 `{Aggregate}RepositoryImpl`로 추가한다.
8. `app/infrastructure/dependencies/{context}_dependencies.py`에 의존성 주입을 추가한다.
9. `app/presentation/router/{context}_router.py`에 FastAPI router를 추가한다.
10. 필요하면 `app/shared/exceptions/domains/{context}/`에 도메인별 예외를 추가한다.
11. 성공 응답은 `ApiResponse.success()` 또는 `ApiResponse.no_content()`를 사용한다.
12. 명시적 API 실패는 `AppException`, 도메인 실패는 `{Context}Error`로 표현한다.
13. `tests/`에 focused test를 추가한다.

## 필수 레이아웃

```text
app/domain/{context}/
  __init__.py
  {aggregate}.py
  repository/
    {aggregate}_repository.py
app/application/service/{context}_service.py
app/infrastructure/repositories/{aggregate}_repository_impl.py
app/infrastructure/dependencies/{context}_dependencies.py
app/presentation/router/{context}_router.py
app/shared/exceptions/domains/{context}/
app/shared/exceptions/domains/{context}/error_code.py
tests/
```

`order` context 예시:

```text
app/domain/order/order.py
app/domain/order/repository/order_repository.py          # OrderRepository
app/infrastructure/repositories/order_repository_impl.py  # OrderRepositoryImpl
```

## 규칙

- router나 infrastructure에 비즈니스 로직을 두지 않는다.
- domain이 FastAPI, DB client, settings를 import하지 않게 한다.
- repository port (`{Aggregate}Repository`)는 domain에, 구현체 (`{Aggregate}RepositoryImpl`)는 infrastructure에 둔다.
- `{Context}Service`는 유스케이스를 조합한다: repository port 호출, domain 규칙 적용, DTO 변환. 쿼리 작성이나 DB client 직접 사용은 하지 않는다.
- `{Aggregate}RepositoryImpl`은 데이터 **저장·조회 방식**(쿼리, document mapping)만 담당한다. 비즈니스 규칙이나 유스케이스 orchestration은 하지 않는다.
- aggregate 불변식과 상태 전이는 domain model에 둔다 (예: `Order.cancel()`). repository impl에 두지 않는다.
- `dependencies/{context}_dependencies.py`에서 `{Context}Service`에 repository **port**를 주입한다. service 코드에서 impl 클래스를 직접 import하지 않는다.
- context와 aggregate 이름이 다르면 repository 파일명은 aggregate 기준으로 짓는다.
- 필요하면 `app/domain/{context}/__init__.py`에서 public domain type을 re-export한다.
- 예외 정의는 `app/shared/exceptions/` 아래에 모은다.
- 새 API router는 `app/presentation/router/api_router.py`에 등록한다.
- 저장소별 구현체가 여러 개 필요하면 `{aggregate}_repository_impl.py` 대신 `{tech}_{aggregate}_repository.py` 패턴으로 전환한다.

## 관련 skill

- `add-api-router` — router 등록만 따로 필요할 때
- `add-error-code` — 도메인별 에러 코드·예외 추가
- `add-config-component` / `add-lifespan-resource` — 외부 리소스 연동이 선행될 때
