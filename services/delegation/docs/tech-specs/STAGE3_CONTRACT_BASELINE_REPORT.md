---
title: Stage 3 Contract Baseline Report
product: CMF Content Harness Visual Asset Editor Delegation Protocol
stage: 3
status: constitutionally_aligned_local_pass
created: 2026-07-14
---

# Stage 3 Contract Baseline Report

## Scope

Stage 3 created a transport-neutral shared-contract release candidate. It did
not implement protocol delivery, persistence, product adapters, Content
Harness behavior, VAE production behavior, or Control Tower projections.

## Baseline Inventory

| Package | Evidence | Result |
|---|---|---|
| Contracts | `packages/contracts/` | 26 active closed schemas, 26 examples, canonical registry, authority registry, lifecycle registry, generated Python and TypeScript bindings |
| Validators | `packages/validators/` | Deterministic canonicalization, schema, authority, lifecycle, compatibility, and fixture validation |
| Fixtures | `packages/fixtures/` | 10 Format 02 reference scenarios plus compatibility and negative inputs |
| Compatibility | `packages/compatibility/` | Behavioral release-candidate manifest, lossless adapters, owner-evidenced submission split, and Visual Asset Demand V1-to-V1.1 migrations |
| Release metadata | `CONTRACT_CHANGELOG.md`, `COMPATIBILITY_MANIFEST.yaml` | Versioned changes, publication status, blockers, and integrity policy |
| Pinning | `packages/contracts/release-manifest.json` | SHA-256 hash for every Stage 3 package file |

## Normative Corrections Implemented

- Advanced only Visual Asset Demand to message `1.1` while preserving envelope
  protocol `1.0` and package versioning at `1.1.0-rc.1`.
- Added exact Activative Intelligence Pack, Identity DNA, Context Premise,
  Resonance, Matrix of Edging, Activative Call, Reaction Receipt, and Expression
  Moment lineage plus the complete constitutional visual contract.
- Made wrong-reading locks non-empty and made parse-only or evaluator-free
  compatibility fail closed.

- Protocol validation and VAE admission are separate owner-specific receipts.
- The VAE result cannot authorize downstream consumption.
- Exact demand identity is mandatory across related messages.
- Public objects are closed and public lifecycle state is typed.
- Message producers use registered principal types; wrapper and failure facts
  bind authority dynamically to the signing principal.
- Canonical JSON uses the RFC 8785 safe-integer profile, SHA-256 hashes, and an
  Ed25519 publication requirement.

## Executable Evidence

The local conformance suite covers schema validity and closure, registry and
release hashes, authority ownership, envelope signer identity, lifecycle
legality, scenario continuity, compatibility negotiation, deterministic legacy
adaptation, and rejection of unsafe canonical values.

Verification on 2026-07-14:

- `python packages/contracts/tools/build_baseline.py`: generated 26 contracts
  and 10 Format 02 scenarios.
- `python -m unittest discover -s packages/validators/tests -v`: 51 tests
  passed with no failures.
- `python -m pytest packages/protocol/tests -q -p no:cacheprovider`: 30 tests
  passed, including the original 24-test regression floor.
- `packages/contracts/release-manifest.json`: 145 contract, fixture,
  compatibility, validator, and protocol files hash-pinned.

## Remaining Publication Blockers

- XRI-001 and XRI-002: immutable upstream source artifacts and implementation
  repositories are unavailable, so owner reconciliation and adapter proof
  cannot be completed.
- XRI-013 and XRI-014: Format 02 product releases and the existing Control
  Tower projection contract are unavailable.
- XRI-015 through XRI-017: trust roots, transport ports, and operational state
  ownership remain unassigned across repositories.
- This checkout has no Git repository, so an immutable tag cannot be created.
- The release candidate has no owner signature or upstream ratification.

## Verdict

`PASS` for the local constitutional contract baseline and executable reference
conformance. `CONCERNS` for external publication and `FAIL` for production
readiness: the unsigned release candidate is suitable for owner review and
upstream reconciliation but is not a production-authorized baseline.
