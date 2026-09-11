# CAE Studio Runtime Orchestrator (M0095)

This package provides one development Studio origin and one bounded process orchestrator. It does **not** move CAE semantic meaning, canonical state, provenance, or promotion authority into external runtimes.

## Brownfield fit

The uploaded repository already contains the CAE FastAPI API (`api/main.py`), React/Vite Studio UI (`apps/web`), CAE health endpoint (`GET /api/health`), and the native OpenChatCut MCP adapter (`services/pipeline/src/cmf_pipeline/media/openchatcut.py`). The orchestrator composes those existing paths without replacing them.

The uploaded snapshot also lacks a live `services/studio/` package and does not contain Git metadata. Those pre-existing gaps are not widened or silently repaired by M0095.

## Topology

The public origin is:

`http://127.0.0.1:3000`

Control/health endpoints are exposed only on loopback and are then proxied through the same origin:

- `/__studio/health`
- `/__studio/capabilities`
- `/__studio/topology`
- `/api/` → CAE API
- `/ws/` → CAE API WebSocket surface
- `/` → CAE Studio UI
- `/runtime/<id>/` → only enabled downstream runtimes

Each launched process gets its own process group/session and its own log file under the orchestrator runtime root (`deployment/dev/caestudio/.runtime/` by default). Launching is sequential and deterministic; the manifest is the campaign control matrix.

## Run

From the repository root:

```bash
python deployment/dev/caestudio/orchestrator.py validate
python deployment/dev/caestudio/orchestrator.py start
```

`validate` renders and syntax-checks the deterministic nginx gateway without launching runtime processes. `start` launches enabled runtimes, the loopback control server, and nginx, then prints an observed health document. Press `Ctrl-C` to terminate the owned process groups.

The CAE API requires the repository's normal Python dependencies. The Studio UI requires its normal Node dependencies (`apps/web/node_modules`). The orchestrator does not install or mutate those dependencies.

## Optional runtime enablement

Optional downstream services are **off by default** and fail closed when an enable flag is set but its command/health environment is missing.

OpenChatCut:

```bash
export CAE_OPENCHATCUT_ENABLED=true
export CAE_OPENCHATCUT_COMMAND='...native OpenChatCut launcher...'
export CAE_OPENCHATCUT_UI_URL='http://127.0.0.1:<port>'
export CAE_OPENCHATCUT_MCP_URL='http://127.0.0.1:5199/api/external-mcp/mcp'
```

The OpenChatCut health probe uses the current CAE adapter's MCP protocol version (`2025-06-18`) and checks `initialize` plus `serverInfo`. This is a runtime reachability/protocol proof only; it is not proof of semantic correctness or operator acceptance.

Presentation, SuperVisual, and SAM3 use the same pattern with their respective `*_ENABLED`, `*_COMMAND`, `*_URL`, and `*_HEALTH_URL` environment variables.

## Evidence boundary

A green orchestrator test or nginx syntax check proves topology/configuration behavior only. It does not prove that a native external runtime is installed, that a UI is base-path compatible, that an external runtime is semantically correct, or that a visual result is evidence-grounded. Operator review remains mandatory for external runtime reachability, visual quality, source lineage, and promotion.
