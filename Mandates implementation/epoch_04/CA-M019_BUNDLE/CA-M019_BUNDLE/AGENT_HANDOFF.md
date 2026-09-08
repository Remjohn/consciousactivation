# CA-M019 Agent Handoff

## Mandate

- **Mandate ID:** `CA-M019`
- **Title:** Expression Moments Semantic Bridge
- **Requirement / invariant:** `FR-SEM-001`
- **Implementation status:** Files prepared for application; tests intentionally **not executed** per operator instruction.
- **Baseline:** supplied repository archive (`codebase_clean.zip`). The archive contains no `.git` directory, so no commit SHA exists for this execution.

## Summary table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/interview/src/conscious_activations_interview_expression/semantic_bridge.py` | Added a fail-closed, deterministic semantic bridge from a raw spoken utterance directly to a supplied conceptual activation vector. The bridge requires an actual admitted-evidence receipt, valid hierarchical context-lineage result, exact source-utterance identity, direct evidence anchors, and exact preservation of core emotional polarity and subject stance. It produces a hash-addressable `ExpressionMoment` with no intermediary semantic-frame channel and exposes a strict composition-input guard that accepts only a genuine `ExpressionMoment` instance. | `FR-SEM-001`: semantic composition is represented as a direct utterance→activation-vector bridge; missing admission/lineage, mismatched source identity, polarity drift, stance drift, and intermediary frames fail closed. |
| `tests/phase4/test_ca_m019_semantic_bridge.py` | Added schema, positive-path, negative/fail-closed, composition-boundary, false-proof, determinism, provenance, and regression coverage for the bridge. | Tests demonstrate that only an actual bridged `ExpressionMoment` crosses the composition guard and that semantic transformations changing polarity or stance are rejected. **Not executed per instruction.** |

## Exact paste instructions

From the repository root, replace/add **exactly** these files and no others:

1. Replace/add `services/interview/src/conscious_activations_interview_expression/semantic_bridge.py` with the bundled file at that exact path.
2. Replace/add `tests/phase4/test_ca_m019_semantic_bridge.py` with the bundled file at that exact path.
3. `AGENT_HANDOFF.md` is an execution handoff artifact and should not be pasted into the repository unless the operator explicitly wants to retain it outside the mandate boundary.

No package initializer, migration, persistence schema, UI surface, composition implementation, authorization module, Reaction Receipt contract, Anchor Hit contract, yield gate, or release module was changed.

## Manual post-apply commands

Run the mandate-specific acceptance suite **after application** (not run during this execution):

```bash
pytest -q tests/phase4/test_ca_m019_semantic_bridge.py
```

No migration or package-install step is required by the two bundled files.

## New automated tests included

- `test_expression_moment_contains_direct_semantic_bridge_fields`
- `test_receipt_is_hash_addressable_and_stamped`
- `test_bridge_accepts_admitted_contextual_utterance_and_vector`
- `test_mapping_inputs_are_supported_without_inferred_intermediaries`
- `test_receipt_is_deterministic_for_identical_inputs`
- `test_missing_admission_receipt_is_rejected`
- `test_quarantined_evidence_cannot_cross_semantic_bridge`
- `test_downstream_blocked_evidence_cannot_cross_semantic_bridge`
- `test_missing_context_lineage_is_rejected`
- `test_invalid_context_lineage_is_rejected`
- `test_vector_for_different_utterance_is_rejected`
- `test_emotional_polarity_change_is_rejected`
- `test_subject_stance_change_is_rejected`
- `test_empty_vector_evidence_refs_are_rejected`
- `test_intermediary_frames_are_rejected_as_hallucinated_semantics`
- `test_invalid_vector_dimension_is_rejected`
- `test_composition_accepts_only_real_expression_moment`
- `test_raw_text_is_rejected_at_composition_boundary`
- `test_fake_expression_moment_mapping_is_rejected_at_composition_boundary`
- `test_matching_object_name_does_not_prove_semantic_bridge`
- `test_highly_detailed_vector_still_fails_when_polarity_changes`
- `test_source_text_and_lineage_are_preserved_verbatim`
- `test_source_anchor_and_vector_evidence_are_retained`

## Evidence locators

- **Bridge boundary:** `services/interview/src/conscious_activations_interview_expression/semantic_bridge.py` — `SemanticBridge.bridge`.
- **Admission gate:** `services/interview/src/conscious_activations_interview_expression/semantic_bridge.py` — `SemanticBridge._require_admitted`.
- **Context gate:** `services/interview/src/conscious_activations_interview_expression/semantic_bridge.py` — `SemanticBridge._require_context_lineage`.
- **Semantic invariants:** `services/interview/src/conscious_activations_interview_expression/semantic_bridge.py` — `SemanticBridge._validate_direct_mapping`.
- **No-intermediary contract:** `ExpressionMoment.__post_init__` rejects non-empty `intermediary_frames`.
- **Composition gate:** `SemanticBridge.require_composition_input` accepts only `ExpressionMoment` instances bearing CA-M019 / FR-SEM-001 authority.
- **Positive executable proof:** `tests/phase4/test_ca_m019_semantic_bridge.py::test_bridge_accepts_admitted_contextual_utterance_and_vector`.
- **Admission fail-closed proof:** `tests/phase4/test_ca_m019_semantic_bridge.py::test_quarantined_evidence_cannot_cross_semantic_bridge`.
- **Polarity preservation proof:** `tests/phase4/test_ca_m019_semantic_bridge.py::test_emotional_polarity_change_is_rejected`.
- **Stance preservation proof:** `tests/phase4/test_ca_m019_semantic_bridge.py::test_subject_stance_change_is_rejected`.
- **Hallucination/intermediary proof:** `tests/phase4/test_ca_m019_semantic_bridge.py::test_intermediary_frames_are_rejected_as_hallucinated_semantics`.
- **Composition boundary negative proof:** `tests/phase4/test_ca_m019_semantic_bridge.py::test_fake_expression_moment_mapping_is_rejected_at_composition_boundary`.
- **False-proof countercase:** `tests/phase4/test_ca_m019_semantic_bridge.py::test_matching_object_name_does_not_prove_semantic_bridge`.

## Verification state and limitations

- Python syntax validation was performed with `python -m py_compile` on both bundled Python files.
- **Tests were not run**, exactly as instructed.
- The supplied archive has no `.git` metadata; therefore this execution cannot truthfully provide a post-change commit SHA and did not create a commit.
- The supplied snapshot does not contain the CA-M017 `evidence_admission.py` or CA-M018 `context_lineage.py` target modules. CA-M019 therefore does not re-implement those mandates; instead it consumes their expected result protocol (`admitted` / `downstream_generation_allowed` and `valid` / lineage references) when those objects are supplied by the applied repository state.
- The bridge deliberately does not infer an activation vector from natural-language utterance text. The vector is an explicit upstream input and remains directly anchored to the exact utterance ID and evidence references; this is the mechanism used here to avoid hallucinated intermediary meaning.
- The mandate request targets `services/interview/.../semantic_bridge.py` and `tests/phase4/test_ca_m019_semantic_bridge.py`; the canonical M019 mandate prose also discusses a broader composer surface, but no composer file was modified because doing so would cross the explicit execution boundary provided for this bundle.

## Operator decision

**Approve or reject CA-M019 based on the post-apply test result and review of the exact boundary above.** Approval should require the mandate-specific suite to pass and should confirm that the applied M017/M018 dependencies expose the expected admitted-evidence and context-lineage result signals.
