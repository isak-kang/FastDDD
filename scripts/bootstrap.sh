#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]:-}"

load_fastddd_lib() {
  local script_path="$1"
  local lib_path
  local repo="isak-kang/FastDDD"
  local ref="${FASTDDD_LIB_REF:-main}"

  if [[ -n "$script_path" && "$script_path" != "-" && -f "$script_path" ]]; then
    lib_path="$(cd "$(dirname "$script_path")" && pwd)/lib/catalog-fetch.sh"
    if [[ -f "$lib_path" ]]; then
      # shellcheck source=lib/catalog-fetch.sh
      source "$lib_path"
      return 0
    fi
  fi

  if ! command -v curl >/dev/null 2>&1; then
    echo "curl is required to load FastDDD helper scripts." >&2
    exit 1
  fi

  local tmp_lib
  tmp_lib="$(mktemp)"
  curl -fsSL "https://raw.githubusercontent.com/${repo}/${ref}/scripts/lib/catalog-fetch.sh" -o "$tmp_lib"
  # shellcheck source=/dev/null
  source "$tmp_lib"
  rm -f "$tmp_lib"
}

load_fastddd_lib "$SCRIPT_PATH"

usage() {
  cat <<EOF
Usage:
  ./scripts/bootstrap.sh [target-dir]
  curl -fsSL https://raw.githubusercontent.com/isak-kang/FastDDD/main/scripts/bootstrap.sh | bash -s -- [target-dir]

Syncs shared documentation skills into an existing project (Cursor, Claude Code, Codex).

To create a new project from a template, use create.sh instead:
  curl -fsSL https://raw.githubusercontent.com/isak-kang/FastDDD/main/scripts/create.sh | bash -s -- ddd ./my-backend --with-shared-skills
EOF
}

TARGET="${1:-.}"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

sync_from_local() {
  local repo_root="$1"
  echo "Syncing shared documentation skills to $TARGET ..."
  "$repo_root/scripts/sync-all.sh" "$TARGET"
}

sync_from_remote() {
  local tmpdir catalog_root
  tmpdir="$(mktemp -d)"
  trap 'rm -rf "$tmpdir"' EXIT

  echo "Fetching FastDDD catalog (${FASTDDD_DEFAULT_REPO}@${FASTDDD_DEFAULT_REF}) ..."
  catalog_root="$(fastddd_fetch_catalog "$tmpdir")"
  echo "Syncing shared documentation skills to $TARGET ..."
  "$catalog_root/scripts/sync-all.sh" "$TARGET"
}

if local_root="$(fastddd_resolve_local_root "$SCRIPT_PATH")"; then
  sync_from_local "$local_root"
else
  sync_from_remote
fi

echo ""
echo "For a new project, use create.sh:"
echo "  curl -fsSL https://raw.githubusercontent.com/isak-kang/FastDDD/main/scripts/create.sh | bash -s -- ddd ./my-backend --with-shared-skills"
