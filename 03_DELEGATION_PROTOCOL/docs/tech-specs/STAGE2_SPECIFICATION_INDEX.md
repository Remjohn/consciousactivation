---
title: Stage 2 Delegation Specification Index
product: CMF Content Harness Visual Asset Editor Delegation Protocol
stage: 2
status: complete_with_concerns
created: 2026-07-14
---

# Stage 2 Specification Index

## Specification set

| Spec | Primary ownership | Decisions | Status |
|---|---|---|---|
| TS-DLG-01 | FR-001..008, FR-017..024; 4 NFRs | D001, D003 | Draft for review |
| TS-DLG-02 | FR-009..016, FR-105..106, FR-110..111; 8 NFRs | D002, D014 | Draft for review |
| TS-DLG-03 | FR-025..032, FR-107..109, FR-112; 12 NFRs | D004, D014 | Draft for review |
| TS-DLG-04 | FR-081..088; 6 NFRs | D011 | Draft for review |
| TS-DLG-05 | FR-033..040, FR-049..064, FR-089..096; 8 NFRs | D005, D007, D008, D012 | Draft for review |
| TS-DLG-06 | FR-041..048, FR-097..104; 4 NFRs | D006, D013 | Draft for review |
| TS-DLG-07 | FR-073..080; 3 NFRs | D010 | Draft for review |
| TS-DLG-08 | FR-113..115; 10 NFRs | D015 | Draft for review |
| TS-DLG-09 | FR-065..072, FR-116..119, FR-121..125, FR-127..128; 5 NFRs | D009, D014, D015, D016 | Draft for review |
| TS-DLG-10 | FR-120, FR-126; verification overlay over all requirements | D016 | Draft for review |

Mechanical allocation result: 128 unique FRs and 60 unique NFRs, with no missing, extra or duplicate primary owners.

## Normative corrections

- Replace the conditional `submission-receipt` with protocol-owned submission validation and VAE-owned admission facts.
- Remove downstream consumption authorization from the VAE-owned result contract; establish it only through acknowledgement.
- Replace bare demand strings with an exact ID/version/hash/canonical-reference object.
- Close all public nested schema objects or register governed extension namespaces.
- Use RFC 8785 canonical JSON, SHA-256 payload/receipt hashes and Ed25519 as the Release 1 signature baseline.
- Serialize lifecycle effects per correlation and separate idempotent retries from hostile replay.
- Preserve immutable history through cancellation, supersession, invalidation, revocation and replacement.
- Extend the existing Harness Control Tower through source-linked projections rather than a second authority store.

## V1.1 alignment disposition

TS-DLG-01, 02, 03, 04, 05, 08, 09, and 10 carry narrow constitutional
amendments for version signaling, exact lineage authority, behavioral
compatibility, traceable migration, audit evidence, and the five required
conformance proofs. TS-DLG-06 and 07 are unaffected. No lifecycle, Delegation
Set, result-governance, or transport decision was reopened.

## Historical Stage 2 verdict

`CONCERNS`. The ten technical specifications are complete enough for architecture review and Stage 3 contract work. Contract publication remains blocked until upstream schema/product owners ratify the corrections, schemas are closed and canonicalized, product/Control Tower/storage interfaces are supplied, and executable conformance evidence exists. Stage 5 implementation remains unauthorized.
