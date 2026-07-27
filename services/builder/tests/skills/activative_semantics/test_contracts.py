from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace
from hashlib import sha256
import json

import pytest

from cmf_builder.skills.activative_contracts import (
    ActivativeCompilerInput,
    ActivativeContractError,
    ActivativeIntelligencePack,
    Applicability,
    ApplicabilityReason,
    DOWNSTREAM_ARTIFACT_ORDER,
    DownstreamApplicabilityDecision,
    DownstreamArtifact,
    EXPECTED_DOWNSTREAM_OWNERS,
    SEMANTIC_FIELD_PATHS,
    SemanticFieldLineage,
)


SOURCE_REF = "evidence://source-lock/activative-example-v1"
AUTHORITY_REF = "authority://activative-example/ratification-v1"
IDENTITY_REF = "identity-dna://activative-example/v1"
AUDIENCE_REF = "audience-context-premise://activative-example/v1"
LIVE_PREMISE_REF = "live-premise://activative-example/v1"
RESONANCE_REF = "resonance-map://activative-example/v1"
EDGING_REF = "matrix-of-edging://activative-example/v1"


def _hash(label: str) -> str:
    return f"sha256:{sha256(label.encode('utf-8')).hexdigest()}"


def _decisions() -> tuple[DownstreamApplicabilityDecision, ...]:
    reason_codes = {
        DownstreamArtifact.REACTION_RECEIPT: (
            ApplicabilityReason.NO_GOVERNED_HUMAN_REACTION_EXISTS
        ),
        DownstreamArtifact.EXPRESSION_MOMENT: (
            ApplicabilityReason.NO_GOVERNED_SOURCE_EXPRESSION_EXISTS
        ),
        DownstreamArtifact.VISUAL_SEMANTIC_PACK: (
            ApplicabilityReason.NON_VISUAL_FORMAT_GOAL
        ),
        DownstreamArtifact.VISUAL_NARRATIVE_PROGRAM: (
            ApplicabilityReason.NON_VISUAL_FORMAT_GOAL
        ),
        DownstreamArtifact.FEATURE_CONTRACTS: (
            ApplicabilityReason.NON_VISUAL_FORMAT_GOAL
        ),
        DownstreamArtifact.TV_ROUTE: ApplicabilityReason.NON_VISUAL_FORMAT_GOAL,
        DownstreamArtifact.COMPOSITION_INTENT: (
            ApplicabilityReason.NON_VISUAL_FORMAT_GOAL
        ),
    }
    return tuple(
        DownstreamApplicabilityDecision(
            artifact=artifact,
            applicability=Applicability.NOT_APPLICABLE,
            reason_code=reason_codes[artifact],
            reason=f"{artifact.value} is outside this non-visual fixture.",
            authority_owner=EXPECTED_DOWNSTREAM_OWNERS[artifact],
            evidence_refs=(f"evidence://applicability/{artifact.value}/v1",),
        )
        for artifact in DOWNSTREAM_ARTIFACT_ORDER
    )


def _lineage(
    decisions: tuple[DownstreamApplicabilityDecision, ...],
) -> tuple[SemanticFieldLineage, ...]:
    exact_sources = {
        "source_refs": SOURCE_REF,
        "authority_refs": AUTHORITY_REF,
        "identity_dna_ref": IDENTITY_REF,
        "audience_context_premise_ref": AUDIENCE_REF,
        "live_premise_evidence_refs": LIVE_PREMISE_REF,
        "resonance_map_ref": RESONANCE_REF,
        "matrix_of_edging_ref": EDGING_REF,
    }
    by_artifact = {decision.artifact.value: decision for decision in decisions}
    records = []
    for field_path in SEMANTIC_FIELD_PATHS:
        if field_path.startswith("downstream_applicability."):
            artifact = field_path.split(".", maxsplit=1)[1]
            source_ref = by_artifact[artifact].evidence_refs[0]
        else:
            source_ref = exact_sources.get(field_path, SOURCE_REF)
        records.append(
            SemanticFieldLineage(
                field_path=field_path,
                source_ref=source_ref,
                source_hash=_hash(f"lineage:{field_path}:{source_ref}"),
                authority_ref=AUTHORITY_REF,
                evidence_refs=(source_ref,),
            )
        )
    return tuple(records)


def make_input(**overrides: object) -> ActivativeCompilerInput:
    decisions = _decisions()
    values: dict[str, object] = {
        "source_refs": (SOURCE_REF,),
        "authority_refs": (AUTHORITY_REF,),
        "identity_dna_ref": IDENTITY_REF,
        "audience_context_premise_ref": AUDIENCE_REF,
        "live_premise_evidence_refs": (LIVE_PREMISE_REF,),
        "resonance_map_ref": RESONANCE_REF,
        "matrix_of_edging_ref": EDGING_REF,
        "edge_pressure": "Prefer explicit governed evidence over fluent invention.",
        "format_goal": "A bounded, non-visual semantic activation package.",
        "desired_roles": ("evidence-conscious operator",),
        "activative_call_constraints": (
            "Invite one reversible evidence-checking action.",
        ),
        "desired_reaction": "The operator notices and verifies one assumption.",
        "micro_commitment": "Inspect the cited evidence before continuing.",
        "wrong_reading_locks": (
            "Do not portray desired reaction as observed human reaction.",
        ),
        "downstream_applicability": decisions,
        "lineage": _lineage(decisions),
    }
    values.update(overrides)
    return ActivativeCompilerInput.create(**values)  # type: ignore[arg-type]


def _error_code(error: pytest.ExceptionInfo[ActivativeContractError]) -> str:
    return error.value.code


def test_valid_contract_preserves_every_semantic_field_and_lineage() -> None:
    compiler_input = make_input()
    pack = ActivativeIntelligencePack.compile(compiler_input)

    compiler_input.validate()
    pack.validate(compiler_input)
    assert tuple(item.field_path for item in pack.lineage) == SEMANTIC_FIELD_PATHS
    assert tuple(item.artifact for item in pack.downstream_applicability) == (
        DOWNSTREAM_ARTIFACT_ORDER
    )
    assert pack.identity_dna_ref == IDENTITY_REF
    assert pack.audience_context_premise_ref == AUDIENCE_REF
    assert pack.desired_roles == ("evidence-conscious operator",)
    assert pack.desired_reaction_status == "intended_not_observed"
    assert pack.issued_receipt_kinds == ()
    assert pack.human_truth_generated is False
    assert pack.human_reaction_generated is False
    assert pack.external_provider_executed is False
    assert pack.production_eligible is False
    assert pack.certified is False


def test_input_exposes_the_frozen_package_field_vocabulary() -> None:
    public_names = {field.name for field in fields(ActivativeCompilerInput)}
    assert {
        "source_refs",
        "authority_refs",
        "identity_dna_ref",
        "audience_context_premise_ref",
        "live_premise_evidence_refs",
        "resonance_map_ref",
        "matrix_of_edging_ref",
        "edge_pressure",
        "format_goal",
        "desired_roles",
        "activative_call_constraints",
        "desired_reaction",
        "micro_commitment",
        "wrong_reading_locks",
        "downstream_applicability",
    } <= public_names


def test_models_are_immutable() -> None:
    compiler_input = make_input()
    pack = ActivativeIntelligencePack.compile(compiler_input)

    with pytest.raises(FrozenInstanceError):
        compiler_input.edge_pressure = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        pack.desired_reaction = "changed"  # type: ignore[misc]


def test_canonical_serialization_and_hashing_are_deterministic() -> None:
    first_input = make_input()
    second_input = make_input()
    first_pack = ActivativeIntelligencePack.compile(first_input)
    second_pack = ActivativeIntelligencePack.compile(second_input)

    assert first_input == second_input
    assert first_input.canonical_bytes() == second_input.canonical_bytes()
    assert first_pack == second_pack
    assert first_pack.canonical_bytes() == second_pack.canonical_bytes()
    assert first_pack.canonical_bytes().endswith(b"\n")
    decoded = json.loads(first_pack.canonical_bytes())
    assert decoded["source_refs"] == [SOURCE_REF]
    assert b"D:\\" not in first_pack.canonical_bytes()


def test_changed_governed_semantics_produce_new_identities() -> None:
    first_input = make_input()
    second_input = make_input(
        edge_pressure="Prefer provenance over an attractive unsupported shortcut."
    )
    first_pack = ActivativeIntelligencePack.compile(first_input)
    second_pack = ActivativeIntelligencePack.compile(second_input)

    assert first_input.input_id != second_input.input_id
    assert first_pack.pack_id != second_pack.pack_id


def test_missing_lineage_evidence_fails_closed() -> None:
    valid = make_input()
    damaged_lineage = list(valid.lineage)
    damaged_lineage[0] = replace(damaged_lineage[0], evidence_refs=())
    damaged = replace(valid, lineage=tuple(damaged_lineage))

    with pytest.raises(ActivativeContractError) as error:
        damaged.validate()
    assert _error_code(error) == "MISSING_EVIDENCE"


def test_contradictory_authority_fails_closed() -> None:
    valid = make_input()
    damaged_lineage = list(valid.lineage)
    damaged_lineage[0] = replace(
        damaged_lineage[0], authority_ref="authority://unratified/v1"
    )
    damaged = replace(valid, lineage=tuple(damaged_lineage))

    with pytest.raises(ActivativeContractError) as error:
        damaged.validate()
    assert _error_code(error) == "AUTHORITY_CONFLICT"


def test_semantic_flattening_into_notes_fails_closed() -> None:
    valid = make_input()
    flattened = list(valid.lineage)
    flattened[4] = replace(flattened[4], field_path="notes")

    with pytest.raises(ActivativeContractError) as error:
        replace(valid, lineage=tuple(flattened)).validate()
    assert _error_code(error) == "SEMANTIC_FLATTENING"


@pytest.mark.parametrize(
    ("field_path", "replacement_ref", "expected_code"),
    (
        ("identity_dna_ref", SOURCE_REF, "IDENTITY_DRIFT"),
        ("audience_context_premise_ref", SOURCE_REF, "AUDIENCE_CONTEXT_DRIFT"),
    ),
)
def test_identity_and_audience_lineage_drift_fails_closed(
    field_path: str, replacement_ref: str, expected_code: str
) -> None:
    valid = make_input()
    damaged = tuple(
        replace(item, source_ref=replacement_ref)
        if item.field_path == field_path
        else item
        for item in valid.lineage
    )

    with pytest.raises(ActivativeContractError) as error:
        replace(valid, lineage=damaged).validate()
    assert _error_code(error) == expected_code


def test_wrong_reading_locks_are_required() -> None:
    valid = make_input()
    with pytest.raises(ActivativeContractError) as error:
        replace(valid, wrong_reading_locks=()).validate()
    assert _error_code(error) == "WRONG_READING_LOCKS_REQUIRED"


def test_every_downstream_artifact_has_explicit_not_applicable_evidence() -> None:
    compiler_input = make_input()
    assert len(compiler_input.downstream_applicability) == 7
    for decision in compiler_input.downstream_applicability:
        assert decision.applicability is Applicability.NOT_APPLICABLE
        assert decision.reason
        assert decision.evidence_refs
        assert decision.authority_owner == EXPECTED_DOWNSTREAM_OWNERS[
            decision.artifact
        ]


def test_unjustified_not_applicable_reason_fails_closed() -> None:
    valid = make_input()
    decisions = list(valid.downstream_applicability)
    decisions[0] = replace(
        decisions[0], reason_code=ApplicabilityReason.NON_VISUAL_FORMAT_GOAL
    )

    with pytest.raises(ActivativeContractError) as error:
        replace(valid, downstream_applicability=tuple(decisions)).validate()
    assert _error_code(error) == "UNJUSTIFIED_APPLICABILITY"


def test_not_applicable_cannot_hide_an_existing_human_artifact() -> None:
    valid = make_input()
    decisions = list(valid.downstream_applicability)
    decisions[0] = replace(
        decisions[0], existing_artifact_refs=("reaction-receipt://rr-1",)
    )

    with pytest.raises(ActivativeContractError) as error:
        replace(valid, downstream_applicability=tuple(decisions)).validate()
    assert _error_code(error) == "UNJUSTIFIED_APPLICABILITY"


@pytest.mark.parametrize(
    "operation",
    (
        "manufacture_human_truth",
        "manufacture_human_reaction",
        "issue_reaction_receipt",
        "issue_expression_moment",
        "approve_identity_dna_amendment",
    ),
)
def test_human_owned_operations_are_forbidden(operation: str) -> None:
    valid = make_input()
    with pytest.raises(ActivativeContractError) as error:
        replace(valid, requested_operations=(operation,)).validate()
    assert _error_code(error) == "HUMAN_TRUTH_BOUNDARY_VIOLATION"


def test_provider_execution_is_forbidden() -> None:
    valid = make_input()
    with pytest.raises(ActivativeContractError) as error:
        replace(valid, external_provider_execution_requested=True).validate()
    assert _error_code(error) == "EXTERNAL_PROVIDER_EXECUTION_FORBIDDEN"


@pytest.mark.parametrize(
    "field_name", ("production_eligible_requested", "certification_requested")
)
def test_production_and_certification_claims_are_forbidden(
    field_name: str,
) -> None:
    valid = make_input()
    with pytest.raises(ActivativeContractError) as error:
        replace(valid, **{field_name: True}).validate()
    assert _error_code(error) == "PRODUCTION_CLAIM_FORBIDDEN"


def test_compiled_pack_cannot_issue_human_owned_receipts() -> None:
    compiler_input = make_input()
    pack = ActivativeIntelligencePack.compile(compiler_input)

    with pytest.raises(ActivativeContractError) as error:
        replace(pack, issued_receipt_kinds=("ReactionReceipt",)).validate(
            compiler_input
        )
    assert _error_code(error) == "HUMAN_TRUTH_BOUNDARY_VIOLATION"


def test_compiled_pack_detects_identity_and_semantic_drift() -> None:
    compiler_input = make_input()
    pack = ActivativeIntelligencePack.compile(compiler_input)

    with pytest.raises(ActivativeContractError) as identity_error:
        replace(pack, identity_dna_ref="identity-dna://forged/v1").validate(
            compiler_input
        )
    assert _error_code(identity_error) == "IDENTITY_DRIFT"

    with pytest.raises(ActivativeContractError) as semantic_error:
        replace(pack, desired_roles=("invented authority",)).validate(
            compiler_input
        )
    assert _error_code(semantic_error) == "SEMANTIC_FLATTENING"


def test_hash_tampering_fails_closed() -> None:
    compiler_input = make_input()
    with pytest.raises(ActivativeContractError) as error:
        replace(compiler_input, input_hash=_hash("tampered")).validate()
    assert _error_code(error) == "HASH_MISMATCH"


def test_absolute_local_reference_fails_closed() -> None:
    valid = make_input()
    with pytest.raises(ActivativeContractError) as error:
        replace(valid, source_refs=("D:/private/semantic-source.yaml",)).validate()
    assert _error_code(error) == "NON_PORTABLE_REFERENCE"


def test_absolute_local_path_in_semantic_text_fails_closed() -> None:
    valid = make_input()
    with pytest.raises(ActivativeContractError) as error:
        replace(valid, format_goal="Read D:/private/semantic-source.yaml").validate()
    assert _error_code(error) == "NON_PORTABLE_REFERENCE"
