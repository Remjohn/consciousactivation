# Observability plan

Emit durable observation intents with fields `run_id`, `story_id`, `artifact_identity`,
`authority_identity`, `version`, `provenance`, `outcome` and `failure_context`.

Required observations are:

- `ST-01.03:EvidenceIndexStarted`;
- `ST-01.03:SpecimenInventoryCompleted` with descriptor/specimen counts;
- `ST-01.03:EvidenceIndexCommitted` with index and Source Lock hashes;
- `ST-01.03:OutcomeVerified`;
- `ST-01.03:OutcomeRejected` with typed error code and no sensitive payload;
- `ST-01.03:EvidenceIndexReplayReturned`;
- `ST-01.03:EvidenceIndexInvalidated`.

Successful observations commit with the Story state through the repository outbox.
Delivery failure leaves retryable intent and cannot change the command verdict.
Rejection observations may be emitted only when no Story state committed.
