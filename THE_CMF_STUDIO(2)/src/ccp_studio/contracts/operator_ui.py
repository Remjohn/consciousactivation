"""Operator UI architecture contracts for TS-CMF-070."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class UiSurface(str, Enum):
    pwa = "pwa"
    telegram = "telegram"


class UiActionStatus(str, Enum):
    accepted = "accepted"
    rejected = "rejected"
    failed = "failed"
    succeeded = "succeeded"
    linked_to_domain_receipt = "linked_to_domain_receipt"


class UiBuildStatus(str, Enum):
    current = "current"
    stale = "stale"
    partial = "partial"
    failed = "failed"


class UiBlockerSummary(BaseModel):
    schema_version: Literal["cmf.ui_blocker_summary.v1"] = "cmf.ui_blocker_summary.v1"
    blocker_code: str = Field(min_length=1)
    severity: Literal["soft", "hard"]
    object_ref: str = Field(min_length=1)
    required_action: str = Field(min_length=1)


class SurfaceRouteDefinition(BaseModel):
    route_key: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    requires_brand_scope: bool = True
    requires_guest_scope: bool = False


class UiReceiptSummary(BaseModel):
    receipt_id: UUID
    status: UiActionStatus
    command_type: str = Field(min_length=1)


class CommandActionSummary(BaseModel):
    command_type: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    enabled: bool
    disabled_reason: str | None = None


class OperatorShellState(BaseModel):
    schema_version: Literal["cmf.operator_shell_state.v1"] = "cmf.operator_shell_state.v1"
    operator_user_id: UUID
    active_role_key: str = Field(min_length=1)
    organization_id: UUID
    organization_name: str = Field(min_length=1)
    brand_workspace_id: UUID
    brand_workspace_code: str = Field(min_length=1)
    brand_workspace_display_name: str = Field(min_length=1)
    brand_workspace_status: Literal["active", "suspended", "archived"] = "active"
    guest_id: UUID | None = None
    guest_code: str | None = None
    guest_display_name: str | None = None
    navigation_sections: list[SurfaceRouteDefinition] = Field(min_length=1)
    unread_notifications: int = Field(ge=0)
    pending_receipts: list[UiReceiptSummary] = Field(default_factory=list)
    blocking_alerts: list[UiBlockerSummary] = Field(default_factory=list)
    generated_contract_version: str = Field(min_length=1)


class BrandGuestScopeState(BaseModel):
    schema_version: Literal["cmf.brand_guest_scope_state.v1"] = "cmf.brand_guest_scope_state.v1"
    organization_id: UUID
    brand_workspace_id: UUID
    brand_workspace_code: str = Field(min_length=1)
    guest_id: UUID | None = None
    guest_code: str | None = None
    expression_session_id: UUID | None = None
    asset_package_id: UUID | None = None
    content_asset_id: UUID | None = None
    scope_kind: Literal["organization", "brand_workspace", "guest", "session", "package", "asset"]
    scope_is_commandable: bool
    scope_blockers: list[UiBlockerSummary] = Field(default_factory=list)


class CommercialSummary(BaseModel):
    allowed_customer_offers: list[str] = Field(default_factory=list)
    forbidden_offer_warnings: list[str] = Field(default_factory=list)


class WorkspaceControlTowerState(BaseModel):
    schema_version: Literal["cmf.workspace_control_tower_state.v1"] = "cmf.workspace_control_tower_state.v1"
    shell: OperatorShellState
    commercial_summary: CommercialSummary
    monthly_entry_artifact: Literal["interview_brief"] = "interview_brief"
    primary_monthly_command_type: Literal["generate_monthly_interview_brief"] = "generate_monthly_interview_brief"
    fallback_entry_artifact: Literal["existing_interview_transcript_video"] = "existing_interview_transcript_video"
    fallback_entry_rule: str = (
        "Use existing interview transcript/video ingestion only when no new interview will be conducted."
    )
    pipeline_stage_summaries: list[dict[str, Any]] = Field(default_factory=list)
    active_guest_workspaces: list[dict[str, Any]] = Field(default_factory=list)
    active_asset_packages: list[dict[str, Any]] = Field(default_factory=list)
    review_queue: dict[str, Any] = Field(default_factory=dict)
    evaluation_queue: dict[str, Any] = Field(default_factory=dict)
    provider_render_queue: dict[str, Any] = Field(default_factory=dict)
    agent_activity: list[dict[str, Any]] = Field(default_factory=list)
    recent_commands: list[UiReceiptSummary] = Field(default_factory=list)
    stale_or_blocked_objects: list[UiBlockerSummary] = Field(default_factory=list)


class GuestWorkspaceState(BaseModel):
    schema_version: Literal["cmf.guest_workspace_state.v1"] = "cmf.guest_workspace_state.v1"
    brand_workspace_id: UUID
    brand_workspace_code: str = Field(min_length=1)
    guest_id: UUID
    guest_code: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    consent_state: dict[str, Any] = Field(default_factory=dict)
    source_artifacts: list[dict[str, Any]] = Field(default_factory=list)
    voice_dna_refs: list[str] = Field(default_factory=list)
    emotional_dna_refs: list[str] = Field(default_factory=list)
    interview_briefs: list[dict[str, Any]] = Field(default_factory=list)
    expression_sessions: list[dict[str, Any]] = Field(default_factory=list)
    interview_asset_contracts: list[dict[str, Any]] = Field(default_factory=list)
    expression_moments: list[dict[str, Any]] = Field(default_factory=list)
    asset_packages: list[dict[str, Any]] = Field(default_factory=list)
    content_assets: list[dict[str, Any]] = Field(default_factory=list)
    approvals: list[dict[str, Any]] = Field(default_factory=list)
    publishing_intents: list[dict[str, Any]] = Field(default_factory=list)
    memory_entries: list[dict[str, Any]] = Field(default_factory=list)
    blockers: list[UiBlockerSummary] = Field(default_factory=list)


class ContentAssetCodeParts(BaseModel):
    schema_version: Literal["cmf.content_asset_code_parts.v1"] = "cmf.content_asset_code_parts.v1"
    brand_workspace_code: str = Field(min_length=1)
    guest_code: str = Field(min_length=1)
    session_code: str = Field(min_length=1)
    package_code: Literal["GAP", "MAE", "CUS"]
    format_code: str = Field(min_length=1)
    sequence_number: str = Field(pattern=r"^[0-9]{3}$")
    version_number: str = Field(pattern=r"^[0-9]{2}$")
    rendered_code: str = Field(min_length=1)


class ContentFormatSubformat(BaseModel):
    code: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    reaction_template_codes: list[str] = Field(default_factory=list)


class ContentFormatFamily(BaseModel):
    family_code: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    subformats: list[ContentFormatSubformat] = Field(default_factory=list)


class ContentAssetFormatRegistryState(BaseModel):
    schema_version: Literal["cmf.content_asset_format_registry_state.v1"] = "cmf.content_asset_format_registry_state.v1"
    format_families: list[ContentFormatFamily] = Field(min_length=1)
    reaction_editing_templates: list[dict[str, Any]] = Field(default_factory=list)
    forbidden_formats: list[str] = Field(default_factory=lambda: ["newsletter"])


class AssetPackageBoardState(BaseModel):
    schema_version: Literal["cmf.asset_package_board_state.v1"] = "cmf.asset_package_board_state.v1"
    brand_workspace_id: UUID
    guest_id: UUID
    asset_package_id: UUID
    package_code: Literal["GAP", "MAE", "CUS"]
    package_display_name: str = Field(min_length=1)
    expression_session_id: UUID | None = None
    route_receipt_id: UUID
    lanes: list[dict[str, Any]] = Field(default_factory=list)
    unsupported_or_skipped_assets: list[dict[str, Any]] = Field(default_factory=list)
    readiness_state: Literal["draft", "ready", "blocked", "in_production", "in_review", "approved", "published"]
    blockers: list[UiBlockerSummary] = Field(default_factory=list)


class ReviewEvidenceState(BaseModel):
    schema_version: Literal["cmf.review_evidence_state.v1"] = "cmf.review_evidence_state.v1"
    review_object_id: UUID
    review_object_type: str = Field(min_length=1)
    content_asset_code: str | None = None
    brand_context_version_id: UUID | None = None
    source_quote: str | None = None
    transcript_timestamp_range: str | None = None
    source_artifact_refs: list[str] = Field(default_factory=list)
    expression_moment_id: UUID | None = None
    route_receipt_id: UUID | None = None
    scene_spec_id: UUID | None = None
    composition_job_id: UUID | None = None
    composition_job_json: dict[str, Any] | None = None
    render_output_id: UUID | None = None
    evaluation_receipts: list[dict[str, Any]] = Field(default_factory=list)
    primitive_failures: list[dict[str, Any]] = Field(default_factory=list)
    consent_state: dict[str, Any] = Field(default_factory=dict)
    approval_blockers: list[UiBlockerSummary] = Field(default_factory=list)
    next_valid_review_commands: list[CommandActionSummary] = Field(default_factory=list)


class AgentFactoryState(BaseModel):
    schema_version: Literal["cmf.agent_factory_state.v1"] = "cmf.agent_factory_state.v1"
    departments: list[dict[str, Any]] = Field(default_factory=list)
    agents: list[dict[str, Any]] = Field(default_factory=list)
    sub_agents: list[dict[str, Any]] = Field(default_factory=list)
    hooks: list[dict[str, Any]] = Field(default_factory=list)
    extensions: list[dict[str, Any]] = Field(default_factory=list)
    skills: list[dict[str, Any]] = Field(default_factory=list)
    jit_skill_modes: list[dict[str, Any]] = Field(default_factory=list)
    eval_bindings: list[dict[str, Any]] = Field(default_factory=list)
    adapter_exports: list[dict[str, Any]] = Field(default_factory=list)
    readiness_findings: list[dict[str, Any]] = Field(default_factory=list)


class UiCommandEnvelope(BaseModel):
    schema_version: Literal["cmf.ui_command_envelope.v1"] = "cmf.ui_command_envelope.v1"
    command_id: UUID
    idempotency_key: str = Field(min_length=1)
    correlation_id: UUID
    requested_by_user_id: UUID
    requested_role_key: str = Field(min_length=1)
    organization_id: UUID
    brand_workspace_id: UUID
    guest_id: UUID | None = None
    active_object_type: str = Field(min_length=1)
    active_object_id: UUID
    command_type: str = Field(min_length=1)
    command_payload: dict[str, Any] = Field(default_factory=dict)
    source_surface: UiSurface
    source_route: str = Field(min_length=1)
    generated_contract_version: str = Field(min_length=1)
    expected_object_version: str | None = None


class ValidationResultSummary(BaseModel):
    code: str = Field(min_length=1)
    passed: bool
    message: str = Field(min_length=1)


class EventSummary(BaseModel):
    event_type: str = Field(min_length=1)
    event_ref: str = Field(min_length=1)


class UiActionReceipt(BaseModel):
    schema_version: Literal["cmf.ui_action_receipt.v1"] = "cmf.ui_action_receipt.v1"
    receipt_id: UUID
    command_id: UUID
    correlation_id: UUID
    source_surface: UiSurface
    status: UiActionStatus
    domain_receipt_id: UUID | None = None
    domain_receipt_type: str | None = None
    active_object_type: str = Field(min_length=1)
    active_object_id: UUID
    content_asset_code: str | None = None
    validation_results: list[ValidationResultSummary] = Field(default_factory=list)
    blockers: list[UiBlockerSummary] = Field(default_factory=list)
    emitted_events: list[EventSummary] = Field(default_factory=list)
    created_at: datetime


class UiStateBuildReceipt(BaseModel):
    schema_version: Literal["cmf.ui_state_build_receipt.v1"] = "cmf.ui_state_build_receipt.v1"
    receipt_id: UUID
    read_model_name: str = Field(min_length=1)
    organization_id: UUID
    brand_workspace_id: UUID
    guest_id: UUID | None = None
    source_event_checkpoint: str = Field(min_length=1)
    contract_version: str = Field(min_length=1)
    projection_version: str = Field(min_length=1)
    build_status: UiBuildStatus
    missing_dependencies: list[str] = Field(default_factory=list)
    created_at: datetime


def render_content_asset_code(
    *,
    brand_workspace_code: str,
    guest_code: str,
    session_code: str,
    package_code: Literal["GAP", "MAE", "CUS"],
    format_code: str,
    sequence_number: int,
    version_number: int,
) -> ContentAssetCodeParts:
    seq = f"{sequence_number:03d}"
    ver = f"{version_number:02d}"
    rendered = f"{brand_workspace_code}-{guest_code}-{session_code}-{package_code}-{format_code}-{seq}-V{ver}"
    return ContentAssetCodeParts(
        brand_workspace_code=brand_workspace_code,
        guest_code=guest_code,
        session_code=session_code,
        package_code=package_code,
        format_code=format_code,
        sequence_number=seq,
        version_number=ver,
        rendered_code=rendered,
    )


def default_content_format_registry() -> ContentAssetFormatRegistryState:
    return ContentAssetFormatRegistryState(
        format_families=[
            ContentFormatFamily(
                family_code="SV",
                display_name="Short Video",
                subformats=[
                    ContentFormatSubformat(code="SV-CSC", display_name="Cinematic Story Commentary"),
                    ContentFormatSubformat(code="SV-EDU", display_name="Educational Explainer"),
                    ContentFormatSubformat(code="SV-FRB", display_name="Challenger / Frame Breaker"),
                    ContentFormatSubformat(
                        code="SV-RRC",
                        display_name="Reaction / Recognition Clip",
                        reaction_template_codes=[
                            "VRS-SPLIT",
                            "TRK-TIER",
                            "RNK-BLIND",
                            "RNK-PROPOSAL",
                            "ELM-BRACKET",
                            "MIR-QUIZ",
                            "AUTH-LADDER",
                        ],
                    ),
                ],
            ),
            ContentFormatFamily(
                family_code="CAR",
                display_name="Carousel",
                subformats=[
                    ContentFormatSubformat(code="CAR-LST", display_name="Listicle Carousel", reaction_template_codes=["TRK-TIER", "RNK-PROPOSAL"]),
                    ContentFormatSubformat(code="CAR-JUX", display_name="Juxtaposition Carousel"),
                ],
            ),
            ContentFormatFamily(
                family_code="VPL",
                display_name="Visual Poll",
                subformats=[
                    ContentFormatSubformat(code="VPL-WYR", display_name="Would You Rather", reaction_template_codes=["VRS-SPLIT", "MIR-QUIZ"]),
                    ContentFormatSubformat(code="VPL-VRS", display_name="Versus Poll", reaction_template_codes=["VRS-SPLIT", "RNK-BLIND", "ELM-BRACKET"]),
                ],
            ),
            ContentFormatFamily(
                family_code="TWQ",
                display_name="Tweet-Like Quote",
                subformats=[
                    ContentFormatSubformat(code="TWQ-STD", display_name="Standard Quote"),
                    ContentFormatSubformat(code="TWQ-IMG", display_name="Image Quote"),
                ],
            ),
            ContentFormatFamily(
                family_code="MEM",
                display_name="Meme",
                subformats=[
                    ContentFormatSubformat(code="MEM-INC", display_name="Insight Contrast Meme"),
                    ContentFormatSubformat(code="MEM-REL", display_name="Relatable Meme", reaction_template_codes=["MIR-QUIZ"]),
                ],
            ),
            ContentFormatFamily(
                family_code="SPV",
                display_name="Super Visual",
                subformats=[
                    ContentFormatSubformat(code="SPV-CON", display_name="Conceptual Super Visual"),
                    ContentFormatSubformat(code="SPV-SYM", display_name="Symbolic Super Visual"),
                    ContentFormatSubformat(code="SPV-PRM", display_name="Premium Super Visual"),
                ],
            ),
            ContentFormatFamily(
                family_code="RCT",
                display_name="Reaction Seed",
                subformats=[
                    ContentFormatSubformat(
                        code="RCT-SEED",
                        display_name="Reaction Seed",
                        reaction_template_codes=[
                            "VRS-SPLIT",
                            "TRK-TIER",
                            "RNK-BLIND",
                            "RNK-PROPOSAL",
                            "ELM-BRACKET",
                            "MIR-QUIZ",
                            "AUTH-LADDER",
                        ],
                    )
                ],
            ),
        ],
        reaction_editing_templates=[
            {"template_code": "VRS-SPLIT", "display_name": "Versus Split Screen", "source_app_ref": "apps/react-debate"},
            {"template_code": "TRK-TIER", "display_name": "Tier List Ranking", "source_app_ref": "apps/react-tierlist"},
            {"template_code": "RNK-BLIND", "display_name": "Blind Ranking", "source_app_ref": "apps/react-blind-rank"},
            {"template_code": "RNK-PROPOSAL", "display_name": "Proposal Ranking Quiz", "source_app_ref": "apps/react-ranking-quiz"},
            {"template_code": "ELM-BRACKET", "display_name": "Elimination Bracket", "source_app_ref": "apps/react-elimination"},
            {"template_code": "MIR-QUIZ", "display_name": "Mirror Quiz", "source_app_ref": "apps/react-mirror-quiz"},
            {"template_code": "AUTH-LADDER", "display_name": "Authority Ladder Quiz", "source_app_ref": "apps/react-authority-quiz"},
        ],
        forbidden_formats=["newsletter"],
    )


def new_ui_state_build_receipt(
    *,
    read_model_name: str,
    organization_id: UUID,
    brand_workspace_id: UUID,
    guest_id: UUID | None,
    contract_version: str,
    projection_version: str,
    build_status: UiBuildStatus = UiBuildStatus.current,
    missing_dependencies: list[str] | None = None,
) -> UiStateBuildReceipt:
    return UiStateBuildReceipt(
        receipt_id=uuid4(),
        read_model_name=read_model_name,
        organization_id=organization_id,
        brand_workspace_id=brand_workspace_id,
        guest_id=guest_id,
        source_event_checkpoint="in_memory:current",
        contract_version=contract_version,
        projection_version=projection_version,
        build_status=build_status,
        missing_dependencies=missing_dependencies or [],
        created_at=utc_now(),
    )
