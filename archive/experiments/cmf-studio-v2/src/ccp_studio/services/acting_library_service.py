"""64-state acting library service for TS-CMF-019."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.acting_library import (
    ActingLibraryAction,
    ActingLibraryVersion,
    ActingProviderReceipt,
    ActingReference,
    ActingReferenceEvaluation,
    ActingReferenceStatus,
    ActingStateCell,
    acting_library_version_hash,
    acting_reference_content_hash,
    acting_state_matrix,
    new_acting_library_receipt,
    new_acting_library_version,
)
from ccp_studio.contracts.brand_genesis import BrandGenesisSessionStatus
from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.acting_library import InMemoryActingLibraryRepository
from ccp_studio.repositories.brand_genesis_sessions import InMemoryBrandGenesisRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.image_critic_service import ImageCriticService


class ActingLibraryServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ActingLibraryService:
    brand_genesis_repository: InMemoryBrandGenesisRepository
    repository: InMemoryActingLibraryRepository = field(default_factory=InMemoryActingLibraryRepository)
    image_critic: ImageCriticService = field(default_factory=ImageCriticService)

    def generate_reference_grid(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
        source_artifact_ids: list[UUID],
        provider_name: str,
    ) -> ActingLibraryVersion:
        self._require_brand_genesis_session(organization_id, brand_id, brand_genesis_session_id)
        if not source_artifact_ids:
            raise ActingLibraryServiceError("BRAND_SOURCE_REQUIRED", "Acting references require source artifacts.")
        version = new_acting_library_version(
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=brand_genesis_session_id,
        )
        self.repository.put_version(version)
        reference_ids: list[UUID] = []
        for cell in acting_state_matrix():
            reference = self._create_generated_reference(
                organization_id=organization_id,
                brand_id=brand_id,
                brand_genesis_session_id=brand_genesis_session_id,
                acting_library_version_id=version.acting_library_version_id,
                source_artifact_ids=source_artifact_ids,
                provider_name=provider_name,
                cell=cell,
            )
            reference_ids.append(reference.acting_reference_id)
        updated = version.model_copy(update={"acting_reference_ids": reference_ids, "updated_at": utc_now()})
        self.repository.put_version(updated)
        self.repository.put_receipt(
            new_acting_library_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                brand_genesis_session_id=brand_genesis_session_id,
                acting_library_version_id=version.acting_library_version_id,
                action=ActingLibraryAction.generated,
                decision_code="ACTING_REFERENCE_GRID_GENERATED",
                evidence_refs=[str(item) for item in reference_ids],
            )
        )
        return updated

    def evaluate_reference(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        acting_reference_id: UUID,
        likeness_score: float,
        gesture_clarity_score: float,
        hand_quality_score: float,
        paper_texture_score: float,
        style_adherence_score: float,
        negative_space_score: float,
        production_usability_score: float,
        failure_notes: list[str] | None = None,
    ) -> ActingReference:
        reference = self._reference_for_brand(organization_id, brand_id, acting_reference_id)
        self._reject_locked_reference(reference)
        evaluation = self.image_critic.evaluate_acting_reference(
            acting_reference_id=acting_reference_id,
            likeness_score=likeness_score,
            gesture_clarity_score=gesture_clarity_score,
            hand_quality_score=hand_quality_score,
            paper_texture_score=paper_texture_score,
            style_adherence_score=style_adherence_score,
            negative_space_score=negative_space_score,
            production_usability_score=production_usability_score,
            failure_notes=failure_notes,
        )
        self.repository.put_evaluation(evaluation)
        updated = reference.model_copy(update={"latest_evaluation": evaluation, "updated_at": utc_now()})
        self.repository.put_reference(updated)
        self.repository.put_receipt(
            new_acting_library_receipt(
                organization_id=reference.organization_id,
                brand_id=reference.brand_id,
                brand_genesis_session_id=reference.brand_genesis_session_id,
                acting_library_version_id=reference.acting_library_version_id,
                acting_reference_id=reference.acting_reference_id,
                action=ActingLibraryAction.evaluated,
                decision_code="ACTING_REFERENCE_EVALUATED",
                evidence_refs=[str(evaluation.evaluation_receipt_id)],
            )
        )
        return updated

    def approve_reference(self, *, organization_id: UUID, brand_id: UUID, acting_reference_id: UUID) -> ActingReference:
        reference = self._reference_for_brand(organization_id, brand_id, acting_reference_id)
        self._reject_locked_reference(reference)
        if reference.provider_receipt_id not in self.repository.provider_receipts:
            raise ActingLibraryServiceError("PROVIDER_RECEIPT_REQUIRED", "Provider receipt is required.")
        if reference.latest_evaluation is None:
            raise ActingLibraryServiceError("EVALUATION_RECEIPT_REQUIRED", "Evaluation receipt is required.")
        if not reference.latest_evaluation.passed(self.image_critic.threshold):
            raise ActingLibraryServiceError(
                "ACTING_REFERENCE_EVALUATION_FAILED",
                "Acting reference failed likeness, gesture, hands, style, negative-space, or usability gate.",
            )
        approved = reference.model_copy(update={"status": ActingReferenceStatus.approved, "updated_at": utc_now()})
        self.repository.put_reference(approved)
        self.repository.put_receipt(
            new_acting_library_receipt(
                organization_id=approved.organization_id,
                brand_id=approved.brand_id,
                brand_genesis_session_id=approved.brand_genesis_session_id,
                acting_library_version_id=approved.acting_library_version_id,
                acting_reference_id=approved.acting_reference_id,
                action=ActingLibraryAction.approved,
                decision_code="ACTING_REFERENCE_APPROVED",
                evidence_refs=[str(approved.latest_evaluation.evaluation_receipt_id)],
            )
        )
        return approved

    def reject_reference(self, *, organization_id: UUID, brand_id: UUID, acting_reference_id: UUID, reason: str) -> ActingReference:
        reference = self._reference_for_brand(organization_id, brand_id, acting_reference_id)
        self._reject_locked_reference(reference)
        rejected = reference.model_copy(update={"status": ActingReferenceStatus.rejected, "updated_at": utc_now()})
        self.repository.put_reference(rejected)
        self.repository.put_receipt(
            new_acting_library_receipt(
                organization_id=rejected.organization_id,
                brand_id=rejected.brand_id,
                brand_genesis_session_id=rejected.brand_genesis_session_id,
                acting_library_version_id=rejected.acting_library_version_id,
                acting_reference_id=rejected.acting_reference_id,
                action=ActingLibraryAction.rejected,
                decision_code="ACTING_REFERENCE_REJECTED",
                evidence_refs=[reason],
            )
        )
        return rejected

    def request_repair(self, *, organization_id: UUID, brand_id: UUID, acting_reference_id: UUID, instructions: str) -> ActingReference:
        reference = self._reference_for_brand(organization_id, brand_id, acting_reference_id)
        self._reject_locked_reference(reference)
        repaired = reference.model_copy(update={"status": ActingReferenceStatus.repair_requested, "updated_at": utc_now()})
        self.repository.put_reference(repaired)
        self.repository.put_receipt(
            new_acting_library_receipt(
                organization_id=repaired.organization_id,
                brand_id=repaired.brand_id,
                brand_genesis_session_id=repaired.brand_genesis_session_id,
                acting_library_version_id=repaired.acting_library_version_id,
                acting_reference_id=repaired.acting_reference_id,
                action=ActingLibraryAction.repair_requested,
                decision_code="ACTING_REFERENCE_REPAIR_REQUESTED",
                evidence_refs=[instructions],
            )
        )
        return repaired

    def replace_reference(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        acting_reference_id: UUID,
        provider_name: str,
    ) -> ActingReference:
        reference = self._reference_for_brand(organization_id, brand_id, acting_reference_id)
        self._reject_locked_reference(reference)
        replacement = self._create_generated_reference(
            organization_id=reference.organization_id,
            brand_id=reference.brand_id,
            brand_genesis_session_id=reference.brand_genesis_session_id,
            acting_library_version_id=reference.acting_library_version_id,
            source_artifact_ids=reference.source_artifact_ids,
            provider_name=provider_name,
            cell=reference.state_cell,
            replaces_reference_id=reference.acting_reference_id,
        )
        replaced = reference.model_copy(update={"status": ActingReferenceStatus.replaced, "updated_at": utc_now()})
        self.repository.put_reference(replaced)
        version = self._version(reference.acting_library_version_id)
        reference_ids = [
            replacement.acting_reference_id if item == reference.acting_reference_id else item
            for item in version.acting_reference_ids
        ]
        self.repository.put_version(version.model_copy(update={"acting_reference_ids": reference_ids, "updated_at": utc_now()}))
        self.repository.put_receipt(
            new_acting_library_receipt(
                organization_id=replacement.organization_id,
                brand_id=replacement.brand_id,
                brand_genesis_session_id=replacement.brand_genesis_session_id,
                acting_library_version_id=replacement.acting_library_version_id,
                acting_reference_id=replacement.acting_reference_id,
                action=ActingLibraryAction.replaced,
                decision_code="ACTING_REFERENCE_REPLACED",
                evidence_refs=[str(reference.acting_reference_id)],
            )
        )
        return replacement

    def lock_library_version(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        acting_library_version_id: UUID,
    ) -> ActingLibraryVersion:
        version = self._version_for_brand(organization_id, brand_id, acting_library_version_id)
        if version.locked:
            return version
        references = [self.repository.references[item] for item in version.acting_reference_ids]
        if len(references) != 64:
            raise ActingLibraryServiceError("ACTING_LIBRARY_INCOMPLETE", "The 64-state acting library requires all 64 references.")
        not_approved = [reference for reference in references if reference.status != ActingReferenceStatus.approved]
        if not_approved:
            raise ActingLibraryServiceError("ACTING_REFERENCE_NOT_APPROVED", "All acting references must be approved before lock.")
        locked_references = []
        for reference in references:
            locked = reference.model_copy(update={"status": ActingReferenceStatus.locked, "updated_at": utc_now()})
            locked_references.append(self.repository.put_reference(locked))
        locked_version = version.model_copy(
            update={
                "version_hash": acting_library_version_hash(locked_references),
                "locked": True,
                "locked_at": utc_now(),
                "updated_at": utc_now(),
            }
        )
        self.repository.put_version(locked_version)
        self.repository.put_receipt(
            new_acting_library_receipt(
                organization_id=locked_version.organization_id,
                brand_id=locked_version.brand_id,
                brand_genesis_session_id=locked_version.brand_genesis_session_id,
                acting_library_version_id=locked_version.acting_library_version_id,
                action=ActingLibraryAction.locked,
                decision_code="ACTING_LIBRARY_VERSION_LOCKED",
                evidence_refs=[locked_version.version_hash],
            )
        )
        return locked_version

    def assert_reference_selectable_for_scenespec(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        acting_library_version_id: UUID,
        acting_reference_id: UUID,
    ) -> ActingReference:
        version = self._version_for_brand(organization_id, brand_id, acting_library_version_id)
        if not version.locked:
            raise ActingLibraryServiceError("ACTING_LIBRARY_VERSION_NOT_LOCKED", "SceneSpec requires a locked acting library.")
        reference = self._reference_for_brand(organization_id, brand_id, acting_reference_id)
        if reference.acting_reference_id not in version.acting_reference_ids:
            raise ActingLibraryServiceError("ACTING_REFERENCE_NOT_IN_VERSION", "Reference does not belong to library version.")
        if reference.status != ActingReferenceStatus.locked:
            raise ActingLibraryServiceError("ACTING_REFERENCE_NOT_APPROVED", "SceneSpec requires an approved locked reference.")
        return reference

    def _create_generated_reference(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
        acting_library_version_id: UUID,
        source_artifact_ids: list[UUID],
        provider_name: str,
        cell: ActingStateCell,
        replaces_reference_id: UUID | None = None,
    ) -> ActingReference:
        if not provider_name:
            raise ActingLibraryServiceError("PROVIDER_RECEIPT_REQUIRED", "Provider receipt is required.")
        reference_id = uuid4()
        artifact_uri = f"brands/{brand_id}/brand-genesis/{brand_genesis_session_id}/acting_library/{cell.state_key}/{reference_id}.png"
        request_hash = acting_reference_content_hash(
            [str(brand_id), str(brand_genesis_session_id), cell.state_key, provider_name, *[str(item) for item in source_artifact_ids]]
        )
        provider_receipt = ActingProviderReceipt(
            schema_version="cmf.acting_provider_receipt.v1",
            provider_receipt_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=brand_genesis_session_id,
            provider_name=provider_name,
            request_hash=request_hash,
            artifact_uri=artifact_uri,
            source_artifact_ids=source_artifact_ids,
            written_at=utc_now(),
        )
        self.repository.put_provider_receipt(provider_receipt)
        reference = ActingReference(
            schema_version="cmf.acting_reference.v1",
            acting_reference_id=reference_id,
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=brand_genesis_session_id,
            acting_library_version_id=acting_library_version_id,
            state_cell=cell,
            source_artifact_ids=source_artifact_ids,
            provider_receipt_id=provider_receipt.provider_receipt_id,
            artifact_uri=artifact_uri,
            content_hash=acting_reference_content_hash([artifact_uri, request_hash]),
            body_language=cell.gesture_family.value,
            facial_expression=cell.emotional_family.value,
            energy_level="medium_high" if cell.emotional_family.value in {"confident", "urgent", "celebratory"} else "medium",
            framing="medium_shot",
            orientation="front_3_4",
            layout_bias="right_side_subject",
            status=ActingReferenceStatus.generated,
            replaces_reference_id=replaces_reference_id,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        return self.repository.put_reference(reference)

    def _require_brand_genesis_session(self, organization_id: UUID, brand_id: UUID, session_id: UUID) -> None:
        session = self.brand_genesis_repository.get_session_for_brand(
            organization_id=organization_id,
            brand_id=brand_id,
            session_id=session_id,
        )
        if session is None:
            raise ActingLibraryServiceError("BRAND_GENESIS_SESSION_REQUIRED", "Brand Genesis session is required.")
        if session.status not in {BrandGenesisSessionStatus.ready, BrandGenesisSessionStatus.running, BrandGenesisSessionStatus.completed}:
            raise ActingLibraryServiceError("BRAND_GENESIS_SESSION_NOT_READY", "Brand Genesis session must pass intake before acting generation.")

    def _reference_for_brand(self, organization_id: UUID, brand_id: UUID, reference_id: UUID) -> ActingReference:
        reference = self.repository.references.get(reference_id)
        if reference is None:
            raise ActingLibraryServiceError("ACTING_REFERENCE_REQUIRED", "Acting reference is required.")
        if reference.organization_id != organization_id or reference.brand_id != brand_id:
            raise ActingLibraryServiceError("BRAND_SCOPE_VIOLATION", "Acting reference is outside the active brand scope.")
        return reference

    def _version_for_brand(self, organization_id: UUID, brand_id: UUID, version_id: UUID) -> ActingLibraryVersion:
        version = self.repository.versions.get(version_id)
        if version is None:
            raise ActingLibraryServiceError("ACTING_LIBRARY_VERSION_REQUIRED", "Acting library version is required.")
        if version.organization_id != organization_id or version.brand_id != brand_id:
            raise ActingLibraryServiceError("BRAND_SCOPE_VIOLATION", "Acting library version is outside the active brand scope.")
        return version

    def _version(self, version_id: UUID | None) -> ActingLibraryVersion:
        if version_id is None or version_id not in self.repository.versions:
            raise ActingLibraryServiceError("ACTING_LIBRARY_VERSION_REQUIRED", "Acting library version is required.")
        return self.repository.versions[version_id]

    @staticmethod
    def _reject_locked_reference(reference: ActingReference) -> None:
        if reference.status == ActingReferenceStatus.locked:
            raise ActingLibraryServiceError("ACTING_LIBRARY_VERSION_IMMUTABLE", "Locked acting references are immutable.")


@dataclass
class ActingLibraryCommandHandler:
    command_type: str
    service: ActingLibraryService
    aggregate_type: str = "acting_library"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "GenerateActingReferenceGridCommand":
            version = self.service.generate_reference_grid(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                brand_genesis_session_id=UUID(payload["brand_genesis_session_id"]),
                source_artifact_ids=[UUID(item) for item in payload["source_artifact_ids"]],
                provider_name=payload["provider_name"],
            )
            return version.model_dump(mode="json")
        if self.command_type == "ApproveActingReferenceCommand":
            return self.service.approve_reference(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                acting_reference_id=UUID(payload["acting_reference_id"]),
            ).model_dump(mode="json")
        if self.command_type == "LockActingLibraryVersionCommand":
            return self.service.lock_library_version(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                acting_library_version_id=UUID(payload["acting_library_version_id"]),
            ).model_dump(mode="json")
        raise ActingLibraryServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("acting_library_version_id") or payload.get("acting_reference_id")
        if isinstance(raw, str):
            return UUID(raw)
        return envelope.brand_id


def register_acting_library_command_handlers(bus: CommandBus, service: ActingLibraryService) -> None:
    for command_type in [
        "GenerateActingReferenceGridCommand",
        "ApproveActingReferenceCommand",
        "LockActingLibraryVersionCommand",
    ]:
        bus.register_handler(ActingLibraryCommandHandler(command_type=command_type, service=service))
