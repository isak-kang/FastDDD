#!/usr/bin/env bash
set -euo pipefail

REPO="https://github.com/isak-kang/fastddd"
INSTALL_DIR="${FASTDDD_DIR:-$HOME/.fastddd}"
TARGET="${1:-.}"

echo "fastDDD 설치를 시작합니다..."

# 레포 클론 또는 업데이트
if [ -d "$INSTALL_DIR/.git" ]; then
  echo "기존 설치 업데이트 중..."
  git -C "$INSTALL_DIR" pull --ff-only
else
  echo "fastDDD 다운로드 중..."
  git clone --depth=1 "$REPO" "$INSTALL_DIR"
fi

# 각 어댑터 동기화
"$INSTALL_DIR/scripts/sync-all.sh" "$TARGET"

echo ""
echo "fastDDD 설치 완료!"
echo ""
echo "Claude Code에서 아래 커맨드를 사용할 수 있습니다:"
echo "  /fastddd:plan-feature"
echo "  /fastddd:implement-feature"
echo "  /fastddd:plan-refactoring"
echo "  /fastddd:write-api-spec"
echo ""
echo "에이전트 세션을 재시작하여 커맨드를 불러오세요."
