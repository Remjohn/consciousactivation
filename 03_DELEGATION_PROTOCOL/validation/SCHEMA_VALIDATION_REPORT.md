# Schema Validation Report

Updated: 2026-07-14  
Status: `PASS`

- PRD-level schemas/examples: 25 / 25 valid.
- Active generated schemas/examples: 26 / 26 valid and closed.
- Visual Asset Demand schema ID/message version: `1.1`.
- All other message schemas remain `1.0` under envelope protocol `1.0`.
- Exact resource identities require resource ID, version, SHA-256 payload hash,
  and canonical reference.
- `wrong_reading_locks` is required with `minItems: 1`.
- Legacy demand aliases are rejected by the canonical schema.
- Generated authority paths resolve exactly once.

Executable evidence: 51 validator tests passed.
