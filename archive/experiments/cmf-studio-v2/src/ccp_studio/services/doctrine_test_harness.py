"""Doctrine-driven test harness service for TS-CMF-077."""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from typing import Any
from uuid import UUID

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.doctrine_tests import (
    DoctrineInvariant,
    DoctrineInvariantResult,
    DoctrineNegativeFixture,
    DoctrineNegativeFixtureResult,
    DoctrinePrimitiveResult,
    DoctrinePrimitiveTestObligation,
    DoctrineTestRunReceipt,
    DoctrineTestTarget,
    new_doctrine_test_run_receipt,
    new_doctrine_test_target,
)
from ccp_studio.project_paths import discover_project_root, resolve_project_path
from ccp_studio.repositories.doctrine_tests import InMemoryDoctrineTestRepository
from ccp_studio.services.command_bus import CommandBus


class DoctrineTestHarnessError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


SPEC_AUDIT_REQUIRED_MARKERS = {
    "files_read": ["## Files Read", "# Files Read", "Files Read"],
    "requirement_trace": ["## Requirement Trace", "# Requirement Trace", "Requirement Trace"],
    "pipeline_stage_trace": ["## Pipeline Stage Trace", "# Pipeline Stage Trace", "Pipeline Stage Trace"],
    "legacy_inventory": [
        "Legacy Inventory",
        "docs/migration/legacy-inventory.md",
        "legacy-inventory.md",
    ],
    "doctrine_test_harness_binding": ["Doctrine-Driven Test Harness Binding"],
    "required_receipt": ["required_receipt", "required receipt", "Required Receipt"],
    "cbar": ["CBAR", "Constraint-Based Adversarial Reasoning"],
}


def canonical_spec_audit_invariants() -> list[DoctrineInvariant]:
    return [
        DoctrineInvariant(
            schema_version="cmf.doctrine_invariant.v1",
            invariant_id=f"INV-SPEC-{marker.upper().replace('_', '-')}",
            name=f"Spec contains {marker.replace('_', ' ')} evidence",
            statement=(
                "Every buildable CMF tech spec must carry explicit evidence that it was "
                "written from source files, mapped to pipeline stage traces, bound to "
                "legacy inventory context, and governed by doctrine test receipts."
            ),
            source_doctrine_refs=[
                "THE CMF STUDIO/docs/tech-specs/TS-CMF-077-doctrine-driven-test-harness-and-primitive-eval-coverage.md",
                "THE CMF STUDIO/docs/architecture/april_updates/PROMPT_Spec_Audit.md",
                "THE CMF STUDIO/docs/migration/legacy-inventory.md",
            ],
            applies_to_target_types=["tech_spec"],
            required_evidence_types=[marker],
            hard_failure_code=f"SPEC_{marker.upper()}_MISSING",
            approval_blocker_code=f"BLOCK_SPEC_{marker.upper()}_MISSING",
        )
        for marker in SPEC_AUDIT_REQUIRED_MARKERS
    ]


@dataclass
class DoctrineTestHarnessService:
    repository: InMemoryDoctrineTestRepository = field(default_factory=InMemoryDoctrineTestRepository)
    workspace_root: Path = field(default_factory=discover_project_root)

    def register_invariant(self, invariant: DoctrineInvariant) -> DoctrineInvariant:
        return self.repository.put_invariant(invariant)

    def register_canonical_spec_audit_invariants(self) -> list[DoctrineInvariant]:
        return [
            self.repository.put_invariant(invariant)
            for invariant in canonical_spec_audit_invariants()
        ]

    def run_suite(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        target: DoctrineTestTarget,
        actor_id: UUID,
        invariants: list[DoctrineInvariant] | None = None,
        primitive_obligations: list[DoctrinePrimitiveTestObligation] | None = None,
        negative_fixtures: list[DoctrineNegativeFixture] | None = None,
        evidence_by_key: dict[str, list[str]] | None = None,
        observed_text: str | None = None,
        command_id: UUID | None = None,
    ) -> DoctrineTestRunReceipt:
        evidence = _normalize_evidence(evidence_by_key or {})
        resolved_invariants = list(invariants) if invariants is not None else self.repository.list_invariants_for_target_type(target.target_type)
        applicable_invariants = [
            invariant
            for invariant in resolved_invariants
            if self._applies_to_target(invariant, target.target_type)
        ]
        invariant_results = [
            self._evaluate_invariant(invariant, target, evidence)
            for invariant in applicable_invariants
        ]
        primitive_results = [
            self._evaluate_primitive_obligation(obligation, target, evidence)
            for obligation in (primitive_obligations or [])
        ]
        negative_results = [
            self._evaluate_negative_fixture(fixture, target, evidence, observed_text or "")
            for fixture in (negative_fixtures or [])
        ]
        receipt = new_doctrine_test_run_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            target=target,
            invariant_results=invariant_results,
            primitive_results=primitive_results,
            negative_fixture_results=negative_results,
            actor_id=actor_id,
            command_id=command_id,
        )
        return self.repository.put_receipt(receipt)

    def audit_spec_file(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        spec_path: str,
        actor_id: UUID,
        spec_id: str | None = None,
        command_id: UUID | None = None,
    ) -> DoctrineTestRunReceipt:
        resolved = resolve_project_path(spec_path, self.workspace_root)
        if not resolved.exists():
            raise DoctrineTestHarnessError("SPEC_FILE_NOT_FOUND", f"{spec_path} does not exist.")
        text = resolved.read_text(encoding="utf-8")
        evidence_by_key = self._spec_marker_evidence(text, spec_path)
        target = new_doctrine_test_target(
            target_type="tech_spec",
            target_id=_uuid_from_text(str(resolved.resolve())),
            object_hash=sha256(text.encode("utf-8")).hexdigest(),
            spec_id=spec_id or resolved.stem,
            pipeline_stage="tech_spec_audit",
            lineage_refs=[f"spec_path:{spec_path}"],
        )
        return self.run_suite(
            organization_id=organization_id,
            brand_id=brand_id,
            target=target,
            actor_id=actor_id,
            invariants=canonical_spec_audit_invariants(),
            evidence_by_key=evidence_by_key,
            observed_text=text,
            command_id=command_id,
        )

    def _evaluate_invariant(
        self,
        invariant: DoctrineInvariant,
        target: DoctrineTestTarget,
        evidence_by_key: dict[str, list[str]],
    ) -> DoctrineInvariantResult:
        evidence_refs, missing = self._evidence_for_required_types(
            required_types=invariant.required_evidence_types,
            subject_key=invariant.invariant_id,
            target=target,
            evidence_by_key=evidence_by_key,
        )
        passed = not missing
        return DoctrineInvariantResult(
            invariant_id=invariant.invariant_id,
            passed=passed,
            evidence_refs=evidence_refs,
            missing_evidence_types=missing,
            hard_failure_code=None if passed else invariant.hard_failure_code,
            approval_blocker_code=None if passed else invariant.approval_blocker_code,
        )

    def _evaluate_primitive_obligation(
        self,
        obligation: DoctrinePrimitiveTestObligation,
        target: DoctrineTestTarget,
        evidence_by_key: dict[str, list[str]],
    ) -> DoctrinePrimitiveResult:
        evidence_refs, missing = self._evidence_for_required_types(
            required_types=obligation.required_evidence_types,
            subject_key=obligation.primitive_ref,
            target=target,
            evidence_by_key=evidence_by_key,
        )
        passed = not missing
        return DoctrinePrimitiveResult(
            primitive_ref=obligation.primitive_ref,
            primitive_family=obligation.primitive_family,
            passed=passed,
            evidence_refs=evidence_refs,
            missing_evidence_types=missing,
            hard_failure_code=None if passed else obligation.hard_failure_code,
            approval_blocker_code=None if passed else obligation.approval_blocker_code,
        )

    def _evaluate_negative_fixture(
        self,
        fixture: DoctrineNegativeFixture,
        target: DoctrineTestTarget,
        evidence_by_key: dict[str, list[str]],
        observed_text: str,
    ) -> DoctrineNegativeFixtureResult:
        lowered = observed_text.lower()
        triggered_terms = [
            term
            for term in fixture.required_absent_terms
            if term.lower() in lowered
        ]
        evidence_refs, missing = self._evidence_for_required_types(
            required_types=fixture.required_evidence_types,
            subject_key=fixture.fixture_id,
            target=target,
            evidence_by_key=evidence_by_key,
        )
        passed = not triggered_terms and not missing
        return DoctrineNegativeFixtureResult(
            fixture_id=fixture.fixture_id,
            forbidden_shortcut=fixture.forbidden_shortcut,
            passed=passed,
            evidence_refs=evidence_refs,
            triggered_terms=triggered_terms,
            missing_evidence_types=missing,
            hard_failure_code=None if passed else fixture.hard_failure_code,
            approval_blocker_code=None if passed else fixture.approval_blocker_code,
        )

    def _evidence_for_required_types(
        self,
        *,
        required_types: list[str],
        subject_key: str,
        target: DoctrineTestTarget,
        evidence_by_key: dict[str, list[str]],
    ) -> tuple[list[str], list[str]]:
        evidence_refs: list[str] = []
        missing: list[str] = []
        subject_refs = evidence_by_key.get(subject_key, [])
        for required_type in required_types:
            refs = [
                *evidence_by_key.get(required_type, []),
                *[
                    ref
                    for ref in subject_refs
                    if required_type.lower() in ref.lower()
                ],
                *[
                    ref
                    for ref in target.lineage_refs
                    if required_type.lower() in ref.lower()
                ],
            ]
            if refs:
                evidence_refs.extend(refs)
            else:
                missing.append(required_type)
        return _unique(evidence_refs), missing

    @staticmethod
    def _applies_to_target(invariant: DoctrineInvariant, target_type: str) -> bool:
        return "*" in invariant.applies_to_target_types or target_type in invariant.applies_to_target_types

    @staticmethod
    def _spec_marker_evidence(spec_text: str, spec_path: str) -> dict[str, list[str]]:
        evidence: dict[str, list[str]] = {}
        for marker, needles in SPEC_AUDIT_REQUIRED_MARKERS.items():
            if any(needle in spec_text for needle in needles):
                evidence[marker] = [f"spec:{spec_path}:{marker}"]
        return evidence


@dataclass
class DoctrineTestHarnessCommandHandler:
    command_type: str
    service: DoctrineTestHarnessService
    aggregate_type: str = "doctrine_test_run"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "RegisterDoctrineInvariantCommand":
            invariant = self.service.register_invariant(DoctrineInvariant(**payload["invariant"]))
            return invariant.model_dump(mode="json")
        if self.command_type == "RunDoctrineTestSuiteCommand":
            receipt = self.service.run_suite(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                target=DoctrineTestTarget(**payload["target"]),
                actor_id=envelope.actor.actor_id,
                invariants=[
                    DoctrineInvariant(**item)
                    for item in payload.get("invariants", [])
                ] or None,
                primitive_obligations=[
                    DoctrinePrimitiveTestObligation(**item)
                    for item in payload.get("primitive_obligations", [])
                ],
                negative_fixtures=[
                    DoctrineNegativeFixture(**item)
                    for item in payload.get("negative_fixtures", [])
                ],
                evidence_by_key=payload.get("evidence_by_key", {}),
                observed_text=payload.get("observed_text"),
                command_id=envelope.command_id,
            )
            return receipt.model_dump(mode="json")
        if self.command_type == "AuditSpecDoctrineBindingCommand":
            receipt = self.service.audit_spec_file(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                spec_path=payload["spec_path"],
                spec_id=payload.get("spec_id"),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            )
            return receipt.model_dump(mode="json")
        raise DoctrineTestHarnessError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("doctrine_test_run_receipt_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        target = payload.get("target")
        if isinstance(target, dict) and target.get("target_id"):
            return UUID(target["target_id"])
        return envelope.brand_id


def register_doctrine_test_harness_command_handlers(
    bus: CommandBus,
    service: DoctrineTestHarnessService,
) -> None:
    for command_type in [
        "RegisterDoctrineInvariantCommand",
        "RunDoctrineTestSuiteCommand",
        "AuditSpecDoctrineBindingCommand",
    ]:
        bus.register_handler(
            DoctrineTestHarnessCommandHandler(command_type=command_type, service=service)
        )


def _normalize_evidence(evidence_by_key: dict[str, list[str]]) -> dict[str, list[str]]:
    return {
        key: [str(item) for item in refs]
        for key, refs in evidence_by_key.items()
    }


def _uuid_from_text(text: str) -> UUID:
    from uuid import UUID

    digest = sha256(text.encode("utf-8")).hexdigest()
    return UUID(digest[:32])


def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    values: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            values.append(item)
    return values
