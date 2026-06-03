# Cursor 어댑터

Cursor는 `.cursor/rules/*.mdc` 에서 영구적인 프로젝트 규칙을 사용한다.

## 프로젝트 레벨 설치

레포지토리 루트에서 실행:

```bash
./scripts/sync-to-cursor.sh /path/to/your-project
```

다음과 같이 복사된다:

```text
cursor-rules/*.mdc
→ /path/to/your-project/.cursor/rules/*.mdc
```

## 권장 프로젝트 파일 구조

```text
your-project/
├── AGENTS.md
└── .cursor/
    └── rules/
```

## 참고

- 영구적인 프로젝트 규칙은 `.cursor/rules/*.mdc` 를 사용한다.
- 워크플로우 전용 프롬프트는 `skills/` 를 소스 자료로 활용한다.
- Cursor 규칙은 구체적이고 파일 패턴을 인식해야 한다.
