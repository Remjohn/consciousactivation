# M0084 Agent Handoff — Evidence-First Source Quality and Adaptive Transformation Rules

**Status:** IMPLEMENTED — OPERATOR REVIEW REQUIRED
**Mandate:** M0084
**Implementation commit:** `b9e332d677739e833412cca5d5d0839b6267e34c`
**Source archive SHA-256:** `7f962c86b13171cc25bec698d6974d412981cef502e858717b5069e50f1810d8`

## 1. Decision implemented

The canonical CAE storyboard transformation path now carries an additive `SourceQualityProfile` and deterministic adaptive transformation rules. The implementation extends the existing `VisualAssetReference → TransformationIntent → TransformationRecipe` lineage; it does not introduce a second asset, storyboard, retrieval, or semantic authority.

Measured profile inputs are source resolution, frame rate, crop history, compression loss, sharpness, prior degradation, and evidence references. The profile derives deterministic quality bands `HIGH`, `MEDIUM`, `LOW`, and `DEGRADED`. Quality bands bound declared scale/reframe/motion magnitude and allowed color treatments, while also recommending safer presentation strategies for degraded evidence.

The adaptive projection preserves `TransformationIntent.intent_id`, semantic constraints, source-quality profile identity, and evidence references. Revision validation rejects source/profile rebinding, evidence lineage drift, and recipes that exceed quality limits. Sensitive primitives fail closed when they omit the magnitude field needed for deterministic validation.

## 2. Authority mapping

The user-authorized official visual-production authority pack is the live repository directory `docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/` with the four files named by M0084. The pack is campaign input; repository Constitution, precedence, existing programs, schemas, and implementation remain the governing repository authorities.

The live repository's canonical constitutional sources are:

- `governance/program-control/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md`
- `governance/program-control/00_CONSTITUTION/current-v1.1/governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`

The authority-pack build plan requires `SourceQualityProfile`, measurable resolution/crop/compression/sharpness/frame-rate metadata, and automatic reduction of aggressive zoom/reframe/motion where source quality would make manipulation visible. The Visual Asset Editor update requires deterministic validation/clamping of model proposals and explicitly gives high-quality sources more latitude than low/degraded sources. The E-Motion standard places source-quality-aware transformation downstream of editorial intent and within deterministic bounds.

## 3. Brownfield reusable objects

- `packages/ca_runtime/src/ca_runtime/storyboard_session.py::TransformationIntent`
- `packages/ca_runtime/src/ca_runtime/storyboard_session.py::TransformationRecipe`
- `packages/ca_runtime/src/ca_runtime/storyboard_session.py::VisualAssetReference`
- `packages/ca_runtime/src/ca_runtime/storyboard_session.py::StoryboardElement`
- `packages/ca_runtime/src/ca_runtime/storyboard_session.py::StoryboardSessionStore._validate_revision_input`
- `services/pipeline/contracts/schemas/transformation_contract.schema.json`

No duplicate transformation authority or source-retrieval system was introduced.

## 4. Exact changed/new repository paths

### Modified

- `packages/ca_runtime/src/ca_runtime/storyboard_session.py`
- `packages/ca_runtime/src/ca_runtime/__init__.py`

### Added

- `tests/cae/test_m0084_source_quality_profile.py`
- `docs/cae/specs/M0084/source_quality_profile.md`
- `docs/cae/specs/M0084/AGENT_HANDOFF.md`
- `docs/cae/specs/M0084/M0084_EVIDENCE_RECEIPT.json`

No files outside the M0084 allowed boundary were changed.

## 5. Implementation rationale

`SourceQualityProfile` is additive on `VisualAssetReference`, preserving compatibility with historic records that lack the structured profile. Quality scoring uses fixed-point basis points so the new policy does not introduce floating-point ambiguity into canonical payloads.

The deterministic limits are M0084 implementation policy, not universal perceptual constants:

| Quality | Scale | Reframe | Motion | Color |
|---|---:|---:|---:|---|
| HIGH | 1200 bps | 1200 bps | 1200 bps | NONE / CONTROLLED / SUBTLE_LUT |
| MEDIUM | 800 bps | 800 bps | 700 bps | NONE / CONTROLLED |
| LOW | 400 bps | 400 bps | 300 bps | NONE / GRAYSCALE / CONTROLLED |
| DEGRADED | 150 bps | 200 bps | 0 bps | NONE / GRAYSCALE |

The safe presentation recommendation moves from standard/subtle treatment at HIGH toward reduced-scale, inset, contextual, grayscale, and containerized strategies as quality deteriorates.

## 6. Verification commands and observed results

### Focused M0084 tests

```text
PYTHONPATH=packages/ca_contracts/src pytest -q tests/cae/test_m0084_source_quality_profile.py
```

Observed:

```text
9 passed, 5 warnings in 0.10s
```

The five warnings are existing Pydantic V1-style `@validator` deprecation warnings in unrelated pre-existing validators in the same module; no M0084 validator uses the deprecated form.

### Native regression collection

```text
pytest -q tests/cae/test_m0079_storyboard_session_revision.py tests/cae/test_m0080_storyboard_program_contracts.py tests/cae/test_visual_derivative_production_program.py
```

Observed: collection is blocked in this environment by:

```text
ModuleNotFoundError: No module named 'psycopg'
```

This is an environment/setup limitation. It is not substituted with a mock and is not represented as native runtime proof.

### Syntax validation

```text
python -m py_compile packages/ca_runtime/src/ca_runtime/storyboard_session.py packages/ca_runtime/src/ca_runtime/__init__.py
```

Observed: success, no output.

### Diff integrity

```text
git diff --check
```

Observed: success, no whitespace errors.

## 7. Test properties established

- HIGH-quality 4K source accepts bounded subtle zoom/reframe/color treatment.
- A plausible but wrong-looking-good 480p/pre-cropped/compressed source with aggressive zoom is rejected.
- DEGRADED adaptation is deterministic and preserves intent and evidence lineage.
- Structured source-quality metadata rejects malformed dimensions/quality ranges and missing evidence.
- A quality profile cannot be rebound to another asset.
- A source-quality profile lowers the quality band as crop retention, compression, sharpness, frame rate, and prior degradation worsen.
- Sensitive `ZOOM` primitives cannot bypass validation by omitting intensity metadata.
- `StoryboardSessionStore._validate_revision_input` rejects quality-damaging recipes through the existing revision gate.

## 8. Evidence classification

- **EXECUTABLE:** implementation in `packages/ca_runtime/src/ca_runtime/storyboard_session.py`.
- **SCHEMA:** `SourceQualityProfile` / `TransformationValidationResult` Pydantic models and additive `VisualAssetReference` field.
- **DOCUMENT:** `docs/cae/specs/M0084/source_quality_profile.md` and repository/authority documentation.
- **TEST:** `tests/cae/test_m0084_source_quality_profile.py`; 9 focused tests pass.
- **HYPOTHESIS:** thresholds are deterministic product policy and still require perceptual/operator validation; they are not claimed as universal psychovisual limits.
- **OPERATOR_DECISION_REQUIRED:** visual preview, semantic adequacy, source lineage, and production runtime reachability remain human/environment checks.
- **MIGRATION:** none.
- **REGISTRY_SOURCE:** none.

## 9. External source information

No external repository code was adopted or extracted. No external implementation license applies to this change.

The live GitHub main reference observed during audit is commit `1238dda04cc89e16ed7ac96ac79417c7c321f8a8`. The supplied archive itself contained no `.git`, so this remote SHA is context only, not archive provenance.

## 10. Limitations / acceptance ceiling

The focused unit suite proves deterministic source-quality logic and the existing storyboard validation path under an isolated module-loading harness. It does not prove native DB-backed runtime reachability because `psycopg` is unavailable in the supplied environment.

No visual preview was available for operator inspection during this execution. Therefore visual perceptual acceptance, semantic fitness of each transformed asset, and absence of gratuitous attention remain explicitly unproven until an operator reviews real previews and source lineage.

Quality thresholds are bounded policy, not a substitute for human creative judgment. A profile absent from a legacy asset remains an intentional compatibility path; such an asset does not receive the new quality-aware gate until a profile is attached.

## 11. Commit identity

Baseline snapshot commit representing the supplied archive:

`fa1ed7c895306846e563550f7d2a58adab9c99ec`

M0084 implementation commit:

`b9e332d677739e833412cca5d5d0839b6267e34c`


## 12. Operator decision requested

Review the implementation, focused evidence, and limitations, then select exactly one:

`APPROVE`
`APPROVE-WITH-LIMITATIONS`
`REJECT`

Do not self-promote. For visual output, operator review must confirm the real preview, meaning-preserving transformation, and source lineage. For any later external-runtime integration, operator review must confirm the runtime remains downstream of CAE authority and replaceable.
