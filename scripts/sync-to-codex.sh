#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "$TARGET/.agents/skills"

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
  rm -rf "$TARGET/.agents/skills/$name"
  cp -R "$skill" "$TARGET/.agents/skills/$name"
  echo "Synced shared skill: $name"
done
