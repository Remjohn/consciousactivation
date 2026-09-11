# CAE-BMAD Review, Proof, Gates & Promotion Specification

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL SPECIFICATION  
**Authority:** CAE Rebuild Program / Operator Mandate M11  
**Scope:** Countertest execution standards, false-proof defenses, adversarial review protocol, operator gate lifecycle, promotion criteria, and non-destructive rollback procedures.

---

## 1. The Anti-False-Proof Standard

In CAE-BMAD, an implementation claim is considered a **false proof** if any of the following conditions exist:
1. **Green Test without Runtime Touch:** A test passes trivially without importing, invoking, or asserting upon physical code surfaces.
2. **Markdown-Only Delivery:** A capability is declared "implemented" merely because a `.md` or `.yaml` file was written.
3. **Untested Negative Paths:** An implementation lacks countertests proving that invalid inputs, out-of-bound arguments, and cyclic references fail cleanly.
4. **Unratified Promotion:** An agent declares a mandate or stage "PROMOTED" without explicit human operator gate sign-off.

---

## 2. The 5-Stage Gate Promotion Lifecycle

```text
[ DRAFT ]
   ↓
[ IN_REVIEW ] (Schema validation + unit tests)
   ↓
[ AUDITED ] (Adversarial reviewer + countertests)
   ↓
[ OPERATOR_GATE ] (Human operator review of evidence packet)
   ↓
[ PROMOTED ] (Canonical baseline locked) OR [ ROLLBACK ] (Quarantine & remediation)
```

---

## 3. Mandatory Countertest Suite Standard

Every major mandate must provide at least 3 distinct countertest patterns:
1. **Truncation / Missing Boundary Countertest:** Rejects inputs with fewer than the minimum required elements.
2. **Invalid Enum / Schema Countertest:** Rejects unapproved type flags, statuses, or arbitrary strings.
3. **Missing Line Proof / Traceability Countertest:** Rejects claims lacking exact line citations or source lineage.

---

## 4. Rollback and Quarantine Protocol

When a gate fails or an invalid promotion is detected:
1. **Quarantine:** Isolate offending artifacts into `quarantine/` with a timestamped diagnostic manifest.
2. **Revert State:** Reset the state machine to the previous certified checkpoint.
3. **Preserve Audit Trail:** Never delete failed test output or negative audit reports; record them in `REVIEW_AND_GATE_RECORD.md`.
