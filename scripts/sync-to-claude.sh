#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "$TARGET/.claude/commands/fastddd"
mkdir -p "$TARGET/.claude/skills/fastddd"

SHARED_SKILLS=(
  write-api-spec
  write-error-code-spec
  write-blog-post
  write-release-note
  review-docs
  publish-docs
)

for name in "${SHARED_SKILLS[@]}"; do
  skill="$REPO_ROOT/skills/$name"
  [ -d "$skill" ] || continue

  cp "$skill/SKILL.md" "$TARGET/.claude/commands/fastddd/$name.md"
  rm -rf "$TARGET/.claude/skills/fastddd/$name"
  cp -R "$skill" "$TARGET/.claude/skills/fastddd/$name"
  echo "Synced shared skill: $name"
done
