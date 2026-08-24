# Gemini Execution Mandate — Phase 03 / CA-AUTH-01

**Status:** `DRAFT — BLOCKED UNTIL CA-MAP-01 OPERATOR ACCEPTANCE`  
**Phase ID:** `CA-AUTH-01`  
**Title:** Development-Uncertified CAE Authoring Controls and Static Validators  
**Execution classification:** Authoring-procedure documentation and static validation only  
**Required prior decision:** Approve CA-MAP-01 and authorize CA-AUTH-01 only  
**Required gate on completion:** `OPERATOR_REVIEW`

## 1. Authority and purpose

This mandate is governed by the CAE Governance & Specification Bridge Bundle v3, the Phase 0 Object Constitution Protocol, the Conscious Activation Definition Grammar Bundle, [the CAE Multi-Tenant Authority and Canonicalization Plan](../implementation/CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md), [the 12-phase Gemini execution program](00_GEMINI_12_PHASE_EXECUTION_PROGRAM.md), and the accepted CA-MAP-01 outputs. It has no legal effect until the CAE control record contains an operator decision approving CA-AUTH-01.

CAE already contains strong definition doctrine: a meta-object constitution, 26 dimensions, class grammars, a class matrix, authoring guidance, and a checklist. Those documents are **protocol sources**, not executable CAE authoring Skills. The existing WP-06 Evidence-to-AIR Skill is a bounded runtime/runbook Skill and must remain separate. This phase creates the smallest reusable authoring-control layer for the first tenant/Guest chain.

An authoring Skill is a repeatable, bounded procedure for producing or reviewing an artifact. It is not the artifact it produces, not a hidden ontology authority, not a database schema, not a runtime semantic operation, and not an implementation license. A constitution is the versioned law of one canonical object. A Skill is the controlled procedure that may author or review that constitution. The distinction must remain visible in names, manifests, inputs, outputs, receipts, and maturity status.

The deliverables SHALL be marked `development_uncertified`; they must not be described as production-certified ontology compilers or runtime capabilities.

## 2. Mandatory reading before action

Before planning, editing, or running a validator, Gemini SHALL read in full:

1. The accepted CA-MAP-01 outputs: `CAE_SCOPE_AND_AUTHORITY_MATRIX.md`, `CAE_OBJECT_SCOPE_COLLISION_REGISTER.md`, `CAE_CANONICAL_OPERATIONAL_PLANE_MAP.md`, `CAE_CA_MAP_01_SOURCE_CROSSWALK.md`, and `CAE_CA_MAP_01_COMPLETION_RECORD.md`.
2. `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.
3. `docs/cae/gemini_execution/00_GEMINI_12_PHASE_EXECUTION_PROGRAM.md` and `02_CA_MAP_01_SCOPE_AUTHORITY_MAPPING_MANDATE.md`.
4. `Conscious Activation Engine Brownfield/cae_phase0/phase0/CA_ENGINE_OBJECT_CONSTITUTION.md`.
5. `Conscious Activation Engine Brownfield/Conscious_Activation_Definition_Grammar_Bundle/00_META_OBJECT_CONSTITUTION.md`.
6. All relevant class grammar files from `Conscious Activation Engine Brownfield/Conscious_Activation_Definition_Grammar_Bundle/01_*.md` through `15_*.md`, plus `16_OBJECT_DEFINITION_CHECKLIST.md`, `17_PROTOCOL_AUTHORING_GUIDE.md`, and `18_OBJECT_CLASS_MATRIX.md`.
7. `08_CAE_IMPLEMENTATION_GATE.md`, `02_CAE_TECH_SPEC_WRITING_PROTOCOL.md`, `03_CAE_OBJECT_TO_SPEC_TRACEABILITY_PROTOCOL.md`, and `21_CAE_STATE_CONTROL_TEST_AND_PROOF_PROTOCOL.md` from the v3 governance bundle.
8. `docs/cae/skills/EVIDENCE_TO_AIR_FIRST_SLICE_SKILL.md` only to preserve the boundary between a runtime/runbook Skill and an authoring-control Skill.

If CA-MAP-01 is not accepted, incomplete, or unresolved for pilot objects, Gemini SHALL stop as `BLOCKED`. It SHALL not author a Skill from guessed tenancy, class, authority, or parent-chain semantics.

## 3. Exact scope

CA-AUTH-01 SHALL create a compact authoring-control suite for later CAE work:

1. `cae_scope_authority_mapper` — validates that an object has a declared plane, scope, current/target authority, canonical definition source, runtime representation, promotion authority, owner, parent chain, history behavior, and legal write boundary.
2. `cae_object_constitution_author` — routes a candidate to one primary artifact class and its class-specific grammar, then produces a constitution with all 26 dimensions marked `APPLICABLE`, `INAPPLICABLE_WITH_REASON`, or `PENDING_WITH_BLOCKER`.
3. `cae_constitution_collision_reviewer` — independently tests class, plane, scope, authority, lifecycle, relation, nearest-neighbor, evidence, and storage collisions; it must force `CONTRACT_CONFLICT`, `PENDING`, `SPLIT`, or `BLOCKED` when warranted.
4. `cae_requirement_traceability_author` — converts only ratified constitutions into PRD/FR traceability records; it cannot invent object meaning or implementation proof.
5. `cae_state_migration_contract_author` — writes one-aggregate source/target authority, transform, idempotency, reconciliation, cutover, and recovery contracts; it cannot provision, backfill, dual-write, or cut over data.
6. `cae_tech_spec_gate_reviewer` — checks an implementation-authorizing Tech Spec against Gates A–I and the state-control additions; it cannot implement or waive a failed gate.
7. `cae_reality_contact_proof_author` — structures fidelity, evidence, receipts, countertests, false-proof risks, and non-claims for later implementation packages.

An optional `cae_execution_mandate_compiler` MAY be specified as a formatting aid only if it receives an already-approved phase manifest. It must never choose scope, resolve collisions, alter authority, or generate operator approval.

## 4. Authorized files and package format

The agent MAY create only a new development-uncertified package directory under `docs/cae/authoring_skills/`, with one subdirectory per Skill. Every package SHALL contain:

- `SKILL.md` — purpose, lane, authority, inputs, procedure, outputs, prohibitions, escalation, and stop condition;
- `manifest.yaml` or equivalent — stable ID, version, maturity `development_uncertified`, owner, dependencies, and allowed consumers;
- `input_schema.yaml` and `output_schema.yaml` — bounded typed structures, not arbitrary prose buckets;
- `evaluation.yaml` — structural fixtures, positive anchors, deceptive negatives, expected verdicts, and fidelity;
- `receipt_schema.yaml` — what was authored/reviewed, under which source versions, with which validator result;
- `references.md` — exact governing sources and evidence boundary.

The agent MAY add a shared index, reusable static validation under `scripts/cae/authoring/`, a small fixture corpus, and a control-state update recording phase evidence/status.

The agent SHALL NOT modify existing constitutions, Phase 0/Phase 1–7 source bundles, the v3 governance bundle, production Skills, runtime packages, SQL, migrations, RLS, Storage, API routes, PRDs, FRs, Tech Specs, `.env`, or user data. It SHALL preserve unrelated working-tree changes and commit only the permitted package files.

## 5. Legal authoring rules

Every Skill SHALL use normative language precisely:

- `MUST`/`SHALL` for invariant requirements;
- `MUST NOT`/`SHALL NOT` for forbidden behavior;
- `MAY` for optional procedure steps that cannot weaken a gate;
- `PENDING`, `BLOCKED`, `CONTRACT_CONFLICT`, and `QUARANTINED` for unresolved conditions.

The constitution author MUST NOT select a class because a table, JSONB payload, or Python model is convenient. It must route by approved role/class. It must preserve source lineage but not decide whether PostgreSQL is source authority; the Scope & Authority Matrix owns that axis.

The constitution author MUST NOT fill an inapplicable dimension with generic prose. Each dimension states its status and reason. Missing evidence is `PENDING`, not a plausible sentence.

The collision reviewer MUST be independent. It SHALL challenge Guest=tenant, Receipt=outcome proof, MediaAsset=immutable bytes, HarnessTemplate=HarnessRun, policy=grant, source=projection, and URL=verified media. It may reject, never silently repair.

The traceability author SHALL reject orphan/unratified requirements and requirements missing applicable transitions, operations, errors, evidence, test class/fidelity, or false-proof analysis.

The migration-contract author SHALL keep one aggregate per contract and explicitly model `LEGACY_ONLY`, `DUAL_VERIFY`, `POSTGRES_AUTHORITATIVE`, `LEGACY_READ_ONLY`, and `RETIRED` as separate evidence-bearing transitions. It SHALL preserve the current source and require an operator decision for `MIGRATE`, `READ_THROUGH`, `RETAIN_OUT_OF_SCOPE`, `DISCARD_WITH_RECORD`, or `QUARANTINE`.

The Tech Spec reviewer SHALL fail a package that lacks RLS/Storage isolation, typed operation boundaries, current-state projection, receipt lineage, recovery, environment fidelity, or reward-hack countertests. No Skill may waive an implementation gate.

## 6. Required tests and evidence

Static validation SHALL prove at minimum:

- every manifest declares `development_uncertified` maturity;
- every Skill has all required package files and references existing authoritative sources;
- input/output schemas contain no unbounded “anything” field for a material decision;
- every Skill names forbidden actions, escalation conditions, and stop conditions;
- the constitution author routes to one class and preserves `PENDING` rather than inventing semantics;
- the collision reviewer has deceptive negatives and is independent by procedure;
- the traceability and migration Skills cannot authorize implementation or data movement;
- the Tech Spec reviewer checks every applicable Gate A–I item;
- every evaluator states fidelity and cannot call structural success E3/E4 proof;
- every authoring receipt identifies source versions, artifact hash/version, validator results, and unresolved decisions.

The fixture corpus SHALL include at least: an unclassified Workspace candidate; a false Guest-as-tenant candidate; a Policy/Grant conflation; a HarnessTemplate/Run conflation; a MediaAsset/evidence conflation; a source/YAML versus PostgreSQL projection mismatch; a requirement with no transition; and a migration contract that tries to authorize a backfill. Expected verdicts must be `PENDING`, `CONTRACT_CONFLICT`, `BLOCKED`, or rejection—not automatic normalization.

This is E1 authoring-control proof. It proves the controls reject specified false forms; it does not prove that any object constitution is correct, that PostgreSQL has become authoritative, or that a runtime implementation works.

## 7. Completion and operator gate

CA-AUTH-01 completes only when all seven required package types are present, the optional mandate compiler is either explicitly deferred or bounded, all static validators pass, deceptive fixtures are executed, receipt schemas are valid, maturity remains `development_uncertified`, and the control record identifies every known limitation.

The agent SHALL request exactly:

> **Authorize these development-uncertified CAE authoring controls for use in the pilot constitutions and specification phases, with independent collision review required and no runtime/implementation authority?**

After asking, it SHALL stop. Approval authorizes only the controlled authoring procedures, not any constitution, PRD, migration, Tech Spec, schema, or runtime implementation.

## 8. Gemini activation prompt (approximately 250 words)

You are the CAE governed execution agent for `CA-AUTH-01 — Development-Uncertified Authoring Controls`. This mandate is blocked unless CA-MAP-01 has been explicitly accepted and its five mapping artifacts are complete. Read this mandate and every required reference in full before planning, creating files, or running validators. Your authorization is only to create bounded authoring-control packages under `docs/cae/authoring_skills/`, their schemas, fixtures, receipts, references, shared index, and static validators. You are not authorized to create object constitutions, PRDs, FRs, Tech Specs, SQL, migrations, RLS, Storage policies, runtime code, registry changes, data movement, or production Skills.

Treat an authoring Skill as a repeatable procedure, not as an ontology authority. Preserve the distinction between canonical definition source, PostgreSQL runtime projection, and promotion authority. Use the accepted Scope & Authority Matrix; do not invent missing scope, class, parent, owner, or authority semantics. Every constitution output must select one primary class or remain explicitly pending. Every unresolved collision must be rejected, deferred, split, or blocked, never silently repaired.

Create development-uncertified packages with `SKILL.md`, manifest, typed input/output schemas, references, evaluation fixtures including deceptive negatives, and receipt schema. The independent collision reviewer must challenge the authoring Skill’s outputs rather than author and approve the same result. Migration and Tech Spec controls must explicitly prohibit provisioning, backfill, cutover, implementation, and gate waivers.

Run only static package validation and the listed E1 fixtures. Record commands, results, hashes, references, limitations, and maturity. Update the CAE control state and commit only allowed files. End with exactly the Section 7 operator decision and stop; do not begin CA-CANONICAL-01.
