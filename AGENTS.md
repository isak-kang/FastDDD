# ISAK Backend — 개발 방법론 & 아키텍처 가이드

나만의 개발 방법론을 적용한 AGENTS.md 파일

---

## 목차

1. [핵심 개발 철학](#1-핵심-개발-철학)
2. [아키텍처 패턴](#2-아키텍처-패턴)
3. [레포지토리 구조](#3-레포지토리-구조)
4. [주요 기술 스택](#4-주요-기술-스택)
5. [코딩 컨벤션](#5-코딩-컨벤션)
6. [API 구조](#6-api-구조)
7. [테스트](#7-테스트)
8. [개발 환경 설정](#8-개발-환경-설정)
9. [환경 변수 및 설정](#9-환경-변수-및-설정)
10. [빌드 및 배포](#10-빌드-및-배포)
11. [참고 자료 & 체크리스트](#11-참고-자료--체크리스트)

---

## 1. 핵심 개발 철학

> AI와 함께 작업할 때도, 혼자 작업할 때도 이 철학을 먼저 따른다.

### 1.1 Problem Definition First

복잡하거나 요구사항이 불명확한 경우, **코딩 전에 반드시 Problem 1-Pager를 먼저 작성한다.**

| 항목 | 설명 |
|------|------|
| **배경(Background)** | 변경이 필요한 맥락과 동기 |
| **문제(Problem)** | 해결하려는 이슈 |
| **목표(Goal)** | 성공 기준 |
| **비목표(Non-goals)** | 범위 밖 |
| **제약(Constraints)** | 기술·비즈니스 제약 |

상세 룰보다 **목적/배경/제약** 중심의 스펙을 우선한다.

### 1.2 개발 원칙

- **작게 시작한다** — 한 번에 하나의 기능, 하나의 책임
- **레이어를 지킨다** — 계층 간 의존성 방향을 절대 역전시키지 않는다
- **도메인이 중심이다** — 비즈니스 로직은 반드시 domain 레이어에 위치한다
- **명시적으로 작성한다** — 암묵적 동작보다 명시적 코드를 선호한다
- **커밋 전 포맷 필수** — `black app/`, `isort app/` 실행 후 커밋한다

### 1.3 AI 에이전트에 대한 지시

- 새 파일 생성 전에 반드시 기존 폴더 구조를 확인한다
- 기능 추가 시 해당 bounded context의 4개 레이어(application/domain/infrastructure/presentation)를 모두 고려한다
- 불명확한 요구사항은 구현 전에 질문한다

---

## 2. 아키텍처 패턴

### 2.1 Clean Architecture 계층 구조

| 레이어 | 역할 |
|--------|------|
| **presentation** | FastAPI 라우터·컨트롤러·스키마 |
| **application** | DTO, 유스케이스 서비스 (도메인별) |
| **domain** | 도메인 모델, Repository 인터페이스 |
| **infrastructure** | DB/캐시/스토리지 클라이언트, Repository 구현체, 의존성 주입, 스케줄러 |
| **shared** | 로깅, 예외, i18n 등 공통 유틸 |

### 2.2 의존성 방향 (절대 역전 금지)

```
presentation → application → domain
infrastructure → domain, config
domain은 어떤 레이어에도 의존하지 않는다
```

### 2.3 데이터 흐름

```
HTTP 요청 → 라우터 → 의존성 주입(Repository/Service)
  → Application Service → Domain/Repository → DB·외부 API
  → Pydantic 스키마 직렬화 → 공통 응답 포맷 반환
```

### 2.4 인증·인가

- JWT (email/비밀번호, SSO)
- `get_current_user` 의존성으로 `request.state.current_user` 설정

---

## 3. 레포지토리 구조

### 3.1 표준 폴더 구조

```
app/
  application/
    service/              # 유스케이스 서비스 (도메인별)
  config/                 # 설정, lifespan 매니저
  domain/                 # 도메인 모델·Repository 인터페이스
    {bounded_context}/
      indexes/            # 인덱스 스펙 (도메인 레이어에서 관리)
    shared/enumeration/
  infrastructure/
    dependencies/         # FastAPI 의존성 (도메인별)
    external/             # 3rd-party API 클라이언트
    persistence/          # DB, Redis, MinIO 등 클라이언트
    repositories/         # Repository 구현체
    scheduler/            # 스케줄러
  presentation/
    router/               # API 라우터
    DTO/                  # Request, Response DTO

  shared/                 # 로깅, 예외, i18n 등

main.py                   # ASGI 진입점
docker/                   # Dockerfile
scripts/                  # 마이그레이션·운영 스크립트
tests/                    # 단위·통합 테스트
```

### 3.2 네이밍 컨벤션

| 대상 | 규칙 | 예시 |
|------|------|------|
| 모듈/파일 | snake_case | `user_service.py`, `auth_controller.py` |
| 클래스 | PascalCase | `AuthService`, `UserRepository` |
| 함수/변수 | snake_case | `get_auth_service`, `user_repo` |
| 상수 | UPPER_SNAKE_CASE | `LOG_ACTIVITY_SPEC` |
| 요청/응답 모델 | Pydantic, PascalCase | `SSOLoginRequest`, `ApiResponse` |

### 3.3 DB 인덱스 관리 컨벤션

- 인덱스 스펙은 **도메인 레이어**에서 관리 (`app/domain/{context}/indexes/*.py`)
- 각 도메인의 `__init__.py`에서 `*_INDEX_SPECS`로 묶어 export
- 등록은 `app/infrastructure/persistence/documentdb/index_registry.py`에서 통합 관리
- 개별 인프라 모듈에 ad-hoc `ensure_*_indexes` 함수를 새로 만들지 않는다

---

## 4. 주요 기술 스택

| 분류 | 기술 |
|------|------|
| **런타임** | Python 3.10+ |
| **프레임워크** | FastAPI, Uvicorn / Gunicorn |
| **검증** | Pydantic, pydantic-settings |
| **DB** | MongoDB (PyMongo), PostgreSQL |
| **캐시·스트림** | Redis (캐시·세션·락·Streams) |
| **스토리지** | MinIO |
| **인증** | python-jose (JWT), passlib[bcrypt] |
| **스케줄러** | APScheduler |
| **로깅** | Loguru |
| **LLM** | OpenAI SDK (필요 시) |
| **패키지 관리** | uv (권장) 또는 pip + pyproject.toml |

---

## 5. 코딩 컨벤션

### 5.1 Python 스타일

- **포맷터**: black (줄 길이 120), isort
- 들여쓰기 4칸, 모듈/함수 snake_case, 클래스 PascalCase
- 실행: `black app/`, `isort app/`

### 5.2 Import 순서

- isort 프로필로 정리 (first party: `app`, local: `app.shared`, `app.config`)

### 5.3 모델

- 요청/응답은 Pydantic 모델 사용
- 도메인 모델은 dataclass 또는 Pydantic으로 일관되게 사용

---

## 6. API 구조

### 6.1 라우터 경로 패턴

```
/api/{domain}/{resource}
```

### 6.2 공통 응답 포맷

- `ApiResponse` 래퍼 사용 (`app/presentation/api/shared`)
- 성공: `{"success": true, "data": {...}}`
- 실패: `{"success": false, "error": {"code": "...", "message": "..."}}`

---

## 7. 테스트

### 7.1 설정

- **pytest** (pytest.ini)
- 커버리지: `--cov=app`, `--cov-fail-under=60`

### 7.2 실행

```bash
pytest
pytest tests/unit/
pytest --cov=app --cov-report=html
```

### 7.3 컨벤션

- 테스트 파일: `test_*.py` / 함수: `test_*`
- 마커: `@pytest.mark.integration`, `@pytest.mark.api` 등으로 구분

---

## 8. 개발 환경 설정

### 8.1 필수 요구사항

- Python >= 3.10, < 3.13
- uv (권장) 또는 pip

### 8.2 설치 및 실행

```bash
uv pip install -e .
uv pip install -e ".[dev]"   # 개발 도구 포함

python main.py
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 9. 환경 변수 및 설정

- Redis, MongoDB, PostgreSQL, MinIO 연결 정보는 환경 변수로 주입
- `app/config`에서 pydantic-settings 기반으로 로드
- 환경 변수는 Git에 올리지 않는다 (`.env` → `.gitignore`)

---

## 10. 빌드 및 배포

- 티어별 Dockerfile: `docker/` 디렉토리
- 배포 전 환경 변수 설정 확인 필수

---

## 11. 참고 자료 & 체크리스트

### 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Pydantic 문서](https://docs.pydantic.dev/)
- [Python 공식 문서](https://docs.python.org/3/)

### 커밋 전 체크리스트

- [ ] Problem 1-Pager 작성 완료 (요구사항이 복잡한 경우)
- [ ] 모듈/파일은 snake_case, 클래스는 PascalCase, 상수는 UPPER_SNAKE_CASE
- [ ] 새 기능은 해당 bounded context의 4개 레이어에 맞게 구성
- [ ] API 요청/응답은 Pydantic 모델 사용
- [ ] `black app/`, `isort app/` 실행 완료
- [ ] 테스트 추가 시 `test_*.py`, `test_*` 네이밍 및 마커 사용
- [ ] 커밋 메시지 type-prefix 스타일 (`feat:`, `fix:`, `refactor:` 등), 72자 이내
