from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import hashlib

import pytest

from cmf_builder.evaluation.root_cause_diagnosis import DiagnosticLayer, RepairField
from cmf_builder.evaluation.selective_repair import (
    AcceptedDiagnosis,
    ImmutableRepairSubject,
    RepairAction,
    RepairAuthority,
    RepairAuthorityStatus,
    RepairFieldChange,
    RepairOwnerKind,
    RepairCommand,
    SelectiveRepairError,
    accept_root_cause_diagnosis,
    canonical_json_bytes,
    compile_selective_repair_candidate,
    compute_accept_payload_sha256,
    compute_candidate_payload_sha256,
)
from tests.stories.st_08_04.test_layer_localization_and_graph import (
    localized_diagnosis,
    unresolved_diagnosis,
    valid_graph,
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def authority(*actions: RepairAction) -> RepairAuthority:
    return RepairAuthority(
        authority_id="od-am-001-st-08.05-development-authority",
        authority_version="1.0.0-development",
        authority_sha256=digest("st-08.05-authority-bytes"),
        permitted_actions=actions
        or (
            RepairAction.ACCEPT_DIAGNOSIS,
            RepairAction.COMPILE_CANDIDATE,
        ),
        status=RepairAuthorityStatus.ACTIVE,
    )


def command(
    *,
    action: RepairAction,
    resource_id: str,
    payload_sha256: str,
    governed_authority: RepairAuthority,
    command_id: str,
) -> RepairCommand:
    return RepairCommand(
        command_id=command_id,
        action=action,
        resource_id=resource_id,
        payload_sha256=payload_sha256,
        expected_authority_identity=governed_authority.authority_identity,
    )


def accepted_diagnosis(
    *,
    diagnosis=None,
    graph=None,
    governed_authority: RepairAuthority | None = None,
) -> AcceptedDiagnosis:
    governed_diagnosis = diagnosis or localized_diagnosis(DiagnosticLayer.SEMANTIC)
    governed_graph = graph or valid_graph(governed_diagnosis)
    governed_authority = governed_authority or authority()
    payload_sha256 = compute_accept_payload_sha256(
        diagnosis=governed_diagnosis,
        graph=governed_graph,
    )
    return accept_root_cause_diagnosis(
        diagnosis=governed_diagnosis,
        graph=governed_graph,
        command=command(
            action=RepairAction.ACCEPT_DIAGNOSIS,
            resource_id=governed_diagnosis.diagnosis_identity,
            payload_sha256=payload_sha256,
            governed_authority=governed_authority,
            command_id="accept-root-cause-diagnosis-v1",
        ),
        authority=governed_authority,
    )


def parent_subject(**changes: object) -> ImmutableRepairSubject:
    values: dict[str, object] = {
        "subject_id": "semantic-projection",
        "subject_version": "1.0.0-development",
        "subject_sha256": digest("semantic-projection-v1-bytes"),
        "active": True,
        "superseded": False,
        "invalidated": False,
    }
    values.update(changes)
    return ImmutableRepairSubject(**values)  # type: ignore[arg-type]


def candidate_inputs(
    *,
    accepted: AcceptedDiagnosis | None = None,
    graph=None,
    parent: ImmutableRepairSubject | None = None,
    owner_kind: RepairOwnerKind = RepairOwnerKind.BUILDER_OWNED_PHASE,
    responsible_unit: str = "builder.semantic.responsible-unit",
    field_changes: tuple[RepairFieldChange, ...] | None = None,
    preserved_state: tuple[str, ...] | None = None,
) -> dict[str, object]:
    governed_graph = graph or valid_graph()
    governed_accepted = accepted or accepted_diagnosis(graph=governed_graph)
    governed_parent = parent or parent_subject()
    return {
        "accepted_diagnosis": governed_accepted,
        "graph": governed_graph,
        "owner_kind": owner_kind,
        "responsible_unit": responsible_unit,
        "parent_subject": governed_parent,
        "candidate_version": "1.0.1-development",
        "field_changes": field_changes
        if field_changes is not None
        else (
            RepairFieldChange(
                layer=DiagnosticLayer.SEMANTIC,
                field_name="semantic_governed_projection",
                prior_value_sha256=digest("semantic-field-before"),
                proposed_value_sha256=digest("semantic-field-after"),
            ),
        ),
        "preserved_state": preserved_state
        or governed_graph.frozen_upstream_and_unaffected_state,
    }


def compile_candidate(**changes: object):
    inputs = candidate_inputs(**changes)
    governed_authority = authority()
    payload_sha256 = compute_candidate_payload_sha256(**inputs)
    return compile_selective_repair_candidate(
        **inputs,
        command=command(
            action=RepairAction.COMPILE_CANDIDATE,
            resource_id=inputs["parent_subject"].subject_identity,  # type: ignore[union-attr]
            payload_sha256=payload_sha256,
            governed_authority=governed_authority,
            command_id="compile-selective-repair-candidate-v1",
        ),
        authority=governed_authority,
    )


def test_acceptance_gate_binds_every_required_st_08_04_diagnosis_and_graph_field() -> None:
    diagnosis = localized_diagnosis(DiagnosticLayer.SEMANTIC)
    graph = valid_graph(diagnosis)

    accepted = accepted_diagnosis(diagnosis=diagnosis, graph=graph)
    payload = accepted.as_dict()

    assert accepted.status == "ACCEPTED_ROOT_CAUSE"
    assert accepted.diagnosis_identity == diagnosis.diagnosis_identity
    assert accepted.diagnosis_version == diagnosis.diagnosis_version
    assert accepted.graph_identity == graph.graph_identity
    assert accepted.failure_id == diagnosis.classification.failure_id
    assert accepted.stable_failure_code == diagnosis.classification.stable_code
    assert accepted.selected_root_cause == diagnosis.selected_root_cause
    assert accepted.confidence_basis == diagnosis.confidence_basis
    assert accepted.smallest_responsible_layer is DiagnosticLayer.SEMANTIC
    assert accepted.responsible_owner == diagnosis.responsible_owner
    assert accepted.responsible_authority_ref == diagnosis.responsible_authority_ref
    assert accepted.permitted_repair_fields == graph.permitted_repair_fields
    assert accepted.frozen_state == graph.frozen_upstream_and_unaffected_state
    assert accepted.affected_descendants == graph.invalidated_descendant_set
    assert accepted.targeted_regression_requirements == graph.targeted_regression_suite
    assert accepted.rollback_conditions == graph.rollback_requirements
    assert accepted.escalation_conditions == graph.escalation_conditions
    assert payload["status"] == "ACCEPTED_ROOT_CAUSE"
    assert payload["repair_executed"] is False


def test_unresolved_ambiguous_or_mismatched_diagnosis_cannot_cross_acceptance_gate() -> None:
    unresolved = unresolved_diagnosis()
    localized_graph = valid_graph(localized_diagnosis(DiagnosticLayer.SEMANTIC))

    with pytest.raises(SelectiveRepairError) as caught:
        accepted_diagnosis(diagnosis=unresolved, graph=localized_graph)
    assert caught.value.code == "DIAGNOSIS_NOT_ACCEPTABLE"

    diagnosis = localized_diagnosis(DiagnosticLayer.SEMANTIC)
    other_graph = valid_graph(localized_diagnosis(DiagnosticLayer.CONTEXT))
    with pytest.raises(SelectiveRepairError) as caught:
        accepted_diagnosis(diagnosis=diagnosis, graph=other_graph)
    assert caught.value.code == "DIAGNOSIS_GRAPH_MISMATCH"


def test_acceptance_gate_detects_post_construction_diagnosis_or_graph_tampering() -> None:
    diagnosis = localized_diagnosis(DiagnosticLayer.SEMANTIC)
    graph = valid_graph(diagnosis)
    object.__setattr__(diagnosis, "selected_root_cause", "forged root cause")

    with pytest.raises(SelectiveRepairError) as caught:
        accepted_diagnosis(diagnosis=diagnosis, graph=graph)
    assert caught.value.code in {"ALTERED_DIAGNOSIS", "INVALID_DIAGNOSIS"}


@pytest.mark.parametrize(
    "owner_kind",
    (
        RepairOwnerKind.BUILDER_OWNED_PHASE,
        RepairOwnerKind.BUILDER_OWNED_CAPABILITY,
        RepairOwnerKind.BUILDER_OWNED_CONTRACT_PROJECTION,
    ),
)
def test_candidate_has_exactly_one_capsule_permitted_builder_owned_primary_unit(
    owner_kind: RepairOwnerKind,
) -> None:
    candidate = compile_candidate(owner_kind=owner_kind)

    assert candidate.owner_kind is owner_kind
    assert candidate.responsible_unit == "builder.semantic.responsible-unit"
    assert candidate.primary_responsible_units == (
        "builder.semantic.responsible-unit",
    )
    assert candidate.external_product_unit is None
    assert candidate.whole_run_regenerated is False


def test_external_product_or_multiple_primary_repair_units_are_prohibited() -> None:
    with pytest.raises(SelectiveRepairError) as caught:
        compile_candidate(owner_kind="external_product")  # type: ignore[arg-type]
    assert caught.value.code == "EXTERNAL_PRODUCT_REPAIR_PROHIBITED"

    inputs = candidate_inputs()
    inputs["responsible_unit"] = (
        "builder.semantic.responsible-unit",
        "builder.context.responsible-unit",
    )
    governed_authority = authority()
    with pytest.raises(SelectiveRepairError) as caught:
        compile_selective_repair_candidate(
            **inputs,
            command=command(
                action=RepairAction.COMPILE_CANDIDATE,
                resource_id=inputs["parent_subject"].subject_identity,  # type: ignore[union-attr]
                payload_sha256=digest("multiple-owner-payload"),
                governed_authority=governed_authority,
                command_id="prohibited-multiple-owner-repair",
            ),
            authority=governed_authority,
        )
    assert caught.value.code in {
        "EXACTLY_ONE_RESPONSIBLE_UNIT_REQUIRED",
        "INVALID_RESPONSIBLE_UNIT",
    }


def test_field_changes_must_be_a_nonempty_subset_of_diagnosed_permitted_scope() -> None:
    candidate = compile_candidate()
    assert candidate.field_changes == (
        RepairFieldChange(
            layer=DiagnosticLayer.SEMANTIC,
            field_name="semantic_governed_projection",
            prior_value_sha256=digest("semantic-field-before"),
            proposed_value_sha256=digest("semantic-field-after"),
        ),
    )

    for invalid_changes in (
        (),
        (
            RepairFieldChange(
                layer=DiagnosticLayer.CONTEXT,
                field_name="minimum_complete_context",
                prior_value_sha256=digest("context-before"),
                proposed_value_sha256=digest("context-after"),
            ),
        ),
        (
            RepairFieldChange(
                layer=DiagnosticLayer.SEMANTIC,
                field_name="unapproved_semantic_field",
                prior_value_sha256=digest("unapproved-before"),
                proposed_value_sha256=digest("unapproved-after"),
            ),
        ),
    ):
        with pytest.raises(SelectiveRepairError) as caught:
            compile_candidate(field_changes=invalid_changes)
        assert caught.value.code in {
            "MISSING_REPAIR_FIELD_CHANGE",
            "REPAIR_FIELD_OUTSIDE_DIAGNOSED_SCOPE",
        }


def test_candidate_is_a_new_immutable_child_and_does_not_mutate_parent_history() -> None:
    parent = parent_subject()
    parent_bytes = canonical_json_bytes(parent.as_dict())

    candidate = compile_candidate(parent=parent)

    assert candidate.parent_subject_identity == parent.subject_identity
    assert candidate.parent_subject_version == parent.subject_version
    assert candidate.parent_subject_sha256 == parent.subject_sha256
    assert candidate.candidate_version != parent.subject_version
    assert candidate.candidate_identity != parent.subject_identity
    assert canonical_json_bytes(parent.as_dict()) == parent_bytes
    assert candidate.prior_bytes_mutated is False
    assert candidate.historical_state_deleted is False
    with pytest.raises(FrozenInstanceError):
        candidate.candidate_version = "rewritten"  # type: ignore[misc]


@pytest.mark.parametrize(
    "parent",
    (
        parent_subject(active=False),
        parent_subject(superseded=True),
        parent_subject(invalidated=True),
    ),
)
def test_inactive_stale_or_invalidated_parent_version_fails_closed(
    parent: ImmutableRepairSubject,
) -> None:
    with pytest.raises(SelectiveRepairError) as caught:
        compile_candidate(parent=parent)
    assert caught.value.code == "INACTIVE_PARENT_VERSION"


def test_candidate_preserves_exact_frozen_upstream_and_unaffected_state() -> None:
    graph = valid_graph()
    candidate = compile_candidate(graph=graph)

    assert candidate.preserved_state == graph.frozen_upstream_and_unaffected_state
    assert not set(candidate.preserved_state).intersection(candidate.affected_descendants)

    with pytest.raises(SelectiveRepairError) as caught:
        compile_candidate(
            graph=graph,
            preserved_state=(graph.frozen_upstream_and_unaffected_state[0],),
        )
    assert caught.value.code == "PRESERVED_STATE_MISMATCH"


def test_repair_cannot_target_only_the_observed_symptom_or_rewrite_upstream_truth() -> None:
    graph = valid_graph()
    symptom_field = RepairFieldChange(
        layer=DiagnosticLayer.SEMANTIC,
        field_name=graph.root_cause_diagnosis_ref,
        prior_value_sha256=digest("symptom-before"),
        proposed_value_sha256=digest("symptom-after"),
    )
    with pytest.raises(SelectiveRepairError) as caught:
        compile_candidate(graph=graph, field_changes=(symptom_field,))
    assert caught.value.code == "REPAIR_FIELD_OUTSIDE_DIAGNOSED_SCOPE"

    upstream_field = RepairFieldChange(
        layer=DiagnosticLayer.SEMANTIC,
        field_name="source_lock",
        prior_value_sha256=digest("source-lock-before"),
        proposed_value_sha256=digest("source-lock-after"),
    )
    with pytest.raises(SelectiveRepairError) as caught:
        compile_candidate(graph=graph, field_changes=(upstream_field,))
    assert caught.value.code == "REPAIR_FIELD_OUTSIDE_DIAGNOSED_SCOPE"


def test_acceptance_and_candidate_records_are_deterministic_and_development_only() -> None:
    first = compile_candidate()
    second = compile_candidate()

    assert first.candidate_identity == second.candidate_identity
    assert canonical_json_bytes(first.as_dict()) == canonical_json_bytes(second.as_dict())
    assert first.as_dict()["external_runtime_executed"] is False
    assert first.as_dict()["production_ready"] is False
    assert first.as_dict()["certified"] is False
