from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
import json

from cmf_builder.domain.capability_ownership import (
    EXPECTED_CAPABILITIES,
    SYNTHETIC_TARGET_PROFILE_REF,
    CapabilityOwnerKind,
    CapabilityOwnershipDecision,
    CapabilityOwnershipGraph,
)


RESPONSIBILITY_MODULE_SCHEMA_ID = "cmf-builder-responsibility-module-graph/v1"
RESPONSIBILITY_MODULE_SCHEMA_VERSION = "1.0.0"
RESPONSIBILITY_MODULE_RECEIPT_SCHEMA_ID = (
    "cmf-builder-responsibility-module-receipt/v1"
)
MODULE_COMPILATION_INPUT_PATH = (
    "development-capsules/ST-04.02/MODULE_COMPILATION_INPUT.json"
)
MODULE_COMPILATION_INPUT_SHA256 = (
    "ebfbe43bfee4bd9b8ef210dc2dd4eda50be050b9dfb2b7e66f432c8cce352d00"
)
MODULE_COMPILATION_INPUT_SCHEMA = (
    "cmf-builder-synthetic-module-compilation-input/v1"
)
RESPONSIBILITY_MODULE_SCOPE = "ST-04.02_SYNTHETIC_CORE_ONLY"
CAPABILITY_OWNERSHIP_CONTRACT = "cmf-builder-capability-ownership/v1@1.0.0"

TECHNICAL_LAYER_IDENTITIES = frozenset(
    {
        "adapter",
        "agent",
        "api",
        "database",
        "infrastructure",
        "queue",
        "router",
        "ui",
        "worker",
    }
)


class ResponsibilityModuleError(Exception):
    code = "ResponsibilityModuleError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class ModuleInputInvalid(ResponsibilityModuleError):
    code = "ModuleInputInvalid"


class ModuleCoverageInvalid(ResponsibilityModuleError):
    code = "ModuleCoverageInvalid"


class ModuleBoundaryInvalid(ResponsibilityModuleError):
    code = "ModuleBoundaryInvalid"


class ModuleDependencyInvalid(ResponsibilityModuleError):
    code = "ModuleDependencyInvalid"


class ResponsibilityModuleInvalidatedError(ResponsibilityModuleError):
    code = "ResponsibilityModulesInvalidated"


def _nonempty_unique(values: tuple[str, ...], label: str) -> None:
    if (
        not values
        or any(not value.strip() for value in values)
        or len(set(values)) != len(values)
    ):
        raise ModuleBoundaryInvalid(f"{label} must be a non-empty unique list.")


@dataclass(frozen=True, slots=True)
class ModulePublicContract:
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    side_effects: tuple[str, ...]

    def __post_init__(self) -> None:
        _nonempty_unique(self.inputs, "Module inputs")
        _nonempty_unique(self.outputs, "Module outputs")
        if self.side_effects:
            raise ModuleBoundaryInvalid(
                "The synthetic responsibility modules permit no side effects.",
                side_effects=self.side_effects,
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
            "side_effects": list(self.side_effects),
        }


@dataclass(frozen=True, slots=True)
class ModuleTestSeam:
    public_command: str
    expected_fixtures: tuple[str, ...]
    contract_tests: tuple[str, ...]
    failure_injections: tuple[str, ...]
    observable_outputs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.public_command.strip():
            raise ModuleBoundaryInvalid("A module test seam needs a public command.")
        for label, values in (
            ("Expected fixtures", self.expected_fixtures),
            ("Contract tests", self.contract_tests),
            ("Failure injections", self.failure_injections),
            ("Observable outputs", self.observable_outputs),
        ):
            _nonempty_unique(values, label)

    def canonical_dict(self) -> dict[str, object]:
        return {
            "public_command": self.public_command,
            "expected_fixtures": list(self.expected_fixtures),
            "contract_tests": list(self.contract_tests),
            "failure_injections": list(self.failure_injections),
            "observable_outputs": list(self.observable_outputs),
        }


@dataclass(frozen=True, slots=True)
class ResponsibilityModule:
    module_id: str
    responsibility: str
    owned_capabilities: tuple[str, ...]
    public_contract: ModulePublicContract
    invariants: tuple[str, ...]
    exclusions: tuple[str, ...]
    dependencies: tuple[str, ...]
    failure_owner: str
    failure_modes: tuple[str, ...]
    boundary_rationale: str
    test_seam: ModuleTestSeam

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.module_id,
                self.responsibility,
                self.failure_owner,
                self.boundary_rationale,
            )
        ):
            raise ModuleBoundaryInvalid("Module identity and responsibility are required.")
        identity_words = set(
            self.module_id.lower().removesuffix("_module").replace("-", "_").split("_")
        )
        responsibility_words = set(
            self.responsibility.lower().replace("-", "_").split("_")
        )
        if (
            identity_words
            and identity_words <= TECHNICAL_LAYER_IDENTITIES
            or responsibility_words
            and responsibility_words <= TECHNICAL_LAYER_IDENTITIES
        ):
            raise ModuleBoundaryInvalid(
                "A module cannot be defined only by a horizontal technical layer.",
                module_id=self.module_id,
            )
        for label, values in (
            ("Owned capabilities", self.owned_capabilities),
            ("Invariants", self.invariants),
            ("Exclusions", self.exclusions),
            ("Failure modes", self.failure_modes),
        ):
            _nonempty_unique(values, label)
        if (
            any(not value.strip() for value in self.dependencies)
            or len(set(self.dependencies)) != len(self.dependencies)
            or self.module_id in self.dependencies
        ):
            raise ModuleDependencyInvalid(
                "Module dependencies must be unique and cannot include self edges.",
                module_id=self.module_id,
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "module_id": self.module_id,
            "responsibility": self.responsibility,
            "owned_capabilities": list(self.owned_capabilities),
            "public_contract": self.public_contract.canonical_dict(),
            "invariants": list(self.invariants),
            "exclusions": list(self.exclusions),
            "dependencies": list(self.dependencies),
            "failure_owner": self.failure_owner,
            "failure_modes": list(self.failure_modes),
            "boundary_rationale": self.boundary_rationale,
            "test_seam": self.test_seam.canonical_dict(),
        }


@dataclass(frozen=True, slots=True)
class ResponsibilityModuleGraph:
    graph_id: str
    graph_hash: str
    schema_id: str
    schema_version: str
    scope: str
    run_id: str
    target_profile_ref: str
    capability_graph_id: str
    capability_graph_hash: str
    ir_id: str
    ir_hash: str
    source_lock_ref: str
    boundary_ref: str
    ratification_ref: str
    model_ref: str
    artifact_set_id: str
    constitutional_report_id: str
    constitutional_report_hash: str
    constitutional_receipt_id: str
    constitutional_receipt_hash: str
    authority_identity: str
    module_input_path: str
    module_input_hash: str
    capability_ownerships: tuple[CapabilityOwnershipDecision, ...]
    modules: tuple[ResponsibilityModule, ...]
    implicit_modules_allowed: bool
    production_eligible: bool
    certified: bool
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        capability_graph: CapabilityOwnershipGraph,
        modules: tuple[ResponsibilityModule, ...],
        authority_identity: str,
    ) -> "ResponsibilityModuleGraph":
        capability_graph.validate()
        candidate = cls(
            graph_id="pending",
            graph_hash="pending",
            schema_id=RESPONSIBILITY_MODULE_SCHEMA_ID,
            schema_version=RESPONSIBILITY_MODULE_SCHEMA_VERSION,
            scope=RESPONSIBILITY_MODULE_SCOPE,
            run_id=capability_graph.run_id,
            target_profile_ref=capability_graph.target_profile_ref,
            capability_graph_id=capability_graph.graph_id,
            capability_graph_hash=capability_graph.graph_hash,
            ir_id=capability_graph.ir_id,
            ir_hash=capability_graph.ir_hash,
            source_lock_ref=capability_graph.source_lock_ref,
            boundary_ref=capability_graph.boundary_ref,
            ratification_ref=capability_graph.ratification_ref,
            model_ref=capability_graph.model_ref,
            artifact_set_id=capability_graph.artifact_set_id,
            constitutional_report_id=capability_graph.constitutional_report_id,
            constitutional_report_hash=capability_graph.constitutional_report_hash,
            constitutional_receipt_id=capability_graph.constitutional_receipt_id,
            constitutional_receipt_hash=capability_graph.constitutional_receipt_hash,
            authority_identity=authority_identity,
            module_input_path=MODULE_COMPILATION_INPUT_PATH,
            module_input_hash=f"sha256:{MODULE_COMPILATION_INPUT_SHA256}",
            capability_ownerships=capability_graph.decisions,
            modules=tuple(sorted(modules, key=lambda item: item.module_id)),
            implicit_modules_allowed=False,
            production_eligible=False,
            certified=False,
            outcome="PASS",
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            graph_id=f"responsibility-module-graph_{digest}",
            graph_hash=f"sha256:{digest}",
        )
        result.validate(capability_graph)
        return result

    @property
    def module_ids(self) -> tuple[str, ...]:
        return tuple(module.module_id for module in self.modules)

    @property
    def capability_ids(self) -> tuple[str, ...]:
        return tuple(
            capability
            for module in self.modules
            for capability in module.owned_capabilities
        )

    @property
    def dependency_count(self) -> int:
        return sum(len(module.dependencies) for module in self.modules)

    def validate(self, capability_graph: CapabilityOwnershipGraph) -> None:
        capability_graph.validate()
        for module in self.modules:
            module.__post_init__()
        if (
            self.schema_id != RESPONSIBILITY_MODULE_SCHEMA_ID
            or self.schema_version != RESPONSIBILITY_MODULE_SCHEMA_VERSION
            or self.scope != RESPONSIBILITY_MODULE_SCOPE
            or self.target_profile_ref != SYNTHETIC_TARGET_PROFILE_REF
            or self.module_input_path != MODULE_COMPILATION_INPUT_PATH
            or self.module_input_hash != f"sha256:{MODULE_COMPILATION_INPUT_SHA256}"
            or self.run_id != capability_graph.run_id
            or self.capability_graph_id != capability_graph.graph_id
            or self.capability_graph_hash != capability_graph.graph_hash
            or self.ir_id != capability_graph.ir_id
            or self.ir_hash != capability_graph.ir_hash
            or self.source_lock_ref != capability_graph.source_lock_ref
            or self.boundary_ref != capability_graph.boundary_ref
            or self.ratification_ref != capability_graph.ratification_ref
            or self.model_ref != capability_graph.model_ref
            or self.artifact_set_id != capability_graph.artifact_set_id
            or self.constitutional_report_id
            != capability_graph.constitutional_report_id
            or self.constitutional_report_hash
            != capability_graph.constitutional_report_hash
            or self.constitutional_receipt_id
            != capability_graph.constitutional_receipt_id
            or self.constitutional_receipt_hash
            != capability_graph.constitutional_receipt_hash
            or self.capability_ownerships != capability_graph.decisions
            or not self.authority_identity.strip()
            or not self.modules
            or self.module_ids != tuple(sorted(self.module_ids))
            or len(set(self.module_ids)) != len(self.module_ids)
            or tuple(sorted(self.capability_ids)) != EXPECTED_CAPABILITIES
            or len(set(self.capability_ids)) != len(self.capability_ids)
            or self.implicit_modules_allowed
            or self.production_eligible
            or self.certified
            or self.outcome != "PASS"
        ):
            raise ModuleCoverageInvalid(
                "Responsibility module graph coverage, lineage, or scope is invalid."
            )
        decisions = {item.capability_id: item for item in self.capability_ownerships}
        module_by_id = {item.module_id: item for item in self.modules}
        for module in self.modules:
            owners = {decisions[item].owner_kind for item in module.owned_capabilities}
            owner_ids = {decisions[item].owner_id for item in module.owned_capabilities}
            if len(owners) != 1:
                raise ModuleBoundaryInvalid(
                    "A module cannot silently mix capability owner kinds.",
                    module_id=module.module_id,
                )
            if module.failure_owner not in owner_ids:
                raise ModuleBoundaryInvalid(
                    "Failure ownership must be attributable to an owned capability.",
                    module_id=module.module_id,
                )
            if any(dependency not in module_by_id for dependency in module.dependencies):
                raise ModuleDependencyInvalid(
                    "A module dependency does not resolve.", module_id=module.module_id
                )
        self._validate_acyclic(module_by_id)
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.graph_id != f"responsibility-module-graph_{digest}"
            or self.graph_hash != f"sha256:{digest}"
        ):
            raise ModuleCoverageInvalid("Responsibility module graph hash is invalid.")

    @staticmethod
    def _validate_acyclic(modules: dict[str, ResponsibilityModule]) -> None:
        visited: set[str] = set()
        active: set[str] = set()

        def visit(module_id: str) -> None:
            if module_id in active:
                raise ModuleDependencyInvalid("Module dependency graph contains a cycle.")
            if module_id in visited:
                return
            active.add(module_id)
            for dependency in modules[module_id].dependencies:
                visit(dependency)
            active.remove(module_id)
            visited.add(module_id)

        for module_id in sorted(modules):
            visit(module_id)

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "scope": self.scope,
            "run_id": self.run_id,
            "target_profile_ref": self.target_profile_ref,
            "capability_graph_id": self.capability_graph_id,
            "capability_graph_hash": self.capability_graph_hash,
            "ir_id": self.ir_id,
            "ir_hash": self.ir_hash,
            "source_lock_ref": self.source_lock_ref,
            "boundary_ref": self.boundary_ref,
            "ratification_ref": self.ratification_ref,
            "model_ref": self.model_ref,
            "artifact_set_id": self.artifact_set_id,
            "constitutional_report_id": self.constitutional_report_id,
            "constitutional_report_hash": self.constitutional_report_hash,
            "constitutional_receipt_id": self.constitutional_receipt_id,
            "constitutional_receipt_hash": self.constitutional_receipt_hash,
            "authority_identity": self.authority_identity,
            "module_input_path": self.module_input_path,
            "module_input_hash": self.module_input_hash,
            "capability_ownerships": [
                item.canonical_dict() for item in self.capability_ownerships
            ],
            "modules": [item.canonical_dict() for item in self.modules],
            "implicit_modules_allowed": self.implicit_modules_allowed,
            "production_eligible": self.production_eligible,
            "certified": self.certified,
            "outcome": self.outcome,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class ResponsibilityModuleReceipt:
    receipt_id: str
    receipt_hash: str
    schema_id: str
    command_id: str
    run_id: str
    graph_id: str
    graph_hash: str
    capability_graph_id: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    module_count: int
    capability_coverage_count: int
    contract_coverage_count: int
    test_seam_coverage_count: int
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        graph: ResponsibilityModuleGraph,
        capability_graph: CapabilityOwnershipGraph,
        authority_identity: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "ResponsibilityModuleReceipt":
        graph.validate(capability_graph)
        candidate = cls(
            receipt_id="pending",
            receipt_hash="pending",
            schema_id=RESPONSIBILITY_MODULE_RECEIPT_SCHEMA_ID,
            command_id=command_id,
            run_id=graph.run_id,
            graph_id=graph.graph_id,
            graph_hash=graph.graph_hash,
            capability_graph_id=graph.capability_graph_id,
            authority_identity=authority_identity,
            event_ids=event_ids,
            stream_version=stream_version,
            module_count=len(graph.modules),
            capability_coverage_count=len(graph.capability_ids),
            contract_coverage_count=len(graph.modules),
            test_seam_coverage_count=len(graph.modules),
            outcome="PASS",
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            receipt_id=f"responsibility-module-receipt_{digest}",
            receipt_hash=f"sha256:{digest}",
        )
        result.validate(graph, capability_graph)
        return result

    def validate(
        self,
        graph: ResponsibilityModuleGraph,
        capability_graph: CapabilityOwnershipGraph,
    ) -> None:
        graph.validate(capability_graph)
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != RESPONSIBILITY_MODULE_RECEIPT_SCHEMA_ID
            or self.run_id != graph.run_id
            or self.graph_id != graph.graph_id
            or self.graph_hash != graph.graph_hash
            or self.capability_graph_id != graph.capability_graph_id
            or not self.authority_identity.strip()
            or len(self.event_ids) != 1
            or self.module_count != len(graph.modules)
            or self.capability_coverage_count != len(graph.capability_ids)
            or self.contract_coverage_count != len(graph.modules)
            or self.test_seam_coverage_count != len(graph.modules)
            or self.outcome != "PASS"
            or self.receipt_id != f"responsibility-module-receipt_{digest}"
            or self.receipt_hash != f"sha256:{digest}"
        ):
            raise ResponsibilityModuleError(
                "Responsibility module receipt does not match its graph."
            )

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "schema_id": self.schema_id,
                "command_id": self.command_id,
                "run_id": self.run_id,
                "graph_id": self.graph_id,
                "graph_hash": self.graph_hash,
                "capability_graph_id": self.capability_graph_id,
                "authority_identity": self.authority_identity,
                "event_ids": list(self.event_ids),
                "stream_version": self.stream_version,
                "module_count": self.module_count,
                "capability_coverage_count": self.capability_coverage_count,
                "contract_coverage_count": self.contract_coverage_count,
                "test_seam_coverage_count": self.test_seam_coverage_count,
                "outcome": self.outcome,
            }
        )


@dataclass(frozen=True, slots=True)
class ResponsibilityModuleInvalidation:
    invalidation_id: str
    invalidation_hash: str
    module_graph_ref: str
    capability_graph_ref: str
    upstream_invalidation_ref: str
    reason: str
    authority_identity: str

    @classmethod
    def create(
        cls,
        *,
        invalidation_id: str,
        module_graph_ref: str,
        capability_graph_ref: str,
        upstream_invalidation_ref: str,
        reason: str,
        authority_identity: str,
    ) -> "ResponsibilityModuleInvalidation":
        candidate = cls(
            invalidation_id=invalidation_id,
            invalidation_hash="pending",
            module_graph_ref=module_graph_ref,
            capability_graph_ref=capability_graph_ref,
            upstream_invalidation_ref=upstream_invalidation_ref,
            reason=reason,
            authority_identity=authority_identity,
        )
        if not all(
            value.strip()
            for value in (
                invalidation_id,
                module_graph_ref,
                capability_graph_ref,
                upstream_invalidation_ref,
                reason,
                authority_identity,
            )
        ):
            raise ResponsibilityModuleError(
                "Responsibility module invalidation identity is incomplete."
            )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(candidate, invalidation_hash=f"sha256:{digest}")

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "invalidation_id": self.invalidation_id,
                "module_graph_ref": self.module_graph_ref,
                "capability_graph_ref": self.capability_graph_ref,
                "upstream_invalidation_ref": self.upstream_invalidation_ref,
                "reason": self.reason,
                "authority_identity": self.authority_identity,
            }
        )


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
