"""Operator UI read-model and command service for TS-CMF-070."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ccp_studio.contracts.agent_factory import AgentActivationState
from ccp_studio.contracts.operator_ui import (
    AgentFactoryState,
    BrandGuestScopeState,
    CommercialSummary,
    ContentAssetCodeParts,
    ContentAssetFormatRegistryState,
    GuestWorkspaceState,
    OperatorShellState,
    ReviewEvidenceState,
    SurfaceRouteDefinition,
    UiActionReceipt,
    UiActionStatus,
    UiBlockerSummary,
    UiBuildStatus,
    UiCommandEnvelope,
    UiReceiptSummary,
    UiSurface,
    ValidationResultSummary,
    WorkspaceControlTowerState,
    default_content_format_registry,
    new_ui_state_build_receipt,
    render_content_asset_code,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.operator_ui import CommandActionSummary
from ccp_studio.contracts.skills import SkillUseMode
from ccp_studio.repositories.agent_factory import InMemoryAgentFactoryRepository
from ccp_studio.repositories.operator_ui import InMemoryOperatorUiRepository


ALLOWED_CUSTOMER_OFFERS = ["$29/week trial Guest Asset Pack", "$99/month Monthly Asset Engine"]
FORBIDDEN_FORMATS = {"newsletter"}


class OperatorUiError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class OperatorUiService:
    repository: InMemoryOperatorUiRepository = field(default_factory=InMemoryOperatorUiRepository)
    agent_factory_repository: InMemoryAgentFactoryRepository | None = None
    generated_contract_version: str = "cmf-ui-contracts.2026-06-22"
    projection_version: str = "in-memory.v1"

    def build_shell_state(
        self,
        *,
        operator_user_id: UUID,
        active_role_key: str,
        organization_id: UUID,
        organization_name: str,
        brand_workspace_id: UUID,
        brand_workspace_code: str,
        brand_workspace_display_name: str,
        guest_id: UUID | None = None,
        guest_code: str | None = None,
        guest_display_name: str | None = None,
        blockers: list[UiBlockerSummary] | None = None,
    ) -> OperatorShellState:
        state = OperatorShellState(
            operator_user_id=operator_user_id,
            active_role_key=active_role_key,
            organization_id=organization_id,
            organization_name=organization_name,
            brand_workspace_id=brand_workspace_id,
            brand_workspace_code=brand_workspace_code,
            brand_workspace_display_name=brand_workspace_display_name,
            guest_id=guest_id,
            guest_code=guest_code,
            guest_display_name=guest_display_name,
            navigation_sections=self._navigation_sections(),
            unread_notifications=0,
            pending_receipts=[
                UiReceiptSummary(
                    receipt_id=receipt.receipt_id,
                    status=receipt.status,
                    command_type=self.repository.command_envelopes.get(receipt.command_id).command_type
                    if receipt.command_id in self.repository.command_envelopes
                    else "unknown",
                )
                for receipt in self.repository.action_receipts.values()
                if receipt.status in {UiActionStatus.accepted, UiActionStatus.failed}
            ],
            blocking_alerts=blockers or [],
            generated_contract_version=self.generated_contract_version,
        )
        self.repository.put_shell_state(state)
        self.repository.put_build_receipt(
            new_ui_state_build_receipt(
                read_model_name="OperatorShellState",
                organization_id=organization_id,
                brand_workspace_id=brand_workspace_id,
                guest_id=guest_id,
                contract_version=self.generated_contract_version,
                projection_version=self.projection_version,
                build_status=UiBuildStatus.current,
            )
        )
        return state

    def build_scope_state(
        self,
        *,
        organization_id: UUID,
        brand_workspace_id: UUID,
        brand_workspace_code: str,
        guest_id: UUID | None = None,
        guest_code: str | None = None,
        expression_session_id: UUID | None = None,
        asset_package_id: UUID | None = None,
        content_asset_id: UUID | None = None,
        blockers: list[UiBlockerSummary] | None = None,
    ) -> BrandGuestScopeState:
        scope_kind = "brand_workspace"
        if content_asset_id:
            scope_kind = "asset"
        elif asset_package_id:
            scope_kind = "package"
        elif expression_session_id:
            scope_kind = "session"
        elif guest_id:
            scope_kind = "guest"
        state = BrandGuestScopeState(
            organization_id=organization_id,
            brand_workspace_id=brand_workspace_id,
            brand_workspace_code=brand_workspace_code,
            guest_id=guest_id,
            guest_code=guest_code,
            expression_session_id=expression_session_id,
            asset_package_id=asset_package_id,
            content_asset_id=content_asset_id,
            scope_kind=scope_kind,  # type: ignore[arg-type]
            scope_is_commandable=not any(blocker.severity == "hard" for blocker in blockers or []),
            scope_blockers=blockers or [],
        )
        return self.repository.put_scope_state(state)

    def build_control_tower_state(self, shell: OperatorShellState) -> WorkspaceControlTowerState:
        state = WorkspaceControlTowerState(
            shell=shell,
            commercial_summary=CommercialSummary(
                allowed_customer_offers=list(ALLOWED_CUSTOMER_OFFERS),
                forbidden_offer_warnings=["newsletters and extra pricing offers are not valid CMF Studio offers"],
            ),
            pipeline_stage_summaries=[
                {
                    "stage_key": "monthly_interview_brief",
                    "display_name": "Monthly Interview Brief",
                    "stage_order": 1,
                    "entry_artifact": "interview_brief",
                    "primary": True,
                    "command_type": "generate_monthly_interview_brief",
                    "entry_rule": "Default monthly entry point when a new interview will be conducted.",
                },
                {
                    "stage_key": "existing_interview_ingestion",
                    "display_name": "Existing Interview Transcript + Video Ingestion",
                    "stage_order": 2,
                    "entry_artifact": "existing_interview_transcript_video",
                    "primary": False,
                    "fallback": True,
                    "command_type": "ingest_existing_interview_source",
                    "entry_rule": "Use only when no new interview will be conducted.",
                },
            ],
            review_queue={"pending": 0, "blocked": len(shell.blocking_alerts)},
            evaluation_queue={"pending": 0},
            provider_render_queue={"pending": 0},
            recent_commands=shell.pending_receipts,
            stale_or_blocked_objects=shell.blocking_alerts,
        )
        self.repository.put_control_tower_state(state)
        self.repository.put_build_receipt(
            new_ui_state_build_receipt(
                read_model_name="WorkspaceControlTowerState",
                organization_id=shell.organization_id,
                brand_workspace_id=shell.brand_workspace_id,
                guest_id=shell.guest_id,
                contract_version=self.generated_contract_version,
                projection_version=self.projection_version,
            )
        )
        return state

    def build_guest_workspace_state(
        self,
        *,
        brand_workspace_id: UUID,
        brand_workspace_code: str,
        guest_id: UUID,
        guest_code: str,
        display_name: str,
        blockers: list[UiBlockerSummary] | None = None,
    ) -> GuestWorkspaceState:
        state = GuestWorkspaceState(
            brand_workspace_id=brand_workspace_id,
            brand_workspace_code=brand_workspace_code,
            guest_id=guest_id,
            guest_code=guest_code,
            display_name=display_name,
            blockers=blockers or [],
        )
        return self.repository.put_guest_workspace_state(state)

    def content_format_registry(self) -> ContentAssetFormatRegistryState:
        return default_content_format_registry()

    def render_asset_code(
        self,
        *,
        brand_workspace_code: str,
        guest_code: str,
        session_code: str,
        package_code: str,
        format_code: str,
        sequence_number: int,
        version_number: int,
    ) -> ContentAssetCodeParts:
        self.validate_format_code(format_code)
        return render_content_asset_code(
            brand_workspace_code=brand_workspace_code,
            guest_code=guest_code,
            session_code=session_code,
            package_code=package_code,  # type: ignore[arg-type]
            format_code=format_code,
            sequence_number=sequence_number,
            version_number=version_number,
        )

    def validate_format_code(self, format_code: str) -> None:
        if format_code.lower() in FORBIDDEN_FORMATS:
            raise OperatorUiError("CONTENT_FORMAT_FORBIDDEN", "Newsletter is not a valid CMF Studio content format.")
        registry = self.content_format_registry()
        valid_codes = {
            subformat.code
            for family in registry.format_families
            for subformat in family.subformats
        }
        if format_code not in valid_codes:
            raise OperatorUiError("CONTENT_FORMAT_UNKNOWN", "Content format code is not registered.")

    def build_review_evidence_state(self, state: ReviewEvidenceState) -> ReviewEvidenceState:
        hard_blocker = any(blocker.severity == "hard" for blocker in state.approval_blockers)
        commands = [
            CommandActionSummary(
                command_type="approve_review_object",
                display_name="Approve",
                enabled=not hard_blocker,
                disabled_reason="hard blocker requires repair" if hard_blocker else None,
            )
        ]
        updated = state.model_copy(update={"next_valid_review_commands": commands})
        return self.repository.put_review_evidence_state(updated)

    def create_command_envelope(
        self,
        *,
        requested_by_user_id: UUID,
        requested_role_key: str,
        organization_id: UUID,
        brand_workspace_id: UUID,
        guest_id: UUID | None,
        active_object_type: str,
        active_object_id: UUID,
        command_type: str,
        command_payload: dict,
        source_surface: UiSurface,
        source_route: str,
        expected_object_version: str | None = None,
    ) -> UiCommandEnvelope:
        if not organization_id or not brand_workspace_id:
            raise OperatorUiError("UI_SCOPE_REQUIRED", "Organization and brand workspace scope are required.")
        envelope = UiCommandEnvelope(
            command_id=uuid4(),
            idempotency_key=f"ui:{source_surface.value}:{command_type}:{uuid4()}",
            correlation_id=uuid4(),
            requested_by_user_id=requested_by_user_id,
            requested_role_key=requested_role_key,
            organization_id=organization_id,
            brand_workspace_id=brand_workspace_id,
            guest_id=guest_id,
            active_object_type=active_object_type,
            active_object_id=active_object_id,
            command_type=command_type,
            command_payload=command_payload,
            source_surface=source_surface,
            source_route=source_route,
            generated_contract_version=self.generated_contract_version,
            expected_object_version=expected_object_version,
        )
        return self.repository.put_command_envelope(envelope)

    def submit_ui_command(
        self,
        envelope: UiCommandEnvelope,
        *,
        blockers: list[UiBlockerSummary] | None = None,
        content_asset_code: str | None = None,
        object_version_current: bool = True,
        pwa_deep_link: str | None = None,
    ) -> UiActionReceipt:
        blockers = blockers or []
        validation_results: list[ValidationResultSummary] = []
        failure_blockers: list[UiBlockerSummary] = list(blockers)
        status = UiActionStatus.accepted
        if any(blocker.severity == "hard" for blocker in blockers):
            status = UiActionStatus.rejected
            validation_results.append(
                ValidationResultSummary(
                    code="HARD_BLOCKER_PRESENT",
                    passed=False,
                    message="Hard blockers disable production commands.",
                )
            )
        if not object_version_current:
            status = UiActionStatus.rejected
            validation_results.append(
                ValidationResultSummary(
                    code="STALE_OBJECT_VERSION",
                    passed=False,
                    message="Object state changed after UI notification.",
                )
            )
        if envelope.source_surface == UiSurface.telegram and self._telegram_requires_pwa(envelope, blockers, object_version_current):
            status = UiActionStatus.rejected
            failure_blockers.append(
                UiBlockerSummary(
                    blocker_code="TELEGRAM_PWA_REVIEW_REQUIRED",
                    severity="hard",
                    object_ref=f"{envelope.active_object_type}:{envelope.active_object_id}",
                    required_action=pwa_deep_link or "open_pwa_review",
                )
            )
            validation_results.append(
                ValidationResultSummary(
                    code="TELEGRAM_PWA_REVIEW_REQUIRED",
                    passed=False,
                    message="Telegram quick action must deep-link to the PWA for this object.",
                )
            )
        if status == UiActionStatus.accepted:
            validation_results.append(
                ValidationResultSummary(
                    code="UI_COMMAND_CONTRACT_ACCEPTED",
                    passed=True,
                    message="Command envelope accepted for backend validation.",
                )
            )
        receipt = UiActionReceipt(
            receipt_id=uuid4(),
            command_id=envelope.command_id,
            correlation_id=envelope.correlation_id,
            source_surface=envelope.source_surface,
            status=status,
            active_object_type=envelope.active_object_type,
            active_object_id=envelope.active_object_id,
            content_asset_code=content_asset_code,
            validation_results=validation_results,
            blockers=failure_blockers,
            created_at=utc_now(),
        )
        return self.repository.put_action_receipt(receipt)

    def build_agent_factory_state(self, *, brand_workspace_id: UUID) -> AgentFactoryState:
        repo = self.agent_factory_repository
        state = AgentFactoryState()
        if repo:
            state = AgentFactoryState(
                departments=[department.model_dump(mode="json") for department in repo.departments.values()],
                agents=[agent.model_dump(mode="json") for agent in repo.agent_roles.values()],
                sub_agents=[sub_agent.model_dump(mode="json") for sub_agent in repo.sub_agent_roles.values()],
                hooks=[hook.model_dump(mode="json") for hook in repo.hook_specs.values()],
                extensions=[extension.model_dump(mode="json") for extension in repo.extension_specs.values()],
                skills=[skill.model_dump(mode="json") for skill in repo.skill_bindings.values()],
                jit_skill_modes=[{"mode": mode.value} for mode in SkillUseMode],
                eval_bindings=[readiness.model_dump(mode="json") for readiness in repo.readiness_evals.values()],
                adapter_exports=[export.model_dump(mode="json") for export in repo.adapter_exports.values()],
                readiness_findings=[
                    {"entity_code": readiness.entity_code, "status": readiness.status, "findings": readiness.findings}
                    for readiness in repo.readiness_evals.values()
                ],
            )
            state.agents.sort(key=lambda item: (item["activation_state"] != AgentActivationState.active.value, item["entity_code"]))
        return self.repository.put_agent_factory_state(brand_workspace_id, state)

    @staticmethod
    def _telegram_requires_pwa(envelope: UiCommandEnvelope, blockers: list[UiBlockerSummary], object_version_current: bool) -> bool:
        command = envelope.command_type.lower()
        high_risk = bool(envelope.command_payload.get("public_or_high_risk"))
        conflicting_evidence = bool(envelope.command_payload.get("evidence_conflicting"))
        primitive_failures = bool(envelope.command_payload.get("primitive_failures"))
        consent_changed = bool(envelope.command_payload.get("consent_changed"))
        return (
            command in {"approve_review_object", "publish_asset", "approve_publication"}
            and (
                not object_version_current
                or high_risk
                or conflicting_evidence
                or primitive_failures
                or consent_changed
                or any(blocker.severity == "hard" for blocker in blockers)
            )
        )

    @staticmethod
    def _navigation_sections() -> list[SurfaceRouteDefinition]:
        return [
            SurfaceRouteDefinition(route_key="control_tower", display_name="Control Tower"),
            SurfaceRouteDefinition(route_key="guests", display_name="Guests"),
            SurfaceRouteDefinition(route_key="pipeline", display_name="Pipeline"),
            SurfaceRouteDefinition(route_key="brand_genesis", display_name="Brand Genesis"),
            SurfaceRouteDefinition(route_key="research", display_name="Research"),
            SurfaceRouteDefinition(route_key="interview", display_name="Interview"),
            SurfaceRouteDefinition(route_key="extraction", display_name="Extraction"),
            SurfaceRouteDefinition(route_key="packages", display_name="Packages"),
            SurfaceRouteDefinition(route_key="production", display_name="Production"),
            SurfaceRouteDefinition(route_key="evals", display_name="Evals"),
            SurfaceRouteDefinition(route_key="review", display_name="Review"),
            SurfaceRouteDefinition(route_key="publishing", display_name="Publishing"),
            SurfaceRouteDefinition(route_key="memory", display_name="Memory"),
            SurfaceRouteDefinition(route_key="agent_factory", display_name="Agent Factory"),
            SurfaceRouteDefinition(route_key="operations", display_name="Operations"),
        ]
