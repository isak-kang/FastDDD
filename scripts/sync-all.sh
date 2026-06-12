#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

"$REPO_ROOT/scripts/sync-to-claude.sh" "$TARGET"
"$REPO_ROOT/scripts/sync-to-codex.sh" "$TARGET"
"$REPO_ROOT/scripts/sync-to-cursor.sh" "$TARGET"
echo "All adapters synced to $TARGET"
