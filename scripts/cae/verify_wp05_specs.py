"""Structural check for the WP-05 reconciliation and first-slice Tech Spec."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RECONCILIATION = ROOT / "docs" / "cae" / "implementation" / "CAE_WP05_PRD_FR_TECHSPEC_RECONCILIATION.md"
TECH_SPEC = ROOT / "docs" / "cae" / "implementation" / "TS-CAE-EVID-001_EVIDENCE_TO_AIR_FIRST_SLICE.md"


def main() -> int:
    reconciliation = RECONCILIATION.read_text(encoding="utf-8")
    tech_spec = TECH_SPEC.read_text(encoding="utf-8")
    requirements = [f"FR-P05-{number:02d}" for number in range(1, 17)]
    requirements += [f"FR-P06-{number:02d}" for number in range(1, 19)]
    requirements += [f"FR-07-{number:02d}" for number in range(1, 16)]
    checks = {
        "all_phase_requirements_classified": all(requirement in reconciliation for requirement in requirements),
        "quarantines_explicit": all(identifier in reconciliation for identifier in ("SFL-FAM-005", "EXP-TRG-001")),
        "current_prd_preserved": "not rewritten" in reconciliation,
        "trace_matrix_present": "Object-to-runtime trace matrix" in reconciliation,
        "all_tech_spec_sections_present": all(f"## {number}." in tech_spec for number in range(1, 15)),
        "state_contracts_named": all(contract in tech_spec for contract in ("STC-EVID-000", "STC-EVID-001", "STC-AIR-001", "STC-AIR-002")),
        "reality_contact_boundary_explicit": "E4 required" in tech_spec and "no claim made" in tech_spec,
        "no_phase7_overclaim": "not a Phase-7 `SemanticProgram`" in tech_spec,
    }
    for name, passed in checks.items():
        print(f"{name}={'PASS' if passed else 'FAIL'}")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
