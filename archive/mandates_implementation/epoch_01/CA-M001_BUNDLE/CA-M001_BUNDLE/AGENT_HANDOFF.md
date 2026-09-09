# CA-M001 Bundle Handoff

## Mandate

`CA-M001` / `Q01` — Immutable Three-Layer Audience Context.

The supplied archive did not contain `.git` metadata, so an exact repository commit SHA could not be captured here. Per the mandate, the applying Operator must record the exact post-apply commit SHA.

## Summary

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/pipeline/src/cmf_pipeline/adapters/audience_context.py` | Added the canonical Stage 01 three-layer Audience Context boundary: explicit Market Macro Signals, Segment Cultural Archetypes, and Live Audience Tensions; frozen in-memory revisions; independent stable identities; per-revision SHA-256 digests; reference-only parent context; repository persistence through the existing revisioned object store; canonical read/reload path; and operator-readable projection. | The runtime representation cannot be a single blended audience blob; each layer has an independent identity, version/revision, payload digest, layer digest, and provenance; sealed revisions are not mutable in place. |
| `services/pipeline/src/cmf_pipeline/adapters/__init__.py` | Exported the new CA-M001 audience-context boundary types and adapter without changing existing synthetic adapter behavior. | The canonical adapter is directly available from the existing `cmf_pipeline.adapters` boundary while preserving the existing synthetic surface. |
| `tests/pipeline/test_audience_context_adapter.py` | Added positive, negative, persistence/reload, tamper, immutability, revision, and adjacent-regression coverage for CA-M001. | Executable tests cover three-layer isolation, digest/version identity, in-place mutation rejection, blended/missing-layer rejection, persistence across reload, historical revision preservation, same-revision tamper rejection, and synthetic adapter compatibility. |

## Exact paste instructions

Replace the following repository paths with the corresponding files in this bundle:

- `CA-M001_BUNDLE/services/pipeline/src/cmf_pipeline/adapters/audience_context.py` → `services/pipeline/src/cmf_pipeline/adapters/audience_context.py`
- `CA-M001_BUNDLE/services/pipeline/src/cmf_pipeline/adapters/__init__.py` → `services/pipeline/src/cmf_pipeline/adapters/__init__.py`
- `CA-M001_BUNDLE/tests/pipeline/test_audience_context_adapter.py` → `tests/pipeline/test_audience_context_adapter.py`

No other repository paths are authorized by this bundle.

## Manual post-apply commands

The requested execution constraint was **DO NOT RUN TEST HERE**, so no tests were executed while producing this bundle.

Run the focused mandate tests after applying the files:

```bash
pytest -q tests/pipeline/test_audience_context_adapter.py
```

Then run the relevant pipeline suite:

```bash
pytest -q tests/pipeline
```

Capture the exact post-apply Git commit SHA:

```bash
git rev-parse HEAD
```

No database migration is required. The implementation uses the repository's existing `pipeline_objects` revisioning mechanism; layers and the parent context are written as separate object types with explicit expected revisions.

## New automated tests included

- `test_positive_path_creates_three_independent_digest_pinned_layers`
- `test_operator_projection_exposes_layers_separately_with_provenance`
- `test_immutable_revision_rejects_in_place_mutation_and_returns_fresh_payload_views`
- `test_conflicting_layer_identity_is_rejected`
- `test_blended_or_missing_layer_representation_fails_closed`
- `test_tampered_layer_digest_is_rejected`
- `test_persistence_and_reload_preserve_exact_layer_revisions_and_digests`
- `test_persist_rejects_changed_payload_reusing_an_existing_revision`
- `test_adjacent_synthetic_adapter_behavior_remains_compatible`

## Evidence / residual limitation

Static Python compilation of the three bundled Python files succeeded during assembly; this is **not** test execution.

Runtime acceptance remains unproven until the Operator runs the focused and relevant pipeline tests. Because the supplied archive has no `.git` directory, the mandate's required exact commit SHA is also necessarily pending the apply/commit step.

## Operator decision

**Approve or reject `CA-M001` after applying the bundle and reviewing the runtime test evidence.**

The executor did not begin Q02 or modify unrelated runtime, UI, release, policy, or later-question surfaces.
