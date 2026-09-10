from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = REPO_ROOT / "docs/cae/evidence/M068"
MATRIX_PATH = EVIDENCE_DIR / "CAE_M068_READINESS_MATRIX.json"
GAP_PATH = EVIDENCE_DIR / "CAE_M068_RESIDUAL_GAP_LEDGER.json"
MANIFEST_PATH = EVIDENCE_DIR / "CAE_M068_EVIDENCE_MANIFEST.json"
REPORT_PATH = EVIDENCE_DIR / "CAE_M068_PRODUCTION_READINESS_CERTIFICATION_REPORT.md"
STATE_PATH = REPO_ROOT / "docs/cae/state/CAE_M068_COMPLETION_RECORD.md"

ALLOWED_STATUSES = {"VERIFIED", "PARTIAL", "BLOCKED", "NOT IN SCOPE"}
EXPECTED_MANDATES = [f"CAE-M0{n}" for n in range(58, 68)]
EXPECTED_COUNTS = {"VERIFIED": 4, "PARTIAL": 5, "BLOCKED": 1, "NOT IN SCOPE": 0}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def test_readiness_matrix_has_exactly_ten_campaign_criteria():
    matrix = _load_json(MATRIX_PATH)
    assert matrix["mandate_id"] == "CAE-M068"
    assert matrix["invariant"] == "INV-CERT-REAL-001"
    assert matrix["criteria_count"] == 10
    assert len(matrix["criteria"]) == 10
    assert [row["mandate_id"] for row in matrix["criteria"]] == EXPECTED_MANDATES


def test_readiness_statuses_are_approved_and_summary_is_consistent():
    matrix = _load_json(MATRIX_PATH)
    counts = {status: 0 for status in ALLOWED_STATUSES}
    for row in matrix["criteria"]:
        assert row["status"] in ALLOWED_STATUSES
        counts[row["status"]] += 1
    assert counts == matrix["summary_counts"] == EXPECTED_COUNTS


def test_each_criterion_has_verifier_scope_and_limitations():
    matrix = _load_json(MATRIX_PATH)
    for row in matrix["criteria"]:
        assert row["criterion"]
        assert row["evidence_class"]
        assert row["evidence_refs"]
        assert row["result"]
        assert row["limitation"]


def test_all_referenced_repository_evidence_paths_exist():
    matrix = _load_json(MATRIX_PATH)
    missing = []
    for row in matrix["criteria"]:
        for ref in row["evidence_refs"]:
            # Directory references are valid evidence anchors too.
            if not (REPO_ROOT / ref).exists():
                missing.append(ref)
    assert missing == []


def test_critical_cross_boundary_criterion_is_blocked():
    matrix = _load_json(MATRIX_PATH)
    m067 = next(row for row in matrix["criteria"] if row["mandate_id"] == "CAE-M067")
    assert m067["status"] == "BLOCKED"
    assert matrix["certification_state"] == "BLOCKED"


def test_m067_upstream_operator_gate_remains_blocked_and_undecided():
    decision = _load_json(
        REPO_ROOT / "docs/cae/evidence/M067/CAE_M067_OPERATOR_DECISION_RECORD.json"
    )
    assert decision["decision_status"] == "OPERATOR_DECISION_REQUIRED"
    assert decision["decision"] is None
    assert decision["recommended_disposition"] == "BLOCK"


def test_no_native_runtime_receipt_is_falsely_claimed():
    receipts = _load_json(
        REPO_ROOT / "docs/cae/evidence/M067/CAE_M067_RUNTIME_RECEIPTS.json"
    )
    native = receipts["native_openchatcut"]
    assert native["reachable"] is False
    assert native["receipt_status"] == "NOT_ISSUED_EXECUTED"
    assert native["mock_substitution"] == "PROHIBITED_AND_NOT_USED"


def test_gap_ledger_contains_all_m067_open_gaps_and_additional_evidence_gaps():
    gaps = _load_json(GAP_PATH)
    gap_ids = {gap["gap_id"] for gap in gaps["open_gaps"]}
    required = {
        "GAP-M068-001",
        "GAP-M068-002",
        "GAP-M068-003",
        "GAP-M068-004",
        "GAP-M068-005",
        "GAP-M068-006",
        "GAP-M068-007",
        "GAP-M068-008",
    }
    assert gaps["status"] == "BLOCKED"
    assert gap_ids == required
    assert all(gap["status"] == "OPEN" for gap in gaps["open_gaps"])


def test_next_campaign_is_proposed_but_not_started():
    gaps = _load_json(GAP_PATH)
    frontier = gaps["next_campaign_frontier"]
    assert frontier["proposed_campaign"] == "Live Runtime and Release-Evidence Closure"
    assert frontier["prohibition"] == "Do not begin this next campaign under M0068; it is only the proposed frontier."


def test_manifest_hash_and_source_identity_are_exact():
    manifest = _load_json(MANIFEST_PATH)
    material = dict(manifest)
    claimed = material.pop("manifest_sha256")
    recomputed = hashlib.sha256(
        json.dumps(material, sort_keys=True).encode("utf-8")
    ).hexdigest()
    assert claimed == recomputed
    assert manifest["git_commit_sha"] is None
    assert len(manifest["source_archive_sha256"]) == 64
    for rel, expected_hash in manifest["entries"].items():
        assert _sha256_file(REPO_ROOT / rel) == expected_hash


def test_report_and_state_match_blocked_certification():
    report = REPORT_PATH.read_text(encoding="utf-8")
    state = STATE_PATH.read_text(encoding="utf-8")
    required_phrases = [
        "**Certified Operational Status:** `BLOCKED`",
        "## 2. Certification matrix",
        "## 5. What the verifier actually measures",
        "## 6. False-proof countercase",
        "## 8. State transition / control record",
        "## 11. Proposed next campaign frontier",
        "## 12. Operator decision",
    ]
    for phrase in required_phrases:
        assert phrase in report
    assert "**Status:** `CERTIFIED BLOCKED — OPERATOR DECISION REQUIRED`" in state
    assert "Exact Git commit:\n`UNAVAILABLE — uploaded archive contains no .git metadata.`" in state
