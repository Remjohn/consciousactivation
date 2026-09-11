# M0082 — Editorial Expression Calculus

**Status:** IMPLEMENTED — OPERATOR REVIEW REQUIRED
**Claim classes used:** `EXECUTABLE`, `SCHEMA`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, `OPERATOR_DECISION_REQUIRED`

## 1. Brownfield decision

M0079 already owns the canonical editable storyboard projection and the typed downstream chain:

`TransformationIntent → TransformationRecipe → MotionPlan`.

M0080 already owns deterministic format-specific storyboard program contracts for VIDEO, CAROUSEL, SUPERVISUAL and PRESENTATION.

M0082 therefore adds one pure CAE runtime calculator and does **not** create a second storyboard, semantic-program, retrieval, asset-rights, format-program, VAE, or state authority.

**Evidence class:** `SCHEMA` / `DOCUMENT`.

## 2. Implemented boundary

The implementation lives at:

`packages/ca_runtime/src/ca_runtime/editorial_expression_calculus.py`

It accepts a bounded `NarrativeEditingGrammar` and returns a frozen `EditorialExpression` containing:

- pace (`pace_bps`);
- shot duration (`shot_duration_ms`);
- hold duration (`hold_duration_ms`);
- cut interval (`cut_interval_ms`);
- occupancy (`occupancy_bps`);
- scale (`scale_bps`, where 10000 = 1.0x reference scale);
- motion amplitude (`motion_amplitude_bps`);
- motion velocity (`motion_velocity_bps_per_second`);
- visual density (`visual_density_bps`);
- caption density (`caption_density_bps`);
- contrast (`contrast_bps`);
- salience (`salience_bps`);
- intervention frequency (`intervention_frequency_per_minute`).

No persistence, retrieval, rendering, model invocation, provider call, operator promotion, or canonical state mutation occurs here.

**Evidence class:** `EXECUTABLE`.

## 3. Narrative editing grammar input

The input vocabulary is deliberately editorial/structural rather than semantic:

| Dimension | Bounded vocabulary |
|---|---|
| rhythm | `HOLD`, `STEADY`, `PUNCTUATED`, `ACCELERATE` |
| attention | `QUIET`, `FOCUS`, `EMPHATIC`, `INTERRUPT` |
| information | `WITHHOLD`, `REVEAL`, `PROVE`, `CONNECT`, `RESOLVE` |
| texture | `CLEAN`, `LAYERED`, `DENSE` |
| captioning | `NONE`, `SPARSE`, `SUPPORTIVE`, `EXPLANATORY` |

Every input also requires a supported CAE format, scene kind, non-empty unique evidence references, and a source-quality floor of `AUDITED`, `HIGH`, or `VERIFIED`.

**Evidence class:** `SCHEMA`.

## 4. Format / scene bounds

The profile registry is a deterministic 4 × 6 matrix produced from one bounded format base plus one bounded scene bias. Supported combinations are:

- VIDEO × OPENING / EXPOSITION / EVIDENCE / PIVOT / CLIMAX / RESOLUTION
- CAROUSEL × the same six scene kinds
- SUPERVISUAL × the same six scene kinds
- PRESENTATION × the same six scene kinds

Profiles are represented by ids such as `M0082:VIDEO:EVIDENCE`.

These profiles are calibration bounds, not format semantics. M0080 remains the canonical format grammar authority.

**Evidence class:** `SCHEMA` / `HYPOTHESIS`.

## 5. Deterministic mapping

All arithmetic uses integers and fixed-point basis points; floating-point values are not used.

The compiler:

1. starts from the format base values;
2. applies a bounded scene bias;
3. applies deterministic deltas for each grammar dimension;
4. clamps each result to the selected profile range;
5. derives shot duration inversely from `pace_bps` using integer interpolation;
6. derives hold duration from inverse pace plus the explicit hold bias;
7. sets cut interval equal to the computed shot duration;
8. derives motion velocity as integer amplitude-per-second and clamps it to the profile range;
9. hashes the canonical output with the existing `ca_contracts.canonical_sha256` function.

The output digest is therefore a replay fingerprint for the same input and profile.

**Evidence class:** `EXECUTABLE` / `SCHEMA`.

## 6. Tuning status

The numeric profile bounds and grammar deltas are initial deterministic tuning constants. No supplied mandatory authority-pack file containing an approved quantitative calibration table was available in the uploaded snapshot. Consequently these constants are **not** represented as constitutional or perceptual truth.

They are explicitly classified as `HYPOTHESIS` until operator/perceptual evaluation establishes acceptable ranges and tradeoffs.

The calculus is intended to provide an executable contract for a later calibration pass without requiring a redesign of the domain model.

**Evidence class:** `HYPOTHESIS` / `OPERATOR_DECISION_REQUIRED`.

## 7. Evidence and false-proof defenses

Focused tests at `tests/cae/test_m0082_editorial_expression_calculus.py` establish:

- a normal evidence-grounded success case;
- deterministic replay (`compile(input) == compile(input)` and equal digest);
- deterministic format/scene profile selection;
- source-quality rejection for `UNKNOWN`, `LOW`, and `UNVERIFIED` inputs;
- rejection of missing and duplicate evidence references;
- rejection of unsupported profile keys;
- a contrastive `ACCELERATE` case that changes pace/duration/motion while remaining bounded.

A green local focused suite proves the pure calculator and its schema behavior only. It does not prove native visual-runtime reachability, perceptual quality, semantic correctness of a resulting visual edit, or operator promotion.

**Evidence class:** `TEST` / `OPERATOR_DECISION_REQUIRED`.

## 8. External-source boundary

No external repository behavior was copied or vendored for M0082. No external runtime is invoked. Therefore there is no adopted upstream source commit/license claim for the implementation.

Existing CAE reference evidence from M0078 was used only as brownfield context: camera/timing language remains downstream of semantic meaning and deterministic code remains responsible for bounded execution. The exact external source files named in M0078 were not re-adopted into M0082.

**Evidence class:** `DOCUMENT` / `REGISTRY_SOURCE` (historical reference only).

## 9. Mandatory-source limitation

The following literal mandatory paths from the M0082 mandate were not present in the supplied snapshot:

- `docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md`
- `governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`
- `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/00_REPOSITORY_TO_PRODUCT_BUILD_PLAN.md`
- `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/01_CAE_Product_Update_Visual_Asset_Editor.md`
- `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/02_CAE_PRD_Update_Visual_Asset_Studio.md`
- `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/03_CONSCIOUS_E_MOTION_EDITING_STANDARDS_v2.md`

For constitutional review, the current governed equivalents under `governance/program-control/00_CONSTITUTION/current-v1.1/` were inspected. M0079/M0080 brownfield artifacts were also inspected. The exact dated Visual Production Authority Pack was not available in this snapshot and is therefore not claimed as read.

Per M0082 stop conditions, this remains an `OPERATOR_DECISION_REQUIRED` limitation.

## 10. Downstream handoff

Preferred future composition path remains:

`Editorial Intent → Narrative Editing Grammar → Editorial Expression Calculus → TransformationIntent → TransformationRecipe → primitives/keyframes`

The output should be treated as bounded quantitative input to a later deterministic transformer. It must not become a semantic authority, approval record, or runtime provider contract.

**Evidence class:** `DOCUMENT`.
