# PROMPT 05 — Per-Spec Revision Factory

**Controller/arbitrator:** GPT-5.6 Sol Extra High  
**Revisers:** GPT-5.6 Sol High  
**Parallel:** Yes for independent specs. Shared-schema or ownership conflicts wait for one Extra High decision.

Execute the V2.1 Tech Spec Revision Factory.

Do not audit. Do not implement code. Do not issue Development Capsules.

## Required gate

Prompt 04 passes; each target has an immutable audit report and state `REVISION_REQUIRED`, or a resolved architecture decision.

## Per-spec revision

Each child:

- revises exactly one spec;
- uses `CA_TECH_SPEC_REVISE_SKILL.md`;
- reads audit findings and accepted decisions;
- fixes only findings and necessary consistency consequences;
- preserves unrelated scope;
- does not decide unresolved architecture;
- produces revised spec, context confirmation, plan, finding-resolution matrix, and revision receipt;
- ends `REVISED_PENDING_REAUDIT` or `REVISION_BLOCKED`.

## Controller work

- resolve cross-product/shared-schema decisions first;
- ensure non-overlapping file ownership;
- verify every finding has a disposition;
- update quality registry and architecture-decision ledger;
- create revision status matrix and completion receipt.

Stop after revisions. Every revised spec returns to Prompt 06.
