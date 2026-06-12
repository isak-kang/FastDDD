---
name: add-api-router
description: Registers a new FastAPI router in the DDD template. Use when adding HTTP endpoints, mounting a domain router, or exposing a new API resource under /api.
---

# Add API Router

## Workflow

1. Read `AGENTS.md`, `app/presentation/router/api_router.py`, and an existing router such as `health_router.py`.
2. Choose a snake_case router module name, such as `{context}_router.py`.
3. Create `app/presentation/router/{context}_router.py`.
4. Define `router = APIRouter(tags=["{context}"])` and add route handlers.
5. Return responses with `ApiResponse.success()`, `ApiResponse.no_content()`, or raise `AppException` / domain errors.
6. Keep handlers thin: delegate business logic to `app/application/service/`.
7. Register the router in `app/presentation/router/api_router.py` with `include_router`.
8. Add request/response Pydantic models in the router file or a dedicated schema module under `app/presentation/` when they grow.
9. Add focused tests under `tests/`.
10. Run lints or focused import checks for changed files.

## Example

`app/presentation/router/user_router.py`:

```python
router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=ApiResponse[list[UserResponse]])
async def list_users(service: UserService = Depends(get_user_service)) -> ApiResponse[list[UserResponse]]:
    users = await service.list_users()
    return ApiResponse.success(users)
```

`app/presentation/router/api_router.py`:

```python
from app.presentation.router.user_router import router as user_router

api_router.include_router(user_router)
```

## Rules

- Register routers only in `api_router.py`, not in `main.py` or `lifespan.py`.
- Do not put business rules in route handlers.
- Do not let routers import DB or Redis clients directly; use application services and `Depends`.
- Use the `/api` prefix from `api_router`; add resource-specific `prefix` on child routers when needed.
- Prefer `ApiResponse` for success and mapped exceptions for failures.

## Related Skills

- `create-bounded-context` — full domain, service, repository, and router scaffold
- `add-lifespan-resource` — when endpoints depend on startup-initialized clients
