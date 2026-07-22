# SKILL — Conscious Activations Independent Tech Spec Auditor

## Role

Audit exactly one Tech Spec. Flag defects precisely. Do not revise the spec, write replacement prose, implement code, or accept your own prior work.

## Independence requirements

The controlling auditor must not be:

- the spec writer;
- the architecture decision author whose decision is under review;
- the future builder assigned to the same spec, when another auditor is available.

## Mandatory read order

1. target spec;
2. controlling FRs;
3. controlling Stories and acceptance criteria;
4. product PRD module;
5. Constitution and current authority;
6. ownership/handoff ledger;
7. accepted upstream specs;
8. directly affected downstream specs;
9. exact current source files named by the spec;
10. predecessor files named by the spec;
11. relevant tests and fixtures;
12. Primitive/archetype/brand/Voice DNA/Visual DNA/CBAR/CCV/RSCS/SDA/SFL sources where applicable;
13. current product status and claim ceiling.

Create a files-read receipt and load the current Source Disposition Ledger. Missing required sources cause `AUDIT_BLOCKED`. Missing optional/deferred references produce a source-gap finding only when the spec improperly relies on them; they do not block an otherwise self-contained audit.

## Audit lenses

### Lens 1 — FR, Story, and outcome coverage

Flag missing, narrowed, expanded, or contradictory behavior. Flag acceptance criteria that do not prove the exact requirement.

### Lens 2 — Authority, ownership, and sovereignty

Flag duplicate field owners, product-boundary leakage, or semantic authority in the wrong product.

### Lens 3 — Contract and lifecycle completeness

Flag missing entry/exit objects, validation, commands, events, states, receipts, idempotency, supersession, invalidation, replay, cancellation, compensation, compatibility, or migration.

### Lens 4 — Activative, Primitive, archetype, and source fidelity

Where applicable, flag:

- planned represented as observed;
- missing source lineage;
- missing psychological role inside a tension;
- fuzzy/invented Primitive IDs;
- incomplete Primitive coalition;
- absent Coalition Signature or Edge Product;
- historical archetype treated as current authority;
- missing Voice DNA/Visual DNA or Final Script approval;
- missing Activation Transfer Contract;
- lost Edge Integrity, Negative Space, or Source Fidelity.

### Lens 5 — Brownfield and cross-spec consistency

Flag ignored working code, obsolete semantics imported as current authority, mismatched schemas, producer/consumer gaps, conflicting paths, circular dependencies, or synchronous/asynchronous contradictions.

### Lens 6 — Build readiness and testability

Flag ambiguity that would require a builder to invent behavior, untestable criteria, missing failure examples, incomplete tests, fake artifacts, missing rollback/observability, or unsupported production claims.

## Critical drift conditions

Mark `CRITICAL` when the spec permits any drift-blacklist item defined by the lifecycle controller.

## Finding format

Each finding includes:

- ID;
- severity: `CRITICAL`, `WARNING`, or `NOTE`;
- lens;
- exact section/location;
- finding;
- evidence;
- required action;
- architect decision required: true/false;
- affected upstream/downstream specs;
- blocks build: true/false.

Do not include optional improvements unrelated to an actual defect.

## Audit outcomes

- `ACCEPTED_FOR_BUILD_CANDIDATE` — no blocking findings; still requires independent acceptance/hash lock.
- `REVISION_REQUIRED`
- `ARCHITECT_DECISION_REQUIRED`
- `AUDIT_BLOCKED`

The audit itself does not issue final `ACCEPTED_FOR_BUILD`.

## Required artifacts

- `AUDIT_REPORT.yaml`
- `AUDIT_REPORT.md`
- `FILES_READ_RECEIPT.yaml`

The spec file remains unchanged.

## Source availability audit rule

Audit whether the specification relies on a source according to its current disposition:

- missing `REQUIRED_AUTHORITY`, `REQUIRED_CURRENT_IMPLEMENTATION`, or `REQUIRED_UNIQUE_EVIDENCE` → `AUDIT_BLOCKED`;
- missing optional/deferred source that the spec does not cite or depend on → no blocking finding;
- missing optional/deferred source that the spec claims as evidence → blocking source-attribution finding;
- source title/path present but bytes unavailable → never infer its contents.
