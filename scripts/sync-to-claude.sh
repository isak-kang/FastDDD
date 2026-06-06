#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "$TARGET/.claude/commands/fastddd"
mkdir -p "$TARGET/.claude/skills/fastddd"

for skill in "$REPO_ROOT"/skills/*; do
  [ -d "$skill" ] || continue
  name="$(basename "$skill")"

  # SKILL.md → .claude/commands/fastddd/{name}.md (/fastddd:{name} 커맨드로 등록)
  cp "$skill/SKILL.md" "$TARGET/.claude/commands/fastddd/$name.md"

  # 전체 스킬 폴더(템플릿 포함) → .claude/skills/fastddd/{name} (참조용)
  rm -rf "$TARGET/.claude/skills/fastddd/$name"
  cp -R "$skill" "$TARGET/.claude/skills/fastddd/$name"

  echo "Synced fastddd skill: $name"
done
