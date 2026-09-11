# CAE-M0063 Retrieval Evaluation Evidence

**Mandate:** CAE-M0063 — Natural-Language Semantic Cinematic Retrieval
**Invariant:** INV-RETRIEVAL-001
**Verification command:** `PYTHONPATH=services/asset-intelligence/src pytest -q -p no:asyncio tests/asset_intelligence`
**Fixture identity:** `tests/api/fixtures/synthetic_interview.mp4` plus governed M063 scene annotations in `tests/asset_intelligence/test_cinematic_retrieval_m063.py`

## What is measured

The verifier measures deterministic hybrid retrieval over already-governed `SceneRecord` objects using lexical overlap plus a bound embedding model, while hard-filtering workspace, candidate, insert-role, semantic-role, and rights constraints. It verifies exact source hash/version and source timestamps are returned from the scene record, emits contextual explanations and semantic/insert roles, and produces immutable-content retrieval receipt identities. Confidence below the request threshold abstains without returning candidates; invalid index state or a mismatched expected index hash blocks retrieval.

## False-proof countercase

A scene can be semantically similar to a query because it shares words/concepts such as `choice` or `operational`, while still being the wrong editorial role. The hard-negative test `test_semantically_close_but_narratively_wrong_candidate_is_rejected_by_role_filter` proves that role eligibility is applied before ranked output, so vector/semantic proximity cannot bypass a governed role constraint.

## Evidence classes

| Evidence | Result | Fidelity |
|---|---|---|
| Executable unit/integration tests | PASS | Real repository Python execution against real MP4 fixture bytes and governed scene models |
| Schema | PASS | Pydantic runtime validation for query, candidate, and receipt contracts |
| Model binding | PASS | Explicit provider-neutral `EmbeddingModel`; deterministic local encoder identity is recorded in every receipt |
| Hybrid ranking | PASS | Lexical overlap + cosine similarity with deterministic tie-breaking |
| Hard filters | PASS | Workspace, candidate, role, semantic-role, and rights policy filters are enforced before scoring output |
| Abstention | PASS | Low-confidence query returns no candidates and `ABSTAIN` receipt |
| Block path | PASS | Wrong index hash returns no candidates and `BLOCKED` receipt |
| Provenance | PASS | Candidate includes scene/media/source/version/hash/candidate identifiers and exact timestamps |

## Results

**34/34 tests passing** in the scoped Asset Intelligence suite after adding the final hard-negative case.

## What this does not measure

It does not establish that the deterministic local encoder has the semantic quality of a production transformer embedding model, nor does it prove legal clearance beyond the rights metadata already attached to the governed scene. Production promotion of an external model requires an explicit approved model binding outside this implementation; retrieval does not grant model or rights authority.

## Environment-fidelity requirement

Run the stated pytest command from repository root with the Asset Intelligence source path available. Full-monorepo execution may require dependencies not installed in a minimal sandbox; that is an environment limitation, not evidence of a retrieval defect.

## Operator validation

Operator validation remains required before treating a specific promoted embedding model or corpus/index snapshot as production authority. This implementation supplies the bounded runtime contract and fail-closed behavior; it does not self-authorize promotion.
