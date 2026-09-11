# Evidence-to-AIR First-Slice Skill

**Companion runbook:** `evidence_to_air_first_slice_v1.yaml` v1.0.0
**Authority:** procedural doctrine only. PostgreSQL/Supabase remains the
authoritative current state, history, events, and receipts.

## Recognition

Use this procedure only for a verified source package/media asset that is being
captured as evidence, independently authenticated, proposed/validated as a
bounded assessment, and sent to named operator review. It does not authorize
question planning, an assertion of Guest truth, SDA/SFL/Primitive selection,
Coalition creation, or a SemanticProgram.

## Procedure

1. Load current aggregate projection and inspect the registered transition
   contract. Never infer state from a prior prompt, runbook note, or receipt.
2. In `RECON`, verify source-to-media relationship, `VERIFIED` media lifecycle,
   and actor workspace membership.
3. Invoke only the runbook-listed typed semantic operation with an idempotency
   key and expected version.
4. After each operation, independently read aggregate state plus command,
   event, and receipt. Advance procedural state only when they agree.
5. At `AUTHENTICATE`, the evaluator must differ from the capture actor.
6. At `OPERATOR_REVIEW`, require a named operator decision; do not turn a
   missing decision into `COMPLETE`.

## Transition discipline

- A missing source, evidence span, actor, contract, receipt, or aggregate
  projection is `BLOCKED` or `REPAIR_REQUIRED`, never success.
- A stale version, idempotency conflict, or payload-integrity failure is a
  typed failure. Preserve its diagnostic and do not retry blindly.
- Do not expose or resolve quarantined registry identities. This slice is
  intentionally registry-neutral.
- A green E3 staging path does not prove semantic quality, human truth, taste,
  anti-centroid integrity, or real-world outcome; those remain unproven until
  their own evaluator and E4 evidence exist.
