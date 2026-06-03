#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "$TARGET/.cursor/rules"

for rule in "$REPO_ROOT"/cursor-rules/*.mdc; do
  [ -f "$rule" ] || continue
  cp "$rule" "$TARGET/.cursor/rules/$(basename "$rule")"
  echo "Synced Cursor rule: $(basename "$rule")"
done
