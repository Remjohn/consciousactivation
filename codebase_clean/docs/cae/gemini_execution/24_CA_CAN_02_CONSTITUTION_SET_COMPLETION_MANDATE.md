# Gemini Execution Mandate — Phase 24 / CA-CAN-02

**Status:** `DRAFT — BLOCKED UNTIL CA-UPTL-01 OPERATOR ACCEPTANCE`  
**Phase ID:** `CA-CAN-02`  
**Title:** Constitution Set Completion (Remaining Object Constitutions to Full Canonical Coverage)  
**Execution classification:** Authoring-only phase: constitution YAML, hard-negative fixtures, collision reviews; no runtime code changes, no schema/DDL changes, no live data, no deployment, no authority change  
**Required prior decision:** “Accept CA-UPTL-01 (or its explicitly blocked subset) and authorize CA-CAN-02 for authoring the remaining object constitutions only, ahead of the operator constitution-reading pause.”  
**Required completion gate:** `IMPLEMENT -> VERIFY -> OPERATOR_REVIEW`; implementation of any constituted object is explicitly out of scope and begins only after the operator’s post-pause decision.

## 1. Authority, purpose, and boundary

CA-CAN-02 is governed by the CAE Governance & Specification Bridge Bundle v3 and inherits the ratified authoring doctrine of CA-AUTH-01 (authoring-control skills), CA-CAN-01A/01B/01C (15 ratified constitutions, 26-dimension completeness standard, hard-negative fixture discipline), CA-MAP-01 (scope/authority matrix, plane separation), and CA-SPEC-01 (PRD/FR traceability).

**Purpose:** complete the object-constitution set so that every scoped canonical object in `CAE_SCOPE_AND_AUTHORITY_MATRIX.md` and the aggregate inventory is governed before the operator reads them. The operator has ordered a **pause after this phase**: they will personally read the full constitution set, and only their post-read decisions determine what is implemented next. This mandate therefore ends at a reading-ready packet — nothing downstream.

The permitted transition is:

```text
15 ratified constitutions + scoped-but-unconstituted objects
  -> gap analysis against scope matrix / aggregate authority matrix
  -> author remaining constitutions at 26-dimension standard
  -> hard-negative fixtures defend each new constitution
  -> collision review across the FULL set (old + new)
  -> contradiction closure against canonical relation map
  -> operator reading packet
  -> OPERATOR_REVIEW (the pause)

implementation of any constituted object: NOT_STARTED until after the pause
```

## 2. Mandatory reading

Before authoring, the agent SHALL read in full:

1. All 15 ratified constitutions under `docs/cae/constitutions/` (`CA-CAN-01A_*`, `CA-CAN-01B_*`, `CA-CAN-01C_*`) as the binding style/completeness precedent.
2. `docs/cae/authoring_skills/` — all seven skill packages and `fixtures/corpus.yaml` deceptive-negative corpus; authoring MUST use these skills.
3. `CAE_SCOPE_AND_AUTHORITY_MATRIX.md`, `CAE_OBJECT_SCOPE_COLLISION_REGISTER.md`, `CAE_CANONICAL_OPERATIONAL_PLANE_MAP.md`.
4. `docs/cae/state/CAE_AGGREGATE_AUTHORITY_MATRIX.md`, the seven state contracts under `docs/cae/state/contracts/`, and `CAE_SOURCE_TO_TARGET_FIELD_CROSSWALK.md`.
5. `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md` and `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`.
6. `docs/cae/specs/PRD-CAE-TEN-001` and the 15 FRs; `TS-CAE-TEN-001` Section 3+ object definitions.
7. The three prior constitution review records (`CAE_CA_CAN_01A/01B/01C_CONSTITUTION_REVIEW.md`) including every correction applied during review.
8. Git history and working-tree state, identifying commits actually inspected.

## 3. Exact scope

### C1 — Coverage gap analysis (read-only)

Build the definitive coverage ledger: every object in the scope matrix (22 scoped objects) and aggregate authority matrix cross-referenced against the 15 ratified constitutions. Classify each uncovered object: `REQUIRES_CONSTITUTION`, `COVERED_BY_EXISTING` (with citation), or `DEFERRED_WITH_OPERATOR_SIGNOFF_REQUIRED`. The gap list SHALL be derived from the matrices, not invented; if the matrices disagree, record the contradiction and stop that item for operator resolution.

### C2 — Authoring to the ratified standard

For each `REQUIRES_CONSTITUTION` object, author a YAML constitution meeting the exact CA-CAN-01 standard: all 26 dimensions present and substantive; canonical-plane/operational-plane placement consistent with the plane map; explicit non-goals and boundary prohibitions; parent chain and legal relations matching the relation map; state vocabulary consistent with existing state contracts; zero tenant facts on the canonical plane. Expected candidates based on prior records include Engagement, HarnessRun lifecycle depth, Evaluation Run, Semantic Program, and the canonical registry objects (SDA/SFL/Primitive as governed objects) — but the C1 ledger governs; do not treat this list as authoritative until C1 confirms it.

Authoring must follow `cae_object_constitution_author` skill conventions, with `cae_constitution_collision_reviewer` applied per constitution.

### C3 — Hard-negative fixtures

Each new constitution SHALL be defended by fixtures in the established pattern (9–11 deceptive negatives per constitution, extending `fixtures/corpus.yaml` conventions): documents that look compliant but violate boundary, locality, immutability, or plane-separation rules, each with the expected rejection rationale. All fixtures must be executed through the static verification harness and rejected as expected.

### C4 — Whole-set collision review and contradiction closure

Run collision review across the FULL set (existing 15 + new), not just the additions: overlapping boundaries, ambiguous parent chains, contradictory state vocabularies, plane violations introduced by combination. Extend or amend the contradiction-closure record; any unresolved collision is quarantined with an owner question for the operator packet — never silently merged.

### C5 — Operator reading packet

Produce the deliverable the pause exists for: `CAE_CAN_02_OPERATOR_READING_PACKET.md` containing (a) the coverage ledger, (b) a one-page plain-language summary per constitution (what this object is, what it forbids, what an enforcing agent would refuse), ordered for reading (canonical plane first, then operational root-downward), (c) open questions requiring operator rulings, and (d) an amendment-request template so the operator’s read produces actionable decisions.

## 4. Evidence protocol

Applies identically to Mandate 23 (`live-probe mandatory`). For this authoring phase the probeable claims are: fixture executions (verbatim runner output committed), static validator runs (probe-executing only — presence checks are non-compliant), dimension-completeness checks (computed counts per YAML against the 26-dimension standard, command shown), and traceability references (each cited document verified to exist at the cited path during the same session). Reviewer-reproducibility is the default proof standard.

## 5. Authorized artifacts and prohibitions

Gemini MAY create or update only:

- `docs/cae/implementation/CAE_CAN_02_COVERAGE_LEDGER.md`;
- new constitutions under `docs/cae/constitutions/` (`CA-CAN-02_*.yaml`);
- extended fixtures under `docs/cae/authoring_skills/fixtures/`;
- `docs/cae/implementation/CAE_CAN_02_COLLISION_AND_CONTRADICTION_CLOSURE.md`;
- `docs/cae/implementation/CAE_CAN_02_OPERATOR_READING_PACKET.md`;
- `docs/cae/implementation/CAE_CAN_02_COMPLETION_RECORD.md`;
- one probe-executing validator under `scripts/cae/constitutions/verify_ca_can_02.py`;
- pure/local tests under `tests/cae/` for the new constitutions/fixtures only;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md` (status line only).

Gemini SHALL NOT: modify the 15 ratified constitutions (propose amendments in the reading packet instead); implement application/schema/runtime code for any constituted object; touch migrations, staging, Storage, `.env`, authorities, receipts, registries’ runtime behavior, or live/synthetic interview content; begin TS/spec authoring for unratified objects; or pre-decide outcomes reserved for the operator’s reading pause.

## 6. Adversarial challenges (each must be answered in the Completion Record)

1. A new constitution copies an existing one with renamed identifiers rather than deriving boundaries from the object’s actual role. — Coverage ledger + reviewer spot-check against the object’s contract/matrix row.
2. Dimensions are present but vacuous (boilerplate satisfying the count). — Completeness check must score substance, flag near-duplicate text across dimensions.
3. Fixtures test the checker, not the constitution (tautological rejects). — At least two fixtures per constitution must be near-miss documents that previously would have passed.
4. Collisions between NEW and EXISTING constitutions go unnoticed because review covers additions only. — Whole-set review evidence required (C4).
5. The reading packet editorializes toward a preferred implementation outcome. — Packet presents options and questions; no recommendations on undecided matters.
6. Matrix disagreements get resolved silently in favor of convenience. — Contradictions are recorded and routed to the operator, never self-resolved.
7. Ratified constitutions are quietly edited "for consistency." — Diff of `docs/cae/constitutions/` must show zero modifications to `CA-CAN-01*` files.
8. Scope creeps into implementing the best-understood object. — Any implementation invalidates the mandate.

## 7. Completion, rollback, and operator gate

CA-CAN-02 completes only when: the coverage ledger accounts for every scoped object; every new constitution meets the 26-dimension standard with defending fixtures executed and rejected-as-expected; whole-set collision review is recorded; the reading packet is assembled; the probe-executing validator passes against the committed tree; and the control state records `CONSTITUTION_SET_COMPLETE_READY_FOR_OPERATOR_READING`.

**Rollback:** Documentation-only phase; revert commits suffice. No system state is mutated.

Gemini SHALL request exactly:

> **Accept the completed constitution set and reading packet, resolve the listed open questions as you read (or defer them with owners), issue any amendments, and name what becomes the first authorized implementation package AFTER your reading pause — with nothing implemented until that decision?**

It SHALL stop after this question.

## 8. Gemini activation prompt (approximately 270 words)

You are the CAE governed execution agent for `CA-CAN-02 — Constitution Set Completion`. Blocked until CA-UPTL-01 is accepted. Read all fifteen ratified constitutions as the binding standard, the seven authoring skills and deceptive-fixture corpus, the scope/authority and aggregate matrices, plane map, relation map, contradiction closures, PRD/FRs, Tech Spec, and the three prior constitution reviews with their corrections.

First build the coverage ledger from the matrices — never invent the gap list; classify every scoped object and route matrix contradictions to the operator instead of resolving them. Author each missing constitution at the full 26-dimension standard using the authoring skills: correct plane placement, legal parents, explicit prohibitions, canonical purity. Defend each with nine-plus deceptive hard negatives including near-misses that would previously have passed. Then run collision review across the WHOLE set — old plus new — and close or quarantine every contradiction.

Then assemble the operator reading packet: per-constitution one-page plain-language summaries ordered canonical-first, open questions isolated, amendment template included. It must inform, not steer.

Live-probe evidence rules apply: commit verbatim fixture-runner outputs, computed dimension counts, and path-verified citations. Validators must execute probes, not check document presence. Do not modify ratified constitutions, implement anything, touch runtime/staging/.env, or pre-decide the operator’s pause decisions. Commit only allowed artifacts, request the exact Section 7 decision, and stop.
