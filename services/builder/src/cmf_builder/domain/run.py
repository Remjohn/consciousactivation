from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from hashlib import sha256
import json
from typing import Iterable, Mapping

from cmf_builder.domain.target_profile import TargetProfile


class LifecycleState(str, Enum):
    CREATED = "CREATED"
    SOURCE_DIAGNOSTIC = "SOURCE_DIAGNOSTIC"
    SOURCE_LOCKED = "SOURCE_LOCKED"
    VISUAL_UNDERSTANDING = "VISUAL_UNDERSTANDING"
    SATURATED = "SATURATED"
    ATOMICITY_RATIFICATION = "ATOMICITY_RATIFICATION"
    GENESIS = "GENESIS"
    ARCHITECTURE_COMPILED = "ARCHITECTURE_COMPILED"
    EVALUATING = "EVALUATING"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"
    READY_FOR_AUTHORIZATION = "READY_FOR_AUTHORIZATION"
    PROTOTYPE_AUTHORIZED = "PROTOTYPE_AUTHORIZED"
    IMPLEMENTATION_AUTHORIZED = "IMPLEMENTATION_AUTHORIZED"
    CAPSULE_ISSUED = "CAPSULE_ISSUED"
    CERTIFIED = "CERTIFIED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class RunContractError(Exception):
    code = "RunContractError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class TransitionRejected(RunContractError):
    code = "TransitionRejected"


class WaiverRejected(RunContractError):
    code = "WaiverRejected"


class EventStreamInvalid(RunContractError):
    code = "EventStreamInvalid"


NON_WAIVABLE_GATES = frozenset(
    {"production_authorization", "production_certification", "HG-015"}
)


@dataclass(frozen=True, slots=True)
class RunEvent:
    event_id: str
    event_type: str
    run_id: str
    stream_version: int
    command_id: str
    actor_id: str
    timestamp: datetime
    correlation_id: str
    causation_id: str
    payload: tuple[tuple[str, object], ...]

    @classmethod
    def create(
        cls,
        *,
        event_id: str,
        event_type: str,
        run_id: str,
        stream_version: int,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
        payload: Mapping[str, object],
    ) -> "RunEvent":
        return cls(
            event_id=event_id,
            event_type=event_type,
            run_id=run_id,
            stream_version=stream_version,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload=tuple(sorted((key, _freeze(value)) for key, value in payload.items())),
        )

    def value(self, key: str, default: object = None) -> object:
        for candidate, value in self.payload:
            if candidate == key:
                return value
        return default

    def canonical_dict(self) -> dict[str, object]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "run_id": self.run_id,
            "stream_version": self.stream_version,
            "command_id": self.command_id,
            "actor_id": self.actor_id,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "payload": {key: _json_value(value) for key, value in self.payload},
        }


@dataclass(frozen=True, slots=True)
class LifecycleWaiver:
    skipped_obligation: str
    rationale: str
    risk: str
    affected_gates: tuple[str, ...]
    scope: str
    expires_at: datetime
    signed_by: str
    human_receipt_id: str


@dataclass(frozen=True, slots=True)
class Run:
    run_id: str
    target_profile: TargetProfile
    lifecycle_state: LifecycleState
    stream_version: int
    compiler_version: str
    created_by: str
    created_at: datetime
    events: tuple[RunEvent, ...]
    human_decision_receipt_ids: tuple[str, ...] = ()
    active_checkpoint_id: str | None = None
    source_lock_ref: str | None = None
    evidence_index_ref: str | None = None
    evidence_index_hash: str | None = None
    evidence_index_invalidation_ref: str | None = None
    saturation_evaluation_ref: str | None = None
    saturation_evaluation_hash: str | None = None
    saturation_evaluation_invalidation_ref: str | None = None
    genesis_question_ref: str | None = None
    genesis_question_hash: str | None = None
    genesis_question_invalidation_ref: str | None = None
    genesis_decision_memory_ref: str | None = None
    genesis_decision_memory_hash: str | None = None
    genesis_decision_invalidation_ref: str | None = None
    atomic_boundary_ref: str | None = None
    atomicity_ratification_ref: str | None = None
    draft_harness_model_ref: str | None = None
    boundary_invalidation_ref: str | None = None
    harness_ir_ref: str | None = None
    harness_ir_invalidation_ref: str | None = None
    artifact_set_ref: str | None = None
    artifact_manifest_ref: str | None = None
    artifact_manifest_hash: str | None = None
    artifact_set_invalidation_ref: str | None = None
    constitutional_validation_ref: str | None = None
    constitutional_validation_hash: str | None = None
    constitutional_validation_invalidation_ref: str | None = None
    capability_ownership_ref: str | None = None
    capability_ownership_hash: str | None = None
    capability_ownership_invalidation_ref: str | None = None
    responsibility_module_ref: str | None = None
    responsibility_module_hash: str | None = None
    responsibility_module_invalidation_ref: str | None = None
    phase_graph_ref: str | None = None
    phase_graph_hash: str | None = None
    phase_graph_invalidation_ref: str | None = None
    phase_handoff_ref: str | None = None
    phase_handoff_hash: str | None = None
    phase_handoff_invalidation_ref: str | None = None
    minimum_context_ref: str | None = None
    minimum_context_hash: str | None = None
    minimum_context_invalidation_ref: str | None = None
    skill_registry_snapshot_ref: str | None = None
    skill_registry_snapshot_hash: str | None = None
    skill_registry_snapshot_invalidation_ref: str | None = None
    skill_necessity_ref: str | None = None
    skill_necessity_hash: str | None = None
    skill_necessity_invalidation_ref: str | None = None
    atomic_harness_definition_ref: str | None = None
    atomic_harness_definition_hash: str | None = None
    atomic_harness_definition_invalidation_ref: str | None = None
    atomic_content_harness_validation_ref: str | None = None
    atomic_content_harness_validation_hash: str | None = None
    atomic_content_harness_validation_invalidation_ref: str | None = None
    development_capsule_ref: str | None = None
    development_capsule_hash: str | None = None
    development_capsule_invalidation_ref: str | None = None

    @property
    def required_work(self) -> tuple[str, ...]:
        return self.target_profile.required_work

    @classmethod
    def create(
        cls,
        *,
        run_id: str,
        profile: TargetProfile,
        compiler_version: str,
        actor_id: str,
        command_id: str,
        event_ids: tuple[str, str],
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", tuple[RunEvent, RunEvent]]:
        if not compiler_version.strip():
            raise RunContractError("Compiler version is required.")
        created = RunEvent.create(
            event_id=event_ids[0],
            event_type="RunCreated",
            run_id=run_id,
            stream_version=1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                **profile.to_payload(),
                "compiler_version": compiler_version,
                "created_by": actor_id,
            },
        )
        selected = RunEvent.create(
            event_id=event_ids[1],
            event_type="TargetProfileSelected",
            run_id=run_id,
            stream_version=2,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=created.event_id,
            payload={
                "target_id": profile.target_id,
                "category_id": profile.category_id,
                "profile_id": profile.profile_id,
                "profile_version": profile.version,
                "profile_hash": profile.profile_hash,
            },
        )
        events = (created, selected)
        return cls.replay(events), events

    @classmethod
    def replay(cls, events: Iterable[RunEvent]) -> "Run":
        ordered = tuple(events)
        if not ordered:
            raise EventStreamInvalid("An empty event stream cannot produce a run.")
        first = ordered[0]
        if first.stream_version != 1 or first.event_type != "RunCreated":
            raise EventStreamInvalid(
                "The first event must be RunCreated at stream version 1.",
                event_type=first.event_type,
                stream_version=first.stream_version,
            )
        profile_payload = {key: value for key, value in first.payload}
        profile = TargetProfile.from_payload(profile_payload)
        run = cls(
            run_id=first.run_id,
            target_profile=profile,
            lifecycle_state=LifecycleState.CREATED,
            stream_version=1,
            compiler_version=str(first.value("compiler_version")),
            created_by=str(first.value("created_by")),
            created_at=first.timestamp,
            events=(first,),
        )
        for event in ordered[1:]:
            run = run._apply(event)
        return run

    def transition(
        self,
        *,
        to_state: LifecycleState,
        prerequisites: frozenset[str],
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if not self.target_profile.allows_transition(self.lifecycle_state.value, to_state.value):
            raise TransitionRejected(
                "The target profile does not permit this lifecycle edge.",
                current_state=self.lifecycle_state.value,
                target_state=to_state.value,
            )
        required = self.target_profile.required_prerequisites(to_state.value)
        missing = sorted(required - prerequisites)
        if missing:
            raise TransitionRejected(
                "Lifecycle prerequisites are incomplete.",
                target_state=to_state.value,
                missing_prerequisites=tuple(missing),
            )
        event = RunEvent.create(
            event_id=event_id,
            event_type="LifecycleTransitioned",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "from_state": self.lifecycle_state.value,
                "to_state": to_state.value,
                "profile_hash": self.target_profile.profile_hash,
                "prerequisites": tuple(sorted(prerequisites)),
            },
        )
        return self._apply(event), event

    def grant_waiver(
        self,
        waiver: LifecycleWaiver,
        *,
        event_id: str,
        command_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        required_text = (
            waiver.skipped_obligation,
            waiver.rationale,
            waiver.risk,
            waiver.scope,
            waiver.signed_by,
        )
        if not all(value.strip() for value in required_text) or not waiver.affected_gates:
            raise WaiverRejected("A waiver requires complete scope, rationale, risk, gates and signer.")
        if waiver.expires_at <= timestamp:
            raise WaiverRejected(
                "An expired waiver cannot be granted.", expires_at=waiver.expires_at.isoformat()
            )
        protected = sorted(set(waiver.affected_gates) & NON_WAIVABLE_GATES)
        if protected:
            raise WaiverRejected(
                "The waiver attempts to bypass a non-waivable production gate.",
                protected_gates=tuple(protected),
            )
        event = RunEvent.create(
            event_id=event_id,
            event_type="LifecycleWaiverGranted",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=waiver.signed_by,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "skipped_obligation": waiver.skipped_obligation,
                "rationale": waiver.rationale,
                "risk": waiver.risk,
                "affected_gates": waiver.affected_gates,
                "scope": waiver.scope,
                "expires_at": waiver.expires_at.isoformat(),
                "human_receipt_id": waiver.human_receipt_id,
            },
        )
        return self._apply(event), event

    def record_checkpoint(
        self,
        *,
        checkpoint_id: str,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        event = RunEvent.create(
            event_id=event_id,
            event_type="CheckpointCreated",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={"checkpoint_id": checkpoint_id},
        )
        return self._apply(event), event

    def attach_source_lock(
        self,
        *,
        source_lock_ref: str,
        source_profile_ref: str,
        source_profile_hash: str,
        target_candidate_ref: str,
        aggregate_hash: str,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if self.lifecycle_state is not LifecycleState.SOURCE_DIAGNOSTIC:
            raise TransitionRejected(
                "A Source Lock may be attached only after source diagnostics pass.",
                current_state=self.lifecycle_state.value,
            )
        if self.source_lock_ref is not None:
            raise TransitionRejected(
                "The run already has an immutable Source Lock reference.",
                source_lock_ref=self.source_lock_ref,
            )
        event = RunEvent.create(
            event_id=event_id,
            event_type="SourceLockAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "source_lock_ref": source_lock_ref,
                "source_profile_ref": source_profile_ref,
                "source_profile_hash": source_profile_hash,
                "target_candidate_ref": target_candidate_ref,
                "aggregate_hash": aggregate_hash,
            },
        )
        return self._apply(event), event

    def attach_evidence_index(
        self,
        *,
        index_ref: str,
        index_hash: str,
        source_lock_ref: str,
        source_lock_hash: str,
        specimen_count: int,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.SOURCE_LOCKED
            or not self.source_lock_ref
            or self.source_lock_ref != source_lock_ref
            or (
                self.evidence_index_ref is not None
                and self.evidence_index_invalidation_ref is None
            )
        ):
            raise TransitionRejected(
                "Evidence indexing requires one active Source Lock and no active index.",
                source_lock_ref=self.source_lock_ref,
                evidence_index_ref=self.evidence_index_ref,
            )
        if (
            not all(
                value.strip()
                for value in (
                    index_ref,
                    index_hash,
                    source_lock_ref,
                    source_lock_hash,
                    actor_id,
                )
            )
            or specimen_count <= 0
        ):
            raise RunContractError("Evidence-index attachment identity is invalid.")
        event = RunEvent.create(
            event_id=event_id,
            event_type="EvidenceIndexAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "index_ref": index_ref,
                "index_hash": index_hash,
                "source_lock_ref": source_lock_ref,
                "source_lock_hash": source_lock_hash,
                "specimen_count": specimen_count,
            },
        )
        return self._apply(event), event

    def invalidate_evidence_index(
        self,
        *,
        index_ref: str,
        index_hash: str,
        source_lock_ref: str,
        invalidation_ref: str,
        reason: str,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.evidence_index_ref != index_ref
            or self.evidence_index_hash != index_hash
            or self.source_lock_ref != source_lock_ref
            or self.evidence_index_invalidation_ref is not None
        ):
            raise TransitionRejected(
                "Only the active evidence index may be invalidated.",
                evidence_index_ref=self.evidence_index_ref,
            )
        if not all(
            value.strip()
            for value in (
                index_ref,
                index_hash,
                source_lock_ref,
                invalidation_ref,
                reason,
                actor_id,
            )
        ):
            raise RunContractError("Evidence-index invalidation identity is invalid.")
        event = RunEvent.create(
            event_id=event_id,
            event_type="EvidenceIndexInvalidated",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "index_ref": index_ref,
                "index_hash": index_hash,
                "source_lock_ref": source_lock_ref,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_version_required": True,
            },
        )
        return self._apply(event), event

    def attach_saturation_evaluation(
        self,
        *,
        evaluation_ref: str,
        evaluation_hash: str,
        contract_ref: str,
        contract_hash: str,
        source_lock_ref: str,
        evidence_index_ref: str,
        outcome: str,
        downstream_consequence: str,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.SOURCE_LOCKED
            or self.source_lock_ref != source_lock_ref
            or self.evidence_index_ref != evidence_index_ref
            or self.evidence_index_invalidation_ref is not None
            or (
                self.saturation_evaluation_ref is not None
                and self.saturation_evaluation_invalidation_ref is None
            )
        ):
            raise TransitionRejected(
                "Saturation evaluation requires the active Source Lock and Evidence Index.",
                source_lock_ref=self.source_lock_ref,
                evidence_index_ref=self.evidence_index_ref,
            )
        if not all(
            value.strip()
            for value in (
                evaluation_ref,
                evaluation_hash,
                contract_ref,
                contract_hash,
                source_lock_ref,
                evidence_index_ref,
                outcome,
                downstream_consequence,
                actor_id,
            )
        ):
            raise RunContractError("Saturation-evaluation attachment identity is invalid.")
        event = RunEvent.create(
            event_id=event_id,
            event_type="SaturationEvaluationAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "evaluation_ref": evaluation_ref,
                "evaluation_hash": evaluation_hash,
                "contract_ref": contract_ref,
                "contract_hash": contract_hash,
                "source_lock_ref": source_lock_ref,
                "evidence_index_ref": evidence_index_ref,
                "outcome": outcome,
                "downstream_consequence": downstream_consequence,
            },
        )
        return self._apply(event), event

    def invalidate_saturation_evaluation(
        self,
        *,
        evaluation_ref: str,
        evaluation_hash: str,
        invalidation_ref: str,
        reason: str,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.saturation_evaluation_ref != evaluation_ref
            or self.saturation_evaluation_hash != evaluation_hash
            or self.saturation_evaluation_invalidation_ref is not None
        ):
            raise TransitionRejected(
                "Only the active saturation evaluation may be invalidated.",
                evaluation_ref=self.saturation_evaluation_ref,
            )
        if not all(
            value.strip()
            for value in (
                evaluation_ref,
                evaluation_hash,
                invalidation_ref,
                reason,
                actor_id,
            )
        ):
            raise RunContractError("Saturation invalidation identity is invalid.")
        event = RunEvent.create(
            event_id=event_id,
            event_type="SaturationEvaluationInvalidated",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "evaluation_ref": evaluation_ref,
                "evaluation_hash": evaluation_hash,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_version_required": True,
            },
        )
        return self._apply(event), event

    def attach_genesis_question(
        self,
        *,
        package_ref: str,
        package_hash: str,
        graph_ref: str,
        graph_hash: str,
        model_ref: str,
        saturation_ref: str,
        selected_decision_id: str,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.ATOMICITY_RATIFICATION
            or self.draft_harness_model_ref != model_ref
            or self.saturation_evaluation_ref != saturation_ref
            or self.boundary_invalidation_ref is not None
            or self.saturation_evaluation_invalidation_ref is not None
            or self.genesis_question_ref is not None
            and self.genesis_question_invalidation_ref is None
        ):
            raise TransitionRejected(
                "Genesis question requires active saturation, ratified boundary and unratified model."
            )
        if not all(
            value.strip()
            for value in (
                package_ref, package_hash, graph_ref, graph_hash, model_ref,
                saturation_ref, selected_decision_id, actor_id,
            )
        ):
            raise RunContractError("Genesis-question attachment identity is invalid.")
        event = RunEvent.create(
            event_id=event_id, event_type="GenesisQuestionPackageAttached",
            run_id=self.run_id, stream_version=self.stream_version + 1,
            command_id=command_id, actor_id=actor_id, timestamp=timestamp,
            correlation_id=correlation_id, causation_id=causation_id,
            payload={
                "package_ref": package_ref, "package_hash": package_hash,
                "graph_ref": graph_ref, "graph_hash": graph_hash,
                "model_ref": model_ref, "saturation_ref": saturation_ref,
                "selected_decision_id": selected_decision_id,
            },
        )
        return self._apply(event), event

    def invalidate_genesis_question(
        self,
        *,
        package_ref: str,
        package_hash: str,
        invalidation_ref: str,
        reason: str,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.genesis_question_ref != package_ref
            or self.genesis_question_hash != package_hash
            or self.genesis_question_invalidation_ref is not None
        ):
            raise TransitionRejected("Only the active Genesis question may be invalidated.")
        if not all(value.strip() for value in (package_ref, package_hash, invalidation_ref, reason, actor_id)):
            raise RunContractError("Genesis-question invalidation identity is invalid.")
        event = RunEvent.create(
            event_id=event_id, event_type="GenesisQuestionPackageInvalidated",
            run_id=self.run_id, stream_version=self.stream_version + 1,
            command_id=command_id, actor_id=actor_id, timestamp=timestamp,
            correlation_id=correlation_id, causation_id=causation_id,
            payload={
                "package_ref": package_ref, "package_hash": package_hash,
                "invalidation_ref": invalidation_ref, "reason": reason,
                "new_version_required": True,
            },
        )
        return self._apply(event), event

    def attach_genesis_decision_memory(
        self, *, memory_ref: str, memory_hash: str, answer_ref: str,
        final_decision_ref: str, amendment_ref: str, graph_ref: str,
        package_ref: str, cascade_status: str, event_id: str, command_id: str,
        actor_id: str, timestamp: datetime, correlation_id: str, causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.genesis_question_ref != package_ref
            or self.genesis_question_invalidation_ref is not None
            or self.genesis_decision_memory_ref is not None
            and self.genesis_decision_invalidation_ref is None
            or self.boundary_invalidation_ref is not None
        ):
            raise TransitionRejected("Genesis decision requires one active question package and model lineage.")
        if not all(value.strip() for value in (memory_ref, memory_hash, answer_ref, final_decision_ref, amendment_ref, graph_ref, package_ref, cascade_status, actor_id)):
            raise RunContractError("Genesis decision attachment identity is invalid.")
        event = RunEvent.create(
            event_id=event_id, event_type="GenesisDecisionMemoryAttached", run_id=self.run_id,
            stream_version=self.stream_version + 1, command_id=command_id, actor_id=actor_id,
            timestamp=timestamp, correlation_id=correlation_id, causation_id=causation_id,
            payload={"memory_ref": memory_ref, "memory_hash": memory_hash,
                     "answer_ref": answer_ref, "final_decision_ref": final_decision_ref,
                     "amendment_ref": amendment_ref, "graph_ref": graph_ref,
                     "package_ref": package_ref, "cascade_status": cascade_status},
        )
        return self._apply(event), event

    def invalidate_genesis_decision_memory(
        self, *, memory_ref: str, memory_hash: str, invalidation_ref: str,
        reason: str, event_id: str, command_id: str, actor_id: str,
        timestamp: datetime, correlation_id: str, causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.genesis_decision_memory_ref != memory_ref
            or self.genesis_decision_memory_hash != memory_hash
            or self.genesis_decision_invalidation_ref is not None
        ):
            raise TransitionRejected("Only the active Genesis decision memory may be reopened.")
        if not all(value.strip() for value in (memory_ref, memory_hash, invalidation_ref, reason, actor_id)):
            raise RunContractError("Genesis decision invalidation identity is invalid.")
        event = RunEvent.create(
            event_id=event_id, event_type="GenesisDecisionMemoryInvalidated", run_id=self.run_id,
            stream_version=self.stream_version + 1, command_id=command_id, actor_id=actor_id,
            timestamp=timestamp, correlation_id=correlation_id, causation_id=causation_id,
            payload={"memory_ref": memory_ref, "memory_hash": memory_hash,
                     "invalidation_ref": invalidation_ref, "reason": reason,
                     "new_version_required": True},
        )
        return self._apply(event), event

    def resume(
        self,
        *,
        checkpoint_id: str | None,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        event = RunEvent.create(
            event_id=event_id,
            event_type="RunResumed",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "checkpoint_id": checkpoint_id or "event-stream-replay",
                "human_decision_receipt_ids": self.human_decision_receipt_ids,
                "replayed_human_decision_count": len(self.human_decision_receipt_ids),
            },
        )
        return self._apply(event), event

    def record_atomicity_decision(
        self,
        *,
        action: str,
        decision_status: str,
        decision_hash: str,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if self.lifecycle_state is not LifecycleState.SOURCE_LOCKED:
            raise TransitionRejected(
                "An atomicity decision requires a SOURCE_LOCKED run.",
                lifecycle_state=self.lifecycle_state.value,
            )
        event = RunEvent.create(
            event_id=event_id,
            event_type="AtomicityDecisionRecorded",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "action": action,
                "decision_status": decision_status,
                "decision_hash": decision_hash,
            },
        )
        return self._apply(event), event

    def freeze_atomic_boundary(
        self,
        *,
        boundary_ref: str,
        model_ref: str,
        ratification_ref: str,
        decision_hash: str,
        event_ids: tuple[str, str, str, str],
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", tuple[RunEvent, RunEvent, RunEvent, RunEvent]]:
        if (
            self.lifecycle_state is not LifecycleState.SOURCE_LOCKED
            or self.source_lock_ref is None
            or self.atomic_boundary_ref is not None
            or self.draft_harness_model_ref is not None
        ):
            raise TransitionRejected(
                "Only one SOURCE_LOCKED boundary may be frozen.",
                lifecycle_state=self.lifecycle_state.value,
                source_lock_ref=self.source_lock_ref,
                boundary_ref=self.atomic_boundary_ref,
            )
        required = (boundary_ref, model_ref, ratification_ref, decision_hash, actor_id)
        if not all(item.strip() for item in required):
            raise RunContractError("Atomicity freeze identities must be complete.")
        ratified = RunEvent.create(
            event_id=event_ids[0],
            event_type="AtomicityRatificationRecorded",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "boundary_ref": boundary_ref,
                "ratification_ref": ratification_ref,
                "human_receipt_id": ratification_ref,
                "decision_hash": decision_hash,
            },
        )
        after_ratification = self._apply(ratified)
        compiled = RunEvent.create(
            event_id=event_ids[1],
            event_type="DraftHarnessModelCompiled",
            run_id=self.run_id,
            stream_version=after_ratification.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=ratified.event_id,
            payload={"model_ref": model_ref, "boundary_ref": boundary_ref},
        )
        after_model = after_ratification._apply(compiled)
        frozen = RunEvent.create(
            event_id=event_ids[2],
            event_type="AtomicBoundaryFrozen",
            run_id=self.run_id,
            stream_version=after_model.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=compiled.event_id,
            payload={
                "boundary_ref": boundary_ref,
                "model_ref": model_ref,
                "ratification_ref": ratification_ref,
            },
        )
        after_freeze = after_model._apply(frozen)
        final_run, transitioned = after_freeze.transition(
            to_state=LifecycleState.ATOMICITY_RATIFICATION,
            prerequisites=frozenset({"atomic_boundary_ratified"}),
            event_id=event_ids[3],
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=frozen.event_id,
        )
        return final_run, (ratified, compiled, frozen, transitioned)

    def attach_harness_ir(
        self,
        *,
        harness_ir_ref: str,
        harness_ir_hash: str,
        schema_version: str,
        revision: int,
        event_ids: tuple[str, str],
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", tuple[RunEvent, RunEvent]]:
        if (
            self.lifecycle_state is not LifecycleState.ATOMICITY_RATIFICATION
            or not self.source_lock_ref
            or not self.atomic_boundary_ref
            or not self.atomicity_ratification_ref
            or not self.draft_harness_model_ref
            or self.boundary_invalidation_ref is not None
            or self.harness_ir_ref is not None
        ):
            raise TransitionRejected(
                "Harness IR requires one active ratified atomic package.",
                lifecycle_state=self.lifecycle_state.value,
                harness_ir_ref=self.harness_ir_ref,
            )
        if not all((harness_ir_ref.strip(), harness_ir_hash.strip(), schema_version.strip())) or revision != 1:
            raise RunContractError("Initial Harness IR identity and revision are invalid.")
        attached = RunEvent.create(
            event_id=event_ids[0],
            event_type="HarnessIRSnapshotAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "harness_ir_ref": harness_ir_ref,
                "harness_ir_hash": harness_ir_hash,
                "schema_version": schema_version,
                "revision": revision,
                "source_lock_ref": self.source_lock_ref,
                "boundary_ref": self.atomic_boundary_ref,
                "ratification_ref": self.atomicity_ratification_ref,
                "model_ref": self.draft_harness_model_ref,
            },
        )
        after_attach = self._apply(attached)
        final_run, transitioned = after_attach.transition(
            to_state=LifecycleState.GENESIS,
            prerequisites=frozenset({"canonical_harness_ir_compiled"}),
            event_id=event_ids[1],
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=attached.event_id,
        )
        return final_run, (attached, transitioned)

    def reopen_atomic_boundary(
        self,
        *,
        invalidation_ref: str,
        reason: str,
        event_ids: tuple[str, ...],
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", tuple[RunEvent, ...]]:
        if (
            self.lifecycle_state not in {
                LifecycleState.ATOMICITY_RATIFICATION,
                LifecycleState.GENESIS,
            }
            or not self.atomic_boundary_ref
            or not self.draft_harness_model_ref
            or self.boundary_invalidation_ref is not None
        ):
            raise TransitionRejected(
                "Only one active frozen boundary may be reopened.",
                lifecycle_state=self.lifecycle_state.value,
                boundary_ref=self.atomic_boundary_ref,
                invalidation_ref=self.boundary_invalidation_ref,
            )
        expected_event_count = (
            15
            if self.development_capsule_ref
            else (
                14
                if self.atomic_content_harness_validation_ref
                else (
                    13
                    if self.atomic_harness_definition_ref
                    else (
                        12
                        if self.skill_necessity_ref
                        else (
                            11
                            if self.skill_registry_snapshot_ref
                            else (
                                10
                                if self.minimum_context_ref
                                else (
                                    9
                                    if self.phase_handoff_ref
                                    else (
                                        8
                                        if self.phase_graph_ref
                                        else (
                                            7
                                            if self.responsibility_module_ref
                                            else (
                                                6
                                                if self.capability_ownership_ref
                                                else (
                                                    5
                                                    if self.constitutional_validation_ref
                                                    else (4 if self.artifact_set_ref else (3 if self.harness_ir_ref else 2))
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
        if len(event_ids) != expected_event_count:
            raise RunContractError(
                "Boundary reopen event identities do not cover all descendants.",
                expected_event_count=expected_event_count,
                observed_event_count=len(event_ids),
            )
        if not invalidation_ref.strip() or not reason.strip():
            raise RunContractError("Boundary reopen requires identity and rationale.")
        reopened = RunEvent.create(
            event_id=event_ids[0],
            event_type="AtomicBoundaryReopened",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "boundary_ref": self.atomic_boundary_ref,
                "model_ref": self.draft_harness_model_ref,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_version_required": True,
            },
        )
        after_reopen = self._apply(reopened)
        invalidated = RunEvent.create(
            event_id=event_ids[1],
            event_type="DraftHarnessModelInvalidated",
            run_id=self.run_id,
            stream_version=after_reopen.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=reopened.event_id,
            payload={
                "model_ref": self.draft_harness_model_ref,
                "invalidation_ref": invalidation_ref,
            },
        )
        after_model = after_reopen._apply(invalidated)
        if not self.harness_ir_ref:
            return after_model, (reopened, invalidated)
        harness_ir_invalidated = RunEvent.create(
            event_id=event_ids[2],
            event_type="HarnessIRInvalidated",
            run_id=self.run_id,
            stream_version=after_model.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=invalidated.event_id,
            payload={
                "harness_ir_ref": self.harness_ir_ref,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_revision_required": True,
            },
        )
        after_ir = after_model._apply(harness_ir_invalidated)
        if not self.artifact_set_ref:
            return after_ir, (reopened, invalidated, harness_ir_invalidated)
        artifact_set_invalidated = RunEvent.create(
            event_id=event_ids[3],
            event_type="ArtifactSetInvalidated",
            run_id=self.run_id,
            stream_version=after_ir.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=harness_ir_invalidated.event_id,
            payload={
                "artifact_set_ref": self.artifact_set_ref,
                "artifact_manifest_ref": self.artifact_manifest_ref,
                "harness_ir_ref": self.harness_ir_ref,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_version_required": True,
            },
        )
        after_artifacts = after_ir._apply(artifact_set_invalidated)
        if not self.constitutional_validation_ref:
            return after_artifacts, (
                reopened,
                invalidated,
                harness_ir_invalidated,
                artifact_set_invalidated,
            )
        constitutional_validation_invalidated = RunEvent.create(
            event_id=event_ids[4],
            event_type="ConstitutionalValidationInvalidated",
            run_id=self.run_id,
            stream_version=after_artifacts.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=artifact_set_invalidated.event_id,
            payload={
                "constitutional_validation_ref": self.constitutional_validation_ref,
                "artifact_set_ref": self.artifact_set_ref,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_version_required": True,
            },
        )
        after_constitutional = after_artifacts._apply(
            constitutional_validation_invalidated
        )
        if not self.capability_ownership_ref:
            return after_constitutional, (
                reopened,
                invalidated,
                harness_ir_invalidated,
                artifact_set_invalidated,
                constitutional_validation_invalidated,
            )
        capability_ownership_invalidated = RunEvent.create(
            event_id=event_ids[5],
            event_type="CapabilityOwnershipInvalidated",
            run_id=self.run_id,
            stream_version=after_constitutional.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=constitutional_validation_invalidated.event_id,
            payload={
                "capability_ownership_ref": self.capability_ownership_ref,
                "constitutional_validation_ref": self.constitutional_validation_ref,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_version_required": True,
            },
        )
        after_capability = after_constitutional._apply(
            capability_ownership_invalidated
        )
        if not self.responsibility_module_ref:
            return after_capability, (
                reopened,
                invalidated,
                harness_ir_invalidated,
                artifact_set_invalidated,
                constitutional_validation_invalidated,
                capability_ownership_invalidated,
            )
        responsibility_modules_invalidated = RunEvent.create(
            event_id=event_ids[6],
            event_type="ResponsibilityModulesInvalidated",
            run_id=self.run_id,
            stream_version=after_capability.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=capability_ownership_invalidated.event_id,
            payload={
                "responsibility_module_ref": self.responsibility_module_ref,
                "capability_ownership_ref": self.capability_ownership_ref,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_version_required": True,
            },
        )
        after_modules = after_capability._apply(responsibility_modules_invalidated)
        if not self.phase_graph_ref:
            return after_modules, (
                reopened,
                invalidated,
                harness_ir_invalidated,
                artifact_set_invalidated,
                constitutional_validation_invalidated,
                capability_ownership_invalidated,
                responsibility_modules_invalidated,
            )
        phase_graph_invalidated = RunEvent.create(
            event_id=event_ids[7],
            event_type="PhaseGraphInvalidated",
            run_id=self.run_id,
            stream_version=after_modules.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=responsibility_modules_invalidated.event_id,
            payload={
                "phase_graph_ref": self.phase_graph_ref,
                "responsibility_module_ref": self.responsibility_module_ref,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_version_required": True,
            },
        )
        after_phase_graph = after_modules._apply(phase_graph_invalidated)
        if not self.phase_handoff_ref:
            return after_phase_graph, (
                reopened,
                invalidated,
                harness_ir_invalidated,
                artifact_set_invalidated,
                constitutional_validation_invalidated,
                capability_ownership_invalidated,
                responsibility_modules_invalidated,
                phase_graph_invalidated,
            )
        phase_handoffs_invalidated = RunEvent.create(
            event_id=event_ids[8],
            event_type="PhaseHandoffsInvalidated",
            run_id=self.run_id,
            stream_version=after_phase_graph.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=phase_graph_invalidated.event_id,
            payload={
                "phase_handoff_ref": self.phase_handoff_ref,
                "phase_graph_ref": self.phase_graph_ref,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_version_required": True,
            },
        )
        after_handoffs = after_phase_graph._apply(phase_handoffs_invalidated)
        if not self.minimum_context_ref:
            return after_handoffs, (
                reopened,
                invalidated,
                harness_ir_invalidated,
                artifact_set_invalidated,
                constitutional_validation_invalidated,
                capability_ownership_invalidated,
                responsibility_modules_invalidated,
                phase_graph_invalidated,
                phase_handoffs_invalidated,
            )
        minimum_context_invalidated = RunEvent.create(
            event_id=event_ids[9],
            event_type="MinimumContextInvalidated",
            run_id=self.run_id,
            stream_version=after_handoffs.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=phase_handoffs_invalidated.event_id,
            payload={
                "minimum_context_ref": self.minimum_context_ref,
                "phase_handoff_ref": self.phase_handoff_ref,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_version_required": True,
            },
        )
        after_context = after_handoffs._apply(minimum_context_invalidated)
        if not self.skill_registry_snapshot_ref:
            return after_context, (
                reopened,
                invalidated,
                harness_ir_invalidated,
                artifact_set_invalidated,
                constitutional_validation_invalidated,
                capability_ownership_invalidated,
                responsibility_modules_invalidated,
                phase_graph_invalidated,
                phase_handoffs_invalidated,
                minimum_context_invalidated,
            )
        skill_registry_invalidated = RunEvent.create(
            event_id=event_ids[10],
            event_type="SkillRegistrySnapshotInvalidated",
            run_id=self.run_id,
            stream_version=after_context.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=minimum_context_invalidated.event_id,
            payload={
                "skill_registry_snapshot_ref": self.skill_registry_snapshot_ref,
                "minimum_context_ref": self.minimum_context_ref,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_version_required": True,
            },
        )
        after_skill_registry = after_context._apply(skill_registry_invalidated)
        if not self.skill_necessity_ref:
            return after_skill_registry, (
                reopened,
                invalidated,
                harness_ir_invalidated,
                artifact_set_invalidated,
                constitutional_validation_invalidated,
                capability_ownership_invalidated,
                responsibility_modules_invalidated,
                phase_graph_invalidated,
                phase_handoffs_invalidated,
                minimum_context_invalidated,
                skill_registry_invalidated,
            )
        skill_necessity_invalidated = RunEvent.create(
            event_id=event_ids[11],
            event_type="SkillNecessityInvalidated",
            run_id=self.run_id,
            stream_version=after_skill_registry.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=skill_registry_invalidated.event_id,
            payload={
                "skill_necessity_ref": self.skill_necessity_ref,
                "skill_registry_snapshot_ref": self.skill_registry_snapshot_ref,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_version_required": True,
            },
        )
        after_skill_necessity = after_skill_registry._apply(skill_necessity_invalidated)
        if not self.atomic_harness_definition_ref:
            return after_skill_necessity, (
                reopened,
                invalidated,
                harness_ir_invalidated,
                artifact_set_invalidated,
                constitutional_validation_invalidated,
                capability_ownership_invalidated,
                responsibility_modules_invalidated,
                phase_graph_invalidated,
                phase_handoffs_invalidated,
                minimum_context_invalidated,
                skill_registry_invalidated,
                skill_necessity_invalidated,
            )
        definition_invalidated = RunEvent.create(
            event_id=event_ids[12],
            event_type="AtomicHarnessDefinitionInvalidated",
            run_id=self.run_id,
            stream_version=after_skill_necessity.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=skill_necessity_invalidated.event_id,
            payload={
                "definition_ref": self.atomic_harness_definition_ref,
                "skill_necessity_ref": self.skill_necessity_ref,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_version_required": True,
            },
        )
        after_definition = after_skill_necessity._apply(definition_invalidated)
        if not self.atomic_content_harness_validation_ref:
            return after_definition, (
                reopened,
                invalidated,
                harness_ir_invalidated,
                artifact_set_invalidated,
                constitutional_validation_invalidated,
                capability_ownership_invalidated,
                responsibility_modules_invalidated,
                phase_graph_invalidated,
                phase_handoffs_invalidated,
                minimum_context_invalidated,
                skill_registry_invalidated,
                skill_necessity_invalidated,
                definition_invalidated,
            )
        target_validation_invalidated = RunEvent.create(
            event_id=event_ids[13],
            event_type="AtomicContentHarnessValidationInvalidated",
            run_id=self.run_id,
            stream_version=after_definition.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=definition_invalidated.event_id,
            payload={
                "validation_ref": self.atomic_content_harness_validation_ref,
                "definition_ref": self.atomic_harness_definition_ref,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_version_required": True,
            },
        )
        after_target_validation = after_definition._apply(
            target_validation_invalidated
        )
        if not self.development_capsule_ref:
            return after_target_validation, (
                reopened,
                invalidated,
                harness_ir_invalidated,
                artifact_set_invalidated,
                constitutional_validation_invalidated,
                capability_ownership_invalidated,
                responsibility_modules_invalidated,
                phase_graph_invalidated,
                phase_handoffs_invalidated,
                minimum_context_invalidated,
                skill_registry_invalidated,
                skill_necessity_invalidated,
                definition_invalidated,
                target_validation_invalidated,
            )
        development_capsule_invalidated = RunEvent.create(
            event_id=event_ids[14],
            event_type="DevelopmentCapsuleInvalidated",
            run_id=self.run_id,
            stream_version=after_target_validation.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=target_validation_invalidated.event_id,
            payload={
                "capsule_ref": self.development_capsule_ref,
                "validation_ref": self.atomic_content_harness_validation_ref,
                "invalidation_ref": invalidation_ref,
                "reason": reason,
                "new_version_required": True,
            },
        )
        return after_target_validation._apply(development_capsule_invalidated), (
            reopened,
            invalidated,
            harness_ir_invalidated,
            artifact_set_invalidated,
            constitutional_validation_invalidated,
            capability_ownership_invalidated,
            responsibility_modules_invalidated,
            phase_graph_invalidated,
            phase_handoffs_invalidated,
            minimum_context_invalidated,
            skill_registry_invalidated,
            skill_necessity_invalidated,
            definition_invalidated,
            target_validation_invalidated,
            development_capsule_invalidated,
        )

    def attach_artifact_manifest(
        self,
        *,
        artifact_set_ref: str,
        manifest_ref: str,
        manifest_hash: str,
        harness_ir_ref: str,
        harness_ir_hash: str,
        artifact_count: int,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.GENESIS
            or not self.harness_ir_ref
            or self.harness_ir_ref != harness_ir_ref
            or self.harness_ir_invalidation_ref is not None
            or self.boundary_invalidation_ref is not None
            or self.artifact_set_ref is not None
            or self.artifact_set_invalidation_ref is not None
        ):
            raise TransitionRejected(
                "Artifact compilation requires one active Harness IR in GENESIS.",
                lifecycle_state=self.lifecycle_state.value,
                harness_ir_ref=self.harness_ir_ref,
                artifact_set_ref=self.artifact_set_ref,
            )
        if (
            not all(
                value.strip()
                for value in (
                    artifact_set_ref,
                    manifest_ref,
                    manifest_hash,
                    harness_ir_ref,
                    harness_ir_hash,
                )
            )
            or artifact_count != 21
        ):
            raise RunContractError("Artifact manifest attachment identity is invalid.")
        event = RunEvent.create(
            event_id=event_id,
            event_type="ArtifactManifestAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "artifact_set_ref": artifact_set_ref,
                "artifact_manifest_ref": manifest_ref,
                "artifact_manifest_hash": manifest_hash,
                "harness_ir_ref": harness_ir_ref,
                "harness_ir_hash": harness_ir_hash,
                "artifact_count": artifact_count,
            },
        )
        return self._apply(event), event

    def attach_constitutional_validation(
        self,
        *,
        report_ref: str,
        report_hash: str,
        policy_hash: str,
        artifact_set_ref: str,
        manifest_ref: str,
        harness_ir_ref: str,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.GENESIS
            or not self.harness_ir_ref
            or not self.artifact_set_ref
            or not self.artifact_manifest_ref
            or self.harness_ir_ref != harness_ir_ref
            or self.artifact_set_ref != artifact_set_ref
            or self.artifact_manifest_ref != manifest_ref
            or self.harness_ir_invalidation_ref is not None
            or self.artifact_set_invalidation_ref is not None
            or self.boundary_invalidation_ref is not None
            or self.constitutional_validation_ref is not None
            or self.constitutional_validation_invalidation_ref is not None
        ):
            raise TransitionRejected(
                "Constitutional validation requires one active generated artifact set in GENESIS.",
                lifecycle_state=self.lifecycle_state.value,
                artifact_set_ref=self.artifact_set_ref,
                validation_ref=self.constitutional_validation_ref,
            )
        if not all(
            value.strip()
            for value in (
                report_ref,
                report_hash,
                policy_hash,
                artifact_set_ref,
                manifest_ref,
                harness_ir_ref,
            )
        ):
            raise RunContractError("Constitutional validation identity is incomplete.")
        event = RunEvent.create(
            event_id=event_id,
            event_type="ConstitutionalValidationAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "report_ref": report_ref,
                "report_hash": report_hash,
                "policy_hash": policy_hash,
                "artifact_set_ref": artifact_set_ref,
                "manifest_ref": manifest_ref,
                "harness_ir_ref": harness_ir_ref,
            },
        )
        return self._apply(event), event

    def attach_capability_ownership(
        self,
        *,
        graph_ref: str,
        graph_hash: str,
        harness_ir_ref: str,
        constitutional_report_ref: str,
        capability_count: int,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.GENESIS
            or not self.harness_ir_ref
            or not self.artifact_set_ref
            or not self.constitutional_validation_ref
            or self.harness_ir_ref != harness_ir_ref
            or self.constitutional_validation_ref != constitutional_report_ref
            or self.boundary_invalidation_ref is not None
            or self.harness_ir_invalidation_ref is not None
            or self.artifact_set_invalidation_ref is not None
            or self.constitutional_validation_invalidation_ref is not None
            or self.capability_ownership_ref is not None
            or self.capability_ownership_invalidation_ref is not None
        ):
            raise TransitionRejected(
                "Capability ownership requires one active constitutional parent in GENESIS.",
                lifecycle_state=self.lifecycle_state.value,
                validation_ref=self.constitutional_validation_ref,
                graph_ref=self.capability_ownership_ref,
            )
        if (
            not all(
                value.strip()
                for value in (
                    graph_ref,
                    graph_hash,
                    harness_ir_ref,
                    constitutional_report_ref,
                )
            )
            or capability_count != 3
        ):
            raise RunContractError("Capability ownership attachment is incomplete.")
        event = RunEvent.create(
            event_id=event_id,
            event_type="CapabilityOwnershipAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "graph_ref": graph_ref,
                "graph_hash": graph_hash,
                "harness_ir_ref": harness_ir_ref,
                "constitutional_report_ref": constitutional_report_ref,
                "capability_count": capability_count,
            },
        )
        return self._apply(event), event

    def attach_responsibility_modules(
        self,
        *,
        graph_ref: str,
        graph_hash: str,
        capability_graph_ref: str,
        harness_ir_ref: str,
        module_count: int,
        capability_count: int,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.GENESIS
            or not self.harness_ir_ref
            or not self.capability_ownership_ref
            or self.harness_ir_ref != harness_ir_ref
            or self.capability_ownership_ref != capability_graph_ref
            or self.boundary_invalidation_ref is not None
            or self.harness_ir_invalidation_ref is not None
            or self.artifact_set_invalidation_ref is not None
            or self.constitutional_validation_invalidation_ref is not None
            or self.capability_ownership_invalidation_ref is not None
            or self.responsibility_module_ref is not None
            or self.responsibility_module_invalidation_ref is not None
        ):
            raise TransitionRejected(
                "Responsibility modules require one active capability graph in GENESIS.",
                lifecycle_state=self.lifecycle_state.value,
                capability_graph_ref=self.capability_ownership_ref,
                module_graph_ref=self.responsibility_module_ref,
            )
        if (
            not all(
                value.strip()
                for value in (
                    graph_ref,
                    graph_hash,
                    capability_graph_ref,
                    harness_ir_ref,
                )
            )
            or module_count != 2
            or capability_count != 3
        ):
            raise RunContractError("Responsibility module attachment is incomplete.")
        event = RunEvent.create(
            event_id=event_id,
            event_type="ResponsibilityModulesAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "graph_ref": graph_ref,
                "graph_hash": graph_hash,
                "capability_graph_ref": capability_graph_ref,
                "harness_ir_ref": harness_ir_ref,
                "module_count": module_count,
                "capability_count": capability_count,
            },
        )
        return self._apply(event), event

    def attach_phase_graph(
        self,
        *,
        graph_ref: str,
        graph_hash: str,
        module_graph_ref: str,
        harness_ir_ref: str,
        phase_count: int,
        module_count: int,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.GENESIS
            or not self.harness_ir_ref
            or not self.responsibility_module_ref
            or self.harness_ir_ref != harness_ir_ref
            or self.responsibility_module_ref != module_graph_ref
            or self.boundary_invalidation_ref is not None
            or self.harness_ir_invalidation_ref is not None
            or self.artifact_set_invalidation_ref is not None
            or self.constitutional_validation_invalidation_ref is not None
            or self.capability_ownership_invalidation_ref is not None
            or self.responsibility_module_invalidation_ref is not None
            or self.phase_graph_ref is not None
            or self.phase_graph_invalidation_ref is not None
        ):
            raise TransitionRejected(
                "Phase Graph requires one active responsibility-module graph in GENESIS.",
                lifecycle_state=self.lifecycle_state.value,
                module_graph_ref=self.responsibility_module_ref,
                phase_graph_ref=self.phase_graph_ref,
            )
        if (
            not all(
                value.strip()
                for value in (graph_ref, graph_hash, module_graph_ref, harness_ir_ref)
            )
            or phase_count != 2
            or module_count != 2
        ):
            raise RunContractError("Phase Graph attachment is incomplete.")
        event = RunEvent.create(
            event_id=event_id,
            event_type="PhaseGraphAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "graph_ref": graph_ref,
                "graph_hash": graph_hash,
                "module_graph_ref": module_graph_ref,
                "harness_ir_ref": harness_ir_ref,
                "phase_count": phase_count,
                "module_count": module_count,
            },
        )
        return self._apply(event), event

    def attach_phase_handoffs(
        self,
        *,
        graph_ref: str,
        graph_hash: str,
        phase_graph_ref: str,
        harness_ir_ref: str,
        context_count: int,
        contract_count: int,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.GENESIS
            or not self.harness_ir_ref
            or not self.phase_graph_ref
            or self.harness_ir_ref != harness_ir_ref
            or self.phase_graph_ref != phase_graph_ref
            or self.boundary_invalidation_ref is not None
            or self.harness_ir_invalidation_ref is not None
            or self.artifact_set_invalidation_ref is not None
            or self.constitutional_validation_invalidation_ref is not None
            or self.capability_ownership_invalidation_ref is not None
            or self.responsibility_module_invalidation_ref is not None
            or self.phase_graph_invalidation_ref is not None
            or self.phase_handoff_ref is not None
            or self.phase_handoff_invalidation_ref is not None
        ):
            raise TransitionRejected(
                "Internal handoffs require one active Phase Graph in GENESIS.",
                lifecycle_state=self.lifecycle_state.value,
                phase_graph_ref=self.phase_graph_ref,
                handoff_graph_ref=self.phase_handoff_ref,
            )
        if (
            not all(value.strip() for value in (graph_ref, graph_hash, phase_graph_ref, harness_ir_ref))
            or context_count != 2
            or contract_count != 1
        ):
            raise RunContractError("Internal handoff attachment is incomplete.")
        event = RunEvent.create(
            event_id=event_id,
            event_type="PhaseHandoffsAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "graph_ref": graph_ref,
                "graph_hash": graph_hash,
                "phase_graph_ref": phase_graph_ref,
                "harness_ir_ref": harness_ir_ref,
                "context_count": context_count,
                "contract_count": contract_count,
            },
        )
        return self._apply(event), event

    def record_internal_handoff_event(
        self,
        *,
        event_type: str,
        handoff_graph_ref: str,
        handoff_ref: str,
        handoff_hash: str,
        sender_phase: str,
        receiver_phase: str,
        status: str,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.GENESIS
            or not self.phase_handoff_ref
            or self.phase_handoff_ref != handoff_graph_ref
            or self.phase_handoff_invalidation_ref is not None
            or self.phase_graph_invalidation_ref is not None
            or event_type not in {
                "InternalHandoffIssued",
                "InternalHandoffAccepted",
                "InternalHandoffRejected",
            }
            or status not in {"ISSUED", "ACCEPTED", "REJECTED"}
            or not all(
                value.strip()
                for value in (
                    handoff_ref,
                    handoff_hash,
                    sender_phase,
                    receiver_phase,
                    event_id,
                    command_id,
                    actor_id,
                )
            )
        ):
            raise TransitionRejected("Internal handoff event is unauthorized or incomplete.")
        event = RunEvent.create(
            event_id=event_id,
            event_type=event_type,
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "handoff_graph_ref": handoff_graph_ref,
                "handoff_ref": handoff_ref,
                "handoff_hash": handoff_hash,
                "sender_phase": sender_phase,
                "receiver_phase": receiver_phase,
                "status": status,
            },
        )
        return self._apply(event), event

    def attach_minimum_context(
        self,
        *,
        graph_ref: str,
        graph_hash: str,
        handoff_graph_ref: str,
        accepted_handoff_ref: str,
        acceptance_decision_ref: str,
        manifest_count: int,
        reference_count: int,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.GENESIS
            or not self.phase_handoff_ref
            or self.phase_handoff_ref != handoff_graph_ref
            or self.phase_handoff_invalidation_ref is not None
            or self.minimum_context_ref is not None
            or self.minimum_context_invalidation_ref is not None
            or not all(
                value.strip()
                for value in (
                    graph_ref,
                    graph_hash,
                    handoff_graph_ref,
                    accepted_handoff_ref,
                    acceptance_decision_ref,
                )
            )
            or manifest_count != 2
            or reference_count != 6
        ):
            raise TransitionRejected(
                "Minimum Complete Context requires one active accepted Builder-internal handoff.",
                lifecycle_state=self.lifecycle_state.value,
                handoff_graph_ref=self.phase_handoff_ref,
                minimum_context_ref=self.minimum_context_ref,
            )
        event = RunEvent.create(
            event_id=event_id,
            event_type="MinimumContextAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "graph_ref": graph_ref,
                "graph_hash": graph_hash,
                "handoff_graph_ref": handoff_graph_ref,
                "accepted_handoff_ref": accepted_handoff_ref,
                "acceptance_decision_ref": acceptance_decision_ref,
                "manifest_count": manifest_count,
                "reference_count": reference_count,
            },
        )
        return self._apply(event), event

    def attach_skill_registry_snapshot(
        self,
        *,
        snapshot_ref: str,
        snapshot_hash: str,
        registry_ref: str,
        registry_hash: str,
        minimum_context_ref: str,
        capability_count: int,
        registered_skill_count: int,
        required_external_skill_count: int,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.GENESIS
            or not self.minimum_context_ref
            or self.minimum_context_ref != minimum_context_ref
            or self.minimum_context_invalidation_ref is not None
            or self.skill_registry_snapshot_ref is not None
            or self.skill_registry_snapshot_invalidation_ref is not None
            or not all(value.strip() for value in (
                snapshot_ref,
                snapshot_hash,
                registry_ref,
                registry_hash,
                minimum_context_ref,
            ))
            or capability_count != 5
            or registered_skill_count != 0
            or required_external_skill_count != 0
        ):
            raise TransitionRejected(
                "Synthetic skill-registry consumption requires one active Minimum Complete Context and exact zero-skill invariants.",
                lifecycle_state=self.lifecycle_state.value,
                minimum_context_ref=self.minimum_context_ref,
                skill_registry_snapshot_ref=self.skill_registry_snapshot_ref,
            )
        event = RunEvent.create(
            event_id=event_id,
            event_type="SkillRegistrySnapshotAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "snapshot_ref": snapshot_ref,
                "snapshot_hash": snapshot_hash,
                "registry_ref": registry_ref,
                "registry_hash": registry_hash,
                "minimum_context_ref": minimum_context_ref,
                "capability_count": capability_count,
                "registered_skill_count": registered_skill_count,
                "required_external_skill_count": required_external_skill_count,
            },
        )
        return self._apply(event), event

    def attach_skill_necessity_decision(
        self,
        *,
        decision_ref: str,
        decision_hash: str,
        snapshot_ref: str,
        snapshot_hash: str,
        capability_count: int,
        external_skills_required_count: int,
        adaptations_required_count: int,
        experiments_required_count: int,
        jit_capsules_required_count: int,
        outcome: str,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.GENESIS
            or not self.skill_registry_snapshot_ref
            or self.skill_registry_snapshot_ref != snapshot_ref
            or self.skill_registry_snapshot_hash != snapshot_hash
            or self.skill_registry_snapshot_invalidation_ref is not None
            or self.skill_necessity_ref is not None
            or self.skill_necessity_invalidation_ref is not None
            or not all(value.strip() for value in (
                decision_ref,
                decision_hash,
                snapshot_ref,
                snapshot_hash,
            ))
            or capability_count != 5
            or any((
                external_skills_required_count,
                adaptations_required_count,
                experiments_required_count,
                jit_capsules_required_count,
            ))
            or outcome != "NO_NEW_SKILL_REQUIRED"
        ):
            raise TransitionRejected(
                "Skill necessity attachment requires the exact active zero-skill snapshot and a proven no-gap result.",
                lifecycle_state=self.lifecycle_state.value,
                skill_registry_snapshot_ref=self.skill_registry_snapshot_ref,
                skill_necessity_ref=self.skill_necessity_ref,
            )
        event = RunEvent.create(
            event_id=event_id,
            event_type="SkillNecessityDecisionAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "decision_ref": decision_ref,
                "decision_hash": decision_hash,
                "snapshot_ref": snapshot_ref,
                "snapshot_hash": snapshot_hash,
                "capability_count": capability_count,
                "external_skills_required_count": external_skills_required_count,
                "adaptations_required_count": adaptations_required_count,
                "experiments_required_count": experiments_required_count,
                "jit_capsules_required_count": jit_capsules_required_count,
                "outcome": outcome,
            },
        )
        return self._apply(event), event

    def attach_atomic_harness_definition(
        self,
        *,
        definition_ref: str,
        definition_hash: str,
        skill_necessity_ref: str,
        skill_necessity_hash: str,
        section_count: int,
        external_skill_count: int,
        external_runtime_count: int,
        synthetic_not_certifiable: bool,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.GENESIS
            or not self.skill_necessity_ref
            or self.skill_necessity_ref != skill_necessity_ref
            or self.skill_necessity_hash != skill_necessity_hash
            or self.skill_necessity_invalidation_ref is not None
            or self.atomic_harness_definition_ref is not None
            or self.atomic_harness_definition_invalidation_ref is not None
            or not all(value.strip() for value in (
                definition_ref,
                definition_hash,
                skill_necessity_ref,
                skill_necessity_hash,
            ))
            or section_count != 20
            or external_skill_count
            or external_runtime_count
            or not synthetic_not_certifiable
        ):
            raise TransitionRejected(
                "Atomic Harness Definition requires the exact active no-skill lineage and synthetic scope.",
                lifecycle_state=self.lifecycle_state.value,
                skill_necessity_ref=self.skill_necessity_ref,
                definition_ref=self.atomic_harness_definition_ref,
            )
        event = RunEvent.create(
            event_id=event_id,
            event_type="AtomicHarnessDefinitionAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "definition_ref": definition_ref,
                "definition_hash": definition_hash,
                "skill_necessity_ref": skill_necessity_ref,
                "skill_necessity_hash": skill_necessity_hash,
                "section_count": section_count,
                "external_skill_count": external_skill_count,
                "external_runtime_count": external_runtime_count,
                "synthetic_not_certifiable": synthetic_not_certifiable,
            },
        )
        return self._apply(event), event

    def attach_atomic_content_harness_validation(
        self,
        *,
        validation_ref: str,
        validation_hash: str,
        definition_ref: str,
        definition_hash: str,
        dimension_count: int,
        section_count: int,
        internal_compatibility: str,
        external_target_compatibility: str,
        synthetic_not_certifiable: bool,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.GENESIS
            or not self.atomic_harness_definition_ref
            or self.atomic_harness_definition_ref != definition_ref
            or self.atomic_harness_definition_hash != definition_hash
            or self.atomic_harness_definition_invalidation_ref is not None
            or self.atomic_content_harness_validation_ref is not None
            or self.atomic_content_harness_validation_invalidation_ref is not None
            or not all(value.strip() for value in (
                validation_ref,
                validation_hash,
                definition_ref,
                definition_hash,
            ))
            or dimension_count != 8
            or section_count != 20
            or internal_compatibility != "PASS"
            or external_target_compatibility
            != "NOT_EVALUATED_EXTERNAL_TARGET_BRANCH"
            or not synthetic_not_certifiable
        ):
            raise TransitionRejected(
                "Target validation requires the exact active synthetic Atomic Harness Definition.",
                lifecycle_state=self.lifecycle_state.value,
                definition_ref=self.atomic_harness_definition_ref,
                validation_ref=self.atomic_content_harness_validation_ref,
            )
        event = RunEvent.create(
            event_id=event_id,
            event_type="AtomicContentHarnessValidationAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "validation_ref": validation_ref,
                "validation_hash": validation_hash,
                "definition_ref": definition_ref,
                "definition_hash": definition_hash,
                "dimension_count": dimension_count,
                "section_count": section_count,
                "internal_compatibility": internal_compatibility,
                "external_target_compatibility": external_target_compatibility,
                "synthetic_not_certifiable": synthetic_not_certifiable,
            },
        )
        return self._apply(event), event

    def attach_development_capsule(
        self,
        *,
        capsule_ref: str,
        capsule_hash: str,
        validation_ref: str,
        validation_hash: str,
        section_count: int,
        reference_count: int,
        obligation_count: int,
        production_eligible: bool,
        certified: bool,
        synthetic_not_certifiable: bool,
        event_id: str,
        command_id: str,
        actor_id: str,
        timestamp: datetime,
        correlation_id: str,
        causation_id: str,
    ) -> tuple["Run", RunEvent]:
        if (
            self.lifecycle_state is not LifecycleState.GENESIS
            or not self.atomic_content_harness_validation_ref
            or self.atomic_content_harness_validation_ref != validation_ref
            or self.atomic_content_harness_validation_hash != validation_hash
            or self.atomic_content_harness_validation_invalidation_ref is not None
            or self.development_capsule_ref is not None
            or self.development_capsule_invalidation_ref is not None
            or not all(
                value.strip()
                for value in (
                    capsule_ref,
                    capsule_hash,
                    validation_ref,
                    validation_hash,
                )
            )
            or section_count != 15
            or reference_count < 20
            or obligation_count != 6
            or production_eligible
            or certified
            or not synthetic_not_certifiable
        ):
            raise TransitionRejected(
                "Development Capsule generation requires the exact active validated synthetic Harness.",
                lifecycle_state=self.lifecycle_state.value,
                validation_ref=self.atomic_content_harness_validation_ref,
                capsule_ref=self.development_capsule_ref,
            )
        event = RunEvent.create(
            event_id=event_id,
            event_type="DevelopmentCapsuleAttached",
            run_id=self.run_id,
            stream_version=self.stream_version + 1,
            command_id=command_id,
            actor_id=actor_id,
            timestamp=timestamp,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={
                "capsule_ref": capsule_ref,
                "capsule_hash": capsule_hash,
                "validation_ref": validation_ref,
                "validation_hash": validation_hash,
                "section_count": section_count,
                "reference_count": reference_count,
                "obligation_count": obligation_count,
                "production_eligible": production_eligible,
                "certified": certified,
                "synthetic_not_certifiable": synthetic_not_certifiable,
            },
        )
        return self._apply(event), event

    def state_hash(self) -> str:
        payload = {
            "run_id": self.run_id,
            "target_profile_hash": self.target_profile.profile_hash,
            "lifecycle_state": self.lifecycle_state.value,
            "stream_version": self.stream_version,
            "compiler_version": self.compiler_version,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "human_decision_receipt_ids": self.human_decision_receipt_ids,
            "active_checkpoint_id": self.active_checkpoint_id,
            "source_lock_ref": self.source_lock_ref,
            "atomic_boundary_ref": self.atomic_boundary_ref,
            "atomicity_ratification_ref": self.atomicity_ratification_ref,
            "draft_harness_model_ref": self.draft_harness_model_ref,
            "boundary_invalidation_ref": self.boundary_invalidation_ref,
            "harness_ir_ref": self.harness_ir_ref,
            "harness_ir_invalidation_ref": self.harness_ir_invalidation_ref,
            "artifact_set_ref": self.artifact_set_ref,
            "artifact_manifest_ref": self.artifact_manifest_ref,
            "artifact_manifest_hash": self.artifact_manifest_hash,
            "artifact_set_invalidation_ref": self.artifact_set_invalidation_ref,
            "constitutional_validation_ref": self.constitutional_validation_ref,
            "constitutional_validation_hash": self.constitutional_validation_hash,
            "constitutional_validation_invalidation_ref": self.constitutional_validation_invalidation_ref,
            "capability_ownership_ref": self.capability_ownership_ref,
            "capability_ownership_hash": self.capability_ownership_hash,
            "capability_ownership_invalidation_ref": self.capability_ownership_invalidation_ref,
            "responsibility_module_ref": self.responsibility_module_ref,
            "responsibility_module_hash": self.responsibility_module_hash,
            "responsibility_module_invalidation_ref": self.responsibility_module_invalidation_ref,
            "phase_graph_ref": self.phase_graph_ref,
            "phase_graph_hash": self.phase_graph_hash,
            "phase_graph_invalidation_ref": self.phase_graph_invalidation_ref,
            "phase_handoff_ref": self.phase_handoff_ref,
            "phase_handoff_hash": self.phase_handoff_hash,
            "phase_handoff_invalidation_ref": self.phase_handoff_invalidation_ref,
            "minimum_context_ref": self.minimum_context_ref,
            "minimum_context_hash": self.minimum_context_hash,
            "minimum_context_invalidation_ref": self.minimum_context_invalidation_ref,
            "skill_registry_snapshot_ref": self.skill_registry_snapshot_ref,
            "skill_registry_snapshot_hash": self.skill_registry_snapshot_hash,
            "skill_registry_snapshot_invalidation_ref": self.skill_registry_snapshot_invalidation_ref,
            "skill_necessity_ref": self.skill_necessity_ref,
            "skill_necessity_hash": self.skill_necessity_hash,
            "skill_necessity_invalidation_ref": self.skill_necessity_invalidation_ref,
            "atomic_harness_definition_ref": self.atomic_harness_definition_ref,
            "atomic_harness_definition_hash": self.atomic_harness_definition_hash,
            "atomic_harness_definition_invalidation_ref": self.atomic_harness_definition_invalidation_ref,
            "atomic_content_harness_validation_ref": self.atomic_content_harness_validation_ref,
            "atomic_content_harness_validation_hash": self.atomic_content_harness_validation_hash,
            "atomic_content_harness_validation_invalidation_ref": self.atomic_content_harness_validation_invalidation_ref,
            "development_capsule_ref": self.development_capsule_ref,
            "development_capsule_hash": self.development_capsule_hash,
            "development_capsule_invalidation_ref": self.development_capsule_invalidation_ref,
            "event_prefix_hash": self.event_prefix_hash(self.stream_version),
        }
        if any(
            value is not None
            for value in (
                self.evidence_index_ref,
                self.evidence_index_hash,
                self.evidence_index_invalidation_ref,
            )
        ):
            payload.update(
                {
                    "evidence_index_ref": self.evidence_index_ref,
                    "evidence_index_hash": self.evidence_index_hash,
                    "evidence_index_invalidation_ref": self.evidence_index_invalidation_ref,
                }
            )
        if any(
            value is not None
            for value in (
                self.saturation_evaluation_ref,
                self.saturation_evaluation_hash,
                self.saturation_evaluation_invalidation_ref,
            )
        ):
            payload.update(
                {
                    "saturation_evaluation_ref": self.saturation_evaluation_ref,
                    "saturation_evaluation_hash": self.saturation_evaluation_hash,
            "saturation_evaluation_invalidation_ref": self.saturation_evaluation_invalidation_ref,
            "genesis_question_ref": self.genesis_question_ref,
            "genesis_question_hash": self.genesis_question_hash,
            "genesis_question_invalidation_ref": self.genesis_question_invalidation_ref,
            "genesis_decision_memory_ref": self.genesis_decision_memory_ref,
            "genesis_decision_memory_hash": self.genesis_decision_memory_hash,
            "genesis_decision_invalidation_ref": self.genesis_decision_invalidation_ref,
                }
            )
        return f"sha256:{sha256(_canonical_json(payload)).hexdigest()}"

    def state_hash_at(self, stream_version: int) -> str:
        if stream_version < 1 or stream_version > self.stream_version:
            raise EventStreamInvalid(
                "Checkpoint stream version is outside the run event range.",
                checkpoint_stream_version=stream_version,
                run_stream_version=self.stream_version,
            )
        return Run.replay(self.events[:stream_version]).state_hash()

    def event_prefix_hash(self, stream_version: int) -> str:
        selected = [
            event.canonical_dict()
            for event in self.events
            if event.stream_version <= stream_version
        ]
        return f"sha256:{sha256(_canonical_json(selected)).hexdigest()}"

    def _apply(self, event: RunEvent) -> "Run":
        if event.run_id != self.run_id:
            raise EventStreamInvalid(
                "An event belongs to a different run.",
                expected_run_id=self.run_id,
                observed_run_id=event.run_id,
            )
        if event.stream_version != self.stream_version + 1:
            raise EventStreamInvalid(
                "Event stream versions are discontinuous.",
                expected_version=self.stream_version + 1,
                observed_version=event.stream_version,
            )
        state = self.lifecycle_state
        human_receipts = self.human_decision_receipt_ids
        checkpoint_id = self.active_checkpoint_id
        source_lock_ref = self.source_lock_ref
        evidence_index_ref = self.evidence_index_ref
        evidence_index_hash = self.evidence_index_hash
        evidence_index_invalidation_ref = self.evidence_index_invalidation_ref
        saturation_evaluation_ref = self.saturation_evaluation_ref
        saturation_evaluation_hash = self.saturation_evaluation_hash
        saturation_evaluation_invalidation_ref = (
            self.saturation_evaluation_invalidation_ref
        )
        genesis_question_ref = self.genesis_question_ref
        genesis_question_hash = self.genesis_question_hash
        genesis_question_invalidation_ref = self.genesis_question_invalidation_ref
        genesis_decision_memory_ref = self.genesis_decision_memory_ref
        genesis_decision_memory_hash = self.genesis_decision_memory_hash
        genesis_decision_invalidation_ref = self.genesis_decision_invalidation_ref
        atomic_boundary_ref = self.atomic_boundary_ref
        atomicity_ratification_ref = self.atomicity_ratification_ref
        draft_harness_model_ref = self.draft_harness_model_ref
        boundary_invalidation_ref = self.boundary_invalidation_ref
        harness_ir_ref = self.harness_ir_ref
        harness_ir_invalidation_ref = self.harness_ir_invalidation_ref
        artifact_set_ref = self.artifact_set_ref
        artifact_manifest_ref = self.artifact_manifest_ref
        artifact_manifest_hash = self.artifact_manifest_hash
        artifact_set_invalidation_ref = self.artifact_set_invalidation_ref
        constitutional_validation_ref = self.constitutional_validation_ref
        constitutional_validation_hash = self.constitutional_validation_hash
        constitutional_validation_invalidation_ref = (
            self.constitutional_validation_invalidation_ref
        )
        capability_ownership_ref = self.capability_ownership_ref
        capability_ownership_hash = self.capability_ownership_hash
        capability_ownership_invalidation_ref = (
            self.capability_ownership_invalidation_ref
        )
        responsibility_module_ref = self.responsibility_module_ref
        responsibility_module_hash = self.responsibility_module_hash
        responsibility_module_invalidation_ref = (
            self.responsibility_module_invalidation_ref
        )
        phase_graph_ref = self.phase_graph_ref
        phase_graph_hash = self.phase_graph_hash
        phase_graph_invalidation_ref = self.phase_graph_invalidation_ref
        phase_handoff_ref = self.phase_handoff_ref
        phase_handoff_hash = self.phase_handoff_hash
        phase_handoff_invalidation_ref = self.phase_handoff_invalidation_ref
        minimum_context_ref = self.minimum_context_ref
        minimum_context_hash = self.minimum_context_hash
        minimum_context_invalidation_ref = self.minimum_context_invalidation_ref
        skill_registry_snapshot_ref = self.skill_registry_snapshot_ref
        skill_registry_snapshot_hash = self.skill_registry_snapshot_hash
        skill_registry_snapshot_invalidation_ref = (
            self.skill_registry_snapshot_invalidation_ref
        )
        skill_necessity_ref = self.skill_necessity_ref
        skill_necessity_hash = self.skill_necessity_hash
        skill_necessity_invalidation_ref = self.skill_necessity_invalidation_ref
        atomic_harness_definition_ref = self.atomic_harness_definition_ref
        atomic_harness_definition_hash = self.atomic_harness_definition_hash
        atomic_harness_definition_invalidation_ref = (
            self.atomic_harness_definition_invalidation_ref
        )
        atomic_content_harness_validation_ref = (
            self.atomic_content_harness_validation_ref
        )
        atomic_content_harness_validation_hash = (
            self.atomic_content_harness_validation_hash
        )
        atomic_content_harness_validation_invalidation_ref = (
            self.atomic_content_harness_validation_invalidation_ref
        )
        development_capsule_ref = self.development_capsule_ref
        development_capsule_hash = self.development_capsule_hash
        development_capsule_invalidation_ref = (
            self.development_capsule_invalidation_ref
        )
        if event.event_type == "LifecycleTransitioned":
            state = LifecycleState(str(event.value("to_state")))
        elif event.event_type == "LifecycleWaiverGranted":
            receipt_id = str(event.value("human_receipt_id"))
            if receipt_id not in human_receipts:
                human_receipts = (*human_receipts, receipt_id)
        elif event.event_type in {"CheckpointCreated", "RunResumed"}:
            checkpoint_id = str(event.value("checkpoint_id"))
        elif event.event_type == "SourceLockAttached":
            source_lock_ref = str(event.value("source_lock_ref"))
        elif event.event_type == "EvidenceIndexAttached":
            evidence_index_ref = str(event.value("index_ref"))
            evidence_index_hash = str(event.value("index_hash"))
            evidence_index_invalidation_ref = None
        elif event.event_type == "EvidenceIndexInvalidated":
            evidence_index_invalidation_ref = str(
                event.value("invalidation_ref")
            )
        elif event.event_type == "SaturationEvaluationAttached":
            saturation_evaluation_ref = str(event.value("evaluation_ref"))
            saturation_evaluation_hash = str(event.value("evaluation_hash"))
            saturation_evaluation_invalidation_ref = None
        elif event.event_type == "SaturationEvaluationInvalidated":
            saturation_evaluation_invalidation_ref = str(
                event.value("invalidation_ref")
            )
        elif event.event_type == "GenesisQuestionPackageAttached":
            genesis_question_ref = str(event.value("package_ref"))
            genesis_question_hash = str(event.value("package_hash"))
            genesis_question_invalidation_ref = None
        elif event.event_type == "GenesisQuestionPackageInvalidated":
            genesis_question_invalidation_ref = str(event.value("invalidation_ref"))
        elif event.event_type == "GenesisDecisionMemoryAttached":
            genesis_decision_memory_ref = str(event.value("memory_ref"))
            genesis_decision_memory_hash = str(event.value("memory_hash"))
            genesis_decision_invalidation_ref = None
        elif event.event_type == "GenesisDecisionMemoryInvalidated":
            genesis_decision_invalidation_ref = str(event.value("invalidation_ref"))
        elif event.event_type == "AtomicityRatificationRecorded":
            receipt_id = str(event.value("human_receipt_id"))
            atomicity_ratification_ref = str(event.value("ratification_ref"))
            if receipt_id not in human_receipts:
                human_receipts = (*human_receipts, receipt_id)
        elif event.event_type == "DraftHarnessModelCompiled":
            draft_harness_model_ref = str(event.value("model_ref"))
        elif event.event_type == "AtomicBoundaryFrozen":
            atomic_boundary_ref = str(event.value("boundary_ref"))
            draft_harness_model_ref = str(event.value("model_ref"))
        elif event.event_type == "AtomicBoundaryReopened":
            boundary_invalidation_ref = str(event.value("invalidation_ref"))
            if boundary_invalidation_ref not in human_receipts:
                human_receipts = (*human_receipts, boundary_invalidation_ref)
        elif event.event_type == "HarnessIRSnapshotAttached":
            harness_ir_ref = str(event.value("harness_ir_ref"))
        elif event.event_type == "HarnessIRInvalidated":
            harness_ir_invalidation_ref = str(event.value("invalidation_ref"))
        elif event.event_type == "ArtifactManifestAttached":
            artifact_set_ref = str(event.value("artifact_set_ref"))
            artifact_manifest_ref = str(event.value("artifact_manifest_ref"))
            artifact_manifest_hash = str(event.value("artifact_manifest_hash"))
        elif event.event_type == "ArtifactSetInvalidated":
            artifact_set_invalidation_ref = str(event.value("invalidation_ref"))
        elif event.event_type == "ConstitutionalValidationAttached":
            constitutional_validation_ref = str(event.value("report_ref"))
            constitutional_validation_hash = str(event.value("report_hash"))
        elif event.event_type == "ConstitutionalValidationInvalidated":
            constitutional_validation_invalidation_ref = str(
                event.value("invalidation_ref")
            )
        elif event.event_type == "CapabilityOwnershipAttached":
            capability_ownership_ref = str(event.value("graph_ref"))
            capability_ownership_hash = str(event.value("graph_hash"))
        elif event.event_type == "CapabilityOwnershipInvalidated":
            capability_ownership_invalidation_ref = str(
                event.value("invalidation_ref")
            )
        elif event.event_type == "ResponsibilityModulesAttached":
            responsibility_module_ref = str(event.value("graph_ref"))
            responsibility_module_hash = str(event.value("graph_hash"))
        elif event.event_type == "ResponsibilityModulesInvalidated":
            responsibility_module_invalidation_ref = str(
                event.value("invalidation_ref")
            )
        elif event.event_type == "PhaseGraphAttached":
            phase_graph_ref = str(event.value("graph_ref"))
            phase_graph_hash = str(event.value("graph_hash"))
        elif event.event_type == "PhaseGraphInvalidated":
            phase_graph_invalidation_ref = str(event.value("invalidation_ref"))
        elif event.event_type == "PhaseHandoffsAttached":
            phase_handoff_ref = str(event.value("graph_ref"))
            phase_handoff_hash = str(event.value("graph_hash"))
        elif event.event_type == "PhaseHandoffsInvalidated":
            phase_handoff_invalidation_ref = str(event.value("invalidation_ref"))
        elif event.event_type == "MinimumContextAttached":
            minimum_context_ref = str(event.value("graph_ref"))
            minimum_context_hash = str(event.value("graph_hash"))
        elif event.event_type == "MinimumContextInvalidated":
            minimum_context_invalidation_ref = str(event.value("invalidation_ref"))
        elif event.event_type == "SkillRegistrySnapshotAttached":
            skill_registry_snapshot_ref = str(event.value("snapshot_ref"))
            skill_registry_snapshot_hash = str(event.value("snapshot_hash"))
        elif event.event_type == "SkillRegistrySnapshotInvalidated":
            skill_registry_snapshot_invalidation_ref = str(
                event.value("invalidation_ref")
            )
        elif event.event_type == "SkillNecessityDecisionAttached":
            skill_necessity_ref = str(event.value("decision_ref"))
            skill_necessity_hash = str(event.value("decision_hash"))
        elif event.event_type == "SkillNecessityInvalidated":
            skill_necessity_invalidation_ref = str(event.value("invalidation_ref"))
        elif event.event_type == "AtomicHarnessDefinitionAttached":
            atomic_harness_definition_ref = str(event.value("definition_ref"))
            atomic_harness_definition_hash = str(event.value("definition_hash"))
        elif event.event_type == "AtomicHarnessDefinitionInvalidated":
            atomic_harness_definition_invalidation_ref = str(
                event.value("invalidation_ref")
            )
        elif event.event_type == "AtomicContentHarnessValidationAttached":
            atomic_content_harness_validation_ref = str(
                event.value("validation_ref")
            )
            atomic_content_harness_validation_hash = str(
                event.value("validation_hash")
            )
        elif event.event_type == "AtomicContentHarnessValidationInvalidated":
            atomic_content_harness_validation_invalidation_ref = str(
                event.value("invalidation_ref")
            )
        elif event.event_type == "DevelopmentCapsuleAttached":
            development_capsule_ref = str(event.value("capsule_ref"))
            development_capsule_hash = str(event.value("capsule_hash"))
        elif event.event_type == "DevelopmentCapsuleInvalidated":
            development_capsule_invalidation_ref = str(
                event.value("invalidation_ref")
            )
        elif event.event_type == "AtomicityDecisionRecorded":
            decision_hash = str(event.value("decision_hash"))
            if decision_hash not in human_receipts:
                human_receipts = (*human_receipts, decision_hash)
        elif event.event_type in {
            "TargetProfileSelected",
            "DraftHarnessModelInvalidated",
            "InternalHandoffIssued",
            "InternalHandoffAccepted",
            "InternalHandoffRejected",
        }:
            pass
        else:
            raise EventStreamInvalid(
                "Unknown event type in run stream.", event_type=event.event_type
            )
        return Run(
            run_id=self.run_id,
            target_profile=self.target_profile,
            lifecycle_state=state,
            stream_version=event.stream_version,
            compiler_version=self.compiler_version,
            created_by=self.created_by,
            created_at=self.created_at,
            events=(*self.events, event),
            human_decision_receipt_ids=human_receipts,
            active_checkpoint_id=checkpoint_id,
            source_lock_ref=source_lock_ref,
            evidence_index_ref=evidence_index_ref,
            evidence_index_hash=evidence_index_hash,
            evidence_index_invalidation_ref=evidence_index_invalidation_ref,
            saturation_evaluation_ref=saturation_evaluation_ref,
            saturation_evaluation_hash=saturation_evaluation_hash,
            saturation_evaluation_invalidation_ref=saturation_evaluation_invalidation_ref,
            genesis_question_ref=genesis_question_ref,
            genesis_question_hash=genesis_question_hash,
            genesis_question_invalidation_ref=genesis_question_invalidation_ref,
            genesis_decision_memory_ref=genesis_decision_memory_ref,
            genesis_decision_memory_hash=genesis_decision_memory_hash,
            genesis_decision_invalidation_ref=genesis_decision_invalidation_ref,
            atomic_boundary_ref=atomic_boundary_ref,
            atomicity_ratification_ref=atomicity_ratification_ref,
            draft_harness_model_ref=draft_harness_model_ref,
            boundary_invalidation_ref=boundary_invalidation_ref,
            harness_ir_ref=harness_ir_ref,
            harness_ir_invalidation_ref=harness_ir_invalidation_ref,
            artifact_set_ref=artifact_set_ref,
            artifact_manifest_ref=artifact_manifest_ref,
            artifact_manifest_hash=artifact_manifest_hash,
            artifact_set_invalidation_ref=artifact_set_invalidation_ref,
            constitutional_validation_ref=constitutional_validation_ref,
            constitutional_validation_hash=constitutional_validation_hash,
            constitutional_validation_invalidation_ref=constitutional_validation_invalidation_ref,
            capability_ownership_ref=capability_ownership_ref,
            capability_ownership_hash=capability_ownership_hash,
            capability_ownership_invalidation_ref=capability_ownership_invalidation_ref,
            responsibility_module_ref=responsibility_module_ref,
            responsibility_module_hash=responsibility_module_hash,
            responsibility_module_invalidation_ref=responsibility_module_invalidation_ref,
            phase_graph_ref=phase_graph_ref,
            phase_graph_hash=phase_graph_hash,
            phase_graph_invalidation_ref=phase_graph_invalidation_ref,
            phase_handoff_ref=phase_handoff_ref,
            phase_handoff_hash=phase_handoff_hash,
            phase_handoff_invalidation_ref=phase_handoff_invalidation_ref,
            minimum_context_ref=minimum_context_ref,
            minimum_context_hash=minimum_context_hash,
            minimum_context_invalidation_ref=minimum_context_invalidation_ref,
            skill_registry_snapshot_ref=skill_registry_snapshot_ref,
            skill_registry_snapshot_hash=skill_registry_snapshot_hash,
            skill_registry_snapshot_invalidation_ref=skill_registry_snapshot_invalidation_ref,
            skill_necessity_ref=skill_necessity_ref,
            skill_necessity_hash=skill_necessity_hash,
            skill_necessity_invalidation_ref=skill_necessity_invalidation_ref,
            atomic_harness_definition_ref=atomic_harness_definition_ref,
            atomic_harness_definition_hash=atomic_harness_definition_hash,
            atomic_harness_definition_invalidation_ref=atomic_harness_definition_invalidation_ref,
            atomic_content_harness_validation_ref=atomic_content_harness_validation_ref,
            atomic_content_harness_validation_hash=atomic_content_harness_validation_hash,
            atomic_content_harness_validation_invalidation_ref=atomic_content_harness_validation_invalidation_ref,
            development_capsule_ref=development_capsule_ref,
            development_capsule_hash=development_capsule_hash,
            development_capsule_invalidation_ref=development_capsule_invalidation_ref,
        )


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return tuple(sorted((str(key), _freeze(item)) for key, item in value.items()))
    if isinstance(value, (list, tuple, set, frozenset)):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def _json_value(value: object) -> object:
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    return value


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
