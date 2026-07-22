# CMF TS-120..132 OpenMontage Adapter ERA3 Audit and Revision

Date: 2026-06-25
Status: audited, revised, and protocol-passed

## Scope

This audit covers `TS-CMF-120` through `TS-CMF-132`, the OpenMontage-inspired CMF production orchestration adapter spec set. The audit checks the specs against the CMF/ERA3 tech spec protocol, the user's legacy-inventory mandate, and implementation-readiness needs for actual backend work.

## Files Audited

| Spec Range | Purpose |
|---|---|
| `TS-CMF-120` | Open-source reference adapter governance. |
| `TS-CMF-121` | Production pipeline manifest registry. |
| `TS-CMF-122` | Stage director skill contract binding. |
| `TS-CMF-123` | Capability/tool registry and provider menu. |
| `TS-CMF-124` | Scored provider selector and capability router. |
| `TS-CMF-125` | Brand-scoped workspace and checkpoint runtime. |
| `TS-CMF-126` | Reference video and existing-footage intake adapter. |
| `TS-CMF-127` | Real-footage corpus and source-media retrieval adapter. |
| `TS-CMF-128` | Render runtime selection and locking. |
| `TS-CMF-129` | Pre-compose delivery promise and slideshow risk gate. |
| `TS-CMF-130` | Post-render self-review and media QA gate. |
| `TS-CMF-131` | Budget, cost, and resource governance. |
| `TS-CMF-132` | Canonical stage artifacts, human approval, and reviewer protocol. |

## Audit Findings and Revisions

| Finding | Severity | Evidence | Revision Applied |
|---|---:|---|---|
| Canonical CMF source trace was incomplete. | High | Specs declared `requires_legacy_inventory: true`, but Files Read did not consistently name the source documents that define interview-first extraction, Brand Genesis, creative pipeline, project-local structure, and Python/DSPy/Pi runtime boundaries. | Added canonical source rows to all 13 Files Read tables: `CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/00_AGENT_START_HERE.md`, `02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md`, `CCP V9`, `CCP V9.1`, Brand Genesis V3, Creative Pipeline V2, and `PROJECT_STRUCTURE.md`. |
| Existing Backend Integration was under-specified for persistence. | High | ERA3 requires exact files, database tables, and API routes. The specs named service/repository files but did not consistently declare exact durable table targets. | Added `Postgres tables:` rows to every Existing Backend Integration table, covering candidates, receipts, manifests, skills, provider capabilities, workspaces, media intake, corpus items, runtime locks, QA receipts, budget entries, and approval artifacts. |
| API route specificity was incomplete. | Medium | Several rows said "add endpoints" without route names. This is enough for a concept spec but weak for build handoff. | Added exact route rows for each spec, such as `/api/v1/orchestration/manifests`, `/api/v1/provider-jobs/provider-selection`, `/api/v1/source/media-intake`, `/api/v1/renders/runtime/lock`, and `/api/v1/review-decisions/artifacts`. |
| Registry namespaces are declared but not yet built. | Medium | New registry paths such as `registries/integrations/`, `registries/pipelines/`, `registries/providers/`, and `registries/skills/` are specified but not created by this doc pass. | Left as implementation tasks because these specs define new build work. Audit marks them as build dependencies, not current-file defects. |
| Structural protocol coverage passed. | None | All specs already had the mandatory 10 sections, CBAR subsection, ADR-05 subsection, Technical Decisions, Primary Output Schema, fallback behavior, tasks, acceptance criteria, dependencies, and tests. | No structural rewrite needed after the first revision wave. |

## Validation Evidence

| Check | Evidence | Result |
|---|---|---|
| Target file count | `rg --files "THE CMF STUDIO\\docs\\tech-specs" | rg "TS-CMF-12[0-9]|TS-CMF-13[0-2]"` | 13 specs. |
| ERA3 protocol markers | PowerShell scan for all required headings, context subsections, failure examples, test evidence, canonical CMF sources, `Postgres tables:`, and `/api/v1/` route rows. | `CHECKED_FILES=13` |
| Forbidden drift terms | `rg -n -i -g "TS-CMF-12*.md" -g "TS-CMF-13*.md" "newsletter|mvp|flux/kontext|\\brunning\\b" "THE CMF STUDIO\\docs\\tech-specs"` | No matches. |
| Line depth after revision | `Measure-Object -Line` across TS-CMF-120..132 | Each revised spec is 174-190 lines. |

## Build Readiness Verdict

The specs are now stronger implementation inputs than the previous pass because they bind OpenMontage-inspired orchestration patterns to CMF's canonical source documents, exact API routes, exact durable persistence targets, existing service owners, primitive gates, CBAR mandates, receipts, and operator review boundaries.

The correct next step is implementation planning for registry seeds and service contracts, beginning with TS-CMF-120 through TS-CMF-124 before moving into workspace, source media, render, QA, budget, and approval layers.

## Residual Risk

No Python service implementation tests were run. This audit only verifies documentation and specification readiness. Runtime completeness still depends on creating the declared registry files, migrations/tables, service contracts, API handlers, and tests.
