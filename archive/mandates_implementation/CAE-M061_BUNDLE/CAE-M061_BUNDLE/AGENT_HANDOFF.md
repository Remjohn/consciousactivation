# CAE-M061 — Production Asset Demand / Resolution Contract

## Mandate ID & Title

**Mandate ID:** CAE-M061  
**Mandate Title:** Production Asset Demand / Resolution Contract  
**Requirement / Invariant:** INV-ASSET-DEMAND-001

The implementation establishes a typed, executable boundary in which an existing Production Semantic Program declares the physical media required by a scene. The asset layer validates candidate assets against those declarations. The runtime validates lifecycle transitions only; it does not infer or re-decide semantic meaning.

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/production-program/src/cae_production_program/domain.py` | Added typed `AssetDemandSpec` (media type/source, insert role, semantic role/obligation, duration, rights, evidence lineage); attached demands to `SemanticSceneSpec`; added `program_version`. | A Program can state the physical-media requirement and preserve the semantic obligation/provenance upstream. |
| `services/production-program/src/cae_production_program/compiler.py` | Validates demand duration, evidence reference, and evidence hash during Program compilation. | Invalid duration/provenance cannot enter the executable Program. |
| `services/production-program/src/cae_production_program/__init__.py` | Exports `AssetDemandSpec`. | The typed Program contract is importable from the canonical package surface. |
| `services/asset-intelligence/src/cae_asset_intelligence/demand_contract.py` | Added provider-neutral demand/resolution models, Program-to-demand translator, candidate/catalog resolver, duration/role/semantic/rights/workspace checks, and resolution outcomes. | Downstream resolution can accept the Program declaration without semantic re-selection; false-proof cases are blocked. |
| `services/asset-intelligence/src/cae_asset_intelligence/__init__.py` | Exports the M061 contract and resolver types. | The executable asset boundary is available from the asset package surface. |
| `packages/ca_runtime/src/ca_runtime/asset_demand_resolution.py` | Added lifecycle enum and transition validator with actor, preconditions, validator, postconditions, receipt, error route, and recovery route. | Runtime owns lifecycle validity only and explicitly preserves Program semantic authority. |
| `packages/ca_runtime/src/ca_runtime/__init__.py` | Exports the runtime lifecycle types. | The lifecycle guard is part of the runtime public surface. |
| `tests/production_program/test_asset_demand_emission.py` | Program-level contract tests, including invalid evidence and duration hard negatives. | Program demand emission is structurally and semantically constrained. |
| `tests/asset_intelligence/test_asset_demand_resolution_contract.py` | Integration-style translator/catalog tests plus wrong-semantic-role, provenance, duration, rights, and workspace negatives. | Field-level preservation and false-proof resistance are executable. |
| `tests/cae/test_asset_demand_resolution_runtime.py` | Lifecycle state transition tests. | Declared state machine and audit fields are enforced. |

## Files Added and Files Modified

### Files Added

- `services/asset-intelligence/src/cae_asset_intelligence/demand_contract.py` — canonical M061 provider-neutral demand/resolution contract, translator, and resolver.
- `packages/ca_runtime/src/ca_runtime/asset_demand_resolution.py` — runtime-only lifecycle validation for demand/resolution state.
- `tests/production_program/test_asset_demand_emission.py` — Program emission and hard-negative coverage.
- `tests/asset_intelligence/test_asset_demand_resolution_contract.py` — demand/resolution integration and false-proof coverage.
- `tests/cae/test_asset_demand_resolution_runtime.py` — runtime lifecycle coverage.

### Files Modified

- `services/production-program/src/cae_production_program/domain.py` — adds typed demand requirements to existing semantic scenes without changing downstream meaning authority.
- `services/production-program/src/cae_production_program/compiler.py` — enforces demand/evidence consistency.
- `services/production-program/src/cae_production_program/__init__.py` — exports the new typed model.
- `services/asset-intelligence/src/cae_asset_intelligence/__init__.py` — exports M061 contract/resolution APIs.
- `packages/ca_runtime/src/ca_runtime/__init__.py` — exports M061 lifecycle APIs.

No unrelated repository paths were modified.

## Exact paste instructions and post-apply commands

1. From the repository root, copy the files in this bundle to the exact relative paths listed above, preserving directories.
2. No database migration is required. No generated schema/code artifact requires regeneration for this implementation.
3. Install/update the two directly affected service packages in the normal repository environment:
   `python -m pip install -e services/asset-intelligence -e services/production-program`
4. The runtime package already declares its existing repository dependency requirements in `packages/ca_runtime/pyproject.toml`; use the repository's standard runtime environment for that package.
5. Run the exact verification command below.

## Test Command

`pytest -q tests/asset_intelligence tests/production_program tests/cae/test_asset_demand_resolution_runtime.py`

## Expected Test Results

**23 automated tests, all passing.**

Observed result in the execution sandbox:

`23 passed in 0.08s`

Additional syntax verification passed with:

`python -m py_compile services/asset-intelligence/src/cae_asset_intelligence/demand_contract.py services/asset-intelligence/src/cae_asset_intelligence/domain.py services/asset-intelligence/src/cae_asset_intelligence/__init__.py services/production-program/src/cae_production_program/domain.py services/production-program/src/cae_production_program/compiler.py services/production-program/src/cae_production_program/__init__.py packages/ca_runtime/src/ca_runtime/asset_demand_resolution.py`

## Evidence / limitations

**What the verifier measures:** typed field preservation from `SemanticProgram` demand declarations into `ProductionAssetDemand`; workspace/candidate/program provenance continuity; media/source/role/semantic-role/duration/rights matching; and governed lifecycle transitions.

**False-proof countercase exercised:** a candidate asset with valid physical media and duration but the wrong semantic role is blocked with `SEMANTIC_OBLIGATION_MISMATCH`; altered evidence hash is blocked; out-of-range duration and insufficient rights evidence are blocked.

**What it does not measure:** retrieval quality, provider selection, media-byte cryptographic verification of a real corpus at runtime, visual quality, or downstream rendering. Those belong to later asset retrieval/selection/production mandates.

**Environment-fidelity limitation:** the sandbox does not have the existing `psycopg` dependency required by the current `ca_runtime` package initializer. Installing it from the network was unavailable. The new runtime lifecycle test therefore loads only the scoped M061 runtime module directly so the M061 state-machine logic can still be executed deterministically; the package-level `import ca_runtime` remains dependent on the repository's declared runtime environment.

**Control state / commit:** the uploaded repository archive has no `.git` directory, so a new local implementation commit could not be captured without fabricating repository history. The GitHub baseline commit inspected for the supplied mandate/repository was `e8696a23b867c336636f14496f8174f3771c77af`. No remote repository write was performed by this execution. The operator gate remains required.

**Operator decision required:** Do you accept M061 and authorize M0062/M0063?
