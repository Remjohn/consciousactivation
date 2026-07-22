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


## Product-adoption exclusion

Do not create a Development Capsule for a specification or proposal in `PRODUCT_ADOPTION_REQUIRED` or `ACCEPTED_FOR_PRODUCT_ADOPTION` state.

Create or update `PRODUCT_ADOPTION_QUEUE.yaml` instead. A product-local capsule becomes eligible only after:

1. target-product write/adoption authority is granted;
2. proposal bytes are adopted into an allowed product-local path;
3. adopted bytes are independently audited or re-audited;
4. the adopted product-local spec receives `ACCEPTED_FOR_BUILD` and a new hash lock.


## Ratification exclusion

Do not issue a Development Capsule for a spec in:

* `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`
* `PRODUCT_ADOPTION_REQUIRED`
* `ACCEPTED_FOR_PRODUCT_ADOPTION`

Such specs remain in the authority/adoption queue until the required attributable decision exists and product-local accepted bytes are hash-locked.
