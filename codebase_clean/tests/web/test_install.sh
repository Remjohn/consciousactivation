#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo "$(dirname "$0")/../..")"

npm install
test -d apps/web/node_modules
test -f package-lock.json
grep -q '"react"' package-lock.json
echo "OK"
