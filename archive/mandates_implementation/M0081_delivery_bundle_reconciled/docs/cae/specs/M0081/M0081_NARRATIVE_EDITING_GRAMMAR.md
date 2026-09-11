# M0081 — Narrative Editing Grammar

**Status:** `IMPLEMENTED — OPERATOR REVIEW REQUIRED`

## Decision boundary

M0081 adds a constrained, CAE-native narrative editing grammar. It expresses relational and sequence conditions that describe how upstream editorial intent and activative meaning become perceptual scene roles.

It is **not** an effects catalog. It contains no geometry, keyframes, provider parameters, generation commands, or runtime authority.

## Authority mapping

| Concern | Canonical CAE authority | M0081 role |
|---|---|---|
| Activative / semantic meaning | Upstream AIR / semantic-program authorities | Required input; never invented here |
| Editorial storyboard identity | `EditorialStoryboardRecord` | Existing semantic storyboard authority |
| Editable scene/revision | `StoryboardRevision` backed by `GraphRevisionRecord` | Existing revision authority |
| Narrative grammar | `NarrativeEditingGrammarRegistry` | Bounded sequence/relationship vocabulary |
| Scene binding | `StoryboardScene.narrative_grammar` | Optional scene-local projection that points to the canonical revision's harness |
| Harness execution identity | `StoryboardRevision.harness_id` | Required and equality-checked for grammar-bound scenes |
| Operator promotion | Existing storyboard validation/feedback/compile path | Unchanged; grammar validation does not self-promote |

**Claim classes:** `SCHEMA` for data contracts; `EXECUTABLE` for registry/validator and storyboard binding; `TEST` for enforcement; `DOCUMENT` for doctrine mapping; `OPERATOR_DECISION_REQUIRED` for final acceptance.

## Grammar vocabulary

| Mode | Relational / sequence pattern | Allowed contexts |
|---|---|---|
| `WITHHOLD` | establish context without decisive resolution → later reframe | OPENING, ORIENTATION, SETUP, TENSION, BRIDGE |
| `REVEAL` | prior withheld state → explicit recognition | TURN, EVIDENCE, RESOLUTION |
| `FOCUS` | broad context → discriminating detail | OPENING, ORIENTATION, SETUP, EVIDENCE, TURN |
| `CONTRAST` | state A <> state B → recognition of difference | TENSION, CONTRAST, TURN |
| `PROVE` | claim → evidence-bearing instance | EVIDENCE, TURN, RESOLUTION |
| `EXPLAIN` | observed state → causal mechanism | ORIENTATION, SETUP, EVIDENCE, TURN |
| `CONNECT` | current state ↔ related state | BRIDGE, TENSION, TURN, AFTERMATH |
| `ESCALATE` | current stakes < next stakes | TENSION, TURN |
| `INTERRUPT` | established pattern → meaningful break → return/reframe | INTERRUPT, TURN, BRIDGE |
| `RESOLVE` | open relation → clarified/closed relation | TURN, RESOLUTION, AFTERMATH |

The executable registry is duplicated as a human-readable machine registry at:

`docs/cae/specs/M0081/narrative_editing_grammar_registry.yaml`

## Binding contract

A grammar-bound scene carries:

- `scene_id`
- `grammar_mode` + `grammar_version`
- opaque `archetype_id` supplied by the upstream narrative/archetype authority
- `harness_id`, which must equal the revision/session harness identity
- non-empty `activative_meaning`
- non-empty `editorial_intent`
- declared `scene_context`
- deterministic `sequence_index`
- source `evidence_refs` where the grammar requires evidence
- relational `relation_scene_ids` where the grammar requires a scene relation
- `wrong_reading_locks`

The grammar validator does not decide whether an archetype is semantically correct. Existing archetype gates remain authoritative. M0081 only requires that a grammar binding identify the archetype it is operating within and preserves that identity through the revision.

## Stateful path

For a grammar-bound revision:

`EditorialStoryboardRecord → StoryboardSession → StoryboardRevision → NarrativeGrammarBinding → format storyboard program → downstream expression`

The save path fails closed before persistence when grammar binding is malformed or inconsistent. Re-validation is repeated when a revision validation report is emitted.

State transition mapping:

| Stage | Actor | Preconditions | Validator | Postcondition | Receipt / error | Recovery |
|---|---|---|---|---|---|---|
| bind grammar | operator / authorized editor | existing storyboard + canonical harness id | `NarrativeEditingGrammarRegistry` | validated scene payload | `StoryboardRevisionValidationError` on failure | repair and create a new revision |
| save revision | editor actor | current base revision | `PreparationGraphStore` CAS | immutable `GraphRevisionRecord` | existing graph revision record | reload latest and retry |
| validate revision | evaluator path | immutable revision exists | storyboard + grammar validators | validation report | existing validation report | repair, then save a new revision |
| compile | operator-approved | passing validation + GOOD feedback | existing compile gate | `StoryboardCompileReceipt` | existing compile receipt / feedback error | obtain valid operator decision or revise |

## False-proof defenses

The validator explicitly rejects cases that may look correct perceptually but fail the narrative contract:

- a `REVEAL` without a prior `WITHHOLD`;
- a `CONTRAST` without a distinct related scene;
- a harness mismatch between a binding and the revision;
- an unsupported scene context;
- missing editorial intent or activative meaning;
- a grammar sequence with non-contiguous positions;
- a visual-looking `PROVE` with no source evidence.

## External behavior

No new external repository behavior was adopted for M0081. The implementation reuses the active CAE brownfield path already established by M0078–M0080. No provider/runtime integration was added.

## Evidence limitations

The supplied repository archive contains no `.git` metadata, so the exact current CAE commit SHA cannot be established from this artifact.

The four dated Authority Pack files required by M0081 were supplied separately as frozen campaign inputs and directly inspected. Their manifest explicitly states that they do not have to exist in the brownfield repository before mandate execution.

The environment lacks `psycopg`; the network is unavailable for dependency installation. M0081 registry tests and an actual-module storyboard integration probe were run successfully, but the full monorepo baseline could not be collected under the supplied environment.
