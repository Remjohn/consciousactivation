# CAE-BMAD Repository, Application, and Script/CLI Specification

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL SPECIFICATION  
**Authority:** CAE Rebuild Program / Operator Mandate M07  
**Scope:** Engineering standards, physical filesystem verification, deployable service mapping, and command-and-control inspection across Operating Levels 06, 07, and 08.

---

## 1. Operating Levels 06, 07, and 08 in the CAE Hierarchy

```text
Level 06: REPOSITORY        [Physical workspace, folder layout, manifests, cross-repo contracts]
         ↕
Level 07: APPLICATION       [Microservices, API servers, workers, runtimes, UI clients]
         ↕
Level 08: SCRIPT / CLI      [Automation harnesses, CLI entrypoints, migration scripts, dev tools]
```

### 1.1 Level 06: REPOSITORY (`cae-repository-analyst`)
- Audits the physical workspace directory structure against `WORKSPACE_MANIFEST.json` and `FOLDER_MAP.md`.
- Verifies cross-repository contracts under `governance/program-control/02_CROSS_REPO_CONTRACTS/`.
- Identifies orphaned, unmanaged, or temporary directories that require quarantine or cleanup.

### 1.2 Level 07: APPLICATION (`cae-application-analyst`)
- Catalogs deployable application services (`services/builder`, `services/delegation`, `services/vae`, `services/world-intelligence`, `services/pipeline`).
- Maps entrypoints, route handlers, daemon loops, and service dependencies.
- Enforces the **Reality Contact Rule**: No service may be marked active unless its entrypoint and core module imports resolve to working Python packages.

### 1.3 Level 08: SCRIPT / CLI (`cae-cli-script-analyst`)
- Catalogs automation toolchains, administrative CLI scripts (`scripts/cae/`, `tools/`), and migration scripts.
- Maps console script entrypoints declared in `pyproject.toml`.
- Validates syntax, argument parser semantics (`argparse`, `click`), and exit codes.

---

## 2. Crosswalk to Brownfield Code Surfaces

| Operating Level | Governed Artifact | Primary Physical Surfaces in Workspace |
|---|---|---|
| `Level 06: REPOSITORY` | `REPOSITORY_REALITY_MAP.md` | `WORKSPACE_MANIFEST.json`, `FOLDER_MAP.md`, `governance/` |
| `Level 07: APPLICATION` | `APPLICATION_MAP.md` | `services/*/src/`, `apps/`, `pyproject.toml` |
| `Level 08: SCRIPT / CLI` | `COMMAND_CONTROL_MAP.md` | `scripts/`, `tools/`, `packages/ca_runtime/` |

---

## 3. False-Proof and Falsification Rules

1. **Physical Existence Invariant:** Listing a directory or service in documentation without verifying its path on disk fails validation (`FALSE_PROOF`).
2. **Import Integrity Invariant:** Application services must have resolvable entrypoints (e.g., `main.py`, `app.py`, or FastAPI / CLI handles).
3. **Executable Script Invariant:** Script entries must declare valid runtime engines (`PYTHON`, `BASH`, `POWERSHELL`, `NODE`) and verifiable file paths.
