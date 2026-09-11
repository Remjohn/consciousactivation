# AGENT_HANDOFF — M0093

## Status

M0093 implementation is complete within the authorized source boundary and is **operator review required**. The execution agent has not self-promoted the change.

Operator decision: `APPROVE` | `APPROVE-WITH-LIMITATIONS` | `REJECT`

## Objective executed

Built downstream runtime adapters for the canonical M0080 carousel and presentation storyboard programs. Carousel produces an Open Carrusel-compatible in-memory payload. Presentation produces deterministic Slidev `slides.md` and reveal.js `index.html` projections. Shared M0079/M0080 storyboard contracts remain authoritative; runtime syntax is downstream and replaceable.

## Implementation

1. `adapters/storyboard_runtime.py`
   - Defines immutable governed runtime handoff and artifact receipts.
   - Revalidates M0079 approval/compile evidence and identity lineage.
   - Re-runs the canonical M0080 program compiler and compares the full projected expression, not only its supplied digest.
   - Fails closed on stale/malformed evidence and unsafe asset URIs.
   - Carries CAE evidence/provenance into downstream HTML metadata.

2. `engines/carousel/runtime_adapter.py`
   - Implements `CarouselStoryboardRuntimeAdapter`.
   - Emits Open Carrusel-compatible `carousels[].slides[]` payload.
   - Preserves scene order, semantic purpose, evidence references and source assets.
   - Enforces the adopted Open Carrusel 20-slide maximum and 1:1 / 4:5 / 9:16 dimensions.
   - Produces no external storage/editor mutation.

3. `engines/presentation/runtime_adapter.py`
   - Implements `PresentationStoryboardRuntimeAdapter` for `slidev` and `revealjs`.
   - Preserves canonical presentation `build_order`.
   - Emits Slidev `v-click` build steps and reveal.js `.fragment` / `data-fragment-index` markers.
   - Emits pinned runtime expectations and explicit `native_reachability_proven=False`.

4. `tests/cae/test_m0093_storyboard_runtime_adapters.py`
   - Happy-path carousel compilation plus deterministic replay/idempotence.
   - Slidev and reveal build-order projection.
   - Good-looking-but-wrong semantic tampering rejected after canonical recompile comparison.
   - Missing operator authorization rejected.
   - Stale compile receipt rejected.
   - Malformed `javascript:` source URI rejected.

## Exact changed/new repository paths

```text
adapters/storyboard_runtime.py
engines/carousel/__init__.py
engines/carousel/runtime_adapter.py
engines/presentation/__init__.py
engines/presentation/runtime_adapter.py
tests/cae/test_m0093_storyboard_runtime_adapters.py
```

Boundary evidence: `M0093_boundary_check.txt` reports exactly six changed files and zero changes outside the allowed boundary.

## Authority / brownfield basis

The uploaded snapshot did not contain the mandate's requested root-relative authority locations verbatim in every case. The equivalent current synchronized paths used for audit include:

```text
governance/program-control/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md
governance/program-control/00_CONSTITUTION/current-v1.1/governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml
docs/PRD/CURRENT.md
docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md
docs/cae/CAE_Operational_Product_Campaign_M0058_M0068_v1/README.md
docs/cae/CAE_Operational_Product_Campaign_M0058_M0068_v1/18_BROWNFIELD_REFERENCE.md
docs/cae/CAE_Production_Convergence_M65_M72_v1/README.md
docs/cae/CAE_Production_Convergence_M65_M72_v1/07_PRODUCTION_OPERATOR_GATES/M72_final_production_gate_current_sync.md
docs/cae/CAE_Product_Brief/10_Media_Intelligence_Asset_Intelligence_Evidence_Retrieval.md
docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/00_REPOSITORY_TO_PRODUCT_BUILD_PLAN.md
docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/01_CAE_Product_Update_Visual_Asset_Editor.md
docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/02_CAE_PRD_Update_Visual_Asset_Studio.md
docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/03_CONSCIOUS_E_MOTION_EDITING_STANDARDS_v2.md
```

Existing M0080 canonical programs were reused rather than duplicated.

## External source mapping

See `M0093_EXTERNAL_UPSTREAM_MAPPING.md` for exact source file paths, pinned refs, licenses, adopted behavior and exclusions.

Open Carrusel audited commit: `8ba717ba4d59c8a9a5f64d278f6e83cbea34efde`.

Slidev audited release: tag `v52.19.1`; GitHub release page displayed commit `dbc307b`; MIT.

reveal.js audited release: tag `6.0.1`; GitHub release page displayed commit `52c6c8b`; MIT.

## Exact verification commands and observed results

### Focused regression suite

```text
PYTHONPATH=/mnt/data/m0093_test_bootstrap:packages/ca_runtime/src:packages/ca_contracts/src:. python -m pytest -q tests/cae/test_m0093_storyboard_runtime_adapters.py tests/cae/test_m0080_storyboard_program_contracts.py tests/cae/test_m0079_storyboard_session_revision.py
```

Observed: `13 passed, 14 warnings in 0.15s`.

### Source parse validation

AST parse of all six changed files: PASS.

### Baseline full-import limitation

```text
python -m pytest -q tests/cae/test_m0080_storyboard_program_contracts.py tests/cae/test_m0079_storyboard_session_revision.py
```

Observed during audit: collection stopped at `ModuleNotFoundError: No module named 'psycopg'`. An isolated import probe also found unavailable `cmf_pipeline` in unrelated package initialization. No application files outside M0093 scope were modified to bypass these dependencies.

### Environment fidelity

```text
Python 3.13.5
Node v22.16.0
npm 10.9.2
pnpm NOT_FOUND
slidev NOT_FOUND
ruff NOT_FOUND
`.git` metadata NOT_FOUND
```

Native Slidev/reveal.js/Open Carrusel execution was not available in the snapshot and is therefore not claimed.

## Evidence that the contract is governed

The adapter requires:

- a passing storyboard validation report,
- a `COMPILE_READY` compile receipt,
- matching workspace/session/revision/storyboard/program/harness identities,
- a valid receipt lineage digest,
- a canonical expression that exactly matches the current M0080 projection,
- safe source URIs before emitting source assets.

The implementation returns downstream artifacts only; it does not mutate revision state or operator feedback.

The contrastive test demonstrates that an expression can be made visually plausible while changing semantic purpose, and that such a tampered expression is rejected even when the stale expression carries a prior canonical digest.

## Limitations / operator gates

1. **Native runtime reachability:** not proven. The emitted artifacts are compatibility projections only.
2. **Perceptual acceptance:** not proven. The operator must inspect the real Slidev/reveal/Open Carrusel preview and confirm meaning, attention behavior, legibility and source lineage.
3. **Repository commit identity:** exact CAE commit SHA unavailable because the supplied snapshot has no Git history. The operator must record the actual tracked commit SHA after applying the six files.
4. **Tooling:** `ruff` unavailable; no ruff claim is made.
5. **Test bootstrap:** the focused suite uses test-only import isolation because unrelated repository dependencies are missing in the supplied environment.

## Rollback

Rollback is limited to the six M0093 additions listed above. No pre-existing file was overwritten. Because the snapshot has no Git history, rollback must be performed by removing/reverting these six paths in the operator's tracked worktree, preserving receipts/evidence and any later accepted state.

## Delivery bundle

- `M0093_EXTERNAL_UPSTREAM_MAPPING.md`
- `M0093_EVIDENCE_RECEIPT.json`
- `M0093_BASELINE_AND_LIMITATIONS.md`
- `M0093_test_run.txt`
- `M0093_python_parse_check.txt`
- `M0093_boundary_check.txt`
- `M0093_environment_and_runtime_reachability.txt`
- `M0093_CHANGED_FILES.patch`
- `M0093_CHANGED_FILES.paths.txt`
- `M0093_CHANGED_FILES.sha256`
- `cae_m0093_modified_repo.zip`

## Commit SHA

`UNAVAILABLE — uploaded snapshot has no .git metadata; operator must supply the real commit SHA after applying the change.`

## Final operator decision request

`OPERATOR_DECISION_REQUIRED: APPROVE | APPROVE-WITH-LIMITATIONS | REJECT`
