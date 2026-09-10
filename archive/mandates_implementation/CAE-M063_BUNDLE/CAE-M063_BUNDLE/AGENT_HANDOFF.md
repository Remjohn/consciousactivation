# CAE-M063 — Natural-Language Semantic Cinematic Retrieval

## Mandate ID & Title

**CAE-M063 — Natural-Language Semantic Cinematic Retrieval**

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/asset-intelligence/src/cae_asset_intelligence/retrieval.py` | Added governed natural-language retrieval, explicit embedding-model binding, deterministic semantic encoder, lexical+semantic hybrid ranking, hard workspace/candidate/role/rights constraints, confidence abstention, blocked stale-index path, ranked candidate provenance, and immutable-content retrieval receipts. | `INV-RETRIEVAL-001`: governed scenes are ranked only after hard policy filtering; exact timestamps/source/version/hash, explanation, semantic role, insert role, rights and provenance are returned; low confidence fails closed. |
| `services/asset-intelligence/src/cae_asset_intelligence/__init__.py` | Exported the M063 retrieval contracts and engine. | Retrieval boundary is directly importable without changing `AssetAnnotation` semantics. |
| `tests/asset_intelligence/test_cinematic_retrieval_m063.py` | Added self-contained unit/integration coverage for paraphrase retrieval, exact terminology, role filtering, rights filtering, abstention, workspace isolation, stale-index blocking, deterministic model binding, false-proof rejection, and stable receipt identity. | Executable proof of `INV-RETRIEVAL-001` and the M0063 false-proof countercase. |
| `services/asset-intelligence/M063_RETRIEVAL_EVALUATION.md` | Added evaluation evidence describing measured behavior, false-proof countercase, evidence classes, environment fidelity, limitations, and operator validation boundary. | Separates executable evidence from unsupported production/model claims. |

## Files Added and Files Modified

### Files Added

- `services/asset-intelligence/src/cae_asset_intelligence/retrieval.py` — new M063 retrieval runtime boundary.
- `tests/asset_intelligence/test_cinematic_retrieval_m063.py` — new M063 test suite and hard-negative fixtures.
- `services/asset-intelligence/M063_RETRIEVAL_EVALUATION.md` — evaluation and evidence artifact.

### Files Modified

- `services/asset-intelligence/src/cae_asset_intelligence/__init__.py` — exports the new retrieval API. No canonical domain semantics were changed.

## Exact paste instructions and post-apply commands

From the repository root, copy the bundle paths verbatim so they land at the relative destinations shown above. No database migration is required: M063 is a derived in-memory retrieval boundary over the existing governed scene corpus and does not introduce a persistent schema.

Post-apply validation:

```bash
PYTHONPATH=services/asset-intelligence/src pytest -q -p no:asyncio tests/asset_intelligence
```

Optional focused command:

```bash
PYTHONPATH=services/asset-intelligence/src pytest -q -p no:asyncio tests/asset_intelligence/test_cinematic_retrieval_m063.py
```

## Test Command

```bash
PYTHONPATH=services/asset-intelligence/src pytest -q -p no:asyncio tests/asset_intelligence
```

## Expected Test Results

**34 automated tests, all passing.**

Observed sandbox result:

```text
34 passed in 0.11s
```

The suite uses the repository's real `tests/api/fixtures/synthetic_interview.mp4` bytes for corpus construction and exercises the M062 governed scene contracts rather than fabricated source-byte placeholders.

The implementation does **not** automatically clear rights, generate scenes, mutate `AssetAnnotation`, or self-authorize promotion of an external embedding model. The default deterministic encoder is an explicit local fallback with its model identity recorded in every retrieval receipt; production promotion of an approved external model remains an operator-controlled boundary.

The false-proof countercase is explicitly tested: a semantically close scene cannot bypass a governed insert-role filter, and a low-confidence semantic match abstains without returning candidates.

Per the M0063 mandate, execution stops at this boundary; M0064 is not started or implemented.
