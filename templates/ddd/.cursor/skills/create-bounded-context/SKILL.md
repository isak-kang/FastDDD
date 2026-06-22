---
name: create-bounded-context
description: Creates a new bounded context in the FastAPI DDD template. Use when adding a new domain, aggregate, use case, repository, or API router under templates/ddd or a project created from it.
---

# Create Bounded Context

## Workflow

1. Read `AGENTS.md` and inspect the existing `app/` structure.
2. Define the bounded context name in snake_case (e.g. `order`).
3. Define the primary aggregate name in snake_case (often same as context, e.g. `order`).
4. Add aggregate under `app/domain/{context}/{aggregate}.py`.
5. Add repository port under `app/domain/{context}/repository/{aggregate}_repository.py` as `{Aggregate}Repository` (ABC).
6. Add use case services under `app/application/service/{context}_service.py`.
7. Add repository implementation under `app/infrastructure/repositories/{aggregate}_repository_impl.py` as `{Aggregate}RepositoryImpl`.
8. Add dependencies under `app/infrastructure/dependencies/{context}_dependencies.py`.
9. Add FastAPI routers under `app/presentation/router/{context}_router.py`.
10. Add domain-specific errors under `app/shared/exceptions/domains/{context}/` when needed.
11. Return responses with `ApiResponse.success()` or `ApiResponse.no_content()`.
12. Represent explicit API failures with `AppException` and mapped domain failures with `{Context}Error`.
13. Add focused tests under `tests/`.

## Required Layout

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

Example for `order` context:

```text
app/domain/order/order.py
app/domain/order/repository/order_repository.py          # OrderRepository
app/infrastructure/repositories/order_repository_impl.py  # OrderRepositoryImpl
```

## Rules

- Do not put business logic in routers or infrastructure.
- Do not let domain import FastAPI, DB clients, or settings.
- Keep repository interfaces (`{Aggregate}Repository`) in domain and implementations (`{Aggregate}RepositoryImpl`) in infrastructure.
- Name repository files by aggregate, not only by context, when they differ.
- Re-export public domain types from `app/domain/{context}/__init__.py` when useful.
- Keep exception definitions centralized under `app/shared/exceptions/`.
- Register new API routers in `app/presentation/router/api_router.py`.
- When multiple storage backends are needed, switch to `{tech}_{aggregate}_repository.py` instead of `{aggregate}_repository_impl.py`.
