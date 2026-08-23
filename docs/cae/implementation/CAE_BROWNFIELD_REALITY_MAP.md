# CAE Brownfield Reality Map — WP-00

**Status:** `RECON_COMPLETE_PENDING_OPERATOR_REVIEW`
**Evidence date:** 2026-08-23
**Boundary:** Read-only audit. This is a reality map, not an implementation plan or an assertion that target architecture is already present.

## Classification rules

| Classification | Meaning in this map |
|---|---|
| `IMPLEMENTED` | Executable source, schema, or runtime surface was directly inspected. This does not imply production or E4 verification. |
| `PARTIAL` | Executable evidence exists, but the target CAE responsibility is incomplete, disconnected, or bounded. |
| `SCHEMA_ONLY` | A typed schema, migration, or registry exists without an inspected runtime consumer proving the target behavior. |
| `DOCUMENT_ONLY` | A PRD, phase document, or plan describes it without direct implementation evidence. |
| `DUPLICATED` | Similar responsibility is present in multiple independent places without reconciliation. |
| `CONFLICTING` | Reliable sources or an adopted target rule and present behavior disagree. |
| `ABSENT` | No executable implementation was found in the audited scope. |

## Evidence sources

- CAE Governance & Specification Bridge Bundle v3, files `00`–`22`.
- `docs/PRD/CURRENT.md`.
- `api/main.py`, dependencies, domain, routers, and campaign repository.
- `packages/ca_runtime/src/ca_runtime/`.
- AIR, Builder, Interview, Interview Composer, Pipeline, Studio, and VAE source/migration directories.
- `Conscious Activation Engine Brownfield/cae_phase0`–`cae_phase7`.
- `Conscious Activation Engine Brownfield/sda.zip` and `sfl.zip`.

## System reality map

| Target system / object | Classification | Direct evidence | Current truth and required reconciliation |
|---|---|---|---|
| CAE Phase 0–7 architecture | `DOCUMENT_ONLY` | Brownfield `cae_phase0`–`cae_phase7` consist of specification artifacts. | Target vocabulary and requirements exist; no phase is implementation-authoritative until validated under v3. |
| API application shell | `IMPLEMENTED` | `api/main.py` mounts health, AIR, harness, interview, campaign, pipeline-status, revision, ship, and composer routers. | Operational gateway exists. It must be mapped to CAE semantic operations rather than replaced. |
| Shared command/event/receipt foundation | `IMPLEMENTED` | `packages/ca_runtime/src/ca_runtime/database.py`, `migrations/0001_foundation.sql`. | Atomic idempotent command/event/receipt persistence exists, but SQLite is development-local and its semantic coverage is generic. |
| Campaign lifecycle | `PARTIAL` | `api/domain/campaign.py`, `api/services/campaign_repository.py`. | Explicit allowed transitions and SQLite persistence exist; no CAE-wide transition/evidence contract was found. |
| Pipeline workflow runtime | `PARTIAL` | `services/pipeline/.../workflow/application/run_service.py`, pipeline migration. | Real workflow/node states, events, checkpoints, and idempotent commands exist. Campaign creation does not call `create_run()`; status/replay consumption alone does not close the bridge. |
| AIR semantic production | `PARTIAL` | AIR application, repositories, migrations, CLI, tests. | Local semantic objects, primitives, archetypes, registry snapshots, and deterministic production surfaces exist. Full CAE world/context/SDA/edging reconciliation is not demonstrated. |
| Interview evidence | `PARTIAL` | Interview Expression and Interview Composer applications, repositories, migrations, API routes. | Durable local objects/edges/events and interview workflows exist. The CAE authentication-state contract remains to be reconciled. |
| Builder / harness authoring | `PARTIAL` | Builder productization service and SQLite repository; Stage 1/2 pipeline. | Builder can produce portable development packages and receipts. It does not populate the runtime harness library for the 49 specimens. |
| Visual syntax evidence | `IMPLEMENTED` | `stage1_output`: 49 `*_STAGE1_REPORT.json`; `stage1_output/specs`: 49 `*_STAGE2_SPEC.json`. | Verified prerequisite evidence only; not a harness manifest or executable product entry. |
| Runtime harness library | `ABSENT` | `storage/harness-library` does not exist; no specimen `manifest.json` was found. | Must remain separate from Stage 1/2 completion. |
| VAE state and jobs | `PARTIAL` | `services/vae/.../repository.py`, `migrations/0001_phase8.sql`, application and schemas. | Local jobs/events/outbox are implemented. Production compute and CAE-wide state authority are not established. |
| Studio bridge | `PARTIAL` | `api/services/studio_bridge.py`; `services/studio/dist/rpc.js` exists. | Build artifact is present. No live bridge exercise was performed in WP-00, so behavior remains unverified. |
| Shared operational state | `CONFLICTING` | API startup uses per-service SQLite files; v3 doctrine and Builder ADR-003 designate PostgreSQL/Supabase as the target authority. | WP-02 must produce a migration/reconciliation contract before implementation. |
| CAE transition-contract service | `ABSENT` | Local service-specific transitions were found; no cross-service CAE transition registry/service was found. | Do not create one until state authority and first bounded transition are reconciled. |
| CAE semantic-operation gateway | `ABSENT` | Local service and route methods exist; no v3-style unified operation contract registry found. | WP-03 candidate after WP-02. |
| SDA registry | `SCHEMA_ONLY` | `sda.zip`: 13 versioned YAML records (invariants, geometries, grammar, crosswalks). | Inherited input, not yet runtime-integrated. Preserve IDs, versions, source lineage, and rationale. |
| SFL registry and failure corpus | `SCHEMA_ONLY` | `sfl.zip`: families, functions, compression rules, crosswalks, five failure cases and five mutation suites. | Inherited input, not yet runtime-integrated. Do not treat parsing as execution readiness. |
| SFL integrity | `CONFLICTING` | Failure cases cite `SFL-FAM-005`, `006`, `007`, `009`, `012`; supplied family records are `001`–`004`. | Quarantine affected cases or establish an authoritative migration mapping; never invent family records. |
| Primitive registry interoperability | `PARTIAL` | AIR migration includes primitive and archetype tables; SDA/SFL crosswalks are external seed assets. | Canonical identity and crosswalk authority remain unresolved. |
| Event and receipt lineage | `DUPLICATED` | `ca_runtime`, Pipeline, Interview, VAE, AIR, Builder, and API each maintain related local patterns. | Reuse compatible seams; do not add a competing receipt system before reconciliation. |
| PostgreSQL/Supabase integration | `ABSENT` | No executable source integration found in `api`, `services`, or `packages`; references are architectural/docs only. | No provision, credential, or migration action is authorized in WP-00. |
| Graph/vector capability | `DOCUMENT_ONLY` | Target documents mention graph/vector retrieval; no reconciled operational CAE graph/vector service was identified in this audit. | Confirm exact existing assets during object reconciliation; do not add infrastructure based on phase prose. |
| Reality-contact / anti-reward-hack proof layer | `ABSENT` | Existing tests and receipts exist, but no repository-wide E0–E4, proxy-to-intent, or taste-governance execution layer found. | WP-08 must adapt existing test infrastructure after core contracts exist. |

## State and persistence topology observed

```text
FastAPI gateway
  ├─ PipelineApplication        -> CA_DATA_ROOT/pipeline.db       (SQLite)
  ├─ AirApplication             -> CA_DATA_ROOT/air.db            (SQLite)
  ├─ VAEApplication             -> CA_DATA_ROOT/vae.db            (SQLite)
  ├─ InterviewExpression        -> CA_DATA_ROOT/interview.db      (SQLite)
  ├─ InterviewComposer          -> CA_DATA_ROOT/interview_composer.db (SQLite)
  ├─ CampaignRepository         -> CA_DATA_ROOT/campaigns/campaigns.sqlite3
  └─ Builder repository          -> CA_DATA_ROOT/builder.db        (SQLite)

Target under the v3 doctrine
  PostgreSQL/Supabase -> authoritative CAE operational state/history
  Object storage      -> immutable large artifacts
  Semantic operations -> governed access to durable state
  Runbooks/Skills     -> procedural control, not state authority
```

The present topology provides useful local seams—transactions, idempotency, events, and receipts—but it is not evidence of shared production state authority or migration parity.

## Dependencies and blocking relationships

```text
WP-00 Reality Map [complete]
        |
        +--> Operator decision: governance adoption + state authority + registry source ownership
        |
        +--> WP-01 Object / ontology reconciliation
        |       |
        |       +--> WP-04 Registry migration and resolver specification
        |
        +--> WP-02 PostgreSQL state-model reconciliation
        |       |
        |       +--> WP-03 Transition contracts + semantic-operation specification
        |               |
        |               +--> WP-06 Harness/runbook integration
        |               +--> WP-07 Receipt/evidence lineage integration
        |
        +--> WP-05 PRD / FR / Tech-Spec reconciliation
                |
                +--> WP-08 Reality-contact and reward-hack test plan
                        |
                        +--> WP-09 one bounded vertical runtime slice
                                |
                                +--> WP-10 regression, promotion, operator acceptance
```

## Proposed state transitions for work-package control

| Transition | Required evidence | Outcome when not satisfied |
|---|---|---|
| `RECON -> OPERATOR_REVIEW` | Reality map, control state, contradiction log, dependency graph, decision list. | `RECON` remains active. |
| `OPERATOR_REVIEW -> MODEL` | Explicit approval of WP-01 scope and the operator decisions it depends on. | `BLOCKED`. |
| `MODEL -> IMPLEMENT` | Relevant package is `SPEC_READY`, identifies file scope, migration/rollback, state contract, tests, and receipt contract. | `REPAIR_REQUIRED` or `BLOCKED`. |
| `IMPLEMENT -> VERIFY` | Bounded implementation artifacts and named test plan exist. | `IMPLEMENT` remains active. |
| `VERIFY -> OPERATOR_REVIEW` | Tests executed, relevant runtime path exercised, receipts preserved, fidelity level recorded, no unresolved material reward-hack gap. | `REPAIR_REQUIRED` or `BLOCKED`. |
| `OPERATOR_REVIEW -> PROMOTE` | Exact operator approval of the named work package. | No promotion. |

## Evidence requirements proposed for subsequent packages

| Package | Minimum evidence before coding | Minimum verification evidence |
|---|---|---|
| WP-01 Object / ontology reconciliation | Object matrix covering class, plane, owner, source status, current code, registry presence, relation/state gaps. | Reviewed contradiction and decision log. |
| WP-02 State-model reconciliation | Explicit state authority decision; SQLite inventory; PostgreSQL/Supabase migration/dual-read/rollback proposal. | E1 design validation only; no production-state claim. |
| WP-03 Semantic operations / transitions | Approved state model; one bounded transition contract with authorized operation, preconditions, validators, receipt, idempotency, failure routes. | E2 repository-integrated test of the selected transition. |
| WP-04 Registry migration | Hashed SDA/SFL inventory, schema/reference report, migration disposition for every broken reference. | Registry-integrity tests plus explicit quarantine/mapping evidence. |
| WP-08 Reality contact | Claim-to-test matrix, E0–E4 target, proxy-to-intent mapping, adversarial countertest, contrastive taste fixture. | Fidelity-appropriate proof packet; E4 required for human/outcome claims. |

## Operator decisions required before implementation

1. Adopt this bridge bundle and `docs/cae/implementation/` as tracked governance artifacts.
2. Confirm PostgreSQL/Supabase as the target authority and authorize a WP-02 reconciliation/specification package; do not authorize infrastructure provisioning yet unless separately requested.
3. Confirm SDA/SFL ZIPs as the migration source and name the authority for resolving the SFL missing-family lineage.
4. Name the approval authority for promotion of each CAE work package.

## WP-00 verification limits

- This audit inspected source, migrations, registry assets, bootstrap wiring, test inventory, and file presence.
- It did not run the complete regression suite, provision infrastructure, exercise the Studio bridge, alter databases, or make a production/state-authority claim.
- Therefore WP-00 is evidence of repository reality, not E2/E3/E4 verification of any CAE capability.
