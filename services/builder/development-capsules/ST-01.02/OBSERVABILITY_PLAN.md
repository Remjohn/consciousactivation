# Observability Plan

Emit and retain evidence for:

- `ST-01.02:SourceDiagnosticAccepted`
- `ST-01.02:SourceDiagnosticRejected`
- `ST-01.02:SourceLockCreated`
- `ST-01.02:SourceLockReplayReturned`
- `ST-01.02:SourceMutationDetected`
- `ST-01.02:OutcomeVerified`
- `ST-01.02:OutcomeRejected`

Every observation must include `run_id`, `story_id`, event name, command ID,
correlation/causation IDs, authority identity, target/category/profile identity,
source-profile ID/version/hash, portable target candidate, source-lock identity
when available, run stream version, outcome, and typed failure context.

The command receipt and completion evidence must additionally record file count,
total bytes, source kinds, archive count, required-role coverage, aggregate hash,
prior invalidated lock when applicable, adapter/contract version, elapsed test
evidence, and proof that no source mutation or extraction occurred.

Successful observations may not claim production readiness, certification,
semantic knowledge, or downstream execution. Rejected commands must prove zero
authoritative run-event and Source-Lock mutation.
