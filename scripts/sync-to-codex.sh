#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "$TARGET/.agents/skills"

for skill in "$REPO_ROOT"/skills/*; do
  [ -d "$skill" ] || continue
  name="$(basename "$skill")"
  rm -rf "$TARGET/.agents/skills/$name"
  cp -R "$skill" "$TARGET/.agents/skills/$name"
  echo "Synced Codex skill: $name"
done
