"""Operations workflow for TS-CMF-059."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ccp_studio.contracts.operations_board import OperationsBoardState
from ccp_studio.contracts.operational_readiness import OperationalReadinessReport
from ccp_studio.contracts.workflow_recovery import WorkflowRecoveryActionType, WorkflowRecoveryReceipt
from ccp_studio.services.operations_board_service import OperationsBoardService
from ccp_studio.services.operational_readiness_service import OperationalReadinessService
from ccp_studio.services.workflow_recovery_service import WorkflowRecoveryService


@dataclass
class OperationsWorkflow:
    operations_board_service: OperationsBoardService
    workflow_recovery_service: WorkflowRecoveryService | None = None
    operational_readiness_service: OperationalReadinessService | None = None

    def overlay_board_state(self, **kwargs: Any) -> OperationsBoardState:
        return self.operations_board_service.overlay_board_state(**kwargs)

    def recover_failed_workflow(self, *, action_type: WorkflowRecoveryActionType | str, **kwargs: Any) -> WorkflowRecoveryReceipt:
        if self.workflow_recovery_service is None:
            raise RuntimeError("WorkflowRecoveryService is required for workflow recovery.")
        return self.workflow_recovery_service.recover_failed_workflow(action_type=action_type, **kwargs)

    def release_readiness_overlay(self, **kwargs: Any) -> OperationalReadinessReport:
        if self.operational_readiness_service is None:
            raise RuntimeError("OperationalReadinessService is required for release readiness.")
        return self.operational_readiness_service.run_operational_readiness_suite(**kwargs)
