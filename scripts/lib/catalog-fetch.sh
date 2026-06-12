#!/usr/bin/env bash

FASTDDD_DEFAULT_REPO="${FASTDDD_DEFAULT_REPO:-isak-kang/FastDDD}"
FASTDDD_DEFAULT_REF="${FASTDDD_DEFAULT_REF:-main}"

fastddd_resolve_local_root() {
  local script_path="${1:-}"

  if [[ -n "${FASTDDD_REPO_ROOT:-}" && -d "${FASTDDD_REPO_ROOT}/templates" ]]; then
    printf '%s\n' "$FASTDDD_REPO_ROOT"
    return 0
  fi

  if [[ -n "$script_path" && "$script_path" != "-" && -f "$script_path" ]]; then
    local root
    root="$(cd "$(dirname "$script_path")/.." && pwd)"
    if [[ -d "$root/templates" ]]; then
      printf '%s\n' "$root"
      return 0
    fi
  fi

  return 1
}

fastddd_archive_url() {
  local repo="$1"
  local ref="$2"

  if [[ "$ref" == refs/* ]]; then
    printf 'https://github.com/%s/archive/%s.tar.gz' "$repo" "$ref"
    return 0
  fi

  if [[ "$ref" == v* ]]; then
    printf 'https://github.com/%s/archive/refs/tags/%s.tar.gz' "$repo" "$ref"
    return 0
  fi

  printf 'https://github.com/%s/archive/refs/heads/%s.tar.gz' "$repo" "$ref"
}

fastddd_fetch_catalog() {
  local dest="$1"
  local repo="${2:-$FASTDDD_DEFAULT_REPO}"
  local ref="${3:-$FASTDDD_DEFAULT_REF}"
  local url extracted

  if ! command -v curl >/dev/null 2>&1; then
    echo "curl is required to fetch templates from GitHub." >&2
    return 1
  fi

  if ! command -v tar >/dev/null 2>&1; then
    echo "tar is required to extract the FastDDD catalog archive." >&2
    return 1
  fi

  url="$(fastddd_archive_url "$repo" "$ref")"
  mkdir -p "$dest"

  if ! curl -fsSL "$url" -o "$dest/archive.tar.gz"; then
    echo "Failed to download FastDDD catalog: $url" >&2
    return 1
  fi

  tar -xzf "$dest/archive.tar.gz" -C "$dest"
  rm -f "$dest/archive.tar.gz"

  extracted="$(find "$dest" -maxdepth 1 -mindepth 1 -type d | head -1)"
  if [[ -z "$extracted" || ! -d "$extracted/templates" ]]; then
    echo "Downloaded archive does not contain templates/: $url" >&2
    return 1
  fi

  printf '%s\n' "$extracted"
}
