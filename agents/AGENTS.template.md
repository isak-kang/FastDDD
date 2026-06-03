# {프로젝트명} — 개발 방법론 & 아키텍처 가이드

---

## 1. 핵심 개발 철학

> AI와 함께 작업할 때도, 혼자 작업할 때도 이 철학을 먼저 따른다.

### Problem Definition First

복잡하거나 요구사항이 불명확한 경우, **코딩 전에 반드시 PRD를 먼저 작성한다.**

| 항목 | 설명 |
|------|------|
| **배경(Background)** | 변경이 필요한 맥락과 동기 |
| **문제(Problem)** | 해결하려는 이슈 |
| **목표(Goal)** | 성공 기준 |
| **비목표(Non-goals)** | 범위 밖 |
| **제약(Constraints)** | 기술·비즈니스 제약 |

### 개발 원칙

- **작게 시작한다** — 한 번에 하나의 기능, 하나의 책임
- **레이어를 지킨다** — 계층 간 의존성 방향을 절대 역전시키지 않는다
- **도메인이 중심이다** — 비즈니스 로직은 반드시 domain 레이어에 위치한다
- **명시적으로 작성한다** — 암묵적 동작보다 명시적 코드를 선호한다
- **커밋 전 포맷 필수** — `black app/`, `isort app/` 실행 후 커밋한다

### AI 에이전트에 대한 지시

- 새 파일 생성 전에 반드시 기존 폴더 구조를 확인한다
- 기능 추가 시 해당 bounded context의 4개 레이어(application/domain/infrastructure/presentation)를 모두 고려한다
- 불명확한 요구사항은 구현 전에 질문한다

---

## 2. 아키텍처 패턴

### Clean Architecture 계층 구조

| 레이어 | 역할 |
|--------|------|
| **presentation** | FastAPI 라우터·컨트롤러·스키마 |
| **application** | DTO, 유스케이스 서비스 (도메인별) |
| **domain** | 도메인 모델, Repository 인터페이스 |
| **infrastructure** | DB/캐시/스토리지 클라이언트, Repository 구현체, 의존성 주입, 스케줄러 |
| **shared** | 로깅, 예외, i18n 등 공통 유틸 |

### 의존성 방향 (절대 역전 금지)

```
presentation → application → domain
infrastructure → domain, config
domain은 어떤 레이어에도 의존하지 않는다
```

### 데이터 흐름

```
HTTP 요청 → 라우터 → 의존성 주입(Repository/Service)
  → Application Service → Domain/Repository → DB·외부 API
  → Pydantic 스키마 직렬화 → ApiResponse 반환
```

---

## 3. 레포지토리 구조

### 표준 폴더 구조

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
docs/
  features/               # PRD 문서
  api/                    # API 명세
  errors/                 # 에러코드 명세
  refactoring/            # 리팩토링 계획
  releases/               # 릴리즈 노트
```

### 네이밍 컨벤션

| 대상 | 규칙 | 예시 |
|------|------|------|
| 모듈/파일 | snake_case | `user_service.py`, `auth_controller.py` |
| 클래스 | PascalCase | `AuthService`, `UserRepository` |
| 함수/변수 | snake_case | `get_auth_service`, `user_repo` |
| 상수 | UPPER_SNAKE_CASE | `LOG_ACTIVITY_SPEC` |
| 요청/응답 모델 | Pydantic, PascalCase | `LoginRequest`, `ApiResponse` |

### DB 인덱스 관리

- 인덱스 스펙은 **도메인 레이어**에서 관리 (`app/domain/{context}/indexes/*.py`)
- 각 도메인의 `__init__.py`에서 `*_INDEX_SPECS`로 묶어 export
- 등록은 `app/infrastructure/persistence/documentdb/index_registry.py`에서 통합 관리
- 개별 인프라 모듈에 ad-hoc `ensure_*_indexes` 함수를 새로 만들지 않는다

---

## 4. 기술 스택

| 분류 | 기술 |
|------|------|
| **런타임** | Python 3.10+ |
| **프레임워크** | FastAPI, Uvicorn / Gunicorn |
| **검증** | Pydantic, pydantic-settings |
| **DB** | {프로젝트에 맞게 작성} |
| **캐시** | {프로젝트에 맞게 작성} |
| **인증** | python-jose (JWT), passlib[bcrypt] |
| **로깅** | Loguru |
| **패키지 관리** | uv |

---

## 5. 코딩 컨벤션

- **포맷터**: black (줄 길이 120), isort
- 들여쓰기 4칸, 모듈/함수 snake_case, 클래스 PascalCase
- 요청/응답은 Pydantic 모델 사용
- 도메인 모델은 dataclass 또는 Pydantic으로 일관되게 사용
- isort first party: `app`, local: `app.shared`, `app.config`

---

## 6. API 구조

### 라우터 경로 패턴

```
/api/{domain}/{resource}
```

### 공통 응답 포맷

- `ApiResponse` 래퍼 사용
- 성공: `{"success": true, "data": {...}}`
- 실패: `{"success": false, "error": {"code": "...", "message": "..."}}`

---

## 7. 테스트

- **pytest** + `--cov=app`, `--cov-fail-under=60`
- 테스트 파일: `test_*.py` / 함수: `test_*`
- 마커: `@pytest.mark.integration`, `@pytest.mark.api`
- 비즈니스 규칙은 서비스 레벨 테스트 필수
- API 변경 시 요청/응답 컨트랙트 검증 필수

---

## 8. 문서 규칙

- API 변경 시 `docs/api/` 업데이트
- 에러 추가/변경 시 `docs/errors/` 업데이트
- 배포 시 `docs/releases/` 릴리즈 노트 작성
- 문서는 실제 DTO와 응답 형식에 맞게 유지한다

---

## 9. 커밋 전 체크리스트

- [ ] PRD 작성 완료 (요구사항이 복잡한 경우)
- [ ] 모듈/파일은 snake_case, 클래스는 PascalCase, 상수는 UPPER_SNAKE_CASE
- [ ] 새 기능은 해당 bounded context의 4개 레이어에 맞게 구성
- [ ] API 요청/응답은 Pydantic 모델 사용
- [ ] `black app/`, `isort app/` 실행 완료
- [ ] 테스트 추가 시 `test_*.py`, `test_*` 네이밍 및 마커 사용
- [ ] 커밋 메시지 type-prefix 스타일 (`feat:`, `fix:`, `refactor:` 등), 72자 이내
