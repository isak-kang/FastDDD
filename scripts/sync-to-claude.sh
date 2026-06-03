#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "$TARGET/.claude/commands"
mkdir -p "$TARGET/.claude/skills"

for skill in "$REPO_ROOT"/skills/*; do
  [ -d "$skill" ] || continue
  name="$(basename "$skill")"

  # SKILL.md → .claude/commands/{name}.md (slash command으로 등록)
  cp "$skill/SKILL.md" "$TARGET/.claude/commands/$name.md"

  # 전체 스킬 폴더(템플릿 포함) → .claude/skills/{name} (참조용)
  rm -rf "$TARGET/.claude/skills/$name"
  cp -R "$skill" "$TARGET/.claude/skills/$name"

  echo "Synced Claude skill: $name"
done
