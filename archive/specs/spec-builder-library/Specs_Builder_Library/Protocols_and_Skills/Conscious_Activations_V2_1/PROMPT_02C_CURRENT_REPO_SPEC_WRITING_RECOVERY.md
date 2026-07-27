# PROMPT 02C — Current-Repository Spec-Writing Recovery

**Controller:** GPT-5.6 Sol Extra High  
**Parallel:** No child writers. This is a bounded recovery and reauthorization step.

Prepare the Current-Repository V2.1 Spec-Writing Recovery Package.

Do not rerun Prompt 01.

Do not rerun the broad Prompt 02 reconciliation.

Do not write Tech Specs.

Do not audit, revise, accept, build, or issue Development Capsules.

Do not require restoration of uncommitted Prompt 03 controller logs.

The purpose is to recover from the failed Prompt 03 and failed Prompt 02B attempts using the canonical records that actually exist in the current repository.

## Current repository facts that must be verified, not assumed

Verify from the active repository:

* `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/COMPLETION_RECEIPT.yaml`
* `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/PROMPT_02_GATE_RECEIPT.yaml`
* `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/COMPLETION_RECEIPT.yaml`
* the Prompt 02 `FILE_MANIFEST.json`
* `CANONICAL_SPEC_LEDGER.csv`
* `FULL_TECH_SPEC_WRITING_QUEUE.yaml`
* `ONE_SPEC_EXECUTION_PACKETS.yaml`
* `SPEC_DEPENDENCY_DAG.yaml`
* `PATH_OWNERSHIP_REGISTRY.yaml`
* `WRITER_LANE_MANIFESTS.yaml`
* `SPEC_QUALITY_STATUS_REGISTRY.yaml`
* `SOURCE_DISPOSITION_LEDGER.yaml`
* `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/PROMPT_02B_MISSING_INPUT_REPORT.yaml`
* current repository-root and product-local `AGENTS.md`

Verify the four locked source archives using the existing Prompt 02 hash lock and manifest.

## 1. Correct the historical-input mistake

The following directory is absent from the current committed repository:

`CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_FACTORY/`

Do not require or reconstruct:

* `CONTROLLER_PREFLIGHT_REPORT.md`
* `PACKET_VALIDATION_RESULT.yaml`
* `FACTORY_GATE_VERDICT.yaml`

Unless exact bytes are separately supplied and hash-locked, classify them as:

```yaml
persistence_class: EPHEMERAL_EXECUTION_LOG_NOT_PERSISTED
canonical_gate_input: false
reconstruction_allowed: false
recovery_effect: NON_BLOCKING
```

Preserve `PROMPT_02B_MISSING_INPUT_REPORT.yaml` as immutable evidence of the failed recovery attempt.

Do not overwrite it.

Create:

* `V2_1_SPEC_WRITING_RECOVERY/EPHEMERAL_LOG_DISPOSITION.yaml`
* `V2_1_SPEC_WRITING_RECOVERY/RECOVERY_INPUT_VERIFICATION.md`

The recovery must be derived from the committed Prompt 02 queue, dependency DAG, packets, path registry, Skills, and repository instructions.

## 2. Correct the ratification-stage mistake

Read the Prompt 01 completion receipt and Prompt 02 gate receipt.

Preserve:

* V2.1 candidate authority remains pending attributable human ratification;
* candidates are not current authority;
* no implementation or production authority exists.

Also preserve the Prompt 02 explicit authorization for specification work.

The absence of final ratification must not block:

* Tech Spec writing;
* independent audit;
* revision;
* re-audit;
* technical convergence.

While ratification remains pending:

* every writer must label candidate authority `CANDIDATE_NOT_CURRENT`;
* no spec controlled by the candidate may receive `ACCEPTED_FOR_BUILD`;
* the maximum later status is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`;
* no Development Capsule or BUILD authority may be issued.

Create:

* `V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml`
* `V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml`

The authorization source must reference the exact Prompt 02 gate receipt and completion receipt.

Do not invent a ratification receipt.

## 3. Classify all specification dependencies by lifecycle stage

For every edge in the existing Prompt 02 dependency DAG assign exactly one primary class:

* `AUTHORITY_DEPENDENCY`
* `WRITE_INTERFACE_DEPENDENCY`
* `WRITE_CONTEXT_DEPENDENCY`
* `ACCEPTANCE_PREREQUISITE`
* `BUILD_PREREQUISITE`
* `REFERENCE_ONLY`

Do not infer write blocking from generic `depends_on` fields.

Apply:

* authority dependencies must be satisfied by current authority or explicit candidate-specification-work authorization;
* write-interface dependencies require a hash-pinned upstream draft, accepted spec, or governed contract seed;
* write-context dependencies may consume a hash-pinned draft as non-authoritative context;
* acceptance prerequisites block final acceptance, not WRITE;
* build prerequisites block BUILD only;
* references do not block unless separately classified as required unique evidence.

Account for every edge exactly once.

Create:

* `SPEC_DEPENDENCY_EDGE_CLASSIFICATION.yaml`
* `SPEC_DEPENDENCY_EDGE_CLASSIFICATION.csv`
* `DEPENDENCY_STAGE_CORRECTION_REPORT.md`

## 4. Compute dependency-safe writing waves

Build a WRITE DAG using only WRITE-blocking edges.

Create:

* `SPEC_WRITING_WAVE_DAG.yaml`
* `SPEC_WRITING_WAVE_PLAN.md`
* `SPEC_WRITING_WAVE_STATUS.yaml`

Rules:

* Wave 0 contains dependency roots.
* Specs inside a wave may run in parallel when paths are disjoint.
* A later wave becomes writable after required upstream specs emit a hash-pinned `WRITTEN_PENDING_AUDIT` or `REVISED_PENDING_REAUDIT` receipt.
* Upstream acceptance is not required during Prompt 03.
* Build state never blocks writing.

If a WRITE cycle exists, isolate only the strongly connected component and request a bounded architecture decision or exact contract seed.

Do not stop unrelated waves.

## 5. Correct every writer packet

For all 60 packets, replace ambiguous dependency data with:

* `upstream_write_inputs`
* `upstream_acceptance_prerequisites`
* `upstream_build_prerequisites`
* `reference_inputs`
* `candidate_authority_state`
* `specification_work_authorization`
* `draft_dependency_policy`
* `writing_wave`
* `output_path_class`
* `nearest_agents_file`
* `repository_write_authority_result`

When a candidate authority controls the spec, include:

```yaml
authority_state: CANDIDATE_NOT_CURRENT
write_authorized: true
build_authorized: false
maximum_pre_ratification_quality_state: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
```

When a non-accepted upstream draft is consumed, require path, quality state, SHA-256, and `DRAFT_DEPENDENCY_NOT_ACCEPTED`.

Update and validate the packet schema.

## 6. Correct VAE and all repository-local path authority

Read `02_VISUAL_ASSET_EDITOR/AGENTS.md`.

Do not write `TS-VAE-BOUND-001` directly into:

`02_VISUAL_ASSET_EDITOR/docs/tech-specs/`

Retarget it to the existing Program Control V2.1 Spec Factory proposal area:

`<CURRENT_SPEC_FACTORY_ROOT>/cross-product-proposals/TS-VAE-BOUND-001.md`

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

Inspect every other packet against its nearest `AGENTS.md`.

Classify:

* `DIRECT_PRODUCT_SPEC_PATH`
* `PROGRAM_CONTROL_CROSS_PRODUCT_PROPOSAL`
* `DEFERRED_UNTIL_PRODUCT_AUTHORIZATION`

Create:

* `SPEC_PACKET_WRITE_AUTHORITY_MATRIX.csv`
* `PRODUCT_ADOPTION_QUEUE.yaml`

## 7. Issue a fresh Prompt 03 authorization

Do not supersede absent Prompt 03 files.

Instead, issue a new recovery-chain authorization derived from committed canonical inputs.

Create:

* `PROMPT_03_RECOVERY_AUTHORIZATION.yaml`
* `FACTORY_RECOVERY_VERDICT.yaml`
* `PROMPT_02C_COMPLETION_RECEIPT.yaml`
* `FILE_MANIFEST.json`

Prompt 03 may be authorized only when:

* Prompt 02 committed inputs and hashes validate;
* all dependency edges are classified;
* a valid writing-wave DAG exists for all unblocked components;
* all packets validate;
* all output paths respect repository instructions;
* VAE is a Program Control proposal;
* specification work authorization is explicit;
* candidate authority remains non-current;
* build and production authorization remain false.

## Acceptance criteria

Pass only when:

* missing Prompt 03 logs are correctly treated as noncanonical ephemeral artifacts;
* no unavailable bytes are reconstructed;
* pending ratification does not incorrectly block specification writing;
* candidate authority is not represented as current;
* all dependency edges are classified exactly once;
* writing waves are explicit;
* every writer packet validates;
* VAE repository instructions are preserved;
* Prompt 03 receives a fresh, truthful, specification-writing-only authorization;
* no Tech Spec, code, contract release, Development Capsule, or build artifact is created.

Stop after this recovery package.

Then run the V3.3 dependency-safe Prompt 03.
