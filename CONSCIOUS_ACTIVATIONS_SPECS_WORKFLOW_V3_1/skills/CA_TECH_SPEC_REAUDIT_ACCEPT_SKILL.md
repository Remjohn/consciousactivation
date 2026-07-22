# SKILL — Conscious Activations Independent Re-Audit and Acceptance

## Role

Independently re-audit exactly one revised Tech Spec, verify the complete document rather than only changed sections, and issue final specification acceptance only when all blocking defects are resolved.

## Independence requirements

The re-auditor must not be the original writer or reviser.

## Required inputs

- revised spec;
- original audit report;
- revision receipt;
- finding-resolution matrix;
- architecture-decision receipts;
- controlling authority, FRs, Stories, and PRD;
- accepted upstream specs;
- affected downstream specs;
- files-read evidence.

## Re-audit process

1. Re-run every audit lens on the full spec.
2. Verify each original finding against actual revised text.
3. Detect new defects introduced by revision.
4. Verify source paths, object ownership, schemas, state transitions, acceptance criteria, tests, and claim ceiling.
5. Verify the spec can be implemented without architectural invention.
6. Verify cross-product consumers can use outputs exactly as defined.

## Acceptance law

A spec may become `ACCEPTED_FOR_BUILD` only when:

- no blocking audit finding remains;
- no unresolved architecture decision remains;
- controlling FRs and Stories are completely covered;
- object and field ownership are unique;
- all upstream spec identities are pinned;
- acceptance criteria are executable;
- source paths and migration dispositions are exact;
- drift-blacklist conditions are excluded;
- the accepted file is hash-locked.

## Outcomes

- `ACCEPTED_FOR_BUILD`
- `REVISION_REQUIRED`
- `ARCHITECT_DECISION_REQUIRED`
- `REAUDIT_BLOCKED`

## Required artifacts

For accepted specs:

- `REAUDIT_REPORT.yaml`
- `REAUDIT_REPORT.md`
- `ACCEPTANCE_RECEIPT.yaml`
- accepted SHA-256 entry in `ACCEPTED_SPEC_HASH_LOCK.yaml`
- accepted entry in `ACCEPTED_SPEC_REGISTRY.yaml`

Acceptance is specification readiness only. It is not implementation, evidence closure, production readiness, or certification.

## Source acceptance rule

Final acceptance requires all required sources to be readable and hash-identified. Optional/deferred sources may remain unavailable only when the accepted spec makes no unsupported claim from them and the source-gap notice is recorded.
