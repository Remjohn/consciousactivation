# Constitutional Alignment Batch A — Authority Delta

Date: 2026-07-14  
Batch: A — authority, requirement, and impact analysis only  
Previous authority: VAE V1 active repository baseline  
Current authority: VAE V1.1 plus CCP Activative Intelligence & Visual Narrative Constitution v1.1.0  
Batch verdict: FAIL

## Scope and authority chain

This analysis preserves the completed Stage 1 audit, Stage 2 technical specifications, Stage 3 RC2 contract analysis, Stage 4 epics and readiness evidence, and the current FAIL readiness verdict. It does not restart the project and does not authorize Stage 5.

The controlling chain is:

1. 00_ALIGNMENT_START_HERE.md and docs/product-authority/CURRENT_AUTHORITY.md.
2. The program authority pointer at CMF_PROGRAM_CONTROL/01_PRODUCT_AUTHORITIES/visual-asset-editor/AUTHORITY_POINTER.md.
3. The current V1.1 unpacked authority package.
4. governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml in that package.
5. The embedded CCP Activative Intelligence & Visual Narrative Constitution v1.1.0, verified against SHA-256 21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b.
6. The binding VAE V1.1 Activative Visual Contract Amendment.

The precedence rule is explicit: the embedded constitution controls Activative and visual-semantic behavior when a local document conflicts. Adoption is by bounded patching of the in-progress repository, not by replacing it with a fresh PRD package.

## Constitutional delta

V1 treated semantic intent, Activative function, composition intent, and wrong-reading locks as sufficient top-level demand context. V1.1 separates upstream meaning from production execution and adds the following mandatory constitutional layers:

| Delta | Binding meaning for VAE |
|---|---|
| Activative semantic lineage | Preserve references to the Activative Intelligence Pack and its Identity DNA, Context Premise, Resonance, Matrix of Edging, and source evidence. Interview-derived work must also preserve Reaction Receipt and Expression Moment references. |
| Activation Contract | Consume edge pressure, activation directions, viewer roles, stance, identity urges, intended reaction, participation design, and smallest useful commitment. VAE does not author these decisions. |
| Visual Semantic Pack | Consume the recognition intent, selected recognition carrier, audience visual-world evidence, relevant behavior traces or dog-whistles, real-life reference classes, emotional load carrier, and Semiotic MCDA receipt. |
| Visual Narrative Program | Consume pattern match, pattern interrupt, attention-state sequence, viewer-role progression, prediction gap, payoff, affinity field, and anticipation residue. |
| Feature Contracts | Treat meaning-bearing gaze, hands, posture, witness, object punctum, negative space, contact, distance, crop, motion, light, and sequence decisions as explicit contracts rather than model defaults. |
| T/V somatic route request | Carry the requested body-delivery route after carrier and narrative selection. T/V cannot choose or repair a missing carrier or narrative. |
| Wrong-reading locks | Require non-empty locks for generation, compositing, restyling, inpainting, outpainting, and semantic transformation. Deterministic resize or encoding may inherit locks only with a reference to the accepted master. |
| No-text survival | A no-text profile must pass the delete-caption test; copy cannot carry meaning that the visual failed to carry. |
| Evaluation precedence | Technical or aesthetic quality cannot compensate for failed activation, role, narrative, wrong-reading, feature-contract, no-text, or composition gates. |

These deltas instantiate constitutional Laws 12 through 20: visual semantics, visual narrative, syntax, feature contracts, somatic routing, no-text survival, pre-generation wrong-reading locks, and harness-based anti-drift are distinct responsibilities.

## PRD delta

The V1.1 authority preserves all 176 functional requirement identifiers and strengthens only four stable requirements:

| Requirement | V1.1 strengthening |
|---|---|
| FR-009 | The Visual Asset Demand becomes constitution-complete: lineage, Activation Contract, Visual Semantic Pack, Visual Narrative Program, applicable Feature Contracts, T/V request, and non-empty wrong-reading locks are required in addition to the existing demand context. |
| FR-107 | Asset-level independent evaluation must compare the candidate against the Activation Contract, Visual Semantic Pack, Visual Narrative Program, Feature Contracts, somatic route, and locks, not only generic semantic intent and Activative function. |
| FR-108 | Composition evaluation adds zero-second hook, pattern match and interrupt, viewer-role progression, prediction gap, payoff, affinity, anticipation residue, anti-cliche strength, and applicable no-text survival. |
| FR-111 | Hard-gate synthesis explicitly prevents technical or aesthetic scores from hiding role, wrong-reading, feature-contract, visual-narrative, no-text, or composition failure. |

The original product boundary is unchanged. Content Harness remains semantic authority. VAE does not own Identity DNA, Context Premise, edge selection, content archetype routing, interviews, Activative Calls, or final downstream composition authorization.

## Current authority package consistency findings

The amendment is binding, but its packaged draft artifacts are not yet sufficient to serve as the final Delegation boundary:

1. The V1.1 demand schema adds the new top-level layers and makes wrong_reading_locks non-empty, but it has no explicit inherited-lock reference for deterministic resize or encoding routes.
2. Reaction Receipt and Expression Moment arrays are optional and the schema has no discriminator that makes them mandatory for interview-derived demands.
3. Feature Contracts are generic references; the owning contract family, applicability signal, and canonical union shape remain unresolved at the shared boundary.
4. The V1.1 evaluation schema adds activation and wrong-reading sections but does not explicitly require activation-direction fidelity or feature-contract compliance, and it does not conditionally require a delete-caption result for no-text profiles. Human affinity is represented only as affinity.
5. The packaged VISUAL_ASSET_DEMAND template remains V1-shaped even though the schema and Format 02 demand example were amended.
6. The current repository is reconciled to an unsigned local Delegation 1.0.0-rc.2. The target named by the alignment authority is Delegation 1.1.0-rc.1. Shared schema or binding work must wait for the owner-published canonical package.

These findings must be resolved by the named owners. Batch A does not invent the missing semantics and does not create a local Delegation fork.

## Acceptance-test audit

| V1.1 acceptance test | Current repository evidence | Result |
|---|---|---|
| Reject generated demand without wrong-reading locks | The active local demand schema does not require wrong_reading_locks and does not set minItems. | FAIL |
| Trace every selected asset to Activative Intelligence Pack and applicable Expression Moment | The active demand, plan, memory, and result path lacks typed Activative lineage. | FAIL |
| Materializer cannot infer recognition carrier or viewer role from free-form semantic intent | Existing specs forbid semantic mutation generally, but do not bind the materializer to the new Visual Semantic Pack and Activation Contract objects. | FAIL |
| Reject technically valid assets that fail role activation, pattern interrupt, or wrong-reading tests | Existing TS-VAE-06 describes Activative and wrong-reading hard gates, but the active evaluation schema and fixture do not require the V1.1 activation evidence. | FAIL |
| Enforce delete-caption test for no-text profiles | No active profile registry, schema condition, or fixture proves the test. | FAIL |

## What can be patched before Delegation 1.1.0-rc.1

- Adopt the constitutional precedence, stable FR wording, governance prohibitions, and readiness blockers without replacing the repository baseline.
- Patch VAE-owned evaluation, plan, memory, repair, benchmark, and test-design artifacts using opaque authoritative references and no copied Delegation types.
- Patch technical specifications and story acceptance criteria where the rule is wire-shape agnostic: preserve the new layers, forbid inference, propagate lineage, apply expanded hard gates, and fail closed.
- Define a VAE-owned versioned Visual Evaluation Profile registry and constitutional negative-test plan.
- Keep implementation authorization false and add explicit gates for the amendment acceptance tests.

## What must wait for Delegation 1.1.0-rc.1

- The canonical Visual Asset Demand public schema, generated bindings, exact field paths, ownership metadata, and compatibility classification.
- Demand templates and canonical producer fixtures.
- Conditional Expression Moment and Reaction Receipt enforcement at the shared boundary.
- The inherited wrong-reading-lock representation for deterministic routes.
- The canonical Feature Contract reference or union shape.
- RC migration, amendment-response consumer repair, result migration, signed pin, and executable producer/consumer/adapter conformance.
- A final Stage 4 readiness re-audit and any Stage 5 decision.

## Batch A verdict

FAIL. The V1.1 direction is compatible with the preserved VAE architecture, so the project does not restart. The active repository is nevertheless not constitutionally aligned: all five amendment acceptance tests lack complete active evidence, the final Delegation RC1 boundary is absent, and four contract or evaluation decisions plus the release-pin decision require authoritative human resolution. Later patch batches are bounded in PATCH_BATCHES.yaml. No later batch is authorized by this verdict.
