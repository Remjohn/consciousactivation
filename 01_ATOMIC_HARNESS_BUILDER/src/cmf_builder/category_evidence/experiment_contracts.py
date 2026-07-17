"""Governed contracts for BD-007 native-versus-flattened experiments.

This module defines evidence infrastructure only.  It deliberately cannot invoke a
provider.  A trial request can be materialized only after an exact BD-004 member has
been admitted and a provider configuration has separate call authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
import re
from typing import Any, Mapping, Sequence


ARCHIVE_SHA256 = "403bd07f8ca3feae94a991b16a08270fb799ffea87a05ab108163b4e1dee37b0"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class EvidenceGateError(ValueError):
    """Raised when a governed evidence prerequisite is absent or inconsistent."""


class ExperimentArm(str, Enum):
    NATIVE = "CATEGORY_NATIVE"
    FLATTENED = "FLATTENED_GENERIC_CONTROL"


class CaseState(str, Enum):
    PENDING_CORPUS_ADMISSION = "PENDING_CORPUS_ADMISSION"
    EXECUTABLE = "EXECUTABLE"


def _hash(value: str, field: str) -> str:
    if not _SHA256.fullmatch(value):
        raise EvidenceGateError(f"{field} must be a lowercase SHA-256 digest")
    return value


def require_sha256(value: str, field: str) -> str:
    """Validate an immutable evidence identity for sibling evidence contracts."""

    return _hash(value, field)


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize governed identities without platform or process variability."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


@dataclass(frozen=True)
class CorpusMemberBinding:
    """An exact member admitted by a governed BD-004 receipt."""

    archive_sha256: str
    admitted_manifest_sha256: str
    admission_receipt_sha256: str
    member_path: str
    member_sha256: str
    usage_authority_receipt_sha256: str
    provenance_status: str

    def __post_init__(self) -> None:
        if _hash(self.archive_sha256, "archive_sha256") != ARCHIVE_SHA256:
            raise EvidenceGateError("member belongs to an archive outside this campaign")
        for field in (
            "admitted_manifest_sha256",
            "admission_receipt_sha256",
            "member_sha256",
            "usage_authority_receipt_sha256",
        ):
            _hash(getattr(self, field), field)
        if not self.member_path or self.member_path.startswith(("/", "\\")):
            raise EvidenceGateError("member_path must be a non-empty archive-relative path")
        if ":" in self.member_path or ".." in self.member_path.replace("\\", "/").split("/"):
            raise EvidenceGateError("member_path must remain inside the admitted archive")
        if not self.provenance_status:
            raise EvidenceGateError("provenance_status is required")

    def as_dict(self) -> dict[str, str]:
        return {
            "archive_sha256": self.archive_sha256,
            "admitted_manifest_sha256": self.admitted_manifest_sha256,
            "admission_receipt_sha256": self.admission_receipt_sha256,
            "member_path": self.member_path.replace("\\", "/"),
            "member_sha256": self.member_sha256,
            "usage_authority_receipt_sha256": self.usage_authority_receipt_sha256,
            "provenance_status": self.provenance_status,
        }


@dataclass(frozen=True)
class CaseTemplate:
    """A non-executable paired-case specification pending corpus admission."""

    case_id: str
    category: str
    profile: str
    activative_applicable: bool
    required_dimensions: tuple[str, ...]
    semantic_field_names: tuple[str, ...]
    native_structure: tuple[str, ...]
    flattened_structure: tuple[str, ...]
    output_contract_fields: tuple[str, ...]
    source_member_role: str
    state: CaseState = CaseState.PENDING_CORPUS_ADMISSION

    def __post_init__(self) -> None:
        for field in ("case_id", "category", "profile", "source_member_role"):
            if not getattr(self, field):
                raise EvidenceGateError(f"{field} is required")
        for field in (
            "required_dimensions",
            "semantic_field_names",
            "native_structure",
            "flattened_structure",
            "output_contract_fields",
        ):
            values = getattr(self, field)
            if not values or len(values) != len(set(values)):
                raise EvidenceGateError(f"{field} must be non-empty and duplicate-free")
        if set(self.native_structure) == set(self.flattened_structure):
            raise EvidenceGateError("native and flattened structures must be materially distinct")
        if self.state is not CaseState.PENDING_CORPUS_ADMISSION:
            raise EvidenceGateError("an unbound template cannot be executable")

    @property
    def template_identity(self) -> str:
        return canonical_sha256(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "category": self.category,
            "profile": self.profile,
            "activative_applicable": self.activative_applicable,
            "required_dimensions": list(self.required_dimensions),
            "semantic_field_names": list(self.semantic_field_names),
            "native_structure": list(self.native_structure),
            "flattened_structure": list(self.flattened_structure),
            "output_contract_fields": list(self.output_contract_fields),
            "source_member_role": self.source_member_role,
            "state": self.state.value,
        }

    def bind(
        self,
        *,
        member: CorpusMemberBinding,
        governed_semantic_input_sha256: str,
        wrong_reading_lock_sha256s: Sequence[str],
        authority_chain_sha256: str,
        lineage_sha256: str,
    ) -> "ExecutableCase":
        locks = tuple(wrong_reading_lock_sha256s)
        if self.activative_applicable and not locks:
            raise EvidenceGateError("Activative cases require non-empty wrong-reading locks")
        for index, digest in enumerate(locks):
            _hash(digest, f"wrong_reading_lock_sha256s[{index}]")
        return ExecutableCase(
            template=self,
            member=member,
            governed_semantic_input_sha256=_hash(
                governed_semantic_input_sha256, "governed_semantic_input_sha256"
            ),
            wrong_reading_lock_sha256s=locks,
            authority_chain_sha256=_hash(authority_chain_sha256, "authority_chain_sha256"),
            lineage_sha256=_hash(lineage_sha256, "lineage_sha256"),
        )


@dataclass(frozen=True)
class ExecutableCase:
    template: CaseTemplate
    member: CorpusMemberBinding
    governed_semantic_input_sha256: str
    wrong_reading_lock_sha256s: tuple[str, ...]
    authority_chain_sha256: str
    lineage_sha256: str

    @property
    def state(self) -> CaseState:
        return CaseState.EXECUTABLE

    @property
    def case_identity(self) -> str:
        return canonical_sha256(self.as_dict())

    def arm_payload(self, arm: ExperimentArm) -> dict[str, Any]:
        structure = (
            self.template.native_structure
            if arm is ExperimentArm.NATIVE
            else self.template.flattened_structure
        )
        return {
            "case_identity": self.case_identity,
            "case_id": self.template.case_id,
            "arm": arm.value,
            "category": self.template.category,
            "profile": self.template.profile,
            "governed_semantic_input_sha256": self.governed_semantic_input_sha256,
            "source_member_sha256": self.member.member_sha256,
            "authority_chain_sha256": self.authority_chain_sha256,
            "lineage_sha256": self.lineage_sha256,
            "wrong_reading_lock_sha256s": list(self.wrong_reading_lock_sha256s),
            "output_contract_fields": list(self.template.output_contract_fields),
            "structure": list(structure),
        }

    def as_dict(self) -> dict[str, Any]:
        return {
            "template": self.template.as_dict(),
            "member": self.member.as_dict(),
            "governed_semantic_input_sha256": self.governed_semantic_input_sha256,
            "wrong_reading_lock_sha256s": list(self.wrong_reading_lock_sha256s),
            "authority_chain_sha256": self.authority_chain_sha256,
            "lineage_sha256": self.lineage_sha256,
            "state": self.state.value,
        }


@dataclass(frozen=True)
class ProviderTrialAuthority:
    configuration_sha256: str
    authority_receipt_sha256: str
    authorized: bool
    maximum_calls: int
    data_scope_sha256: str

    def __post_init__(self) -> None:
        for field in (
            "configuration_sha256",
            "authority_receipt_sha256",
            "data_scope_sha256",
        ):
            _hash(getattr(self, field), field)
        if self.maximum_calls < 1:
            raise EvidenceGateError("maximum_calls must be positive")


@dataclass(frozen=True)
class TrialRequest:
    case_identity: str
    case_id: str
    arm: ExperimentArm
    provider_configuration_sha256: str
    provider_authority_receipt_sha256: str
    request_payload_sha256: str
    repeat_index: int
    execution_budget_sha256: str
    deterministic_controls_sha256: str

    @property
    def request_identity(self) -> str:
        return canonical_sha256(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_identity": self.case_identity,
            "case_id": self.case_id,
            "arm": self.arm.value,
            "provider_configuration_sha256": self.provider_configuration_sha256,
            "provider_authority_receipt_sha256": self.provider_authority_receipt_sha256,
            "request_payload_sha256": self.request_payload_sha256,
            "repeat_index": self.repeat_index,
            "execution_budget_sha256": self.execution_budget_sha256,
            "deterministic_controls_sha256": self.deterministic_controls_sha256,
        }


def build_trial_requests(
    case: ExecutableCase,
    authority: ProviderTrialAuthority,
    *,
    repeats: int,
    execution_budget: Mapping[str, Any],
    deterministic_controls: Mapping[str, Any],
) -> tuple[TrialRequest, ...]:
    """Create paired immutable requests, never executing them."""

    if not authority.authorized:
        raise EvidenceGateError("provider calls are not governed and authorized")
    if repeats < 3:
        raise EvidenceGateError("each arm requires at least three repeats")
    required_calls = repeats * len(ExperimentArm)
    if required_calls > authority.maximum_calls:
        raise EvidenceGateError("trial exceeds the governed maximum call count")
    budget_hash = canonical_sha256(dict(execution_budget))
    controls_hash = canonical_sha256(dict(deterministic_controls))
    requests: list[TrialRequest] = []
    for arm in ExperimentArm:
        payload_hash = canonical_sha256(case.arm_payload(arm))
        for repeat_index in range(1, repeats + 1):
            requests.append(
                TrialRequest(
                    case_identity=case.case_identity,
                    case_id=case.template.case_id,
                    arm=arm,
                    provider_configuration_sha256=authority.configuration_sha256,
                    provider_authority_receipt_sha256=authority.authority_receipt_sha256,
                    request_payload_sha256=payload_hash,
                    repeat_index=repeat_index,
                    execution_budget_sha256=budget_hash,
                    deterministic_controls_sha256=controls_hash,
                )
            )
    return tuple(
        sorted(requests, key=lambda item: (item.case_id, item.arm.value, item.repeat_index))
    )


def governed_case_templates() -> tuple[CaseTemplate, ...]:
    """Return the fixed v1 case families without pretending they bind corpus evidence."""

    activative_semantics = (
        "category_identity",
        "category_constitution_version",
        "shared_activative_core_ref",
        "identity_dna_ref",
        "audience_context_premise_ref",
        "edge_pressure",
        "activative_call_constraints",
        "desired_human_role",
        "desired_reaction",
        "micro_commitment",
        "wrong_reading_locks",
        "semantic_lineage",
    )
    activative_outputs = (
        "category_identity",
        "category_native_projection",
        "semantic_lineage",
        "wrong_reading_locks",
        "compatibility_status",
        "maturity_status",
    )
    return (
        CaseTemplate(
            case_id="BD007-CASE-SHORT-FORM-EDITED-VIDEO",
            category="short_form_edited_video",
            profile="PENDING_FINAL_ADMITTED_SHORT_FORM_PROFILE",
            activative_applicable=True,
            required_dimensions=(
                "category_identity_preservation",
                "category_native_syntax",
                "spatial_structure",
                "temporal_structure",
                "reading_order_integrity",
                "identity_fidelity",
                "audience_context_fidelity",
                "edge_pressure_preservation",
                "activative_call_integrity",
                "desired_human_role_integrity",
                "desired_reaction_integrity",
                "micro_commitment_integrity",
                "wrong_reading_resistance",
                "semantic_lineage_completeness",
                "non_invention_of_human_truth",
                "output_contract_compliance",
            ),
            semantic_field_names=activative_semantics,
            native_structure=(
                "visual_hierarchy",
                "shot_and_cut_identity",
                "spatial_order",
                "temporal_order",
                "reading_order",
                "edited_video_activative_sequence",
            ),
            flattened_structure=("generic_section", "generic_item", "generic_sequence"),
            output_contract_fields=activative_outputs,
            source_member_role="short_form_category_syntax_and_sequencing_evidence",
        ),
        CaseTemplate(
            case_id="BD007-CASE-FORMAT02-2D-CHARACTER-ANIMATION",
            category="2d_character_animation",
            profile="format02_minimal_coach_theatre",
            activative_applicable=True,
            required_dimensions=(
                "category_identity_preservation",
                "category_native_syntax",
                "spatial_structure",
                "temporal_structure",
                "reading_order_integrity",
                "identity_fidelity",
                "audience_context_fidelity",
                "edge_pressure_preservation",
                "activative_call_integrity",
                "desired_human_role_integrity",
                "desired_reaction_integrity",
                "micro_commitment_integrity",
                "wrong_reading_resistance",
                "semantic_lineage_completeness",
                "non_invention_of_human_truth",
                "output_contract_compliance",
            ),
            semantic_field_names=activative_semantics,
            native_structure=(
                "stage_and_scene_identity",
                "character_state",
                "pose_gaze_gesture",
                "spatial_blocking",
                "performance_timing",
                "character_performance_activative_sequence",
            ),
            flattened_structure=("generic_video_timeline", "generic_shot", "generic_transition"),
            output_contract_fields=activative_outputs,
            source_member_role="format02_character_performance_syntax_and_sequencing_evidence",
        ),
        CaseTemplate(
            case_id="BD007-CASE-STRUCTURAL-CONVERSATIONAL",
            category="conversational_activation_expression",
            profile="PENDING_FINAL_ADMITTED_STRUCTURAL_CONVERSATIONAL_PROFILE",
            activative_applicable=True,
            required_dimensions=(
                "category_identity_preservation",
                "category_native_syntax",
                "temporal_structure",
                "conversational_turn_integrity",
                "identity_fidelity",
                "audience_context_fidelity",
                "edge_pressure_preservation",
                "activative_call_integrity",
                "desired_human_role_integrity",
                "desired_reaction_integrity",
                "micro_commitment_integrity",
                "wrong_reading_resistance",
                "semantic_lineage_completeness",
                "non_invention_of_human_truth",
                "output_contract_compliance",
            ),
            semantic_field_names=activative_semantics
            + ("reaction_receipt_applicability", "expression_moment_applicability"),
            native_structure=(
                "turn_identity",
                "speaker_authority",
                "reaction_boundary",
                "follow_up_turn",
                "expression_elevation",
                "governed_close",
            ),
            flattened_structure=("generic_document", "generic_paragraph", "generic_timeline"),
            output_contract_fields=activative_outputs
            + ("reaction_receipt_applicability", "expression_moment_applicability"),
            source_member_role="structural_conversational_turn_syntax_evidence",
        ),
        CaseTemplate(
            case_id="BD007-CASE-GENERIC-NON-ACTIVATIVE-CONTROL",
            category="NOT_APPLICABLE",
            profile="generic_non_activative_control",
            activative_applicable=False,
            required_dimensions=(
                "category_identity_preservation",
                "semantic_lineage_completeness",
                "non_invention_of_human_truth",
                "output_contract_compliance",
            ),
            semantic_field_names=(
                "atomic_task_identity",
                "governed_source_ref",
                "input_contract",
                "output_contract",
                "semantic_lineage",
                "category_applicability_justification",
            ),
            native_structure=(
                "explicit_category_not_applicable",
                "atomic_input_contract",
                "deterministic_transformation",
                "atomic_output_contract",
            ),
            flattened_structure=("generic_document", "generic_section", "generic_value"),
            output_contract_fields=(
                "category_applicability",
                "deterministic_output",
                "semantic_lineage",
                "production_ready",
                "certified",
            ),
            source_member_role="generic_non_activative_negative_control_evidence",
        ),
    )


def template_arm_identity(template: CaseTemplate, arm: ExperimentArm) -> str:
    """Hash the unbound arm instructions; this is not an empirical request hash."""

    return canonical_sha256(
        {
            "template_identity": template.template_identity,
            "arm": arm.value,
            "structure": list(
                template.native_structure
                if arm is ExperimentArm.NATIVE
                else template.flattened_structure
            ),
            "semantic_field_names": list(template.semantic_field_names),
            "output_contract_fields": list(template.output_contract_fields),
            "corpus_binding": "PENDING_FINAL_ADMITTED_MEMBER",
        }
    )
