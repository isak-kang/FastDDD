#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-.}"

echo "Syncing shared documentation skills to $TARGET ..."
"$REPO_ROOT/scripts/sync-all.sh" "$TARGET"

echo ""
echo "To start a new project from a template, use:"
echo "  ./scripts/new-from-template.sh ddd /path/to/my-backend --with-shared-skills"
