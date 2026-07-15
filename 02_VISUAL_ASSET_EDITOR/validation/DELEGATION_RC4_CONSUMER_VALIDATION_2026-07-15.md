# Delegation RC4 VAE Consumer Validation

Date: 2026-07-15  
Consumer: CMF Visual Asset Editor  
Release: `1.1.0-rc.4`  
Verdict: **PASS — local contract adoption only**

## Immutable release identity

- Release digest: `sha256:c614a4d9b705e382456f4d6cd1cd6b7bcbc892517a22b358950db7404e3b4c44`
- Release-receipt hash: `sha256:042ab1ad99a4e5a4f8ff3a08c559b410db9c17cbade48ef05e92d6170dddc25f`
- Release-manifest hash: `sha256:7a23c0896f215c008bd2f9f0f7079cb97c23d05d100ac5a4b60691bb8abb9882`
- Compatibility profile: `cmf-delegation-compatibility-1.1.0-rc.4`
- Trust status: `local_unsigned_release_candidate`
- Production eligibility: `false`

The Program Control and Delegation RC4 distributions contain the same 164 release files. Every release-receipt entry matched its declared size and SHA-256 value. Clean extracted-layout validation passed without repository-relative imports or unshipped cache dependencies.

## RC3-to-RC4 comparison

The Visual Asset Demand schema remains byte-identical. RC4 adds the portable derivative-lock inheritance contract, validator, generated declarations, fixtures, migration and manifest coverage. Existing VAE adapters and mappings outside this semantic addition remain preserved.

## Consumer assertions

The VAE RC4 integration suite passed 14 of 14 tests. It proves:

- exact RC4 identity and receipt coverage;
- source-kind and interview-expression provenance enforcement;
- lossless request/result mapping;
- declaration of the required `EVALUATE` capability and every required evaluation domain;
- rejection of unsupported evaluation-profile requirements;
- enforcement of parent-lock inheritance and exact derivative evidence;
- use of the shared Format 02 alias registry;
- separation of capability availability from evaluator certification and production authorization;
- continued Stage 5 prohibition.

The evaluator remains `specified_not_certified`. The capability is specified and contract-compatible, but it does not establish approved empirical thresholds, evaluator certification or production fitness.

## Corrective artifacts

| Artifact | SHA-256 |
|---|---|
| `contracts/integration/DELEGATION_CONTRACT_PIN.yaml` | `779679fb359a7cb57d76c45316f2709ceffede4c822f6a7cf4dd53b2cc3d4221` |
| `contracts/integration/DELEGATION_RC4_COMPATIBILITY.yaml` | `66d22de20736e1cb93b754e56ac668fe4c23c68ae40c0dab4092c54f81bdb75a` |
| `contracts/integration/DERIVATIVE_LOCK_INHERITANCE_MAPPING.yaml` | `e953c288b651d4ede90b9f1ba8e1223fbfdde79f4d42534a9cb84d78e512413e` |
| `contracts/integration/BOUNDARY_ADAPTER_MANIFEST.yaml` | `bc6c0e28ab37d47a270691e73fe1a55dfff861d9a3959812ba63ea530f4dc58e` |
| `validation/fixtures/delegation-rc4/VAE_RC4_BOUNDARY_CASES.json` | `ee1834902587e569d5209041f2a50ad88cfb1f939f977c1aa7927a3df2d83d2e` |
| `validation/tests/test_delegation_rc4_integration.py` | `647a3430ff2316e983b7a99c70422703b63947d1dc652d0a0085fff0e2450d8b` |
| Shared Format 02 alias registry | `21ad1a618361a14ec62576ce4e1d7ce3c7267e3bd77a1004aa8b996d51c87d57` |

## Authorization boundary

This validation is bounded consumer-conformance evidence. Stage 5 remains not started and unauthorized; compute, recovery/rollback, real end-to-end evidence, evaluator certification, release signing and publication remain open.
