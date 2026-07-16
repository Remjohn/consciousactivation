# TS-15: Format 02 Release 1 Reference Vertical Slice

Status: `EMPIRICAL_VERTICAL_SPEC_COMPLETE_PENDING_BD-004_BD-007_BD-008_BD-010`

## Traceability

- Owned: FR-167, FR-168; deferred FR-169.
- Exercises: all Release 1 FRs and NFRs assigned to TS-01 through TS-14.
- Decisions: D001-D027 and D029-D033. D028 V2.1 migration is not applicable to this repository.
- Reference resolution: Format 02 Minimal Coach Theatre under 2D Character Animation, per current user directive and FR-143.

## Responsibility And Authority

Own the end-to-end proof that Builder can transform a hash-locked Format 02 evidence workspace into an implementation-authorized Development Capsule and ingest downstream Content Harness certification evidence. It does not implement the final Format 02 harness, Visual Asset Editor, Delegation Protocol, ComfyUI, model execution, training, or GPU scheduling.

The product lead owns reference-slice scope. The category steward owns 2D Character Animation/Format 02 policy. Evidence and benchmark stewards own corpora/labels. Builder owns compilation and proof. A downstream Content Harness owner implements and certifies the generated capsule outside this repository.

## Reference Inputs And Components

Required inputs:

1. Authoritative Format 02 specimen corpus and source authority metadata.
2. 2D Character Animation constitution and Format 02 profile.
3. Atomic Content Harness target profile.
4. Evaluated seed skills or explicit capability-gap decisions.
5. Protected benchmark cases and ratified thresholds.
6. Contract-tested stub Asset Demand port backed by approved fixtures, as ratified in ADR-018.
7. Recorded manual shadow workflow and operator/human-gate identities.

The slice uses all modules specified in TS-01 through TS-14. External asset demand is a typed fixture boundary only.

## Canonical Data Structures And Slice Manifest

`ReferenceSlice { slice_id, format_profile_ref, target_profile_ref, source_lock_ref, workflow_profile_ref, harness_ir_ref, corpus_ref, required_artifacts, required_receipts, external_contract_refs, certification_scope }`

`ReferenceSliceReceipt { slice_hash, node_results, hard_gates, benchmark_scorecard, development_capsule_hash, downstream_result_refs, outcome }`

The slice identity binds every source, schema, decision, workflow, capsule, evaluator, compiler, and artifact version.

## End-To-End Workflow

1. Select Atomic Content Harness target and Format 02 profile.
2. Diagnose and lock the evidence workspace.
3. Normalize specimens; parse visual, character-performance, staging, continuity, and temporal syntax.
4. Induce Format 02 visual/sequence grammar and draft Activative hypotheses.
5. Evaluate saturation, compare atomic boundaries, and obtain human atomicity ratification.
6. Run dependency-driven Genesis to cascade lock.
7. Compile Harness IR, Capability Ownership Map, modules, Phase/Context/Contract/Reference/Loading/Repair graphs.
8. Register/adapt required skills, compile recipes, and produce exact JIT capsule plans.
9. Compile Format 02 category/profile and Atomic Content Harness target artifacts.
10. Run skill, capsule, phase, workflow, category, and end-to-end benchmarks with protected cases.
11. Repair at the responsible layer and rerun targeted suites until gates resolve or fail.
12. Evaluate readiness and issue prototype-only or implementation authorization.
13. Compile the Development Capsule and dependency-ordered vertical stories.
14. Hand off to the external Content Harness implementation owner.
15. Ingest exact downstream implementation and harness-effectiveness receipts.

## APIs, Commands, Events, Persistence

- Command: `StartReferenceSlice(format02_profile, corpus, workflow_profile)` and existing subsystem commands.
- Query: `GetReferenceSliceTrace(slice_id)` returns every requirement, event, artifact, test, gate, and downstream receipt.
- Events: `ReferenceSliceStarted`, `ShadowWorkflowCaptured`, `ReferenceSliceGateEvaluated`, `DevelopmentCapsuleHandedOff`, `DownstreamCertificationIngested`, `ReferenceSliceCertified`.
- Persistence: one Run Ledger stream family, immutable artifacts in CAS, and a trace projection; external downstream receipts are imported as signed immutable references.

## Dependency, Invalidation, Idempotency, Resume

The slice resumes from validated workflow checkpoints. Any source, profile, ontology, decision, skill, recipe, evaluator, threshold, workflow, compiler, or external contract change invalidates its exact dependents and the final slice receipt. Re-running identical identities returns existing artifacts/receipts. A new identity creates a new slice version; history is never overwritten.

## Security And Isolation

Generators cannot access protected labels. Evidence is read-only. External asset and downstream systems use contract fixtures or signed result imports without runtime credentials. Agent nodes run in least-privilege sandboxes. Human ratification and authorization use distinct identities from generator/evaluator roles.

## Observability, Cost, And Performance

Control Tower must expose the complete critical path, node attempts, evidence/decisions, graph state, capsule identities, benchmark results, repair, sandbox, route, budget, cost, latency, human interventions, authorization, capsule handoff, and downstream outcome. Numeric gates are calibrated under BD-008, not invented here.

## Failures And Recovery

Any HG-001-HG-014 failure blocks certification. Missing empirical thresholds permits only bounded prototype authorization. Asset port failure remains contained and cannot cause editor implementation inside Builder. Downstream failure reopens the responsible Builder layer only when signed evidence establishes causality.

## Acceptance Tests

1. A fresh repository can execute the complete Format 02 shadow/profile workflow from source lock to Development Capsule.
2. Every Release 1 requirement maps to a passed test/receipt or an explicit blocked outcome.
3. Every material artifact traces to source, IR, decision, compiler, workflow, and evaluator identity.
4. Visual Syntax precedes hypotheses, atomicity, and Genesis.
5. Human gates cannot be bypassed by agents or workflow configuration.
6. Public-seam workflow, replay, resume, fault, sandbox, budget, and rollback tests pass.
7. Protected benchmark integrity and category-native sequence fidelity gates pass.
8. Development Capsule contains no final harness/editor/delegation production implementation.
9. Downstream Content Harness results bind to the exact capsule and feed back into Builder scorecards.
10. Other categories and targets remain structurally valid, explicitly `UNCERTIFIED`, and cannot inherit the Format 02 production claim.

## Implementation Tasks

1. Resolve slice blockers and lock corpus/profile/threshold/interface identities.
2. Record the manual shadow workflow with all actors, inputs, outputs, failures, costs, and human gates.
3. Compile and ratify the Release 1 Workflow Profile.
4. Build subsystem vertical stories in dependency order from TS-01 through TS-14.
5. Implement cross-spec public-seam, fault, benchmark, security, and trace suites.
6. Compile the Development Capsule and execute external handoff/certification protocol.
7. Issue the Release 1 reference receipt and retain general certification as deferred.

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Preserve Format 02 as the sole Release 1 reference while adding structural fifth-category support | format_02_slice_owner | Format 02 remains 2D Character Animation; conversational profiles are schema/contract fixtures only | reference-slice profile plus five-category registry and `UNCERTIFIED` markers | Reject claims that Format 02 certifies conversation or all five categories | non-regression and false-portfolio-claim tests | Format 02 path remains unchanged and other profiles cannot issue production authorization | ADR-014 and accepted slice scope remain intact; V1.2 adds no execution dependency |
| Prove stubbed asset demand carries activation-first semantic lineage | format_02_slice_owner | Stub validates demand/response; editor runtime remains external | Asset Demand refs to Visual Semantic Pack, Visual Narrative Program, Composition Asset Pack, and T/V route | Reject semantic mutation, missing provenance, or runtime code | enriched fixture, hash, provenance, and no-editor-code tests | Stub proves typed non-mutation boundary with exact upstream refs | Extends fixtures under ADR-018; no production editor migration |

## Delegation RC4 Reference-Slice Addendum

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Exercise the Format 02 boundary through the exact RC4 candidate without widening Release 1 | format_02_slice_owner | Format 02 proof emits and validates demand and derivative-lock relationship fixtures; Delegation and VAE execution remain external | `DELEGATION_CONTRACT_PIN.yaml`, RC4 Visual Asset Demand 1.1, derivative-lock-inheritance 1.0, wire and lineage mappings | Reject a non-exact pin, missing parent-lock evidence, runtime invocation, semantic loss, or false production eligibility | release-digest, schema, generated-type, lineage, derivative-validator, no-network, and no-local-fork tests | Reference fixtures preserve all mapped lineage and portable lock evidence and record RC4 as unsigned/non-production-eligible | RC1/RC2/RC3 are historical; RC4 does not authorize implementation or alter the 69-Story subset |
| Prevent Format 02 certification leakage into conversational profiles | format_02_slice_owner | Reference-path evidence is scoped only to `2d_character_animation/format02_minimal_coach_theatre` | governed Program Control alias registry, `CATEGORY_PROFILE_COMPATIBILITY.yaml`, and Release 1 subset boundary | Reject unknown aliases or any inherited benchmark, limited-production, or production flag | alias resolution, false-certification, and category/profile matrix tests | Format 02 is a contract-compatible reference profile but not benchmarked or certified; Public Comment, Reply/DM, ReelCast Expression, and Interview Expression remain structural, contract-compatible, and uncertified | Historical `minimal_coach_theatre` is read through the alias registry only; no conversational certification migration is allowed |

## Non-Goals And Migration

This slice does not migrate V2.1, certify every category/target, implement a universal creative engine, or place downstream production behavior in Builder. FR-169 remains deferred until a ratified transfer portfolio exists.
