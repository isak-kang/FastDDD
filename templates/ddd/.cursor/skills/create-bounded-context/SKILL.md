---
name: create-bounded-context
description: Creates a new bounded context in the FastAPI DDD template. Use when adding a new domain, aggregate, use case, repository, or API router under templates/ddd or a project created from it.
---

# Create Bounded Context

## Workflow

1. Read `AGENTS.md` and inspect the existing `app/` structure.
2. Define the bounded context name in snake_case.
3. Add domain files under `app/domain/{context}/`.
4. Add use case services under `app/application/service/`.
5. Add repository implementations and dependencies under `app/infrastructure/`.
6. Add FastAPI routers under `app/presentation/router/`.
7. Add domain-specific errors under `app/shared/exceptions/domains/{context}/` when needed.
8. Return responses with `ApiResponse.success()` or `ApiResponse.no_content()`.
9. Represent explicit API failures with `AppException` and mapped domain failures with `{Context}Error`.
10. Add focused tests under `tests/`.

## Required Layout

```text
app/domain/{context}/
app/application/service/{context}_service.py
app/infrastructure/repositories/{context}_repository.py
app/infrastructure/dependencies/{context}_dependencies.py
app/presentation/router/{context}_router.py
app/shared/exceptions/domains/{context}/
app/shared/exceptions/domains/{context}/error_code.py
tests/
```

## Rules

- Do not put business logic in routers or infrastructure.
- Do not let domain import FastAPI, DB clients, or settings.
- Keep repository interfaces in domain and implementations in infrastructure.
- Keep exception definitions centralized under `app/shared/exceptions/`.
- Register new API routers in `app/presentation/router/api_router.py`.
