# FastDDD

FastDDD는 **실행 가능한 프로젝트 템플릿 카탈로그**다. 스택·아키텍처별 starter kit은 `templates/`에 두고, 문서·명세 작성용 공통 skill만 루트 `skills/`에서 관리한다.

## 구조

```text
FastDDD/
  AGENTS.md                  # 카탈로그 운영 규칙 (Cursor/Codex)
  CLAUDE.md                  # 카탈로그 운영 규칙 (Claude Code)
  skills/                    # 스택 무관 문서·명세 skill
  scripts/
    create.sh                # 새 프로젝트 생성 (curl 지원)
    new-from-template.sh     # 로컬 카탈로그에서 템플릿 복사
    sync-all.sh              # 공통 skill을 Cursor+Claude+Codex에 모두 동기화
    sync-shared-skills.sh    # 공통 skill을 Cursor에 복사
    sync-to-claude.sh        # 공통 skill을 Claude Code에 복사
    sync-to-codex.sh         # 공통 skill을 Codex에 복사
    bootstrap.sh             # 기존 프로젝트에 공통 skill 동기화
  templates/
    ddd/                     # FastAPI + DDD 백엔드 (자급자족)
      AGENTS.md
      CLAUDE.md
      .cursor/rules/
      .cursor/skills/
      .claude/skills/
      app/
```

## 템플릿

| 템플릿 | 목적 |
|------|------|
| `templates/ddd` | FastAPI + DDD + Clean Architecture 백엔드 |

## 루트 공통 skill (문서·명세)

| 스킬 | 목적 |
|------|------|
| `write-api-spec` | API 명세 문서 작성 |
| `write-error-code-spec` | 에러코드 정의 문서 작성 |
| `write-blog-post` | 기술 블로그 글 작성 |
| `write-release-note` | 릴리즈 노트 작성 |
| `review-docs` | 문서 일관성 검토 |
| `publish-docs` | 외부 문서 배포 준비 |

개발 workflow skill(기능 착수, 리팩토링 착수, 코드 리뷰)은 **템플릿 내부**에 둔다. 예: `templates/ddd/.cursor/skills/start-feature`.

## 새 프로젝트 시작

레포 clone 없이 (권장):

```bash
curl -fsSL https://raw.githubusercontent.com/isak-kang/FastDDD/main/scripts/create.sh \
  | bash -s -- ddd ./my-backend --with-shared-skills

cd my-backend
cp .env.example .env
uv pip install -e ".[dev]"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pytest
```

카탈로그 레포를 이미 clone한 경우:

```bash
./scripts/create.sh ddd ../my-backend --with-shared-skills
# 또는
./scripts/new-from-template.sh ddd ../my-backend --with-shared-skills
```

복사된 프로젝트의 `CLAUDE.md`(Claude Code) 또는 `AGENTS.md` + `.cursor/rules/`(Cursor/Codex), 그리고 `.claude/skills/` / `.cursor/skills/`가 실제 개발 규칙이다.

`--with-shared-skills`는 API 명세·에러코드 문서 등 **루트 공통 skill**을 프로젝트의 `.cursor/skills/`, `.claude/skills/fastddd/`, `.agents/skills/`에 모두 복사한다. 생략해도 템플릿만으로 개발은 가능하다.

특정 브랜치·태그에서 생성하려면 `--ref`를 붙인다:

```bash
curl -fsSL https://raw.githubusercontent.com/isak-kang/FastDDD/main/scripts/create.sh \
  | bash -s -- ddd ./my-backend --with-shared-skills --ref dev
```

## 기존 프로젝트에 공통 skill만 추가

```bash
curl -fsSL https://raw.githubusercontent.com/isak-kang/FastDDD/main/scripts/bootstrap.sh \
  | bash -s -- /path/to/your-project
```

카탈로그 레포 안에서:

```bash
./scripts/bootstrap.sh /path/to/your-project
# Cursor skill만 필요하면
./scripts/sync-shared-skills.sh /path/to/your-project
# Claude Code skill만 필요하면
./scripts/sync-to-claude.sh /path/to/your-project
```

Claude Code / Codex용 동기화는 `bootstrap.sh`(내부적으로 `sync-all.sh`)가 함께 처리한다 (로컬·curl 모두).

## 원칙

- 루트 = 템플릿 카탈로그 + 스택 무관 문서 skill
- 템플릿 = 코드 + 아키텍처 규칙 + 개발 workflow skill
- MVC 등 새 템플릿은 `templates/{name}/`에 독립적으로 추가한다
