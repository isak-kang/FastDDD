---
name: add-api-router
description: FastAPI DDD 템플릿에 API router를 등록한다. HTTP 엔드포인트 추가, domain router 마운트, /api 하위 리소스 노출 시 사용한다.
---

# API Router 추가 (Add API Router)

## 목적

새 FastAPI router 모듈을 만들고 `api_router.py`에 등록한다.

## 필요한 입력

- AGENTS.md
- `app/presentation/router/api_router.py`
- 참고용 기존 router (예: `health_router.py`)
- context 이름 (snake_case, 예: `order`)

## 진행 순서

1. `AGENTS.md`, `app/presentation/router/api_router.py`, 기존 router(예: `health_router.py`)를 읽는다.
2. router 모듈 이름을 snake_case로 정한다 (예: `{context}_router.py`).
3. `app/presentation/router/{context}_router.py`를 생성한다.
4. `router = APIRouter(tags=["{context}"])`를 정의하고 route handler를 추가한다.
5. `ApiResponse.success()`, `ApiResponse.no_content()`로 응답하거나 `AppException` / domain error를 raise한다.
6. handler는 얇게 유지하고 비즈니스 로직은 `app/application/service/`에 위임한다.
7. `app/presentation/router/api_router.py`에서 `include_router`로 등록한다.
8. request/response Pydantic model이 커지면 router 파일 또는 `app/presentation/` 아래 schema 모듈로 분리한다.
9. `tests/`에 focused test를 추가한다.
10. 변경 파일에 대해 lint 또는 import 검사를 실행한다.

## 예시

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

## 규칙

- router 등록은 `api_router.py`에서만 한다. `main.py`나 `lifespan.py`에 등록하지 않는다.
- route handler에 비즈니스 규칙을 두지 않는다.
- router가 DB나 Redis client를 직접 import하지 않게 한다. application service와 `Depends`를 사용한다.
- `/api` prefix는 `api_router`에서 처리한다. resource별 `prefix`는 child router에 둔다.
- 성공 응답은 `ApiResponse`, 실패는 매핑된 exception을 사용한다.

## 관련 skill

- `create-bounded-context` — domain, service, repository, router 전체 스캐폴드
- `add-lifespan-resource` — startup에서 초기화된 client에 endpoint가 의존할 때
