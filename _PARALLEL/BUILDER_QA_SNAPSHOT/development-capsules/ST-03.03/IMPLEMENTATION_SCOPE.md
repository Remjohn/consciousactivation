# Implementation scope

Implement one Builder-owned vertical command that compiles the active synthetic run's exact immutable upstream artifacts into one canonical `HarnessIR` snapshot.

The command must:

1. Load the run, Source Lock, frozen boundary, ratification, and Draft Harness Model through typed ports.
2. Require lifecycle `ATOMICITY_RATIFICATION`, exact active references, no upstream invalidation, the repository-owned synthetic profile, and `HG-003=PASS` evidence.
3. Compile the complete initial IR section set from upstream governed values without semantic invention or authority promotion.
4. Preserve each material value's value, authority, knowledge status, evidence/decision references, confidence/disposition, creator/version, and dependency impact.
5. Represent absent synthetic Activative/category/external fields as explicit governed `NOT_APPLICABLE` values under their canonical keys, never as generic notes.
6. Canonicalize JSON deterministically using UTF-8, sorted keys, normalized values, and no timestamp inside the IR identity hash.
7. Keep `HarnessIR` separate from `WorkflowIR` and reject orchestration fields.
8. Declare initial compatibility: read/write `1.0.0`, no supported prior migrations, unsupported versions blocked, and an explicit empty deprecation set.
9. Atomically commit snapshot, run reference/event, command record, and compilation receipt with optimistic concurrency and idempotent replay.
10. Emit complete Story observations and provide a formal invalidation link when the upstream boundary/model is reopened.

The implementation remains in-memory development/test persistence. It may not generate Markdown, OpenSpec, schemas, target packages, an Atomic Harness Definition, or a Development Capsule for the synthetic task; those are later Stories.
