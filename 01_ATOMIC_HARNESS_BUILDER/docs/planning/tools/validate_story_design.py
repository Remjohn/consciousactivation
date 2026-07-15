from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
PLANNING = ROOT / "docs" / "planning"

INVENTORY = PLANNING / "PLANNING_REQUIREMENTS_INVENTORY.csv"
EPIC_INVENTORY = PLANNING / "EPIC_INVENTORY.yaml"
EPIC_COVERAGE = PLANNING / "EPIC_REQUIREMENT_COVERAGE.csv"
EPIC_PROPOSAL = PLANNING / "EPIC_DESIGN_PROPOSAL.md"
EPIC_VALIDATION = PLANNING / "EPIC_DESIGN_VALIDATION_REPORT.json"
EPIC_CONFIRMATION = PLANNING / "EPIC_INVENTORY_CONFIRMATION_RECEIPT.yaml"

STORY_INVENTORY = PLANNING / "STORY_INVENTORY.yaml"
STORY_COVERAGE = PLANNING / "STORY_REQUIREMENT_COVERAGE.csv"
STORY_DEPENDENCIES = PLANNING / "STORY_DEPENDENCY_GRAPH.csv"
STORY_PROPOSAL = PLANNING / "STORY_DESIGN_PROPOSAL.md"
STORY_GROUPED = PLANNING / "STORY_INVENTORY_BY_EPIC.md"
STORY_BLOCKED = PLANNING / "STORY_BLOCKED_CONDITIONAL_REGISTER.yaml"
STORY_RELEASE_1 = PLANNING / "RELEASE_1_STORY_SUBSET.yaml"
STORY_CROSS_REPOSITORY = PLANNING / "STORY_CROSS_REPOSITORY_DEPENDENCIES.yaml"
REPORT = PLANNING / "STORY_DESIGN_VALIDATION_REPORT.json"
PROGRAM_STATUS = ROOT / "PROGRAM_STATUS_EXPORT.yaml"

REQUIRED_GATES = {"HD-006", "HD-007", "BD-004", "BD-007", "BD-008", "BD-010", "BD-014"}
EXPECTED_CATEGORIES = {
    "short_form_edited_video", "2d_character_animation", "carousels", "supervisuals", "conversational_activation_expression"
}
EXPECTED_PROFILES = {"public_comment", "reply_dm", "reelcast_expression", "interview_expression"}
EXPECTED_TARGETS = {"atomic_content_harness", "visual_asset_editor", "content_asset_delegation_contract"}
ALLOWED_GATE_STATES = {
    "BLOCKED_PENDING_HUMAN_DECISION",
    "EVIDENCE_GATED",
    "CONDITIONAL_EXTERNAL_DEPENDENCY",
    "PLANNING_COMPLETE_IMPLEMENTATION_PROHIBITED",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def refs(value: str | None) -> set[str]:
    if not value:
        return set()
    return {item.strip() for item in value.split(";") if item.strip()}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []

    inventory_rows = read_csv(INVENTORY) if INVENTORY.is_file() else []
    epic_rows = read_csv(EPIC_COVERAGE) if EPIC_COVERAGE.is_file() else []
    story_rows = read_csv(STORY_COVERAGE) if STORY_COVERAGE.is_file() else []
    dependency_rows = read_csv(STORY_DEPENDENCIES) if STORY_DEPENDENCIES.is_file() else []
    epic_doc = yaml.safe_load(EPIC_INVENTORY.read_text(encoding="utf-8")) if EPIC_INVENTORY.is_file() else {}
    story_doc = yaml.safe_load(STORY_INVENTORY.read_text(encoding="utf-8")) if STORY_INVENTORY.is_file() else {}
    blocked_doc = yaml.safe_load(STORY_BLOCKED.read_text(encoding="utf-8")) if STORY_BLOCKED.is_file() else {}
    release_1_doc = yaml.safe_load(STORY_RELEASE_1.read_text(encoding="utf-8")) if STORY_RELEASE_1.is_file() else {}
    cross_repository_doc = yaml.safe_load(STORY_CROSS_REPOSITORY.read_text(encoding="utf-8")) if STORY_CROSS_REPOSITORY.is_file() else {}
    confirmation = yaml.safe_load(EPIC_CONFIRMATION.read_text(encoding="utf-8")) if EPIC_CONFIRMATION.is_file() else {}
    program = yaml.safe_load(PROGRAM_STATUS.read_text(encoding="utf-8")) if PROGRAM_STATUS.is_file() else {}

    if confirmation.get("status") != "CONFIRMED_STEP_3_AUTHORIZED":
        errors.append("Epic confirmation receipt does not authorize Step 3")
    if confirmation.get("confirmation_text") != "CONFIRM BUILDER V1.2 EPIC INVENTORY AND BEGIN STEP 3":
        errors.append("Epic confirmation receipt does not preserve the exact human response")
    confirmed_design = confirmation.get("confirmed_epic_design", {})
    expected_hash_paths = {
        "epic_inventory": EPIC_INVENTORY,
        "epic_requirement_coverage": EPIC_COVERAGE,
        "epic_design_proposal": EPIC_PROPOSAL,
        "epic_design_validation": EPIC_VALIDATION,
    }
    for key, path in expected_hash_paths.items():
        if confirmed_design.get(key, {}).get("sha256") != sha256(path):
            errors.append(f"confirmed Step 2 artifact hash changed: {key}")

    epic_by_id = {item["id"]: item for item in epic_doc.get("epics", [])}
    epic_ids = set(epic_by_id)
    categories = {item["category_id"] for item in epic_doc.get("canonical_categories", [])}
    profiles = {item["profile_id"] for item in epic_doc.get("conversational_profiles", [])}
    targets = {item["target_id"] for item in epic_doc.get("compilation_targets", [])}
    if categories != EXPECTED_CATEGORIES:
        errors.append(f"confirmed category set changed: {sorted(categories)}")
    if profiles != EXPECTED_PROFILES:
        errors.append(f"confirmed conversational profile set changed: {sorted(profiles)}")
    if targets != EXPECTED_TARGETS:
        errors.append(f"confirmed compilation target set changed: {sorted(targets)}")

    boundary = story_doc.get("planning_boundary", {})
    if story_doc.get("schema_version") != "cmf-builder-vertical-story-inventory/v2":
        errors.append("Story registry schema version is not the complete Step 3 v2 contract")
    if story_doc.get("status") != "PROPOSED_AWAITING_HUMAN_CONFIRMATION":
        errors.append("Story inventory is not awaiting human confirmation")
    if boundary.get("story_authoring_completed") is not True:
        errors.append("Story inventory does not report Story authoring complete")
    if boundary.get("step_4_authorized") is not False:
        errors.append("Story inventory improperly authorizes Step 4")
    if boundary.get("production_implementation_authorized") is not False:
        errors.append("Story inventory improperly authorizes production implementation")
    if boundary.get("implementation_readiness") != "FAIL":
        errors.append("Story inventory does not preserve implementation readiness FAIL")

    stories = story_doc.get("stories", [])
    story_ids = [item.get("story_id", "") for item in stories]
    if len(stories) != 69 or len(set(story_ids)) != 69:
        errors.append(f"Story inventory must contain 69 unique Stories, found {len(stories)}")
    if sorted(item.get("global_order") for item in stories) != list(range(1, 70)):
        errors.append("Story global order must be exactly 1 through 69")
    if any(not re.fullmatch(r"ST-\d{2}\.\d{2}", story_id) for story_id in story_ids):
        errors.append("one or more Story IDs do not match ST-NN.NN")

    story_by_id = {item["story_id"]: item for item in stories if item.get("story_id")}
    order_by_id = {item["story_id"]: item["global_order"] for item in stories if item.get("story_id")}
    primary_counts = Counter(row.get("primary_story_id", "") for row in story_rows)
    dependency_edges = 0

    for item in stories:
        story_id = item["story_id"]
        if item.get("epic_id") not in epic_ids:
            errors.append(f"{story_id}: unknown Epic {item.get('epic_id')}")
        for field in (
            "title", "primary_outcome", "narrative", "prerequisites", "release_1_disposition", "release_1_role",
            "implementation_owners", "component_boundary", "relevant_requirements", "affected_contracts_and_schemas",
            "contracts_and_seams", "failure_behavior", "authority_behavior", "observability", "observability_evidence",
            "migration_or_compatibility", "implementation_gate_status", "cross_product_boundary",
            "acceptance_criteria", "test_plan", "completion_receipt", "fresh_context_scope",
        ):
            if not item.get(field):
                errors.append(f"{story_id}: missing {field}")
        narrative = item.get("narrative", {})
        if not all(narrative.get(field) for field in ("as_a", "i_want", "so_that")):
            errors.append(f"{story_id}: incomplete user-value narrative")
        if not isinstance(item.get("primary_outcome"), str) or item.get("primary_outcome") != narrative.get("so_that"):
            errors.append(f"{story_id}: must declare exactly one scalar primary outcome matching the user-value narrative")
        if item.get("primary_obligation_count") != len(item.get("primary_obligation_ids", [])):
            errors.append(f"{story_id}: primary obligation count differs from listed IDs")
        if primary_counts[story_id] != item.get("primary_obligation_count"):
            errors.append(f"{story_id}: coverage row count differs from Story inventory")
        if not 1 <= item.get("primary_obligation_count", 0) <= 15:
            errors.append(f"{story_id}: fresh-context obligation count is outside 1..15")
        requirements = item.get("relevant_requirements", {})
        requirement_partition = (
            requirements.get("fr_ids", [])
            + requirements.get("nfr_ids", [])
            + requirements.get("other_planning_obligation_ids", [])
        )
        if set(requirement_partition) != set(item.get("primary_obligation_ids", [])) or len(requirement_partition) != len(set(requirement_partition)):
            errors.append(f"{story_id}: FR/NFR/other requirement partition differs from owned obligations")
        if any(not requirement.startswith("FR-") for requirement in requirements.get("fr_ids", [])):
            errors.append(f"{story_id}: relevant FR list contains a non-FR obligation")
        if any(not requirement.startswith("NFR-") for requirement in requirements.get("nfr_ids", [])):
            errors.append(f"{story_id}: relevant NFR list contains a non-NFR obligation")
        prerequisites = item.get("prerequisites", {})
        expected_receipts = {f"{dependency}:StoryCompletionReceipt" for dependency in item.get("dependencies", [])}
        if set(prerequisites.get("story_receipts", [])) != expected_receipts:
            errors.append(f"{story_id}: prerequisite completion receipts differ from Story dependencies")
        if set(prerequisites.get("decision_or_blocker_ids", [])) != set(item.get("gate_refs", [])):
            errors.append(f"{story_id}: prerequisite blocker IDs differ from Story gate references")
        expected_cross_repository = set(epic_by_id.get(item.get("epic_id"), {}).get("cross_repository_dependencies", []))
        if set(prerequisites.get("cross_repository_dependency_ids", [])) != expected_cross_repository:
            errors.append(f"{story_id}: cross-repository prerequisites differ from the confirmed Epic")
        contracts = item.get("affected_contracts_and_schemas", {})
        if not contracts.get("contract_ids_or_planned_handles") or not contracts.get("schema_disposition"):
            errors.append(f"{story_id}: affected contracts or schema disposition is missing")
        for schema_ref in contracts.get("schema_refs", []):
            schema_path = schema_ref.split("#", 1)[0]
            if not (ROOT / schema_path).is_file():
                errors.append(f"{story_id}: affected schema does not exist: {schema_ref}")
        criteria = item.get("acceptance_criteria", [])
        joined = " ".join(criteria)
        if len(criteria) < 3 or not criteria[0].startswith("Given ") or not criteria[1].startswith("When ") or not criteria[2].startswith("Then "):
            errors.append(f"{story_id}: acceptance criteria are not testable Given/When/Then statements")
        for term in ("Given", "When", "Then", "failure", "authority", "observable", "compatibility"):
            if term.lower() not in joined.lower():
                errors.append(f"{story_id}: acceptance criteria missing {term}")
        test_plan = item.get("test_plan", {})
        required_tests = test_plan.get("required_tests", [])
        if not test_plan.get("public_seam") or len(required_tests) < 4:
            errors.append(f"{story_id}: test plan lacks a public seam or required vertical, negative, authority, and receipt tests")
        if len({test.get("test_id") for test in required_tests}) != len(required_tests):
            errors.append(f"{story_id}: test IDs are not unique")
        if any(not test.get("assertion") for test in required_tests):
            errors.append(f"{story_id}: one or more tests lack a verifiable assertion")
        observability = item.get("observability_evidence", {})
        if not all(observability.get(field) for field in ("required_fields", "success_evidence", "failure_evidence", "receipt_link")):
            errors.append(f"{story_id}: observability evidence contract is incomplete")
        completion = item.get("completion_receipt", {})
        if completion.get("receipt_type") != "StoryCompletionReceipt" or completion.get("current_status") != "PLANNED_NOT_ISSUED":
            errors.append(f"{story_id}: completion receipt is missing or improperly issued during planning")
        if not completion.get("receipt_id_template", "").startswith(f"{story_id}:StoryCompletionReceipt:"):
            errors.append(f"{story_id}: completion receipt identity is not Story-scoped")
        if not completion.get("required_evidence") or not completion.get("issuance_rule"):
            errors.append(f"{story_id}: completion receipt lacks evidence or issuance rules")
        gate_state = item.get("implementation_gate_status")
        if gate_state not in ALLOWED_GATE_STATES:
            errors.append(f"{story_id}: invalid implementation gate state {gate_state}")
        if item.get("gate_refs") and gate_state not in {"BLOCKED_PENDING_HUMAN_DECISION", "EVIDENCE_GATED"}:
            errors.append(f"{story_id}: unresolved decision or blocker is not marked blocked or evidence-gated")
        cross_boundary = item.get("cross_product_boundary", {})
        prohibited = " ".join(cross_boundary.get("prohibited_builder_implementation", []))
        for external_boundary in ("Visual Asset Editor", "Delegation Protocol", "Interview Expression", "ReelCast"):
            if external_boundary not in prohibited:
                errors.append(f"{story_id}: cross-product boundary omits {external_boundary}")
        for dependency in item.get("dependencies", []):
            dependency_edges += 1
            if dependency not in story_by_id:
                errors.append(f"{story_id}: unknown dependency {dependency}")
            elif order_by_id[dependency] >= order_by_id[story_id]:
                errors.append(f"{story_id}: dependency {dependency} is not earlier")

    inventory_ids = {row["inventory_id"] for row in inventory_rows}
    story_coverage_ids = [row.get("inventory_id", "") for row in story_rows]
    duplicate_ids = sorted(item for item, count in Counter(story_coverage_ids).items() if count > 1)
    missing_ids = sorted(inventory_ids - set(story_coverage_ids))
    extra_ids = sorted(set(story_coverage_ids) - inventory_ids)
    if duplicate_ids:
        errors.append(f"duplicate Story coverage IDs: {duplicate_ids}")
    if missing_ids or extra_ids:
        errors.append(f"Story coverage differs missing={missing_ids} extra={extra_ids}")

    epic_by_inventory = {row["inventory_id"]: row["primary_epic_id"] for row in epic_rows}
    story_coverage_by_id = {row["inventory_id"]: row for row in story_rows if row.get("inventory_id")}
    carried_gates = set()
    authority_counts = Counter()
    story_counts_by_epic = Counter()
    for row in story_rows:
        inventory_id = row.get("inventory_id", "<missing>")
        story_id = row.get("primary_story_id", "")
        story_item = story_by_id.get(story_id, {})
        if row.get("primary_epic_id") != epic_by_inventory.get(inventory_id):
            errors.append(f"{inventory_id}: Story mapping changes confirmed primary Epic ownership")
        if story_item.get("epic_id") != row.get("primary_epic_id"):
            errors.append(f"{inventory_id}: Story belongs to a different Epic")
        source = next((item for item in inventory_rows if item["inventory_id"] == inventory_id), {})
        if row.get("authority_type") != source.get("authority_type"):
            errors.append(f"{inventory_id}: authority type differs from confirmed inventory")
        if row.get("source_release_scope") != source.get("release_scope"):
            errors.append(f"{inventory_id}: release scope differs from confirmed inventory")
        if not refs(source.get("active_blockers")) <= refs(row.get("gate_refs")):
            errors.append(f"{inventory_id}: active blocker not carried to Story")
        carried_gates |= refs(row.get("gate_refs"))
        authority_counts[row.get("authority_type", "")] += 1
        story_counts_by_epic[row.get("primary_epic_id", "")] += 1

    if not REQUIRED_GATES <= carried_gates:
        errors.append(f"required unresolved gates missing from Story design: {sorted(REQUIRED_GATES - carried_gates)}")

    dependency_by_story = {row.get("story_id", ""): row for row in dependency_rows}
    if set(dependency_by_story) != set(story_ids):
        errors.append("dependency graph Story IDs differ from Story inventory")
    for story_id, item in story_by_id.items():
        graph_row = dependency_by_story.get(story_id, {})
        if refs(graph_row.get("dependency_story_ids")) != set(item.get("dependencies", [])):
            errors.append(f"{story_id}: dependency graph differs from Story inventory")
        if graph_row.get("backward_only") != "true":
            errors.append(f"{story_id}: dependency graph is not backward-only")
        if refs(graph_row.get("prerequisite_receipt_ids")) != set(item.get("prerequisites", {}).get("story_receipts", [])):
            errors.append(f"{story_id}: dependency graph prerequisite receipts differ from Story inventory")
        if refs(graph_row.get("decision_or_blocker_ids")) != set(item.get("gate_refs", [])):
            errors.append(f"{story_id}: dependency graph blocker set differs from Story inventory")
        if refs(graph_row.get("cross_repository_dependency_ids")) != set(item.get("prerequisites", {}).get("cross_repository_dependency_ids", [])):
            errors.append(f"{story_id}: dependency graph cross-repository set differs from Story inventory")
        if graph_row.get("implementation_gate_status") != item.get("implementation_gate_status"):
            errors.append(f"{story_id}: dependency graph gate state differs from Story inventory")

    blocked_entries = blocked_doc.get("entries", [])
    blocked_by_story = {entry.get("story_id"): entry for entry in blocked_entries}
    expected_registered_story_ids = {
        story_id for story_id, item in story_by_id.items()
        if item.get("implementation_gate_status") != "PLANNING_COMPLETE_IMPLEMENTATION_PROHIBITED"
    }
    if set(blocked_by_story) != expected_registered_story_ids:
        errors.append("blocked and conditional register does not match gated Story set")
    if blocked_doc.get("entry_count") != len(blocked_entries):
        errors.append("blocked and conditional register count is incorrect")
    for story_id, entry in blocked_by_story.items():
        if entry.get("classification") != story_by_id.get(story_id, {}).get("implementation_gate_status"):
            errors.append(f"{story_id}: blocked register classification differs from Story inventory")
        if set(entry.get("decision_or_blocker_ids", [])) != set(story_by_id.get(story_id, {}).get("gate_refs", [])):
            errors.append(f"{story_id}: blocked register gate set differs from Story inventory")

    release_1_story_ids = release_1_doc.get("release_1_story_ids", [])
    if set(release_1_story_ids) != set(story_ids) or len(release_1_story_ids) != len(story_ids):
        errors.append("Release 1 Story subset does not identify every planned Release 1 Story exactly once")
    if release_1_doc.get("certified_reference_path") != "Format 02":
        errors.append("Release 1 subset does not preserve Format 02 as the certified reference path")
    if release_1_doc.get("reference_path_proof_story") != "ST-12.03" or release_1_doc.get("certification_scope_story") != "ST-12.04":
        errors.append("Release 1 subset does not identify the reference proof and bounded certification Stories")
    if release_1_doc.get("implementation_authorized") is not False or release_1_doc.get("implementation_readiness") != "FAIL":
        errors.append("Release 1 subset improperly authorizes implementation or changes readiness")
    certification_boundaries = release_1_doc.get("certification_boundaries", {})
    for boundary in ("format_02", "conversational_activation", "interview_expression", "reelcast_expression", "visual_asset_editor", "delegation_protocol"):
        if not certification_boundaries.get(boundary):
            errors.append(f"Release 1 subset omits certification boundary {boundary}")

    confirmed_cross_dependencies = {item["id"]: item for item in epic_doc.get("cross_repository_dependencies", [])}
    cross_dependencies = {item.get("id"): item for item in cross_repository_doc.get("dependencies", [])}
    if set(cross_dependencies) != set(confirmed_cross_dependencies):
        errors.append("cross-repository dependency register differs from confirmed Epic dependencies")
    for dependency_id, item in cross_dependencies.items():
        expected_epics = {
            epic["id"] for epic in epic_doc.get("epics", [])
            if dependency_id in epic.get("cross_repository_dependencies", [])
        }
        expected_stories = {story_id for story_id, story in story_by_id.items() if story.get("epic_id") in expected_epics}
        if set(item.get("consuming_epic_ids", [])) != expected_epics or set(item.get("consuming_story_ids", [])) != expected_stories:
            errors.append(f"{dependency_id}: cross-repository consumers differ from confirmed Story ownership")
        if not item.get("builder_boundary") or not item.get("current_constraint"):
            errors.append(f"{dependency_id}: cross-repository ownership boundary is incomplete")
    if cross_repository_doc.get("external_product_implementation_stories") != []:
        errors.append("cross-repository register contains external-product implementation Stories")

    grouped_text = STORY_GROUPED.read_text(encoding="utf-8") if STORY_GROUPED.is_file() else ""
    for epic_id in epic_ids:
        if epic_id not in grouped_text:
            errors.append(f"grouped Story inventory omits {epic_id}")
    for story_id in story_ids:
        if story_id not in grouped_text:
            errors.append(f"grouped Story inventory omits {story_id}")

    epic_story_counts = Counter(item.get("epic_id") for item in stories)
    if epic_story_counts.get("EP-09", 0) < 2 or epic_story_counts.get("EP-10", 0) < 2:
        errors.append("EP-09 or EP-10 was not decomposed into multiple vertical outcomes")
    if any(item.get("title", "").lower() in {"workflow runtime", "control tower"} for item in stories):
        errors.append("monolithic workflow runtime or Control Tower Story detected")

    if any(row.get("epic_ids") or row.get("story_ids") for row in inventory_rows):
        errors.append("confirmed 410-row inventory baseline was mutated")

    proposal_text = STORY_PROPOSAL.read_text(encoding="utf-8") if STORY_PROPOSAL.is_file() else ""
    for term in (
        "69", "410", "Step 4 full coverage and implementation-readiness validation: `NOT_AUTHORIZED`",
        "Production implementation: `PROHIBITED_READINESS_FAIL`", "ST-06.05", "ST-07.03", "ST-12.04",
    ):
        if term not in proposal_text:
            errors.append(f"Story proposal missing required term: {term}")

    if program.get("current_stage") != "story_step_3_complete_pending_human_confirmation":
        errors.append("program status does not report Step 3 complete pending confirmation")
    if program.get("vertical_story_authoring_authorized") is not True:
        errors.append("program status does not record Step 3 authorization")
    if program.get("step_4_authorized") is not False:
        errors.append("program status improperly authorizes Step 4")
    if program.get("production_implementation_authorized") is not False:
        errors.append("program status improperly authorizes production implementation")
    if program.get("baseline", {}).get("proposed_stories") != 69:
        errors.append("program status Story count is not 69")
    issued_completion_receipts = [
        item["story_id"] for item in stories
        if item.get("completion_receipt", {}).get("current_status") != "PLANNED_NOT_ISSUED"
    ]
    if issued_completion_receipts:
        errors.append(f"Story completion receipts were issued during planning: {issued_completion_receipts}")
    production_paths = [ROOT / path for path in ("src", "app", "packages", "tests")]
    if any(path.exists() for path in production_paths):
        errors.append("a production implementation path appeared during Step 3")

    status = "PASS" if not errors else "FAIL"
    report = {
        "status": status,
        "story_proposal_gate": "PENDING_HUMAN_CONFIRMATION",
        "step_4_gate": "NOT_AUTHORIZED",
        "production_implementation_gate": "PROHIBITED_READINESS_FAIL",
        "implementation_readiness_gate": "FAIL",
        "confirmed_epics": len(epic_ids),
        "proposed_stories": len(stories),
        "confirmed_obligations": len(inventory_rows),
        "primary_story_assignments": len(story_rows),
        "unique_primary_story_assignments": len(set(story_coverage_ids)),
        "missing_story_assignments": missing_ids,
        "duplicate_story_assignments": duplicate_ids,
        "stories_with_zero_primary_obligations": sorted(story_id for story_id in story_ids if primary_counts[story_id] == 0),
        "stories_with_exactly_one_primary_outcome": sum(isinstance(item.get("primary_outcome"), str) and bool(item.get("primary_outcome")) for item in stories),
        "stories_with_testable_given_when_then": sum(
            len(item.get("acceptance_criteria", [])) >= 3
            and item["acceptance_criteria"][0].startswith("Given ")
            and item["acceptance_criteria"][1].startswith("When ")
            and item["acceptance_criteria"][2].startswith("Then ")
            for item in stories
        ),
        "stories_with_explicit_test_plans": sum(len(item.get("test_plan", {}).get("required_tests", [])) >= 4 for item in stories),
        "story_completion_receipts_issued": len(issued_completion_receipts),
        "maximum_primary_obligations_per_story": max(primary_counts.values()) if primary_counts else 0,
        "dependency_edges": dependency_edges,
        "forward_dependency_edges": sum(
            order_by_id.get(dependency, 0) >= order_by_id.get(story_id, 0)
            for story_id, item in story_by_id.items() for dependency in item.get("dependencies", [])
        ),
        "backward_only_dependency_validation": "PASS" if not any("dependency" in error for error in errors) else "FAIL",
        "story_counts_by_epic": dict(sorted(Counter(item["epic_id"] for item in stories).items())),
        "implementation_gate_state_counts": dict(sorted(Counter(item.get("implementation_gate_status") for item in stories).items())),
        "blocked_or_conditional_register_entries": len(blocked_entries),
        "release_1_story_subset_count": len(release_1_story_ids),
        "cross_repository_dependency_count": len(cross_dependencies),
        "external_product_implementation_story_count": len(cross_repository_doc.get("external_product_implementation_stories", [])),
        "production_implementation_started": False if not any(path.exists() for path in production_paths) else True,
        "primary_obligation_counts_by_epic": dict(sorted(story_counts_by_epic.items())),
        "authority_type_counts": dict(sorted(authority_counts.items())),
        "canonical_categories": sorted(categories),
        "conversational_profiles": sorted(profiles),
        "compilation_targets": sorted(targets),
        "carried_decisions_and_blockers": sorted(carried_gates),
        "confirmed_inventory_sha256": sha256(INVENTORY),
        "errors": errors,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
