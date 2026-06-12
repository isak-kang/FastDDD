---
name: add-config-component
description: Adds a new configuration component to the FastAPI DDD template. Use when adding Redis, database, auth, storage, external API, scheduler, or any new environment-driven settings.
---

# Add Config Component

## Workflow

1. Read `AGENTS.md`, `app/config/settings.py`, `.env.example`, and `docs/environment.md`.
2. Choose a snake_case component name, such as `redis`, `database`, `auth`, or `storage`.
3. Create `app/config/components/{name}.py`.
4. Define `{Name}Config(BaseConfig)` with typed fields and safe defaults.
5. Add `{name}: {Name}Config` to `Settings` in `app/config/settings.py`.
6. Instantiate `{Name}Config()` inside `get_settings()`.
7. Add required variables to `.env.example`.
8. Document each variable in `docs/environment.md`.
9. Update application code to access values through `settings.{name}`.
10. Run lints or focused import checks for changed files.

## Example

```python
class RedisConfig(BaseConfig):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str | None = None
```

Use it as:

```python
settings = get_settings()
settings.redis.redis_host
```

## Rules

- Do not put environment variables directly in routers, services, repositories, or domain objects.
- Do not make `domain` import `app.config`.
- Keep config fields typed and explicit.
- When adding an environment variable, update the config component, `.env.example`, and `docs/environment.md` together.

## When the Resource Needs a Connection

Config alone is not enough for Redis, DB, scheduler, or storage clients.
After this skill, continue with `add-lifespan-resource` to wire startup, shutdown, and `app.state`.
