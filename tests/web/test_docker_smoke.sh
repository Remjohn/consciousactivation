#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo "$(dirname "$0")/../..")"

docker compose -f infra/docker/docker-compose.yml up --build -d web
trap "docker compose -f infra/docker/docker-compose.yml down" EXIT
for i in $(seq 1 15); do
  if curl -sf http://localhost:3000/ | grep -q '<div id="root">'; then
    echo "OK"
    exit 0
  fi
  sleep 2
done
echo "web container did not become ready" >&2
exit 1
