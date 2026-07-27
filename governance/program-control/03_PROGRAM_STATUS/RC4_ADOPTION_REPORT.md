# Delegation RC4 Bounded Adoption Report

Date: 2026-07-15  
Release: `delegation-contracts@1.1.0-rc.4`  
Remediation result: **COMPLETE — pending a fresh read-only convergence audit**

## Release validation gate

RC4 passed the hard stop gate before consumer remediation began. Program Control and Delegation contain identical 164-file distributions; all 163 release-receipt entries match their declared SHA-256 and size. The clean extracted package passes 83 validator tests and 35 protocol tests and does not depend on repository layout or unshipped cache files.

| Identity | Value |
|---|---|
| Release digest | `sha256:c614a4d9b705e382456f4d6cd1cd6b7bcbc892517a22b358950db7404e3b4c44` |
| Release receipt | `sha256:042ab1ad99a4e5a4f8ff3a08c559b410db9c17cbade48ef05e92d6170dddc25f` |
| Release manifest | `sha256:7a23c0896f215c008bd2f9f0f7079cb97c23d05d100ac5a4b60691bb8abb9882` |
| Compatibility manifest | `compatibility/manifest.json`, `sha256:51667cd6c346c6794c2b648d0369b6961fc9519fd2d5e52ac03589a2a24d32cd` |
| Compatibility profile | `cmf-delegation-compatibility-profile-1-0@1.0` |
| Trust | `local_unsigned_release_candidate` |
| Production eligibility | `false` |

RC3-to-RC4 comparison confirmed that the Visual Asset Demand bytes are unchanged. The bounded semantic addition is portable derivative-lock inheritance structure and enforcement, with its schema, validator, generated declarations, fixtures and migration.

## Consumer adoption

Builder now pins the exact RC4 identity, preserves source/provenance and Activative lineage, emits RC4-complete derivative parent-lock evidence, and uses the governed Format 02 canonical identifier. Its bounded integration validator passes. The 410 obligations, 12 Epics and 69 Stories were not regenerated; Step 4 was not started.

VAE independently pins and validates RC4, preserves unaffected adapters, enforces derivative inheritance, and declares the required `EVALUATE` capability for deterministic, independent VLM, composition, wrong-reading, Feature Contract and derivative-lock evaluation. Its integration suite passes 14/14. Unsupported evaluation requirements fail closed. The evaluator remains `specified_not_certified`, production certification is false, and Stage 5 was not started.

## Format 02 governance

The Builder V1.2 canonical identifier is `format02_minimal_coach_theatre`. The shared `FORMAT02_PROFILE_ALIAS_REGISTRY.yaml` preserves `minimal_coach_theatre` only as a deprecated historical compatibility alias for read/migration. New active emissions use only the canonical ID.

The strongest justified state is `contract_compatible`: the profile remains the Release 1 reference, but it is not benchmarked, limited-production-certified or production-certified.

## Program status

- RC1: historical consumer rejection.
- RC2: historical convergence rejection.
- RC3: historical convergence rejection.
- RC4: current local unsigned release candidate.
- Builder: Step 3 complete; Step 4 not started; implementation readiness false.
- VAE: RC4 adopted locally; evaluator not certified; compute/recovery/readiness blockers open; Stage 5 unauthorized.
- Delegation: locally validated; feature development frozen; signing/publication pending; production authorization false.

All 11 dimensions that failed the previous RC3 audit now have bounded corrective artifacts and validation evidence in `CONVERGENCE_REMEDIATION_REGISTER.yaml`. This report does not rerun or replace that audit. The last formal verdict remains `FAIL` until a fresh read-only convergence audit is performed.

## Next permitted action

Run the fresh read-only cross-repository convergence audit against exact RC4 bytes. Do not begin Builder Step 4, VAE Stage 5, or production implementation/publication through this remediation receipt.
