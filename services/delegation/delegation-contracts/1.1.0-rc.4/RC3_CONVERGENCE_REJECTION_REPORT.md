# Delegation 1.1.0-rc.3 Convergence Rejection Report

historical_evidence: true

Date: 2026-07-15  
Rejected release: `delegation-contracts@1.1.0-rc.3`  
Failure class: portable derivative wrong-reading-lock inheritance enforcement  
Replacement candidate: `delegation-contracts@1.1.0-rc.4`  
Production compatibility: false

## Audit finding

The final cross-repository convergence audit found that RC3 preserved
wrong-reading locks inside authoritative demands but did not ship a portable,
release-only relationship contract and validator able to prove that a
derivative retained every authoritative parent lock without weakening its
meaning, scope, or enforcement strength. Parsing the existing fields therefore
could not establish derivative-flow behavioral compatibility.

## Preserved RC3 evidence

- Release digest: `sha256:e3100f9b3ec5db4077def2861128795451085bb8993f1fe318f5aaf6a6653cdf`
- Release receipt SHA-256: `sha256:bb5c5c236fd77b4715bb279f378e72881a05943527e1b88ad4845bb71f0f7c4d`
- Release manifest SHA-256: `sha256:e7501488be54221da3ab437a32d57f80a74cabf3347b6b6b874922b1019ff51f`
- Files excluding receipt: `146`

The local and Program Control RC3 directories remain immutable historical
evidence. No RC3 byte, receipt, hash, or validation report is modified by the
corrective release.

## Correction boundary

RC4 may add only the portable derivative relationship contract, structured
lock evidence, validators, generated types, compatibility declaration,
fixtures, migration declaration, tests, and directly required documentation.
Lifecycle, authority ownership, source-kind, interview provenance, Activative
lineage, acceptance, and acknowledgement behavior remain unchanged.
