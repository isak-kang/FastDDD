# DDD Template

FastAPI + DDD + Clean Architecture 기반 백엔드 프로젝트 템플릿이다.

## 포함된 기본값

- FastAPI 앱 팩토리와 `main.py`
- `app/domain`, `app/application`, `app/infrastructure`, `app/presentation`, `app/shared` 레이어
- 컴포넌트 기반 `app/config` 설정 구조
- router registry와 lifespan 스켈레톤
- 공통 `ApiResponse` 응답 모델 (`data`는 항상 포함, 없으면 `null`)
- 공통 `ErrorCode`, `AppException`, 전역 예외 핸들러
- 응답 처리시간 헤더 `X-Process-Time-Ms` 미들웨어
- 환경 변수(`CORS_ALLOW_ORIGINS`)로 켜는 CORS 설정
- `/api/health` health check endpoint
- pytest 기반 API 테스트와 테스트 중 네트워크 연결 차단 가드
- `Dockerfile`, `.dockerignore`, `.gitignore`
- 템플릿 전용 `AGENTS.md`/`CLAUDE.md`, Cursor rules, Cursor/Claude skills

## 실행

```bash
uv sync --extra dev
cp .env.example .env
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
uv run pytest
```

컨테이너로 실행할 때:

```bash
docker build -t my-backend .
docker run --rm -p 8000:8000 --env-file .env my-backend
```

## 테스트

테스트는 DB, 캐시, 스토리지나 외부 API 없이 돈다. `tests/conftest.py`가 테스트 중 TCP 연결을 막으므로, 실수로 외부에 붙으려는 테스트는 `NetworkAccessError`로 실패한다. 의존성은 `app.dependency_overrides`와 가짜 객체로 대신한다.

## API 응답 형식

모든 응답은 같은 envelope를 쓴다. `data`는 항상 포함되며, 값이 없으면 `null`이다.

```json
{"status": 200, "code": "COMMON_SUCCESS", "message": "", "data": {}}
```

```json
{"status": 404, "code": "NOT_FOUND", "message": "Resource not found.", "data": null}
```

## 환경 변수

`.env.example`을 기준으로 `.env`를 구성한다. 각 환경 변수의 의미는 `docs/environment.md`를 참고한다.

## 개발 문서 경로

| 용도 | 경로 | Skill |
|------|------|-------|
| 기능 kickoff | `docs/features/{name}.kickoff.md` | `start-feature` |
| 리팩토링 | `docs/refactoring/{name}.refactoring.md` | `start-refactoring` |

## 템플릿 전용 skill

### 개발 workflow

- `start-feature` — 기능 착수 문서 작성 및 구현
- `start-refactoring` — 리팩토링 착수 문서 작성 및 실행
- `review-code`

### DDD 스캐폴드·인프라

- `create-bounded-context`
- `add-error-code`
- `add-config-component`
- `add-lifespan-resource`
- `add-api-router`

## 새 프로젝트 시작

FastDDD 카탈로그에서:

```bash
curl -fsSL https://raw.githubusercontent.com/isak-kang/FastDDD/main/scripts/create.sh \
  | bash -s -- ddd ./my-backend --with-shared-skills
```

카탈로그 레포를 clone한 경우:

```bash
./scripts/create.sh ddd /path/to/my-backend --with-shared-skills
```

`--with-shared-skills`는 API 명세·에러코드 문서 등 공통 문서 skill을 함께 복사한다.

복사한 프로젝트에서는 이 디렉토리의 `CLAUDE.md`(Claude Code) 또는 `AGENTS.md` + `.cursor/`(Cursor/Codex) 설정을 개발 규칙으로 사용한다.
