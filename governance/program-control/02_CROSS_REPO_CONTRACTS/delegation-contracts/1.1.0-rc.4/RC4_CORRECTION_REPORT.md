# Delegation 1.1.0-rc.4 Portable Derivative-Lock Correction Report

historical_evidence: true

Date: 2026-07-15  
Correction class: PORTABLE_DERIVATIVE_LOCK_INHERITANCE_ENFORCEMENT  
Predecessor status: `1.1.0-rc.3` convergence rejected  
Production authorization: false

## Corrected behavior

RC4 adds the closed `derivative-lock-inheritance@1.0` contract. It pins the
authoritative parent resource, parent contract version, governing authoritative
demand, inline or immutable parent lock evidence and hash, derivative resource,
derivative lock set, derivation type, semantic classification, and optional
authoritative lock authorization.

The release-only validator compares stable lock IDs, canonical meaning hashes,
scope paths, and enforcement levels. Exact inheritance and stricter additions
pass. Removal, weakened meaning/scope/strength, missing parent evidence,
ambiguous classification, and semantic shortcutting fail with typed outcomes.
An authorized relaxation is valid only when a new immutable demand version
explicitly supersedes the governing demand and supplies the applicable lock
set. The validator never invents locks or determines their semantic content.

## Compatibility and migration

Consumers claiming derivative asset-flow support must declare both `PRESERVE`
and `ENFORCE` with evidence. `PARSE` alone is incompatible. The adapter gate
requires exact preservation of parent, derivative, classification, and lock
authorization evidence. Legacy derivative relationships are not classified or
populated automatically; they return `DERIVATION_CLASSIFICATION_REQUIRED` or
`PARENT_LOCK_EVIDENCE_REQUIRED` until authoritative inputs are supplied.

## Preservation from RC3

The Visual Asset Demand schema and VAE boundary fixtures remain byte-identical
to the RC2/RC3 semantic baseline. Envelope protocol `1.0`, Visual Asset Demand
`1.1`, compatibility profile `1.0`, source-kind and interview provenance,
Activative lineage, authority, lifecycle, acceptance, acknowledgement,
idempotency, replay, cancellation, amendment, supersession, replacement, and
Delegation Set behavior are unchanged.

## Conformance

- Source validator suite: `83 passed`.
- Source reference-protocol suite: `35 passed`.
- Existing RC3 regression behavior: preserved and passing.
- Clean extracted release-only rehearsal: `PASS` (27 examples, 47 fixture JSON
  files, 4 migration declarations, 83 validator tests, 35 protocol tests,
  zero stale declarations, and zero transient files).
- Signature status: `UNSIGNED`.
- Production authorized: `false`.
