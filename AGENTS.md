# FastDDD — 템플릿 저장소 운영 가이드

이 저장소는 여러 프로젝트 starter template을 모아 관리하는 **카탈로그**다. 특정 스택의 앱 개발 규칙은 루트가 아니라 각 `templates/{template}/` 안에 둔다.

## 저장소 역할

| 위치 | 역할 |
|------|------|
| `templates/{template}/` | 실행 가능한 프로젝트 starter (코드, AGENTS, rules, skills) |
| `skills/` | 스택 무관 문서·명세·블로그 skill |
| `scripts/` | 템플릿 복사, 공통 skill 동기화 |
| `.cursor/rules/` | **이 카탈로그 레포** 편집용 규칙만 |

## 표준 구조

```text
FastDDD/
  AGENTS.md
  README.md
  skills/                    # write-api-spec, write-error-code-spec, ...
  scripts/
    new-from-template.sh
    sync-shared-skills.sh
  templates/
    ddd/
      AGENTS.md
      .cursor/rules/
      .cursor/skills/
      app/
    mvc/                     # 추후 추가
```

## 무엇을 어디에 둘까

| 내용 | 위치 |
|------|------|
| DDD 개발 workflow (PRD, 구현, 리팩토링, 코드 리뷰) | `templates/ddd/.cursor/skills/` |
| DDD 아키텍처 규칙 | `templates/ddd/.cursor/rules/`, `templates/ddd/AGENTS.md` |
| bounded context, lifespan, router 추가 절차 | `templates/ddd/.cursor/skills/` |
| API 명세, 에러코드 문서, 릴리즈 노트, 블로그 | 루트 `skills/` |
| MVC 전용 규칙·skill | `templates/mvc/` (추가 시) |

## 템플릿 추가 원칙

1. `templates/{name}/`에 자급자족 starter를 만든다.
2. 해당 템플릿 전용 `AGENTS.md`와 `.cursor/` 설정을 함께 작성한다.
3. 개발 workflow skill은 템플릿 내부에 둔다.
4. 루트 `skills/`에 스택 전제가 들어간 skill을 추가하지 않는다.

## 새 프로젝트 생성

```bash
./scripts/new-from-template.sh ddd /path/to/my-backend --with-shared-skills
```

## 첫 번째 템플릿

`templates/ddd/` — FastAPI + DDD + Clean Architecture 백엔드. 개발 규칙은 `templates/ddd/AGENTS.md`를 따른다.
