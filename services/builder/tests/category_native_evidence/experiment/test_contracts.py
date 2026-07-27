from __future__ import annotations

import pytest

from cmf_builder.category_evidence.experiment_contracts import (
    ARCHIVE_SHA256,
    CaseState,
    CaseTemplate,
    CorpusMemberBinding,
    EvidenceGateError,
    ExperimentArm,
    ProviderTrialAuthority,
    build_trial_requests,
    governed_case_templates,
    template_arm_identity,
)


H = "a" * 64


def template(*, activative: bool = True) -> CaseTemplate:
    return CaseTemplate(
        case_id="BD007-CASE-SHORT-FORM-EDITED-VIDEO",
        category="short_form_edited_video",
        profile="short_form_governed_profile_pending_member",
        activative_applicable=activative,
        required_dimensions=("category_native_syntax", "wrong_reading_resistance"),
        semantic_field_names=("identity_dna_ref", "audience_context_ref", "activative_call_ref"),
        native_structure=("shot", "cut", "temporal_beat", "reading_order"),
        flattened_structure=("generic_section", "generic_item"),
        output_contract_fields=("semantic_lineage", "wrong_reading_locks", "projection"),
        source_member_role="edited_video_syntax_and_sequence_evidence",
    )


def member() -> CorpusMemberBinding:
    return CorpusMemberBinding(
        archive_sha256=ARCHIVE_SHA256,
        admitted_manifest_sha256=H,
        admission_receipt_sha256=H,
        member_path="VISUAL SYNTAX BUILDER/Content Formats/example.json",
        member_sha256=H,
        usage_authority_receipt_sha256=H,
        provenance_status="LIMITED_BUT_ADMITTED_FOR_DEVELOPMENT_ONLY",
    )


def executable_case():
    return template().bind(
        member=member(),
        governed_semantic_input_sha256=H,
        wrong_reading_lock_sha256s=(H,),
        authority_chain_sha256=H,
        lineage_sha256=H,
    )


def test_template_is_explicitly_non_executable_until_corpus_binding() -> None:
    case = template()
    assert case.state is CaseState.PENDING_CORPUS_ADMISSION
    assert len(case.template_identity) == 64
    with pytest.raises(EvidenceGateError, match="wrong-reading locks"):
        case.bind(
            member=member(),
            governed_semantic_input_sha256=H,
            wrong_reading_lock_sha256s=(),
            authority_chain_sha256=H,
            lineage_sha256=H,
        )


def test_member_must_belong_to_exact_campaign_archive() -> None:
    with pytest.raises(EvidenceGateError, match="outside this campaign"):
        CorpusMemberBinding(
            archive_sha256="b" * 64,
            admitted_manifest_sha256=H,
            admission_receipt_sha256=H,
            member_path="evidence.json",
            member_sha256=H,
            usage_authority_receipt_sha256=H,
            provenance_status="LIMITED",
        )


def test_paired_arms_change_structure_only() -> None:
    case = executable_case()
    native = case.arm_payload(ExperimentArm.NATIVE)
    flattened = case.arm_payload(ExperimentArm.FLATTENED)
    changed = {key for key in native if native[key] != flattened[key]}
    assert changed == {"arm", "structure"}
    assert native["governed_semantic_input_sha256"] == flattened["governed_semantic_input_sha256"]


def test_trial_requests_require_separate_authority_and_three_repeats() -> None:
    case = executable_case()
    denied = ProviderTrialAuthority(H, H, False, 6, H)
    with pytest.raises(EvidenceGateError, match="not governed"):
        build_trial_requests(
            case, denied, repeats=3, execution_budget={"tokens": 1}, deterministic_controls={"seed": 7}
        )
    allowed = ProviderTrialAuthority(H, H, True, 6, H)
    with pytest.raises(EvidenceGateError, match="at least three"):
        build_trial_requests(
            case, allowed, repeats=2, execution_budget={"tokens": 1}, deterministic_controls={"seed": 7}
        )
    requests = build_trial_requests(
        case, allowed, repeats=3, execution_budget={"tokens": 1}, deterministic_controls={"seed": 7}
    )
    assert len(requests) == 6
    assert {request.arm for request in requests} == set(ExperimentArm)
    assert len({request.execution_budget_sha256 for request in requests}) == 1
    assert len({request.deterministic_controls_sha256 for request in requests}) == 1


def test_identical_inputs_produce_identical_request_identities() -> None:
    authority = ProviderTrialAuthority(H, H, True, 6, H)
    args = dict(repeats=3, execution_budget={"tokens": 100}, deterministic_controls={"seed": 0})
    first = build_trial_requests(executable_case(), authority, **args)
    second = build_trial_requests(executable_case(), authority, **args)
    assert [item.request_identity for item in first] == [item.request_identity for item in second]


def test_governed_template_families_cover_campaign_scope_without_becoming_cases() -> None:
    templates = governed_case_templates()
    assert len(templates) == 4
    assert {item.category for item in templates} == {
        "short_form_edited_video",
        "2d_character_animation",
        "conversational_activation_expression",
        "NOT_APPLICABLE",
    }
    assert all(item.state is CaseState.PENDING_CORPUS_ADMISSION for item in templates)
    assert all(
        template_arm_identity(item, ExperimentArm.NATIVE)
        != template_arm_identity(item, ExperimentArm.FLATTENED)
        for item in templates
    )
