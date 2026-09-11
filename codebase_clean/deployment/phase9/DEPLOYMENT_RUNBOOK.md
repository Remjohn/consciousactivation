# Phase 9 Deployment Runbook

This is a development reference topology, not production authorization.

1. Verify all Phase 1–9 tests and the release manifest.
2. Copy `env.example` to a local untracked environment file.
3. Run `docker compose -f deployment/phase9/docker-compose.local.yml config`.
4. Build and start the local services only when Docker is available.
5. Confirm each product reports `production_authorized: false` and `certified: false`.
6. Use `ca-release pilot` to execute the local reference campaign.
7. Run the backup and restore rehearsal before retaining any development state.

The cloud profile remains an operator-supplied template and was not executed by Phase 9.
