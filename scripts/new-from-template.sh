#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/new-from-template.sh <template> <target-dir> [--with-shared-skills]

Examples:
  ./scripts/new-from-template.sh ddd ../my-backend
  ./scripts/new-from-template.sh ddd ../my-backend --with-shared-skills

Copies templates/<template>/ to <target-dir>.
Use --with-shared-skills to also copy stack-agnostic doc skills from the catalog root
into Cursor, Claude Code, and Codex adapters.
EOF
}

TEMPLATE=""
TARGET=""
WITH_SHARED_SKILLS=false

for arg in "$@"; do
  case "$arg" in
    --with-shared-skills)
      WITH_SHARED_SKILLS=true
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [[ -z "$TEMPLATE" ]]; then
        TEMPLATE="$arg"
      elif [[ -z "$TARGET" ]]; then
        TARGET="$arg"
      else
        echo "Unknown argument: $arg" >&2
        usage
        exit 1
      fi
      ;;
  esac
done

if [[ -z "$TEMPLATE" || -z "$TARGET" ]]; then
  usage
  exit 1
fi

TEMPLATE_DIR="$REPO_ROOT/templates/$TEMPLATE"
if [[ ! -d "$TEMPLATE_DIR" ]]; then
  echo "Template not found: $TEMPLATE_DIR" >&2
  exit 1
fi

if [[ -e "$TARGET" ]]; then
  echo "Target already exists: $TARGET" >&2
  exit 1
fi

mkdir -p "$(dirname "$TARGET")"
cp -R "$TEMPLATE_DIR" "$TARGET"
echo "Created project from template '$TEMPLATE' at $TARGET"

if $WITH_SHARED_SKILLS; then
  "$REPO_ROOT/scripts/sync-all.sh" "$TARGET"
fi
