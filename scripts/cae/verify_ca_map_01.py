"""Static verification script for CA-MAP-01 scope, authority, and plane mapping artifacts."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = ROOT / "docs" / "cae" / "implementation"

FILES = {
    "matrix": DOCS_DIR / "CAE_SCOPE_AND_AUTHORITY_MATRIX.md",
    "collision": DOCS_DIR / "CAE_OBJECT_SCOPE_COLLISION_REGISTER.md",
    "plane_map": DOCS_DIR / "CAE_CANONICAL_OPERATIONAL_PLANE_MAP.md",
    "crosswalk": DOCS_DIR / "CAE_CA_MAP_01_SOURCE_CROSSWALK.md",
    "completion": DOCS_DIR / "CAE_CA_MAP_01_COMPLETION_RECORD.md",
}

REQUIRED_MATRIX_COLUMNS = [
    "object",
    "candidate primary class",
    "canonical/operational plane",
    "scope class",
    "current authority",
    "target runtime representation",
    "definition source",
    "change/promotion authority",
    "owner",
    "mutability/history",
    "legal parent chain",
    "write boundary",
    "evidence/receipt",
    "storage",
    "consumers",
    "evidence reference",
    "status",
    "unresolved question",
]

REQUIRED_OBJECTS = [
    "OperatorOrganization",
    "Workspace",
    "WorkspaceMembership",
    "OperatorAccessPolicy",
    "OperatorAccessGrant",
    "Engagement",
    "Guest",
    "GuestIdentityLink",
    "MediaAsset",
    "Immutable Media Evidence Bytes",
    "HarnessTemplate",
    "HarnessRun",
    "Receipt",
    "ExecutionReceipt",
    "SDA Registry",
    "SFL Registry",
    "Primitive Registry",
    "SourcePackage",
    "InterviewSession",
    "InterviewTurn",
    "EvidenceItem",
    "EvidenceSpan",
    "EvidenceAuthentication",
    "SemanticAssessment",
    "AssessmentEvidenceLink",
    "StateAggregate",
    "StateTransitionContract",
    "StateTransition",
    "Command",
    "Event",
]

REQUIRED_COLLISION_IDS = [
    "COL-MAP-001",
    "COL-MAP-002",
    "COL-MAP-003",
    "COL-MAP-004",
    "COL-MAP-005",
    "COL-MAP-006",
    "COL-MAP-007",
    "COL-MAP-008",
]

EXACT_SECTION_7_QUESTION = (
    "Approve the CA-MAP-01 scope/authority map, confirm Workspace as the initial "
    "client boundary, and authorize CA-AUTH-01 only: development-uncertified authoring "
    "controls and static validators?"
)


def verify() -> dict[str, bool]:
    results = {}

    # 1. File existence and size check
    all_files_exist = True
    for key, path in FILES.items():
        if not path.is_file() or path.stat().st_size < 500:
            print(f"FAIL: File {path} missing or too small")
            all_files_exist = False
    results["all_mapping_files_exist_and_non_empty"] = all_files_exist

    matrix_text = FILES["matrix"].read_text(encoding="utf-8")
    collision_text = FILES["collision"].read_text(encoding="utf-8")
    plane_map_text = FILES["plane_map"].read_text(encoding="utf-8")
    crosswalk_text = FILES["crosswalk"].read_text(encoding="utf-8")
    completion_text = FILES["completion"].read_text(encoding="utf-8")

    # 2. Matrix column validation
    matrix_header_match = re.search(r"\|\s*object\s*\|.*\|", matrix_text, re.IGNORECASE)
    if matrix_header_match:
        header_line = matrix_header_match.group(0).lower()
        cols_present = all(col.lower() in header_line for col in REQUIRED_MATRIX_COLUMNS)
        results["matrix_has_all_18_required_columns"] = cols_present
    else:
        results["matrix_has_all_18_required_columns"] = False

    # 3. Object completeness in matrix
    objects_found = [obj for obj in REQUIRED_OBJECTS if f"`{obj}`" in matrix_text or obj in matrix_text]
    results["all_scoped_objects_present_in_matrix"] = (len(objects_found) == len(REQUIRED_OBJECTS))
    if len(objects_found) < len(REQUIRED_OBJECTS):
        missing = set(REQUIRED_OBJECTS) - set(objects_found)
        print(f"Missing objects in matrix: {missing}")

    # 4. Evidence labels present
    evidence_tags = [
        "[EXECUTABLE]",
        "[SCHEMA]",
        "[MIGRATION]",
        "[REGISTRY_SOURCE]",
        "[DOCUMENT]",
        "[TEST]",
        "[HYPOTHESIS]",
        "[OPERATOR_DECISION_REQUIRED]",
    ]
    results["evidence_classification_tags_used"] = all(tag in matrix_text for tag in evidence_tags)

    # 5. Collision register items validation
    collisions_found = all(col_id in collision_text for col_id in REQUIRED_COLLISION_IDS)
    results["all_required_collisions_registered"] = collisions_found

    # 6. Collision status validation (only RATIFIED, SPLIT, DEFERRED, BLOCKED)
    valid_statuses = ["RATIFIED", "SPLIT", "DEFERRED", "BLOCKED"]
    status_matches = re.findall(r"\*\*Status\*\*\s*\|\s*`([A-Z_]+)`", collision_text)
    results["collision_statuses_valid"] = len(status_matches) > 0 and all(
        any(valid in s for valid in valid_statuses) for s in status_matches
    )

    # 7. Plane map principles present
    results["plane_map_covers_isolation_and_boundaries"] = (
        "CANONICAL PLANE" in plane_map_text
        and "OPERATIONAL PLANE" in plane_map_text
        and "Workspace" in plane_map_text
        and "THREE AXES OF AUTHORITY" in plane_map_text
        and "Legal Parent Chains" in plane_map_text
    )

    # 8. Source crosswalk coverage
    results["source_crosswalk_covers_brownfield_classifications"] = (
        "NEW" in crosswalk_text
        and "EXTEND" in crosswalk_text
        and "ADAPT" in crosswalk_text
        and "RETAIN" in crosswalk_text
        and "QUARANTINE" in crosswalk_text
    )

    # 9. Exact Section 7 stop question present
    results["exact_section_7_decision_question_present"] = EXACT_SECTION_7_QUESTION in completion_text

    return results


def main() -> int:
    print("=== CA-MAP-01 Static Mapping Verifier ===")
    results = verify()
    all_passed = True
    for check_name, passed in results.items():
        status_str = "PASS" if passed else "FAIL"
        print(f"  [{status_str}] {check_name}")
        if not passed:
            all_passed = False

    print("=========================================")
    if all_passed:
        print("RESULT: ALL CA-MAP-01 STATIC CHECKS PASSED")
        return 0
    else:
        print("RESULT: CA-MAP-01 STATIC CHECKS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
