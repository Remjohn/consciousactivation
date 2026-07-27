"""Operator UI repository for TS-CMF-070."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.operator_ui import (
    AgentFactoryState,
    BrandGuestScopeState,
    GuestWorkspaceState,
    OperatorShellState,
    ReviewEvidenceState,
    UiActionReceipt,
    UiCommandEnvelope,
    UiStateBuildReceipt,
    WorkspaceControlTowerState,
)


@dataclass
class InMemoryOperatorUiRepository:
    shell_states: dict[UUID, OperatorShellState] = field(default_factory=dict)
    scope_states: dict[str, BrandGuestScopeState] = field(default_factory=dict)
    control_tower_states: dict[UUID, WorkspaceControlTowerState] = field(default_factory=dict)
    guest_workspace_states: dict[UUID, GuestWorkspaceState] = field(default_factory=dict)
    review_evidence_states: dict[UUID, ReviewEvidenceState] = field(default_factory=dict)
    agent_factory_states: dict[UUID, AgentFactoryState] = field(default_factory=dict)
    command_envelopes: dict[UUID, UiCommandEnvelope] = field(default_factory=dict)
    action_receipts: dict[UUID, UiActionReceipt] = field(default_factory=dict)
    build_receipts: dict[UUID, UiStateBuildReceipt] = field(default_factory=dict)

    def put_shell_state(self, state: OperatorShellState) -> OperatorShellState:
        self.shell_states[state.operator_user_id] = state
        return state

    def put_scope_state(self, state: BrandGuestScopeState) -> BrandGuestScopeState:
        self.scope_states[self.scope_key(state)] = state
        return state

    def put_control_tower_state(self, state: WorkspaceControlTowerState) -> WorkspaceControlTowerState:
        self.control_tower_states[state.shell.brand_workspace_id] = state
        return state

    def put_guest_workspace_state(self, state: GuestWorkspaceState) -> GuestWorkspaceState:
        self.guest_workspace_states[state.guest_id] = state
        return state

    def put_review_evidence_state(self, state: ReviewEvidenceState) -> ReviewEvidenceState:
        self.review_evidence_states[state.review_object_id] = state
        return state

    def put_agent_factory_state(self, brand_workspace_id: UUID, state: AgentFactoryState) -> AgentFactoryState:
        self.agent_factory_states[brand_workspace_id] = state
        return state

    def put_command_envelope(self, envelope: UiCommandEnvelope) -> UiCommandEnvelope:
        self.command_envelopes[envelope.command_id] = envelope
        return envelope

    def put_action_receipt(self, receipt: UiActionReceipt) -> UiActionReceipt:
        self.action_receipts[receipt.receipt_id] = receipt
        return receipt

    def put_build_receipt(self, receipt: UiStateBuildReceipt) -> UiStateBuildReceipt:
        self.build_receipts[receipt.receipt_id] = receipt
        return receipt

    @staticmethod
    def scope_key(state: BrandGuestScopeState) -> str:
        return ":".join(
            [
                str(state.organization_id),
                str(state.brand_workspace_id),
                str(state.guest_id or "none"),
                str(state.expression_session_id or "none"),
                str(state.asset_package_id or "none"),
                str(state.content_asset_id or "none"),
            ]
        )

