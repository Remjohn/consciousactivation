"""
Unit and structural tests for Mandate CA-UPTL-01 — Upstream Intelligence Completion.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
IMPL_DIR = ROOT_DIR / "docs" / "cae" / "implementation"

sys.path.insert(0, str(ROOT_DIR / "scripts" / "cae" / "audit"))
sys.path.insert(0, str(ROOT_DIR / "packages" / "ca_contracts" / "src"))
sys.path.insert(0, str(ROOT_DIR / "packages" / "ca_runtime" / "src"))
sys.path.insert(0, str(ROOT_DIR / "services" / "pipeline" / "src"))
sys.path.insert(0, str(ROOT_DIR / "services" / "air" / "src"))

import verify_ca_uptl_01


def test_required_documentation_files_exist():
    """All 6 CA-UPTL-01 documentation files exist and are non-empty."""
    for fname in verify_ca_uptl_01.REQUIRED_DOCS:
        fpath = IMPL_DIR / fname
        assert fpath.is_file(), f"Missing file: {fname}"
        assert fpath.stat().st_size > 0, f"Empty file: {fname}"


def test_admission_and_reclassifications():
    """Admission record documents formal authorization and reclassification of prior chain."""
    content = (IMPL_DIR / "CAE_UPTL_01_ADMISSION_RECORD.md").read_text(encoding="utf-8")
    assert "CLAIMS_UNVERIFIED_BY_OPERATOR" in content
    assert "CA-E3-08" in content
    assert "CA-STAGE-09" in content
    assert "CA-ACCEPT-10" in content
    assert "ADMITTED_AND_AUTHORIZED" in content


def test_u1_custodian_disposition_packet():
    """Custodian disposition packet catalogs 5 absent SFL families, duplicate, and 23 unversioned records."""
    content = (IMPL_DIR / "CAE_UPTL_01_CUSTODIAN_DISPOSITION_PACKET.md").read_text(encoding="utf-8")
    assert "SFL-FAM-005" in content
    assert "EXP-TRG-001" in content
    assert "Route B" in content
    assert "RegistryItemQuarantinedError" in content


def test_u1_registry_typed_refusals():
    """Runtime Registry raises typed refusal errors on quarantined/ambiguous/versionless items."""
    passed, msg = verify_ca_uptl_01.probe_2_u1_registry_defect_refusal()
    assert passed, msg


def test_u2_model_reasoning_module():
    """ModelReasoningEngine registers entities, executes inference or loudly fails on missing credentials."""
    passed, msg = verify_ca_uptl_01.probe_3_u2_reasoning_module()
    assert passed, msg


def test_u3_semantic_chain_demonstration():
    """SemanticChainDemonstration executes World -> Context -> SDA -> Edging with immutable receipts."""
    passed, msg = verify_ca_uptl_01.probe_4_u3_semantic_chain_demonstration()
    assert passed, msg


def test_u4_air_generation_services():
    """AIR generation services (F17, F28, F29, F30) enforce reasoning engine requirements and fail against stubs."""
    passed, msg = verify_ca_uptl_01.probe_5_u4_air_generation_services()
    assert passed, msg


def test_completion_record_structure_and_gate_decision():
    """Completion record contains verbatim Section 7 gate prompt and epistemic certifications."""
    content = (IMPL_DIR / "CAE_UPTL_01_COMPLETION_RECORD.md").read_text(encoding="utf-8")
    assert "CA-UPTL-01" in content
    assert "reward_hack_result: UNVERIFIED" in content
    assert "CLAIMS_UNVERIFIED_BY_OPERATOR" in content
    assert "CA-CAN-02" in content
