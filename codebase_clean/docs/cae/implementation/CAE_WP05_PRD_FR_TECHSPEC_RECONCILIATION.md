# CAE WP-05 PRD / FR / Tech-Spec Reconciliation

**Work package:** WP-05 — PRD / FR / Tech-Spec reconciliation
**Status:** `COMPLETE_PENDING_OPERATOR_REVIEW`
**Date:** 2026-08-24
**Boundary:** requirements/specification reconciliation only. No service, staging
schema, source registry, or operational record changed.

## Authority ordering

1. Runtime repository and staging proof establish current behavior.
2. Immutable SDA/SFL/Primitive snapshots establish inherited registry facts.
3. CAE governance establishes target architecture.
4. Phase 5–7 PRD/FR documents are target requirements, not current-runtime proof.
5. `docs/PRD/CURRENT.md` was read as user-maintained brownfield context and is
   not rewritten by this package.

## Reconciled requirement register

`IMPLEMENTED_SLICE` is narrower than whole-Phase delivery. `SPECIFIED` has a
defined later contract but cannot enter implementation yet. `DEFERRED` has no
adequate current authority or integration boundary.

| Requirement | Classification | Evidence / disposition |
|---|---|---|
| FR-P05-01 Interview Brief Compiler | DEFERRED | No canonical ActivationEvent or brief contract in staging. |
| FR-P05-02 Question Grammar Registry | DEFERRED | No supplied registry authority. |
| FR-P05-03 Sequential Interview Planner | DEFERRED | Interview Composer plans local payloads; no CAE query surface. |
| FR-P05-04 Human Response Capture | PARTIAL | Interview Expression stores local sources; WP-03 captures only verified spans. |
| FR-P05-05 Evidence Span Extraction | IMPLEMENTED_SLICE | `cae.evidence.capture@1.0.0`. |
| FR-P05-06 Evidence Assessment | DEFERRED | No assessment metric/validator. |
| FR-P05-07 Authentication Decision Engine | IMPLEMENTED_SLICE | `cae.evidence.authenticate@1.0.0` requires a distinct evaluator. |
| FR-P05-08 Dynamic Replanning | DEFERRED | Requires planner and session-state authority. |
| FR-P05-09 Anti-Leading Patrol | SPECIFIED | Required before canonical question issuance; no evaluator exists. |
| FR-P05-10 Anti-Centroid Patrol | SPECIFIED | No Phase-5 evaluator; SFL corpus is only partial input. |
| FR-P05-11 Semantic Evidence Packet Compiler | PARTIAL | Interview Expression has local read-only pack; CAE adapter absent. |
| FR-P05-12 Interview Receipt Service | IMPLEMENTED_SLICE | WP-03 envelope, not full session receipt. |
| FR-P05-13 Authorized Retrieval Functions | DEFERRED | No approved planning SQL view/function. |
| FR-P05-14 Error Taxonomy and Repair | SPECIFIED | Error terms reconciled; repair router absent. |
| FR-P05-15 Brownfield Adapter Layer | SPECIFIED | Must preserve Interview Expression ownership/read-only AIR handoff. |
| FR-P05-16 Human Operator Review Surface | DEFERRED | Confirmation exists; review surface does not. |
| FR-P06-01 Semantic Field Assembly | DEFERRED | Needs authenticated evidence plus validated SDA runtime packet. |
| FR-P06-02 Primitive Eligibility Retrieval | PARTIAL | Pinned resolver reads non-quarantined records; no eligibility policy. |
| FR-P06-03 Candidate Generation | DEFERRED | No candidate schema/operation. |
| FR-P06-04 Candidate Assessment | DEFERRED | No evaluator/calibration proof. |
| FR-P06-05 Candidate Rejection Logging | DEFERRED | No candidate state/error route. |
| FR-P06-06 Compatibility Evaluation | DEFERRED | No verified compatibility source/validator. |
| FR-P06-07 Coalition Formation | DEFERRED | No coalition contract. |
| FR-P06-08 Coalition Validation | DEFERRED | No geometry/range/routeability validator. |
| FR-P06-09 Edge Product Derivation | DEFERRED | No edge-product contract. |
| FR-P06-10 Edge Distinctiveness | DEFERRED | No benchmark memory/evaluator. |
| FR-P06-11 Anti-Centroid Patrol | DEFERRED | Needs candidate/coalition corpus/evaluator. |
| FR-P06-12 Hard-Negative Evaluation | SPECIFIED | SFL failures cannot substitute for Phase-6 semantic negatives. |
| FR-P06-13 Receipt Generation | DEFERRED | WP-03 receipts are infrastructure, not coalition receipts. |
| FR-P06-14 Controlled Agent Query Surface | PARTIAL | Registry resolver is pinned/read-only; no Phase-6 program. |
| FR-P06-15 Error Taxonomy Routing | DEFERRED | No candidate/coalition error router. |
| FR-P06-16 Registry-Gap Escalation | SPECIFIED | Issue ledger exists; no primitive may be invented inline. |
| FR-P06-17 Benchmark Memory | DEFERRED | No outcome model or retention policy. |
| FR-P06-18 Brownfield Adapter | SPECIFIED | AIR local registry remains separate. |
| FR-07-01 Archetype Registry Consumption | DEFERRED | AIR archetypes not reconciled into CAE authority. |
| FR-07-02 Archetype Eligibility | DEFERRED | No structural eligibility contract. |
| FR-07-03 Archetype Selection | DEFERRED | No alternatives/evaluator ledger. |
| FR-07-04 SFL Canonical Registry | PARTIAL | Versioned snapshot imported; five affected failure assets quarantined. |
| FR-07-05 SFL Runtime Stack | DEFERRED | Registry presence does not authorize a stack. |
| FR-07-06 Influence Alignment | DEFERRED | No alignment policy/validator. |
| FR-07-07 Composition Depth | DEFERRED | No depth profile contract. |
| FR-07-08 Director Note Compilation | DEFERRED | No canonical grammar/parser. |
| FR-07-09 Semantic Program | DEFERRED | No schema/operation/consumer. |
| FR-07-10 Anti-Centroid Patrol | DEFERRED | Corpus cannot alone prove taste. |
| FR-07-11 Typed Errors | SPECIFIED | Bind only with a real Phase-7 operation. |
| FR-07-12 Receipts | DEFERRED | WP-03 envelopes are not Phase-7 semantics. |
| FR-07-13 Brownfield Compatibility | PARTIAL | Registry lineage preserved; no AIR cutover. |
| FR-07-14 Phase Boundary Enforcement | SPECIFIED | SemanticProgram must prohibit renderer instructions. |
| FR-07-15 Human Auditability | DEFERRED | No review UI/receipt inspector. |

## Object-to-runtime trace matrix

| Object / contract | Schema | State/event | FR | Tech Spec | Code/data | Test/proof | Receipt/outcome |
|---|---|---|---|---|---|---|---|
| Verified source asset | media/source tables | STC-EVID-000 precondition | P05-04/05 | TS-CAE-EVID-001 | WP-02/03 | WP-03 | receipt; outcome N/A |
| Evidence/authentication | evidence tables | STC-EVID-000/001 | P05-05/07/12 | TS-CAE-EVID-001 | WP-03 adapter | WP-03 | receipt; human truth not proven |
| AIR assessment lifecycle | assessment/link tables | STC-AIR-000/001/002 | P05-11/P06 input | TS-CAE-EVID-001 | WP-03 adapter | WP-03 | direction not proven |
| SDA records/crosswalks | registry tables | immutable | P06-01/02 | future TS-CAE-REG-001 | WP-04 resolver | WP-04 | import run; N/A |
| SFL records/failure assets | registry tables | immutable/quarantine | P07-04/10 | future TS-CAE-REG-001 | WP-04 resolver | WP-04 | perceptual claim not proven |
| Primitive definitions | registry tables | immutable/quarantine | P06-02/16 | future TS-CAE-REG-001 | WP-04 resolver | WP-04 | eligibility not proven |
| Candidate/Coalition/Edge | MISSING | MISSING | P06-03–13 | MISSING | MISSING | MISSING | MISSING |
| Archetype/SFL Stack/Semantic Program | MISSING | MISSING | P07-01–15 | MISSING | local AIR-adjacent only | MISSING | MISSING |

## Binding contradictions and decisions

| ID | Reconciled fact | Decision |
|---|---|---|
| SPEC-001 | Phase 5 calls its PRD “Draft Source of Truth,” but governance requires reconciliation first. | Requirements only, not implementation authority. |
| SPEC-002 | WP-03 assessment validation proves lifecycle/evidence gating, not registry-derived semantic direction. | Keep it registry-neutral until a later AIR/registry adapter package. |
| SPEC-003 | SFL failures target absent `SFL-FAM-005`, `SFL-FAM-006`, `SFL-FAM-007`, `SFL-FAM-009`, and `SFL-FAM-012`. | Quarantine; do not use at runtime or invent records. |
| SPEC-004 | AIR local primitive/archetype data overlaps CAE registry concepts; `EXP-TRG-001` is duplicate/ambiguous. | No merge/cutover; decide an explicit authority adapter later. |
| SPEC-005 | `CURRENT.md` is user-maintained and changed. | Preserve it; CAE docs carry reconciliation authority. |

## WP-05 outcome and next gate

`TS-CAE-EVID-001` is the only bounded implementation-ready contract here; it
is staging-proven but still needs a later API/Interview Expression bridge
package. Phase 6 and 7 are not ready for development.

## Operator gate

**A. What changed:** all 49 Phase 5–7 FRs now have an explicit readiness
classification, an object trace matrix, five contradiction dispositions, and a
14-section first-slice Tech Spec.

**B. Why:** the phase documents describe valuable target behavior but previously
could be mistaken for runtime capability or a license to merge local AIR data.

**C. What was proven:** WP-03 has a real staging evidence lifecycle; WP-04 has
an immutable registry/resolver boundary; all reconciled claims reference those
facts or are explicitly deferred.

**D. What was not proven:** a complete interview compiler, Phase-6 candidate
compiler, Phase-7 stack/program compiler, operator UI, service adapter,
semantic quality, or real-world outcome.

**E–F. Uncertainty / what could still be wrong:** the local AIR and Interview
objects may have additional compatible capabilities that need a later dedicated
adapter audit. Registry lineage defects and the actual accountable source owner
remain unresolved.

**G. Inspect:** the classifications for P05-09/10/13/16, P06-01 through 18,
P07-01 through 15, the `SPEC-001`–`SPEC-005` decisions, and the explicit E3/E4
boundary in `TS-CAE-EVID-001`.

**Exact decision required:** **Promote WP-05 and authorize WP-06 to design the
Harness / Skills / Runbook integration around this bounded slice, without
exposing quarantined registry records or redirecting legacy authority?**
