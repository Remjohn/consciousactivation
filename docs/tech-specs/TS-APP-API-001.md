---
spec_id: TS-APP-API-001
title: FastAPI Gateway Bootstrap
document_class: TECH_SPEC
product: Conscious Activations
module: api
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CURRENT
build_authority: false
controlling_frs:
  - FR-APP-001 (workspace)
  - FR-APP-050 (campaign order)
  - FR-APP-060 (control tower)
  - all FR-APP-* (gateway is the HTTP entry point for every module)
controlling_stories:
  - ST-APP-06.01 (harness library — first story that needs a running server)
  - ST-APP-07.01 (create campaign)
  - ST-APP-08.01 (control tower)
upstream_dependencies:
  - CA_PROJECT_SNAPSHOT_V2.md (authority — CURRENT)
  - CA_APP_FR_EPIC_SPEC_PLAN.md (authority — CURRENT)
downstream_consumers:
  - TS-APP-API-002 (harness library API)
  - TS-APP-API-003 (interview admission API)
  - TS-APP-API-004 (campaign CRUD)
  - TS-APP-API-005 (pipeline WebSocket)
  - TS-APP-API-006 (supervision + ship)
  - TS-APP-UI-001 (React scaffold — cannot start until this server runs)
output_path: api/main.py (and supporting files listed in section 7)
wave: 1
---

# TS-APP-API-001 — FastAPI Gateway Bootstrap

## 1. Files and Authorities Read

| File | SHA-256 | Status | Fact extracted |
|---|---|---|---|
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/application.py` | `a32b6cea` | READ — CURRENT IMPLEMENTATION | `PipelineApplication.__init__` accepts `database_path: str \| Path \| None`; `.status()` returns dict with `production_authorized: False` |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/application.py` | `02784b27` | READ — CURRENT IMPLEMENTATION | `AirApplication.__init__` accepts `database_path`; `.status()` returns `external_model_calls: 0` confirming no live inference |
| `02_VISUAL_ASSET_EDITOR/src/cmf_vae/application.py` | `e646e0e5` | READ — CURRENT IMPLEMENTATION | `VAEApplication.__init__` requires `database_path`, `storage_root`, `delegation_root` — three separate paths, not one |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/application.py` | `25bd47f5` | READ — CURRENT IMPLEMENTATION | `InterviewExpressionApplication` exposes `.source_packages`, `.transcripts`, `.expression`, `.live` as service handles |
| `packages/ca_contracts/src/ca_contracts/__init__.py` | `710e7869` | READ — CURRENT IMPLEMENTATION | Exposes `canonical_sha256`, `utc_now_rfc3339`, `validate_payload` |
| `packages/ca_runtime/src/ca_runtime/database.py` | `abdf2727` | READ — CURRENT IMPLEMENTATION | `ProductHealth.to_dict()` is the canonical health response shape used by all services |
| `deployment/phase9/docker-compose.local.yml` | READ | READ — CURRENT | Each service uses `CA_DATA_ROOT` env var; all share a single `ca-state` volume |
| `05_ATOMIC_HARNESS_PIPELINE/pyproject.toml` | READ | READ — CURRENT | Package name is `cmf-atomic-harness-pipeline`, CLI entry is `cmf-pipeline` |

**Source gap notice:** `01_ATOMIC_HARNESS_BUILDER` has no `application.py` — it uses a `BuilderProductizationService` under `application/productization_service.py`. The health route for the Builder must call that service directly. This does not block writing.

---

## 2. Problem, User Outcome, Solution, and Scope

### Problem without this spec
Every Python module — AIR, Pipeline, Interview Expression, VAE, Builder — exposes only a CLI entrypoint. Nothing can be called over HTTP. The React frontend has no server to connect to. The Pi Coding Agent has no endpoint to POST a Harness definition. No integration test can exercise the live system. The product exists entirely as command-line tools.

### User outcome
A developer can run `docker compose up` and immediately hit `GET /api/health` to see the live status of every service. A React component can call `GET /api/campaigns` and receive data. The Pi Coding Agent can call `POST /api/harnesses/build`. Every subsequent spec in Wave 2 and Wave 3 has a running server to test against.

### Solution
A FastAPI application at `api/main.py` that:
- instantiates all six service application objects against a shared `CA_DATA_ROOT`
- exposes `/api/health` returning real status from every service
- exposes `/api/health/{service}` returning per-service status
- registers routers for every Wave 2 module via `include_router`
- handles CORS, error contracts, and startup/shutdown lifecycle
- provides typed `Depends()` factories so every router receives pre-initialised application objects

### In scope
- `api/main.py` — FastAPI app creation, lifespan, CORS, router registration
- `api/dependencies.py` — `Depends()` factories for all six application objects
- `api/routers/health.py` — `GET /api/health`, `GET /api/health/{service}`
- `api/errors.py` — typed error response model, exception handlers
- `api/config.py` — environment variable loading (`CA_DATA_ROOT`, `CA_MEDIA_ROOT`, `CA_DELEGATION_ROOT`)
- `infra/docker/dockerfile.api` — replaces `deployment/phase9/Dockerfile.python`
- `infra/docker/docker-compose.yml` — replaces `deployment/phase9/docker-compose.local.yml` with long-running services

### Out of scope
- Any route beyond `/api/health` and `/api/health/{service}` (covered in TS-APP-API-002 through TS-APP-API-006)
- Authentication (covered separately after MVP routes work)
- WebSocket (TS-APP-API-005)
- React frontend (TS-APP-UI-001)
- Database migrations (each application object calls `.initialize()` on startup — already implemented)
- Any modification to existing Python service packages

---

## 3. Governing Decisions and Constraints

**Service application objects are singletons.** Each application class (`PipelineApplication`, `AirApplication`, etc.) holds open SQLite connections and in-memory registries. They must be instantiated once at server startup and shared via FastAPI's dependency injection — never re-instantiated per request.

**`CA_DATA_ROOT` is the single shared state root.** All six services write SQLite databases under this directory. The existing docker-compose already establishes this convention. The FastAPI app inherits it exactly.

**VAE requires three separate paths.** `VAEApplication.__init__` takes `database_path`, `storage_root`, and `delegation_root` separately, unlike the other services which take only `database_path`. The dependency factory must read all three from environment variables.

**`.status()` and `.initialize()` contracts must not be modified.** These methods are defined by the existing service packages. The gateway calls them; it does not redefine their shape.

**Error responses must be typed and machine-readable.** Every error — service unavailable, validation failure, unknown route — returns a JSON body matching `ErrorResponse`. No HTML error pages.

**No float in canonical responses.** Following `ca_contracts` conventions, no floating-point values appear in API responses. Timestamps are RFC 3339 strings. Counts are integers.

**Claim ceiling:** `GATEWAY_BOOTSTRAP_DEVELOPMENT_EVIDENCE`. The gateway does not claim production readiness, authentication completeness, or certified operation.

---

## 4. Current Brownfield Architecture

| Component | Path | Actual behaviour | Disposition | Reason |
|---|---|---|---|---|
| `docker-compose.local.yml` | `deployment/phase9/docker-compose.local.yml` | Runs each service as a one-shot CLI command (`cmf-pipeline status --json`) and exits | REPLACE | One-shot commands are not long-running servers; replaced by `infra/docker/docker-compose.yml` with `uvicorn` |
| `Dockerfile.python` | `deployment/phase9/Dockerfile.python` | Installs all six Python packages + ffmpeg; sets `CA_DATA_ROOT` | ADAPT | Copy to `infra/docker/dockerfile.api`; add `fastapi`, `uvicorn[standard]`, `python-multipart` to install list |
| `Dockerfile.studio` | `deployment/phase9/Dockerfile.studio` | Node build of Studio TypeScript | REUSE | Copy to `infra/docker/dockerfile.studio`; unchanged |
| `PipelineApplication` | `services/pipeline/src/cmf_pipeline/application.py` | Full pipeline runtime; `.status()` returns authoritative dict | REUSE | Called by dependency factory; not modified |
| `AirApplication` | `services/air/src/cmf_activative_intelligence/application.py` | Full AIR runtime; `.status()` returns authoritative dict | REUSE | Called by dependency factory; not modified |
| `VAEApplication` | `services/vae/src/cmf_vae/application.py` | Full VAE runtime; needs three path args | REUSE | Called by dependency factory; not modified |
| `InterviewExpressionApplication` | `services/interview/src/conscious_activations_interview_expression/application.py` | Full interview runtime | REUSE | Called by dependency factory; not modified |
| `BuilderProductizationService` | `services/builder/src/cmf_builder/application/productization_service.py` | Builder runtime | REUSE | Called by dependency factory; not modified |
| `ca_contracts` | `packages/ca_contracts/` | Canonical JSON + SHA-256 | REUSE | Imported by gateway for response hashing |
| `ca_runtime.database.ProductHealth` | `packages/ca_runtime/` | Health dict shape | REUSE | Gateway serialises `.to_dict()` output directly |

---

## 5. Proposed Architecture and Workflows

### Application object lifecycle

```
Server startup (lifespan)
  ├── Load config (CA_DATA_ROOT, CA_MEDIA_ROOT, CA_DELEGATION_ROOT)
  ├── Instantiate PipelineApplication(database_path)   → .initialize()
  ├── Instantiate AirApplication(database_path)        → .initialize() → .load_registries()
  ├── Instantiate VAEApplication(db, storage, delegation) → .initialize()
  ├── Instantiate InterviewExpressionApplication(db)   → .initialize()
  ├── Instantiate BuilderProductizationService(db)
  └── Store all in app.state

Request handling
  └── Router calls Depends(get_pipeline) → returns app.state.pipeline
                   Depends(get_air)      → returns app.state.air
                   etc.

Server shutdown (lifespan)
  └── Each application object closes its SQLite connections
```

### Health route behaviour

`GET /api/health`
- Calls `.status()` on each service application object
- Assembles aggregate response
- Returns HTTP 200 if all services return `integrity: ok`
- Returns HTTP 503 if any service status call raises or returns `integrity` != `ok`

`GET /api/health/{service}`
- Valid service names: `pipeline`, `air`, `vae`, `interview`, `builder`, `all`
- Returns single-service status dict
- Returns HTTP 404 for unknown service name

### Error contract

Every non-2xx response body:
```json
{
  "error_code": "SERVICE_UNAVAILABLE",
  "message": "pipeline service failed to initialize",
  "service": "pipeline",
  "timestamp": "2026-07-25T10:00:00Z"
}
```

`error_code` values for this spec: `SERVICE_UNAVAILABLE`, `NOT_FOUND`, `INTERNAL_ERROR`.

### CORS policy (development)
```python
allow_origins=["http://localhost:3000", "http://localhost:5173"]
allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
allow_headers=["*"]
allow_credentials=False
```
Production CORS policy is out of scope for this spec.

---

## 6. Data Models, Contracts, Schemas, and APIs

### `ServiceHealthItem`
```python
class ServiceHealthItem(BaseModel):
    service: str                    # "pipeline" | "air" | "vae" | "interview" | "builder"
    product_id: str                 # from ProductHealth.product_id
    product_version: str            # semver string
    authority_state: str            # e.g. "phase_09_development_release_candidate"
    database_path: str              # absolute path to SQLite file
    integrity: str                  # "ok" | "error"
    command_count: int
    event_count: int
    receipt_count: int
    production_authorized: bool     # always False at this stage
    certified: bool                 # always False at this stage
    claim_ceiling: str
```

### `HealthResponse`
```python
class HealthResponse(BaseModel):
    status: str                     # "ok" | "degraded" | "error"
    timestamp: str                  # RFC 3339
    gateway_version: str            # "0.1.0"
    ca_data_root: str               # resolved absolute path
    services: dict[str, ServiceHealthItem]
```

### `ErrorResponse`
```python
class ErrorResponse(BaseModel):
    error_code: str
    message: str
    service: str | None = None
    timestamp: str                  # RFC 3339
```

### Endpoints defined in this spec

| Method | Path | Response | Error codes |
|---|---|---|---|
| `GET` | `/api/health` | `HealthResponse` (200 or 503) | `SERVICE_UNAVAILABLE` |
| `GET` | `/api/health/{service}` | `ServiceHealthItem` (200) | `NOT_FOUND`, `SERVICE_UNAVAILABLE` |

Positive example — `GET /api/health` when all services healthy:
```json
{
  "status": "ok",
  "timestamp": "2026-07-25T10:00:00Z",
  "gateway_version": "0.1.0",
  "ca_data_root": "/state",
  "services": {
    "pipeline": {
      "service": "pipeline",
      "product_id": "cmf-atomic-harness-pipeline",
      "product_version": "0.9.0.dev1",
      "authority_state": "phase_09_development_release_candidate",
      "database_path": "/state/pipeline.db",
      "integrity": "ok",
      "command_count": 0,
      "event_count": 0,
      "receipt_count": 0,
      "production_authorized": false,
      "certified": false,
      "claim_ceiling": "PHASE_09_DEVELOPMENT_RELEASE_CANDIDATE_EVIDENCE"
    },
    "air": { "...": "..." },
    "vae": { "...": "..." },
    "interview": { "...": "..." },
    "builder": { "...": "..." }
  }
}
```

Negative example — `GET /api/health/{service}` with unknown name:
```json
{
  "error_code": "NOT_FOUND",
  "message": "Unknown service: 'unknown'. Valid values: pipeline, air, vae, interview, builder",
  "service": "unknown",
  "timestamp": "2026-07-25T10:00:00Z"
}
```

---

## 7. Implementation Stages and Exact Target Paths

All paths are relative to the repository root after the directory restructure described in CA_APP_FR_EPIC_SPEC_PLAN.md Part 5 has been applied.

### Stage 1 — Config and dependencies (no service code yet)

**`api/__init__.py`** — empty, marks `api/` as a Python package

**`api/config.py`**
```python
from __future__ import annotations
import os
from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class AppConfig:
    ca_data_root: Path
    ca_media_root: Path
    ca_delegation_root: Path
    gateway_version: str = "0.1.0"

def load_config() -> AppConfig:
    data_root = Path(os.environ.get("CA_DATA_ROOT", "/state"))
    return AppConfig(
        ca_data_root=data_root,
        ca_media_root=Path(os.environ.get("CA_MEDIA_ROOT", data_root / "media")),
        ca_delegation_root=Path(
            os.environ.get("CA_DELEGATION_ROOT",
            # default: find ca_delegation_rc4 package data
            Path(__file__).parent.parent / "packages" / "ca_delegation_rc4")
        ),
    )
```

**`api/dependencies.py`**
```python
from __future__ import annotations
from fastapi import Request
from cmf_pipeline.application import PipelineApplication
from cmf_activative_intelligence.application import AirApplication
from cmf_vae.application import VAEApplication
from conscious_activations_interview_expression.application import InterviewExpressionApplication

def get_pipeline(request: Request) -> PipelineApplication:
    return request.app.state.pipeline

def get_air(request: Request) -> AirApplication:
    return request.app.state.air

def get_vae(request: Request) -> VAEApplication:
    return request.app.state.vae

def get_interview(request: Request) -> InterviewExpressionApplication:
    return request.app.state.interview

def get_builder(request: Request):
    return request.app.state.builder
```

**`api/errors.py`**
```python
from __future__ import annotations
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ca_contracts import utc_now_rfc3339

class ErrorResponse(BaseModel):
    error_code: str
    message: str
    service: str | None = None
    timestamp: str

def not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            error_code="NOT_FOUND",
            message=str(exc),
            timestamp=utc_now_rfc3339(),
        ).model_dump(),
    )

def internal_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred",
            timestamp=utc_now_rfc3339(),
        ).model_dump(),
    )
```

### Stage 2 — Health router

**`api/routers/__init__.py`** — empty

**`api/routers/health.py`**
```python
from __future__ import annotations
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ca_contracts import utc_now_rfc3339

router = APIRouter()

VALID_SERVICES = {"pipeline", "air", "vae", "interview", "builder"}

class ServiceHealthItem(BaseModel):
    service: str
    product_id: str
    product_version: str
    authority_state: str
    database_path: str
    integrity: str
    command_count: int
    event_count: int
    receipt_count: int
    production_authorized: bool
    certified: bool
    claim_ceiling: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    gateway_version: str
    ca_data_root: str
    services: dict[str, dict]

def _collect_service_status(app_state, service_name: str) -> dict:
    try:
        app_obj = getattr(app_state, service_name)
        raw = app_obj.status()
        return {"service": service_name, "integrity": "ok", **raw}
    except Exception as exc:
        return {
            "service": service_name,
            "integrity": "error",
            "error": str(exc),
            "production_authorized": False,
            "certified": False,
        }

@router.get("/health", response_model=HealthResponse)
def get_health(request: Request):
    config = request.app.state.config
    statuses = {
        name: _collect_service_status(request.app.state, name)
        for name in VALID_SERVICES
    }
    overall = "ok" if all(s.get("integrity") == "ok" for s in statuses.values()) else "degraded"
    response = HealthResponse(
        status=overall,
        timestamp=utc_now_rfc3339(),
        gateway_version=config.gateway_version,
        ca_data_root=str(config.ca_data_root),
        services=statuses,
    )
    status_code = 200 if overall == "ok" else 503
    return JSONResponse(content=response.model_dump(), status_code=status_code)

@router.get("/health/{service}")
def get_service_health(service: str, request: Request):
    if service not in VALID_SERVICES:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown service: '{service}'. Valid values: {', '.join(sorted(VALID_SERVICES))}",
        )
    status = _collect_service_status(request.app.state, service)
    status_code = 200 if status.get("integrity") == "ok" else 503
    return JSONResponse(content=status, status_code=status_code)
```

### Stage 3 — Main application

**`api/main.py`**
```python
from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.config import load_config
from api.errors import not_found_handler, internal_error_handler
from api.routers import health

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    config = load_config()
    app.state.config = config

    db_path = config.ca_data_root

    # Pipeline
    from cmf_pipeline.application import PipelineApplication
    pipeline = PipelineApplication(database_path=db_path / "pipeline.db")
    pipeline.initialize()
    pipeline.load_default_development_candidates()
    app.state.pipeline = pipeline

    # AIR
    from cmf_activative_intelligence.application import AirApplication
    air = AirApplication(database_path=db_path / "air.db")
    air.initialize()
    air.load_registries()
    app.state.air = air

    # VAE
    from cmf_vae.application import VAEApplication
    vae = VAEApplication(
        database_path=db_path / "vae.db",
        storage_root=config.ca_media_root,
        delegation_root=config.ca_delegation_root,
    )
    vae.initialize()
    app.state.vae = vae

    # Interview Expression
    from conscious_activations_interview_expression.application import InterviewExpressionApplication
    interview = InterviewExpressionApplication(database_path=db_path / "interview.db")
    interview.initialize()
    app.state.interview = interview

    # Builder
    from cmf_builder.application.productization_service import BuilderProductizationService
    builder = BuilderProductizationService()
    app.state.builder = builder

    yield  # server runs here

    # --- shutdown --- (SQLite connections are closed by garbage collection;
    # explicit close hooks can be added per service if needed)

app = FastAPI(
    title="Conscious Activations",
    version="0.1.0",
    description="One product. Interview to content batch.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)

app.add_exception_handler(404, not_found_handler)
app.add_exception_handler(500, internal_error_handler)

app.include_router(health.router, prefix="/api")
# Wave 2 routers registered here as each spec is implemented:
# app.include_router(harnesses.router, prefix="/api/harnesses", tags=["harnesses"])
# app.include_router(interviews.router, prefix="/api/interviews", tags=["interviews"])
# app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])
# app.include_router(revisions.router, prefix="/api/revisions", tags=["revisions"])
# app.include_router(ship.router, prefix="/api/ship", tags=["ship"])
```

### Stage 4 — Infrastructure

**`infra/docker/dockerfile.api`**
```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install packages in dependency order
COPY packages/ca_contracts packages/ca_contracts
COPY packages/ca_runtime packages/ca_runtime
COPY packages/ca_delegation_rc4 packages/ca_delegation_rc4
COPY packages/ca_release packages/ca_release
COPY services/builder services/builder
COPY services/air services/air
COPY services/pipeline services/pipeline
COPY services/interview services/interview
COPY services/vae services/vae

RUN pip install --no-cache-dir \
    packages/ca_contracts \
    packages/ca_runtime \
    packages/ca_delegation_rc4 \
    packages/ca_release \
    services/builder \
    services/air \
    services/pipeline \
    services/interview \
    services/vae \
    fastapi==0.115.0 \
    uvicorn[standard]==0.30.0 \
    python-multipart==0.0.9 \
    pydantic==2.7.0

COPY api api
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**`infra/docker/docker-compose.yml`** (replaces `deployment/phase9/docker-compose.local.yml`)
```yaml
name: conscious-activations

services:
  api:
    build:
      context: ../..
      dockerfile: infra/docker/dockerfile.api
    ports:
      - "8000:8000"
    environment:
      CA_DATA_ROOT: /state
      CA_MEDIA_ROOT: /media
      CA_DELEGATION_ROOT: /app/packages/ca_delegation_rc4
    volumes:
      - ca-state:/state
      - ca-media:/media
    command: ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    restart: unless-stopped

  web:
    build:
      context: ../../apps/web
      dockerfile: ../../infra/docker/dockerfile.web
    ports:
      - "3000:3000"
    environment:
      VITE_API_URL: http://localhost:8000
    depends_on:
      - api

volumes:
  ca-state: {}
  ca-media: {}
```

**`api/requirements.txt`** (for local dev without Docker)
```
fastapi==0.115.0
uvicorn[standard]==0.30.0
python-multipart==0.0.9
pydantic==2.7.0
```

---

## 8. Failure, Migration, Rollback, Recovery, and Observability

### Typed failures

| Failure | Cause | Behaviour | Recovery |
|---|---|---|---|
| `SERVICE_INIT_FAILED` | A service application object raises during startup lifespan | Server refuses to start; `docker compose up` exits with non-zero code; log shows which service failed and why | Fix the underlying service issue (e.g. missing delegation root path) and restart |
| `SERVICE_STATUS_ERROR` | `.status()` raises during a `/health` request | Returns `integrity: "error"` for that service, aggregate status `"degraded"`, HTTP 503 | Does not crash the server; other services continue operating |
| `DATABASE_NOT_FOUND` | `CA_DATA_ROOT` path does not exist | `SERVICE_INIT_FAILED` — SQLite will fail to open | Create the directory or mount the volume correctly |
| `VAE_DELEGATION_ROOT_MISSING` | `CA_DELEGATION_ROOT` path missing | `SERVICE_INIT_FAILED` — VAEApplication raises | Verify `ca_delegation_rc4` package installation path |

### Migration
This spec introduces the `api/` directory and `infra/docker/` directory. It does not modify any existing Python package. No database migration is required — each service calls `.initialize()` which runs its own SQLite migration on startup.

The old `deployment/phase9/docker-compose.local.yml` and `deployment/phase9/Dockerfile.python` are superseded. They must not be deleted until `infra/docker/docker-compose.yml` passes its acceptance tests.

### Observability
- Uvicorn access log: every request logged to stdout with method, path, status, latency
- Startup log: each service name and database path logged at `INFO` on successful init
- Shutdown log: "Conscious Activations API shutting down" at `INFO`
- `/api/health` is the primary observability surface; no external monitoring tool is required for this spec

---

## 9. Acceptance Criteria

**AC-001 — Server starts cleanly**
Given `CA_DATA_ROOT` points to a writable directory and `ca_delegation_rc4` is installed,
When `uvicorn api.main:app --host 0.0.0.0 --port 8000` is run,
Then the server starts without error, all five services initialise, and the log shows each service database path.
Failure example: server raises `ImportError` because a service package is not installed.
Evidence: stdout log captured in CI.
Test layer: integration — `tests/api/test_startup.py`.

**AC-002 — Health endpoint returns all services**
Given the server is running with all five service packages installed,
When `GET /api/health` is called,
Then the response is HTTP 200 with `status: "ok"`, `services` dict contains exactly the keys `pipeline`, `air`, `vae`, `interview`, `builder`, and each has `integrity: "ok"`.
Failure example: `services` dict missing `"vae"` key, or `integrity: "error"` for any service.
Evidence: response body JSON.
Test layer: integration — `tests/api/test_health.py::test_all_services_healthy`.

**AC-003 — Per-service health endpoint**
Given the server is running,
When `GET /api/health/pipeline` is called,
Then the response is HTTP 200 with `service: "pipeline"` and `integrity: "ok"`.
When `GET /api/health/unknown` is called,
Then the response is HTTP 404 with `error_code: "NOT_FOUND"`.
Failure example: HTTP 200 returned for unknown service name.
Evidence: response status code and body.
Test layer: integration — `tests/api/test_health.py::test_per_service_health`.

**AC-004 — Degraded status on service failure**
Given the `pipeline` service database path is deliberately set to an unwritable location,
When `GET /api/health` is called,
Then the response is HTTP 503, `status: "degraded"`, `services.pipeline.integrity: "error"`, and all other services show `integrity: "ok"`.
Failure example: entire server crashes instead of returning 503.
Evidence: response status code and body.
Test layer: integration — `tests/api/test_health.py::test_degraded_on_service_failure`.

**AC-005 — CORS headers present**
Given the server is running,
When `OPTIONS /api/health` is called with `Origin: http://localhost:3000`,
Then the response includes `Access-Control-Allow-Origin: http://localhost:3000`.
Failure example: CORS header absent, causing browser to block the request.
Evidence: response headers.
Test layer: integration — `tests/api/test_health.py::test_cors_headers`.

**AC-006 — Docker Compose brings up a live server**
Given `infra/docker/docker-compose.yml` and all source directories are present,
When `docker compose -f infra/docker/docker-compose.yml up --build -d api` is run,
Then within 30 seconds `curl http://localhost:8000/api/health` returns HTTP 200.
Failure example: container exits immediately due to import error.
Evidence: curl exit code 0 and response body.
Test layer: deployment smoke test — `tests/api/test_smoke.sh`.

**AC-007 — No modification to existing service packages**
Given the Phase 9 test suite at `tests/` was passing before this spec,
When this spec is fully implemented and `python -m pytest tests/ -q` is run,
Then all pre-existing tests continue to pass.
Failure example: any test that was previously passing now fails.
Evidence: pytest output — 0 failures.
Test layer: regression — run full existing suite.

---

## 10. Testing and Completion Evidence

### Test files to create

**`tests/api/__init__.py`** — empty

**`tests/api/test_health.py`**
- `test_all_services_healthy` — AC-002
- `test_per_service_health` — AC-003 (valid name)
- `test_unknown_service_returns_404` — AC-003 (invalid name)
- `test_degraded_on_service_failure` — AC-004
- `test_cors_headers` — AC-005
- `test_error_response_shape` — validates `ErrorResponse` schema on 404

**`tests/api/test_startup.py`**
- `test_lifespan_initialises_all_services` — AC-001
- `test_app_state_has_all_service_objects` — each `app.state.{service}` is not None after startup

**`tests/api/test_smoke.sh`** (bash, run in CI after Docker build)
- builds the api image
- starts the container
- polls `GET /api/health` until 200 or 30-second timeout
- asserts `status == "ok"` in response body

### Test tooling
Use `httpx` + `anyio` + `pytest-anyio` for async FastAPI testing:
```bash
pip install httpx pytest-anyio --break-system-packages
```

FastAPI `TestClient` pattern (synchronous, no async needed for health tests):
```python
from fastapi.testclient import TestClient
from api.main import app

def test_all_services_healthy():
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert set(data["services"].keys()) == {"pipeline", "air", "vae", "interview", "builder"}
```

### Pre-existing regression
Run before and after implementing this spec:
```bash
python -m pytest tests/ -q --tb=short
```
Zero new failures is a hard gate.

### Build Receipt claim ceiling
`GATEWAY_BOOTSTRAP_DEVELOPMENT_EVIDENCE`

This spec does not claim:
- authentication or authorisation
- production deployment
- Wave 2 routes (harnesses, campaigns, interviews, revisions, ship)
- WebSocket support
- React frontend connectivity beyond CORS headers
- certified operation

---
spec_end: true
next_spec: TS-APP-API-002 (Harness Library API)
prerequisite_for_next: AC-006 must pass (server running in Docker) before TS-APP-API-002 implementation begins
