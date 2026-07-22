from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.gates import GateStatus
from ccp_studio.contracts.legacy import LegacyDisposition, new_target_map
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.registry import RegistryConflict, RegistryFamily
from ccp_studio.gates.greenfield_gates import GreenfieldGateError, GreenfieldGateService
from ccp_studio.repositories.registry_entries import InMemoryRegistryRepository
from ccp_studio.services.migration_service import MigrationService


def _migration_repository_with_target():
    reviewer_id = uuid4()
    migration = MigrationService()
    entry = migration.propose_asset(
        source_path="src/ccp/services/anti_draft_calibrator.py",
        legacy_type="service_module",
        registry_family="Voice DNA Verification",
        canonicality_confidence=0.95,
        source_owner="CMF Core Team",
        runtime_language="Python",
        valuable_mechanics=["anti-draft checks"],
        known_defects=["slow sync calls"],
        content="legacy anti draft",
        disposition=LegacyDisposition.reference_implementation,
        actor_id=reviewer_id,
    )
    migration.map_asset(
        entry_id=entry.migration_ledger_entry_id,
        target_map=new_target_map(
            target_python_package="ccp_studio.dspy_programs.anti_draft_calibration_program",
            pydantic_contract_target="ccp_studio.contracts.voice.CalibrationReport",
            fixture_target="tests/fixtures/voice_dna_calibration_samples.json",
            eval_target="tests/evals/anti_draft_calibration_test.py",
            reviewer_actor_id=reviewer_id,
        ),
        actor_id=reviewer_id,
    )
    return migration.repository


def test_direct_production_import_from_legacy_runtime_fails_with_ledger_target():
    gate = GreenfieldGateService(migration_repository=_migration_repository_with_target())
    source_text = "from src.ccp.services.anti_draft_calibrator import AntiDraftCalibrator"

    receipt = gate.run_legacy_import_gate(object_ref="src/ccp_studio/services/example.py", source_text=source_text)

    assert receipt.status == GateStatus.blocked
    assert receipt.decision_code == "LEGACY_IMPORT_BLOCKED"
    assert receipt.repair_target == "ccp_studio.dspy_programs.anti_draft_calibration_program"


def test_clean_production_import_passes_legacy_import_gate():
    gate = GreenfieldGateService()

    receipt = gate.run_legacy_import_gate(
        object_ref="src/ccp_studio/services/example.py",
        source_text="from ccp_studio.contracts.skills import SaturationContextBundle",
    )

    assert receipt.status == GateStatus.approved
    assert receipt.decision_code == "LEGACY_IMPORT_GATE_PASSED"


def test_unapproved_prompt_stack_is_blocked_until_migrated_into_registry_or_compiler():
    gate = GreenfieldGateService()

    blocked = gate.validate_prompt_stack(object_ref="workflow:extract", raw_prompt="legacy raw prompt")
    approved = gate.validate_prompt_stack(
        object_ref="workflow:extract",
        raw_prompt="typed prompt",
        registry_entry_id=uuid4(),
    )

    assert blocked.status == GateStatus.blocked
    assert blocked.decision_code == "PROMPT_STACK_NOT_MIGRATED"
    assert approved.status == GateStatus.approved
    assert approved.decision_code == "PROMPT_STACK_APPROVED"


def test_duplicate_registry_truth_requires_conflict_resolution_before_activation():
    registry = InMemoryRegistryRepository()
    entry_id = uuid4()
    registry.put_conflict(
        RegistryConflict(
            schema_version="cmf.registry_conflict.v1",
            registry_conflict_id=uuid4(),
            registry_family=RegistryFamily.archetype,
            existing_registry_entry_id=uuid4(),
            proposed_registry_entry_id=entry_id,
            conflict_key="challenger",
            created_at=utc_now(),
        )
    )
    gate = GreenfieldGateService(registry_repository=registry)

    receipt = gate.validate_registry_conflicts(object_ref="registry:challenger", registry_entry_id=entry_id)

    assert receipt.status == GateStatus.blocked
    assert receipt.decision_code == "REGISTRY_CONFLICT_REQUIRES_REVIEW"


def test_provider_template_without_approved_hash_is_blocked_then_approved_hash_passes():
    gate = GreenfieldGateService()

    blocked = gate.validate_provider_template(template_key="comfyui:portrait:v1", content="{workflow:1}")
    approval = gate.approve_provider_template(
        template_key="comfyui:portrait:v1",
        content="{workflow:1}",
        compatibility_notes="Requires 24GB VRAM worker and source image input.",
        required_inputs=["source_image", "brand_style"],
        output_contract="ComfyWorkflowAsset",
        known_defects=["slow cold start"],
        evaluation_target_id=uuid4(),
        approved_by_actor_id=uuid4(),
    )
    approved = gate.validate_provider_template(template_key="comfyui:portrait:v1", content="{workflow:1}")
    mismatch = gate.validate_provider_template(template_key="comfyui:portrait:v1", content="{workflow:2}")

    assert blocked.decision_code == "PROVIDER_TEMPLATE_HASH_REQUIRED"
    assert approval.compatibility_notes.startswith("Requires")
    assert approved.status == GateStatus.approved
    assert mismatch.decision_code == "PROVIDER_TEMPLATE_HASH_MISMATCH"


def test_spec_runtime_boundary_drift_is_flagged_but_generated_leaf_consumers_pass():
    gate = GreenfieldGateService()

    drift = gate.run_spec_runtime_boundary_gate(
        object_ref="docs/tech-specs/bad.md",
        spec_text="TypeScript owns domain contracts and UI owns canonical state.",
    )
    leaf = gate.run_spec_runtime_boundary_gate(
        object_ref="docs/tech-specs/good.md",
        spec_text="TypeScript leaf generated consumer only.",
    )

    assert drift.status == GateStatus.revision_required
    assert drift.decision_code == "RUNTIME_BOUNDARY_DRIFT"
    assert leaf.status == GateStatus.approved


def test_gate_bypass_attempt_is_blocked():
    gate = GreenfieldGateService()

    receipt = gate.validate_prompt_stack(object_ref="workflow:extract", bypass_requested=True)

    assert receipt.status == GateStatus.blocked
    assert receipt.decision_code == "GREENFIELD_GATE_BYPASS_FORBIDDEN"


def test_provider_template_approval_requires_explicit_reviewer():
    gate = GreenfieldGateService()

    with pytest.raises(GreenfieldGateError) as exc:
        gate.approve_provider_template(
            template_key="comfyui:portrait:v1",
            content="{workflow:1}",
            compatibility_notes="ok",
            required_inputs=["source_image"],
            output_contract="ComfyWorkflowAsset",
            known_defects=[],
            evaluation_target_id=uuid4(),
            approved_by_actor_id=None,
        )

    assert exc.value.code == "TEMPLATE_REVIEWER_REQUIRED"
