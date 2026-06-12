#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SHARED_SKILLS=(
  write-api-spec
  write-error-code-spec
  write-blog-post
  write-release-note
  review-docs
  publish-docs
)

mkdir -p "$TARGET/.cursor/skills"

for name in "${SHARED_SKILLS[@]}"; do
  src="$REPO_ROOT/skills/$name"
  if [[ ! -d "$src" ]]; then
    echo "Missing shared skill: $src" >&2
    exit 1
  fi
  rm -rf "$TARGET/.cursor/skills/$name"
  cp -R "$src" "$TARGET/.cursor/skills/$name"
  echo "Synced shared skill: $name"
done
