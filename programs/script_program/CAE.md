# Script Program Runtime — CAE Governance

## Program Identity
- **Program ID**: `script_program`
- **Version**: `1.0.0`
- **Governing Mandates**: CAE Phase 4 Mandate M40, 00_CONTROL/30_PHASE4_PRODUCTION_CONTRACT.md, FR-APP-032

## Authority Lanes
1. **HUNTER**: Context admission, JIT Authoring Request assembly (`cae.script.request_jit@1.0.0`).
2. **COMPOSER**: Script proposal authoring, scene compilation, revisions (`cae.script.propose@1.0.0`, `cae.script.compile_package@1.0.0`, `cae.script.revise@1.0.0`).
3. **ANALYST**: Semantic QA verification, forbidden centroid checks, quote verification (`cae.script.evaluate_qa@1.0.0`).
4. **COMMANDER**: Backend-authoritative operator approval gate, transfer contract creation, repair (`cae.script.approve@1.0.0`, `cae.script.create_transfer_contract@1.0.0`, `cae.script.repair@1.0.0`).

## Invariants
- Transfer contract creation is strictly prohibited for unapproved scripts.
- Revisions create governed v2 proposals with explicit parent script SHA-256 and reset approval status.
- Spoken quote segments must match verbatim evidence hashes.
