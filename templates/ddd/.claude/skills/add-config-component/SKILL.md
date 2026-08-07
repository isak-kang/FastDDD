---
name: add-config-component
description: FastAPI DDD 템플릿에 설정 컴포넌트를 추가한다. Redis, database, auth, storage, external API, scheduler 등 환경 변수 기반 설정 추가 시 사용한다.
---

# 설정 컴포넌트 추가 (Add Config Component)

## 목적

환경 변수 기반 설정을 `app/config/components/`에 타입-safe하게 추가한다.

## 필요한 입력

- AGENTS.md
- `app/config/settings.py`
- `.env.example`
- `docs/environment.md`
- 컴포넌트 이름 (snake_case, 예: `redis`, `database`, `auth`, `storage`)

## 진행 순서

1. `AGENTS.md`, `app/config/settings.py`, `.env.example`, `docs/environment.md`를 읽는다.
2. 컴포넌트 이름을 snake_case로 정한다 (예: `redis`, `database`, `auth`, `storage`).
3. `app/config/components/{name}.py`를 생성한다.
4. `{Name}Config(BaseConfig)`를 typed field와 안전한 default로 정의한다.
5. `app/config/settings.py`의 `Settings`에 `{name}: {Name}Config`를 추가한다.
6. `get_settings()` 안에서 `{Name}Config()`를 인스턴스화한다.
7. 필요한 환경 변수를 `.env.example`에 추가한다.
8. 각 변수를 `docs/environment.md`에 문서화한다.
9. 애플리케이션 코드는 `settings.{name}`으로 값에 접근하게 한다.
10. 변경 파일에 대해 lint 또는 import 검사를 실행한다.

## 예시

```python
class RedisConfig(BaseConfig):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str | None = None
```

사용:

```python
settings = get_settings()
settings.redis.redis_host
```

## 규칙

- router, service, repository, domain object에 환경 변수를 직접 두지 않는다.
- `domain`이 `app.config`를 import하지 않게 한다.
- config field는 typed하고 명시적으로 유지한다.
- 환경 변수를 추가할 때는 config component, `.env.example`, `docs/environment.md`를 함께 수정한다.

## 연결이 필요한 리소스

Redis, DB, scheduler, storage client처럼 **런타임 연결**이 필요하면 config만으로는 부족하다.
이 skill 적용 후 `add-lifespan-resource`로 startup, shutdown, `app.state` wiring을 이어서 한다.

## 관련 skill

- `add-lifespan-resource` — 설정값으로 client 연결·해제
- `create-bounded-context` — 설정/리소스 준비 후 domain 추가
