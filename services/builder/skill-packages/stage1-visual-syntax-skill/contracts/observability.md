# Observability — Visual Syntax Reconstruction Analyst

## Telemetry & Audit Receipts

This Skill emits one contract report per invocation, conforming to
`contracts/output.schema.json`, containing:

- `harness_id` — the single harness this invocation processed.
- `input_receipt` — the data-integrity block (recorded vs. observed
  sha256, match boolean, vision_model_used, base_url, pipeline-deviation
  flag). Technical only — see `references/context-requirements.md`.
- `checkpoints_completed` — which of the eight state-machine checkpoints
  this invocation reached.
- `observations` — the full evidence layer, per specimen frame.
- `taxonomy_summary` — canonical/variant/novel-candidate/unknown counts,
  plus the full novel-candidate proposals for operator inspection.
- `syntax_analyses` — the assembled visual syntax per slide, including
  `syntax_hash` for deduplication.
- `validation_summary` — structural/semantic/evidence status plus the full
  findings list with error codes.
- `fyi` — non-blocking notes only (e.g. an unrelated artifact the Skill
  noticed but did not act on).
- `operator_review` — always emitted with `operator_disposition: null` from
  this Skill; filled in later, outside this Skill's execution.
- `stage1_complete` / `compiler_ready` — always `false` as emitted by this
  Skill. These only become `true` downstream, once an operator `APPROVE`
  is recorded against a non-`BLOCKED`/`FAIL` technical status.

Nothing this Skill emits ever asserts licensing, provenance, or usability
disposition, and no downstream consumer should expect such a field to
exist in this output.
