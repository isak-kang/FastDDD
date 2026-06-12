---
name: add-lifespan-resource
description: Wires an external resource (Redis, database, scheduler, storage) into startup and shutdown. Use when adding connection initialization, app.state clients, graceful cleanup, or readiness checks for infrastructure dependencies.
---

# Add Lifespan Resource

Use this skill when a resource needs to connect at app startup and disconnect at shutdown.
Configuration values alone belong in `add-config-component`; this skill covers runtime wiring.

## When to Use Lifespan

| Scenario | Use lifespan |
|----------|--------------|
| Redis, MongoDB, PostgreSQL, MinIO client pool | Yes |
| APScheduler or background worker start/stop | Yes |
| `app.state.ready` or dependency readiness | Yes |
| Reading a static env flag with no connection | No — config only |
| Per-request lazy connection inside repository | Optional — prefer lifespan for shared clients |

## Workflow

1. Read `AGENTS.md`, `app/config/lifespan.py`, and the target infrastructure folder.
2. If the resource has new environment variables, run `add-config-component` first.
3. Add a client factory or wrapper under `app/infrastructure/persistence/` or `app/infrastructure/scheduler/`.
   - Example paths: `persistence/redis_client.py`, `persistence/mongo_client.py`, `scheduler/apscheduler.py`
4. Keep connection logic out of `domain` and `presentation`.
5. In `app/config/lifespan.py`:
   - Import `get_settings()` and the infrastructure client helper.
   - In `_startup(app)`: create the client, attach it to `app.state`, set `app.state.ready = True` only after required resources succeed.
   - In `_shutdown(app)`: close or stop clients in reverse startup order, then set `app.state.ready = False`.
6. Expose the client to routes and services through `app/infrastructure/dependencies/` when using FastAPI `Depends`.
7. Optionally extend `health_router` with a readiness endpoint that checks `app.state` or pings the resource.
8. Add or update focused tests (lifespan startup/shutdown or integration tests when applicable).
9. Run lints or focused import checks for changed files.

## `app.state` Convention

Use predictable attribute names on `app.state`:

```text
app.state.redis
app.state.mongo
app.state.scheduler
app.state.ready
```

Access in dependencies, not directly in domain code:

```python
from fastapi import Request

def get_redis(request: Request):
    return request.app.state.redis
```

## Example (`lifespan.py`)

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

## Rules

- Do not initialize Redis, DB, scheduler, or storage in `main.py`.
- Do not register API routers in `lifespan.py`; use `api_router.py`.
- Do not let `domain` import config, clients, or `app.state`.
- Do not read environment variables outside `app/config/components/`.
- Startup failures for required resources should fail fast before `app.state.ready = True`.
- Cleanup in `_shutdown` must be idempotent when possible.
- When adding env vars, still update `.env.example` and `docs/environment.md` via `add-config-component`.

## Related Skills

- `add-config-component` — settings and environment variables
- `add-api-router` — new HTTP endpoints after infrastructure is ready
- `create-bounded-context` — domain and repository layers that consume the resource
