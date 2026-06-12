# DDD Template

FastAPI + DDD + Clean Architecture 기반 백엔드 프로젝트 템플릿이다.

## 포함된 기본값

- FastAPI 앱 팩토리와 `main.py`
- `app/domain`, `app/application`, `app/infrastructure`, `app/presentation`, `app/shared` 레이어
- 컴포넌트 기반 `app/config` 설정 구조
- router registry와 lifespan 스켈레톤
- 공통 `ApiResponse` 응답 모델
- 공통 `ErrorCode`, `AppException`, 전역 예외 핸들러
- `/api/health` health check endpoint
- pytest 기반 API 테스트
- 템플릿 전용 `AGENTS.md`, Cursor rules, Cursor skills

## 실행

```bash
uv pip install -e ".[dev]"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pytest
```

## 환경 변수

`.env.example`을 기준으로 `.env`를 구성한다. 각 환경 변수의 의미는 `docs/environment.md`를 참고한다.

## 템플릿 전용 skill

### 개발 workflow

- `plan-feature` / `implement-feature`
- `plan-refactoring` / `implement-refactoring`
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
./scripts/new-from-template.sh ddd /path/to/my-backend --with-shared-skills
```

`--with-shared-skills`는 API 명세·에러코드 문서 등 공통 문서 skill을 함께 복사한다.

복사한 프로젝트에서는 이 디렉토리의 `AGENTS.md`와 `.cursor/` 설정을 개발 규칙으로 사용한다.
