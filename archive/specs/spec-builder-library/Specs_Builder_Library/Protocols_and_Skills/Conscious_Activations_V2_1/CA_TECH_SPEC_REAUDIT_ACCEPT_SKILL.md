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
- upstream specifications required as `ACCEPTANCE_PREREQUISITE`;
- affected downstream specifications;
- dependency-edge classification ledger;
- repository write-authority classification;
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
- `ACCEPTED_FOR_PRODUCT_ADOPTION`
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


## Dependency acceptance rule

Final `ACCEPTED_FOR_BUILD` requires every dependency classified as `ACCEPTANCE_PREREQUISITE` to be accepted and hash-pinned. Draft-only upstream dependencies are insufficient for final build acceptance.

A `BUILD_PREREQUISITE` need not be implemented for spec acceptance, but it must be recorded in the Build DAG.

## Cross-product proposal acceptance rule

When the audited document is a `PROGRAM_CONTROL_CROSS_PRODUCT_PROPOSAL` and the target repository currently disallows the proposed adoption path:

- the highest permitted outcome is `ACCEPTED_FOR_PRODUCT_ADOPTION`;
- record `PRODUCT_ADOPTION_REQUIRED`;
- hash-lock the proposal bytes separately from future product-local adopted bytes;
- do not create a product-local Development Capsule;
- after product adoption, audit the adopted product-local file before granting `ACCEPTED_FOR_BUILD`.


## Pending-ratification disposition

When the specification is technically valid but its controlling authority remains `CANDIDATE_NOT_CURRENT`, issue:

`TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`

Do not issue `ACCEPTED_FOR_BUILD`.

Record the exact ratification receipt required to unlock build acceptance. After ratification, perform a bounded authority-transition verification and hash check; re-audit only affected sections unless the ratification changed substance.
