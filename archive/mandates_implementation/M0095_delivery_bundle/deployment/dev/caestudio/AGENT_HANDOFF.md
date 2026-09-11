# M0095 Agent Handoff

**Mandate:** M0095 — Unified CAE Studio Runtime Orchestrator and Single-Tab Topology
**Campaign:** E1 RUNTIME INTEGRATION
**Status:** `OPERATOR_REVIEW_REQUIRED`
**Operator decision requested:** `APPROVE`, `APPROVE-WITH-LIMITATIONS`, or `REJECT`

## 1. Delivered artifact

M0095 adds one bounded development/runtime orchestration layer under `deployment/dev/caestudio/`. The layer launches required CAE API/UI processes and accepts explicit operator-supplied commands for OpenChatCut, presentation, SuperVisual, and SAM3. It exposes a single loopback Studio origin through nginx and registers capabilities/health under the same origin.

The orchestrator is downstream of CAE authority. It does not own semantic meaning, canonical state, provenance, storyboard authority, VAE state, or promotion. External runtimes are declared `downstream_runtime_only` in the manifest and are replaceable.

## 2. Exact paths added

- `deployment/dev/caestudio/.gitignore`
- `deployment/dev/caestudio/README.md`
- `deployment/dev/caestudio/__init__.py`
- `deployment/dev/caestudio/manifest.json`
- `deployment/dev/caestudio/orchestrator.py`
- `deployment/dev/caestudio/M0095_EVIDENCE_RECEIPT.json`
- `deployment/dev/caestudio/AGENT_HANDOFF.md`
- `tests/cae/test_m0095_runtime_orchestrator.py`

No existing repository file was modified.

## 3. Brownfield authority mapping

| Area | Existing source | M0095 treatment | Evidence class |
|---|---|---|---|
| CAE API lifecycle | `api/main.py` | launch unchanged through uvicorn | `DOCUMENT` / `EXECUTABLE` |
| CAE health | `api/routers/health.py` | probe existing `/api/health`; no health authority duplicated | `REGISTRY_SOURCE` / `EXECUTABLE` |
| Existing Studio bridge | `api/services/studio_bridge.py` | retained; M0095 does not replace its internal runtime contract | `DOCUMENT` |
| Web dev surface | `apps/web/vite.config.ts` | proxy unchanged; gateway owns the single public origin | `DOCUMENT` / `EXECUTABLE` |
| OpenChatCut | `services/pipeline/src/cmf_pipeline/media/openchatcut.py` | MCP health probe adapts the existing native transport contract | `REGISTRY_SOURCE` / `TEST` |
| Presentation | `engines/presentation/runtime_adapter.py` | downstream launch slot only; no renderer copied | `REGISTRY_SOURCE` |
| SuperVisual | `engines/visual/supervisual/editor.py` | downstream launch slot only; no competing editor state | `REGISTRY_SOURCE` |
| SAM3 | manifest capability slot | downstream tracking/geometry capability only; no semantic authority | `SCHEMA` / `OPERATOR_DECISION_REQUIRED` |

The mandatory reading set was inspected before editing, including the Constitution, Constitutional Precedence Contract, current PRD, CAE Mandate Authoring Protocol, M0058-M0068 brownfield references, M65-M72 convergence evidence and final gate, Media Intelligence brief, and the 2026-09-10 Visual Production Authority Pack. The mandate-listed `AUTHORITY_PACK/...` paths resolve in the supplied tree as `docs/AUTHORITY_PACK/...`.

## 4. Runtime behavior

The control matrix is `deployment/dev/caestudio/manifest.json`.

Public origin:

`http://127.0.0.1:3000`

Same-origin control endpoints:

- `/__studio/health`
- `/__studio/capabilities`
- `/__studio/topology`
- `/api/` → CAE API
- `/ws/` → CAE API WebSocket surface
- `/` → CAE Studio UI
- `/runtime/<id>/` → only enabled downstream runtime routes

Each launched process uses its own process group/session and its own log file under `deployment/dev/caestudio/.runtime/` by default. The orchestrator launches processes sequentially, then starts its loopback control server and nginx gateway.

Launch failures are surfaced as `LaunchError` with the affected runtime/log. Health failures are represented as `unhealthy`/`degraded`, not silently promoted to healthy. Configuration errors for enabled optional runtimes fail closed.

## 5. OpenChatCut boundary

The existing CAE adapter records the native OpenChatCut MCP default endpoint and protocol version at `services/pipeline/src/cmf_pipeline/media/openchatcut.py:23-24`, and its initialize path requires JSON-RPC success plus `serverInfo` at lines 173-190. M0095 adapts those transport semantics for health observation and accepts both JSON and `text/event-stream` responses.

No external OpenChatCut source was copied or merged. No external repository license is claimed by M0095. The operator supplies the actual native runtime command and UI URL. The MCP health endpoint defaults to the existing CAE-native adapter URL and can take `CAE_OPENCHATCUT_MCP_TOKEN` from the environment.

## 6. Verification commands and observed results

`python -m py_compile deployment/dev/caestudio/orchestrator.py tests/cae/test_m0095_runtime_orchestrator.py`
**Observed:** exit 0.

`python -m pytest -q tests/cae/test_m0095_runtime_orchestrator.py`
**Observed:** `9 passed in 2.25s`.

`python deployment/dev/caestudio/orchestrator.py validate`
**Observed:** exit 0; deterministic public origin `http://127.0.0.1:3000`; CAE API/UI enabled; external runtimes disabled by default.

`nginx -t -c /mnt/data/cae_m0095_repo/deployment/dev/caestudio/.runtime/nginx.conf -p /mnt/data/cae_m0095_repo/deployment/dev/caestudio/.runtime`
**Observed:** nginx syntax ok; test successful.

`CAE_OPENCHATCUT_ENABLED=true python deployment/dev/caestudio/orchestrator.py validate`
**Observed:** exit 2 with structured `ConfigurationError` because the enabled runtime lacks `CAE_OPENCHATCUT_UI_URL`.

`git diff --check 1269bc57629b397414e5f02f7a51f8a462c5d066..b9af237ecb79cc7d79b1e9489f9bfad81b68fa36`
**Observed:** no whitespace errors.

`git status --short`
**Observed after cleanup:** clean.

## 7. Required counterexamples / negative proof

The test suite includes a process that stays alive but fails an expected HTTP health contract. This deliberately distinguishes “looks alive / looks good” from actual health acceptance.

It also includes missing enabled-runtime configuration, malformed/incorrect MCP response semantics, process launch failure, and deterministic replay of the gateway rendering.

These tests do **not** prove that an external native runtime is semantically correct or visually acceptable.

## 8. Environment fidelity and limitations

Observed environment: Python 3.13.5, Node v22.16.0, npm 10.9.2, nginx 1.26.3. Existing CAE Docker/runtime declarations target Python 3.12.x. `apps/web/node_modules` is absent in the supplied snapshot, while the required Python API dependencies are present.

Native OpenChatCut, presentation, SuperVisual, and SAM3 availability was not established. No mock is represented as production evidence. The external runtime slots remain disabled unless an operator provides native commands and health/target URLs.

A true single-tab external UI requires the downstream runtime to honor its mapped base path. M0095 verifies the gateway topology and does not assert that every external UI is base-path-safe.

## 9. Git provenance

The uploaded archive contained no `.git` metadata. A fresh local audit history was therefore created from the untouched archive extraction so the implementation delta is reviewable without falsely representing the archive as a remote checkout.

- Local baseline snapshot commit: `1269bc57629b397414e5f02f7a51f8a462c5d066`
- **M0095 implementation commit:** `b9af237ecb79cc7d79b1e9489f9bfad81b68fa36`
- M0095 implementation parent: `1269bc57629b397414e5f02f7a51f8a462c5d066`

The implementation commit contains the six M0095 code/test additions. This handoff and its evidence receipt are documentation follow-up artifacts and do not change the implementation SHA above.

## 10. Stop/rollback boundary

Rollback is bounded to the M0095 additions. The runtime root is ignored and disposable. Existing CAE services, canonical state, receipts, rejected artifacts, and upstream/source history are not deleted or migrated by this mandate.

## 11. Operator acceptance gate

Before promotion, the operator must:

1. Review the real Studio preview through the single origin and confirm the intended runtime routing.
2. Confirm native runtime reachability for each enabled external service; do not infer this from the focused suite.
3. Confirm external runtimes remain downstream of CAE semantic/state/provenance authority and are independently replaceable.
4. For visual output, verify source lineage, evidence-first retrieval/transformation order where applicable, and that motion/attention serves meaning rather than introducing gratuitous emphasis.

**Decision required:** `APPROVE` / `APPROVE-WITH-LIMITATIONS` / `REJECT`.
