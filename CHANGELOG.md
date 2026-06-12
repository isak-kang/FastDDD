# Changelog

## Unreleased

- Added `scripts/create.sh` for curl-based project creation from GitHub
- Added `scripts/lib/catalog-fetch.sh` for remote catalog downloads
- Updated `bootstrap.sh` to sync skills into existing projects via curl or local repo

## 0.1.0

- Initial repository scaffold
- Reorganized repo as template catalog: dev workflow skills moved to `templates/ddd/.cursor/skills/`
- Added `scripts/new-from-template.sh` and `scripts/sync-shared-skills.sh`
- Root `skills/` now holds stack-agnostic documentation skills only
- Removed root `cursor-rules/` and legacy `agents/*.template.md`
- Added core skills
- Added Claude Code, Codex, and Cursor adapters
- Added sync scripts
