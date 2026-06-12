# Codex 어댑터

## 새 프로젝트

```bash
curl -fsSL https://raw.githubusercontent.com/isak-kang/FastDDD/main/scripts/create.sh \
  | bash -s -- ddd ./my-backend --with-shared-skills
```

프로젝트의 `AGENTS.md`와 템플릿 `.cursor/` 설정을 기준으로 작업한다.

## 공통 문서 skill 동기화

```bash
./scripts/sync-to-codex.sh /path/to/your-project
```

```text
skills/{skill-name}/
→ .agents/skills/{skill-name}/
```
