from __future__ import annotations

import json
import re
from dataclasses import dataclass, replace
from enum import Enum
from hashlib import sha256
from typing import Mapping


SKILL_ID = "activative_intelligence_pack_compiler"
SKILL_VERSION = "1.0.0"
AUTHORITY_LANE = "Analyst"
MATURITY_STATUS = "development_uncertified"
INPUT_SCHEMA_ID = "cmf-builder-activative-compiler-input/v1"
PACK_SCHEMA_ID = "cmf-builder-activative-intelligence-pack/v1"


class ActivativeContractError(ValueError):
    """A typed, fail-closed semantic contract violation."""

    def __init__(self, code: str, message: str, *, field_path: str) -> None:
        super().__init__(message)
        self.code = code
        self.field_path = field_path


class DownstreamArtifact(str, Enum):
    REACTION_RECEIPT = "reaction_receipt"
    EXPRESSION_MOMENT = "expression_moment"
    VISUAL_SEMANTIC_PACK = "visual_semantic_pack"
    VISUAL_NARRATIVE_PROGRAM = "visual_narrative_program"
    FEATURE_CONTRACTS = "feature_contracts"
    TV_ROUTE = "tv_route"
    COMPOSITION_INTENT = "composition_intent"


class Applicability(str, Enum):
    APPLICABLE = "APPLICABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class ApplicabilityReason(str, Enum):
    EXTERNAL_HUMAN_REACTION_CAPTURE_REQUIRED = (
        "external_human_reaction_capture_required"
    )
    NO_GOVERNED_HUMAN_REACTION_EXISTS = "no_governed_human_reaction_exists"
    SOURCE_BACKED_EXPRESSION_REQUIRED = "source_backed_expression_required"
    NO_GOVERNED_SOURCE_EXPRESSION_EXISTS = (
        "no_governed_source_expression_exists"
    )
    VISUAL_SEMANTIC_ROUTE_REQUIRED = "visual_semantic_route_required"
    VISUAL_NARRATIVE_ROUTE_REQUIRED = "visual_narrative_route_required"
    FEATURE_CONTRACTS_REQUIRED = "feature_contracts_required"
    SOMATIC_ROUTE_REQUIRED = "somatic_route_required"
    COMPOSITION_HANDOFF_REQUIRED = "composition_handoff_required"
    NON_VISUAL_FORMAT_GOAL = "non_visual_format_goal"


DOWNSTREAM_ARTIFACT_ORDER = tuple(DownstreamArtifact)

EXPECTED_DOWNSTREAM_OWNERS = {
    DownstreamArtifact.REACTION_RECEIPT: "human_expression_source_owner",
    DownstreamArtifact.EXPRESSION_MOMENT: "human_expression_source_owner",
    DownstreamArtifact.VISUAL_SEMANTIC_PACK: "activative_visual_semantics_owner",
    DownstreamArtifact.VISUAL_NARRATIVE_PROGRAM: (
        "activative_visual_narrative_owner"
    ),
    DownstreamArtifact.FEATURE_CONTRACTS: "feature_contract_owner",
    DownstreamArtifact.TV_ROUTE: "somatic_route_owner",
    DownstreamArtifact.COMPOSITION_INTENT: "composition_owner",
}

_APPLICABLE_REASONS = {
    DownstreamArtifact.REACTION_RECEIPT: {
        ApplicabilityReason.EXTERNAL_HUMAN_REACTION_CAPTURE_REQUIRED
    },
    DownstreamArtifact.EXPRESSION_MOMENT: {
        ApplicabilityReason.SOURCE_BACKED_EXPRESSION_REQUIRED
    },
    DownstreamArtifact.VISUAL_SEMANTIC_PACK: {
        ApplicabilityReason.VISUAL_SEMANTIC_ROUTE_REQUIRED
    },
    DownstreamArtifact.VISUAL_NARRATIVE_PROGRAM: {
        ApplicabilityReason.VISUAL_NARRATIVE_ROUTE_REQUIRED
    },
    DownstreamArtifact.FEATURE_CONTRACTS: {
        ApplicabilityReason.FEATURE_CONTRACTS_REQUIRED
    },
    DownstreamArtifact.TV_ROUTE: {ApplicabilityReason.SOMATIC_ROUTE_REQUIRED},
    DownstreamArtifact.COMPOSITION_INTENT: {
        ApplicabilityReason.COMPOSITION_HANDOFF_REQUIRED
    },
}

_NOT_APPLICABLE_REASONS = {
    DownstreamArtifact.REACTION_RECEIPT: {
        ApplicabilityReason.NO_GOVERNED_HUMAN_REACTION_EXISTS
    },
    DownstreamArtifact.EXPRESSION_MOMENT: {
        ApplicabilityReason.NO_GOVERNED_SOURCE_EXPRESSION_EXISTS
    },
    DownstreamArtifact.VISUAL_SEMANTIC_PACK: {
        ApplicabilityReason.NON_VISUAL_FORMAT_GOAL
    },
    DownstreamArtifact.VISUAL_NARRATIVE_PROGRAM: {
        ApplicabilityReason.NON_VISUAL_FORMAT_GOAL
    },
    DownstreamArtifact.FEATURE_CONTRACTS: {
        ApplicabilityReason.NON_VISUAL_FORMAT_GOAL
    },
    DownstreamArtifact.TV_ROUTE: {ApplicabilityReason.NON_VISUAL_FORMAT_GOAL},
    DownstreamArtifact.COMPOSITION_INTENT: {
        ApplicabilityReason.NON_VISUAL_FORMAT_GOAL
    },
}


@dataclass(frozen=True, slots=True)
class DownstreamApplicabilityDecision:
    artifact: DownstreamArtifact
    applicability: Applicability
    reason_code: ApplicabilityReason
    reason: str
    authority_owner: str
    evidence_refs: tuple[str, ...]
    existing_artifact_refs: tuple[str, ...] = ()

    def validate(self) -> None:
        path = f"downstream_applicability.{self.artifact.value}"
        _require_text(self.reason, f"{path}.reason")
        _require_ref(self.authority_owner, f"{path}.authority_owner")
        _require_nonempty_unique_refs(
            self.evidence_refs, f"{path}.evidence_refs", code="MISSING_EVIDENCE"
        )
        _require_unique_refs(
            self.existing_artifact_refs, f"{path}.existing_artifact_refs"
        )
        if self.authority_owner != EXPECTED_DOWNSTREAM_OWNERS[self.artifact]:
            raise ActivativeContractError(
                "AUTHORITY_CONFLICT",
                "Downstream semantic authority cannot be reassigned to this skill.",
                field_path=f"{path}.authority_owner",
            )
        reasons = (
            _APPLICABLE_REASONS[self.artifact]
            if self.applicability is Applicability.APPLICABLE
            else _NOT_APPLICABLE_REASONS[self.artifact]
        )
        if self.reason_code not in reasons:
            raise ActivativeContractError(
                "UNJUSTIFIED_APPLICABILITY",
                "The reason does not govern this artifact and applicability status.",
                field_path=f"{path}.reason_code",
            )
        if (
            self.applicability is Applicability.NOT_APPLICABLE
            and self.existing_artifact_refs
        ):
            raise ActivativeContractError(
                "UNJUSTIFIED_APPLICABILITY",
                "NOT_APPLICABLE cannot discard governed artifact references.",
                field_path=f"{path}.existing_artifact_refs",
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "applicability": self.applicability.value,
            "artifact": self.artifact.value,
            "authority_owner": self.authority_owner,
            "evidence_refs": list(self.evidence_refs),
            "existing_artifact_refs": list(self.existing_artifact_refs),
            "reason": self.reason,
            "reason_code": self.reason_code.value,
        }


@dataclass(frozen=True, slots=True)
class SemanticFieldLineage:
    field_path: str
    source_ref: str
    source_hash: str
    authority_ref: str
    evidence_refs: tuple[str, ...]

    def validate(self) -> None:
        _require_ref(self.field_path, "lineage.field_path")
        _require_ref(self.source_ref, f"lineage.{self.field_path}.source_ref")
        _require_hash(self.source_hash, f"lineage.{self.field_path}.source_hash")
        _require_ref(
            self.authority_ref, f"lineage.{self.field_path}.authority_ref"
        )
        _require_nonempty_unique_refs(
            self.evidence_refs,
            f"lineage.{self.field_path}.evidence_refs",
            code="MISSING_EVIDENCE",
        )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "authority_ref": self.authority_ref,
            "evidence_refs": list(self.evidence_refs),
            "field_path": self.field_path,
            "source_hash": self.source_hash,
            "source_ref": self.source_ref,
        }


def _semantic_field_paths() -> tuple[str, ...]:
    base = (
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
    )
    downstream = tuple(
        f"downstream_applicability.{artifact.value}"
        for artifact in DOWNSTREAM_ARTIFACT_ORDER
    )
    return (*base, *downstream)


SEMANTIC_FIELD_PATHS = _semantic_field_paths()


@dataclass(frozen=True, slots=True)
class ActivativeCompilerInput:
    input_id: str
    input_hash: str
    schema_id: str
    skill_id: str
    skill_version: str
    authority_lane: str
    source_refs: tuple[str, ...]
    authority_refs: tuple[str, ...]
    identity_dna_ref: str
    audience_context_premise_ref: str
    live_premise_evidence_refs: tuple[str, ...]
    resonance_map_ref: str
    matrix_of_edging_ref: str
    edge_pressure: str
    format_goal: str
    desired_roles: tuple[str, ...]
    activative_call_constraints: tuple[str, ...]
    desired_reaction: str
    micro_commitment: str
    wrong_reading_locks: tuple[str, ...]
    downstream_applicability: tuple[DownstreamApplicabilityDecision, ...]
    lineage: tuple[SemanticFieldLineage, ...]
    requested_operations: tuple[str, ...]
    authority_conflicts: tuple[str, ...]
    external_provider_execution_requested: bool
    production_eligible_requested: bool
    certification_requested: bool

    @classmethod
    def create(
        cls,
        *,
        source_refs: tuple[str, ...],
        authority_refs: tuple[str, ...],
        identity_dna_ref: str,
        audience_context_premise_ref: str,
        live_premise_evidence_refs: tuple[str, ...],
        resonance_map_ref: str,
        matrix_of_edging_ref: str,
        edge_pressure: str,
        format_goal: str,
        desired_roles: tuple[str, ...],
        activative_call_constraints: tuple[str, ...],
        desired_reaction: str,
        micro_commitment: str,
        wrong_reading_locks: tuple[str, ...],
        downstream_applicability: tuple[DownstreamApplicabilityDecision, ...],
        lineage: tuple[SemanticFieldLineage, ...],
        requested_operations: tuple[str, ...] = ("compile_activation_field",),
        authority_conflicts: tuple[str, ...] = (),
        external_provider_execution_requested: bool = False,
        production_eligible_requested: bool = False,
        certification_requested: bool = False,
    ) -> "ActivativeCompilerInput":
        candidate = cls(
            input_id="pending",
            input_hash="pending",
            schema_id=INPUT_SCHEMA_ID,
            skill_id=SKILL_ID,
            skill_version=SKILL_VERSION,
            authority_lane=AUTHORITY_LANE,
            source_refs=source_refs,
            authority_refs=authority_refs,
            identity_dna_ref=identity_dna_ref,
            audience_context_premise_ref=audience_context_premise_ref,
            live_premise_evidence_refs=live_premise_evidence_refs,
            resonance_map_ref=resonance_map_ref,
            matrix_of_edging_ref=matrix_of_edging_ref,
            edge_pressure=edge_pressure,
            format_goal=format_goal,
            desired_roles=desired_roles,
            activative_call_constraints=activative_call_constraints,
            desired_reaction=desired_reaction,
            micro_commitment=micro_commitment,
            wrong_reading_locks=wrong_reading_locks,
            downstream_applicability=downstream_applicability,
            lineage=lineage,
            requested_operations=requested_operations,
            authority_conflicts=authority_conflicts,
            external_provider_execution_requested=(
                external_provider_execution_requested
            ),
            production_eligible_requested=production_eligible_requested,
            certification_requested=certification_requested,
        )
        candidate.validate(verify_identity=False)
        digest = sha256(candidate._content_bytes()).hexdigest()
        result = replace(
            candidate,
            input_id=f"activative-compiler-input_{digest}",
            input_hash=f"sha256:{digest}",
        )
        result.validate()
        return result

    def validate(self, *, verify_identity: bool = True) -> None:
        if (
            self.schema_id != INPUT_SCHEMA_ID
            or self.skill_id != SKILL_ID
            or self.skill_version != SKILL_VERSION
            or self.authority_lane != AUTHORITY_LANE
        ):
            raise ActivativeContractError(
                "CONTRACT_VERSION_MISMATCH",
                "The input does not match the frozen skill interface.",
                field_path="schema_id",
            )
        _require_nonempty_unique_refs(
            self.source_refs, "source_refs", code="MISSING_EVIDENCE"
        )
        _require_nonempty_unique_refs(
            self.authority_refs, "authority_refs", code="MISSING_EVIDENCE"
        )
        for path, value in (
            ("identity_dna_ref", self.identity_dna_ref),
            (
                "audience_context_premise_ref",
                self.audience_context_premise_ref,
            ),
            ("resonance_map_ref", self.resonance_map_ref),
            ("matrix_of_edging_ref", self.matrix_of_edging_ref),
        ):
            _require_ref(value, path)
        _require_nonempty_unique_refs(
            self.live_premise_evidence_refs,
            "live_premise_evidence_refs",
            code="MISSING_EVIDENCE",
        )
        for path, value in (
            ("edge_pressure", self.edge_pressure),
            ("format_goal", self.format_goal),
            ("desired_reaction", self.desired_reaction),
            ("micro_commitment", self.micro_commitment),
        ):
            _require_text(value, path)
        _require_nonempty_unique_text(self.desired_roles, "desired_roles")
        _require_nonempty_unique_text(
            self.activative_call_constraints, "activative_call_constraints"
        )
        if not self.wrong_reading_locks:
            raise ActivativeContractError(
                "WRONG_READING_LOCKS_REQUIRED",
                "At least one explicit wrong-reading lock is required.",
                field_path="wrong_reading_locks",
            )
        _require_nonempty_unique_text(
            self.wrong_reading_locks, "wrong_reading_locks"
        )
        self._validate_downstream_applicability()
        self._validate_lineage()
        if self.authority_conflicts:
            raise ActivativeContractError(
                "AUTHORITY_CONFLICT",
                "Unresolved field authority conflicts block compilation.",
                field_path="authority_conflicts",
            )
        if self.requested_operations != ("compile_activation_field",):
            raise ActivativeContractError(
                "HUMAN_TRUTH_BOUNDARY_VIOLATION",
                "The skill may compile the activation field only.",
                field_path="requested_operations",
            )
        if self.external_provider_execution_requested:
            raise ActivativeContractError(
                "EXTERNAL_PROVIDER_EXECUTION_FORBIDDEN",
                "The semantic compiler cannot execute providers.",
                field_path="external_provider_execution_requested",
            )
        if self.production_eligible_requested or self.certification_requested:
            raise ActivativeContractError(
                "PRODUCTION_CLAIM_FORBIDDEN",
                "The development skill cannot claim production or certification.",
                field_path=(
                    "production_eligible_requested"
                    if self.production_eligible_requested
                    else "certification_requested"
                ),
            )
        if verify_identity:
            digest = sha256(self._content_bytes()).hexdigest()
            if (
                self.input_id != f"activative-compiler-input_{digest}"
                or self.input_hash != f"sha256:{digest}"
            ):
                raise ActivativeContractError(
                    "HASH_MISMATCH",
                    "The input identity does not match canonical content.",
                    field_path="input_hash",
                )

    def _validate_downstream_applicability(self) -> None:
        artifacts = tuple(item.artifact for item in self.downstream_applicability)
        if artifacts != DOWNSTREAM_ARTIFACT_ORDER:
            raise ActivativeContractError(
                "SEMANTIC_FLATTENING",
                "Every downstream artifact requires one ordered decision.",
                field_path="downstream_applicability",
            )
        for decision in self.downstream_applicability:
            decision.validate()

    def _validate_lineage(self) -> None:
        paths = tuple(item.field_path for item in self.lineage)
        if paths != SEMANTIC_FIELD_PATHS or len(set(paths)) != len(paths):
            raise ActivativeContractError(
                "SEMANTIC_FLATTENING",
                "Every semantic field requires independent ordered lineage.",
                field_path="lineage",
            )
        allowed_sources = {
            *self.source_refs,
            *self.authority_refs,
            self.identity_dna_ref,
            self.audience_context_premise_ref,
            *self.live_premise_evidence_refs,
            self.resonance_map_ref,
            self.matrix_of_edging_ref,
        }
        for decision in self.downstream_applicability:
            allowed_sources.update(decision.evidence_refs)
            allowed_sources.update(decision.existing_artifact_refs)
        for item in self.lineage:
            item.validate()
            if item.authority_ref not in self.authority_refs:
                raise ActivativeContractError(
                    "AUTHORITY_CONFLICT",
                    "Field lineage cites authority outside authority_refs.",
                    field_path=f"lineage.{item.field_path}.authority_ref",
                )
            if item.source_ref not in allowed_sources:
                raise ActivativeContractError(
                    "MISSING_EVIDENCE",
                    "Field lineage cites evidence outside the governed input.",
                    field_path=f"lineage.{item.field_path}.source_ref",
                )
        by_path = {item.field_path: item for item in self.lineage}
        exact_reference_fields = {
            "identity_dna_ref": (self.identity_dna_ref, "IDENTITY_DRIFT"),
            "audience_context_premise_ref": (
                self.audience_context_premise_ref,
                "AUDIENCE_CONTEXT_DRIFT",
            ),
            "resonance_map_ref": (self.resonance_map_ref, "LINEAGE_DRIFT"),
            "matrix_of_edging_ref": (
                self.matrix_of_edging_ref,
                "LINEAGE_DRIFT",
            ),
        }
        for path, (expected, code) in exact_reference_fields.items():
            if by_path[path].source_ref != expected:
                raise ActivativeContractError(
                    code,
                    "A reference field differs from its governed lineage source.",
                    field_path=f"lineage.{path}.source_ref",
                )

    def _content_dict(self) -> dict[str, object]:
        return {
            "activative_call_constraints": list(
                self.activative_call_constraints
            ),
            "audience_context_premise_ref": self.audience_context_premise_ref,
            "authority_conflicts": list(self.authority_conflicts),
            "authority_lane": self.authority_lane,
            "authority_refs": list(self.authority_refs),
            "certification_requested": self.certification_requested,
            "desired_reaction": self.desired_reaction,
            "desired_reaction_status": "intended_not_observed",
            "desired_roles": list(self.desired_roles),
            "downstream_applicability": [
                item.canonical_dict() for item in self.downstream_applicability
            ],
            "edge_pressure": self.edge_pressure,
            "external_provider_execution_requested": (
                self.external_provider_execution_requested
            ),
            "format_goal": self.format_goal,
            "identity_dna_ref": self.identity_dna_ref,
            "lineage": [item.canonical_dict() for item in self.lineage],
            "live_premise_evidence_refs": list(
                self.live_premise_evidence_refs
            ),
            "matrix_of_edging_ref": self.matrix_of_edging_ref,
            "micro_commitment": self.micro_commitment,
            "production_eligible_requested": self.production_eligible_requested,
            "requested_operations": list(self.requested_operations),
            "resonance_map_ref": self.resonance_map_ref,
            "schema_id": self.schema_id,
            "skill_id": self.skill_id,
            "skill_version": self.skill_version,
            "source_refs": list(self.source_refs),
            "wrong_reading_locks": list(self.wrong_reading_locks),
        }

    def _content_bytes(self) -> bytes:
        return _canonical_json(self._content_dict())

    def canonical_dict(self) -> dict[str, object]:
        return {
            "input_hash": self.input_hash,
            "input_id": self.input_id,
            **self._content_dict(),
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class ActivativeIntelligencePack:
    pack_id: str
    pack_hash: str
    schema_id: str
    skill_id: str
    skill_version: str
    authority_lane: str
    compiler_input_id: str
    compiler_input_hash: str
    source_refs: tuple[str, ...]
    authority_refs: tuple[str, ...]
    identity_dna_ref: str
    audience_context_premise_ref: str
    live_premise_evidence_refs: tuple[str, ...]
    resonance_map_ref: str
    matrix_of_edging_ref: str
    edge_pressure: str
    format_goal: str
    desired_roles: tuple[str, ...]
    activative_call_constraints: tuple[str, ...]
    desired_reaction: str
    micro_commitment: str
    wrong_reading_locks: tuple[str, ...]
    downstream_applicability: tuple[DownstreamApplicabilityDecision, ...]
    lineage: tuple[SemanticFieldLineage, ...]
    performed_operations: tuple[str, ...]
    desired_reaction_status: str
    issued_receipt_kinds: tuple[str, ...]
    human_truth_generated: bool
    human_reaction_generated: bool
    identity_approval_issued: bool
    external_provider_executed: bool
    maturity_status: str
    production_eligible: bool
    certified: bool

    @classmethod
    def compile(
        cls, compiler_input: ActivativeCompilerInput
    ) -> "ActivativeIntelligencePack":
        compiler_input.validate()
        candidate = cls(
            pack_id="pending",
            pack_hash="pending",
            schema_id=PACK_SCHEMA_ID,
            skill_id=SKILL_ID,
            skill_version=SKILL_VERSION,
            authority_lane=AUTHORITY_LANE,
            compiler_input_id=compiler_input.input_id,
            compiler_input_hash=compiler_input.input_hash,
            source_refs=compiler_input.source_refs,
            authority_refs=compiler_input.authority_refs,
            identity_dna_ref=compiler_input.identity_dna_ref,
            audience_context_premise_ref=(
                compiler_input.audience_context_premise_ref
            ),
            live_premise_evidence_refs=(
                compiler_input.live_premise_evidence_refs
            ),
            resonance_map_ref=compiler_input.resonance_map_ref,
            matrix_of_edging_ref=compiler_input.matrix_of_edging_ref,
            edge_pressure=compiler_input.edge_pressure,
            format_goal=compiler_input.format_goal,
            desired_roles=compiler_input.desired_roles,
            activative_call_constraints=(
                compiler_input.activative_call_constraints
            ),
            desired_reaction=compiler_input.desired_reaction,
            micro_commitment=compiler_input.micro_commitment,
            wrong_reading_locks=compiler_input.wrong_reading_locks,
            downstream_applicability=compiler_input.downstream_applicability,
            lineage=compiler_input.lineage,
            performed_operations=("compile_activation_field",),
            desired_reaction_status="intended_not_observed",
            issued_receipt_kinds=(),
            human_truth_generated=False,
            human_reaction_generated=False,
            identity_approval_issued=False,
            external_provider_executed=False,
            maturity_status=MATURITY_STATUS,
            production_eligible=False,
            certified=False,
        )
        candidate.validate(compiler_input, verify_identity=False)
        digest = sha256(candidate._content_bytes()).hexdigest()
        result = replace(
            candidate,
            pack_id=f"activative-intelligence-pack_{digest}",
            pack_hash=f"sha256:{digest}",
        )
        result.validate(compiler_input)
        return result

    def validate(
        self,
        compiler_input: ActivativeCompilerInput,
        *,
        verify_identity: bool = True,
    ) -> None:
        compiler_input.validate()
        if (
            self.schema_id != PACK_SCHEMA_ID
            or self.skill_id != SKILL_ID
            or self.skill_version != SKILL_VERSION
            or self.authority_lane != AUTHORITY_LANE
            or self.compiler_input_id != compiler_input.input_id
            or self.compiler_input_hash != compiler_input.input_hash
        ):
            raise ActivativeContractError(
                "LINEAGE_DRIFT",
                "The pack does not preserve its exact compiler input.",
                field_path="compiler_input_hash",
            )
        if self.identity_dna_ref != compiler_input.identity_dna_ref:
            raise ActivativeContractError(
                "IDENTITY_DRIFT",
                "The pack cannot rewrite or approve Identity DNA.",
                field_path="identity_dna_ref",
            )
        if (
            self.audience_context_premise_ref
            != compiler_input.audience_context_premise_ref
        ):
            raise ActivativeContractError(
                "AUDIENCE_CONTEXT_DRIFT",
                "The pack cannot promote or rewrite the audience premise.",
                field_path="audience_context_premise_ref",
            )
        semantic_values = (
            "source_refs",
            "authority_refs",
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
            "lineage",
        )
        if any(
            getattr(self, name) != getattr(compiler_input, name)
            for name in semantic_values
        ):
            raise ActivativeContractError(
                "SEMANTIC_FLATTENING",
                "The pack must preserve each semantic field and its lineage.",
                field_path="lineage",
            )
        if (
            self.performed_operations != ("compile_activation_field",)
            or self.desired_reaction_status != "intended_not_observed"
            or self.issued_receipt_kinds
            or self.human_truth_generated
            or self.human_reaction_generated
            or self.identity_approval_issued
        ):
            raise ActivativeContractError(
                "HUMAN_TRUTH_BOUNDARY_VIOLATION",
                "The pack cannot manufacture human truth, reaction, or receipts.",
                field_path="performed_operations",
            )
        if self.external_provider_executed:
            raise ActivativeContractError(
                "EXTERNAL_PROVIDER_EXECUTION_FORBIDDEN",
                "The semantic pack cannot report provider execution.",
                field_path="external_provider_executed",
            )
        if (
            self.maturity_status != MATURITY_STATUS
            or self.production_eligible
            or self.certified
        ):
            raise ActivativeContractError(
                "PRODUCTION_CLAIM_FORBIDDEN",
                "The pack remains development-only and uncertified.",
                field_path="maturity_status",
            )
        if verify_identity:
            digest = sha256(self._content_bytes()).hexdigest()
            if (
                self.pack_id != f"activative-intelligence-pack_{digest}"
                or self.pack_hash != f"sha256:{digest}"
            ):
                raise ActivativeContractError(
                    "HASH_MISMATCH",
                    "The pack identity does not match canonical content.",
                    field_path="pack_hash",
                )

    def _content_dict(self) -> dict[str, object]:
        result = {
            key: value
            for key, value in ActivativeCompilerInput(
                input_id=self.compiler_input_id,
                input_hash=self.compiler_input_hash,
                schema_id=INPUT_SCHEMA_ID,
                skill_id=self.skill_id,
                skill_version=self.skill_version,
                authority_lane=self.authority_lane,
                source_refs=self.source_refs,
                authority_refs=self.authority_refs,
                identity_dna_ref=self.identity_dna_ref,
                audience_context_premise_ref=self.audience_context_premise_ref,
                live_premise_evidence_refs=self.live_premise_evidence_refs,
                resonance_map_ref=self.resonance_map_ref,
                matrix_of_edging_ref=self.matrix_of_edging_ref,
                edge_pressure=self.edge_pressure,
                format_goal=self.format_goal,
                desired_roles=self.desired_roles,
                activative_call_constraints=self.activative_call_constraints,
                desired_reaction=self.desired_reaction,
                micro_commitment=self.micro_commitment,
                wrong_reading_locks=self.wrong_reading_locks,
                downstream_applicability=self.downstream_applicability,
                lineage=self.lineage,
                requested_operations=("compile_activation_field",),
                authority_conflicts=(),
                external_provider_execution_requested=False,
                production_eligible_requested=False,
                certification_requested=False,
            )._content_dict().items()
            if key
            not in {
                "authority_conflicts",
                "certification_requested",
                "external_provider_execution_requested",
                "production_eligible_requested",
                "requested_operations",
                "schema_id",
            }
        }
        result.update(
            {
                "certified": self.certified,
                "compiler_input_hash": self.compiler_input_hash,
                "compiler_input_id": self.compiler_input_id,
                "desired_reaction_status": self.desired_reaction_status,
                "external_provider_executed": self.external_provider_executed,
                "human_reaction_generated": self.human_reaction_generated,
                "human_truth_generated": self.human_truth_generated,
                "identity_approval_issued": self.identity_approval_issued,
                "issued_receipt_kinds": list(self.issued_receipt_kinds),
                "maturity_status": self.maturity_status,
                "performed_operations": list(self.performed_operations),
                "production_eligible": self.production_eligible,
                "schema_id": self.schema_id,
            }
        )
        return result

    def _content_bytes(self) -> bytes:
        return _canonical_json(self._content_dict())

    def canonical_dict(self) -> dict[str, object]:
        return {
            "pack_hash": self.pack_hash,
            "pack_id": self.pack_id,
            **self._content_dict(),
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


def _canonical_json(value: Mapping[str, object]) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def _require_text(value: str, field_path: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ActivativeContractError(
            "MISSING_EVIDENCE",
            "A required semantic value is missing.",
            field_path=field_path,
        )
    if (
        "\\" in value
        or re.search(r"(?:^|\s)[a-zA-Z]:/", value) is not None
        or value.lower().startswith("file://")
    ):
        raise ActivativeContractError(
            "NON_PORTABLE_REFERENCE",
            "Semantic values cannot contain absolute local paths.",
            field_path=field_path,
        )


def _require_ref(value: str, field_path: str) -> None:
    _require_text(value, field_path)


def _require_hash(value: str, field_path: str) -> None:
    if re.fullmatch(r"sha256:[0-9a-f]{64}", value) is None:
        raise ActivativeContractError(
            "HASH_MISMATCH",
            "A governed SHA-256 reference is malformed.",
            field_path=field_path,
        )


def _require_nonempty_unique_text(values: tuple[str, ...], field_path: str) -> None:
    if not values or len(values) != len(set(values)):
        raise ActivativeContractError(
            "MISSING_EVIDENCE",
            "The semantic collection must be non-empty and unique.",
            field_path=field_path,
        )
    for value in values:
        _require_text(value, field_path)


def _require_unique_refs(values: tuple[str, ...], field_path: str) -> None:
    if len(values) != len(set(values)):
        raise ActivativeContractError(
            "LINEAGE_DRIFT",
            "Reference collections cannot contain duplicate identities.",
            field_path=field_path,
        )
    for value in values:
        _require_ref(value, field_path)


def _require_nonempty_unique_refs(
    values: tuple[str, ...], field_path: str, *, code: str
) -> None:
    if not values:
        raise ActivativeContractError(
            code,
            "At least one governed evidence reference is required.",
            field_path=field_path,
        )
    _require_unique_refs(values, field_path)
