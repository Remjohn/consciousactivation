# Visual Derivative Production Program — CAE Governance

## Program Identity
- **Program ID**: `visual_derivative_production_program`
- **Version**: `1.0.0`
- **Phase**: 4 — Production and Acceptance (Mandate M42)
- **Harness**: `VISUAL_DERIVATIVE_PRODUCTION_HARNESS_V1`
- **State Machine**: `VISUAL_DERIVATIVE_PRODUCTION_STATE_MACHINE_V1`

## Authority Invariants
1. **Four Authority Lanes Separation**:
   - `COMMANDER`: Admits programs, authorizes derivative releases, conducts repair pathways, and signs receipts.
   - `HUNTER`: Extracts multi-modal visual source spans and verbatim evidence anchors from authentic recordings.
   - `ANALYST`: Performs dual-axis QA evaluation (Semantic QA: source fidelity, quote checksums, wrong-reading locks; Render QA: file existence, byte size, dimensions, geometry pass, frame integrity).
   - `COMPOSER`: Compiles `CompositionIR` requests and triggers physical rendering/realization passes.
2. **Dual-Axis QA Independence**:
   - Semantic QA evaluates meaning, quotes, and locks.
   - Render QA evaluates geometry, files, dimensions, and frame integrity.
   - Acceptance requires BOTH dimensions to pass independently. Rendering success alone is never evidence of semantic validity.
3. **Passive Flat Skills**:
   - Zero Skill-to-Skill delegation.
   - Zero subagents.
4. **Source Sovereignty & Anti-Synthetic Defense**:
   - All derivative claims must bind to authentic evidence spans with matching cryptographic hashes.
   - Synthetic or mock fixtures fail closed.
