---
name: add-lifespan-resource
description: FastAPI DDD 템플릿에 외부 리소스 startup/shutdown wiring을 추가한다. Redis, database, scheduler, storage 연결 초기화, app.state client, graceful cleanup, readiness 확인 시 사용한다.
---

# Lifespan 리소스 연결 (Add Lifespan Resource)

## 목적

앱 startup에서 리소스를 연결하고 shutdown에서 정리한다.
설정값만 필요하면 `add-config-component`를, 런타임 wiring은 이 skill을 사용한다.

## 필요한 입력

- AGENTS.md
- `app/config/lifespan.py`
- 대상 infrastructure 폴더
- (신규 env가 있으면) `add-config-component` 선행

## Lifespan 사용 기준

| 시나리오 | lifespan 사용 |
|----------|---------------|
| Redis, MongoDB, PostgreSQL, MinIO client pool | Yes |
| APScheduler 또는 background worker start/stop | Yes |
| `app.state.ready` 또는 dependency readiness | Yes |
| 연결 없이 static env flag만 읽기 | No — config만 |
| repository 내부 per-request lazy connection | Optional — shared client는 lifespan 권장 |

## 진행 순서

1. `AGENTS.md`, `app/config/lifespan.py`, 대상 infrastructure 폴더를 읽는다.
2. 리소스에 새 환경 변수가 필요하면 먼저 `add-config-component`를 적용한다.
3. `app/infrastructure/persistence/` 또는 `app/infrastructure/scheduler/` 아래에 client factory 또는 wrapper를 추가한다.
   - 예: `persistence/redis_client.py`, `persistence/mongo_client.py`, `scheduler/apscheduler.py`
4. 연결 로직을 `domain`과 `presentation` 밖에 둔다.
5. `app/config/lifespan.py`에서:
   - `get_settings()`와 infrastructure client helper를 import한다.
   - `_startup(app)`: client 생성, `app.state`에 attach, 필수 리소스 성공 후에만 `app.state.ready = True` 설정.
   - `_shutdown(app)`: startup 역순으로 client close/stop, `app.state.ready = False` 설정.
6. FastAPI `Depends`를 쓸 때 `app/infrastructure/dependencies/`를 통해 route·service에 client를 노출한다.
7. 필요하면 `health_router`에 `app.state` 또는 resource ping 기반 readiness endpoint를 추가한다.
8. focused test(lifespan startup/shutdown 또는 integration test)를 추가·갱신한다.
9. 변경 파일에 대해 lint 또는 import 검사를 실행한다.

## `app.state` 규칙

`app.state` attribute 이름을 예측 가능하게 유지한다:

```text
app.state.redis
app.state.mongo
app.state.scheduler
app.state.ready
```

domain 코드에서 직접 접근하지 않고 dependencies를 통해 사용한다:

```python
from fastapi import Request

def get_redis(request: Request):
    return request.app.state.redis
```

## 예시 (`lifespan.py`)

```python
from app.config.settings import get_settings
from app.infrastructure.persistence.redis_client import create_redis_client, close_redis_client

async def _startup(app: FastAPI) -> None:
    settings = get_settings()
    app.state.redis = await create_redis_client(settings.redis)
    app.state.ready = True


async def _shutdown(app: FastAPI) -> None:
    await close_redis_client(app.state.redis)
    app.state.ready = False
```

## 규칙

- Redis, DB, scheduler, storage를 `main.py`에서 초기화하지 않는다.
- API router를 `lifespan.py`에 등록하지 않는다. `api_router.py`를 사용한다.
- `domain`이 config, client, `app.state`를 import하지 않게 한다.
- `app/config/components/` 밖에서 환경 변수를 읽지 않는다.
- 필수 리소스 startup 실패 시 `app.state.ready = True` 전에 fail fast한다.
- `_shutdown` cleanup은 가능하면 idempotent하게 작성한다.
- env var 추가 시 `add-config-component`를 통해 `.env.example`, `docs/environment.md`도 함께 갱신한다.

## 관련 skill

- `add-config-component` — settings와 환경 변수
- `add-api-router` — infrastructure 준비 후 HTTP endpoint 추가
- `create-bounded-context` — 리소스를 사용하는 domain·repository layer 추가
