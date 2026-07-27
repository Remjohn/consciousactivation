# Delegation 1.1.0-rc.2 Source Provenance Drift Report

Date: 2026-07-14  
Report status: COMPLETE  
Baseline disposition: FROZEN AND RETAINED UNCHANGED  
Release action: NEW IMMUTABLE CANDIDATE REQUIRED FOR THE SOURCE CORRECTIONS

## Scope and immutable-release control

This investigation is limited to the five declarations whose hashes changed after the `1.1.0-rc.2` source manifest was generated. The frozen repository-local and Program Control copies of `1.1.0-rc.2` were not edited, regenerated, or overwritten.

The previous hashes below are the hashes recorded in the RC2 source manifest and present in both frozen RC2 copies. The current hashes are from the corresponding files in the mutable producer checkout.

## Changed source paths

### 1. `packages/contracts/package.json`

- Previous/RC2 hash: `sha256:6ca287a2c43a58733bf5de3d9f4eaa899ac62389c799f9f705c50ebd940082a4`
- Current producer hash: `sha256:32b7e09da7cd0aae9b57dca2669c21563d16bb4fc3ea6d4e50aa7c9eb7e4decd`
- Reason: corrected the Node package version declaration from `1.1.0-rc.1` to `1.1.0-rc.2` so package metadata agrees with the release identity.
- Distributed in RC2: **Yes**, as `contracts/package.json`.
- Protocol runtime behavior affected: **No**.
- Release behavior or compatibility affected: **Yes**. Package identity and package-manager compatibility metadata differ from the immutable RC2 file.

### 2. `packages/contracts/pyproject.toml`

- Previous/RC2 hash: `sha256:d9cce799563b0298971785aed87a4457ffbb58502869ae63b52871232213ad6d`
- Current producer hash: `sha256:fe1841ba74db9d86de5286a1f1fa9a044c387316d48b9e8d35d2d5001158a025`
- Reason: corrected the Python contracts package version declaration from `1.1.0rc1` to `1.1.0rc2` so Python packaging metadata agrees with the release identity.
- Distributed in RC2: **Yes**, as `contracts/pyproject.toml`.
- Protocol runtime behavior affected: **No**.
- Release behavior or compatibility affected: **Yes**. Python package identity and installation metadata differ from the immutable RC2 file.

### 3. `packages/validators/pyproject.toml`

- Previous/RC2 hash: `sha256:b270a697b5abaae998751a226bf138f6c7fb12dbf8fe8465e17149fbbe889b15`
- Current producer hash: `sha256:a7d1996a887324edb8349bd87915d051f2f2d2fc5ffc5796e968668c7b61ea43`
- Reason: corrected the Python validators package version declaration from `1.1.0rc1` to `1.1.0rc2` so validator packaging metadata agrees with the release identity.
- Distributed in RC2: **Yes**, as `validators/pyproject.toml`.
- Protocol runtime behavior affected: **No**.
- Release behavior or compatibility affected: **Yes**. Validator package identity and installation metadata differ from the immutable RC2 file.

### 4. `packages/validators/tests/test_contracts.py`

- Previous/RC2 hash: `sha256:13d8a88c9927176e903266101e532fae84f78bd4edc52ded1dbdbc8884143552`
- Current producer hash: `sha256:b416a11974dcb78823bab5920ec913960cc681efb768971a8569dda159279156`
- Reason: added deterministic assertions that the registry, Node package declaration, and both Python package declarations all identify `1.1.0-rc.2`/`1.1.0rc2`.
- Distributed in RC2: **Yes**, as `validators/tests/test_contracts.py`.
- Protocol runtime behavior affected: **No**.
- Release behavior or compatibility affected: **Yes**. The strengthened conformance test detects the stale identity declarations shipped in RC2; the RC2 copy does not include this assertion.

### 5. `packages/validators/run_release_validation.py`

- Previous/RC2 hash: `sha256:43362da0f990bde352c498c9a016ac25967ff55594c8bd903173cc3a6a6c40cb`
- Current producer hash: `sha256:032f710093086641e39b89e7211c341b7f65e0262335dec7fb543a99bf2abee5`
- Reason: added release-identity consistency enforcement across the receipt, release manifest, contract registry, compatibility manifest, Node package declaration, and Python package declarations.
- Distributed in RC2: **Yes**, as `validators/run_release_validation.py`.
- Protocol runtime behavior affected: **No**.
- Release behavior or compatibility affected: **Yes**. The strengthened validator changes release-validation behavior and would reject the inconsistent package declarations in the frozen RC2 candidate.

## Findings

1. The mutable producer checkout has exactly five source-manifest hash drifts, all listed above.
2. Each changed source file has a distributed counterpart in `1.1.0-rc.2`.
3. No schema, generated semantic type, fixture, migration, compatibility rule, or protocol-engine implementation changed in this drift set.
4. Delegation lifecycle behavior, semantic lineage behavior, authority enforcement, idempotency, replay, cancellation, amendment, supersession, replacement, and Delegation Set behavior are not changed by these five source edits.
5. Release identity/packaging metadata and release-validation behavior are affected. This is sufficient to prohibit back-porting the changes into the immutable RC2 directory.
6. RC2 remains the current locally validated and VAE-adopted shared-contract baseline, but it remains unsigned and not production-authorized.

## Immutable baseline verification

- Repository-local RC2 path: `D:/Work/CONSCIOUS_ACTIVATIONS/03_DELEGATION_PROTOCOL/delegation-contracts/1.1.0-rc.2`
- Program Control RC2 path: `D:/Work/CONSCIOUS_ACTIVATIONS/CMF_PROGRAM_CONTROL/02_CROSS_REPO_CONTRACTS/delegation-contracts/1.1.0-rc.2`
- Release digest: `sha256:d4958cd3d02f0acef9d66bf245078ea70dab36b727d0c1541031fdceb63f6e41`
- Release manifest SHA-256 in both copies: `sha256:6e765eeef4ebed71d6e725cf11f49815f9cc0cafbe42ef157c8f189d8c7d582c`
- Release receipt SHA-256 in both copies: `sha256:ff97185ec1dfd1c2eaf936beec318e28b583fd2e3da809df9b860f504c7b6cff`
- Distributed RC2 modified by this investigation: **No**.

## Decision and recommendation

Because distributed files are affected, `1.1.0-rc.2` must not be mutated. Retain RC2 unchanged as historical evidence and as the frozen current local shared-contract baseline. When a corrected candidate is authorized, publish the five reconciled declarations and regenerated hashes as a new immutable release candidate, recommended version `1.1.0-rc.3`.

Feature development remains frozen. Production authorization remains false until the existing trust, signing, and operational blockers are closed.
