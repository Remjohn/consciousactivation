"""Evidence-rich review state service for TS-CMF-051."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.brand_context import BrandContextVersion
from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.consent import ConsentVersionStatus
from ccp_studio.contracts.evaluation_receipts import EvaluationReceipt, evidence_ref
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.review_evidence import (
    ApprovalBlockerCode,
    ApprovalEvidenceView,
    TranscriptRevisionSummary,
)
from ccp_studio.contracts.review_state import (
    ConsentCompatibilitySnapshot,
    EvaluationFailureView,
    EvidenceCompleteness,
    EvidencePanel,
    EvidencePanelType,
    ReviewEvidenceState,
    ReviewStateDomainEvent,
    ReviewStateReceipt,
    RevisionHistoryItem,
    TelegramComplexity,
    new_review_state_receipt,
)
from ccp_studio.contracts.revision import RevisionRequest, RevisionVersion
from ccp_studio.contracts.surfaces import DeepLinkTarget
from ccp_studio.repositories.brand_context_versions import InMemoryBrandContextRepository
from ccp_studio.repositories.consent_record_versions import InMemoryConsentRepository
from ccp_studio.repositories.evaluation_receipts import InMemoryEvaluationReceiptRepository
from ccp_studio.repositories.review_read_models import InMemoryReviewReadModelRepository
from ccp_studio.repositories.review_state import InMemoryReviewStateRepository
from ccp_studio.repositories.revision import InMemoryRevisionRepository
from ccp_studio.services.command_bus import CommandBus


class ReviewStateError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ReviewStateService:
    review_read_repository: InMemoryReviewReadModelRepository
    consent_repository: InMemoryConsentRepository | None = None
    evaluation_repository: InMemoryEvaluationReceiptRepository | None = None
    revision_repository: InMemoryRevisionRepository | None = None
    brand_context_repository: InMemoryBrandContextRepository | None = None
    repository: InMemoryReviewStateRepository = field(default_factory=InMemoryReviewStateRepository)
    telegram_complexity_threshold: int = 3

    def build_review_evidence_state(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        approval_evidence_view_id: UUID,
        actor_id: UUID,
        preview_ref: str | None = None,
        source_quote_ref: str | None = None,
        archetype_route_ref: str | None = None,
        brand_context_version_id: UUID | None = None,
        selected_asset_refs: list[str] | None = None,
        render_output_refs: list[str] | None = None,
        rendered_with_consent_record_version_id: UUID | None = None,
        telegram_complexity_score: int = 0,
        surface_route: str | None = None,
        command_id: UUID | None = None,
    ) -> ReviewEvidenceState:
        view = self._view(approval_evidence_view_id, organization_id, brand_id)
        selected_assets = selected_asset_refs or []
        render_outputs = render_output_refs or []
        evaluations = self._evaluation_receipts(view)
        brand_context = self._brand_context(organization_id, brand_id, brand_context_version_id)
        consent_snapshot = self._consent_snapshot(view, rendered_with_consent_record_version_id)
        revision_history = self._revision_history(view.object_type, view.object_id)
        evaluation_failures = self._evaluation_failures(evaluations)
        route = surface_route or f"/brands/{brand_id}/review/{view.object_type}/{view.object_id}"
        panels = self._panels(
            view=view,
            preview_ref=preview_ref,
            source_quote_ref=source_quote_ref,
            archetype_route_ref=archetype_route_ref,
            brand_context=brand_context,
            selected_asset_refs=selected_assets,
            render_output_refs=render_outputs,
            evaluations=evaluations,
            revision_history=revision_history,
            consent_snapshot=consent_snapshot,
        )
        telegram_complexity = self._telegram_complexity(
            panels=panels,
            evaluation_failures=evaluation_failures,
            telegram_complexity_score=telegram_complexity_score,
        )
        deep_link = self.create_pwa_review_deep_link(
            organization_id=organization_id,
            brand_id=brand_id,
            object_type=view.object_type,
            object_id=view.object_id,
            route=route,
            required_reason="PWA_REVIEW_REQUIRED",
        ) if telegram_complexity == TelegramComplexity.pwa_required else None
        state = ReviewEvidenceState(
            schema_version="cmf.review_evidence_state.v1",
            review_state_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            object_type=view.object_type,
            object_id=view.object_id,
            approval_evidence_view_id=view.approval_evidence_view_id,
            panels=panels,
            evaluation_failures=evaluation_failures,
            revision_history=revision_history,
            consent_snapshot=consent_snapshot,
            brand_context_version_id=brand_context.brand_context_version_id if brand_context else brand_context_version_id,
            selected_asset_refs=selected_assets,
            render_output_refs=render_outputs,
            pwa_route=route,
            telegram_complexity=telegram_complexity,
            pwa_deep_link=deep_link,
            generated_at=utc_now(),
        )
        self.repository.put_state(state)
        receipt = self.repository.put_receipt(new_review_state_receipt(state=state, command_id=command_id))
        self._append_event(
            "ReviewEvidenceStateBuilt",
            state,
            {
                "review_state_receipt_id": str(receipt.review_state_receipt_id),
                "panel_completeness": receipt.panel_completeness,
            },
        )
        self._append_event(
            "ReviewStateReceiptRecorded",
            state,
            {"review_state_receipt_id": str(receipt.review_state_receipt_id)},
        )
        return state

    def expand_evaluation_failure(self, *, review_state_id: UUID, category: str) -> EvaluationFailureView:
        state = self.repository.states.get(review_state_id)
        if state is None:
            raise ReviewStateError("REVIEW_STATE_REQUIRED", "Review state is required.")
        failure = next((item for item in state.evaluation_failures if item.category == category), None)
        if failure is None:
            raise ReviewStateError("EVALUATION_FAILURE_REQUIRED", "Evaluation failure is required.")
        self._append_event(
            "EvaluationFailureExpanded",
            state,
            {"category": failure.category, "failure_code": failure.failure_code},
        )
        return failure

    def validate_review_evidence_completeness(self, review_state_id: UUID) -> dict[str, str]:
        state = self.repository.states.get(review_state_id)
        if state is None:
            raise ReviewStateError("REVIEW_STATE_REQUIRED", "Review state is required.")
        result = {panel.panel_type.value: panel.completeness.value for panel in state.panels}
        self._append_event("ReviewEvidenceCompletenessValidated", state, result)
        return result

    def create_pwa_review_deep_link(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        object_type: str,
        object_id: UUID,
        route: str,
        required_reason: str,
    ) -> DeepLinkTarget:
        link = DeepLinkTarget(
            schema_version="cmf.deep_link_target.v1",
            target_surface="pwa",
            route=route,
            object_type=object_type,
            object_id=object_id,
            brand_id=brand_id,
            required_reason=required_reason,
        )
        self.repository.append_event(
            ReviewStateDomainEvent(
                schema_version="cmf.review_state_domain_event.v1",
                review_state_event_id=uuid4(),
                event_type="PwaReviewDeepLinkCreated",
                object_type=object_type,
                object_id=object_id,
                payload={"organization_id": str(organization_id), "brand_id": str(brand_id), "route": route},
                created_at=utc_now(),
            )
        )
        return link

    def stage13_build_evidence_state(self, **kwargs: Any) -> ReviewEvidenceState:
        return self.build_review_evidence_state(**kwargs)

    def _view(self, approval_evidence_view_id: UUID, organization_id: UUID, brand_id: UUID) -> ApprovalEvidenceView:
        view = self.review_read_repository.evidence_views.get(approval_evidence_view_id)
        if view is None:
            raise ReviewStateError("APPROVAL_EVIDENCE_VIEW_REQUIRED", "Approval evidence view is required.")
        if view.organization_id != organization_id or view.brand_id != brand_id:
            raise ReviewStateError("BRAND_SCOPE_VIOLATION", "Review evidence state cannot cross organization or brand boundary.")
        return view

    def _evaluation_receipts(self, view: ApprovalEvidenceView) -> list[EvaluationReceipt]:
        if self.evaluation_repository is None:
            return []
        receipts: list[EvaluationReceipt] = []
        for evaluation_receipt_id in view.evaluation_receipt_ids:
            receipt = self.evaluation_repository.receipts.get(evaluation_receipt_id)
            if receipt is None:
                continue
            if receipt.organization_id != view.organization_id or receipt.brand_id != view.brand_id:
                raise ReviewStateError("BRAND_SCOPE_VIOLATION", "Evaluation receipt belongs to another organization or brand.")
            receipts.append(receipt)
        return receipts

    def _brand_context(
        self,
        organization_id: UUID,
        brand_id: UUID,
        brand_context_version_id: UUID | None,
    ) -> BrandContextVersion | None:
        if brand_context_version_id is None or self.brand_context_repository is None:
            return None
        version = self.brand_context_repository.versions.get(brand_context_version_id)
        if version is None:
            return None
        if version.organization_id != organization_id or version.brand_id != brand_id:
            raise ReviewStateError("BRAND_SCOPE_VIOLATION", "Brand Context version belongs to another organization or brand.")
        return version

    def _consent_snapshot(
        self,
        view: ApprovalEvidenceView,
        rendered_with_consent_record_version_id: UUID | None,
    ) -> ConsentCompatibilitySnapshot:
        version = self.consent_repository.versions.get(view.consent_record_version_id) if self.consent_repository else None
        status = version.status.value if version else "unknown"
        changed_after_render = (
            rendered_with_consent_record_version_id is not None
            and rendered_with_consent_record_version_id != view.consent_record_version_id
        )
        consent_blockers = [
            blocker.blocker_code.value
            for blocker in view.blockers
            if blocker.blocker_code == ApprovalBlockerCode.consent_incompatible
        ]
        compatible = status == ConsentVersionStatus.active.value and not changed_after_render and not consent_blockers
        if changed_after_render:
            consent_blockers.append("consent_changed_after_render")
        return ConsentCompatibilitySnapshot(
            schema_version="cmf.consent_compatibility_snapshot.v1",
            consent_record_version_id=view.consent_record_version_id,
            status=status,
            compatible=compatible,
            changed_after_render=changed_after_render,
            blocker_codes=consent_blockers,
        )

    def _revision_history(self, object_type: str, object_id: UUID) -> list[RevisionHistoryItem]:
        if self.revision_repository is None:
            return []
        items: list[RevisionHistoryItem] = []
        requests = [
            request
            for request in self.revision_repository.revision_requests.values()
            if request.target_object_type == object_type and request.target_object_id == object_id
        ]
        for request in sorted(requests, key=lambda item: item.created_at):
            version = self._version_for_request(request)
            receipt = next(
                (
                    item
                    for item in self.revision_repository.receipts.values()
                    if item.revision_request_id == request.revision_request_id
                ),
                None,
            )
            items.append(self._history_item(request, version, receipt.decision_code if receipt else None))
        return items

    def _version_for_request(self, request: RevisionRequest) -> RevisionVersion | None:
        if self.revision_repository is None:
            return None
        return next(
            (
                version
                for version in self.revision_repository.revision_versions.values()
                if version.revision_request_id == request.revision_request_id
            ),
            None,
        )

    @staticmethod
    def _history_item(
        request: RevisionRequest,
        version: RevisionVersion | None,
        decision_code: str | None,
    ) -> RevisionHistoryItem:
        return RevisionHistoryItem(
            revision_request_id=request.revision_request_id,
            revision_version_id=version.revision_version_id if version else None,
            target_object_type=request.target_object_type,
            target_object_id=request.target_object_id,
            prior_version_id=request.prior_version_id,
            reason=request.reason,
            decision_code=decision_code,
            created_at=request.created_at,
        )

    def _evaluation_failures(self, evaluations: list[EvaluationReceipt]) -> list[EvaluationFailureView]:
        failures: list[EvaluationFailureView] = []
        for receipt in evaluations:
            for failure in receipt.hard_failures:
                failures.append(
                    EvaluationFailureView(
                        evaluation_receipt_id=receipt.evaluation_receipt_id,
                        category=failure.category.value,
                        failure_code=failure.code,
                        evidence_refs=[evidence_ref(pointer) for pointer in failure.evidence],
                        repair_recommendation=f"repair_{failure.category.value}",
                    )
                )
        return failures

    def _panels(
        self,
        *,
        view: ApprovalEvidenceView,
        preview_ref: str | None,
        source_quote_ref: str | None,
        archetype_route_ref: str | None,
        brand_context: BrandContextVersion | None,
        selected_asset_refs: list[str],
        render_output_refs: list[str],
        evaluations: list[EvaluationReceipt],
        revision_history: list[RevisionHistoryItem],
        consent_snapshot: ConsentCompatibilitySnapshot,
    ) -> list[EvidencePanel]:
        transcript_refs = self._transcript_refs(view.transcript_revisions)
        panels = [
            self._panel(EvidencePanelType.preview, [preview_ref] if preview_ref else [], "Preview render output."),
            self._panel(
                EvidencePanelType.source_quote,
                [source_quote_ref] if source_quote_ref else [str(item.source_reference_id) for item in view.source_references],
                "Source quote and timestamped claim reference.",
            ),
            self._panel(EvidencePanelType.transcript, transcript_refs, "Transcript segment and revision hash."),
            self._panel(EvidencePanelType.archetype_route, [archetype_route_ref] if archetype_route_ref else [], "Archetype and asset route evidence."),
            self._panel(
                EvidencePanelType.brand_context,
                [str(brand_context.brand_context_version_id)] if brand_context else [],
                "Locked Brand Context Version lineage.",
            ),
            self._panel(EvidencePanelType.selected_assets, selected_asset_refs, "Selected assets and asset-roll refs."),
            self._panel(EvidencePanelType.render_output, render_output_refs, "Rendered output and provider/render refs."),
            self._panel(
                EvidencePanelType.evaluation,
                [str(receipt.evaluation_receipt_id) for receipt in evaluations],
                "Evaluation receipts and expandable failures.",
                EvidenceCompleteness.conflicting if any(receipt.hard_failures for receipt in evaluations) else None,
                ["evaluation_hard_failure"] if any(receipt.hard_failures for receipt in evaluations) else [],
            ),
            self._panel(
                EvidencePanelType.revision_history,
                [str(item.revision_request_id or item.revision_version_id) for item in revision_history] or ["revision_history:none"],
                "Revision history and prior decision reasons.",
            ),
            self._panel(
                EvidencePanelType.consent_state,
                [str(consent_snapshot.consent_record_version_id)],
                "Current consent compatibility.",
                EvidenceCompleteness.complete if consent_snapshot.compatible else EvidenceCompleteness.conflicting,
                consent_snapshot.blocker_codes,
            ),
        ]
        return panels

    @staticmethod
    def _transcript_refs(revisions: list[TranscriptRevisionSummary]) -> list[str]:
        return [
            f"{revision.transcript_revision_id}:{revision.text_ref}:{revision.transcript_hash}"
            for revision in revisions
        ]

    @staticmethod
    def _panel(
        panel_type: EvidencePanelType,
        refs: list[str],
        summary: str,
        completeness: EvidenceCompleteness | None = None,
        blocker_codes: list[str] | None = None,
    ) -> EvidencePanel:
        resolved = completeness or (EvidenceCompleteness.complete if refs else EvidenceCompleteness.missing)
        return EvidencePanel(
            panel_type=panel_type,
            object_refs=refs,
            summary=summary,
            completeness=resolved,
            blocker_codes=blocker_codes or ([] if refs else [f"{panel_type.value}_missing"]),
        )

    def _telegram_complexity(
        self,
        *,
        panels: list[EvidencePanel],
        evaluation_failures: list[EvaluationFailureView],
        telegram_complexity_score: int,
    ) -> TelegramComplexity:
        if telegram_complexity_score > self.telegram_complexity_threshold:
            return TelegramComplexity.pwa_required
        if evaluation_failures:
            return TelegramComplexity.pwa_required
        if any(panel.completeness != EvidenceCompleteness.complete for panel in panels):
            return TelegramComplexity.pwa_required
        return TelegramComplexity.quick_allowed

    def _append_event(self, event_type: str, state: ReviewEvidenceState, payload: dict[str, Any]) -> ReviewStateDomainEvent:
        return self.repository.append_event(
            ReviewStateDomainEvent(
                schema_version="cmf.review_state_domain_event.v1",
                review_state_event_id=uuid4(),
                event_type=event_type,
                review_state_id=state.review_state_id,
                object_type=state.object_type,
                object_id=state.object_id,
                payload=payload,
                created_at=utc_now(),
            )
        )


@dataclass
class ReviewStateCommandHandler:
    command_type: str
    service: ReviewStateService
    aggregate_type: str = "review_state"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "reviewer", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "BuildReviewEvidenceStateCommand":
            return self.service.build_review_evidence_state(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                approval_evidence_view_id=UUID(payload["approval_evidence_view_id"]),
                actor_id=envelope.actor.actor_id,
                preview_ref=payload.get("preview_ref"),
                source_quote_ref=payload.get("source_quote_ref"),
                archetype_route_ref=payload.get("archetype_route_ref"),
                brand_context_version_id=UUID(payload["brand_context_version_id"]) if payload.get("brand_context_version_id") else None,
                selected_asset_refs=payload.get("selected_asset_refs", []),
                render_output_refs=payload.get("render_output_refs", []),
                rendered_with_consent_record_version_id=UUID(payload["rendered_with_consent_record_version_id"]) if payload.get("rendered_with_consent_record_version_id") else None,
                telegram_complexity_score=int(payload.get("telegram_complexity_score", 0)),
                surface_route=payload.get("surface_route"),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "ExpandEvaluationFailureCommand":
            return self.service.expand_evaluation_failure(
                review_state_id=UUID(payload["review_state_id"]),
                category=payload["category"],
            ).model_dump(mode="json")
        if self.command_type == "ValidateReviewEvidenceCompletenessCommand":
            return self.service.validate_review_evidence_completeness(
                UUID(payload["review_state_id"])
            )
        if self.command_type == "CreatePwaReviewDeepLinkCommand":
            return self.service.create_pwa_review_deep_link(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                object_type=payload["object_type"],
                object_id=UUID(payload["object_id"]),
                route=payload["route"],
                required_reason=payload.get("required_reason", "PWA_REVIEW_REQUIRED"),
            ).model_dump(mode="json")
        if self.command_type == "RecordReviewStateReceiptCommand":
            state = self.service.repository.states.get(UUID(payload["review_state_id"]))
            if state is None:
                raise ReviewStateError("REVIEW_STATE_REQUIRED", "Review state is required.")
            receipt = self.service.repository.put_receipt(
                new_review_state_receipt(state=state, command_id=envelope.command_id)
            )
            return receipt.model_dump(mode="json")
        raise ReviewStateError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("review_state_id") or payload.get("object_id") or payload.get("approval_evidence_view_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_review_state_command_handlers(bus: CommandBus, service: ReviewStateService) -> None:
    for command_type in [
        "BuildReviewEvidenceStateCommand",
        "ExpandEvaluationFailureCommand",
        "ValidateReviewEvidenceCompletenessCommand",
        "CreatePwaReviewDeepLinkCommand",
        "RecordReviewStateReceiptCommand",
    ]:
        bus.register_handler(ReviewStateCommandHandler(command_type=command_type, service=service))
