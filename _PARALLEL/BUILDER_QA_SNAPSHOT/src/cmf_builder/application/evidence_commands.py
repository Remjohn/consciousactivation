from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json

from cmf_builder.application.authority import Action, AuthorityService
from cmf_builder.application.ports import (
    Clock,
    CommandRecord,
    EvidenceWorkspace,
    EvidenceWorkspaceRepository,
    IdempotencyPayloadMismatch,
    IdProvider,
    Observation,
    ObservationSink,
)
from cmf_builder.domain.evidence_workspace import (
    EvidenceWorkspaceReceipt,
    SourceLock,
    SourceProfile,
    SourceProfileInvalid,
)
from cmf_builder.domain.run import LifecycleState, Run


SOURCE_PROFILE_PATH = "development-capsules/ST-01.02/SYNTHETIC_SOURCE_PROFILE.json"
SOURCE_PROFILE_SHA256 = (
    "cf036f38d26b37624c10e24094401e93c4f74e512d11613182a29cb859fbcd3d"
)
SOURCE_PROFILE_ID = "synthetic_task_definition_source_v1"
SOURCE_PROFILE_VERSION = "1.0.0"
TARGET_CANDIDATE_URI = (
    "repo://development-capsules/ST-01.01-SYNTHETIC-PROOF/"
    "SYNTHETIC_TARGET_PROFILE_FIXTURE.yaml"
)
SYNTHETIC_CATEGORY_ID = "none_test_only"
SYNTHETIC_PROFILE_ID = "synthetic_text_normalization_v1"
SYNTHETIC_PROFILE_VERSION = "1.0.0"


class EvidenceWorkspaceCommandRejected(Exception):
    code = "EvidenceWorkspaceCommandRejected"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


@dataclass(frozen=True, slots=True)
class LockEvidenceWorkspaceCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    source_profile_path: str = SOURCE_PROFILE_PATH
    source_profile_sha256: str = SOURCE_PROFILE_SHA256
    target_candidate_uri: str = TARGET_CANDIDATE_URI
    invalidates_lock_ref: str | None = None


class EvidenceWorkspaceCommandService:
    STORY_ID = "ST-01.02"
    CONTRACT_VERSION = "cmf-builder-evidence-workspace/v1"

    def __init__(
        self,
        *,
        repository: EvidenceWorkspaceRepository,
        workspace: EvidenceWorkspace,
        authority: AuthorityService,
        ids: IdProvider,
        clock: Clock,
        observations: ObservationSink,
    ) -> None:
        self._repository = repository
        self._workspace = workspace
        self._authority = authority
        self._ids = ids
        self._clock = clock
        self._observations = observations

    def lock(self, command: LockEvidenceWorkspaceCommand) -> EvidenceWorkspaceReceipt:
        run: Run | None = None
        profile: SourceProfile | None = None
        source_lock: SourceLock | None = None
        try:
            duplicate = self._duplicate(command)
            if duplicate is not None:
                return duplicate
            now = self._clock.now()
            run = self._repository.load_run(command.run_id)
            self._validate_run_and_command(run, command)
            self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.LOCK_EVIDENCE_WORKSPACE,
                resource_id=command.run_id,
                now=now,
            )
            profile = self._workspace.load_profile(
                command.source_profile_path, command.source_profile_sha256
            )
            self._validate_profile(run, command, profile)
            source_lock, scan = self._workspace.create_lock(
                run_id=run.run_id,
                profile=profile,
                created_at=now,
                created_by=command.actor_id,
                invalidates_lock_ref=command.invalidates_lock_ref,
            )

            diagnostic_run, diagnostic_event = run.transition(
                to_state=LifecycleState.SOURCE_DIAGNOSTIC,
                prerequisites=frozenset({"target_profile_selected"}),
                event_id=self._ids.new_id("event"),
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=now,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            attached_run, attached_event = diagnostic_run.attach_source_lock(
                source_lock_ref=source_lock.lock_id,
                source_profile_ref=source_lock.source_profile_ref,
                source_profile_hash=source_lock.source_profile_hash,
                target_candidate_ref=source_lock.target_candidate_ref,
                aggregate_hash=source_lock.aggregate_hash,
                event_id=self._ids.new_id("event"),
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=now,
                correlation_id=command.correlation_id,
                causation_id=diagnostic_event.event_id,
            )
            locked_run, locked_event = attached_run.transition(
                to_state=LifecycleState.SOURCE_LOCKED,
                prerequisites=frozenset({"source_lock_attached"}),
                event_id=self._ids.new_id("event"),
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=now,
                correlation_id=command.correlation_id,
                causation_id=attached_event.event_id,
            )
            events = (diagnostic_event, attached_event, locked_event)
            receipt = EvidenceWorkspaceReceipt.create(
                receipt_id=self._ids.new_id("receipt"),
                command_id=command.command_id,
                run_id=run.run_id,
                source_lock_ref=source_lock.lock_id,
                source_profile_ref=profile.ref,
                authority_identity=command.actor_id,
                event_ids=tuple(event.event_id for event in events),
                diagnostics=scan.diagnostics,
                outcome="PASS",
            )
            record = CommandRecord(
                payload_hash=_command_hash(command), result=receipt
            )
            self._repository.commit_evidence_workspace(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=events,
                source_lock=source_lock,
                command_id=command.command_id,
                command_record=record,
            )
            self._emit(
                command,
                locked_run,
                "ST-01.02:SourceDiagnosticAccepted",
                "PASS",
                {},
                profile,
                source_lock,
            )
            self._emit(
                command,
                locked_run,
                "ST-01.02:SourceLockCreated",
                "PASS",
                {
                    "file_count": source_lock.file_count,
                    "total_bytes": source_lock.total_bytes,
                    "archive_count": scan.archive_count,
                    "aggregate_hash": source_lock.aggregate_hash,
                },
                profile,
                source_lock,
            )
            self._emit(
                command,
                locked_run,
                "ST-01.02:OutcomeVerified",
                "PASS",
                {},
                profile,
                source_lock,
            )
            return receipt
        except Exception as error:
            self._reject(command, run, profile, source_lock, error)
            raise

    def _duplicate(
        self, command: LockEvidenceWorkspaceCommand
    ) -> EvidenceWorkspaceReceipt | None:
        record = self._repository.get_command_record(command.command_id)
        if record is None:
            return None
        observed = _command_hash(command)
        if observed != record.payload_hash:
            raise IdempotencyPayloadMismatch(
                "A command identity was reused with a different payload.",
                command_id=command.command_id,
                original_payload_hash=record.payload_hash,
                observed_payload_hash=observed,
            )
        if not isinstance(record.result, EvidenceWorkspaceReceipt):
            raise IdempotencyPayloadMismatch(
                "Stored command result has an incompatible type.",
                command_id=command.command_id,
            )
        run = self._repository.load_run(record.result.run_id)
        lock = self._repository.get_source_lock(record.result.source_lock_ref)
        self._emit(
            command,
            run,
            "ST-01.02:SourceLockReplayReturned",
            "PASS",
            {},
            None,
            lock,
        )
        return record.result

    @staticmethod
    def _validate_run_and_command(
        run: Run, command: LockEvidenceWorkspaceCommand
    ) -> None:
        profile = run.target_profile
        if (
            run.lifecycle_state is not LifecycleState.CREATED
            or profile.profile_id != SYNTHETIC_PROFILE_ID
            or profile.version != SYNTHETIC_PROFILE_VERSION
            or profile.category_id != SYNTHETIC_CATEGORY_ID
            or profile.supplemental_proof is None
            or not profile.supplemental_proof.synthetic
            or not profile.supplemental_proof.repository_owned
            or not profile.supplemental_proof.builder_core_validation_only
        ):
            raise EvidenceWorkspaceCommandRejected(
                "Only a CREATED governed synthetic Builder Core run may be source-locked.",
                lifecycle_state=run.lifecycle_state.value,
                target_profile=profile.profile_ref,
            )
        if command.expected_version != run.stream_version:
            # The atomic repository remains authoritative for the final comparison.
            raise EvidenceWorkspaceCommandRejected(
                "Expected stream version does not match the loaded run.",
                expected_version=command.expected_version,
                current_version=run.stream_version,
            )
        if (
            command.source_profile_path != SOURCE_PROFILE_PATH
            or command.source_profile_sha256 != SOURCE_PROFILE_SHA256
            or command.target_candidate_uri != TARGET_CANDIDATE_URI
            or command.invalidates_lock_ref is not None
        ):
            raise EvidenceWorkspaceCommandRejected(
                "The command attempts to substitute an ungoverned source profile or candidate.",
                source_profile_path=command.source_profile_path,
                target_candidate_uri=command.target_candidate_uri,
            )

    @staticmethod
    def _validate_profile(
        run: Run,
        command: LockEvidenceWorkspaceCommand,
        profile: SourceProfile,
    ) -> None:
        if (
            profile.profile_id != SOURCE_PROFILE_ID
            or profile.version != SOURCE_PROFILE_VERSION
            or profile.target_profile_ref
            != f"{run.target_profile.profile_id}@{run.target_profile.version}"
            or profile.target_candidate.uri != command.target_candidate_uri
            or profile.category_binding != "none"
            or profile.production_eligible
            or profile.certified
            or profile.authority_policy.privacy_class != "non_personal_synthetic"
            or profile.authority_policy.consent_policy_required
        ):
            raise SourceProfileInvalid(
                "Source profile is not the governed category-neutral synthetic definition.",
                source_profile_ref=profile.ref,
                target_profile_ref=profile.target_profile_ref,
            )

    def _reject(
        self,
        command: LockEvidenceWorkspaceCommand,
        run: Run | None,
        profile: SourceProfile | None,
        source_lock: SourceLock | None,
        error: Exception,
    ) -> None:
        if not hasattr(error, "code"):
            return
        context = {
            "code": str(getattr(error, "code")),
            **getattr(error, "context", {}),
        }
        self._emit(
            command,
            run,
            "ST-01.02:SourceDiagnosticRejected",
            "FAIL",
            context,
            profile,
            source_lock,
        )
        self._emit(
            command,
            run,
            "ST-01.02:OutcomeRejected",
            "FAIL",
            context,
            profile,
            source_lock,
        )

    def _emit(
        self,
        command: LockEvidenceWorkspaceCommand,
        run: Run | None,
        event_name: str,
        outcome: str,
        failure_context: dict[str, object],
        profile: SourceProfile | None,
        source_lock: SourceLock | None,
    ) -> None:
        self._observations.emit(
            Observation(
                event_name=event_name,
                run_id=run.run_id if run else command.run_id,
                story_id=self.STORY_ID,
                artifact_identity=(
                    source_lock.aggregate_hash
                    if source_lock
                    else (run.state_hash() if run else "EvidenceWorkspace")
                ),
                authority_identity=command.actor_id,
                version=self.CONTRACT_VERSION,
                provenance=self.STORY_ID,
                outcome=outcome,
                failure_context=dict(failure_context),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                command_id=command.command_id,
                target_id=(
                    run.target_profile.target_id if run else "atomic_content_harness"
                ),
                category_id=(
                    run.target_profile.category_id if run else SYNTHETIC_CATEGORY_ID
                ),
                profile_id=(
                    run.target_profile.profile_id if run else SYNTHETIC_PROFILE_ID
                ),
                stream_version=run.stream_version if run else 0,
                source_profile_id=(
                    profile.profile_id if profile else SOURCE_PROFILE_ID
                ),
                source_profile_version=(
                    profile.version if profile else SOURCE_PROFILE_VERSION
                ),
                source_profile_hash=(
                    profile.profile_sha256 if profile else command.source_profile_sha256
                ),
                target_candidate=(
                    profile.target_candidate.uri
                    if profile
                    else command.target_candidate_uri
                ),
                source_lock_id=(
                    source_lock.lock_id if source_lock else "unassigned"
                ),
            )
        )


def _command_hash(command: LockEvidenceWorkspaceCommand) -> str:
    payload = _canonical_value(asdict(command))
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return f"sha256:{sha256(encoded).hexdigest()}"


def _canonical_value(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): _canonical_value(item) for key, item in value.items()}
    if isinstance(value, (set, frozenset)):
        return sorted(_canonical_value(item) for item in value)
    if isinstance(value, (list, tuple)):
        return [_canonical_value(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    return value
