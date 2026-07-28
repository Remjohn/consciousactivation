#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo "$(dirname "$0")/../..")"

npm run build --workspace=apps/web
npm run preview --workspace=apps/web &
PREVIEW_PID=$!
trap "kill $PREVIEW_PID" EXIT
for i in $(seq 1 15); do
  if curl -sf http://localhost:4173/ > /dev/null; then
    echo "OK"
    exit 0
  fi
  sleep 2
done
echo "preview server did not become ready" >&2
exit 1
