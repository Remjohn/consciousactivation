#!/usr/bin/env bash
# AC-006: Docker Compose brings up a live server.
# Run from the repository root.
set -euo pipefail

COMPOSE_FILE="infra/docker/docker-compose.yml"
TIMEOUT_SECONDS=30
URL="http://localhost:8000/api/health"

echo "Building and starting the api service..."
docker compose -f "$COMPOSE_FILE" up --build -d api

cleanup() {
  echo "Tearing down..."
  docker compose -f "$COMPOSE_FILE" down
}
trap cleanup EXIT

echo "Polling ${URL} (timeout ${TIMEOUT_SECONDS}s)..."
elapsed=0
until curl --fail --silent --output /tmp/ca_health_response.json "$URL"; do
  elapsed=$((elapsed + 1))
  if [ "$elapsed" -ge "$TIMEOUT_SECONDS" ]; then
    echo "FAIL: ${URL} did not return 200 within ${TIMEOUT_SECONDS}s"
    docker compose -f "$COMPOSE_FILE" logs api
    exit 1
  fi
  sleep 1
done

echo "Response body:"
cat /tmp/ca_health_response.json
echo

status=$(python3 -c "import json,sys; print(json.load(open('/tmp/ca_health_response.json'))['status'])")
if [ "$status" != "ok" ]; then
  echo "FAIL: expected status \"ok\", got \"${status}\""
  exit 1
fi

echo "PASS: api container is up and /api/health reports status=ok"
