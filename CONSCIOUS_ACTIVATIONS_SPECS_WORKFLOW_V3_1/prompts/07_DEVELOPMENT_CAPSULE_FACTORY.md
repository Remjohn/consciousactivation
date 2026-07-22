# PROMPT 07 — Development Capsule and Build-Readiness Factory

**Model:** GPT-5.6 Sol Extra High  
**Parallel:** Capsule drafting may run in parallel per accepted spec on disjoint paths; final dependency/path authorization is sequential.

Create one Development Capsule per accepted implementation responsibility.

Do not implement code. Do not combine unrelated specs. Do not create a capsule for a spec without an accepted hash lock.

## Required gate

Prompt 06 passes; accepted registry/hash lock exists.

## Per-spec capsule

Each capsule contains exactly one target Tech Spec and:

- accepted spec ID/path/SHA-256;
- controlling FRs and Story;
- acceptance receipt and audit lineage;
- exact authority sources;
- exact allowed file scope and forbidden paths;
- upstream dependency receipt;
- implementation scope and non-goals;
- acceptance criteria;
- test plan;
- observability plan;
- failure/rollback plan;
- completion receipt template;
- claim ceiling.

## Controller work

- create build dependency DAG;
- create parallel path-ownership registry;
- ensure shared contracts build before consumers;
- initialize/update Build Ledger;
- assign `READY_TO_BUILD` only where accepted specs, upstream prerequisites, capsule validation, and file ownership all pass;
- publish capsule index, build wave plan, readiness report, and completion receipt.

Stop before implementation. Prompt 08 builds shared contracts first.
