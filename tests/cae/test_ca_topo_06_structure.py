"""
Pure unit test suite for Phase 18 / CA-TOPO-06 structural and governance integrity.

Validates that all CA-TOPO-06 documentation artifacts, topology classifications,
contract-route mappings, option matrices, and control state entries conform to Mandate 18.
"""

from __future__ import annotations

from pathlib import Path
import pytest

DOCS_DIR = Path(__file__).resolve().parent.parent.parent / "docs/cae/implementation"
CONTROL_STATE_PATH = DOCS_DIR / "CAE_IMPLEMENTATION_CONTROL_STATE.md"


def test_ca_topo_06_documents_exist():
    expected_docs = [
        "CAE_TOPO_06_F02_TOPOLOGY_INVENTORY.md",
        "CAE_TOPO_06_F02_CONTRACT_ROUTE_MATRIX.md",
        "CAE_TOPO_06_F02_COLLISION_AND_OPTION_ANALYSIS.md",
        "CAE_TOPO_06_F02_READ_ONLY_STAGING_INSPECTION.md",
        "CAE_TOPO_06_OPERATOR_DECISION_PACKET.md",
        "CAE_TOPO_06_COMPLETION_RECORD.md",
    ]
    for doc in expected_docs:
        doc_path = DOCS_DIR / doc
        assert doc_path.is_file(), f"Missing required CA-TOPO-06 document: {doc}"
        assert doc_path.stat().st_size > 500, f"Document {doc} is unexpectedly small"


def test_ca_topo_06_topology_inventory_content():
    inv_path = DOCS_DIR / "CAE_TOPO_06_F02_TOPOLOGY_INVENTORY.md"
    content = inv_path.read_text(encoding="utf-8")
    assert "WP03_TEXT_FAMILY" in content
    assert "CA_IMPL_UUID_FAMILY" in content
    for i in range(1, 12):
        assert f"TOPO-{i:02d}" in content, f"Missing item TOPO-{i:02d} in topology inventory"
    assert "TOPOLOGY_EVIDENCED_DECISION_REQUIRED" in content


def test_ca_topo_06_contract_route_matrix_content():
    crm_path = DOCS_DIR / "CAE_TOPO_06_F02_CONTRACT_ROUTE_MATRIX.md"
    content = crm_path.read_text(encoding="utf-8")
    assert "CAE-BRIDGE-001.verified-interview-source-registration" in content
    assert "CAE-MEDIA-001.media-verification" in content
    assert "register_verified_interview_source" in content
    assert "verify_media_asset" in content
    assert "cae.project" in content
    assert "BLOCKED_SCHEMA_MISMATCH" in content
    assert "BOUNDED_TYPED_ROUTE_ACTIVE" in content


def test_ca_topo_06_collision_and_options_content():
    opt_path = DOCS_DIR / "CAE_TOPO_06_F02_COLLISION_AND_OPTION_ANALYSIS.md"
    content = opt_path.read_text(encoding="utf-8")
    assert "Option A: Canonical CA-IMPL UUID Target" in content
    assert "Option B: Canonical WP-03 Text-Keyed Topology" in content
    assert "Option C: Namespaced Dual Coexistence" in content
    assert "TS-CAE-TEN-001" in content


def test_ca_topo_06_staging_inspection_content():
    stg_path = DOCS_DIR / "CAE_TOPO_06_F02_READ_ONLY_STAGING_INSPECTION.md"
    content = stg_path.read_text(encoding="utf-8")
    assert "ENVIRONMENT_BLOCKED" in content
    assert "evnxdssbxxrsesftdvgx" in content
    assert "No Negative Inference" in content
    assert "Source Truth Rigor" in content


def test_ca_topo_06_operator_decision_packet_content():
    dp_path = DOCS_DIR / "CAE_TOPO_06_OPERATOR_DECISION_PACKET.md"
    content = dp_path.read_text(encoding="utf-8")
    assert "DECISION_TOPO_OPTION_A_CANONICAL_UUID_TARGET" in content
    assert "DECISION_TOPO_OPTION_B_RETAIN_WP03_TEXT_BASELINE" in content
    assert "DECISION_TOPO_OPTION_C_NAMESPACED_DUAL_COEXISTENCE" in content


def test_ca_topo_06_completion_record_and_section_6_question():
    comp_path = DOCS_DIR / "CAE_TOPO_06_COMPLETION_RECORD.md"
    content = comp_path.read_text(encoding="utf-8")
    for sec in [
        "## A. What Changed in the Disposable Target and Why",
        "## B. Tests, Environment, and Evidence Captured",
        "## C. What Failed or Remained Unproven",
        "## D. Cleanup and Teardown Result",
        "## E. F-01 and F-02 Status",
        "## F. Risks and Non-Claims",
        "## G. Exact Next Authorization Requested",
    ]:
        assert sec in content, f"Missing section '{sec}' in Completion Record"

    expected_q = (
        "Select one CA-TOPO-06 topology option and its named canonical route/identity boundary for the "
        "F-02-affected relations, preserve all other options and non-claims as rejected or deferred, and "
        "authorize CA-TOPO-07 only to implement and prove that selected topology in a new disposable "
        "environment—without moving client data, altering shared staging, or changing operational authority?"
    )
    assert " ".join(expected_q.split()) in " ".join(content.split())


def test_ca_topo_06_control_state():
    content = CONTROL_STATE_PATH.read_text(encoding="utf-8")
    assert "**Control status:** `F02_TOPOLOGY_EVIDENCED_DECISION_REQUIRED`" in content
    assert "current_work_package: CA-TOPO-06" in content
    assert "operational_authority_change: ZERO_AUTHORITY_CHANGED" in content
