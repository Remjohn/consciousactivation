# Human Resolution → Programming Material Architecture

## Core law

Every human-resolved decision becomes programming material automatically.

This is automatic **capture and attribution**, not an automatic unreviewed mutation of
live weights or universal doctrine.

## Canonical record

```yaml
human_resolution_episode:
  episode_id: immutable
  workspace_id: required
  project_id: required
  campaign_id: required
  run_id: required
  harness_id: required
  harness_version: required
  category_id: required
  format_profile_id: optional

  resolution_kind:
    - initial_seed
    - taste_direction
    - approval
    - rejection
    - candidate_selection
    - revision_request
    - manual_parameter_change
    - manual_timeline_change
    - tool_override
    - escalation_resolution
    - publication_decision

  state_before_ref: required
  artifact_before_refs: []
  request_text: optional
  request_structured_ref: optional

  selected_or_rejected_candidates: []
  exact_changes:
    - target_object
      operation
      before
      after

  tool_program_ref: optional
  exact_tool_calls: []
  runtime_and_model_identities: []
  retrieved_context_ref: optional
  declared_invariants: []
  required_transformations: []
  creative_degrees_of_freedom: []
  wrong_reading_locks: []

  result_refs: []
  evaluation_refs: []
  accepted: boolean
  human_authority_identity: required
  scope:
    - run_local
    - harness_profile
    - category
    - workspace
    - avatar_or_identity
    - candidate_doctrine

  programming_material_dispositions:
    retrieval_memory: automatic
    hard_negative: derived
    supervised_example: candidate
    preference_pair: candidate
    repair_trajectory: candidate
    programmed_model_training: candidate
    steering_recipe_evidence: candidate
```

## Automatic pipeline

```text
human action in Studio
→ immutable HumanResolutionEpisode
→ typed attribution to responsible layer
→ immediate retrieval indexing
→ training-material queue
→ offline dataset construction
→ shadow replay against future models
→ claim-specific evaluation
→ human-authorized promotion
```

## Important distinction

A human decision must never disappear as a generic UI click.

Dragging a clip, changing a crop, choosing candidate B, requesting “make the coach feel
more present,” rejecting a background, or changing the order of Carousel slides must all
produce the same evidence quality as a text correction.

## New required specs

- `TS-CAS-PM-001` — Human Resolution Episode and Programming Material Ledger
- `TS-CAS-PM-002` — Programming Material Attribution and Dataset Builder
- `TS-CAS-PM-003` — Preference, Hard-Negative, Repair, and Demonstration Extraction
- `TS-CAS-PM-004` — Shadow Replay, Evaluation, and Programmed Model Promotion
