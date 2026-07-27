# ADR-007: Evidence Identity And Source Profiles

Status: `ACCEPTED`

Owners: Evidence architecture and source authority. Trace: D005, D007, D023; TS-02. External blocker: BD-004.

## Context

Builder decisions depend on exact target evidence. Path-based identity, generic profiles, mutable sources, and unregistered embedded references make provenance and saturation unreliable.

## Decision

Every run selects a versioned target-specific Source Profile and exact target candidate before initialization. Source bytes receive SHA-256 identity, immutable descriptors, authority/license/privacy metadata, stable specimen IDs, and an aggregate Source Lock. All evidence claims link to source spans and knowledge status.

## Alternatives

- Paths as identity: rejected because paths move and bytes change.
- Copy every source into the database: rejected for scale and media operations.
- One universal source checklist: rejected because targets require different evidence roles and readiness.

## Interfaces, Data, And Errors

Ports: source adapter, archive/media inspector, CAS, evidence index. Core records: `SourceProfile`, `SourceDescriptor`, `SourceLock`, `Specimen`, `EvidenceClaim`, `Gap`, `AuthorityConflict`, `SaturationContract`. Errors are typed for unsafe archive, missing role, hash mismatch, unsupported media, authority conflict, and insufficient saturation.

## Authority, Security, And Determinism

Deterministic tools hash, index, and validate. Agents may propose semantic tags but cannot promote authority. Sources are read-only. Archive traversal, symlink escape, decompression bombs, and mutable remote inputs fail closed.

## Consequences

Positive: portable provenance, exact invalidation, repeatable saturation. Cost: profile maintenance, media/CAS capacity, and source-authority review.

## Observability, Performance, Migration

Report files/bytes/specimens, cache hits, duplicates, gaps, conflicts, role coverage, and processing budgets. Changed hashes create a new lock and invalidate dependents. No V2.1 source-profile import applies.

## V1.2 Constitutional Alignment Amendment

The accepted evidence-identity decision is unchanged and now applies to conversational human-reaction evidence.

| Implementation owner | Component boundary | Data / contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- |
| evidence_architecture_and_source_authority | Originating content harness captures source truth; Builder registers, validates, redacts, and invalidates references | `ReactionReceipt`, `ExpressionMoment`, consent-policy ref, transcript/timecode span, withdrawal state | Quarantine missing consent/provenance; withdrawal invalidates dependent moments, proposals, and evaluations | consent, retention, redaction, span, and withdrawal fixtures | Every reaction/expression record is hash-addressed, policy-bound, access-controlled, and revocable | Additive source-profile fields; production authorization remains blocked by HD-006 and expanded BD-004 |

## Delegation RC3 Source-Kind Addendum

The accepted evidence-identity decision now binds Builder handoffs to the governed RC3 source-kind enumeration. Builder must derive source kind from authoritative evidence and fail closed when classification is ambiguous.

| Implementation owner | Component boundary | Data / contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- |
| evidence_architecture_and_source_authority | Builder maps evidence to an external Delegation field; Delegation retains schema authority | `SOURCE_PROVENANCE_MAPPING.yaml`, RC3 `/source_provenance/source_kind`, Reaction Receipt and Expression Moment refs | Reject unknown/guessed source kind, ambiguous operator-authored source, missing interview refs, or unreceipted legacy migration | exhaustive source-kind, ambiguous classification, interview conditional, optional non-interview refs, and migration receipt fixtures | All eight RC3 kinds are accepted only by rule; Interview Expression/ReelCast require both provenance arrays; non-interview arrays validate when supplied | Active pre-RC3 mappings are superseded; pre-source-kind records require owner classification and legacy records require a traceable lossless receipt |

## Verification

Security/property tests cover archives and identity; scale tests cover large descriptor sets; Format 02 cannot proceed without a ratified corpus and profile.
