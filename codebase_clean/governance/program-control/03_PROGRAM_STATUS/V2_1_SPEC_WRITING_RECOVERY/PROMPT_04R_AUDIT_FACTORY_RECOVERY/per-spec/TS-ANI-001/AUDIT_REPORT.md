# Audit Report — TS-ANI-001

**Receipt ID:** CA-P04R-AUDIT-TS-ANI-001-REPORT-2026-07-23
**Spec:** TS-ANI-001 — Source-Grounded Non-Format-02 2D Animation Derivative Runtime
**Product:** Atomic Harness Pipeline
**Batch:** 10
**Issued:** 2026-07-23
**Auditor:** Independent Auditor Controller (not the writer, not the controller)

---

## Outcome: AUDIT_PASS

> AUDIT_PASS does not mean ACCEPTED_FOR_BUILD. The maximum pre-ratification state is TECHNICALLY_ACCEPTED_PENDING_RATIFICATION.

---

## Independence Declaration

The auditor is not the writer of TS-ANI-001 and is not the program controller. No conflict of interest.

---

## Spec Identity

| Field | Value |
|---|---|
| Hash on record | `8bce45fdf570d41a263f5df882d2297ce52fa1fef7615d534c025b1c8cc12ff9` |
| Quality state claimed | `WRITTEN_PENDING_AUDIT` |
| Authority state | `CANDIDATE_NOT_CURRENT` |
| Build authority | `false` |
| Build state | `NOT_BUILD_READY` |
| Format 02 state | `DEFERRED_NOT_ACTIVE` |
| Ceiling | `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION` |
| Writing wave | 12 |

---

## Six-Lens Results

| Lens | Result |
|---|---|
| Lens 1 — FR, Story, and outcome coverage | PASS |
| Lens 2 — Authority, ownership, and sovereignty | PASS |
| Lens 3 — Contract and lifecycle completeness | PASS |
| Lens 4 — Activative, Primitive, archetype, and source fidelity | PASS |
| Lens 5 — Brownfield and cross-spec consistency | PASS |
| Lens 6 — Build readiness and testability | PASS |

**Blocking findings:** 0
**Warnings:** 0
**Notes:** 1

---

## Lens 1 — FR, Story, and Outcome Coverage

**PASS**

TS-ANI-001 controls FR-147 (one source-grounded 2D animation derivative through a separately authorized Harness/runtime without Format 02), FR-148 (exact language and voice transformation labels, attribution, approval, lineage), and ST-05.04 (deny unauthorized cloned voice, trace spoken segments and visual ideas, exact state/decision/handoff/replay/recovery evidence). Section 2.3 provides 10 explicit numbered items mapping directly to all requirements. AC-ANI-001 through AC-ANI-028 all cite FRs/Story explicitly. Section 10.2 provides a trace matrix. No orphaned requirements.

---

## Lens 2 — Authority, Ownership, and Sovereignty

**PASS**

Product sovereignty table (section 3.1) is exhaustive: IE/AIR/Builder/Pipeline/VAE/Delegation/Studio with owned meaning, allowed actions, and prohibitions. Key enforcement points:
- Format 02 exclusion gate: canonical ID `format02_minimal_coach_theatre` plus all governed aliases (registry hash `21ad1a618361...` pinned). All blocked with `Format02ExclusionReceiptV1`. Historical certification does not transfer.
- AIR semantic immutability: section 3.2 — Pipeline compiles execution values only within AIR allowed variation; each derived value records its AIR source ref and derivation rule.
- Deferred external references (HyperFrames/StretchyStudio) correctly handled: `DEFERRED_REFERENCE`, no factual claims attributed, `SOURCE_GAP_NOTICE.yaml` preserves non-blocking gaps.
- Build authority consistently false. Authority state `CANDIDATE_NOT_CURRENT`.

---

## Lens 3 — Contract and Lifecycle Completeness

**PASS**

State machine (section 5.8) covers the complete case lifecycle: REQUESTED → INPUTS_ADMITTED → EXECUTION_PROGRAM_COMPILED → VALIDATED → RENDER_AUTHORIZED → RENDERING → ... → ACCEPTED/REJECTED, plus BLOCKED/CANCELLED/SUPERSEDED/INVALIDATED/REVOKED branches. 26 typed failure codes (section 8.1) with owner, retry class, and correction route for each. Repository invariants (section 6.7): 8-item transaction boundary with bidirectional validation rule. Atomicity, idempotency, CAS, cancellation, replay (section 5.9, 8.2, 8.3). Migration (section 6.8): `MigrationReceiptV1` with `MIGRATION_BLOCKED_MISSING_SEMANTICS` for missing required meaning. Language/voice provenance (`SpokenSegmentProvenanceV1`, section 6.3) complete with enforcement rules for all 5 LanguageTransformationClass values and all 5 VoiceRealizationClass values.

---

## Lens 4 — Activative, Primitive, Archetype, and Source Fidelity

**PASS**

AIR-owned fields (scene purpose, role/tension, Matrix/Edge, transfer, Final Script, Composition Intent, Feature Contracts, Visual Narrative Program) are consumed as immutable references with never-rewritten semantics. AC-ANI-009: "Pipeline creates no replacement semantic value." AC-ANI-010: Composition IR retains source Composition Intent ref, reason, and allowed-variation refs alongside geometry — correctly dual-tracked.

`PerformanceTrackV1` (section 6.4): cue types (POSE, GESTURE, EXPRESSION, GAZE, MOUTH_SHAPE, CAMERA_RELATION, TRANSITION) with source-evidence ref when observed, generated-performance label otherwise. A renderer cannot claim generated performance is the participant's actual reaction. Section 3.4 fully typed `LanguageTransformationClass` and `VoiceRealizationClass` with strict structural and behavioral enforcement rules. `VERBATIM_SOURCE` requires exact normalized text equality to joined source spans.

Identity: `RigRuntimeBindingV1` pins identity, Visual DNA, forbidden controls, continuity constraints, capability profile — strict scope.

---

## Lens 5 — Brownfield and Cross-Spec Consistency

**PASS**

Brownfield disposition (sections 4.2–4.4):
- Historical 2D Character Engine bundle: `ADAPT_AS_REFERENCE` — useful concepts only, PaperCut/Format 02-adjacent doctrine excised
- Studio assembly contracts: `ADAPT`/`REPLACE` — vocabulary preserved, implementation replaced
- Studio Architecture Amendment: required decisions preserved (Format 02 deferred, supervisory Studio, typed correction, HumanResolutionEpisode)

Format 02: canonical ID `format02_minimal_coach_theatre` plus aliases all blocked. Registry hash pinned. AC-ANI-013 tests this. Deferred external references (HyperFrames, StretchyStudio) correctly handled with `DEFERRED_REFERENCE` and `SOURCE_GAP_NOTICE.yaml`.

VAE boundary correct: Pipeline emits Visual Asset Demands, does not select provider/model/LoRA (section 5.4). VAE production acceptance is separate from Pipeline consumption acknowledgement (AC-ANI-016). Interview provenance enforcement (AC-ANI-002): source_kind=interview_expression requires non-empty Reaction Receipt and Expression Moment refs.

---

## Lens 6 — Build Readiness and Testability

**PASS**

Section 10.1: 9 test layers (unit, property, contract, integration, persistence, replay, security, evaluation, architecture). Section 10.2: mandatory fixture set naming 30+ specific fixtures including positive reference slice, archive traversal, offline historical replay bundle. Section 10.3: determinism proof — fresh processes varying TZ/locale/random/hash seed/env/working directory. Section 10.4: 13-item completion evidence package. `format02_state: DEFERRED_NOT_ACTIVE`, `product_adoption_claim: false`, `implementation_created: false`, `development_capsule_created: false` explicitly stated in section 10.5.

---

## Notes

### NOTE-ANI-001-001 — Generated Performance Label Field Not Explicitly Named in Cue Pseudocode

**Lens 4 | Severity: NOTE (implementation design-completion item, not an audit blocker)**

Section 6.4 `PerformanceTrackV1` states cues contain "source-evidence ref when representing observed behavior, generated-performance label otherwise, and lock refs." Section 3.4 further requires `GENERATED_PERFORMANCE` labeling unless a cue is a direct source-timed representation. AC-ANI-008 tests this requirement.

The pseudocode description of the cue object does not explicitly name the generated-performance label as a typed enum/boolean field. The behavioral requirement is stated clearly, and the validation AC and failure mode are specified. This is not a blocking finding.

Implementors must ensure an explicit typed field (e.g., `performance_truth_class: OBSERVED_SOURCE | GENERATED_PERFORMANCE`) is present in the cue schema and that its absence or incorrect value fails validation before render authorization. This field should be added at the implementation/schema design stage.

---

## Upstream Draft Dependencies

| Spec | Hash Pinned | Status | Revision Impact |
|---|---|---|---|
| TS-AHP-003 | `072041914b...` | `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Reopen all 6 impact sections |
| TS-AIR-015 | `58946bef28...` | `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Reopen all 6 impact sections |
| TS-AIR-017 | `0e87466a32...` | `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Reopen all 6 impact sections |

---

*The next lifecycle action for TS-ANI-001 is: program-controller ratification of this AUDIT_PASS result. ACCEPTED_FOR_BUILD and Development Capsule are not issued here.*
