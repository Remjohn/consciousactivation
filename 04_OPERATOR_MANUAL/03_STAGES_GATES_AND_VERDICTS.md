# Stages, Gates and Verdicts

- `PASS`: evidence is sufficient to enter the next explicitly named stage.
- `CONCERNS`: work may continue only where the current stage permits it; named concerns must remain visible.
- `FAIL`: the next gated stage is prohibited unless an explicit, documented override defines a bounded non-production exception.
- `BLOCKED`: required evidence or dependency is unavailable.
- `HUMAN CONFIRMATION`: automated preparation is complete; the operator is authorizing the stated baseline, not the entire product.

External blockers do not erase valid local work. They prevent overclaiming readiness.
