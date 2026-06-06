# fastDDD

FastAPI + DDD 기반 백엔드 개발을 위한 AI 에이전트 스킬팩.

PRD 작성부터 기능 구현, 리팩토링, API 명세, 에러코드, 문서 배포까지 — 반복되는 개발 워크플로우를 스킬로 패키지화했다.

## 핵심 개념

- `skills/` 가 소스 오브 트루스다.
- `adapters/claude-code/` 는 Claude Code에 스킬을 설치하는 방법을 설명한다.
- `adapters/codex/` 는 Codex에 스킬을 설치하는 방법을 설명한다.
- `adapters/cursor/` 는 Cursor용 rule 파일을 제공한다.
- `examples/` 는 실제 백엔드 프로젝트에 스킬을 적용한 예시를 보여준다.

## 프로젝트에서 사용하는 방법

```text
your-project/
├── AGENTS.md
├── .claude/
│   ├── commands/
│   └── skills/
├── .agents/
│   └── skills/
└── .cursor/
    └── rules/
```

## 스킬 목록

| 스킬 | 목적 |
|------|------|
| `plan-feature` | 기능 구현 전 PRD 작성 |
| `implement-feature` | 승인된 PRD 기반으로 기능 구현 |
| `plan-refactoring` | 코드 변경 전 리팩토링 계획 수립 |
| `implement-refactoring` | 외부 동작을 유지하며 리팩토링 실행 |
| `review-code` | 요구사항·아키텍처·신뢰성·테스트 기준 코드 리뷰 |
| `write-api-spec` | API 명세 문서 생성 또는 업데이트 |
| `write-error-code-spec` | 에러코드 정의 문서 생성 또는 업데이트 |
| `review-docs` | API/에러/스펙 문서 일관성 검토 |
| `publish-docs` | Notion, Google Drive 등 외부 문서 시스템에 배포 준비 |

## 빠른 시작

### 설치 (Bootstrap)

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/isak-kang/fastddd/main/scripts/bootstrap.sh)"
```

### 수동 설치

```bash
# Claude Code
./scripts/sync-to-claude.sh /path/to/your-project

# Cursor
./scripts/sync-to-cursor.sh /path/to/your-project

# Codex
./scripts/sync-to-codex.sh /path/to/your-project

# 전체
./scripts/sync-all.sh /path/to/your-project
```

### 커맨드 호출 (Claude Code)

```bash
/fastddd:plan-feature    # PRD 작성
/fastddd:implement-feature  # 기능 구현
/fastddd:plan-refactoring   # 리팩토링 계획
/fastddd:write-api-spec     # API 명세 작성
```

## 원칙

`skills/` 를 먼저 수정한다. `.claude/skills`, `.agents/skills`, `.cursor/rules` 에 복사된 파일을 직접 수정하지 않는다. 프로젝트별 오버라이드가 필요한 경우에만 예외로 한다.
