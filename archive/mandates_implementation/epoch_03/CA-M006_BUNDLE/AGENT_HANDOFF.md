# CA-M006 Agent Handoff

## Mandate

**Mandate ID:** CA-M006  
**Mandate title:** Activative to Elicitation Linking  
**Requirement / Invariant:** FR-006 / FR-ELIC-001 linkage contract  
**Execution instruction:** Test suite was **not run**, per operator request.

## Summary

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/activative_elicitation_link.py` | Added an authoritative SQLite-backed many-to-many edge registry for immutable Activative trigger revisions and Elicitation Step revisions. Added parent canonical SHA-256 digests, deterministic edge trace hashing, foreign-key integrity, workspace isolation, duplicate-edge rejection, revision immutability, bidirectional resolution, and a structured interview-planning projection. Elicitation-branch resolution fails closed unless every step has an authorized, integrity-verified Activative origin. | Code-level contract proves the required positive relationship shapes and fail-closed boundaries. The branch resolver verifies workspace, authorization, parent identity/revision, parent digests, and edge trace hash before returning planning input. |
| `tests/cae/test_ca_m006_activative_elicitation_link.py` | Added acceptance/integration coverage for one-to-many, many-to-one, true many-to-many, deterministic trace hashing, revision/hash changes, missing parents, duplicate edges, immutable revision conflicts, invalid revisions, cross-workspace links, unauthorized origins, orphan branches, trace tampering, structured planning projection, and SQLite reload persistence. | Test suite contains explicit positive, negative, persistence, and tamper-detection evidence for FR-006. Tests were not executed in this run because execution of tests was explicitly prohibited. |

## Exact paste instructions

Replace/add these repository paths exactly:

1. Replace/add `packages/ca_runtime/src/ca_runtime/activative_elicitation_link.py` with the bundled file at the same path.
2. Replace/add `tests/cae/test_ca_m006_activative_elicitation_link.py` with the bundled file at the same path.
3. Copy `AGENT_HANDOFF.md` only as the handoff document; it is not a repository source change.

No other repository paths are part of this bundle.

## Manual post-apply commands

No database migration is required for this implementation because the CA-M006 registry creates only its own SQLite tables (`ca_m006_activative_triggers`, `ca_m006_elicitation_steps`, and `ca_m006_links`) when instantiated.

No commands were executed during this handoff beyond static source parsing. The CA-M006 test suite remains pending because the operator explicitly instructed: **DO NOT run TEST**.

Recommended verification after the bundle is applied, when testing is authorized:

```bash
pytest -q tests/cae/test_ca_m006_activative_elicitation_link.py
```

## New automated tests included

- `test_ca_m006_one_activative_to_many_steps`
- `test_ca_m006_many_activatives_to_one_step`
- `test_ca_m006_true_many_to_many_is_queryable_both_directions`
- `test_ca_m006_trace_hash_is_deterministic`
- `test_ca_m006_revision_change_changes_trace_hash`
- `test_ca_m006_missing_parent_is_rejected`
- `test_ca_m006_duplicate_edge_is_rejected`
- `test_ca_m006_revision_reuse_with_different_bytes_is_rejected`
- `test_ca_m006_invalid_revision_is_rejected`
- `test_ca_m006_cross_workspace_link_is_rejected`
- `test_ca_m006_unauthorized_activative_cannot_origin_link`
- `test_ca_m006_untraced_branch_fails_closed`
- `test_ca_m006_tampered_trace_hash_fails_closed`
- `test_ca_m006_branch_projection_is_structured_and_authoritative`
- `test_ca_m006_persists_and_reloads_edges_from_sqlite`

## Evidence locators

Implementation:
- `activative_elicitation_link.py:95` — `ActivativeTrigger`
- `activative_elicitation_link.py:157` — `ElicitationStep`
- `activative_elicitation_link.py:213` — `ActivativeElicitationLink` and deterministic trace construction
- `activative_elicitation_link.py:293` — authoritative registry and relational schema
- `activative_elicitation_link.py:523` — governed link insertion and parent validation
- `activative_elicitation_link.py:645` — fail-closed branch resolution
- `activative_elicitation_link.py:743` — reverse Activative-to-Elicitation resolution
- `activative_elicitation_link.py:811` — structured interview-planning input projection

Tests:
- `test_ca_m006_activative_elicitation_link.py:88` — one-to-many
- `test_ca_m006_activative_elicitation_link.py:109` — many-to-one
- `test_ca_m006_activative_elicitation_link.py:131` — true many-to-many/bidirectional
- `test_ca_m006_activative_elicitation_link.py:174` — deterministic trace hash
- `test_ca_m006_activative_elicitation_link.py:206` — duplicate edge rejection
- `test_ca_m006_activative_elicitation_link.py:246` — cross-workspace rejection
- `test_ca_m006_activative_elicitation_link.py:259` — unauthorized-origin rejection
- `test_ca_m006_activative_elicitation_link.py:271` — orphan-branch fail-closed behavior
- `test_ca_m006_activative_elicitation_link.py:286` — trace tamper detection
- `test_ca_m006_activative_elicitation_link.py:373` — SQLite persistence/reload

## Scope and residual limitations

Only the two authorized code/test paths were included in the implementation bundle.

The repository snapshot contains no `.git` metadata, so an exact source commit SHA cannot be truthfully captured from the supplied archive. **Commit SHA: unavailable in supplied snapshot.**

The bundle implements the CA-M006 relationship boundary and its structured planning projection, but the existing `InterviewSemanticProgramCoordinator` was not edited because that file is outside the exact file boundary requested by the operator. Integration into that coordinator therefore requires an explicitly authorized follow-on change or an import/use by the existing planning caller.

## Operator decision

**Decision requested:** approve or reject CA-M006 as implemented in this bounded bundle, after authorized test execution confirms the included acceptance suite.
