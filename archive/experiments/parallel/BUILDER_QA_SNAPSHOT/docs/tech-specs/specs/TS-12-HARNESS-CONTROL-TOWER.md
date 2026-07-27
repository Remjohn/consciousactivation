# TS-12: Harness Control Tower

Status: `SPEC_RATIFIED_PENDING_STORY_MAPPING`

## Traceability

- Owned: FR-117 through FR-126; NFR-PERF-001, NFR-TRACE-002, NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-UX-001, NFR-UX-002.
- Decisions: D002, D007, D010, D011, D013, D014, D015, D017, D018, D020, D021, D024, D025, D026, D027, D033.
- UX contract: `docs/ux/HARNESS_CONTROL_TOWER_UX_CONTRACT.md`, approved on 2026-07-14.

## Responsibility And Authority

Own event-derived read models and governed command surfaces for run overview, graphs, evidence/visual parses, Genesis, skills/capsules, contracts/modules, evaluation/repair, cost/latency/context, queues, incidents, and human actions. It does not own canonical state. UI state is ephemeral presentation only.

Deterministic projectors own status. Humans issue authenticated commands. Agents may never drive privileged UI actions or authoritatively edit projection data.

## Modules And Components

`control_tower/projections.py`, `control_tower/queries.py`, `control_tower/commands.py`, `api/{runs,evidence,graphs,evaluation,actions}.py`, and proposed `ui/` React/TypeScript application.

## Canonical Data Structures

- `RunOverviewProjection { run_id, target, lifecycle, active_node, blockers, gates, latest_checkpoint, cost, latency, authorization }`
- `GraphProjection { graph_ref, nodes, edges, statuses, evidence_links, invalidations }`
- `ActionDescriptor { action_id, command_type, allowed_actor, preconditions, confirmation, expected_version }`
- `ProjectionCursor { projector_id, event_position, schema_version, rebuilt_at }`
- `ExportBundle { query, projection_versions, event_range, redactions, artifacts, generated_at }`

Every displayed status includes evidence/receipt links and event position. The UI cannot write database tables; it calls command handlers with expected versions.

## APIs, Commands, Events, Persistence

- Queries: `GET /runs`, `/runs/{id}`, `/graphs/{kind}`, `/evidence`, `/decisions`, `/skills`, `/evaluations`, `/repairs`, `/workflows`, `/events`, `/exports`.
- Commands: `POST /commands/{type}` for ratify, reject, waive, retry, cancel, authorize, revoke, and export; each uses idempotency key and optimistic version.
- Input events: all Run Ledger domain/workflow events. Output event: `ControlTowerCommandRequested`; domain services emit the authoritative result.
- Persistence: rebuildable relational projections and search indexes; no canonical mutation.

## Dependency, Invalidation, Idempotency, Resume

Projectors process ordered events at least once and apply each event ID once. Rebuild starts from zero or a verified projection checkpoint. Schema upgrades use side-by-side projection versions and atomic read switch. Stale command versions return current state and require deliberate retry.

## Security And Isolation

Role-based and attribute-based authorization constrains queries/actions by run, evidence class, benchmark role, and human authority. Protected labels, secrets, raw chain-of-thought, and unrelated sources never enter projections. Exports are redacted and audited.

## Observability, Cost, And Performance

Targets subject to ratification: p95 query under 500 ms, command acknowledgement under 1 second, event-to-view lag under 2 seconds, WCAG 2.2 AA, keyboard-complete operation, and no layout dependence on color alone. Report projection lag, errors, rebuild time, command conflicts, and UI performance.

## Failures And Recovery

Projection failure pauses only the projector and exposes lag; authoritative events remain intact. Rebuild verifies cursor/event continuity. UI disconnect resumes from cursor. Command failure shows typed domain reason and receipt link without optimistic local success.

## Acceptance Tests

1. Every status links to evidence or receipt and event position.
2. Rebuilding all projections from events yields equivalent views.
3. Direct projection writes cannot change run state.
4. Stale/unauthorized commands fail without domain events.
5. Protected benchmark labels never appear in UI or export.
6. Keyboard, screen-reader, focus, contrast, and reduced-motion tests pass.
7. Workflow queues, routes, retries, sandbox status, budgets, and incidents are visible for Format 02.
8. Projection outage does not stop authoritative workflow processing.

## Implementation Tasks

1. Ratify UI/deployment profile and accessibility budget.
2. Define projection, query, action, export, and redaction schemas.
3. Implement idempotent projectors and rebuild tooling.
4. Implement command/query API with authority guards.
5. Build operational React views after API contracts stabilize.
6. Add replay, lag, security, accessibility, and performance tests.

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Project constitutional lineage and conversational state without redesigning approved UX | control_tower_projection_owner | Event-derived read model only; UI remains non-authoritative | `ControlTowerConstitutionalProjection` with category/profile, lineage, calls, receipts, moments, wrong-reading locks, HG-015, and external handoffs | Mark projection stale/unavailable; never synthesize missing authority or expose protected data | replay, redaction, stale projection, and authorization fixtures | Existing routes render additive fields and preserve approved command authority | Additive API/projection version; original UX approval and routes remain valid |

## Non-Goals And Migration

The Control Tower is not a second database, a free-form IR editor, a final harness UI, or a V2.1 UI migration.
