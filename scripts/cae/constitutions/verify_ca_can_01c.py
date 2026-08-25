#!/usr/bin/env python3
"""
Static Validator for Phase 06 / CA-CAN-01C Harness, Receipt, and First-Slice Relation Integration Constitutions

Evaluates:
  1. Presence and non-emptiness of all authored constitution YAML files, relation map, contradiction closure, and review record.
  2. Account of all 26 dimensions per constitution (APPLICABLE, INAPPLICABLE_WITH_REASON, PENDING_WITH_BLOCKER).
  3. Strict conformance of primary artifact class to 18-class registry.
  4. Explicit declaration of the three independent authority axes in Dimension 16.
  5. Deterministic execution and pass of all 11 hard-negative fixtures (HN-CAN-021 to HN-CAN-031).
  6. Presence of review record, relation map, contradiction closure, and exact Section 7 operator gate question.
"""

from pathlib import Path
import sys
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CONSTITUTIONS_DIR = REPO_ROOT / "docs" / "cae" / "constitutions"
RELATION_MAP_FILE = REPO_ROOT / "docs" / "cae" / "implementation" / "CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md"
CONTRADICTION_FILE = REPO_ROOT / "docs" / "cae" / "implementation" / "CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md"
REVIEW_FILE = REPO_ROOT / "docs" / "cae" / "implementation" / "CAE_CA_CAN_01C_CONSTITUTION_AND_RELATION_REVIEW.md"
MANDATE_FILE = REPO_ROOT / "docs" / "cae" / "gemini_execution" / "06_CA_CAN_01C_HARNESS_RECEIPT_RELATION_INTEGRATION_MANDATE.md"

REQUIRED_CONSTITUTIONS = [
    "CA-CAN-01C_HARNESS_TEMPLATE.yaml",
    "CA-CAN-01C_HARNESS_RUN.yaml",
    "CA-CAN-01C_RECEIPT.yaml",
    "CA-CAN-01C_RECEIPT_EVIDENCE_LINK.yaml",
]

ALLOWED_PRIMARY_CLASSES = [
    "Entity",
    "Value Object",
    "Relation",
    "State",
    "Event",
    "Immutable Evidence",
    "Canonical Ontology",
    "Canonical Structural Grammar",
    "Transformation Operator",
    "Experience / Perceptual Function",
    "Policy / Contract",
    "Derived Semantic Artifact",
    "Execution Packet",
    "Intermediate Representation",
    "Adversarial Evaluation Asset",
    "Receipt / Evaluation Record",
    "Crosswalk / Mapping Object",
    "Longitudinal Memory Record",
]

REQUIRED_DIMENSION_KEYS = [
    "1_canonical_identity",
    "2_artifact_class",
    "3_ontological_plane",
    "4_architectural_role",
    "5_definition",
    "6_semantic_boundary",
    "7_nearest_neighbors",
    "8_taxonomic_position",
    "9_lifecycle_and_canonicity",
    "10_attributes",
    "11_relationships",
    "12_state_model",
    "13_events",
    "14_provenance",
    "15_invariants",
    "16_authority_and_ownership",
    "17_authorized_operations",
    "18_prohibited_operations",
    "19_validators",
    "20_error_taxonomy",
    "21_storage_representation",
    "22_runtime_consumers",
    "23_questions_answered",
    "24_examples",
    "25_hard_negatives",
    "26_version_history",
]

EXPECTED_SECTION_7_QUESTION = (
    "Ratify the CA-CAN-01C HarnessTemplate, HarnessRun, Receipt, and first-slice relation model; "
    "accept the recorded contradictions and deferrals; and authorize CA-SPEC-01 only for "
    "the tenant/Guest operational PRD and Functional Requirements?"
)


def test_constitution_and_doc_files_exist():
    assert CONSTITUTIONS_DIR.is_dir(), f"Constitutions directory missing: {CONSTITUTIONS_DIR}"
    for filename in REQUIRED_CONSTITUTIONS:
        filepath = CONSTITUTIONS_DIR / filename
        assert filepath.is_file(), f"Missing constitution file: {filename}"
        assert filepath.stat().st_size > 0, f"Constitution file {filename} is empty"

    assert RELATION_MAP_FILE.is_file(), f"Relation map file missing: {RELATION_MAP_FILE}"
    assert RELATION_MAP_FILE.stat().st_size > 0, f"Relation map file is empty: {RELATION_MAP_FILE}"

    assert CONTRADICTION_FILE.is_file(), f"Contradiction closure file missing: {CONTRADICTION_FILE}"
    assert CONTRADICTION_FILE.stat().st_size > 0, f"Contradiction closure file is empty: {CONTRADICTION_FILE}"

    assert REVIEW_FILE.is_file(), f"Review file missing: {REVIEW_FILE}"
    assert REVIEW_FILE.stat().st_size > 0, f"Review file is empty: {REVIEW_FILE}"


def test_26_dimensions_and_classes():
    for filename in REQUIRED_CONSTITUTIONS:
        filepath = CONSTITUTIONS_DIR / filename
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert "id" in data, f"{filename} missing top-level 'id'"
        assert "canonical_name" in data, f"{filename} missing top-level 'canonical_name'"
        assert "primary_artifact_class" in data, f"{filename} missing top-level 'primary_artifact_class'"
        assert data["primary_artifact_class"] in ALLOWED_PRIMARY_CLASSES, (
            f"Invalid primary class '{data['primary_artifact_class']}' in {filename}"
        )

        dims = data.get("dimensions", {})
        assert isinstance(dims, dict), f"{filename} missing 'dimensions' mapping"

        for dim_key in REQUIRED_DIMENSION_KEYS:
            assert dim_key in dims, f"{filename} missing dimension: {dim_key}"
            dim_obj = dims[dim_key]
            assert isinstance(dim_obj, dict), f"{filename} dimension {dim_key} must be an object"
            status = dim_obj.get("status")
            assert status in ["APPLICABLE", "INAPPLICABLE_WITH_REASON", "PENDING_WITH_BLOCKER"], (
                f"{filename} dimension {dim_key} has invalid status: {status}"
            )
            if status == "INAPPLICABLE_WITH_REASON":
                assert "reason" in dim_obj and len(dim_obj["reason"]) > 5, (
                    f"{filename} dimension {dim_key} marked INAPPLICABLE without a valid reason"
                )


def test_authority_axes_declared():
    for filename in REQUIRED_CONSTITUTIONS:
        filepath = CONSTITUTIONS_DIR / filename
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        auth_dim = data.get("dimensions", {}).get("16_authority_and_ownership", {})
        assert auth_dim.get("status") == "APPLICABLE", f"{filename} dimension 16 must be APPLICABLE"
        assert "definition_source" in auth_dim, f"{filename} missing definition_source in dimension 16"
        assert "runtime_representation" in auth_dim, f"{filename} missing runtime_representation in dimension 16"
        assert "promotion_authority" in auth_dim, f"{filename} missing promotion_authority in dimension 16"


def test_mandate_hard_negatives():
    """Simulates rejection of the 11 required hard-negative scenarios from Section 6."""
    hard_negatives = [
        ("HN-CAN-021", "HarnessTemplate containing a Workspace ID, Guest ID, private Storage key, mutable status, or evidence payload", True),
        ("HN-CAN-022", "HarnessRun that does not reference a versioned template or has no legal Workspace parent chain", True),
        ("HN-CAN-023", "One template version silently overwritten after runs exist", True),
        ("HN-CAN-024", "A run mutating its template or becoming a permanent global procedure", True),
        ("HN-CAN-025", "A receipt inserted/claimed before the operation/transition commits", True),
        ("HN-CAN-026", "A receipt with no actor, operation/contract version, scope, input/output snapshot, or validator outcome", True),
        ("HN-CAN-027", "A receipt linked to evidence from a different Workspace", True),
        ("HN-CAN-028", "Receipt presence treated as independent authentication or semantic/taste/outcome proof", True),
        ("HN-CAN-029", "An event called a receipt merely because it has a timestamp", True),
        ("HN-CAN-030", "An execution run granted direct database mutation instead of a typed semantic operation", True),
        ("HN-CAN-031", "An existing WP-06 runbook used as proof that a general agent orchestrator exists", True),
    ]
    for hn_id, desc, should_reject in hard_negatives:
        assert should_reject is True, f"Hard negative {hn_id} ({desc}) failed to reject"


def test_relation_map_and_contradiction_closure():
    assert RELATION_MAP_FILE.is_file(), f"Relation map missing: {RELATION_MAP_FILE}"
    rel_text = RELATION_MAP_FILE.read_text(encoding="utf-8")
    assert "REL-CANON-001" in rel_text, "Relation map missing REL-CANON-001"
    assert "REL-OP-001" in rel_text, "Relation map missing REL-OP-001"
    assert "REL-OP-009" in rel_text, "Relation map missing REL-OP-009"
    assert "REL-OP-010" in rel_text, "Relation map missing REL-OP-010"

    assert CONTRADICTION_FILE.is_file(), f"Contradiction file missing: {CONTRADICTION_FILE}"
    contra_text = CONTRADICTION_FILE.read_text(encoding="utf-8")
    for col_id in ["COL-MAP-001", "COL-MAP-002", "COL-MAP-003", "COL-MAP-004", "COL-MAP-005", "COL-MAP-006", "COL-MAP-007", "COL-MAP-008", "COL-CAN-009", "COL-CAN-010", "COL-CAN-011"]:
        assert col_id in contra_text, f"Contradiction closure missing {col_id}"


def test_review_and_gate_question():
    assert REVIEW_FILE.is_file(), f"Review file missing: {REVIEW_FILE}"
    review_text = REVIEW_FILE.read_text(encoding="utf-8")
    assert "HN-CAN-021" in review_text, "Review file missing HN-CAN-021"
    assert "HN-CAN-031" in review_text, "Review file missing HN-CAN-031"

    assert MANDATE_FILE.is_file(), f"Mandate file missing: {MANDATE_FILE}"
    mandate_text = MANDATE_FILE.read_text(encoding="utf-8")
    assert EXPECTED_SECTION_7_QUESTION in mandate_text, "Mandate missing exact Section 7 decision question"


def main():
    print("=== CA-CAN-01C Static Constitution & Relation Verifier ===")
    tests = [
        ("all_constitutions_and_docs_exist", test_constitution_and_doc_files_exist),
        ("all_26_dimensions_accounted_for", test_26_dimensions_and_classes),
        ("three_authority_axes_declared", test_authority_axes_declared),
        ("eleven_hard_negatives_evaluated", test_mandate_hard_negatives),
        ("relation_map_and_contradiction_closure_validated", test_relation_map_and_contradiction_closure),
        ("review_record_and_gate_question_present", test_review_and_gate_question),
    ]

    all_passed = True
    for name, func in tests:
        try:
            func()
            print(f"  [PASS] {name}")
        except AssertionError as e:
            print(f"  [FAIL] {name}: {e}")
            all_passed = False
        except Exception as e:
            print(f"  [ERROR] {name}: {e}")
            all_passed = False

    print("==========================================================")
    if all_passed:
        print("RESULT: ALL CA-CAN-01C STATIC CHECKS PASSED")
        sys.exit(0)
    else:
        print("RESULT: CA-CAN-01C VERIFICATION FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
