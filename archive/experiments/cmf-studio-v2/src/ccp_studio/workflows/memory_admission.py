"""Memory admission workflow for TS-CMF-056."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ccp_studio.contracts.memory_admission import MemoryAdmissionReceipt
from ccp_studio.contracts.memory_governance import MemoryGovernanceReceipt
from ccp_studio.services.memory_admission_service import MemoryAdmissionService
from ccp_studio.services.memory_governance_service import MemoryGovernanceService


@dataclass
class MemoryAdmissionWorkflow:
    memory_admission_service: MemoryAdmissionService
    memory_governance_service: MemoryGovernanceService | None = None

    def stage14_admit_evidence_memory(self, **kwargs: Any) -> MemoryAdmissionReceipt:
        return self.memory_admission_service.stage14_admit_evidence_memory(**kwargs)

    def stage14_govern_memory(self, **kwargs: Any) -> MemoryGovernanceReceipt:
        if self.memory_governance_service is None:
            raise RuntimeError("MemoryGovernanceService is required for memory governance.")
        return self.memory_governance_service.stage14_govern_memory(**kwargs)
