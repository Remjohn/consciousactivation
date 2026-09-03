---
name: caebmad-application-investigate
description: Maps and audits deployable services, API servers, daemon workers, entrypoints, and runtime dependencies at Level 07.
version: 0.3.0-rebuild
agent: cae-application-analyst
---

# Skill: caebmad-application-investigate

## 1. Purpose & Invocation
The `caebmad-application-investigate` skill enables the `cae-application-analyst` to map deployable services, audit entrypoints, and verify runtime dependencies at `Level 07: APPLICATION`.

## 2. Invocation Preconditions
1. Service directories (`services/`, `apps/`) accessible.
2. `pyproject.toml` and package manifests available.
3. Schema `schemas/application_map.schema.json` loaded.

## 3. Execution Logic
1. **Service Discovery:** Locate all microservices and runtime packages under `services/` and `packages/`.
2. **Entrypoint & Handler Audit:** Identify concrete entrypoint files (`main.py`, `app.py`, `compiler.py`, `verifier.py`).
3. **Dependency Mapping:** Extract internal and external package dependencies.
4. **Status Verification:** Validate that entrypoints exist and assign `ACTIVE`, `STANDALONE`, `MIGRATING`, or `PLANNED`.
5. **Map Assembly:** Emit `docs/cae-bmad/07_brownfield/APPLICATION_MAP.json` and `.md`.

## 4. Output Contract
- `docs/cae-bmad/07_brownfield/APPLICATION_MAP.json`
- `docs/cae-bmad/07_brownfield/APPLICATION_MAP.md`
