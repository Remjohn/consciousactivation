# Implementation Scope

## Exact permitted outcome

Implement one deterministic Builder run-governance vertical slice that can:

1. create a run only when exactly one governed compilation target and one authorized Format 02 profile are supplied;
2. assign stable opaque run and event identities and bind compiler version, operator identity, command identity, timestamps, stream version, category and profile;
3. expose target-specific required work for the selected Format 02 lifecycle profile;
4. accept legal lifecycle commands only from an authorized actor with the expected stream version and a unique idempotency key;
5. append immutable typed events for accepted authoritative commands;
6. reject illegal, unauthorized, ambiguous, stale or payload-mismatched commands without authoritative mutation;
7. create deterministic checkpoints and resume the same run from the newest valid checkpoint/event stream without replaying a human decision; and
8. produce deterministic Story test, observability, file-manifest, rollback and completion-receipt evidence.

## Implementation method

- Python 3.12-compatible standard-library code only.
- Pure domain rules under `src/cmf_builder/domain/`.
- Application commands, authority and checkpoint selection under `src/cmf_builder/application/`.
- Explicit ports plus deterministic in-memory/file-reading adapters under the exact allowed adapter paths.
- No API, CLI or UI is required; the application command interface is the independently testable public seam.
- No network access, service installation, database, migration, package dependency, container, worker or external credential.
- Registry and compatibility inputs are read-only and hash-checked; implementation must not copy them into a new source of truth.

## Bounded target rule

The implementation may recognize `atomic_content_harness`, `visual_asset_editor`, and `content_asset_delegation_contract` as the only governed compilation-target identities. The only executable Story path is:

`atomic_content_harness` -> `2d_character_animation` -> `format02_minimal_coach_theatre`

VAE, Delegation and conversational selections must return a typed `UnsupportedTargetForAuthorizedSlice` or equivalent fail-closed outcome. Recognizing their identity is not implementing their behavior.

## Done boundary

The Story is complete only when every Given/When/Then criterion and deterministic test passes, required events/evidence are captured, capsule/file hashes are recorded, rollback is demonstrated for the additive scaffold, and a `StoryCompletionReceipt` is issued. Completion does not make ST-01.02 ready, certify Format 02, or change full Release 1/full-product readiness.

