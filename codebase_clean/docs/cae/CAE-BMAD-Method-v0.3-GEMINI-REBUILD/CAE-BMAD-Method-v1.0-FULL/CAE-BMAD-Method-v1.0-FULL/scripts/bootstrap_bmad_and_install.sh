#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${1:-https://github.com/Remjohn/BMAD-METHOD.git}"
TARGET="${2:-./BMAD-METHOD}"

if [[ -e "$TARGET/.git" ]]; then
  echo "Using existing repository: $TARGET"
else
  git clone "$REPO_URL" "$TARGET"
fi

"$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/scripts/install_into_bmad.sh" "$TARGET"
