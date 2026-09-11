# Phase 2 — Replay / Idempotency Contract

Every state-changing operation declares:
- effect kind;
- replay-safe / replay-unsafe / reconciliation-required;
- idempotency key;
- settlement ID;
- reconciliation/compensation;
- receipt semantics;
- failure window.

Exactly-once external effects must never be assumed across process failure.
