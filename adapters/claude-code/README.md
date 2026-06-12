# Claude Code 어댑터

## 새 프로젝트

```bash
./scripts/new-from-template.sh ddd /path/to/my-backend --with-shared-skills
```

## 공통 문서 skill 동기화

```bash
./scripts/sync-to-claude.sh /path/to/your-project
```

다음 경로로 복사된다:

```text
skills/{skill-name}/SKILL.md
→ .claude/commands/fastddd/{skill-name}.md

skills/{skill-name}/
→ .claude/skills/fastddd/{skill-name}/
```

개발 workflow skill(PRD, 구현, 리팩토링)은 템플릿 `.cursor/skills/`에 있으며, 템플릿 복사 시 함께 따라간다.
