# FastAPI DDD 템플릿 — Claude Code 운영 가이드

> 이 문서는 `AGENTS.md`와 동일한 규칙을 Claude Code용으로 담은 문서다. Cursor/Codex는 `AGENTS.md` + `.cursor/rules/`를 따르고, Claude Code는 이 문서 하나로 동일한 규칙을 따른다. 두 문서는 서로 동기화되어야 한다.

이 템플릿은 FastAPI + DDD + Clean Architecture 기반 백엔드 프로젝트 시작점이다. 비즈니스 로직은 도메인 중심으로 작성하고, 계층 간 의존성 방향을 지킨다.

## 핵심 원칙

- 복잡하거나 요구사항이 불명확한 **기능** 작업은 구현 전에 `start-feature` skill로 kickoff 문서(또는 Problem 1-Pager)를 먼저 작성한다.
- **구조 변경·리팩토링**은 코드 수정 전에 `start-refactoring` skill로 리팩토링 문서를 먼저 작성한다.
- 한 번에 하나의 기능, 하나의 bounded context 단위로 작게 변경한다.
- 비즈니스 규칙은 `app/domain/`에 둔다.
- 유스케이스 조합은 `app/application/`에 둔다.
- FastAPI 라우터와 요청/응답 스키마는 `app/presentation/`에 둔다.
- DB, 외부 API, 캐시, 스토리지 구현은 `app/infrastructure/`에 둔다.
- 공통 응답, 에러, 로깅, 유틸은 `app/shared/`에 둔다.

## 의존성 방향

```text
presentation -> application -> domain
infrastructure -> domain
infrastructure -> config
shared -> domain 의존 금지
domain -> 다른 레이어 의존 금지
```

`domain`은 FastAPI, Pydantic settings, DB client, HTTP client 같은 외부 프레임워크에 의존하지 않는다. config, 클라이언트, `app.state`에도 직접 의존하지 않는다.

## 표준 구조

```text
app/
  application/
    service/
  config/
    components/
    lifespan.py
    shared/
  domain/
    {context}/
      {aggregate}.py
      repository/
        {aggregate}_repository.py
      indexes/
    shared/
      enumeration/
  infrastructure/
    dependencies/
    external/
    persistence/
    repositories/
    scheduler/
  presentation/
    router/
      api_router.py
  shared/
    exceptions/
      domains/
    logging/
    response/
main.py
tests/
```

## API 응답과 에러

- 성공 응답은 `app/shared/response/api_response.py`의 `ApiResponse.success()`를 사용한다.
- 데이터가 없는 성공 응답은 `ApiResponse.no_content()`를 사용한다.
- 실패 응답은 `ApiResponse.fail()`, `ApiResponse.request_error()`, `ApiResponse.server_error()` 형식을 유지한다.
- 공통 에러 코드는 `app/shared/exceptions/error_code.py`의 `ErrorCode`에 추가한다.
- 도메인별 에러 코드는 `app/shared/exceptions/domains/{domain}/error_code.py`에 `{Domain}ErrorCode` enum으로 추가한다.
- 명시적인 API 예외는 `AppException`을 사용한다.
- 도메인별 예외는 `app/shared/exceptions/domains/{domain}/`에 모은다.
- 도메인별 기본 예외는 `{Domain}Error` 이름을 사용하고 `BaseAppException`을 상속한다.
- 도메인별 `{Domain}ErrorCode` enum 값은 `(status_code, code, default_message)` 형식을 사용한다.
- 전역 예외 핸들러와 FastAPI 등록 함수는 `app/shared/exceptions/handlers.py`에서 관리한다.
- 앱 진입점은 `register_exception_handlers(app)`만 호출한다.

## 라우터와 Lifespan

- API 라우터 등록은 `app/presentation/router/api_router.py`에서 관리한다. `main.py`와 `lifespan.py`에 라우터를 추가하지 않는다.
- `main.py`는 `app.include_router(api_router)`만 호출한다.
- 앱 시작/종료 스켈레톤은 `app/config/lifespan.py`에서 관리한다.
- DB, Redis, scheduler, storage 초기화가 생기면 `lifespan`의 `_startup()`과 `_shutdown()`에 연결한다.
- 라우터 등록은 lifespan에 두지 않는다. tier별 조건부 라우팅이 필요해질 때만 lifespan manager 패턴을 검토한다.

## 외부 리소스 연동 (책임 구분)

새 외부 리소스를 붙일 때는 아래 위치를 함께 고려한다.

| 책임 | 위치 |
|------|------|
| 환경 변수·타입·기본값 | `app/config/components/{name}.py` |
| 연결/풀/클라이언트 구현 | `app/infrastructure/persistence/` 또는 `app/infrastructure/scheduler/` |
| 시작 시 연결·종료 시 정리 | `app/config/lifespan.py`의 `_startup()` / `_shutdown()` |
| `Depends`로 주입 | `app/infrastructure/dependencies/` |
| HTTP 엔드포인트 | `app/presentation/router/` + `api_router.py` |
| 비즈니스 규칙 | `app/domain/`, `app/application/` |

연결된 클라이언트는 `app.state.{resource}`에 둔다. 예: `app.state.redis`, `app.state.mongo`.
필수 리소스 초기화가 실패하면 `app.state.ready = True`를 설정하기 전에 실패시킨다.
준비 상태 확인이 필요하면 `health_router`에 readiness 엔드포인트를 추가한다.

반복 작업은 `.claude/skills/`의 skill을 따른다. 전체 목록은 아래 **Claude skills** 절을 참고한다.

- 기능·리팩토링: `start-feature`, `start-refactoring`, `review-code`
- 스캐폴드·인프라: `create-bounded-context`, `add-error-code`, `add-config-component`, `add-lifespan-resource`, `add-api-router`

## 기능·리팩토링 워크플로우

기능을 구현할 때:

1. `start-feature` skill로 kickoff 문서를 작성하거나 기존 문서를 확인한다.
2. kickoff 범위 밖의 기능을 구현하지 않는다.
3. 구현은 kickoff 문서의 레시피 skill + 이 문서의 레이어 규칙을 따른다.
4. API가 변경되는 경우 코드 작성 전에 API 컨트랙트를 kickoff에 정의한다.
5. 비즈니스 로직은 테스트 우선으로 작성하는 것을 선호한다.
6. 비동기 작업, 외부 호출, 장시간 실행 태스크에 대한 가시성을 추가한다.

리팩토링할 때:

1. `start-refactoring` skill로 리팩토링 문서를 작성하거나 기존 문서를 확인한다.
2. In-scope / Out-of-scope를 고정하고 기능 변경을 리팩토링에 섞지 않는다.
3. 구조 변경 전 characterization / 회귀 테스트로 동작을 고정한다.
4. 작은 단위로 적용하고, 미사용 코드 제거 전 참조 검색을 한다.
5. 회귀 검증 후 변경 로그와 동작 보존 근거를 문서에 남긴다.

## 로깅

- 공통 logger는 `app/shared/logging/logger.py`의 `get_logger()`를 사용한다.
- 앱 시작 시 `setup_logging(settings.logging.log_level)`로 루트 로거를 초기화한다.
- 로그 레벨은 `LOG_LEVEL` 환경 변수로 제어한다.
- 예외 핸들러는 4xx를 warning, 5xx와 예상하지 못한 예외를 error/exception으로 기록한다.

## 설정 구조

- 통합 설정 진입점은 `app/config/settings.py`의 `get_settings()`다.
- 설정 컴포넌트는 `app/config/components/`에 둔다.
- 환경 구분 enum은 `app/config/shared/environment.py`에 둔다.
- 앱 기본 설정은 `settings.app`, 로깅 설정은 `settings.logging`으로 접근한다.
- 새 설정 영역이 생기면 `components/{name}.py`를 추가하고 `Settings`에 명시적으로 연결한다.

## 환경 변수

- 환경 변수 예시는 `.env.example`에 둔다.
- 환경 변수 설명은 `docs/environment.md`에 둔다.
- 새 환경 변수를 추가할 때는 해당 `app/config/components/*.py`, `.env.example`, `docs/environment.md`를 함께 수정한다.

성공 응답:

```json
{"status": 200, "code": "COMMON_SUCCESS", "message": "", "data": {}}
```

실패 응답:

```json
{"status": 400, "code": "AUTH_018", "message": "Auth User not found"}
```

## Bounded Context 추가 규칙

새 도메인을 추가할 때는 최소한 다음 레이어를 함께 고려한다.

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
tests/
```

### Domain 레이아웃

- bounded context는 `app/domain/{context}/` 폴더로 구분한다.
- aggregate root는 `app/domain/{context}/{aggregate}.py`에 둔다.
- context와 aggregate 이름이 같으면 `order/order.py`처럼 경로가 반복되어도 된다.
- aggregate가 여러 개면 `{aggregate}.py`와 `repository/{aggregate}_repository.py`를 aggregate마다 추가한다.
- value object가 필요해지면 `value_objects/` 서브폴더를 추가한다.

### Repository 네이밍

| 역할 | 위치 | 클래스명 |
|------|------|----------|
| Port (인터페이스) | `app/domain/{context}/repository/{aggregate}_repository.py` | `{Aggregate}Repository` |
| Adapter (구현체) | `app/infrastructure/repositories/{aggregate}_repository_impl.py` | `{Aggregate}RepositoryImpl` |

예시 (`order` context):

```text
app/domain/order/order.py                          # Order aggregate
app/domain/order/repository/order_repository.py    # OrderRepository (ABC)
app/infrastructure/repositories/order_repository_impl.py  # OrderRepositoryImpl
```

구현체가 저장소별로 여러 개 필요해지면 `{tech}_{aggregate}_repository.py` 패턴(예: `mongo_order_repository.py`)으로 전환한다.

### Service와 Repository 책임

| 레이어 | 역할 | 하는 일 | 하지 않을 일 |
|--------|------|---------|--------------|
| **domain** (`{aggregate}.py`) | 도메인 규칙 | aggregate 상태 변경, 불변식·도메인 규칙 검증 | DB/HTTP 호출, 저장소 접근 |
| **application service** (`{context}_service.py`) | 유스케이스 조합 | repository port 호출, 여러 aggregate/외부 자원 조율, 트랜잭션 경계, API DTO ↔ domain 변환 | 쿼리 작성, document mapping, 클라이언트 직접 사용 |
| **repository port** (`{aggregate}_repository.py`) | persistence 계약 | 도메인 언어로 필요한 저장·조회 메서드 정의 | 구현, 비즈니스 판단 |
| **repository impl** (`{aggregate}_repository_impl.py`) | persistence 구현 | **데이터를 어떻게 가져오고 저장할지** 결정 (쿼리, projection, mapping) | 비즈니스 규칙, 유스케이스 흐름 |

판단 기준:

- "주문 취소 가능한가?" → **domain** (`Order.cancel()`)
- "상품 조회 후 재고 확인하고 주문 생성" → **application service**
- "id로 Order를 persist에서 읽는다" → **repository port** (`get_by_id`)
- "Mongo `orders` 컬렉션에서 `_id`로 find_one" → **repository impl**

예시:

```python
# domain — 규칙
class Order:
    def cancel(self) -> None:
        if self.status == OrderStatus.SHIPPED:
            raise OrderError(...)
        self.status = OrderStatus.CANCELLED

# application — 유스케이스
class OrderService:
    async def cancel_order(self, order_id: str) -> None:
        order = await self._order_repository.get_by_id(order_id)
        if order is None:
            raise OrderError(...)
        order.cancel()
        await self._order_repository.save(order)

# infrastructure — 저장·조회 방식
class OrderRepositoryImpl(OrderRepository):
    async def get_by_id(self, order_id: str) -> Order | None:
        doc = await self._collection.find_one({"_id": order_id})
        return self._to_domain(doc) if doc else None
```

service는 repository **port**에만 의존한다. impl, DB client, `app.state`를 직접 import하지 않는다.

## 인덱스 관리

DB 등 영속 저장소를 연동할 때 적용한다. (현재 starter에는 DB가 포함되지 않는다.)

- 인덱스 **스펙**(어떤 필드·조합이 필요한지)은 `app/domain/{context}/indexes/`에 둔다.
- 인덱스 **적용**은 infrastructure에서 한곳에서 처리한다. 저장소마다 방식은 다를 수 있다.
  - RDB(PostgreSQL, MySQL 등): migration(Alembic 등)
  - DocumentDB(MongoDB 등): startup 시 통합 registry
- repository·service마다 `ensure_*_indexes`를 만들지 않는다.

구체 스캐폴드는 DB 종류와 함께 `add-lifespan-resource`·migration 설정 연동 시 추가한다.

## Python 스타일

- 모듈과 함수는 snake_case를 사용한다.
- 클래스와 Pydantic 모델은 PascalCase를 사용한다.
- 상수와 에러 코드는 UPPER_SNAKE_CASE를 사용한다.
- 포맷은 `black app/ tests/`, import 정리는 `isort app/ tests/`를 사용한다.
- 요청/응답 모델은 Pydantic 모델로 명시한다.
- 라우터 함수는 명시적인 `response_model`과 반환 타입을 작성한다.

## Claude skills

반복 작업은 `.claude/skills/`의 skill을 우선 따른다. Claude Code가 대화 맥락에 맞는 skill을 자동으로 선택한다.

### 개발 workflow

| Skill | 용도 |
|-------|------|
| `start-feature` | 기능 착수 문서 작성 및 합의된 범위 구현 |
| `start-refactoring` | 리팩토링 착수 문서 작성 및 외부 동작 유지 실행 |
| `review-code` | 코드 리뷰 |

### DDD 스캐폴드·인프라

| Skill | 용도 |
|-------|------|
| `create-bounded-context` | 새 도메인·서비스·리포지토리·라우터 스캐폴드 |
| `add-error-code` | 도메인별 에러 코드와 예외 |
| `add-config-component` | 설정 컴포넌트와 환경 변수 문서 |
| `add-lifespan-resource` | startup/shutdown 연결, `app.state` wiring |
| `add-api-router` | 새 API 라우터와 `api_router.py` 등록 |

문서·명세 skill(API 명세, 에러코드 문서, 릴리즈 노트, 블로그)은 FastDDD 카탈로그 루트 `skills/`에 있으며, `--with-shared-skills`로 프로젝트의 `.claude/skills/fastddd/`에 함께 복사할 수 있다.

원칙과 책임 구분은 이 문서에, 단계별 절차는 skill에 둔다. (Cursor/Codex를 함께 쓰는 프로젝트는 `AGENTS.md` + `.cursor/rules/` + `.cursor/skills/`가 동일한 내용을 담당한다.)

## 실행과 테스트

```bash
uv pip install -e ".[dev]"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pytest
```

커밋 전에는 포맷, import 정리, 테스트를 실행한다.
