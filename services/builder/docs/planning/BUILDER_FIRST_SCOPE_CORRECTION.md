# Builder-First Product-Scope Correction

**Date:** 2026-07-15  
**Authority:** Builder PRD V1.2 and Activative Intelligence Constitution V1.1  
**Change type:** confirmed planning rebaseline  
**Implementation code changed:** no  
**Confirmed inventory changed:** conditional overlay only; IDs and obligation ownership unchanged  
**Application verdict:** `CONFIRMED_APPLIED`

**Human confirmation:** `CONFIRM BUILDER-FIRST CORE TRACK AND STORY AMENDMENTS`, received 2026-07-15.  
**Application receipt:** `docs/planning/BUILDER_FIRST_STORY_AMENDMENT_RECEIPT.yaml`.

## Executive finding

Yes. The current confirmed Story sequence improperly couples construction of the category-neutral Builder to Format 02 and later product concerns.

The coupling is structural:

- `ST-03.04`, the first deterministic artifact compiler, has 12 transitive predecessors and therefore cannot run without the complete evidence/syntax chain through `ST-02.05`.
- `ST-07.02`, the Atomic Content Harness target compiler, has 25 transitive predecessors, including all category Stories through `ST-06.05` and the three-target registration Story.
- `ST-11.01`, the Development Capsule compiler, has all 62 earlier Stories as transitive predecessors. It therefore requires category adapters, conversational structure, external target handoffs, protected evaluation, workflow operations, and all 14 Control Tower Stories before the Builder can emit its own primary product.
- The corrected readiness matrix then propagates the Format 02 `BD-004` corpus gate through that chain. That result is internally consistent with the confirmed graph but reverses the intended product relationship.

The corrected relationship is:

```text
Atomic Harness Builder core
-> generic Harness compilation
-> synthetic category-neutral proof
-> category adapters and reference profiles
-> Format 02 reference validation
```

Format 02 remains an important future reference Harness. It is not an input prerequisite for constructing the generic Builder core.

## Corrected first useful Builder outcome

A user submits a governed, repository-owned synthetic atomic-task definition. The Builder accepts and hash-locks the definition, validates its declared atomic boundary, compiles one canonical Harness IR, derives a target/output contract, required-context manifest, capability and skill requirements, phase/execution plan, and executable acceptance-test definitions, and emits:

1. a validated `AtomicHarnessDefinition` package;
2. a validated `DevelopmentCapsule` package; and
3. a deterministic compilation/validation receipt binding every input and output hash.

The proposed proof fixture is `synthetic_text_normalization_v1`: a deliberately non-product task that describes normalizing UTF-8 line endings and one terminal newline. The Builder compiles the Harness definition; it does not implement or execute the final normalizer. The fixture:

- is test-only and repository-owned;
- is not a sixth canonical category;
- is not a production profile;
- has no Format 02, conversational, VAE, Delegation-runtime, ComfyUI, GPU, provider-comparison, or VLM dependency;
- declares deterministic code-owned capabilities and an explicitly empty specialized-skill requirement under the eventual BD-010 policy;
- can never produce benchmark or certification claims.

## Story inventory audit

Every one of the 69 confirmed Stories is classified exactly once in `STORY_PRODUCT_CLASSIFICATION.csv`.

| Classification | Story count | Product meaning |
|---|---:|---|
| `BUILDER_CORE` | 24 | Category-independent governance, IR, architecture, context, skill ecology, repair, and implementation-governance capabilities |
| `GENERIC_BUILDER_PROOF` | 4 | Deterministic artifacts, Atomic Content Harness compilation/validation, and Development Capsule generation used by the synthetic proof |
| `CATEGORY_ADAPTER` | 7 | Substrate/category syntax and category-profile compilation after the core exists |
| `FORMAT02_REFERENCE_VALIDATION` | 3 | V2.1/Format 02 migration and complete reference-spine proof |
| `CONVERSATIONAL_FUTURE` | 2 | Conversational and expression feedback/evaluation outcomes |
| `EXTERNAL_PRODUCT_INTEGRATION` | 2 | Three-target and VAE/Delegation handoff outcomes |
| `CONTROL_TOWER_OR_OPERATIONS` | 22 | Workflow-runtime operation and all Control Tower surfaces |
| `PRODUCTION_CERTIFICATION` | 5 | Protected evaluation, maturity promotion, authorization, and bounded certification |
| **Total** | **69** | **Every confirmed Story assigned exactly once** |

This classification does not delete, renumber, or reassign an obligation. The confirmed 410 primary obligation assignments remain historically authoritative.

## Review of ST-01.02 through ST-03.04

| Story | Actual product scope | Current coupling | Corrected treatment |
|---|---|---|---|
| `ST-01.02` | Generic safe source-lock/evidence-workspace capability | Real-profile wording activates BD-004 and external/conversational gates globally | Add a synthetic-definition branch; BD-004 activates only for a real profile corpus |
| `ST-01.03` | Generic multi-specimen indexing and provenance | Inherits the Format 02 corpus frontier | Preserve for later evidence-rich Builder use; not required for a one-file governed synthetic definition |
| `ST-01.04` | Generic saturation and evidence-gap decision | Inherits the Format 02 corpus frontier | Preserve for later evidence-derived runs; the proof fixture declares a complete bounded input contract |
| `ST-02.01` | Category/substrate syntax normalization | Visual/conversational evidence and provider baselines are treated as core | Move after generic proof as `CATEGORY_ADAPTER` |
| `ST-02.02` | Category/substrate relationship graphs | Same | Move after generic proof as `CATEGORY_ADAPTER` |
| `ST-02.03` | Syntax-first grammar induction | Same, plus certification threshold coupling | Move after generic proof as `CATEGORY_ADAPTER` |
| `ST-02.04` | Generic evidence-derived atomic-boundary comparison | Forced onto every path through the syntax chain | Preserve for evidence-derived candidates; omit when a governed synthetic task already declares its boundary |
| `ST-02.05` | Generic ratification and freeze of one atomic boundary | Requires `ST-02.04` even for a predeclared boundary | Add `DECLARED_BOUNDARY` and `DISCOVERED_BOUNDARY` dependency modes |
| `ST-03.01` | Generic interactive Genesis question selection | Forced onto a complete pre-ratified synthetic definition | Preserve for interactive Genesis; omit when all required synthetic decisions are already governed |
| `ST-03.02` | Generic human-decision transaction/resume | Same | Preserve for interactive Genesis; ST-01.01 already supplies run resume for the proof |
| `ST-03.03` | Generic canonical Harness IR | BD-014 and interactive Genesis are treated as unconditional | Accept a pre-ratified synthetic decision package; activate BD-014 only for external-target fields |
| `ST-03.04` | Generic deterministic human/machine compilation | Inherits all preceding Format 02/category work | Keep on Track A immediately after the generic IR branch |

None of `ST-01.02` through `ST-03.04` is wholly a Format 02 reference-validation Story. `ST-02.01` through `ST-02.03` are category-adapter work; the rest contain generic Builder capabilities whose current activation or dependency rules are overly profile-specific.

## Track A — Builder Core

The proposed minimum existing-Story sequence is:

```text
ST-01.01 -> ST-01.02 -> ST-02.05 -> ST-03.03 -> ST-03.04 -> ST-03.05
-> ST-04.01 -> ST-04.02 -> ST-04.03 -> ST-04.04 -> ST-04.05
-> ST-05.01 -> ST-05.02 -> ST-07.02 -> ST-07.04 -> ST-11.01
```

This sequence is valid only after the conditional Story amendments in `STORY_AMENDMENT_PROPOSAL.yaml` are human-confirmed. All proposed edges point backward. The original full-product branches remain intact.

The sequence contains 16 confirmed Story IDs:

- `ST-01.01` remains `COMPLETE/PASS` and supplies run identity, authority, replay, checkpoints, and target-selection seams. Its existing Format 02-only executable adapter is not mistaken for generic proof support. A supplemental synthetic-proof acceptance branch and receipt are proposed; the original receipt remains valid and unchanged.
- `ST-01.02` becomes the safe governed-input intake for the synthetic definition.
- `ST-02.05` validates and freezes the fixture's predeclared atomic boundary without requiring syntax induction.
- `ST-03.03` through `ST-03.05` compile canonical IR, deterministic artifacts, and constitutional precedence.
- `ST-04.01` through `ST-04.05` compile capabilities, responsibility boundaries, test seams, phase graph, handoffs, and minimum complete context.
- `ST-05.01` and `ST-05.02` compile the governed skill requirement and prove that the synthetic task needs no specialized agent skill.
- `ST-07.02` and the Atomic Content Harness branch of `ST-07.04` compile and validate the `AtomicHarnessDefinition` without VAE or Delegation behavior.
- The synthetic branch of `ST-11.01` emits the hash-bound Development Capsule without requiring certification, workflow automation, or Control Tower completion.

Current readiness on this proposed path is deliberately not overstated:

- `ST-01.01`: `COMPLETE_PASS` under its existing receipt.
- Currently `READY`: **0** Stories, because the amended core branch has not been human-confirmed.
- First implementation unit after confirmation: the supplemental synthetic-proof acceptance branch for `ST-01.01`, under a new bounded capsule and additive receipt.
- First subsequent Story: `ST-01.02`, after that additive receipt validates.
- `BD-010` must close before `ST-04.01`; the approved empty-registry policy is the minimum closure for this synthetic proof.

## Track B — Format 02 Reference Validation

Track B starts only after Track A proves that the Builder can compile a synthetic Harness and Development Capsule. It then introduces:

- the governed Format 02 corpus and portable source profile (`BD-004`);
- provider comparison and deterministic visual-syntax baselines (`BD-007`);
- Format 02 syntax/category adapter Stories;
- evaluated skill/capsule and protected benchmark evidence;
- VAE/Delegation contract handoffs and, later, external runtime evidence;
- evaluator certification, GPU-backed work where empirically required, and production evidence;
- the explicit `ST-12.03` Format 02 spine proof and `ST-12.04` bounded certification claims.

Track B validates the Builder. It does not construct the prerequisite Builder core.

## Blocker correction

The following do not block Track A:

- `BD-004` Format 02 corpus;
- `BD-007` provider comparison and visual-syntax baselines;
- VAE readiness or execution;
- Delegation runtime execution;
- evaluator or VLM certification;
- GPU/ComfyUI infrastructure;
- Format 02 benchmark or production evidence;
- `HD-006` and `HD-007` conversational policy/certification;
- `BD-008` protected production-threshold evidence;
- `BD-014` external handoff compatibility, except when an external branch is selected.

The genuine Builder-core cut is:

1. human reconfirmation of the conditional Story/dependency amendments;
2. a supplemental, bounded ST-01.01 synthetic-proof acceptance receipt without rewriting its existing PASS receipt;
3. sequential prior-Story completion receipts;
4. `BD-010` closure through an approved empty-registry policy or another governed core-capability seed policy; and
5. a complete bounded Development Capsule and explicit implementation authorization for each Story increment.

Program Control authority (`XDEP-001`) remains governing input, not an external runtime blocker. Activation Compiler and Delegation schemas may be consumed as pinned contract fixtures when a Story genuinely references them, but neither runtime is required on Track A.

## Human governance effect

The proposed changes alter conditional acceptance and dependency activation for confirmed Stories. They therefore require human reconfirmation even though:

- no Epic is redesigned;
- no Story ID is added, removed, or renumbered;
- no obligation changes primary owner;
- the 410-obligation coverage remains exact;
- the original 103-edge graph and confirmation receipts remain preserved as historical evidence;
- every proposed active Track A edge points backward.

No Story split is recommended. Conditional acceptance/dependency modes preserve one independently verifiable outcome for every affected Story more cleanly than splitting them.

## Exact next phrase

The planning rebaseline is confirmed. To authorize implementation of only the supplemental branch after its capsule validates, use exactly:

`AUTHORIZE BUILDER ST-01.01-SYNTHETIC-PROOF BOUNDED IMPLEMENTATION`

No implementation is authorized by the planning confirmation itself. `ST-01.02` remains blocked until the supplemental branch issues a PASS completion receipt. The human-approved empty-skill policy closes only the synthetic Builder Core sub-scope of BD-010.
