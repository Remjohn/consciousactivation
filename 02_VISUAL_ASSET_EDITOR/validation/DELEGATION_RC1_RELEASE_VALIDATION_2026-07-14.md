# Delegation 1.1.0-rc.1 Release Validation

Date: 2026-07-14  
Consumer: CMF Visual Asset Editor  
Candidate path: `D:/Work/CONSCIOUS_ACTIVATIONS/CMF_PROGRAM_CONTROL/02_CROSS_REPO_CONTRACTS/delegation-contracts/1.1.0-rc.1`  
Gate verdict: **FAIL**

## Observed identity and trust

| Item | Expected | Observed | Result |
|---|---|---|---|
| Package version | `1.1.0-rc.1` | `1.1.0-rc.1` | PASS |
| Release digest | `sha256:8bf07bd5b51b11d77b6852678967e439f019219d247b4c999877379196fd4e56` | exact match | PASS |
| Release receipt hash | `sha256:39250ccc3f148f885b24e0f459ed8139f5695878c151ec6b3371d1c3a477cdbe` | exact match | PASS |
| Source manifest hash | `sha256:a323851203841a09ae29fc89f2fe4b6f74206d2cc4964866a3826fe36fec7217` | exact match | PASS |
| Trust | `local_unsigned_release_candidate` | receipt says `UNSIGNED`; production authorization false | PASS |

The identity is observed, not adopted as a VAE dependency pin. No production trust or authorization is claimed.

## Artifact validation

| Check | Result | Evidence |
|---|---|---|
| Release receipt inventory | PASS | All 138 files excluding the receipt are present; byte counts and SHA-256 values match; no unlisted release file exists |
| Source-manifest artifact hash | PASS | File hash matches the expected source provenance hash |
| Source-manifest reproducibility against release | FAIL | The source manifest lists 11 `packages/protocol/.pytest_cache/**` and `packages/validators/.pytest_cache/**` files that the release receipt correctly does not contain |
| Registered schemas and examples | PASS | 26 registered examples validate; public schemas are closed |
| Generated Python types | PASS, structural | Source compiles without writing bytecode |
| Generated TypeScript types | PASS, structural | Expected Visual Asset Demand interface exists and delimiters are balanced |
| Fixture JSON | PASS | 31 fixture files parse |
| Migration declarations | PASS | Two migration declarations parse |
| Compatibility and migration tests | PASS | 13 of 13 focused validator compatibility tests pass |
| Protocol tests | PASS | 30 of 30 pass in a reconstructed source-layout harness |
| Full validator suite | FAIL | 50 of 51 pass; release-manifest pinning test fails on the 11 omitted cache artifacts |

The released validator modules also assume a source checkout at `packages/contracts`, `packages/fixtures`, and `packages/compatibility`, while the release candidate is flattened to `contracts`, `fixtures`, and `compatibility`. Validation therefore required a temporary, non-repository source-layout harness; no release artifact was changed.

## Mandatory semantic-enforcement validation

### H-002 interview-derived applicability — FAIL

The approved policy requires a typed `source_kind`. When `source_kind` is `interview_expression`, Reaction Receipt and Expression Moment provenance is mandatory; other source kinds explicitly permit absence. VAE must never infer the source class.

The candidate cannot express or enforce this policy:

- `visual-asset-demand.schema.json` contains no `source_kind`;
- `activative_semantic_lineage.reaction_receipt_refs` and `expression_moment_refs` are required arrays but have no `minItems`, so both can be empty and the payload validates;
- adding `source_kind: interview_expression` fails because the object is closed;
- generated Python and TypeScript bindings contain no `source_kind`;
- the published compatibility suite does not test this discriminator or conditional requirement.

This is parse-without-enforcement compatibility and is rejected.

### H-003 wrong-reading-lock inheritance — policy resolved, integration not attempted

The VAE can enforce parent-lock inheritance for internal deterministic variants without rewriting the shared demand. That bounded mapping and its positive/negative tests were not created because the release failed the preceding gate.

### H-004 Feature Contract ownership — shared schema shape acceptable, integration not attempted

The candidate uses typed, versioned `ResourceIdentityRef` values under `feature_contracts` and assigns field authority to `CONTENT_HARNESS`. This supports the approved ownership rule. VAE realization/feasibility/receipt mappings were not created because the release failed the preceding gate.

## Gate disposition

- Candidate identity: observed, not pinned.
- Trust status: `local_unsigned_release_candidate`.
- Batch B: **BLOCKED BEFORE INTEGRATION**.
- Boundary adapters, request/result mappings, compatibility manifests, integration fixtures, contract tests, and version pins: unchanged.
- Shared Delegation schemas: unchanged; no VAE fork created.
- Batch D rerun: not performed because Batch B did not pass.
- Stage 5: not started and not authorized.

## Required Delegation reissue

1. Add a typed `source_kind` discriminator and conditional `interview_expression` provenance requirements to the canonical demand.
2. Regenerate schemas, Python/TypeScript types, examples, authority paths, compatibility fixtures, migration declarations, and release receipt.
3. Add positive and negative tests proving interview provenance is mandatory only for the typed interview source kind and cannot be inferred.
4. Remove transient pytest cache entries from the source manifest, or include a coherent self-validating source package without making cache state a release artifact.
5. Make validator path discovery release-layout safe and publish a 51/51 or greater passing validation report for the exact reissued digest.
