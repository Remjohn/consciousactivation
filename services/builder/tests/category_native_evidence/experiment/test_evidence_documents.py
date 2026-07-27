from __future__ import annotations

from pathlib import Path

import yaml

from cmf_builder.category_evidence.experiment_contracts import (
    ExperimentArm,
    governed_case_templates,
    template_arm_identity,
)
from cmf_builder.category_evidence.experiment_evaluation import (
    DIMENSIONS,
    NONCOMPENSABLE_FAILURES,
    rubric_identity,
)


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "docs/implementation/category-native-evidence"


def load(name: str):
    return yaml.safe_load((EVIDENCE / name).read_text(encoding="utf-8"))


def test_case_and_arm_template_hashes_match_the_implementation() -> None:
    manifest = load("BD007_CASE_MANIFEST.yaml")
    hashes = load("BD007_NATIVE_AND_FLATTENED_INPUT_HASHES.yaml")
    by_id = {item["case_id"]: item for item in manifest["templates"]}
    hash_by_id = {item["case_id"]: item for item in hashes["templates"]}
    for template in governed_case_templates():
        assert by_id[template.case_id]["template_sha256"] == template.template_identity
        assert hash_by_id[template.case_id]["case_template_sha256"] == template.template_identity
        assert hash_by_id[template.case_id]["native_arm_template_sha256"] == template_arm_identity(
            template, ExperimentArm.NATIVE
        )
        assert hash_by_id[template.case_id]["flattened_arm_template_sha256"] == template_arm_identity(
            template, ExperimentArm.FLATTENED
        )


def test_rubric_and_noncompensable_register_match_frozen_code() -> None:
    rubric = load("BD007_EVALUATION_RUBRIC.yaml")
    failures = load("BD007_NONCOMPENSABLE_FAILURES.yaml")
    assert rubric["rubric_sha256"] == rubric_identity()
    assert [item["id"] for item in rubric["dimensions"]] == list(DIMENSIONS)
    assert [item["id"] for item in failures["failures"]] == list(NONCOMPENSABLE_FAILURES)


def test_evidence_documents_make_no_unearned_empirical_claim() -> None:
    manifest = load("BD007_CASE_MANIFEST.yaml")
    hashes = load("BD007_NATIVE_AND_FLATTENED_INPUT_HASHES.yaml")
    plan = load("BD007_TRIAL_PLAN.yaml")
    assert manifest["summary"]["executable_case_count"] == 0
    assert manifest["summary"]["live_calls_performed"] == 0
    assert manifest["summary"]["scorecards_created"] == 0
    assert all(item["admitted_member_binding"] is None for item in manifest["templates"])
    assert hashes["live_empirical_state"]["provider_outputs_hashed"] == 0
    assert plan["not_executed_declarations"]["empirical_advantage_claimed"] is False
    assert plan["production_ready"] is False
    assert plan["certified"] is False


def test_trial_plan_requires_admission_authority_and_complete_repeats() -> None:
    plan = load("BD007_TRIAL_PLAN.yaml")
    assert "truthful_operator_declaration_receipt_valid" in plan["gates"]
    assert "provider_calls_budget_and_credential_authorized" in plan["gates"]
    assert plan["execution_design"]["repeats_per_arm_per_configuration"] == 3
    assert plan["execution_design"]["minimum_calls_per_configuration"] == 24
    assert plan["closure_rule"]["native_noncompensable_failures"] == 0
