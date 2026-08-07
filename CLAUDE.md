# FastDDD — 템플릿 저장소 운영 가이드 (Claude Code)

> 이 문서는 `AGENTS.md` + `.cursor/rules/00-catalog.mdc`와 동일한 규칙을 Claude Code용으로 담은 문서다. Cursor/Codex는 `AGENTS.md`(+`.cursor/rules/`)를 따르고, Claude Code는 이 문서 하나로 동일한 규칙을 따른다. 두 문서는 서로 동기화되어야 한다.

이 저장소는 여러 프로젝트 starter template을 모아 관리하는 **카탈로그**다. 특정 스택의 앱 개발 규칙은 루트가 아니라 각 `templates/{template}/` 안에 둔다.

## 저장소 역할

| 위치 | 역할 |
|------|------|
| `templates/{template}/` | 실행 가능한 프로젝트 starter (코드, AGENTS/CLAUDE, rules, skills) |
| `skills/` | 스택 무관 문서·명세·블로그 skill (Claude Code 프로젝트로 sync 시 `.claude/skills/fastddd/`) |
| `scripts/` | 템플릿 복사, 공통 skill 동기화 (Cursor/Claude/Codex 어댑터) |
| `.cursor/rules/` | **이 카탈로그 레포** Cursor 편집용 규칙 (이 문서와 내용 동일) |

## 이 카탈로그 레포 편집 규칙

- 이 저장소는 템플릿 카탈로그다. 앱 아키텍처 규칙은 `templates/{template}/` 내부에만 둔다.
- 편집 전에 루트 `AGENTS.md`/`CLAUDE.md`와 대상 템플릿의 `AGENTS.md`/`CLAUDE.md`를 읽는다.
- 스택별 개발 workflow skill은 `templates/{template}/.claude/skills/`(Claude) 또는 `templates/{template}/.cursor/skills/`(Cursor)에 둔다.
- 문서·명세·블로그용 공통 skill만 루트 `skills/`에 둔다.
- 새 프로젝트는 `scripts/create.sh`(또는 `scripts/new-from-template.sh`)로 템플릿을 복사해 시작한다.
- 존재하지 않는 모듈, 커맨드, 설정값을 임의로 만들지 않는다.

## 표준 구조

```text
FastDDD/
  AGENTS.md
  CLAUDE.md
  README.md
  skills/                    # write-api-spec, write-error-code-spec, ...
  scripts/
    create.sh
    new-from-template.sh
    sync-all.sh
    sync-shared-skills.sh
    sync-to-claude.sh
    sync-to-codex.sh
    sync-to-cursor.sh
    bootstrap.sh
  templates/
    ddd/
      AGENTS.md
      CLAUDE.md
      .cursor/rules/
      .cursor/skills/
      .claude/skills/
      app/
    mvc/                     # 추후 추가
```

## 무엇을 어디에 둘까

| 내용 | 위치 |
|------|------|
| DDD 개발 workflow (start-feature, start-refactoring, 코드 리뷰) | `templates/ddd/.claude/skills/`, `templates/ddd/.cursor/skills/` |
| DDD 아키텍처 규칙 | `templates/ddd/CLAUDE.md`, `templates/ddd/AGENTS.md`, `templates/ddd/.cursor/rules/` |
| bounded context, lifespan, router 추가 절차 | `templates/ddd/.claude/skills/`, `templates/ddd/.cursor/skills/` |
| API 명세, 에러코드 문서, 릴리즈 노트, 블로그 | 루트 `skills/` |
| MVC 전용 규칙·skill | `templates/mvc/` (추가 시) |

## 템플릿 추가 원칙

1. `templates/{name}/`에 자급자족 starter를 만든다.
2. 해당 템플릿 전용 `AGENTS.md` + `CLAUDE.md`와 `.cursor/`, `.claude/` 설정을 함께 작성한다.
3. 개발 workflow skill은 템플릿 내부에 둔다.
4. 루트 `skills/`에 스택 전제가 들어간 skill을 추가하지 않는다.

## 새 프로젝트 생성

```bash
./scripts/create.sh ddd /path/to/my-backend --with-shared-skills
```

`--with-shared-skills`는 루트 공통 skill을 Cursor(`.cursor/skills/`), Claude Code(`.claude/skills/fastddd/`), Codex(`.agents/skills/`)에 모두 동기화한다.

## 첫 번째 템플릿

`templates/ddd/` — FastAPI + DDD + Clean Architecture 백엔드. 개발 규칙은 `templates/ddd/CLAUDE.md`(Claude Code) 또는 `templates/ddd/AGENTS.md`(Cursor/Codex)를 따른다.
