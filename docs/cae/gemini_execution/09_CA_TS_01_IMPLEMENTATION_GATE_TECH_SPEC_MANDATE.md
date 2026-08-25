# Gemini Execution Mandate — Phase 09 / CA-TS-01

**Status:** `DRAFT — BLOCKED UNTIL CA-STATE-01 OPERATOR ACCEPTANCE`  
**Phase ID:** `CA-TS-01`  
**Title:** Tenant/Guest Vertical-Slice Implementation Tech Spec and Gate Review  
**Execution classification:** Implementation-authorizing specification and independent gate review only; no implementation  
**Required decision:** Approve CA-STATE-01 aggregate dispositions/contracts and authorize CA-TS-01 only  
**Gate:** `OPERATOR_REVIEW`

## 1. Authority and purpose

This mandate is governed by the CAE Governance & Specification Bridge Bundle v3, especially the Implementation Gate, Tech Spec Writing, Object-to-Spec Traceability, Semantic Operation API, PostgreSQL State Model, Harness/Runbook Integration, Test Governance, Reality-Contact, and State-Control Test/Proof protocols. It also follows accepted CA-MAP-01, CA-AUTH-01, CA-CAN-01A/B/C, CA-SPEC-01, and CA-STATE-01 artifacts, [the CAE Multi-Tenant Authority and Canonicalization Plan](../implementation/CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md), and [the Gemini 12-Phase Execution Program](00_GEMINI_12_PHASE_EXECUTION_PROGRAM.md).

CA-TS-01 produces the sole specification that may later authorize `CA-IMPL-01A`. It converts ratified constitutional law, approved PRD/FR behavior, and per-aggregate authority contracts into exact implementation boundaries for one tenant-scoped staging slice:

```text
Workspace -> authorized membership/operator access -> Engagement -> Guest
  -> verified MediaAsset/evidence boundary -> HarnessRun -> Receipt lineage
```

It must specify the schema/relationship design, operations, state/transition contracts, API/service boundary, RLS and Storage policy, migration sequence, source/target authority path, error taxonomy, test commands, proof fidelity, receipts, recovery, and rollout/rollback plan. It must specify only the objects and aggregates authorized by the accepted contracts. It must not adopt a generic CAE engine, global person identity, unrestricted operator bypass, all-Guest migration, registry runtime expansion, client portal, or any later semantic-domain implementation.

The Tech Spec is not code. It shall name exact future files and signatures only after inspecting the current brownfield paths. A design can be `READY_FOR_DEVELOPMENT` only if every applicable Gate A–I criterion has evidence or an explicit approved non-applicability rationale. A structurally complete document is not an automatic gate pass.

## 2. Mandatory reading before action

Gemini SHALL read in full before planning or editing:

1. `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.
2. All approved CA-SPEC-01 PRD/FR, traceability, Brownfield Impact, exception, and review artifacts.
3. All approved CA-STATE-01 authority matrix, aggregate contracts, source/target crosswalk, quality/quarantine register, decision ledger, and review record.
4. All accepted CA-MAP-01 and CA-CAN-01A/B/C constitution, relation-map, and contradiction-closure records.
5. The CA-AUTH-01 Tech-Spec/Gate reviewer and reality-contact authoring controls.
6. `docs/cae/implementation/CAE_POSTGRES_STATE_MODEL_RECONCILIATION.md`, `CAE_POSTGRES_MIGRATION_EXECUTION_PLAN.md`, `CAE_WP02A_FOUNDATION_PROOF.md`, and `CAE_WP03_SEMANTIC_OPERATION_PROOF.md`.
7. `CAE_WP06_HARNESS_RUNBOOK_INTEGRATION.md`, `CAE_WP07_EXECUTION_RECEIPTS_EVIDENCE_LINEAGE.md`, `CAE_WP08_REALITY_CONTACT_AND_REWARD_HACKING.md`, and `CAE_WP09_FIRST_VERTICAL_RUNTIME_SLICE.md`.
8. Actual source/migration/test paths identified as `EXTEND`/`ADAPT` in the Brownfield Impact Map, including applicable `AGENTS.md` instructions before naming a change there.
9. Bundle v3 documents `02`, `03`, `04`, `08`, `09`, `10`, `14`, `15`, `16`, `17`, and `21`.

If any approved requirement lacks a constitutional owner, any aggregate contract lacks a disposition, any target source path cannot be inspected, or a required privacy/authority/operator decision remains unresolved, Gemini SHALL mark the relevant Gate item failed or blocked. It shall not create an implementation plan that guesses an answer.

## 3. Exact scope and required Tech Spec content

The Tech Spec SHALL define one bounded staging implementation slice, not a production release. It must include:

1. **Authority and traceability.** Exact source references, constitutional owners, FR IDs, aggregate contracts, current brownfield evidence, and a clear `NEW`/`EXTEND`/`ADAPT`/`RETAIN` decision per file/component.
2. **Logical data design.** Named entities, stable fields, JSONB limits, keys, Workspace containment, legal parent chains, direct versus inherited scope, immutable/history/current projection behavior, relation constraints, and a logical DDL/relationship diagram. This is design only; no SQL file is created.
3. **Authority/migration design.** One aggregate at a time, with migration order, source transform, field crosswalk, data quality/quarantine behavior, idempotency, reconciliation, dual-verify read/write behavior if approved, cutover preconditions, rollback/recovery, and first cutover exclusion boundaries.
4. **Typed semantic operations.** Exact operation family/name, request/response schemas, actor/context resolution, authorization, state source/target, evidence/validators, transaction boundary, events, receipt payload, typed errors, retry/idempotency, and recovery. The operation derives Workspace from trusted authorization context and never trusts a caller-supplied scope alone.
5. **Service/API boundary.** Exact repository/service/module placement and signatures, current integration point, no-direct-SQL normal agent rule, and prohibited consumers. Do not expose an external client API unless specifically required by an approved FR.
6. **RLS and Storage design.** Shared-schema containment/RLS policy design, membership/operator-grant behavior, server-only credential rules, private object path structure, signed-access lifecycle, byte/hash readback, retention/revocation, and audit requirements. The design must state why schema-per-Workspace is not selected for this slice.
7. **Run/receipt design.** HarnessTemplate version reference, HarnessRun scope/context, event versus receipt behavior, evidence lineage, current-state projection, failure routes, and no self-attestation claim.
8. **Test and proof plan.** Unit, integration, environment-fidelity, reality-contact, contrastive, anti-reward-hack, and operator-taste classifications; exact commands/files, fixture topology, E0–E4 claim table, independent evidence, cleanup, and falsification path.
9. **Delivery plan.** Allowed implementation files, prohibited files, migration ordering, feature flags/read paths if any, environment requirements without secrets, observability, receipts, rollback, and exact CA-IMPL-01A completion gate.

## 4. Gate A–I review requirements

The independent gate review SHALL evaluate and record every applicable item:

```text
A Architecture: role, class, plane, neighbor/boundary resolved.
B Evidence: stable claims traced; hypotheses/lineage explicit.
C Data model: schema, relations, state/event, storage explicit.
D Runtime: legal operations, queries/views, execution plan, typed packet, receipts.
E Protection: errors, validators, anti-centroid preservation, repair/escalation.
F Brownfield: inspected sources, decisions, migration/rollback, no duplicate service.
G Verification: named tests, hard negatives, fidelity, countertests, measurable acceptance.
H Reality contact: claim/fidelity match, evidence snapshots, evaluator gaming, known gaps.
I Anti-centroid: applicable sharpness/taste constraints preserved and tested, not smoothed away.
```

For each item, the review record must give `PASS`, `FAIL`, `NOT_APPLICABLE_WITH_REASON`, or `BLOCKED`, plus evidence reference and reviewer rationale. A stateful implementation gate also requires authoritative PostgreSQL/Supabase target, current projection, history/events, legal transitions, semantic operations, evidence/receipt, recovery, countertest, and fidelity target. No item can become `PASS` based only on a future intention.

The Tech Spec must state that structural tenancy proofs do not prove SDA direction, SFL perceptual quality, Matrix of Edging, semantic truth, anti-centroid quality, human value, or E4 outcome unless a specific later evaluator covers them. Gate I may be non-applicable for this mechanical boundary only with a reason; it may not be silently omitted.

## 5. Authorized artifacts and file boundary

Gemini MAY create or update only:

- `docs/cae/tech_specs/TS-CAE-TEN-001_TENANT_GUEST_VERTICAL_SLICE.md`
- `docs/cae/tech_specs/TS-CAE-TEN-001_GATE_A_TO_I_REVIEW.md`
- `docs/cae/tech_specs/TS-CAE-TEN-001_OPERATION_AND_TRANSITION_CONTRACTS.yaml`
- `docs/cae/tech_specs/TS-CAE-TEN-001_TEST_AND_PROOF_PLAN.yaml`
- `docs/cae/tech_specs/TS-CAE-TEN-001_IMPLEMENTATION_FILE_ALLOWLIST.md`
- `docs/cae/tech_specs/TS-CAE-TEN-001_RISK_AND_ROLLBACK_REGISTER.md`
- `docs/cae/implementation/CAE_CA_TS_01_RECONCILIATION_AND_REVIEW.md`
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`
- a static Tech-Spec/Gate validator under `scripts/cae/` that reads only these artifacts.

Gemini SHALL NOT create or modify implementation code, SQL/DDL/migrations, RLS, Storage buckets/objects, data, API routes, environments, registry sources, or deployment configuration. It may inspect files and produce design examples, but example syntax must be labelled non-executable and cannot be placed into runtime paths. It shall preserve unrelated working-tree changes and commit only authorized artifacts.

## 6. Required adversarial design review

The test/proof plan and gate review must reject at least these false proofs:

- a `workspace_id` parameter controls a write without trusted actor-context authorization;
- RLS is described but a server/service role bypass is exposed to an untrusted caller;
- a cross-Workspace relation passes because only direct table checks, not parent chains, are tested;
- a private object path/URL exists without byte readback/hash verification;
- a receipt is persisted before its transition commits or references fabricated evidence;
- idempotency passes for one Workspace but collides/reuses another Workspace’s key;
- a same-name/email Guest becomes merged or cross-searchable;
- source/target counts match while scope ownership, versions, or lineage are wrong;
- a mocked Storage/service fixture proves E3 production-shaped isolation;
- an operation returns success while a downstream event/receipt/current-state projection is absent;
- a generic repair smooths semantic/taste output to pass a mechanical validator.

The output must clearly state what CA-IMPL-01A would prove if implemented: staging foundation, containment, RLS/Storage design realization, and migration mechanics—not broad authority cutover, client data migration, semantic quality, or production readiness.

## 7. Completion and operator gate

CA-TS-01 completes only when every listed artifact exists, traceability is complete, the independent Gate A–I review is evidence-based, all failures/blocks are explicit, the static validator passes, and the Tech Spec identifies one narrow implementation file allowlist and rollback boundary.

Gemini SHALL request exactly:

> **Does TS-CAE-TEN-001 pass the implementation gate and authorize CA-IMPL-01A only: staging relational containment, RLS, private Storage foundation, and typed model scaffolding within the approved allowlist?**

After asking, Gemini SHALL stop. It has no authority to implement, apply a migration, alter RLS/Storage, create data, invoke a runtime operation, or start CA-IMPL-01B.

## 8. Gemini activation prompt (approximately 250 words)

You are the CAE governed execution agent for `CA-TS-01 — Tenant/Guest Vertical-Slice Implementation Tech Spec and Gate Review`. This mandate is blocked unless CA-STATE-01 has been explicitly accepted. Read this mandate and all required artifacts before planning or editing. You may author only the Tech Spec, Gate A–I review, operation/transition contracts, test/proof plan, implementation allowlist, risk/rollback register, reconciliation record, control-state update, and static validator. You are not authorized to modify runtime code, SQL/migrations, RLS, Storage, APIs, environments, registries, or data.

Translate ratified constitutions, PRD/FR behavior, and approved per-aggregate contracts into exact design. Inspect real brownfield paths before naming future files or signatures. Preserve distinct canonical-definition, runtime, and promotion authorities. Derive Workspace scope from trusted authorization context; Guest is local, not global; templates, runs, events, operations, and receipts remain distinct. State exact containment, source/target/recovery, typed errors, receipts, and read/write transitions. Do not turn a target schema or staging proof into an authority-cutover claim.

Evaluate Gate A–I independently. Every pass needs current evidence; every failure/block needs a direct reason. Include E0–E4 fidelity, falsification, cleanup, and reward-hack cases that catch scope forgery, RLS bypass, path-without-bytes, receipt self-proof, identity merge, wrong lineage, mock topology, and missing downstream effect. Explicitly state all non-claims, including semantic/taste/E4 quality and production readiness.

Run only static Tech-Spec validation. Update control state, commit allowed documents only, ask exactly the Section 7 decision, and stop before CA-IMPL-01A.
