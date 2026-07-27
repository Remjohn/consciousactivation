from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping

from cmf_builder.application.authority import Action, ActorKind, AuthorityService
from cmf_builder.application.ports import (
    AtomicCommitFailed,
    Clock,
    CommandRecord,
    ConcurrencyConflict,
    IdempotencyPayloadMismatch,
    ImplementationPlanRepository,
    Observation,
    ObservationSink,
)
from cmf_builder.domain.development_capsule import VersionedTraceableDevelopmentCapsule
from cmf_builder.domain.implementation_plan import (
    DIRECT_DEPENDENCIES,
    EXTERNAL_TARGET_COMPATIBILITY,
    OWNED_OBLIGATIONS,
    PLAN_INPUT_PATH,
    PLAN_INPUT_SHA256,
    PLAN_MODE,
    PLAN_OUTCOME,
    PLAN_PROFILE_ID,
    ImplementationPlanAuthorityInvalid,
    ImplementationPlanInputInvalid,
    ImplementationPlanInvalidatedError,
    ImplementationPlanReceipt,
    ImplementationPlanScopeInvalid,
    ImplementationPlanTraceInvalid,
    VerticalImplementationPlan,
)
from cmf_builder.domain.run import LifecycleState, Run


@dataclass(frozen=True, slots=True)
class CompileImplementationPlanCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    plan_input_path: str = PLAN_INPUT_PATH
    plan_input_sha256: str = PLAN_INPUT_SHA256
    requested_operation: str = "compile_dependency_ordered_vertical_plan"
    requested_mode: str = PLAN_MODE
    requested_profile_id: str = PLAN_PROFILE_ID
    requested_obligations: tuple[str, ...] = OWNED_OBLIGATIONS
    requested_dependencies: tuple[str, ...] = DIRECT_DEPENDENCIES
    requested_external_target_compatibility: str = EXTERNAL_TARGET_COMPATIBILITY
    requested_implementation_authorized: bool = False
    requested_production_eligible: bool = False
    requested_certified: bool = False
    requested_external_runtime_ids: tuple[str, ...] = ()
    requested_external_skill_ids: tuple[str, ...] = ()
    requested_increment_overrides: tuple[tuple[str, str], ...] = ()


class ImplementationPlanCommandService:
    STORY_ID = "ST-11.02"
    CONTRACT_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        root: Path,
        repository: ImplementationPlanRepository,
        authority: AuthorityService,
        clock: Clock,
        observations: ObservationSink,
    ) -> None:
        self._root = root.resolve()
        self._repository = repository
        self._authority = authority
        self._clock = clock
        self._observations = observations

    def compile(
        self, command: CompileImplementationPlanCommand
    ) -> ImplementationPlanReceipt:
        run: Run | None = None
        capsule: VersionedTraceableDevelopmentCapsule | None = None
        plan: VerticalImplementationPlan | None = None
        try:
            payload_hash = _command_hash(command)
            duplicate = self._duplicate(command.command_id, payload_hash)
            if duplicate is not None:
                self._emit_replay(command, duplicate)
                return duplicate
            self._validate_command(command)
            run = self._repository.load_run(command.run_id)
            self._require_version(command.expected_version, run)
            self._authorize_code(command.actor_id, command.run_id)
            capsule = self._load_active_capsule(run)
            plan_input = self._load_input(command)
            plan = VerticalImplementationPlan.create(
                capsule=capsule,
                plan_input=plan_input,
                authority_identity=command.actor_id,
            )
            receipt = ImplementationPlanReceipt.create(
                command_id=command.command_id,
                plan=plan,
                stream_version=run.stream_version,
            )
            self._repository.commit_implementation_plan(
                run_id=run.run_id,
                expected_version=command.expected_version,
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                plan=plan,
                receipt=receipt,
            )
            self._emit(
                event_name="implementation_plan_compilation_started",
                outcome="PASS",
                command=command,
                run=run,
                capsule=capsule,
                plan=plan,
                receipt=receipt,
                replay_status="NEW_COMMIT",
                failure_context={},
            )
            for increment in plan.increments:
                self._emit(
                    event_name="implementation_plan_increment_compiled",
                    outcome="PASS",
                    command=command,
                    run=run,
                    capsule=capsule,
                    plan=plan,
                    receipt=receipt,
                    replay_status="NEW_COMMIT",
                    failure_context={"increment_id": increment.increment_id},
                )
            self._emit(
                event_name="implementation_plan_compilation_committed",
                outcome="PASS",
                command=command,
                run=run,
                capsule=capsule,
                plan=plan,
                receipt=receipt,
                replay_status="NEW_COMMIT",
                failure_context={},
            )
            return receipt
        except Exception as error:
            if not isinstance(error, AtomicCommitFailed):
                self._emit(
                    event_name="implementation_plan_compilation_rejected",
                    outcome="FAIL",
                    command=command,
                    run=run,
                    capsule=capsule,
                    plan=plan,
                    receipt=None,
                    replay_status="NOT_COMMITTED",
                    failure_context={
                        "code": str(getattr(error, "code", type(error).__name__)),
                        "message": str(error),
                        **dict(getattr(error, "context", {})),
                    },
                )
            raise

    def get_active(self, run_id: str) -> VerticalImplementationPlan:
        run = self._repository.load_run(run_id)
        capsule = self._load_active_capsule(run)
        plans = self._repository.implementation_plans(run_id)
        if len(plans) != 1:
            raise ImplementationPlanInvalidatedError(
                "No single active implementation plan is available."
            )
        plan = plans[0]
        if self._repository.is_implementation_plan_invalidated(plan.plan_id):
            raise ImplementationPlanInvalidatedError(
                "The implementation plan parent capsule is invalidated."
            )
        plan.validate(capsule)
        return plan

    def get_historical(self, plan_id: str) -> VerticalImplementationPlan:
        plan = self._repository.get_implementation_plan(plan_id)
        if plan is None:
            raise KeyError(plan_id)
        capsule = self._repository.get_development_capsule(plan.capsule_id)
        if capsule is None:
            raise ImplementationPlanTraceInvalid(
                "Historical implementation plan parent is unavailable."
            )
        plan.validate(capsule)
        return plan

    def _load_active_capsule(self, run: Run) -> VersionedTraceableDevelopmentCapsule:
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.development_capsule_ref
            or not run.development_capsule_hash
            or run.development_capsule_invalidation_ref is not None
            or self._repository.is_development_capsule_invalidated(
                run.development_capsule_ref
            )
        ):
            raise ImplementationPlanInvalidatedError(
                "Implementation planning requires one active accepted Development Capsule."
            )
        capsule = self._repository.get_development_capsule(run.development_capsule_ref)
        receipts = self._repository.development_capsule_receipts(run.run_id)
        if (
            capsule is None
            or capsule.capsule_hash != run.development_capsule_hash
            or len(receipts) != 1
            or receipts[0].capsule_id != capsule.capsule_id
            or receipts[0].capsule_hash != capsule.capsule_hash
        ):
            raise ImplementationPlanTraceInvalid(
                "Development Capsule identity, hash or completion evidence is altered."
            )
        receipts[0].validate(capsule)
        return capsule

    def _load_input(
        self, command: CompileImplementationPlanCommand
    ) -> Mapping[str, object]:
        if (
            command.plan_input_path != PLAN_INPUT_PATH
            or command.plan_input_sha256 != PLAN_INPUT_SHA256
        ):
            raise ImplementationPlanInputInvalid(
                "Implementation plan input pin differs from capsule authority."
            )
        path = (self._root / command.plan_input_path).resolve()
        try:
            path.relative_to(self._root)
        except ValueError as error:
            raise ImplementationPlanScopeInvalid(
                "Implementation plan input must remain inside the Builder repository."
            ) from error
        try:
            raw = path.read_bytes()
            observed = sha256(raw).hexdigest()
            value = json.loads(raw.decode("utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ImplementationPlanInputInvalid(
                "Implementation plan input is missing, unreadable or invalid."
            ) from error
        if observed != PLAN_INPUT_SHA256 or not isinstance(value, Mapping):
            raise ImplementationPlanInputInvalid(
                "Implementation plan input bytes do not match the immutable pin."
            )
        return value

    def _validate_command(self, command: CompileImplementationPlanCommand) -> None:
        if (
            not all(
                value.strip()
                for value in (
                    command.command_id,
                    command.run_id,
                    command.actor_id,
                    command.correlation_id,
                    command.causation_id,
                )
            )
            or command.expected_version < 1
            or command.requested_operation
            != "compile_dependency_ordered_vertical_plan"
            or command.requested_mode != PLAN_MODE
            or command.requested_profile_id != PLAN_PROFILE_ID
            or command.requested_obligations != OWNED_OBLIGATIONS
            or command.requested_dependencies != DIRECT_DEPENDENCIES
            or command.requested_external_target_compatibility
            != EXTERNAL_TARGET_COMPATIBILITY
        ):
            raise ImplementationPlanInputInvalid(
                "Implementation plan command identity or contract is invalid."
            )
        if (
            command.requested_implementation_authorized
            or command.requested_production_eligible
            or command.requested_certified
        ):
            raise ImplementationPlanAuthorityInvalid(
                "A handoff plan cannot authorize implementation, production or certification."
            )
        if command.requested_external_runtime_ids or command.requested_external_skill_ids:
            raise ImplementationPlanScopeInvalid(
                "The synthetic handoff plan cannot introduce external skills or runtimes."
            )
        if command.requested_increment_overrides:
            raise ImplementationPlanTraceInvalid(
                "Command-supplied plan overrides are not authoritative."
            )

    def _authorize_code(self, actor_id: str, run_id: str) -> None:
        actor = self._authority.authorize(
            actor_id=actor_id,
            action=Action.TRANSITION_RUN,
            resource_id=run_id,
            now=self._clock.now(),
        )
        if actor.kind is not ActorKind.CODE:
            raise ImplementationPlanAuthorityInvalid(
                "Only deterministic Builder code may compile the plan."
            )

    @staticmethod
    def _require_version(expected_version: int, run: Run) -> None:
        if expected_version != run.stream_version:
            raise ConcurrencyConflict(
                "Expected stream version does not match authoritative state.",
                expected_version=expected_version,
                current_version=run.stream_version,
            )

    def _duplicate(
        self, command_id: str, payload_hash: str
    ) -> ImplementationPlanReceipt | None:
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if (
            record.payload_hash != payload_hash
            or not isinstance(record.result, ImplementationPlanReceipt)
        ):
            raise IdempotencyPayloadMismatch(
                "Command identity was reused with a different payload or result contract.",
                command_id=command_id,
            )
        return record.result

    def _emit_replay(
        self,
        command: CompileImplementationPlanCommand,
        receipt: ImplementationPlanReceipt,
    ) -> None:
        run = self._repository.load_run(command.run_id)
        plan = self._repository.get_implementation_plan(receipt.plan_id)
        capsule = self._repository.get_development_capsule(receipt.capsule_id)
        if plan is None or capsule is None:
            raise ImplementationPlanTraceInvalid(
                "Replayed implementation plan evidence is unavailable."
            )
        self._emit(
            event_name="implementation_plan_compilation_replayed",
            outcome="PASS",
            command=command,
            run=run,
            capsule=capsule,
            plan=plan,
            receipt=receipt,
            replay_status="ORIGINAL_RECEIPT_RETURNED",
            failure_context={},
        )

    def _emit(
        self,
        *,
        event_name: str,
        outcome: str,
        command: CompileImplementationPlanCommand,
        run: Run | None,
        capsule: VersionedTraceableDevelopmentCapsule | None,
        plan: VerticalImplementationPlan | None,
        receipt: ImplementationPlanReceipt | None,
        replay_status: str,
        failure_context: dict[str, object],
    ) -> None:
        context = dict(failure_context)
        context.update(
            {
                "plan_id": plan.plan_id if plan else "unassigned",
                "plan_hash": plan.plan_hash if plan else "unassigned",
                "plan_receipt_id": receipt.receipt_id if receipt else "unassigned",
                "increment_count": len(plan.increments) if plan else 0,
                "implementation_authorized": False,
                "replay_status": replay_status,
            }
        )
        self._observations.emit(
            Observation(
                event_name=event_name,
                run_id=command.run_id,
                story_id=self.STORY_ID,
                artifact_identity=plan.plan_id if plan else "unassigned",
                authority_identity=command.actor_id,
                version=self.CONTRACT_VERSION,
                provenance=(
                    plan.plan_hash
                    if plan
                    else capsule.capsule_hash
                    if capsule
                    else "unassigned"
                ),
                outcome=outcome,
                failure_context=context,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                command_id=command.command_id,
                target_id=(run.target_profile.target_id if run else PLAN_PROFILE_ID),
                category_id=(run.target_profile.category_id if run else "none"),
                profile_id=(run.target_profile.profile_id if run else PLAN_PROFILE_ID),
                stream_version=(run.stream_version if run else command.expected_version),
                development_capsule_id=(
                    capsule.capsule_id if capsule else "unassigned"
                ),
                development_capsule_hash=(
                    capsule.capsule_hash if capsule else "unassigned"
                ),
                development_capsule_replay_status=replay_status,
            )
        )


def _command_hash(command: CompileImplementationPlanCommand) -> str:
    value = json.dumps(
        asdict(command), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return f"sha256:{sha256(value).hexdigest()}"
