# CA-M010 Agent Handoff

## Mandate

- Mandate: `CA-M010`
- Question: `Q10`
- Objective: Digest-pinned, structured Research Brief as a governed causal input.
- Operator gate: **REQUIRED / NOT RECORDED BY THIS BUNDLE**.
- Git commit SHA: **UNAVAILABLE**. The supplied `codebase_clean.zip` contains no `.git` metadata, so an exact commit SHA cannot be truthfully captured.

## Summary table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/pipeline/src/cmf_pipeline/briefs/__init__.py` | Exports the CA-M010 typed models and canonical service boundary. | Downstream callers have one explicit import surface for the governed brief contract. |
| `services/pipeline/src/cmf_pipeline/briefs/models.py` | Adds frozen Pydantic models for brief drafts, revision-bound claims, citations, source anchors, authority tiers, falsification conditions, operator inspection, and admission receipts. | Each admitted claim is structurally bound to a brief revision and requires citation identity plus a verifiable source anchor and falsification condition; authority tier is constrained to 1–4. |
| `services/pipeline/src/cmf_pipeline/briefs/service.py` | Adds canonical admission, source-pinning validation, immutable revisioning through `PipelineRepository.store_object`, deterministic receipt persistence, fail-closed consumption, and operator inspection. | Runtime consumers read the sealed structured object, current revision only, with canonical digest verification and exact source identity/revision/digest or immutable-locator checks. |
| `tests/pipeline/test_research_briefs.py` | Adds positive, negative, persistence, revision, provenance, authority, stale, source-substitution, false-proof, and operator-inspection tests. | The mandated fail-closed boundary is executable and tested rather than schema-only. |

## Exact paste instructions

This bundle contains **new files only**. No existing repository file is replaced.

Create/copy these exact paths relative to the repository root:

```text
CA-M010_BUNDLE/services/pipeline/src/cmf_pipeline/briefs/__init__.py
→ services/pipeline/src/cmf_pipeline/briefs/__init__.py

CA-M010_BUNDLE/services/pipeline/src/cmf_pipeline/briefs/models.py
→ services/pipeline/src/cmf_pipeline/briefs/models.py

CA-M010_BUNDLE/services/pipeline/src/cmf_pipeline/briefs/service.py
→ services/pipeline/src/cmf_pipeline/briefs/service.py

CA-M010_BUNDLE/tests/pipeline/test_research_briefs.py
→ tests/pipeline/test_research_briefs.py
```

The implementation intentionally reuses the existing `PipelineRepository.pipeline_objects` revision/digest/idempotency primitive. No new migration is required.

The source resolver is intentionally duck-typed to the existing research-source boundary. `ca_runtime.research_source_program.ResearchSourceProgramCoordinator.get_source_record(...)` is compatible with the required resolver shape and can be supplied when wiring the service into a live caller.

## Manual post-apply commands

Install the repository's normal development dependencies before running the suite. Then run:

```bash
pytest -q tests/pipeline/test_research_briefs.py
pytest -q tests/pipeline
pytest -q tests/phase3/test_research_source_program.py
```

No database migration command is required for CA-M010 because existing `pipeline_objects`, `pipeline_command_results`, and `pipeline_edges` storage already provide the required persistence/revision primitives.

## Automated tests included

- `test_multi_claim_admission_persists_structured_brief_and_receipt`
- `test_revision_preserves_prior_immutable_revision_and_rejects_stale_consumer`
- `test_missing_citation_is_blocked_before_persistence`
- `test_false_proof_clickable_citation_without_digest_or_immutable_locator_fails_closed`
- `test_bad_source_digest_is_rejected_and_operator_inspection_exposes_block_reason`
- `test_source_substitution_is_fail_closed_at_consumption_boundary`
- `test_invalid_authority_lane_is_rejected_without_state_change`
- `test_stale_expected_revision_is_rejected_before_new_revision_is_created`
- `test_malformed_claim_and_invalid_authority_tier_fail_at_schema_boundary`
- `test_inspection_of_current_revision_is_ready_and_contains_source_lineage`
- `test_locator_only_citation_is_admissible_when_source_identity_and_revision_are_resolved`
- `test_missing_falsification_condition_is_blocked_fail_closed`

## Verification evidence

Environment used for the focused execution:

- Python: `3.13.5`
- pytest: `9.0.2`
- Pydantic: `2.13.4`

Observed results:

```text
pytest -q tests/pipeline/test_research_briefs.py tests/pipeline
29 passed

pytest -q tests/phase3/test_research_source_program.py
9 passed
```

`python -m compileall -q services/pipeline/src/cmf_pipeline/briefs tests/pipeline/test_research_briefs.py` also passed.

The execution container did not include the repository's `psycopg` dependency or the full installed-package environment. The test run therefore used a temporary, non-bundled `psycopg` stub only to allow import of the existing runtime in the isolated container. This does not alter product code or the submitted bundle. The real repository environment must rerun the commands above with its normal dependencies.

File SHA-256 values for the bundled code:

```text
af5b3e8aa218137fdbffc900983910a5e1a13fcf9f140ad984cd06ad5a9a1ca9  services/pipeline/src/cmf_pipeline/briefs/__init__.py
0bd41e95c9049096b867912c8c8295d978297af47ed50dc6ca2f36885f174369  services/pipeline/src/cmf_pipeline/briefs/models.py
c7b66cc6a7e197c3eeb4ae6ea07feba71c5d9a6c8b080bfb84f233741fa506ac  services/pipeline/src/cmf_pipeline/briefs/service.py
37568a05c3dc1e7a5759bf2af0387ca1a7f800099a87f4dcd0764c81a7810a3a  tests/pipeline/test_research_briefs.py
```

## Mechanical checks vs operator judgments

Mechanical checks implemented here:

- typed schema and forbidden extra fields;
- authority tier bounds;
- citation identity and source revision presence;
- source digest format and exact digest matching when pinned;
- immutable locator matching when used;
- source workspace matching;
- source quarantine/rejection/deletion blocking;
- claim-to-brief revision binding;
- current-revision / stale-revision blocking;
- canonical payload digest verification;
- deterministic receipt hashing and receipt persistence;
- idempotent repository command path;
- operator inspection of provenance and blocked reason codes.

Not established mechanically by this mandate:

- whether an external source is substantively true in the world;
- whether a claim is philosophically or editorially insightful;
- whether an authority tier is substantively appropriate beyond the declared ordinal field;
- downstream collision quality, narrative quality, or audience convergence.

## Control-state / completion limitation

The supplied archive does not contain `.git` metadata, so the exact commit SHA cannot be captured. The mandate also requires CAE control-state update and an explicit operator decision. Those are **not claimed complete** in this bundle because the authorized CA-M010 file surface does not include a global control-state mutation surface and no commit identity is available from the archive.

The required operator action remains: **approve CA-M010 and authorize its use as an input to CA-M011; separately record the operator decision required for any legacy research artifacts.**

Stop after that gate; do not implement CA-M011, collision discovery, narrative generation, or audience-layer convergence as part of CA-M010.
