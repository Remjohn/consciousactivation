# CAE-BMAD Brownfield Reconciliation Specification

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL SPECIFICATION  
**Authority:** CAE Rebuild Program / Operator Mandate M10  
**Scope:** Reality contact enforcement, brownfield delta reconciliation, missing-layer detection, legacy quarantine standards, and the Missing Implementation Register across all 13 operating levels.

---

## 1. The Reality Enforcement Mandate

A foundational principle of CAE-BMAD is that **missing implementation must never be concealed**.
- A plan, PRD, or architectural document claiming a capability that does not exist in code must be explicitly cataloged as `MISSING_LAYER` or `PARTIAL_IMPLEMENTATION`.
- `cae-brownfield-auditor` is structurally adversarial to ungrounded claims, ensuring that greenfield aspirations are cleanly distinguished from empirical codebase reality.

```text
Product Claims / Intent (Levels 01-05)
                ↕
[ BROWNFIELD DELTA RECONCILIATION ]
                ↕
Empirical Codebase Reality (Levels 06-13)
```

---

## 2. Fidelity Classification Taxonomy

Every subsystem, capability, or story evaluated receives one of four formal verdicts:
1. `VERIFIED_COMPLETE`: Backed by active code on disk, resolvable entrypoints, and passing tests.
2. `PARTIAL_IMPLEMENTATION`: Code exists on disk (e.g. domain models, compilers) but lacks complete end-to-end integration or tests.
3. `MISSING_LAYER`: Documented in PRD/architecture but zero corresponding physical code exists on disk.
4. `CONTRADICTED`: Implementation directly conflicts with product intent or constitutional invariants.

---

## 3. Legacy Quarantine & Migration Standard

1. **Non-Destructive Quarantine:** Legacy code in `Conscious Activation Engine Brownfield/` is preserved as historical evidence and reference lineage, not deleted.
2. **Explicit Crosswalk Mapping:** Any active capability inherited from brownfield must be mapped through explicit crosswalks in `docs/cae-bmad/01_reconstruction/PRODUCT_RECONSTRUCTION.md`.
3. **Reality Gap Registry:** All identified gaps are compiled into `docs/cae-bmad/07_brownfield/MISSING_IMPLEMENTATION_REGISTER.md` with blocking flags and remediation paths.
