# Codex 어댑터

Codex는 `AGENTS.md` 에서 레포지토리 지침을 읽고, `.agents/skills/{skill-name}/SKILL.md` 에서 스킬을 사용할 수 있다.

## 프로젝트 레벨 설치

레포지토리 루트에서 실행:

```bash
./scripts/sync-to-codex.sh /path/to/your-project
```

다음과 같이 복사된다:

```text
skills/{skill-name}/
→ /path/to/your-project/.agents/skills/{skill-name}/
```

## 권장 프로젝트 파일 구조

```text
your-project/
├── AGENTS.md
└── .agents/
    └── skills/
```

## 참고

- `SKILL.md` 파일에 포함된 `name`, `description` 프론트매터는 Codex 호환성을 위한 것이다.
- 프로젝트 아키텍처와 코딩 규칙은 `AGENTS.md` 에 유지한다.
