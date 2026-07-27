---
title: "CMF TS-CMF-106 Video Edit Program Audit and Revision"
status: "revised"
created_at: "2026-06-25"
auditor_role: "Principal CCP Architecture Reviewer"
reviser_role: "Principal CCP Architecture Reviser"
scope:
  - "TS-CMF-106-video-edit-program-compiler-otio-and-render-runtime.md"
protocols:
  - "THE CMF STUDIO/docs/architecture/april_updates/TRIGGER_COMMAND_AUDIT.md"
  - "THE CMF STUDIO/docs/architecture/april_updates/PROMPT_Spec_Audit.md"
  - "THE CMF STUDIO/docs/architecture/april_updates/TRIGGER_COMMAND_REVISION.md"
  - "THE CMF STUDIO/docs/architecture/april_updates/PROMPT_Spec_Revision.md"
  - "THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md"
---

# CMF TS-CMF-106 Video Edit Program Audit and Revision

## 1. Audit Scope

This audit reviews `TS-CMF-106-video-edit-program-compiler-otio-and-render-runtime.md`, the parent video editing compiler spec created to fill the reserved TS-CMF-106 slot. The goal is to verify whether the spec can safely guide implementation of the interview-first `VideoEditProgram` without falling into generic video-template assembly, fuzzy primitive references, weak gate thresholds, or untraceable render state.

## 2. Sources Loaded

| Source | Use |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/PROMPT_Spec_Audit.md` | Five-lens audit protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/PROMPT_Spec_Revision.md` | Section-targeted revision protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Required 10-section tech spec shape and backend integration expectations. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Phase 4 CBAR mandates: intelligence-gated intercept, cinematic meaning, inline routing, frictionless block, actionable rejection. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Phase 5 CBAR mandates: verifiable artifact and earned escalation. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Exact primitive IDs, route roles, thresholds, evidence requirements, and hard failures. |
| `THE CMF STUDIO/docs/audits/CMF_VIDEO_EDITING_ENGINE_MCDA_2026-06-24.md` | Identifies the missing `VideoEditProgram` abstraction and TS-CMF-106 target. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-106-video-edit-program-compiler-otio-and-render-runtime.md` | Audited target. |

## 3. Executive Verdict

The spec was directionally correct and filled the intended architectural gap, but it was not yet ERA3-hard enough for implementation. The main issue was not scope. The issue was auditability: primitive requirements were partly expressed as readable labels instead of exact registry IDs, gate thresholds were not fully numeric, receipt writes were implied rather than stage-specific, and the schema still allowed loose primitive strings.

Revision has been applied. The spec is now build-ready at documentation level, pending implementation.

## 4. PASS

No zero-flag pass before revision.

## 5. FLAGS

**[TS-CMF-106] | LENS 2 | SEVERITY: CRITICAL**
- **Finding:** The ADR-05 primitive table used descriptive labels such as narrative pressure, concept compression, edge integrity, and reaction timing instead of exact YAML primitive IDs.
- **Location:** Section 3, `ADR-05 Primitives`.
- **Required Action:** Replace fuzzy labels with exact route-specific primitive IDs, roles, registry refs, and thresholds from `CMF-COMP-PRIMITIVE-TRIADS-001`.
- **Revision Applied:** Yes. The spec now lists exact minimum primitive triads for `SV-CSC`, `SV-EDU`, `SV-FRB`, and `SV-RRC`.

**[TS-CMF-106] | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** Video edit eval gates existed as concepts, but several gates lacked exact numeric thresholds and deterministic verdict semantics.
- **Location:** Section 3, `CBAR Mandate Enforcement`; Section 8, Acceptance Criteria; Section 10, Testing Strategy.
- **Required Action:** Add a gate threshold and verdict matrix with `PASS`, `PROVISIONAL`, `FAIL`, and `BLOCKED` semantics, numeric thresholds, blocker codes, and receipt fields.
- **Revision Applied:** Yes. The spec now includes a full gate matrix for source timing, brand scope, format route, format feel, primitive triad, doctrine, masks, captions, audio, generated asset drift, OTIO coverage, and approval.

**[TS-CMF-106] | LENS 4 + LENS 5 | SEVERITY: CRITICAL**
- **Finding:** Receipt objects were named, but state-changing pipeline stages did not specify exact Receipt Chain Guard writes, idempotency keys, or emitted domain events.
- **Location:** Section 4, Implementation Plan; Section 5, `VideoEditProgramReceipt`.
- **Required Action:** Add a pipeline transformation and receipt chain guard matrix covering draft create, source load, format compile, transcript clock compile, scene/layer compile, provider plan, proxy render, eval, review, final render, OTIO export, and package handoff.
- **Revision Applied:** Yes. Section 4 now defines the stage input, transformation, output, receipt action, idempotency key, and event requirement.

**[TS-CMF-106] | LENS 1 | SEVERITY: WARNING**
- **Finding:** The implementation plan listed steps but did not provide a full input-to-transform-to-output map for every pipeline stage.
- **Location:** Section 4, Implementation Plan.
- **Required Action:** Add a transformation matrix that makes each pipeline stage executable and auditable.
- **Revision Applied:** Yes. The new `Pipeline Transformation and Receipt Chain Guard` matrix resolves this.

**[TS-CMF-106] | LENS 2 + LENS 5 | SEVERITY: WARNING**
- **Finding:** The primary schema and sample JSON used `primitive_triads: list[str]` and example strings such as `human_proof`, `recognition_timing`, and `participatory_cue`, which contradicted the registry requirement for exact primitive IDs and role coverage.
- **Location:** Section 5, `FormatCompositionContract`; Section 5, `Format Composition JSON Requirements`.
- **Required Action:** Replace loose primitive strings with role-aware primitive validation objects carrying `primitive_id`, `primitive_name`, `role`, `registry_ref`, `minimum_score`, `evidence_ref`, `composition_element_ref`, and verdict.
- **Revision Applied:** Yes. The schema now defines `PrimitiveValidationRef`, `VideoEditGateVerdict`, and `VideoEditReceiptChainWrite`; the JSON example now uses exact `PRM-PSY-001`, `PRM-REF-009`, and `PRM-VSG-015` route primitives.

## 6. Revision Log

| Target | Revision |
|---|---|
| Section 1 | Added audit/revision prompts, Phase 4/5 epic files, and primitive triad registry to `Files Read`. |
| Section 3 | Replaced fuzzy primitive coverage labels with exact route primitive IDs and thresholds. |
| Section 3 | Added primitive verdict semantics. |
| Section 3 | Added numeric gate threshold and verdict matrix. |
| Section 4 | Added pipeline transformation and receipt chain guard matrix. |
| Section 5 | Added `PrimitiveValidationRef`, `VideoEditGateVerdict`, and `VideoEditReceiptChainWrite`. |
| Section 5 | Replaced `primitive_triads: list[str]` with `primitive_validations: list[PrimitiveValidationRef]`. |
| Section 5 | Updated sample format JSON to exact primitive validation objects. |
| Section 8 | Tightened acceptance criteria for primitive IDs, caption thresholds, audio thresholds, generated asset drift, OTIO coverage, and receipts. |
| Section 10 | Added tests for route primitive registry thresholds, gate verdict receipts, idempotent receipt writes, 100% OTIO coverage, and per-stage receipt writes. |

## 7. Summary Statistics

| Metric | Count |
|---|---:|
| Specs reviewed | 1 |
| Specs with zero flags before revision | 0 |
| Critical findings | 3 |
| Warning findings | 2 |
| Notes | 0 |
| Critical findings revised | 3 |
| Warning findings revised | 2 |
| DEP/primitive integrity issues repaired | 2 |
| Gate threshold issues repaired | 1 |
| Receipt chain issues repaired | 1 |

## 8. Residual Risk

The spec is now ready for implementation, but implementation must still create the actual Python contracts, registries, services, API routes, OTIO exporter, tests, and review UI bindings. The audit did not execute code because TS-CMF-106 is currently a specification document.
