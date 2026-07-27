"""Revision and reconstruction audit service for TS-CMF-040."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.revision import (
    FinalApprovalBinding,
    ReconstructionAuditView,
    RevisionChain,
    RevisionDelta,
    RevisionLineageRefs,
    RevisionReceipt,
    RevisionRequest,
    RevisionVersion,
    new_revision_receipt,
    revision_hash,
)
from ccp_studio.repositories.revision import InMemoryRevisionRepository
from ccp_studio.services.assembly_planner import AssemblyPlanner
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.complete_editing_session_service import CompleteEditingSessionService
from ccp_studio.services.composition_service import CompositionService
from ccp_studio.services.scene_spec_compiler import SceneSpecCompiler


LINEAGE_FIELD_PATHS = {
    "source_expression_moment_id",
    "asset_route_receipt_id",
    "brand_context_version_id",
    "lineage_refs",
    "composition_job_ids",
    "provider_receipt_ids",
    "render_manifest_ids",
}


class RevisionServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class RevisionService:
    editing_session_service: CompleteEditingSessionService
    scene_spec_compiler: SceneSpecCompiler
    composition_service: CompositionService
    assembly_planner: AssemblyPlanner
    repository: InMemoryRevisionRepository = field(default_factory=InMemoryRevisionRepository)

    def request_scene_revision(
        self,
        *,
        complete_editing_session_id: UUID,
        requested_by_user_id: UUID,
        reason: str,
        target_object_type: str,
        target_object_id: UUID,
        deltas: list[RevisionDelta | dict[str, Any]],
        prior_version_id: UUID,
        evaluation_state: str = "reviewed_for_revision",
        evaluation_receipt_ids: list[UUID] | None = None,
        command_id: UUID | None = None,
    ) -> RevisionRequest:
        parsed_deltas = [item if isinstance(item, RevisionDelta) else RevisionDelta(**item) for item in deltas]
        session = self._session(complete_editing_session_id)
        lineage = self._lineage_refs(complete_editing_session_id, evaluation_receipt_ids=evaluation_receipt_ids)
        try:
            self.validate_revision_lineage(deltas=parsed_deltas, lineage_refs=lineage)
        except RevisionServiceError as exc:
            self._blocked_receipt(session.organization_id, session.brand_id, requested_by_user_id, complete_editing_session_id, exc.code, command_id)
            raise
        request = RevisionRequest(
            schema_version="cmf.revision_request.v1",
            revision_request_id=uuid4(),
            complete_editing_session_id=complete_editing_session_id,
            requested_by_user_id=requested_by_user_id,
            reason=reason,
            target_object_type=target_object_type,
            target_object_id=target_object_id,
            deltas=parsed_deltas,
            prior_version_id=prior_version_id,
            lineage_refs=lineage,
            evaluation_state=evaluation_state,
            created_at=utc_now(),
        )
        self.repository.put_revision_request(request)
        version = self.apply_revision(revision_request_id=request.revision_request_id, actor_id=requested_by_user_id)
        receipt = self.repository.put_receipt(
            new_revision_receipt(
                organization_id=session.organization_id,
                brand_id=session.brand_id,
                actor_id=requested_by_user_id,
                complete_editing_session_id=complete_editing_session_id,
                revision_request_id=request.revision_request_id,
                prior_version_id=prior_version_id,
                new_version_id=version.revision_version_id,
                target_object_type=target_object_type,
                target_object_id=target_object_id,
                deltas=parsed_deltas,
                lineage_refs=lineage,
                evaluation_state=evaluation_state,
                decision_code="REVISION_REQUESTED",
                evidence_refs=[
                    reason,
                    f"prior_version:{prior_version_id}",
                    f"new_version:{version.revision_version_id}",
                    *[str(item) for item in lineage.provider_receipt_ids],
                    *[str(item) for item in lineage.render_manifest_ids],
                ],
                command_id=command_id,
            )
        )
        lineage = lineage.model_copy(update={"revision_receipt_ids": [*lineage.revision_receipt_ids, receipt.revision_receipt_id]})
        request = request.model_copy(update={"lineage_refs": lineage})
        version = version.model_copy(update={"lineage_refs": lineage})
        self.repository.put_revision_request(request)
        self.repository.put_revision_version(version)
        self._upsert_chain(request, version, receipt.revision_receipt_id)
        return request

    def validate_revision_lineage(self, *, deltas: list[RevisionDelta], lineage_refs: RevisionLineageRefs) -> bool:
        if not lineage_refs.source_expression_moment_id or not lineage_refs.asset_route_receipt_id or not lineage_refs.brand_context_version_id:
            raise RevisionServiceError("LINEAGE_REQUIRED", "Revision lineage must preserve source, route, and Brand Context.")
        for delta in deltas:
            field = delta.field_path.split(".")[-1]
            if field in LINEAGE_FIELD_PATHS and delta.new_value_hash.lower() in {"drop", "null", "none", "empty", "sha256-null"}:
                raise RevisionServiceError("LINEAGE_DROPPING_REVISION_BLOCKED", "Revision cannot drop source, route, context, composition, provider, or manifest lineage.")
        return True

    def apply_revision(self, *, revision_request_id: UUID, actor_id: UUID) -> RevisionVersion:
        request = self.repository.revision_requests.get(revision_request_id)
        if request is None:
            raise RevisionServiceError("REVISION_REQUEST_REQUIRED", "Revision request is required.")
        version = RevisionVersion(
            schema_version="cmf.revision_version.v1",
            revision_version_id=uuid4(),
            revision_request_id=request.revision_request_id,
            complete_editing_session_id=request.complete_editing_session_id,
            target_object_type=request.target_object_type,
            target_object_id=request.target_object_id,
            prior_version_id=request.prior_version_id,
            version_hash=revision_hash(
                {
                    "revision_request_id": request.revision_request_id,
                    "target_object_id": request.target_object_id,
                    "deltas": [item.model_dump(mode="json") for item in request.deltas],
                    "lineage": request.lineage_refs.model_dump(mode="json"),
                }
            ),
            lineage_refs=request.lineage_refs,
            created_at=utc_now(),
        )
        return self.repository.put_revision_version(version)

    def approve_final_version(
        self,
        *,
        complete_editing_session_id: UUID,
        final_version_id: UUID,
        approved_by_actor_id: UUID,
        human_decision_ref: str,
        command_id: UUID | None = None,
    ) -> FinalApprovalBinding:
        session = self._session(complete_editing_session_id)
        version = self.repository.revision_versions.get(final_version_id)
        if version is None or version.complete_editing_session_id != complete_editing_session_id:
            raise RevisionServiceError("FINAL_VERSION_REQUIRED", "Final approval must reference a revision version in this session.")
        chain = self._chain_for_version(version)
        binding = self.repository.put_approval_binding(
            FinalApprovalBinding(
                schema_version="cmf.final_approval_binding.v1",
                final_approval_binding_id=uuid4(),
                complete_editing_session_id=complete_editing_session_id,
                final_version_id=final_version_id,
                revision_chain_id=chain.revision_chain_id,
                prior_version_ids=[item for item in chain.version_ids if item != final_version_id],
                approved_by_actor_id=approved_by_actor_id,
                human_decision_ref=human_decision_ref,
                approved_at=utc_now(),
            )
        )
        self.repository.put_receipt(
            new_revision_receipt(
                organization_id=session.organization_id,
                brand_id=session.brand_id,
                actor_id=approved_by_actor_id,
                complete_editing_session_id=complete_editing_session_id,
                new_version_id=final_version_id,
                lineage_refs=version.lineage_refs.model_copy(update={"approval_event_ids": [binding.final_approval_binding_id]}),
                approval_binding_id=binding.final_approval_binding_id,
                decision_code="FINAL_VERSION_APPROVED",
                evidence_refs=[human_decision_ref, f"revision_chain:{chain.revision_chain_id}", f"final_version:{final_version_id}"],
                command_id=command_id,
            )
        )
        return binding

    def build_reconstruction_audit_view(self, *, complete_editing_session_id: UUID, actor_id: UUID | None = None, command_id: UUID | None = None) -> ReconstructionAuditView:
        session = self._session(complete_editing_session_id)
        lineage = self._lineage_refs(complete_editing_session_id)
        versions = [
            item.revision_version_id
            for item in self.repository.revision_versions.values()
            if item.complete_editing_session_id == complete_editing_session_id
        ]
        approvals = [
            item.final_approval_binding_id
            for item in self.repository.approval_bindings.values()
            if item.complete_editing_session_id == complete_editing_session_id
        ]
        view = self.repository.put_audit_view(
            ReconstructionAuditView(
                schema_version="cmf.reconstruction_audit_view.v1",
                complete_editing_session_id=complete_editing_session_id,
                source_expression_moment_id=session.source_expression_moment_id,
                asset_route_receipt_id=session.asset_route_receipt_id,
                brand_context_version_id=session.brand_context_version_id,
                scene_spec_versions=[*lineage.scene_spec_ids, *versions],
                composition_job_ids=lineage.composition_job_ids,
                provider_job_ids=lineage.provider_receipt_ids,
                render_manifest_ids=lineage.render_manifest_ids,
                evaluation_receipt_ids=lineage.evaluation_receipt_ids,
                approval_event_ids=approvals,
                revision_receipt_ids=list(self.repository.receipts.keys()),
            )
        )
        if actor_id is not None:
            self.repository.put_receipt(
                new_revision_receipt(
                    organization_id=session.organization_id,
                    brand_id=session.brand_id,
                    actor_id=actor_id,
                    complete_editing_session_id=complete_editing_session_id,
                    lineage_refs=lineage,
                    decision_code="RECONSTRUCTION_AUDIT_VIEW_BUILT",
                    evidence_refs=[
                        f"source_expression_moment:{view.source_expression_moment_id}",
                        f"asset_route_receipt:{view.asset_route_receipt_id}",
                        f"brand_context_version:{view.brand_context_version_id}",
                    ],
                    command_id=command_id,
                )
            )
        return view

    def block_lineage_dropping_revision(
        self,
        *,
        complete_editing_session_id: UUID,
        actor_id: UUID,
        reason: str,
        command_id: UUID | None = None,
    ) -> RevisionReceipt:
        session = self._session(complete_editing_session_id)
        return self._blocked_receipt(session.organization_id, session.brand_id, actor_id, complete_editing_session_id, reason, command_id)

    def _lineage_refs(self, complete_editing_session_id: UUID, *, evaluation_receipt_ids: list[UUID] | None = None) -> RevisionLineageRefs:
        session = self._session(complete_editing_session_id)
        scene_specs = [
            item
            for item in self.scene_spec_compiler.repository.scene_specs.values()
            if item.complete_editing_session_id == complete_editing_session_id
        ]
        scene_spec_ids = [item.scene_spec_id for item in scene_specs]
        composition_jobs = [
            item
            for item in self.composition_service.repository.composition_jobs.values()
            if item.complete_editing_session_id == complete_editing_session_id
        ]
        provider_receipts = [
            receipt.provider_receipt_id
            for receipt in self.composition_service.repository.provider_receipts.values()
            if receipt.composition_job_id in {job.composition_job_id for job in composition_jobs}
        ]
        render_manifest_ids: list[UUID] = []
        for plan in self.assembly_planner.repository.assembly_plans.values():
            if plan.complete_editing_session_id == complete_editing_session_id:
                render_manifest_ids.extend(
                    [
                        plan.layer_manifest_id,
                        plan.animation_plan_id,
                        plan.edit_decision_list_id,
                        plan.timeline_manifest_id,
                        plan.caption_manifest_id,
                        plan.audio_mix_manifest_id,
                    ]
                )
        return RevisionLineageRefs(
            schema_version="cmf.revision_lineage_refs.v1",
            complete_editing_session_id=complete_editing_session_id,
            source_expression_moment_id=session.source_expression_moment_id,
            asset_route_receipt_id=session.asset_route_receipt_id,
            brand_context_version_id=session.brand_context_version_id,
            scene_spec_ids=scene_spec_ids,
            composition_job_ids=[item.composition_job_id for item in composition_jobs],
            provider_receipt_ids=provider_receipts,
            render_manifest_ids=render_manifest_ids,
            evaluation_receipt_ids=evaluation_receipt_ids or [],
            approval_event_ids=[item.final_approval_binding_id for item in self.repository.approval_bindings.values() if item.complete_editing_session_id == complete_editing_session_id],
            revision_receipt_ids=list(self.repository.receipts.keys()),
        )

    def _upsert_chain(self, request: RevisionRequest, version: RevisionVersion, receipt_id: UUID) -> RevisionChain:
        existing = next(
            (
                item
                for item in self.repository.revision_chains.values()
                if item.complete_editing_session_id == request.complete_editing_session_id
                and item.target_object_type == request.target_object_type
                and item.target_object_id == request.target_object_id
            ),
            None,
        )
        if existing is None:
            return self.repository.put_revision_chain(
                RevisionChain(
                    schema_version="cmf.revision_chain.v1",
                    revision_chain_id=uuid4(),
                    complete_editing_session_id=request.complete_editing_session_id,
                    target_object_type=request.target_object_type,
                    target_object_id=request.target_object_id,
                    version_ids=[request.prior_version_id, version.revision_version_id],
                    revision_request_ids=[request.revision_request_id],
                    revision_receipt_ids=[receipt_id],
                    updated_at=utc_now(),
                )
            )
        if version.revision_version_id not in existing.version_ids:
            existing = existing.model_copy(
                update={
                    "version_ids": [*existing.version_ids, version.revision_version_id],
                    "revision_request_ids": [*existing.revision_request_ids, request.revision_request_id],
                    "revision_receipt_ids": [*existing.revision_receipt_ids, receipt_id],
                    "updated_at": utc_now(),
                }
            )
        return self.repository.put_revision_chain(existing)

    def _chain_for_version(self, version: RevisionVersion) -> RevisionChain:
        chain = next((item for item in self.repository.revision_chains.values() if version.revision_version_id in item.version_ids), None)
        if chain is None:
            raise RevisionServiceError("REVISION_CHAIN_REQUIRED", "Revision chain is required for final approval.")
        return chain

    def _session(self, complete_editing_session_id: UUID):
        session = self.editing_session_service.repository.sessions.get(complete_editing_session_id)
        if session is None:
            raise RevisionServiceError("COMPLETE_EDITING_SESSION_REQUIRED", "Complete Editing Session is required.")
        return session

    def _blocked_receipt(self, organization_id: UUID, brand_id: UUID, actor_id: UUID, complete_editing_session_id: UUID, reason: str, command_id: UUID | None) -> RevisionReceipt:
        return self.repository.put_receipt(
            new_revision_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                actor_id=actor_id,
                complete_editing_session_id=complete_editing_session_id,
                decision_code="LINEAGE_DROPPING_REVISION_BLOCKED",
                evidence_refs=[reason],
                command_id=command_id,
            )
        )


@dataclass
class RevisionCommandHandler:
    command_type: str
    service: RevisionService
    aggregate_type: str = "revision"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "reviewer", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "RequestSceneRevisionCommand":
            return self.service.request_scene_revision(
                complete_editing_session_id=UUID(payload["complete_editing_session_id"]),
                requested_by_user_id=envelope.actor.actor_id,
                reason=payload["reason"],
                target_object_type=payload["target_object_type"],
                target_object_id=UUID(payload["target_object_id"]),
                deltas=payload["deltas"],
                prior_version_id=UUID(payload["prior_version_id"]),
                evaluation_state=payload.get("evaluation_state", "reviewed_for_revision"),
                evaluation_receipt_ids=[UUID(item) for item in payload.get("evaluation_receipt_ids", [])],
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "ValidateRevisionLineageCommand":
            lineage = self.service._lineage_refs(UUID(payload["complete_editing_session_id"]))
            self.service.validate_revision_lineage(deltas=[RevisionDelta(**item) for item in payload["deltas"]], lineage_refs=lineage)
            return {"validated": True, "complete_editing_session_id": payload["complete_editing_session_id"]}
        if self.command_type == "ApplyRevisionCommand":
            return self.service.apply_revision(
                revision_request_id=UUID(payload["revision_request_id"]),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "ApproveFinalVersionCommand":
            return self.service.approve_final_version(
                complete_editing_session_id=UUID(payload["complete_editing_session_id"]),
                final_version_id=UUID(payload["final_version_id"]),
                approved_by_actor_id=envelope.actor.actor_id,
                human_decision_ref=payload["human_decision_ref"],
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "BuildReconstructionAuditViewCommand":
            return self.service.build_reconstruction_audit_view(
                complete_editing_session_id=UUID(payload["complete_editing_session_id"]),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "BlockLineageDroppingRevisionCommand":
            return self.service.block_lineage_dropping_revision(
                complete_editing_session_id=UUID(payload["complete_editing_session_id"]),
                actor_id=envelope.actor.actor_id,
                reason=payload["reason"],
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        raise RevisionServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("revision_request_id") or payload.get("complete_editing_session_id") or payload.get("target_object_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_revision_command_handlers(bus: CommandBus, service: RevisionService) -> None:
    for command_type in [
        "RequestSceneRevisionCommand",
        "ValidateRevisionLineageCommand",
        "ApplyRevisionCommand",
        "ApproveFinalVersionCommand",
        "BuildReconstructionAuditViewCommand",
        "BlockLineageDroppingRevisionCommand",
    ]:
        bus.register_handler(RevisionCommandHandler(command_type=command_type, service=service))
