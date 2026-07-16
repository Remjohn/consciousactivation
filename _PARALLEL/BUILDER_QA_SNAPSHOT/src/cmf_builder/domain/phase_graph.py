from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
import json

from cmf_builder.domain.responsibility_modules import (
    ResponsibilityModule,
    ResponsibilityModuleGraph,
)


PHASE_GRAPH_SCHEMA_ID = "cmf-builder-phase-graph/v1"
PHASE_GRAPH_SCHEMA_VERSION = "1.0.0"
PHASE_GRAPH_RECEIPT_SCHEMA_ID = "cmf-builder-phase-graph-receipt/v1"
PHASE_GRAPH_INPUT_PATH = "development-capsules/ST-04.03/PHASE_GRAPH_INPUT.json"
PHASE_GRAPH_INPUT_SHA256 = (
    "5702b46f57f6fb898199a4faf05dc889daf91a99ca3bd70925d3903c22f0e009"
)
PHASE_GRAPH_INPUT_SCHEMA = "cmf-builder-synthetic-phase-graph-input/v1"
PHASE_GRAPH_SCOPE = "ST-04.03_SYNTHETIC_CORE_ONLY"
RESPONSIBILITY_MODULE_CONTRACT = (
    "cmf-builder-responsibility-module-graph/v1@1.0.0"
)
DETERMINISTIC_EXECUTION_KIND = "DETERMINISTIC_CODE"


class PhaseGraphError(Exception):
    code = "PhaseGraphError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class PhaseGraphInputInvalid(PhaseGraphError):
    code = "PhaseGraphInputInvalid"


class PhaseCoverageInvalid(PhaseGraphError):
    code = "PhaseCoverageInvalid"


class PhaseDependencyInvalid(PhaseGraphError):
    code = "PhaseDependencyInvalid"


class PhaseAuthorityInvalid(PhaseGraphError):
    code = "PhaseAuthorityInvalid"


class PhaseGraphInvalidatedError(PhaseGraphError):
    code = "PhaseGraphInvalidated"


def _nonempty_unique(values: tuple[str, ...], label: str) -> None:
    if (
        not values
        or any(not value.strip() for value in values)
        or len(set(values)) != len(values)
    ):
        raise PhaseCoverageInvalid(f"{label} must be a non-empty unique list.")


@dataclass(frozen=True, slots=True)
class PhaseNode:
    phase_id: str
    responsibility: str
    module_refs: tuple[str, ...]
    dependencies: tuple[str, ...]
    parallel_with: tuple[str, ...]
    entry_conditions: tuple[str, ...]
    exit_evidence: tuple[str, ...]
    failure_owner: str
    required_gates: tuple[str, ...]
    execution_kind: str

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.phase_id,
                self.responsibility,
                self.failure_owner,
                self.execution_kind,
            )
        ):
            raise PhaseCoverageInvalid(
                "Phase identity, responsibility, failure owner, and execution kind are required."
            )
        for label, values in (
            ("Module references", self.module_refs),
            ("Entry conditions", self.entry_conditions),
            ("Exit evidence", self.exit_evidence),
            ("Required gates", self.required_gates),
        ):
            _nonempty_unique(values, label)
        for label, values in (
            ("Dependencies", self.dependencies),
            ("Parallel declarations", self.parallel_with),
        ):
            if any(not value.strip() for value in values) or len(set(values)) != len(
                values
            ):
                raise PhaseDependencyInvalid(f"{label} must be unique and explicit.")
        if self.phase_id in self.dependencies or self.phase_id in self.parallel_with:
            raise PhaseDependencyInvalid("A phase cannot depend on or parallel itself.")
        if set(self.dependencies) & set(self.parallel_with):
            raise PhaseDependencyInvalid(
                "A phase cannot be both dependent on and parallel with the same phase."
            )
        if self.execution_kind != DETERMINISTIC_EXECUTION_KIND:
            raise PhaseAuthorityInvalid(
                "The bounded Phase Graph permits deterministic Builder code only.",
                execution_kind=self.execution_kind,
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "phase_id": self.phase_id,
            "responsibility": self.responsibility,
            "module_refs": list(self.module_refs),
            "dependencies": list(self.dependencies),
            "parallel_with": list(self.parallel_with),
            "entry_conditions": list(self.entry_conditions),
            "exit_evidence": list(self.exit_evidence),
            "failure_owner": self.failure_owner,
            "required_gates": list(self.required_gates),
            "execution_kind": self.execution_kind,
        }


@dataclass(frozen=True, slots=True)
class PhaseExecutionPlan:
    topological_order: tuple[str, ...]
    initially_runnable: tuple[str, ...]
    blocked_by: tuple[tuple[str, tuple[str, ...]], ...]
    parallel_pairs: tuple[tuple[str, str], ...]

    @classmethod
    def create(cls, phases: tuple[PhaseNode, ...]) -> "PhaseExecutionPlan":
        by_id = {phase.phase_id: phase for phase in phases}
        if len(by_id) != len(phases):
            raise PhaseCoverageInvalid("Phase identities must be unique.")
        for phase in phases:
            if any(dependency not in by_id for dependency in phase.dependencies):
                raise PhaseDependencyInvalid(
                    "A phase dependency does not resolve.", phase_id=phase.phase_id
                )
            if any(candidate not in by_id for candidate in phase.parallel_with):
                raise PhaseDependencyInvalid(
                    "A parallel phase declaration does not resolve.",
                    phase_id=phase.phase_id,
                )
        initially_runnable = tuple(
            sorted(phase.phase_id for phase in phases if not phase.dependencies)
        )
        remaining = {phase.phase_id: set(phase.dependencies) for phase in phases}
        order: list[str] = []
        while remaining:
            ready = sorted(
                phase_id
                for phase_id, dependencies in remaining.items()
                if dependencies <= set(order)
            )
            if not ready:
                raise PhaseDependencyInvalid("Phase dependency graph contains a cycle.")
            phase_id = ready[0]
            order.append(phase_id)
            del remaining[phase_id]
        parallel_pairs: set[tuple[str, str]] = set()
        for phase in phases:
            for other_id in phase.parallel_with:
                other = by_id[other_id]
                if phase.phase_id not in other.parallel_with:
                    raise PhaseDependencyInvalid(
                        "Parallel declarations must be symmetric.",
                        phase_id=phase.phase_id,
                        other_phase_id=other_id,
                    )
                if (
                    phase.required_gates != other.required_gates
                    or _reachable(phase.phase_id, other_id, by_id)
                    or _reachable(other_id, phase.phase_id, by_id)
                ):
                    raise PhaseDependencyInvalid(
                        "Parallel phases must be dependency-independent and gate-compatible.",
                        phase_id=phase.phase_id,
                        other_phase_id=other_id,
                    )
                parallel_pairs.add(tuple(sorted((phase.phase_id, other_id))))
        return cls(
            topological_order=tuple(order),
            initially_runnable=initially_runnable,
            blocked_by=tuple(
                sorted(
                    (phase.phase_id, tuple(sorted(phase.dependencies)))
                    for phase in phases
                    if phase.dependencies
                )
            ),
            parallel_pairs=tuple(sorted(parallel_pairs)),
        )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "topological_order": list(self.topological_order),
            "initially_runnable": list(self.initially_runnable),
            "blocked_by": [
                {"phase_id": phase_id, "dependencies": list(dependencies)}
                for phase_id, dependencies in self.blocked_by
            ],
            "parallel_pairs": [list(pair) for pair in self.parallel_pairs],
        }


@dataclass(frozen=True, slots=True)
class PhaseGraph:
    graph_id: str
    graph_hash: str
    schema_id: str
    schema_version: str
    scope: str
    run_id: str
    target_profile_ref: str
    module_graph_id: str
    module_graph_hash: str
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
    phase_input_path: str
    phase_input_hash: str
    modules: tuple[ResponsibilityModule, ...]
    phases: tuple[PhaseNode, ...]
    execution_plan: PhaseExecutionPlan
    implicit_phases_allowed: bool
    default_parallelism_allowed: bool
    production_eligible: bool
    certified: bool
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        module_graph: ResponsibilityModuleGraph,
        phases: tuple[PhaseNode, ...],
        authority_identity: str,
    ) -> "PhaseGraph":
        plan = PhaseExecutionPlan.create(phases)
        candidate = cls(
            graph_id="pending",
            graph_hash="pending",
            schema_id=PHASE_GRAPH_SCHEMA_ID,
            schema_version=PHASE_GRAPH_SCHEMA_VERSION,
            scope=PHASE_GRAPH_SCOPE,
            run_id=module_graph.run_id,
            target_profile_ref=module_graph.target_profile_ref,
            module_graph_id=module_graph.graph_id,
            module_graph_hash=module_graph.graph_hash,
            capability_graph_id=module_graph.capability_graph_id,
            capability_graph_hash=module_graph.capability_graph_hash,
            ir_id=module_graph.ir_id,
            ir_hash=module_graph.ir_hash,
            source_lock_ref=module_graph.source_lock_ref,
            boundary_ref=module_graph.boundary_ref,
            ratification_ref=module_graph.ratification_ref,
            model_ref=module_graph.model_ref,
            artifact_set_id=module_graph.artifact_set_id,
            constitutional_report_id=module_graph.constitutional_report_id,
            constitutional_report_hash=module_graph.constitutional_report_hash,
            constitutional_receipt_id=module_graph.constitutional_receipt_id,
            constitutional_receipt_hash=module_graph.constitutional_receipt_hash,
            authority_identity=authority_identity,
            phase_input_path=PHASE_GRAPH_INPUT_PATH,
            phase_input_hash=f"sha256:{PHASE_GRAPH_INPUT_SHA256}",
            modules=module_graph.modules,
            phases=tuple(sorted(phases, key=lambda phase: phase.phase_id)),
            execution_plan=plan,
            implicit_phases_allowed=False,
            default_parallelism_allowed=False,
            production_eligible=False,
            certified=False,
            outcome="PASS",
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            graph_id=f"phase-graph_{digest}",
            graph_hash=f"sha256:{digest}",
        )
        result.validate(module_graph)
        return result

    @property
    def phase_ids(self) -> tuple[str, ...]:
        return tuple(phase.phase_id for phase in self.phases)

    @property
    def module_refs(self) -> tuple[str, ...]:
        return tuple(reference for phase in self.phases for reference in phase.module_refs)

    @property
    def dependency_count(self) -> int:
        return sum(len(phase.dependencies) for phase in self.phases)

    @property
    def gate_count(self) -> int:
        return sum(len(phase.required_gates) for phase in self.phases)

    def validate(self, module_graph: ResponsibilityModuleGraph) -> None:
        module_by_id = {module.module_id: module for module in module_graph.modules}
        for phase in self.phases:
            phase.__post_init__()
        if (
            self.schema_id != PHASE_GRAPH_SCHEMA_ID
            or self.schema_version != PHASE_GRAPH_SCHEMA_VERSION
            or self.scope != PHASE_GRAPH_SCOPE
            or self.phase_input_path != PHASE_GRAPH_INPUT_PATH
            or self.phase_input_hash != f"sha256:{PHASE_GRAPH_INPUT_SHA256}"
            or self.run_id != module_graph.run_id
            or self.target_profile_ref != module_graph.target_profile_ref
            or self.module_graph_id != module_graph.graph_id
            or self.module_graph_hash != module_graph.graph_hash
            or self.capability_graph_id != module_graph.capability_graph_id
            or self.capability_graph_hash != module_graph.capability_graph_hash
            or self.ir_id != module_graph.ir_id
            or self.ir_hash != module_graph.ir_hash
            or self.source_lock_ref != module_graph.source_lock_ref
            or self.boundary_ref != module_graph.boundary_ref
            or self.ratification_ref != module_graph.ratification_ref
            or self.model_ref != module_graph.model_ref
            or self.artifact_set_id != module_graph.artifact_set_id
            or self.constitutional_report_id != module_graph.constitutional_report_id
            or self.constitutional_report_hash != module_graph.constitutional_report_hash
            or self.constitutional_receipt_id != module_graph.constitutional_receipt_id
            or self.constitutional_receipt_hash != module_graph.constitutional_receipt_hash
            or self.modules != module_graph.modules
            or not self.authority_identity.strip()
            or not self.phases
            or self.phase_ids != tuple(sorted(self.phase_ids))
            or len(set(self.phase_ids)) != len(self.phase_ids)
            or tuple(sorted(self.module_refs)) != tuple(sorted(module_by_id))
            or len(set(self.module_refs)) != len(self.module_refs)
            or self.implicit_phases_allowed
            or self.default_parallelism_allowed
            or self.production_eligible
            or self.certified
            or self.outcome != "PASS"
        ):
            raise PhaseCoverageInvalid(
                "Phase Graph coverage, lineage, identity, or scope is invalid."
            )
        for phase in self.phases:
            selected = [module_by_id.get(reference) for reference in phase.module_refs]
            if any(module is None for module in selected):
                raise PhaseCoverageInvalid(
                    "A phase references an undeclared module.", phase_id=phase.phase_id
                )
            modules = tuple(module for module in selected if module is not None)
            failure_owners = {module.failure_owner for module in modules}
            if len(failure_owners) != 1 or phase.failure_owner not in failure_owners:
                raise PhaseAuthorityInvalid(
                    "Phase failure ownership must preserve its owning module authority.",
                    phase_id=phase.phase_id,
                )
            allowed_evidence = {
                output
                for module in modules
                for output in (
                    *module.public_contract.outputs,
                    *module.test_seam.observable_outputs,
                )
            }
            if not set(phase.exit_evidence) <= allowed_evidence:
                raise PhaseCoverageInvalid(
                    "Phase completion evidence is not owned by its declared modules.",
                    phase_id=phase.phase_id,
                )
        expected_plan = PhaseExecutionPlan.create(self.phases)
        if self.execution_plan != expected_plan:
            raise PhaseDependencyInvalid("Phase execution-plan projection has drifted.")
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.graph_id != f"phase-graph_{digest}"
            or self.graph_hash != f"sha256:{digest}"
        ):
            raise PhaseCoverageInvalid("Phase Graph content identity is invalid.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "scope": self.scope,
            "run_id": self.run_id,
            "target_profile_ref": self.target_profile_ref,
            "module_graph_id": self.module_graph_id,
            "module_graph_hash": self.module_graph_hash,
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
            "phase_input_path": self.phase_input_path,
            "phase_input_hash": self.phase_input_hash,
            "modules": [module.canonical_dict() for module in self.modules],
            "phases": [phase.canonical_dict() for phase in self.phases],
            "execution_plan": self.execution_plan.canonical_dict(),
            "implicit_phases_allowed": self.implicit_phases_allowed,
            "default_parallelism_allowed": self.default_parallelism_allowed,
            "production_eligible": self.production_eligible,
            "certified": self.certified,
            "outcome": self.outcome,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class PhaseGraphReceipt:
    receipt_id: str
    receipt_hash: str
    schema_id: str
    command_id: str
    run_id: str
    graph_id: str
    graph_hash: str
    module_graph_id: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    phase_count: int
    module_coverage_count: int
    dependency_count: int
    gate_count: int
    initially_runnable_count: int
    blocked_count: int
    parallel_pair_count: int
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        graph: PhaseGraph,
        module_graph: ResponsibilityModuleGraph,
        authority_identity: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "PhaseGraphReceipt":
        graph.validate(module_graph)
        candidate = cls(
            receipt_id="pending",
            receipt_hash="pending",
            schema_id=PHASE_GRAPH_RECEIPT_SCHEMA_ID,
            command_id=command_id,
            run_id=graph.run_id,
            graph_id=graph.graph_id,
            graph_hash=graph.graph_hash,
            module_graph_id=graph.module_graph_id,
            authority_identity=authority_identity,
            event_ids=event_ids,
            stream_version=stream_version,
            phase_count=len(graph.phases),
            module_coverage_count=len(graph.module_refs),
            dependency_count=graph.dependency_count,
            gate_count=graph.gate_count,
            initially_runnable_count=len(graph.execution_plan.initially_runnable),
            blocked_count=len(graph.execution_plan.blocked_by),
            parallel_pair_count=len(graph.execution_plan.parallel_pairs),
            outcome="PASS",
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            receipt_id=f"phase-graph-receipt_{digest}",
            receipt_hash=f"sha256:{digest}",
        )
        result.validate(graph, module_graph)
        return result

    def validate(
        self, graph: PhaseGraph, module_graph: ResponsibilityModuleGraph
    ) -> None:
        graph.validate(module_graph)
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != PHASE_GRAPH_RECEIPT_SCHEMA_ID
            or self.run_id != graph.run_id
            or self.graph_id != graph.graph_id
            or self.graph_hash != graph.graph_hash
            or self.module_graph_id != graph.module_graph_id
            or not self.authority_identity.strip()
            or len(self.event_ids) != 1
            or self.phase_count != len(graph.phases)
            or self.module_coverage_count != len(graph.module_refs)
            or self.dependency_count != graph.dependency_count
            or self.gate_count != graph.gate_count
            or self.initially_runnable_count
            != len(graph.execution_plan.initially_runnable)
            or self.blocked_count != len(graph.execution_plan.blocked_by)
            or self.parallel_pair_count != len(graph.execution_plan.parallel_pairs)
            or self.outcome != "PASS"
            or self.receipt_id != f"phase-graph-receipt_{digest}"
            or self.receipt_hash != f"sha256:{digest}"
        ):
            raise PhaseGraphError("Phase Graph receipt does not match its graph.")

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "schema_id": self.schema_id,
                "command_id": self.command_id,
                "run_id": self.run_id,
                "graph_id": self.graph_id,
                "graph_hash": self.graph_hash,
                "module_graph_id": self.module_graph_id,
                "authority_identity": self.authority_identity,
                "event_ids": list(self.event_ids),
                "stream_version": self.stream_version,
                "phase_count": self.phase_count,
                "module_coverage_count": self.module_coverage_count,
                "dependency_count": self.dependency_count,
                "gate_count": self.gate_count,
                "initially_runnable_count": self.initially_runnable_count,
                "blocked_count": self.blocked_count,
                "parallel_pair_count": self.parallel_pair_count,
                "outcome": self.outcome,
            }
        )


@dataclass(frozen=True, slots=True)
class PhaseGraphInvalidation:
    invalidation_id: str
    invalidation_hash: str
    phase_graph_ref: str
    module_graph_ref: str
    upstream_invalidation_ref: str
    reason: str
    authority_identity: str

    @classmethod
    def create(
        cls,
        *,
        invalidation_id: str,
        phase_graph_ref: str,
        module_graph_ref: str,
        upstream_invalidation_ref: str,
        reason: str,
        authority_identity: str,
    ) -> "PhaseGraphInvalidation":
        candidate = cls(
            invalidation_id=invalidation_id,
            invalidation_hash="pending",
            phase_graph_ref=phase_graph_ref,
            module_graph_ref=module_graph_ref,
            upstream_invalidation_ref=upstream_invalidation_ref,
            reason=reason,
            authority_identity=authority_identity,
        )
        if not all(
            value.strip()
            for value in (
                invalidation_id,
                phase_graph_ref,
                module_graph_ref,
                upstream_invalidation_ref,
                reason,
                authority_identity,
            )
        ):
            raise PhaseGraphError("Phase Graph invalidation identity is incomplete.")
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(candidate, invalidation_hash=f"sha256:{digest}")

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "invalidation_id": self.invalidation_id,
                "phase_graph_ref": self.phase_graph_ref,
                "module_graph_ref": self.module_graph_ref,
                "upstream_invalidation_ref": self.upstream_invalidation_ref,
                "reason": self.reason,
                "authority_identity": self.authority_identity,
            }
        )


def _reachable(
    source_id: str, target_id: str, phases: dict[str, PhaseNode]
) -> bool:
    pending = list(phases[source_id].dependencies)
    seen: set[str] = set()
    while pending:
        current = pending.pop()
        if current == target_id:
            return True
        if current in seen:
            continue
        seen.add(current)
        pending.extend(phases[current].dependencies)
    return False


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
