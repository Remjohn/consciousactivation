# PROMPT 02B — Spec Writing Dependency and Repository Authority Correction

**Controller:** GPT-5.6 Sol Extra High  
**Parallel:** No child writers. This is a bounded Program Control correction.

Prepare the V2.1 Spec-Writing Dependency-Stage and Repository Write-Authority Correction.

Do not rerun the broad authority convergence.

Do not write Tech Specs.

Do not audit, revise, accept, build, or issue Development Capsules.

Do not overwrite the historical Prompt 03 preflight or gate verdict. Preserve them and issue superseding records.

The purpose is to correct two workflow defects exposed by the Prompt 03 controller:

1. generic upstream specification dependencies were incorrectly treated as requiring `ACCEPTED_FOR_BUILD` before WRITE;
2. `TS-VAE-BOUND-001` targets a VAE path prohibited by the current VAE `AGENTS.md`.

## Required inputs

Read and hash:

* Prompt 02 completion receipt and 21-file manifest;
* canonical specification ledger;
* specification dependency DAG;
* all 60 writer packets;
* writing queue and lane manifests;
* Spec Quality Status Registry;
* Prompt 03 `CONTROLLER_PREFLIGHT_REPORT.md`;
* Prompt 03 `PACKET_VALIDATION_RESULT.yaml`;
* Prompt 03 `FACTORY_GATE_VERDICT.yaml`;
* current lifecycle and Tech Spec writer Skills;
* every applicable product-local `AGENTS.md`, especially `02_VISUAL_ASSET_EDITOR/AGENTS.md`.

Verify the four already locked source-archive hashes. Do not require re-upload when the existing source lock matches.

## 1. Classify every dependency edge by lifecycle stage

For every edge in the existing spec dependency DAG assign exactly one primary class:

* `AUTHORITY_DEPENDENCY`
* `WRITE_INTERFACE_DEPENDENCY`
* `WRITE_CONTEXT_DEPENDENCY`
* `ACCEPTANCE_PREREQUISITE`
* `BUILD_PREREQUISITE`
* `REFERENCE_ONLY`

An edge may additionally declare later-stage requirements, but it must have one primary WRITE behavior.

Do not infer `ACCEPTED_FOR_BUILD` at WRITE time from a generic `depends_on`, `upstream_specs`, or implementation ordering field.

Use these rules:

* authority must be ratified before writing;
* interface dependencies require a hash-pinned upstream draft, accepted spec, or exact Program Control contract seed;
* context dependencies may use a hash-pinned upstream draft and must be labeled non-authoritative;
* acceptance prerequisites block final spec acceptance, not initial writing unless separately classified as a write dependency;
* build prerequisites block build only;
* references do not block unless promoted to required unique evidence.

Create:

* `SPEC_DEPENDENCY_EDGE_CLASSIFICATION_V2_1.yaml`
* `SPEC_DEPENDENCY_EDGE_CLASSIFICATION_V2_1.csv`
* `DEPENDENCY_STAGE_CORRECTION_REPORT.md`

Account for all 118 reported edges exactly once.

## 2. Compute dependency-safe writing waves

Build a WRITE DAG using only:

* authority dependencies;
* write-interface dependencies;
* write-context dependencies that contain unique required information.

Create:

* `SPEC_WRITING_WAVE_DAG.yaml`
* `SPEC_WRITING_WAVE_PLAN.md`
* `SPEC_WRITING_WAVE_STATUS.yaml`

Rules:

* Wave 0 contains specs with no unresolved WRITE-blocking edges.
* All specs in one wave may be written in parallel when paths are disjoint.
* A later wave becomes writable when its required upstream specs have emitted `WRITTEN_PENDING_AUDIT` or `REVISED_PENDING_REAUDIT` receipts and exact hashes.
* Acceptance is not required during the writing factory.
* Build state never affects writing waves.

If a WRITE cycle exists:

1. identify the exact strongly connected component;
2. check whether ratified shared contracts resolve it;
3. otherwise create an `ARCHITECT_DECISION_REQUIRED` record or exact `WRITE_TIME_CONTRACT_SEED` request;
4. block only that component, not unrelated waves.

Do not invent an interface seed without current authority.

## 3. Correct all writer packets

For each of the 60 packets replace ambiguous dependency fields with:

* `upstream_write_inputs`
* `upstream_acceptance_prerequisites`
* `upstream_build_prerequisites`
* `reference_inputs`
* `draft_dependency_policy`
* `writing_wave`
* `output_path_class`
* `nearest_agents_file`
* `repository_write_authority_result`

Every draft dependency must require:

* path;
* quality state;
* SHA-256;
* `DRAFT_DEPENDENCY_NOT_ACCEPTED` label;
* downstream revision-impact section.

Update packet validation schema and rerun structural validation.

## 4. Correct `TS-VAE-BOUND-001`

Read `02_VISUAL_ASSET_EDITOR/AGENTS.md` and preserve its current write restriction.

Do not modify:

`02_VISUAL_ASSET_EDITOR/docs/tech-specs/`

Retarget the writing packet to a governed Program Control proposal path under the existing V2.1 Spec Factory root, for example:

`<SPEC_FACTORY_ROOT>/cross-product-proposals/TS-VAE-BOUND-001.md`

Use the exact existing Spec Factory root rather than inventing a parallel registry.

Set:

```yaml
document_class: PROPOSED_CROSS_PRODUCT_TECH_SPEC_AMENDMENT
target_product: 02_VISUAL_ASSET_EDITOR
proposed_adoption_path: 02_VISUAL_ASSET_EDITOR/docs/tech-specs/TS-VAE-BOUND-001.md
output_path_class: PROGRAM_CONTROL_CROSS_PRODUCT_PROPOSAL
quality_target: WRITTEN_PENDING_AUDIT
adoption_status: PRODUCT_ADOPTION_REQUIRED
build_status: NOT_BUILD_READY
```

The proposal may be written, audited, revised, and accepted for product adoption. It may not receive product-local build acceptance or a VAE Development Capsule until VAE write/adoption authority is granted and the adopted bytes are re-audited.

## 5. Inspect every other packet against repository-local write authority

For every target path:

* locate the nearest applicable `AGENTS.md`;
* verify the exact path is permitted;
* classify as:
  * `DIRECT_PRODUCT_SPEC_PATH`;
  * `PROGRAM_CONTROL_CROSS_PRODUCT_PROPOSAL`;
  * `DEFERRED_UNTIL_PRODUCT_AUTHORIZATION`.

Retarget any other disallowed product path to Program Control only when current Program Control authority permits a proposal. Otherwise block only that packet.

Create:

* `SPEC_PACKET_WRITE_AUTHORITY_MATRIX.csv`
* `PRODUCT_ADOPTION_QUEUE.yaml`

## 6. Supersede the failed Prompt 03 gate

Preserve the original files unchanged.

Create superseding records:

* `FACTORY_GATE_CORRECTION_V2_1.yaml`
* `PROMPT_03_REAUTHORIZATION.yaml`
* `PROMPT_02B_COMPLETION_RECEIPT.yaml`
* `FILE_MANIFEST_PROMPT_02B.json`

`PROMPT_03_REAUTHORIZATION.yaml` may authorize Prompt 03 only when:

* all 118 edges are classified;
* a valid writing DAG exists for all unblocked components;
* every packet has a valid output path class;
* VAE is retargeted as a Program Control proposal;
* no product-local allowlist is violated;
* source locks still match.

## Acceptance criteria

Pass only when:

* the 118 dependency edges are accounted for exactly once;
* build dependencies no longer block WRITE;
* acceptance prerequisites no longer block WRITE unless separately classified;
* topological writing waves are explicit;
* every packet is structurally valid;
* VAE repository restrictions are preserved;
* `TS-VAE-BOUND-001` is a non-buildable Program Control proposal;
* original failed gate evidence remains immutable;
* Prompt 03 receives a truthful superseding authorization.

Stop after this bounded correction. Then rerun the corrected Prompt 03 only.
