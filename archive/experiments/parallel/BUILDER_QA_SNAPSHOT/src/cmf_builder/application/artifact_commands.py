from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Mapping

from cmf_builder.application.artifact_renderers import render_artifacts
from cmf_builder.application.authority import Action, ActorKind, AuthorityService
from cmf_builder.application.ports import (
    ArtifactRepository,
    Clock,
    CommandRecord,
    ConcurrencyConflict,
    IdProvider,
    IdempotencyPayloadMismatch,
    Observation,
    ObservationSink,
)
from cmf_builder.domain.generated_artifacts import (
    ARTIFACT_MANIFEST_SCHEMA_ID,
    ArtifactDriftReport,
    ArtifactManifest,
    ArtifactSetCompilationReceipt,
    ArtifactSetInvalidatedError,
    ReproducibleBuildConfig,
)
from cmf_builder.domain.harness_ir import HarnessIR, HarnessIRAuthorityRejected
from cmf_builder.domain.run import LifecycleState, Run


class ArtifactCommandRejected(Exception):
    code = "ArtifactCommandRejected"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class ArtifactUpstreamInvalid(ArtifactCommandRejected):
    code = "ArtifactUpstreamInvalid"


@dataclass(frozen=True, slots=True)
class CompileArtifactSetCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    build_config: ReproducibleBuildConfig


@dataclass(frozen=True, slots=True)
class ValidateArtifactBytesCommand:
    command_id: str
    run_id: str
    actor_id: str
    correlation_id: str
    causation_id: str
    manifest_id: str
    observed_artifacts: Mapping[str, bytes]


class ArtifactCommandService:
    STORY_ID = "ST-03.04"
    CONTRACT_VERSION = ARTIFACT_MANIFEST_SCHEMA_ID

    def __init__(
        self,
        *,
        repository: ArtifactRepository,
        authority: AuthorityService,
        ids: IdProvider,
        clock: Clock,
        observations: ObservationSink,
    ) -> None:
        self._repository = repository
        self._authority = authority
        self._ids = ids
        self._clock = clock
        self._observations = observations

    def compile(
        self, command: CompileArtifactSetCommand
    ) -> ArtifactSetCompilationReceipt:
        run: Run | None = None
        ir: HarnessIR | None = None
        manifest: ArtifactManifest | None = None
        try:
            payload_hash = _command_hash(command)
            duplicate = self._duplicate(command.command_id, payload_hash)
            if duplicate is not None:
                self._emit_replay(command, duplicate)
                return duplicate
            self._validate_command_identity(command)
            run = self._repository.load_run(command.run_id)
            if command.expected_version != run.stream_version:
                raise ConcurrencyConflict(
                    "Expected stream version does not match authoritative state.",
                    expected_version=command.expected_version,
                    current_version=run.stream_version,
                )
            actor = self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.TRANSITION_RUN,
                resource_id=command.run_id,
                now=self._clock.now(),
            )
            if actor.kind is not ActorKind.CODE:
                raise HarnessIRAuthorityRejected(
                    "Only deterministic Builder code may compile generated artifacts.",
                    actor_id=actor.actor_id,
                    actor_kind=actor.kind.value,
                )
            ir = self._load_active_ir(run)
            command.build_config.validate()
            first_render = render_artifacts(ir, command.build_config)
            second_render = render_artifacts(ir, command.build_config)
            if first_render != second_render:
                raise ArtifactCommandRejected(
                    "Deterministic rerender produced different artifacts."
                )
            manifest = ArtifactManifest.create(
                ir=ir,
                config=command.build_config,
                artifacts=first_render,
            )
            event_id = self._ids.new_id("event")
            final_run, event = run.attach_artifact_manifest(
                artifact_set_ref=manifest.artifact_set_id,
                manifest_ref=manifest.manifest_id,
                manifest_hash=manifest.manifest_hash,
                harness_ir_ref=ir.ir_id,
                harness_ir_hash=ir.ir_hash,
                artifact_count=manifest.artifact_count,
                event_id=event_id,
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = ArtifactSetCompilationReceipt.create(
                command_id=command.command_id,
                run_id=run.run_id,
                manifest=manifest,
                authority_identity=command.actor_id,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            receipt.validate(manifest)
            self._repository.commit_artifact_set(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                manifest=manifest,
                artifacts=first_render,
                receipt=receipt,
            )
            for event_name in (
                "ST-03.04:ArtifactSetCompiled",
                "ST-03.04:ArtifactManifestCommitted",
                "ST-03.04:CrossArtifactConsistencyValidated",
                "ST-03.04:OutcomeVerified",
            ):
                self._emit(
                    event_name=event_name,
                    outcome="PASS",
                    command=command,
                    run=final_run,
                    ir=ir,
                    manifest=manifest,
                    receipt=receipt,
                    failure_context={},
                )
            return receipt
        except Exception as error:
            self._reject(command, run=run, ir=ir, manifest=manifest, error=error)
            raise

    def get_active(self, run_id: str) -> ArtifactManifest:
        run = self._repository.load_run(run_id)
        if (
            not run.artifact_set_ref
            or not run.artifact_manifest_ref
            or run.artifact_set_invalidation_ref is not None
            or self._repository.is_artifact_set_invalidated(run.artifact_set_ref)
        ):
            raise ArtifactSetInvalidatedError(
                "No active generated artifact set is available.", run_id=run_id
            )
        manifest = self._repository.get_artifact_manifest(run.artifact_manifest_ref)
        if manifest is None or manifest.artifact_set_id != run.artifact_set_ref:
            raise ArtifactUpstreamInvalid(
                "Run references an unavailable or inconsistent artifact manifest.",
                run_id=run_id,
            )
        ir = self._load_active_ir(run)
        manifest.validate(ir, _manifest_config(manifest))
        return manifest

    def validate_artifacts(
        self, command: ValidateArtifactBytesCommand
    ) -> ArtifactDriftReport:
        if not all(
            value.strip()
            for value in (
                command.command_id,
                command.run_id,
                command.actor_id,
                command.correlation_id,
                command.causation_id,
                command.manifest_id,
            )
        ):
            raise ArtifactCommandRejected("Artifact validation identity is incomplete.")
        run = self._repository.load_run(command.run_id)
        actor = self._authority.authorize(
            actor_id=command.actor_id,
            action=Action.TRANSITION_RUN,
            resource_id=command.run_id,
            now=self._clock.now(),
        )
        if actor.kind is not ActorKind.CODE:
            raise HarnessIRAuthorityRejected(
                "Only deterministic Builder code may validate generated artifacts."
            )
        manifest = self.get_active(command.run_id)
        if manifest.manifest_id != command.manifest_id:
            raise ArtifactUpstreamInvalid(
                "Validation requested a non-active manifest.",
                requested=command.manifest_id,
                active=manifest.manifest_id,
            )
        report = ArtifactDriftReport.create(
            manifest=manifest,
            observed=dict(command.observed_artifacts),
        )
        self._repository.save_artifact_drift_report(report)
        self._emit_validation(command, run, manifest, report)
        return report

    def _load_active_ir(self, run: Run) -> HarnessIR:
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.harness_ir_ref
            or run.harness_ir_invalidation_ref is not None
            or run.boundary_invalidation_ref is not None
            or self._repository.is_harness_ir_invalidated(run.harness_ir_ref)
        ):
            raise ArtifactUpstreamInvalid(
                "Artifact compilation requires one active authorized Harness IR.",
                lifecycle_state=run.lifecycle_state.value,
            )
        ir = self._repository.get_harness_ir(run.harness_ir_ref)
        if ir is None:
            raise ArtifactUpstreamInvalid("Active Harness IR snapshot is unavailable.")
        ir.validate()
        if (
            ir.run_id != run.run_id
            or ir.source_lock_ref != run.source_lock_ref
            or ir.boundary_ref != run.atomic_boundary_ref
            or ir.ratification_ref != run.atomicity_ratification_ref
            or ir.model_ref != run.draft_harness_model_ref
        ):
            raise ArtifactUpstreamInvalid("Harness IR lineage differs from active run lineage.")
        return ir

    @staticmethod
    def _validate_command_identity(command: CompileArtifactSetCommand) -> None:
        if not all(
            value.strip()
            for value in (
                command.command_id,
                command.run_id,
                command.actor_id,
                command.correlation_id,
                command.causation_id,
            )
        ):
            raise ArtifactCommandRejected("Artifact compile command identity is incomplete.")

    def _duplicate(
        self, command_id: str, payload_hash: str
    ) -> ArtifactSetCompilationReceipt | None:
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if record.payload_hash != payload_hash:
            raise IdempotencyPayloadMismatch(
                "Command identity was reused with a different payload.",
                command_id=command_id,
            )
        if not isinstance(record.result, ArtifactSetCompilationReceipt):
            raise IdempotencyPayloadMismatch(
                "Command identity belongs to a different result contract.",
                command_id=command_id,
            )
        return record.result

    def _emit_replay(
        self,
        command: CompileArtifactSetCommand,
        receipt: ArtifactSetCompilationReceipt,
    ) -> None:
        run = self._repository.load_run(command.run_id)
        manifest = self._repository.get_artifact_manifest(receipt.manifest_id)
        ir = self._repository.get_harness_ir(receipt.ir_id)
        if manifest is None or ir is None:
            raise ArtifactUpstreamInvalid("Replay evidence is unavailable.")
        self._emit(
            event_name="ST-03.04:CompilationReplayReturned",
            outcome="PASS",
            command=command,
            run=run,
            ir=ir,
            manifest=manifest,
            receipt=receipt,
            failure_context={},
        )

    def _reject(
        self,
        command: CompileArtifactSetCommand,
        *,
        run: Run | None,
        ir: HarnessIR | None,
        manifest: ArtifactManifest | None,
        error: Exception,
    ) -> None:
        context = dict(getattr(error, "context", {}))
        context.update(
            {
                "code": getattr(error, "code", type(error).__name__),
                "message": str(error),
            }
        )
        self._emit(
            event_name="ST-03.04:OutcomeRejected",
            outcome="FAIL",
            command=command,
            run=run,
            ir=ir,
            manifest=manifest,
            receipt=None,
            failure_context=context,
        )

    def _emit(
        self,
        *,
        event_name: str,
        outcome: str,
        command: CompileArtifactSetCommand,
        run: Run | None,
        ir: HarnessIR | None,
        manifest: ArtifactManifest | None,
        receipt: ArtifactSetCompilationReceipt | None,
        failure_context: dict[str, object],
    ) -> None:
        profile = run.target_profile if run else None
        self._observations.emit(
            Observation(
                event_name=event_name,
                run_id=command.run_id,
                story_id=self.STORY_ID,
                artifact_identity=(manifest.artifact_set_id if manifest else "unassigned"),
                authority_identity=command.actor_id,
                version=self.CONTRACT_VERSION,
                provenance=(ir.ir_hash if ir else "unassigned"),
                outcome=outcome,
                failure_context=failure_context,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                command_id=command.command_id,
                target_id=(profile.target_id if profile else "unassigned"),
                category_id=(profile.category_id if profile else "unassigned"),
                profile_id=(profile.profile_id if profile else "unassigned"),
                stream_version=(run.stream_version if run else command.expected_version),
                source_lock_id=(ir.source_lock_ref if ir else "unassigned"),
                boundary_id=(ir.boundary_ref if ir else "unassigned"),
                model_id=(ir.model_ref if ir else "unassigned"),
                decision_receipt_id=(receipt.receipt_id if receipt else "unassigned"),
                decision_receipt_hash=(receipt.receipt_hash if receipt else "unassigned"),
                harness_ir_id=(ir.ir_id if ir else "unassigned"),
                harness_ir_hash=(ir.ir_hash if ir else "unassigned"),
                harness_ir_schema_id=(ir.schema_id if ir else "unassigned"),
                harness_ir_schema_version=(ir.schema_version if ir else "unassigned"),
                harness_ir_revision=(ir.revision if ir else 0),
                harness_ir_status=(ir.status.value if ir else "unassigned"),
                artifact_set_id=(manifest.artifact_set_id if manifest else "unassigned"),
                artifact_manifest_id=(manifest.manifest_id if manifest else "unassigned"),
                artifact_manifest_hash=(manifest.manifest_hash if manifest else "unassigned"),
                artifact_compiler_id=command.build_config.compiler_id,
                artifact_compiler_version=command.build_config.compiler_version,
                artifact_config_hash=command.build_config.config_hash,
                artifact_generation_timestamp=command.build_config.generation_timestamp,
                artifact_count=(manifest.artifact_count if manifest else 0),
                artifact_total_bytes=(manifest.total_bytes if manifest else 0),
                artifact_dependency_selectors=(
                    tuple(
                        f"{item.path}:{','.join(item.source_node_paths)}"
                        for item in manifest.artifacts
                    )
                    if manifest
                    else ()
                ),
                reproducibility_disposition=(
                    "BYTE_IDENTICAL_DOUBLE_RENDER" if manifest else "unassigned"
                ),
                drift_disposition="MANIFEST_HASH_BOUND",
                quarantine_disposition="NOT_REQUIRED",
                nondeterminism_disposition="NO_EXCEPTIONS",
            )
        )

    def _emit_validation(
        self,
        command: ValidateArtifactBytesCommand,
        run: Run,
        manifest: ArtifactManifest,
        report: ArtifactDriftReport,
    ) -> None:
        self._observations.emit(
            Observation(
                event_name=(
                    "ST-03.04:ArtifactDriftDetected"
                    if report.quarantined
                    else "ST-03.04:CrossArtifactConsistencyValidated"
                ),
                run_id=run.run_id,
                story_id=self.STORY_ID,
                artifact_identity=report.report_id,
                authority_identity=command.actor_id,
                version=self.CONTRACT_VERSION,
                provenance=manifest.manifest_hash,
                outcome=("FAIL" if report.quarantined else "PASS"),
                failure_context={
                    "mismatched_paths": tuple(item.path for item in report.mismatches)
                },
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                command_id=command.command_id,
                target_id=run.target_profile.target_id,
                category_id=run.target_profile.category_id,
                profile_id=run.target_profile.profile_id,
                stream_version=run.stream_version,
                source_lock_id=manifest.source_lock_ref,
                harness_ir_id=manifest.ir_id,
                harness_ir_hash=manifest.ir_hash,
                artifact_set_id=manifest.artifact_set_id,
                artifact_manifest_id=manifest.manifest_id,
                artifact_manifest_hash=manifest.manifest_hash,
                artifact_compiler_id=manifest.compiler_id,
                artifact_compiler_version=manifest.compiler_version,
                artifact_config_hash=manifest.config_hash,
                artifact_generation_timestamp=manifest.generation_timestamp,
                artifact_count=manifest.artifact_count,
                artifact_total_bytes=manifest.total_bytes,
                drift_disposition=report.outcome,
                quarantine_disposition=(
                    "QUARANTINED_NO_IR_MUTATION"
                    if report.quarantined
                    else "NOT_REQUIRED"
                ),
                nondeterminism_disposition="NO_EXCEPTIONS",
            )
        )


def _manifest_config(manifest: ArtifactManifest) -> ReproducibleBuildConfig:
    return ReproducibleBuildConfig(
        compiler_id=manifest.compiler_id,
        compiler_version=manifest.compiler_version,
        config_version=manifest.config_version,
        generation_timestamp=manifest.generation_timestamp,
    )


def _command_hash(command: object) -> str:
    return f"sha256:{sha256(_canonical_json(_canonical_value(asdict(command)))).hexdigest()}"


def _canonical_value(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): _canonical_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_canonical_value(item) for item in value]
    if isinstance(value, bytes):
        return {"sha256": sha256(value).hexdigest(), "length": len(value)}
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
