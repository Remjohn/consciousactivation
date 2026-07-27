from __future__ import annotations

from dataclasses import replace
from datetime import timedelta
from hashlib import sha256

import pytest

from cmf_builder.domain.atomic_harness_definition import (
    AtomicHarnessDefinition,
    AtomicHarnessDefinitionReceipt,
    DefinitionLineageInvalid,
    GovernedDefinitionSection,
)
from cmf_builder.domain.target_package_validation import (
    AtomicContentHarnessValidationReport,
    TargetValidationAuthorityInvalid,
    TargetValidationLineageInvalid,
)
from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)
from cmf_builder.domain.run import RunEvent
from tests.stories.st_01_01_synthetic_proof import NOW
from tests.stories.st_07_02 import build_context, compile_command
from tests.stories.st_07_04 import build_context as build_validation_context
from tests.stories.st_07_04 import validation_command


SEMANTIC_MUTATIONS = {
    "task_id": "forged_task",
    "goal": "forged goal",
    "success_condition": "forged success",
    "input_contract": "forged input",
    "output_contract": "forged output",
    "evaluation_requirements": ("forged_evaluation",),
    "repair_retry_policy": "forged_retry",
    "compatibility_status": "production_ready",
}


def _rehash(
    definition: AtomicHarnessDefinition, **changes: object
) -> AtomicHarnessDefinition:
    candidate = replace(
        definition,
        definition_id="pending",
        definition_hash="pending",
        **changes,
    )
    digest = sha256(candidate.canonical_bytes()).hexdigest()
    return replace(
        candidate,
        definition_id=f"atomic-harness-definition_{digest}",
        definition_hash=f"sha256:{digest}",
    )


def _governed_inputs(repository, run_id: str) -> dict[str, object]:
    run = repository.load_run(run_id)
    context = repository.get_minimum_context_graph(run.minimum_context_ref)
    assert context is not None
    values = {
        "run": run,
        "source_lock": repository.get_source_lock(run.source_lock_ref),
        "boundary": repository.get_atomic_boundary(run.atomic_boundary_ref),
        "ratification": repository.get_atomicity_ratification(
            run.atomicity_ratification_ref
        ),
        "model": repository.get_draft_harness_model(run.draft_harness_model_ref),
        "ir": repository.get_harness_ir(run.harness_ir_ref),
        "manifest": repository.get_artifact_manifest(run.artifact_manifest_ref),
        "constitutional": repository.get_constitutional_validation_report(
            run.constitutional_validation_ref
        ),
        "capability": repository.get_capability_ownership_graph(
            run.capability_ownership_ref
        ),
        "modules": repository.get_responsibility_module_graph(
            run.responsibility_module_ref
        ),
        "phases": repository.get_phase_graph(run.phase_graph_ref),
        "handoff_graph": repository.get_phase_handoff_graph(run.phase_handoff_ref),
        "accepted_handoff": repository.get_internal_handoff(
            context.accepted_handoff_id
        ),
        "handoff_decision": repository.get_internal_handoff_decision(
            context.accepted_handoff_id
        ),
        "context": context,
        "snapshot": repository.get_skill_registry_snapshot(
            run.skill_registry_snapshot_ref
        ),
        "necessity": repository.get_skill_necessity_decision(
            run.skill_necessity_ref
        ),
    }
    assert all(value is not None for value in values.values())
    return values


@pytest.fixture(scope="module")
def governed_definition():
    service, _, repository, _, run_id, _, _, _ = build_context(
        seed="BQA-P0-001"
    )
    original_receipt = service.compile(compile_command(run_id))
    definition = service.get_active(run_id)
    return repository, run_id, definition, original_receipt, _governed_inputs(
        repository, run_id
    )


@pytest.mark.parametrize("field", tuple(SEMANTIC_MUTATIONS))
def test_each_rehashed_semantic_forgery_is_rejected(
    governed_definition, field: str
) -> None:
    _, _, definition, _, inputs = governed_definition
    forged = _rehash(definition, **{field: SEMANTIC_MUTATIONS[field]})

    with pytest.raises(DefinitionLineageInvalid):
        forged.validate(**inputs)
    with pytest.raises(DefinitionLineageInvalid):
        AtomicHarnessDefinitionReceipt.create(
            command_id="forged-definition-command",
            definition=forged,
            authority_identity=forged.authority_identity,
            event_ids=("forged-event",),
            stream_version=23,
        )
    with pytest.raises(TargetValidationLineageInvalid):
        AtomicContentHarnessValidationReport.create(
            definition=forged,
            authority_identity="code-1",
        )


@pytest.mark.parametrize(
    ("section_field", "replacement"),
    (
        ("section_id", "forged_section"),
        ("applicability", "NOT_APPLICABLE"),
        ("source_refs", ("invented-local-authority",)),
        ("basis", "ungoverned"),
    ),
)
@pytest.mark.parametrize("section_index", range(20))
def test_every_section_projection_is_authority_bound(
    governed_definition,
    section_index: int,
    section_field: str,
    replacement: object,
) -> None:
    _, _, definition, _, inputs = governed_definition
    sections = list(definition.sections)
    section = sections[section_index]
    sections[section_index] = replace(section, **{section_field: replacement})
    forged = _rehash(definition, sections=tuple(sections))

    with pytest.raises(DefinitionLineageInvalid):
        forged.validate(**inputs)


def test_complete_forgery_cannot_be_receipted_or_reported(governed_definition) -> None:
    _, _, definition, _, inputs = governed_definition
    sections = list(definition.sections)
    sections[0] = GovernedDefinitionSection(
        section_id=sections[0].section_id,
        applicability=sections[0].applicability,
        source_refs=("invented-local-authority",),
        basis="ungoverned",
    )
    forged = _rehash(
        definition,
        **SEMANTIC_MUTATIONS,
        authority_identity="unratified-actor",
        sections=tuple(sections),
    )

    with pytest.raises(DefinitionLineageInvalid):
        forged.validate(**inputs)
    with pytest.raises(DefinitionLineageInvalid):
        AtomicHarnessDefinitionReceipt.create(
            command_id="forged-command",
            definition=forged,
            authority_identity="unratified-actor",
            event_ids=("forged-event",),
            stream_version=23,
        )
    with pytest.raises(TargetValidationLineageInvalid):
        AtomicContentHarnessValidationReport.create(
            definition=forged,
            authority_identity="code-1",
        )


def test_untouched_governed_definition_identity_is_preserved(governed_definition) -> None:
    _, _, definition, original_receipt, inputs = governed_definition
    definition.validate(**inputs)
    reproduced = AtomicHarnessDefinition.create(
        **inputs,
        authority_identity=definition.authority_identity,
    )
    assert reproduced.canonical_bytes() == definition.canonical_bytes()
    assert reproduced.definition_id == definition.definition_id
    assert original_receipt.definition_id == definition.definition_id


@pytest.mark.parametrize("compiler_actor", ("unknown-compiler", "architect-1", "stale-code"))
def test_target_command_rejects_unknown_wrong_kind_and_stale_compiler_authority(
    compiler_actor: str,
) -> None:
    service, _, _, repository, _, run_id, _, definition = build_validation_context(
        seed=f"BQA-P0-authority-{compiler_actor}"
    )
    forged = _rehash(definition, authority_identity=compiler_actor)
    old_event = repository.events(run_id)[-1]
    payload = dict(old_event.payload)
    payload["definition_ref"] = forged.definition_id
    payload["definition_hash"] = forged.definition_hash
    forged_event = RunEvent.create(
        event_id=old_event.event_id,
        event_type=old_event.event_type,
        run_id=old_event.run_id,
        stream_version=old_event.stream_version,
        command_id=old_event.command_id,
        actor_id=compiler_actor,
        timestamp=old_event.timestamp,
        correlation_id=old_event.correlation_id,
        causation_id=old_event.causation_id,
        payload=payload,
    )
    forged_receipt = AtomicHarnessDefinitionReceipt.create(
        command_id=old_event.command_id,
        definition=forged,
        authority_identity=compiler_actor,
        event_ids=(old_event.event_id,),
        stream_version=old_event.stream_version,
    )
    old_definition_id = definition.definition_id
    repository._streams[run_id] = (
        *repository.events(run_id)[:-1],
        forged_event,
    )
    del repository._atomic_harness_definitions[old_definition_id]
    repository._atomic_harness_definitions[forged.definition_id] = forged
    repository._run_atomic_harness_definitions[run_id] = (forged.definition_id,)
    repository._atomic_harness_definition_receipts.clear()
    repository._atomic_harness_definition_receipts[
        forged_receipt.receipt_id
    ] = forged_receipt
    repository._run_atomic_harness_definition_receipts[run_id] = (
        forged_receipt.receipt_id,
    )
    if compiler_actor == "stale-code":
        service._authority = AuthorityService(
            actors=(
                Actor("code-1", ActorKind.CODE),
                Actor("stale-code", ActorKind.CODE),
            ),
            grants=(
                AuthorityGrant(
                    actor_id="code-1",
                    actions=frozenset(Action),
                    resource_id="*",
                    expires_at=NOW + timedelta(days=1),
                ),
                AuthorityGrant(
                    actor_id="stale-code",
                    actions=frozenset(Action),
                    resource_id="*",
                    expires_at=NOW - timedelta(seconds=1),
                ),
            ),
        )
    before = repository.event_count(run_id)
    command = validation_command(run_id)

    with pytest.raises(TargetValidationAuthorityInvalid):
        service.validate(command)

    assert repository.event_count(run_id) == before
    assert repository.atomic_content_harness_validation_reports(run_id) == ()
    assert repository.atomic_content_harness_validation_receipts(run_id) == ()
    assert repository.get_command_record(command.command_id) is None
    assert repository.pending_observations(command.command_id) == ()
