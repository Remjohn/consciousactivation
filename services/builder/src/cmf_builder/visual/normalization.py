"""Deterministic typed syntax-observation normalization for ST-02.01.

The module implements only the OD-AM-001 offline structural branch.  It accepts
governed repository fixtures, produces immutable syntax observations, and rejects
any attempt to promote provider text or semantic hypotheses into observations.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence

from cmf_builder.visual.geometry import NormalizedBox, PixelBox, normalize_box
from cmf_builder.visual.ontology import (
    Applicability,
    ApplicabilityStatus,
    EvidenceOrigin,
    GovernedStatus,
    KnowledgeStatus,
    ObservationContaminated,
    ObservationStatus,
    ProvenanceReference,
    ProviderOnlyClaimRejected,
    SourceEvidenceInvalid,
    SourceReference,
    SyntaxContractError,
    SyntaxOntology,
    Uncertainty,
    UncertaintyKind,
    canonical_sha256,
    require_identifier,
    validate_structural_fields,
)


STORY_ID = "ST-02.01"
DEVELOPMENT_MODE = "OD_AM_001_OFFLINE_DEVELOPMENT"


class SpecimenInvalid(SyntaxContractError):
    code = "SpecimenInvalid"


class DuplicateInflationRejected(SyntaxContractError):
    code = "DuplicateInflationRejected"


class DuplicateKind(str, Enum):
    EXACT_SOURCE_HASH = "EXACT_SOURCE_HASH"
    NEAR_DUPLICATE_STRUCTURE = "NEAR_DUPLICATE_STRUCTURE"


@dataclass(frozen=True, slots=True)
class ComponentEvidence:
    component_id: str
    ontology_term_id: str
    pixel_box: PixelBox
    observation_status: ObservationStatus
    knowledge_status: KnowledgeStatus
    provenance: tuple[ProvenanceReference, ...]
    uncertainty: Uncertainty
    applicability: Applicability
    structural_fields: tuple[tuple[str, str | int | bool], ...] = ()

    @classmethod
    def create(
        cls,
        *,
        component_id: str,
        ontology_term_id: str,
        pixel_box: PixelBox,
        observation_status: ObservationStatus,
        knowledge_status: KnowledgeStatus,
        provenance: Sequence[ProvenanceReference],
        uncertainty: Uncertainty,
        applicability: Applicability,
        structural_fields: Mapping[str, str | int | bool] | None = None,
    ) -> "ComponentEvidence":
        return cls(
            component_id=component_id,
            ontology_term_id=ontology_term_id,
            pixel_box=pixel_box,
            observation_status=observation_status,
            knowledge_status=knowledge_status,
            provenance=tuple(
                sorted(
                    provenance,
                    key=lambda item: (
                        item.artifact_id,
                        item.relationship,
                        item.artifact_sha256,
                    ),
                )
            ),
            uncertainty=uncertainty,
            applicability=applicability,
            structural_fields=validate_structural_fields(structural_fields or {}),
        )

    def __post_init__(self) -> None:
        require_identifier(self.component_id, "component_id")
        require_identifier(self.ontology_term_id, "ontology_term_id")
        if not self.provenance:
            raise SpecimenInvalid("component provenance cannot be empty")
        field_names = tuple(name for name, _ in self.structural_fields)
        if len(field_names) != len(set(field_names)):
            raise SpecimenInvalid("component structural fields must be unique")
        if tuple(sorted(self.structural_fields)) != self.structural_fields:
            raise SpecimenInvalid("component structural fields must be canonical")
        if self.knowledge_status is KnowledgeStatus.HYPOTHESIS:
            raise ObservationContaminated(
                "a hypothesis cannot enter a syntax observation",
                component_id=self.component_id,
            )
        expected = {
            ObservationStatus.MEASURED: KnowledgeStatus.OBSERVATION,
            ObservationStatus.DETERMINISTICALLY_DERIVED: KnowledgeStatus.DETERMINISTIC_DERIVATION,
        }[self.observation_status]
        if self.applicability.status is ApplicabilityStatus.NOT_APPLICABLE:
            if (
                self.knowledge_status is not KnowledgeStatus.NOT_APPLICABLE
                or self.uncertainty.kind is not UncertaintyKind.NOT_APPLICABLE
            ):
                raise SpecimenInvalid(
                    "not-applicable components require explicit not-applicable knowledge and uncertainty"
                )
        elif self.knowledge_status is not expected:
            raise ObservationContaminated(
                "observation and knowledge statuses disagree",
                component_id=self.component_id,
            )


@dataclass(frozen=True, slots=True)
class SpecimenEvidence:
    specimen_id: str
    source: SourceReference
    category_id: str
    canvas_width_px: int
    canvas_height_px: int
    governed_status: GovernedStatus
    origin: EvidenceOrigin
    provenance: tuple[ProvenanceReference, ...]
    components: tuple[ComponentEvidence, ...]

    def __post_init__(self) -> None:
        require_identifier(self.specimen_id, "specimen_id")
        require_identifier(self.category_id, "category_id")
        if self.canvas_width_px <= 0 or self.canvas_height_px <= 0:
            raise SpecimenInvalid("specimen canvas dimensions must be positive")
        if self.governed_status is GovernedStatus.UNVERIFIED:
            raise SourceEvidenceInvalid(
                "unverified evidence cannot enter the governed offline normalization path",
                specimen_id=self.specimen_id,
            )
        if self.origin is EvidenceOrigin.PROVIDER_ONLY:
            raise ProviderOnlyClaimRejected(
                "provider-only output cannot become a governed syntax observation",
                specimen_id=self.specimen_id,
            )
        if not self.provenance or not self.components:
            raise SpecimenInvalid("specimen provenance and components are required")
        component_ids = tuple(item.component_id for item in self.components)
        if len(component_ids) != len(set(component_ids)):
            raise DuplicateInflationRejected(
                "duplicate component identities would inflate observation support",
                specimen_id=self.specimen_id,
            )


@dataclass(frozen=True, slots=True)
class NormalizationPolicy:
    policy_id: str
    version: str
    normalization_version: str
    allowed_categories: tuple[str, ...]
    ontology: SyntaxOntology

    def __post_init__(self) -> None:
        require_identifier(self.policy_id, "normalization_policy_id")
        require_identifier(self.version, "normalization_policy_version")
        require_identifier(self.normalization_version, "normalization_version")
        if not self.allowed_categories or len(set(self.allowed_categories)) != len(
            self.allowed_categories
        ):
            raise SyntaxContractError(
                "normalization policy categories must be non-empty and duplicate-free"
            )
        for category in self.allowed_categories:
            require_identifier(category, "allowed_category")

    @property
    def policy_sha256(self) -> str:
        return canonical_sha256(self.as_dict())

    def as_dict(self) -> dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "version": self.version,
            "normalization_version": self.normalization_version,
            "allowed_categories": list(sorted(self.allowed_categories)),
            "ontology_sha256": self.ontology.ontology_sha256,
        }


@dataclass(frozen=True, slots=True)
class SyntaxObservation:
    observation_id: str
    specimen_id: str
    component_id: str
    category_id: str
    ontology_term_id: str
    geometry: NormalizedBox
    observation_status: ObservationStatus
    governed_status: GovernedStatus
    knowledge_status: KnowledgeStatus
    source: SourceReference
    provenance: tuple[ProvenanceReference, ...]
    uncertainty: Uncertainty
    applicability: Applicability
    structural_fields: tuple[tuple[str, str | int | bool], ...]

    @classmethod
    def create(
        cls,
        *,
        specimen: SpecimenEvidence,
        component: ComponentEvidence,
        geometry: NormalizedBox,
    ) -> "SyntaxObservation":
        provenance = tuple(
            sorted(
                {*specimen.provenance, *component.provenance},
                key=lambda item: (
                    item.artifact_id,
                    item.relationship,
                    item.artifact_sha256,
                ),
            )
        )
        payload = {
            "specimen_id": specimen.specimen_id,
            "component_id": component.component_id,
            "category_id": specimen.category_id,
            "ontology_term_id": component.ontology_term_id,
            "geometry": geometry.as_dict(),
            "observation_status": component.observation_status.value,
            "governed_status": specimen.governed_status.value,
            "knowledge_status": component.knowledge_status.value,
            "source": specimen.source.as_dict(),
            "provenance": [item.as_dict() for item in provenance],
            "uncertainty": component.uncertainty.as_dict(),
            "applicability": component.applicability.as_dict(),
            "structural_fields": [list(item) for item in component.structural_fields],
        }
        return cls(
            observation_id=canonical_sha256(payload),
            specimen_id=specimen.specimen_id,
            component_id=component.component_id,
            category_id=specimen.category_id,
            ontology_term_id=component.ontology_term_id,
            geometry=geometry,
            observation_status=component.observation_status,
            governed_status=specimen.governed_status,
            knowledge_status=component.knowledge_status,
            source=specimen.source,
            provenance=provenance,
            uncertainty=component.uncertainty,
            applicability=component.applicability,
            structural_fields=component.structural_fields,
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "observation_id": self.observation_id,
            "specimen_id": self.specimen_id,
            "component_id": self.component_id,
            "category_id": self.category_id,
            "ontology_term_id": self.ontology_term_id,
            "geometry": self.geometry.as_dict(),
            "observation_status": self.observation_status.value,
            "governed_status": self.governed_status.value,
            "knowledge_status": self.knowledge_status.value,
            "source": self.source.as_dict(),
            "provenance": [item.as_dict() for item in self.provenance],
            "uncertainty": self.uncertainty.as_dict(),
            "applicability": self.applicability.as_dict(),
            "structural_fields": [list(item) for item in self.structural_fields],
        }

@dataclass(frozen=True, slots=True)
class NormalizedSpecimen:
    specimen_id: str
    source: SourceReference
    category_id: str
    normalization_version: str
    ontology_sha256: str
    observations: tuple[SyntaxObservation, ...]
    structural_fingerprint: str
    artifact_sha256: str

    def as_dict(self) -> dict[str, object]:
        return {
            "specimen_id": self.specimen_id,
            "source": self.source.as_dict(),
            "category_id": self.category_id,
            "normalization_version": self.normalization_version,
            "ontology_sha256": self.ontology_sha256,
            "observations": [item.as_dict() for item in self.observations],
            "structural_fingerprint": self.structural_fingerprint,
            "artifact_sha256": self.artifact_sha256,
        }


@dataclass(frozen=True, slots=True)
class DuplicateFinding:
    kind: DuplicateKind
    canonical_specimen_id: str
    related_specimen_id: str
    evidence_sha256: str
    contributes_to_support: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "kind": self.kind.value,
            "canonical_specimen_id": self.canonical_specimen_id,
            "related_specimen_id": self.related_specimen_id,
            "evidence_sha256": self.evidence_sha256,
            "contributes_to_support": self.contributes_to_support,
        }


@dataclass(frozen=True, slots=True)
class SyntaxNormalizationReceipt:
    receipt_id: str
    run_id: str
    result_sha256: str
    policy_sha256: str
    input_specimen_count: int
    accepted_specimen_count: int
    observation_count: int
    exact_duplicate_count: int
    near_duplicate_count: int
    grammar_support_count: int
    event_name: str = "ST-02.01:OutcomeVerified"
    story_id: str = STORY_ID
    development_mode: str = DEVELOPMENT_MODE
    evidence_gate_status: str = "EVIDENCE_PENDING"
    production_ready: bool = False
    certified: bool = False

    @property
    def receipt_sha256(self) -> str:
        return canonical_sha256(self.as_dict())

    def as_dict(self) -> dict[str, object]:
        return {
            "receipt_id": self.receipt_id,
            "run_id": self.run_id,
            "story_id": self.story_id,
            "development_mode": self.development_mode,
            "event_name": self.event_name,
            "result_sha256": self.result_sha256,
            "policy_sha256": self.policy_sha256,
            "input_specimen_count": self.input_specimen_count,
            "accepted_specimen_count": self.accepted_specimen_count,
            "observation_count": self.observation_count,
            "exact_duplicate_count": self.exact_duplicate_count,
            "near_duplicate_count": self.near_duplicate_count,
            "grammar_support_count": self.grammar_support_count,
            "evidence_gate_status": self.evidence_gate_status,
            "production_ready": self.production_ready,
            "certified": self.certified,
        }


@dataclass(frozen=True, slots=True)
class SyntaxNormalizationResult:
    specimens: tuple[NormalizedSpecimen, ...]
    duplicates: tuple[DuplicateFinding, ...]
    support_specimen_ids: tuple[str, ...]
    result_sha256: str
    receipt: SyntaxNormalizationReceipt

    def as_dict(self) -> dict[str, object]:
        return {
            "specimens": [item.as_dict() for item in self.specimens],
            "duplicates": [item.as_dict() for item in self.duplicates],
            "support_specimen_ids": list(self.support_specimen_ids),
            "result_sha256": self.result_sha256,
            "receipt": self.receipt.as_dict(),
        }


def _normalized_specimen(
    specimen: SpecimenEvidence, policy: NormalizationPolicy
) -> NormalizedSpecimen:
    if specimen.category_id not in policy.allowed_categories:
        raise SpecimenInvalid(
            "specimen category is outside the governed normalization policy",
            category_id=specimen.category_id,
        )
    observations: list[SyntaxObservation] = []
    structure: list[dict[str, object]] = []
    for component in sorted(specimen.components, key=lambda item: item.component_id):
        policy.ontology.require_term(component.ontology_term_id, specimen.category_id)
        geometry = normalize_box(
            component.pixel_box,
            canvas_width=specimen.canvas_width_px,
            canvas_height=specimen.canvas_height_px,
        )
        observation = SyntaxObservation.create(
            specimen=specimen,
            component=component,
            geometry=geometry,
        )
        observations.append(observation)
        structure.append(
            {
                "ontology_term_id": component.ontology_term_id,
                "geometry": geometry.as_dict(),
                "observation_status": component.observation_status.value,
                "knowledge_status": component.knowledge_status.value,
                "applicability": component.applicability.as_dict(),
                "structural_fields": [list(item) for item in component.structural_fields],
            }
        )
    structural_fingerprint = canonical_sha256(
        {"category_id": specimen.category_id, "components": structure}
    )
    artifact_payload = {
        "specimen_id": specimen.specimen_id,
        "source": specimen.source.as_dict(),
        "category_id": specimen.category_id,
        "normalization_version": policy.normalization_version,
        "ontology_sha256": policy.ontology.ontology_sha256,
        "observations": [item.as_dict() for item in observations],
        "structural_fingerprint": structural_fingerprint,
    }
    return NormalizedSpecimen(
        specimen_id=specimen.specimen_id,
        source=specimen.source,
        category_id=specimen.category_id,
        normalization_version=policy.normalization_version,
        ontology_sha256=policy.ontology.ontology_sha256,
        observations=tuple(observations),
        structural_fingerprint=structural_fingerprint,
        artifact_sha256=canonical_sha256(artifact_payload),
    )


def normalize_evidence(
    *,
    run_id: str,
    specimens: Sequence[SpecimenEvidence],
    policy: NormalizationPolicy,
) -> SyntaxNormalizationResult:
    require_identifier(run_id, "run_id")
    ordered_inputs = tuple(sorted(specimens, key=lambda item: item.specimen_id))
    if not ordered_inputs:
        raise SpecimenInvalid("at least one governed specimen is required")
    specimen_ids = tuple(item.specimen_id for item in ordered_inputs)
    if len(specimen_ids) != len(set(specimen_ids)):
        raise DuplicateInflationRejected(
            "specimen identities must be unique before normalization"
        )

    accepted: list[NormalizedSpecimen] = []
    duplicates: list[DuplicateFinding] = []
    source_hash_owner: dict[str, str] = {}
    structure_owner: dict[str, str] = {}
    support_ids: list[str] = []

    for specimen in ordered_inputs:
        # Validate and normalize every governed input before duplicate suppression.
        # A repeated source hash must never become a path around ontology, geometry,
        # applicability, or contamination checks.
        normalized = _normalized_specimen(specimen, policy)
        existing_source = source_hash_owner.get(specimen.source.content_sha256)
        if existing_source is not None:
            duplicates.append(
                DuplicateFinding(
                    kind=DuplicateKind.EXACT_SOURCE_HASH,
                    canonical_specimen_id=existing_source,
                    related_specimen_id=specimen.specimen_id,
                    evidence_sha256=specimen.source.content_sha256,
                    contributes_to_support=False,
                )
            )
            continue
        source_hash_owner[specimen.source.content_sha256] = specimen.specimen_id
        existing_structure = structure_owner.get(normalized.structural_fingerprint)
        if existing_structure is None:
            structure_owner[normalized.structural_fingerprint] = specimen.specimen_id
            support_ids.append(specimen.specimen_id)
        else:
            duplicates.append(
                DuplicateFinding(
                    kind=DuplicateKind.NEAR_DUPLICATE_STRUCTURE,
                    canonical_specimen_id=existing_structure,
                    related_specimen_id=specimen.specimen_id,
                    evidence_sha256=normalized.structural_fingerprint,
                    contributes_to_support=False,
                )
            )
        accepted.append(normalized)

    duplicate_order = tuple(
        sorted(
            duplicates,
            key=lambda item: (
                item.kind.value,
                item.canonical_specimen_id,
                item.related_specimen_id,
            ),
        )
    )
    result_core = {
        "run_id": run_id,
        "story_id": STORY_ID,
        "development_mode": DEVELOPMENT_MODE,
        "policy_sha256": policy.policy_sha256,
        "specimens": [item.as_dict() for item in accepted],
        "duplicates": [item.as_dict() for item in duplicate_order],
        "support_specimen_ids": support_ids,
        "evidence_gate_status": "EVIDENCE_PENDING",
        "production_ready": False,
        "certified": False,
    }
    result_sha256 = canonical_sha256(result_core)
    exact_count = sum(
        finding.kind is DuplicateKind.EXACT_SOURCE_HASH for finding in duplicate_order
    )
    near_count = sum(
        finding.kind is DuplicateKind.NEAR_DUPLICATE_STRUCTURE for finding in duplicate_order
    )
    receipt = SyntaxNormalizationReceipt(
        receipt_id=f"ST-02.01:OfflineNormalization:{result_sha256}",
        run_id=run_id,
        result_sha256=result_sha256,
        policy_sha256=policy.policy_sha256,
        input_specimen_count=len(ordered_inputs),
        accepted_specimen_count=len(accepted),
        observation_count=sum(len(item.observations) for item in accepted),
        exact_duplicate_count=exact_count,
        near_duplicate_count=near_count,
        grammar_support_count=len(support_ids),
    )
    return SyntaxNormalizationResult(
        specimens=tuple(accepted),
        duplicates=duplicate_order,
        support_specimen_ids=tuple(support_ids),
        result_sha256=result_sha256,
        receipt=receipt,
    )
