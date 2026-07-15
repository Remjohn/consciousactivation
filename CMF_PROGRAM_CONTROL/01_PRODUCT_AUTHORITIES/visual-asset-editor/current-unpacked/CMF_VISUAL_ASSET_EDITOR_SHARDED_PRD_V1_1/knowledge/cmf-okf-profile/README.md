# CMF-OKF Visual Memory Profile

This directory demonstrates how the Visual Asset Editor projects durable knowledge into Open Knowledge Format-compatible Markdown with CMF extensions.

## Role

CMF-OKF is used for:

- Visual Steering Recipes;
- production and failure patterns;
- workflow/model/LoRA knowledge;
- Visual Syntax usage context;
- benchmark findings;
- operator and course knowledge.

It is **not** used as canonical state for live workflow runs, asset lifecycle, contracts, queues, locks, budgets, secrets, or registries.

## Consumption order

1. Read [`index.md`](index.md).
2. Apply typed authority and compatibility filters from operational state.
3. Traverse relevant typed edges.
4. Run hybrid lexical/semantic/visual/syntax retrieval.
5. VLM-rerank against current demand, composition, failure, and preservation constraints.
6. Load only Minimum Complete Context into the current JIT Execution Capsule.

## CMF extensions

Concept frontmatter adds:

- `cmf_profile`;
- stable `id` and `version`;
- `lifecycle_status`;
- `authority_class`;
- retrieval facets;
- typed edges;
- source-record references;
- content hash placeholder.

Architecture will define how hashes and indexes are generated automatically.
