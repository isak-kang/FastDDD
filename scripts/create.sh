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
  ./scripts/create.sh <template> <target-dir> [options]
  curl -fsSL https://raw.githubusercontent.com/isak-kang/FastDDD/main/scripts/create.sh | bash -s -- <template> <target-dir> [options]

Options:
  --with-shared-skills   Copy stack-agnostic documentation skills into the project
                          (Cursor, Claude Code, and Codex adapters)
  --ref <branch|tag>       Catalog git ref (default: ${FASTDDD_DEFAULT_REF})
  --repo <owner/name>      Catalog repository (default: ${FASTDDD_DEFAULT_REPO})
  -h, --help               Show this help

Examples:
  ./scripts/create.sh ddd ./my-backend --with-shared-skills
  curl -fsSL https://raw.githubusercontent.com/isak-kang/FastDDD/main/scripts/create.sh | bash -s -- ddd ./my-backend --with-shared-skills
EOF
}

TEMPLATE=""
TARGET=""
WITH_SHARED_SKILLS=false
REF="$FASTDDD_DEFAULT_REF"
REPO="$FASTDDD_DEFAULT_REPO"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-shared-skills)
      WITH_SHARED_SKILLS=true
      shift
      ;;
    --ref)
      REF="${2:-}"
      if [[ -z "$REF" ]]; then
        echo "--ref requires a value." >&2
        exit 1
      fi
      shift 2
      ;;
    --repo)
      REPO="${2:-}"
      if [[ -z "$REPO" ]]; then
        echo "--repo requires a value." >&2
        exit 1
      fi
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
    *)
      if [[ -z "$TEMPLATE" ]]; then
        TEMPLATE="$1"
      elif [[ -z "$TARGET" ]]; then
        TARGET="$1"
      else
        echo "Unexpected argument: $1" >&2
        usage
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ -z "$TEMPLATE" || -z "$TARGET" ]]; then
  usage
  exit 1
fi

if [[ -e "$TARGET" ]]; then
  echo "Target already exists: $TARGET" >&2
  exit 1
fi

create_from_local() {
  local repo_root="$1"
  local args=("$TEMPLATE" "$TARGET")

  if $WITH_SHARED_SKILLS; then
    args+=(--with-shared-skills)
  fi

  bash "$repo_root/scripts/new-from-template.sh" "${args[@]}"
  print_next_steps
  exit 0
}

create_from_remote() {
  local tmpdir catalog_root template_dir
  tmpdir="$(mktemp -d)"
  trap 'rm -rf "$tmpdir"' EXIT

  echo "Fetching template '$TEMPLATE' from ${REPO}@${REF} ..."
  catalog_root="$(fastddd_fetch_catalog "$tmpdir" "$REPO" "$REF")"
  template_dir="$catalog_root/templates/$TEMPLATE"

  if [[ ! -d "$template_dir" ]]; then
    echo "Template not found: templates/$TEMPLATE (repo: $REPO, ref: $REF)" >&2
    exit 1
  fi

  mkdir -p "$(dirname "$TARGET")"
  cp -R "$template_dir" "$TARGET"
  echo "Created project from template '$TEMPLATE' at $TARGET"

  if $WITH_SHARED_SKILLS; then
    "$catalog_root/scripts/sync-all.sh" "$TARGET"
  fi
}

print_next_steps() {
  cat <<EOF

Next steps:
  cd $TARGET
  cp .env.example .env
  uv pip install -e ".[dev]"
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  pytest
EOF
}

if local_root="$(fastddd_resolve_local_root "$SCRIPT_PATH")"; then
  create_from_local "$local_root"
fi

create_from_remote
print_next_steps
