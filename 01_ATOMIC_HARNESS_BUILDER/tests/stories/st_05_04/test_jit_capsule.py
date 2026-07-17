from __future__ import annotations

import dataclasses

import pytest

from cmf_builder.application.jit_capsule_commands import AssembleJITCapsuleCommand, JITCapsuleCommandService
from cmf_builder.skills.jit_capsule import ContextClass, ContextRequirement, JITCapsuleError


H = "a" * 64
P = "b" * 64


def requirement(
    context_id: str,
    classification: ContextClass = ContextClass.REQUIRED,
    *,
    condition: bool = False,
    na_reason: str | None = None,
) -> ContextRequirement:
    return ContextRequirement(
        context_id=context_id,
        context_hash=H,
        classification=classification,
        source_ref=f"authority:{context_id}@1",
        provenance_ref=f"lineage:{context_id}@1",
        owning_responsibility="activative_semantic_compilation",
        consuming_phase="compile_activative_intelligence_pack",
        inclusion_reason=f"Governed {classification.value} context.",
        authority_ref="Activative Intelligence Constitution V1.1",
        condition_satisfied=condition,
        not_applicable_reason=na_reason,
    )


def command(**changes: object) -> AssembleJITCapsuleCommand:
    requirements = (
        requirement("identity_dna"),
        requirement("audience_context"),
        requirement("optional_style", ContextClass.OPTIONAL),
        requirement("actual_human_reaction", ContextClass.NOT_APPLICABLE, na_reason="Human reaction remains external."),
        requirement("external_provider", ContextClass.FORBIDDEN),
    )
    base: dict[str, object] = {
        "command_id": "cmd-1",
        "actor_id": "analyst-1",
        "phase_id": "compile_activative_intelligence_pack",
        "skill_id": "activative_intelligence_pack_compiler",
        "skill_version": "1.0.0",
        "skill_package_hash": P,
        "minimum_context_ref": "mcc:activative:1",
        "minimum_context_hash": H,
        "requirements": requirements,
        "supplied_context_ids": ("identity_dna", "audience_context"),
        "authority_refs": ("Builder PRD V1.2", "Activative Intelligence Constitution V1.1"),
        "input_contract_ref": "ActivativeCompilerInput@1.0.0",
        "output_contract_ref": "ActivativeIntelligencePack@1.0.0",
        "acceptance_test_refs": ("evaluation:development_validated",),
        "failure_and_stop_conditions": ("missing_evidence", "authority_conflict"),
        "observability_requirements": ("artifact_identity", "failure_context", "lineage"),
        "rollback_requirements": ("zero_partial_capsules",),
        "wrong_reading_locks": ("Do not manufacture human truth.",),
        "semantic_lineage_refs": ("source-lock:1", "identity-dna:1", "audience-context:1"),
        "evaluation_status": "development_validated",
    }
    base.update(changes)
    return AssembleJITCapsuleCommand(**base)


def test_assembles_exact_minimum_phase_context_deterministically() -> None:
    first_service = JITCapsuleCommandService(authorized_actor_ids=("analyst-1",))
    second_service = JITCapsuleCommandService(authorized_actor_ids=("analyst-1",))
    first = first_service.assemble(command())
    second = second_service.assemble(command())
    assert first == second
    assert first.capsule_hash == second.capsule_hash
    assert [item.context_id for item in first.selected_context] == ["audience_context", "identity_dna"]
    assert first.production_eligible is False and first.certified is False
    assert first_service.observations[-1].outcome == "PASS"


@pytest.mark.parametrize(
    ("supplied", "match"),
    [
        (("identity_dna",), "missing"),
        (("identity_dna", "audience_context", "optional_style"), "Optional context"),
        (("identity_dna", "audience_context", "external_provider"), "Forbidden"),
        (("identity_dna", "audience_context", "unknown"), "Unjustified"),
    ],
)
def test_fails_closed_on_incomplete_or_nonminimal_context(supplied: tuple[str, ...], match: str) -> None:
    service = JITCapsuleCommandService(authorized_actor_ids=("analyst-1",))
    with pytest.raises(JITCapsuleError, match=match):
        service.assemble(command(supplied_context_ids=supplied))
    assert service.observations[-1].outcome == "FAIL"


def test_rejects_unauthorized_or_uncertified_inputs_and_machine_paths() -> None:
    service = JITCapsuleCommandService(authorized_actor_ids=("analyst-1",))
    with pytest.raises(JITCapsuleError, match="authority"):
        service.assemble(command(actor_id="intruder"))
    with pytest.raises(JITCapsuleError, match="development-validated"):
        service.assemble(command(command_id="cmd-2", evaluation_status="certified"))
    with pytest.raises(JITCapsuleError, match="absolute path"):
        service.assemble(command(command_id="cmd-3", input_contract_ref="D:/machine/contract.json"))


def test_idempotency_conflict_atomic_failure_and_invalidation() -> None:
    service = JITCapsuleCommandService(authorized_actor_ids=("analyst-1",))
    first = service.assemble(command())
    assert service.assemble(command()) is first
    with pytest.raises(JITCapsuleError, match="payload changed"):
        service.assemble(command(phase_id="different"))
    with pytest.raises(JITCapsuleError, match="Injected"):
        service.assemble(command(command_id="cmd-fail"), inject_failure=True)
    with pytest.raises(KeyError):
        service.get("jit:missing")
    service.invalidate(first.capsule_id)
    with pytest.raises(KeyError):
        service.get(first.capsule_id)


def test_changed_governed_context_changes_identity_and_hash_drift_is_detected() -> None:
    first = JITCapsuleCommandService(authorized_actor_ids=("analyst-1",)).assemble(command())
    changed_requirements = tuple(
        dataclasses.replace(item, context_hash="c" * 64) if item.context_id == "identity_dna" else item
        for item in command().requirements
    )
    second = JITCapsuleCommandService(authorized_actor_ids=("analyst-1",)).assemble(
        command(command_id="cmd-2", requirements=changed_requirements)
    )
    assert second.capsule_hash != first.capsule_hash
    with pytest.raises(JITCapsuleError, match="drifted"):
        dataclasses.replace(first, wrong_reading_locks=("weakened",)).canonical_dict()
