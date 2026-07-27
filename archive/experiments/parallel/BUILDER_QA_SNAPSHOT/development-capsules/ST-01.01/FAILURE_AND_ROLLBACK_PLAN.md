# Failure, Rollback and Cleanup Plan

## Runtime failure behavior

- Missing, multiple, unknown or non-authorized target/profile: typed rejection; no run or event committed.
- Illegal lifecycle edge or incomplete prerequisite: `TransitionRejected`; no state mutation.
- Unauthorized actor or unsafe waiver: `AuthorityDenied`; no state mutation or grant expansion.
- Expected-version mismatch: concurrency conflict containing current version; no retry side effect.
- Reused idempotency key with different payload: typed mismatch; original result remains authoritative.
- Corrupt checkpoint with valid event stream: quarantine the checkpoint, replay events, and emit an incident observation.
- Corrupt or discontinuous event stream or incompatible policy/profile identity: block resume; never reset or replace the run silently.
- Registry hash/identity mismatch: fail closed before run creation.
- Attempted VAE, Delegation, conversational, evidence, workflow, Control Tower or certification behavior: reject as outside the authorized slice.

## Implementation failure stop rule

Stop immediately if an acceptance criterion requires an unlisted file, new third-party dependency, schema/registry amendment, external service, later Story, policy decision, or external-product behavior. Preserve passing additive work and report the exact unmet criterion; do not broaden the capsule.

## Rollback boundary

The implementation is additive and uses only in-memory state. It creates no database, migration, durable production artifact, external message, credential, deployment or remote side effect. Rollback therefore consists of reverting only the exact implementation and test paths in `ALLOWED_FILE_SCOPE.yaml`; governed inputs and this immutable capsule are not edited.

Before completion receipt issuance:

1. record hashes of every created/modified path in `completion/FILE_CHANGE_MANIFEST.json`;
2. run the deterministic test command twice;
3. demonstrate that removing the additive `src/cmf_builder` and Story-test scaffold restores the pre-Story executable state without touching governed documents;
4. restore the implementation files after the demonstration and rerun tests; and
5. record the procedure and results in `completion/ROLLBACK_EVIDENCE.md`.

No automatic deletion is authorized by this plan. The implementation agent must use a reversible workspace/commit operation approved for the implementation context.

## Cleanup

Tests must dispose of in-memory stores, temporary checkpoints and captured observations after each case. They may not create pytest caches, bytecode files, files outside the completion-evidence directory, or persistent local services. Cleanup failure fails the Story receipt.

