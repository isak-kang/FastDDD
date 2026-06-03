# Claude Code 어댑터

## 프로젝트 레벨 설치

레포지토리 루트에서 실행:

```bash
./scripts/sync-to-claude.sh /path/to/your-project
```

다음과 같이 복사된다:

```text
skills/{skill-name}/SKILL.md
→ /path/to/your-project/.claude/commands/{skill-name}.md

skills/{skill-name}/
→ /path/to/your-project/.claude/skills/{skill-name}/
```

## 권장 프로젝트 파일 구조

```text
your-project/
├── AGENTS.md
├── CLAUDE.md
└── .claude/
    ├── commands/
    └── skills/
```

## 참고

- 공통 워크플로우는 `skills/` 에서 관리한다.
- Claude Code 전용 프로젝트 가이드는 `CLAUDE.md` 에 작성한다.
- 여러 도구가 공유하는 규칙은 `AGENTS.md` 에 작성한다.
