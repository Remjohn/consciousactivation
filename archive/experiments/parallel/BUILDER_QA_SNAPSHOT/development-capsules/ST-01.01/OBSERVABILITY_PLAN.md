# Observability Plan

## Required evidence fields

Every Story-level success or rejection observation contains:

- `run_id`
- `story_id` = `ST-01.01`
- `artifact_identity`
- `authority_identity`
- `version`
- `provenance`
- `outcome`
- `failure_context` (empty object on success, typed data on failure)
- `correlation_id`
- `causation_id`
- `command_id`
- `target_id`
- `category_id`
- `profile_id`
- `stream_version`

No observation contains source evidence bodies, Human Reaction material, credentials or secrets.

## Domain events

Accepted authoritative operations emit immutable events from the TS-01 vocabulary as applicable: `RunCreated`, `TargetProfileSelected`, `LifecycleTransitioned`, `LifecycleWaiverGranted`, `CheckpointCreated`, `RunResumed`, and `RunCancelled`. Each event has deterministic identity, actor/authority reference, prior and resulting stream versions, policy/profile versions and causation.

Rejected operations emit diagnostic observations but no authoritative state event. Required typed reasons include `TargetSelectionRejected`, `UnsupportedTargetForAuthorizedSlice`, `TransitionRejected`, `AuthorityDenied`, `ConcurrencyConflict`, `IdempotencyPayloadMismatch`, `CheckpointInvalid`, and `ResumeRejected`.

## Story outcome events

- Success: `ST-01.01:OutcomeVerified`
- Failure: `ST-01.01:OutcomeRejected`
- Completion receipt link: `ST-01.01:StoryCompletionReceipt`

## Required measures

- accepted and rejected command counts by reason;
- lifecycle transition validation duration;
- checkpoint selected/invalid count;
- replayed event count;
- resume duration;
- duplicate command count;
- authority allow/deny count;
- waiver count and expiry result;
- external-target or conversational execution rejection count.

Performance values are observations, not certification thresholds. The TS-01 p95 targets remain subject to later Release 1 calibration.

## Completion evidence

`completion/OBSERVABILITY_EVIDENCE.json` must include at least one redacted success example, one invalid-transition example, one authority-denial example, one resume example, field-completeness checks, and proof that rejected commands did not change the authoritative stream. Missing fields or leaked prohibited data fail completion.

