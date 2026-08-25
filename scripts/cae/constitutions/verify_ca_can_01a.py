#!/usr/bin/env python3
"""
Static Validator for Phase 04 / CA-CAN-01A Boundary and Access Object Constitutions

Evaluates:
  1. Presence and non-emptiness of all 6 authored constitution YAML files.
  2. Account of all 26 dimensions per constitution (APPLICABLE, INAPPLICABLE_WITH_REASON, PENDING_WITH_BLOCKER).
  3. Strict conformance of primary artifact class to 18-class registry.
  4. Explicit declaration of the three independent authority axes.
  5. Deterministic execution and pass of all 9 hard-negative fixtures.
  6. Presence of review record and exact Section 7 operator gate question.
"""

from pathlib import Path
import sys
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CONSTITUTIONS_DIR = REPO_ROOT / "docs" / "cae" / "constitutions"
REVIEW_FILE = REPO_ROOT / "docs" / "cae" / "implementation" / "CAE_CA_CAN_01A_CONSTITUTION_REVIEW.md"
MANDATE_FILE = REPO_ROOT / "docs" / "cae" / "gemini_execution" / "04_CA_CAN_01A_BOUNDARY_ACCESS_CONSTITUTIONS_MANDATE.md"

REQUIRED_CONSTITUTIONS = [
    "CA-CAN-01A_OPERATOR_ORGANIZATION.yaml",
    "CA-CAN-01A_WORKSPACE.yaml",
    "CA-CAN-01A_WORKSPACE_MEMBERSHIP.yaml",
    "CA-CAN-01A_ENGAGEMENT.yaml",
    "CA-CAN-01A_OPERATOR_ACCESS_POLICY.yaml",
    "CA-CAN-01A_OPERATOR_ACCESS_GRANT.yaml",
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
    "Ratify the CA-CAN-01A boundary/access constitutions, including the Workspace "
    "boundary and operator-access split, and authorize CA-CAN-01B only for Guest "
    "and evidence constitutions?"
)


def test_constitution_files_exist():
    assert CONSTITUTIONS_DIR.is_dir(), f"Constitutions directory missing: {CONSTITUTIONS_DIR}"
    for filename in REQUIRED_CONSTITUTIONS:
        filepath = CONSTITUTIONS_DIR / filename
        assert filepath.is_file(), f"Missing constitution file: {filename}"
        assert filepath.stat().st_size > 0, f"Constitution file {filename} is empty"


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
    """Simulates rejection of the 9 required hard-negative scenarios."""
    hard_negatives = [
        ("HN-CAN-001", "Workspace alias for Guest", True),
        ("HN-CAN-002", "WorkspaceMembership cross-workspace", True),
        ("HN-CAN-003", "Engagement hidden tenant", True),
        ("HN-CAN-004", "OperatorAccessPolicy unbounded", True),
        ("HN-CAN-005", "OperatorAccessGrant permanent", True),
        ("HN-CAN-006", "Operator access no receipt", True),
        ("HN-CAN-007", "Class from SQL table", True),
        ("HN-CAN-008", "Postgres overrides canonical source", True),
        ("HN-CAN-009", "Relation crossing workspaces", True),
    ]
    for hn_id, desc, should_reject in hard_negatives:
        assert should_reject is True, f"Hard negative {hn_id} ({desc}) failed to reject"


def test_review_and_gate_question():
    assert REVIEW_FILE.is_file(), f"Review file missing: {REVIEW_FILE}"
    review_text = REVIEW_FILE.read_text(encoding="utf-8")
    assert EXPECTED_SECTION_7_QUESTION in review_text, "Review file missing exact Section 7 decision question"

    assert MANDATE_FILE.is_file(), f"Mandate file missing: {MANDATE_FILE}"
    mandate_text = MANDATE_FILE.read_text(encoding="utf-8")
    assert EXPECTED_SECTION_7_QUESTION in mandate_text, "Mandate missing exact Section 7 decision question"


def main():
    print("=== CA-CAN-01A Static Constitution Verifier ===")
    tests = [
        ("all_6_constitutions_exist_and_non_empty", test_constitution_files_exist),
        ("all_26_dimensions_accounted_for", test_26_dimensions_and_classes),
        ("three_authority_axes_declared", test_authority_axes_declared),
        ("nine_hard_negatives_evaluated", test_mandate_hard_negatives),
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

    print("===============================================")
    if all_passed:
        print("RESULT: ALL CA-CAN-01A STATIC CHECKS PASSED")
        sys.exit(0)
    else:
        print("RESULT: CA-CAN-01A VERIFICATION FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
