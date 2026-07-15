# RC2 Consumer-Failure Correction Report

Date: 2026-07-14  
Rejected candidate: `1.1.0-rc.1`  
Replacement candidate: `1.1.0-rc.2`  
Rejecting consumer: Visual Asset Editor  
Failure class: semantic enforcement and release packaging  

## Reproduced failure

The VAE report hash is
`sha256:9672522c37b8d171863fd3860e6f783e559ab1f63e0d08af47140c2ed6faeba2`.
RC1 identity, receipt inventory, and hashes validate. Its source manifest lists
11 `.pytest_cache` entries omitted from the clean release. Direct execution of
the shipped validator suite from the flattened release fails because path
discovery resolves a non-existent external `packages/...` tree. The RC1 demand
schema also rejects `source_kind`, permits empty Reaction Receipt and Expression
Moment arrays, and cannot conditionally enforce interview provenance.

RC1 is retained unchanged as historical evidence and is classified
`consumer_rejected`, not production-compatible.

## Contract correction

RC2 establishes the single canonical path
`source_provenance.source_kind`. `source_provenance` and its governed enum
discriminator are mandatory on every Visual Asset Demand. Supported values are:

- `interview_expression`
- `public_comment`
- `direct_message_reply`
- `authored_source`
- `live_premise`
- `research_synthesis`
- `operator_supplied`
- `legacy_migrated`

When the kind is `interview_expression`, both
`activative_semantic_lineage.reaction_receipt_refs` and
`activative_semantic_lineage.expression_moment_refs` are required and non-empty.
For other source kinds they are optional, but supplied collections and identity
references remain fully validated. The Delegation Protocol validates and
preserves these fields; it does not infer or manufacture them.

## Migration correction

The migration from a pre-discriminator V1.1 demand returns
`SOURCE_KIND_CLASSIFICATION_REQUIRED` when no authoritative classification is
supplied. Only explicit Content Harness classification can create an immutable
successor. Interview classification without both provenance collections returns
`INTERVIEW_PROVENANCE_REQUIRED`; no default source kind or missing reference is
synthesized.

## Packaging correction

- Internal registry, fixture, validator, and protocol paths are release-root
  relative.
- Source-only files are recorded separately and are not release dependencies.
- Cache, bytecode, temporary, editor-swap, and operating-system metadata are
  excluded and rejected by manifest validators.
- The canonical release manifest is generated after staging from the actual
  release directory.
- Manifest and receipt validators require exact file-set, size, and SHA-256
  equality.
- A clean-room harness copies only the sealed candidate to a temporary directory
  and runs shipped validation, the full validator suite, and the full protocol
  suite without access to the source checkout.

## Preservation

No lifecycle or transport architecture was replaced. Existing authority,
integrity, replay, idempotency, cancellation, amendment, supersession,
replacement, and Delegation Set behavior remains under regression coverage.
Production authorization remains false while trust, signing, and operational
blockers remain open.
