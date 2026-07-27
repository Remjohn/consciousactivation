# BD-007 Visual Baseline Scope Audit

Date: 2026-07-16  
Lane: `BD007_VISUAL_BASELINE_AGENT`  
Audit scope: `ST-06.01 / Bind Every Harness to One of Five Canonical Categories`

## Verdict

For the exact structural, uncertified branch of ST-06.01, BD-007 is:

`SCOPED_NOT_APPLICABLE_TO_STRUCTURAL_UNCERTIFIED_BRANCH`

This disposition does not close BD-007 globally. Provider comparison, empirical
Visual Syntax quality, benchmark thresholds, production-provider selection and
production certification remain open.

## Authority finding

The current authority separates category identity from empirical syntax parsing:

- FR-137 through FR-141 and the ST-06.01 Story contract require the Shared Activative
  Core, exactly five stable category identities, versioned constitutions and one
  category binding per applicable Harness.
- FR-145 through FR-147, owned by later category-native work, require actual
  category-specific parsing and sequencing.
- ADR-008 requires at least two adapter-compatible providers plus the deterministic
  baseline on protected Format 02 cases before a production provider is selected.
- The accepted architecture explicitly authorizes provider-neutral boundaries and
  prototype fixtures while leaving production visual parsing blocked.
- The Format 02 reference-validation track records BD-007 as a Track B entry gate;
  it is not a prerequisite for the already completed category-neutral Builder Core.

Therefore a registry operation that binds an immutable Harness to one canonical
category does not intrinsically invoke a provider, parse a specimen, compare model
quality or establish a benchmark threshold. Requiring provider results at this seam
would confuse structural category conformance with later empirical behavior.

## Scope separation

| BD-007 sub-scope | Evidence state | ST-06.01 effect | Governed disposition |
|---|---|---|---|
| Structural Visual Syntax contract | Existing authority defines Visual Syntax First, category isolation, category-native applicability and the five category IDs | Required; sufficient for structural validation | `CLOSED_PASS_BY_EXISTING_AUTHORITY` |
| Structural category syntax descriptors | Existing requirements distinguish spatial, temporal, reading-order and conversational applicability without asserting measured quality | Required; sufficient as contract descriptors only | `CLOSED_PASS_BY_EXISTING_AUTHORITY` |
| Development-time empirical baseline | No governed provider run or protected real-profile result was found | Not invoked by category identity binding | `SCOPED_NOT_APPLICABLE_TO_STRUCTURAL_UNCERTIFIED_BRANCH` |
| Provider comparison | No comparison of two adapter-compatible providers plus deterministic baseline was found | Not invoked by category identity binding | `REMAINS_BLOCKED_EXTERNAL_EVIDENCE` |
| Benchmark thresholds | No ratified Visual Syntax production threshold was found | Not invoked and no threshold may be claimed | `REMAINS_BLOCKED_EXTERNAL_EVIDENCE` |
| Production-provider selection | No provider has passed the required protected Format 02 comparison | Prohibited claim | `REMAINS_BLOCKED_EXTERNAL_EVIDENCE` |
| Production certification | Category compatibility records explicitly show `benchmarked: false` and `production_certified: false` | Must remain false | `REMAINS_BLOCKED_EXTERNAL_EVIDENCE` |

## What the structural branch may validate

ST-06.01 may validate only that:

1. exactly five constitutional category identities exist;
2. an applicable Activative Harness binds to exactly one of them;
3. each category carries explicit syntax-applicability descriptors without being
   flattened into generic metadata;
4. spatial, temporal, reading-order and conversational dimensions distinguish
   `APPLICABLE`, profile-conditional, unsupported/not evaluated, and justified
   `NOT_APPLICABLE` states;
5. Visual Syntax First remains the development evidence order and Activation First
   remains the runtime semantic law;
6. wrong-reading locks remain mandatory where constitutionally applicable;
7. every category and profile remains uncertified unless separate empirical evidence
   authorizes a stronger state.

It may not validate parse accuracy, provider fitness, real-profile grammar induction,
benchmark superiority, production thresholds or certification.

## Category non-flattening and applicability findings

- **Short-Form Edited Video:** visual composition, temporal state/cut relations and
  attention/reading order are structurally applicable. No empirical quality result
  was found.
- **2D Character Animation:** visual composition, character state, gaze/scene
  relations, continuity and temporal performance are structurally applicable.
  Format 02 is only contract-compatible and unbenchmarked.
- **Carousels:** per-slide spatial hierarchy and swipe/slide-role sequence are
  structurally applicable. Frame-time motion is explicitly not applicable unless a
  later profile adds governed motion evidence.
- **Supervisuals:** one-frame hierarchy and reading order are structurally applicable.
  Time-based syntax is explicitly not applicable to the one-frame category contract.
- **Conversational Activation / Human Expression:** turn, Reaction Receipt and
  Expression Moment sequence are structurally applicable; visual/spatial syntax is
  profile-conditional and not evaluated here. No certification is inherited.

These are contract descriptors derived from authority, not measured baselines.

## Wrong-reading and authority controls

Known structural wrong readings that ST-06.01 can reject without provider evidence:

- treating Format 02 as Short-Form Edited Video;
- treating a carousel as frame-time video;
- assigning video pacing to a Supervisual;
- treating conversational turns as generic visual metadata;
- allowing Visual Syntax to invent upstream Activative meaning;
- omitting or weakening mandatory wrong-reading locks;
- interpreting structural support or contract compatibility as certification.

## Later empirical closure

The broader BD-007 blocker remains open until the evidence in
`BD007_REQUIRED_EXTERNAL_EVIDENCE.yaml` exists and validates. No provider result,
accuracy score, cost observation, confidence threshold or certification claim was
fabricated by this audit.

## Sources reviewed

The hash-pinned evidence set is recorded in `BD007_BASELINE_INVENTORY.yaml`. Principal
sources were the Constitution V1.1, constitutional precedence and category registries,
F03, F14, TS-03, TS-11, ADR-008, the ST-06.01 Story contract and the independent
category/profile compatibility mapping.

