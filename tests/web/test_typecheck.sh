#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo "$(dirname "$0")/../..")"

npm run typecheck --workspace=apps/web
echo "OK"
