"""Executable greenfield gates for TS-CMF-016."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ccp_studio.contracts.gates import (
    GateReceipt,
    GateStatus,
    GateViolationType,
    ProviderTemplateApproval,
    RuntimeBoundaryFinding,
    new_gate_receipt,
    template_hash,
)
from ccp_studio.repositories.migration_ledger_entries import InMemoryMigrationLedgerRepository
from ccp_studio.repositories.registry_entries import InMemoryRegistryRepository


LEGACY_IMPORT_PATTERNS = {
    r"src\.ccp\.services\.anti_draft_calibrator": "src/ccp/services/anti_draft_calibrator.py",
    r"ccp\.services\.anti_draft_calibrator": "src/ccp/services/anti_draft_calibrator.py",
    r"audio_engine": "src/ccp/cmf/audio_engine.py",
    r"from\s+legacy\.": "legacy",
}


class GreenfieldGateError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class GreenfieldGateService:
    migration_repository: InMemoryMigrationLedgerRepository | None = None
    registry_repository: InMemoryRegistryRepository | None = None
    receipts: dict[UUID, GateReceipt] = field(default_factory=dict)
    provider_template_approvals: dict[str, ProviderTemplateApproval] = field(default_factory=dict)
    runtime_findings: dict[UUID, RuntimeBoundaryFinding] = field(default_factory=dict)

    def run_legacy_import_gate(self, *, object_ref: str, source_text: str) -> GateReceipt:
        for pattern, source_path in LEGACY_IMPORT_PATTERNS.items():
            if re.search(pattern, source_text):
                repair_target = self._ledger_repair_target(source_path)
                return self._receipt(
                    violation_type=GateViolationType.legacy_import,
                    status=GateStatus.blocked,
                    object_ref=object_ref,
                    decision_code="LEGACY_IMPORT_BLOCKED",
                    evidence_refs=[source_path],
                    repair_target=repair_target,
                )
        return self._receipt(
            violation_type=GateViolationType.legacy_import,
            status=GateStatus.approved,
            object_ref=object_ref,
            decision_code="LEGACY_IMPORT_GATE_PASSED",
        )

    def validate_prompt_stack(
        self,
        *,
        object_ref: str,
        raw_prompt: str | None = None,
        registry_entry_id: UUID | None = None,
        compiler_key: str | None = None,
        bypass_requested: bool = False,
    ) -> GateReceipt:
        if bypass_requested:
            return self._receipt(
                violation_type=GateViolationType.hidden_prompt,
                status=GateStatus.blocked,
                object_ref=object_ref,
                decision_code="GREENFIELD_GATE_BYPASS_FORBIDDEN",
            )
        if raw_prompt and registry_entry_id is None and compiler_key is None:
            return self._receipt(
                violation_type=GateViolationType.hidden_prompt,
                status=GateStatus.blocked,
                object_ref=object_ref,
                decision_code="PROMPT_STACK_NOT_MIGRATED",
                evidence_refs=["raw_prompt"],
                repair_target="typed_registry_or_jit_skill_compiler",
            )
        return self._receipt(
            violation_type=GateViolationType.hidden_prompt,
            status=GateStatus.approved,
            object_ref=object_ref,
            decision_code="PROMPT_STACK_APPROVED",
            evidence_refs=[str(registry_entry_id or compiler_key)],
        )

    def validate_registry_conflicts(self, *, object_ref: str, registry_entry_id: UUID) -> GateReceipt:
        conflicts = (
            self.registry_repository.unresolved_conflicts_for_entry(registry_entry_id)
            if self.registry_repository is not None
            else []
        )
        if conflicts:
            return self._receipt(
                violation_type=GateViolationType.registry_conflict,
                status=GateStatus.blocked,
                object_ref=object_ref,
                decision_code="REGISTRY_CONFLICT_REQUIRES_REVIEW",
                evidence_refs=[str(conflict.registry_conflict_id) for conflict in conflicts],
                repair_target="resolve_registry_conflict",
            )
        return self._receipt(
            violation_type=GateViolationType.registry_conflict,
            status=GateStatus.approved,
            object_ref=object_ref,
            decision_code="REGISTRY_CONFLICT_GATE_PASSED",
        )

    def approve_provider_template(
        self,
        *,
        template_key: str,
        content: str | bytes,
        compatibility_notes: str,
        required_inputs: list[str],
        output_contract: str,
        known_defects: list[str],
        evaluation_target_id: UUID,
        approved_by_actor_id: UUID | None,
    ) -> ProviderTemplateApproval:
        if approved_by_actor_id is None:
            raise GreenfieldGateError("TEMPLATE_REVIEWER_REQUIRED", "Provider template approval requires reviewer.")
        if not compatibility_notes or not required_inputs or not output_contract:
            raise GreenfieldGateError("PROVIDER_TEMPLATE_HASH_REQUIRED", "Template hash, compatibility, inputs, and output contract are required.")
        approval = ProviderTemplateApproval(
            schema_version="cmf.provider_template_approval.v1",
            provider_template_approval_id=uuid4(),
            template_key=template_key,
            content_hash=template_hash(content),
            compatibility_notes=compatibility_notes,
            required_inputs=required_inputs,
            output_contract=output_contract,
            known_defects=known_defects,
            evaluation_target_id=evaluation_target_id,
            approved_by_actor_id=approved_by_actor_id,
        )
        self.provider_template_approvals[template_key] = approval
        self._receipt(
            violation_type=GateViolationType.provider_template_hash,
            status=GateStatus.approved,
            object_ref=template_key,
            decision_code="PROVIDER_TEMPLATE_APPROVED",
            evidence_refs=[approval.content_hash, str(evaluation_target_id)],
        )
        return approval

    def validate_provider_template(self, *, template_key: str, content: str | bytes) -> GateReceipt:
        approval = self.provider_template_approvals.get(template_key)
        observed_hash = template_hash(content)
        if approval is None:
            return self._receipt(
                violation_type=GateViolationType.provider_template_hash,
                status=GateStatus.blocked,
                object_ref=template_key,
                decision_code="PROVIDER_TEMPLATE_HASH_REQUIRED",
                evidence_refs=[observed_hash],
                repair_target="approve_provider_template",
            )
        if approval.content_hash != observed_hash:
            return self._receipt(
                violation_type=GateViolationType.provider_template_hash,
                status=GateStatus.blocked,
                object_ref=template_key,
                decision_code="PROVIDER_TEMPLATE_HASH_MISMATCH",
                evidence_refs=[approval.content_hash, observed_hash],
                repair_target="review_provider_template_hash",
            )
        return self._receipt(
            violation_type=GateViolationType.provider_template_hash,
            status=GateStatus.approved,
            object_ref=template_key,
            decision_code="PROVIDER_TEMPLATE_APPROVED",
            evidence_refs=[observed_hash],
        )

    def run_spec_runtime_boundary_gate(self, *, object_ref: str, spec_text: str) -> GateReceipt:
        lowered = spec_text.lower()
        drift = (
            "typescript owns domain" in lowered
            or "next.js defines domain contracts" in lowered
            or "ui owns canonical state" in lowered
            or "typescript-first backend" in lowered
        )
        permitted_leaf = "typescript leaf" in lowered or "generated consumer" in lowered
        if drift and not permitted_leaf:
            finding = RuntimeBoundaryFinding(
                schema_version="cmf.runtime_boundary_finding.v1",
                runtime_boundary_finding_id=uuid4(),
                object_ref=object_ref,
                finding_code="RUNTIME_BOUNDARY_DRIFT",
                message="Spec assigns domain authority to a non-permitted runtime boundary.",
                evidence_refs=["runtime_boundary"],
            )
            self.runtime_findings[finding.runtime_boundary_finding_id] = finding
            return self._receipt(
                violation_type=GateViolationType.runtime_boundary,
                status=GateStatus.revision_required,
                object_ref=object_ref,
                decision_code="RUNTIME_BOUNDARY_DRIFT",
                evidence_refs=[str(finding.runtime_boundary_finding_id)],
                repair_target="python_pydantic_domain_boundary",
            )
        return self._receipt(
            violation_type=GateViolationType.runtime_boundary,
            status=GateStatus.approved,
            object_ref=object_ref,
            decision_code="RUNTIME_BOUNDARY_GATE_PASSED",
        )

    def _ledger_repair_target(self, source_path: str) -> str | None:
        if self.migration_repository is None:
            return None
        entry = self.migration_repository.get_by_source_path(source_path)
        if entry is None:
            return None
        return entry.replacement_target or entry.target_map.target_python_package or entry.target_map.pydantic_contract_target

    def _receipt(
        self,
        *,
        violation_type: GateViolationType,
        status: GateStatus,
        object_ref: str,
        decision_code: str,
        evidence_refs: list[str] | None = None,
        repair_target: str | None = None,
    ) -> GateReceipt:
        receipt = new_gate_receipt(
            violation_type=violation_type,
            status=status,
            object_ref=object_ref,
            decision_code=decision_code,
            evidence_refs=evidence_refs,
            repair_target=repair_target,
        )
        self.receipts[receipt.gate_receipt_id] = receipt
        return receipt
