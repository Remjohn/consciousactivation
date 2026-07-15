from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json

from cmf_builder.application.artifact_renderers import render_artifacts
from cmf_builder.application.authority import Action, ActorKind, AuthorityService
from cmf_builder.application.ports import (
    Clock,
    CommandRecord,
    ConcurrencyConflict,
    ConstitutionalPolicyRepository,
    ConstitutionalValidationRepository,
    IdProvider,
    IdempotencyPayloadMismatch,
    Observation,
    ObservationSink,
)
from cmf_builder.domain.constitutional_validation import (
    BUILDER_PRD_AMENDMENT_SHA256,
    CONSTITUTION_SHA256,
    POLICY_PATH,
    POLICY_SHA256,
    ArtifactConsistencyFinding,
    ConstitutionalConflict,
    ConstitutionalPolicyInvalid,
    ConstitutionalPrecedencePolicy,
    ConstitutionalValidationInvalidatedError,
    ConstitutionalValidationReceipt,
    ConstitutionalValidationReport,
)
from cmf_builder.domain.generated_artifacts import (
    ARTIFACT_AUTHORITY_CLASS,
    ARTIFACT_PATHS,
    ArtifactManifest,
    ReproducibleBuildConfig,
)
from cmf_builder.domain.harness_ir import (
    ACTIVATIVE_LINEAGE_PATHS,
    CONSTITUTION_REF,
    HarnessIR,
    HarnessIRAuthorityRejected,
)
from cmf_builder.domain.run import LifecycleState, Run


class ConstitutionalCommandRejected(Exception):
    code = "ConstitutionalCommandRejected"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


@dataclass(frozen=True, slots=True)
class ValidateConstitutionalPrecedenceCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    policy_path: str = POLICY_PATH
    policy_sha256: str = POLICY_SHA256
    constitution_sha256: str = CONSTITUTION_SHA256
    builder_prd_amendment_sha256: str = BUILDER_PRD_AMENDMENT_SHA256


class ConstitutionalCommandService:
    STORY_ID = "ST-03.05"
    CONTRACT_VERSION = "cmf-builder-constitutional-validation/v1@1.0.0"

    def __init__(
        self,
        *,
        repository: ConstitutionalValidationRepository,
        policies: ConstitutionalPolicyRepository,
        authority: AuthorityService,
        ids: IdProvider,
        clock: Clock,
        observations: ObservationSink,
    ) -> None:
        self._repository = repository
        self._policies = policies
        self._authority = authority
        self._ids = ids
        self._clock = clock
        self._observations = observations

    def validate(
        self, command: ValidateConstitutionalPrecedenceCommand
    ) -> ConstitutionalValidationReceipt:
        run: Run | None = None
        ir: HarnessIR | None = None
        manifest: ArtifactManifest | None = None
        policy: ConstitutionalPrecedencePolicy | None = None
        report: ConstitutionalValidationReport | None = None
        try:
            payload_hash = _command_hash(command)
            duplicate = self._duplicate(command.command_id, payload_hash)
            if duplicate is not None:
                self._emit_replay(command, duplicate)
                return duplicate
            self._validate_command(command)
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
                    "Only deterministic Builder code may issue a constitutional validation.",
                    actor_id=actor.actor_id,
                    actor_kind=actor.kind.value,
                )
            policy = self._policies.load(command.policy_path, command.policy_sha256)
            if (
                command.constitution_sha256 != policy.constitution_hash
                or command.builder_prd_amendment_sha256
                != policy.builder_prd_amendment_hash
            ):
                raise ConstitutionalPolicyInvalid(
                    "The command authority identities do not match the pinned policy."
                )
            ir, manifest = self._load_active_inputs(run)
            findings = self._findings(ir, manifest)
            if findings:
                raise ConstitutionalConflict(
                    "Generated artifacts conflict with their governing Harness IR.",
                    findings=findings,
                )
            report = ConstitutionalValidationReport.create(
                run_id=run.run_id,
                ir_id=ir.ir_id,
                ir_hash=ir.ir_hash,
                artifact_set_id=manifest.artifact_set_id,
                manifest_id=manifest.manifest_id,
                manifest_hash=manifest.manifest_hash,
                policy=policy,
                coverage=ARTIFACT_PATHS,
                governed_node_count=len(ir.material_values),
                rich_lineage_paths=tuple(sorted(ACTIVATIVE_LINEAGE_PATHS)),
            )
            event_id = self._ids.new_id("event")
            final_run, event = run.attach_constitutional_validation(
                report_ref=report.report_id,
                report_hash=report.report_hash,
                policy_hash=report.policy_hash,
                artifact_set_ref=manifest.artifact_set_id,
                manifest_ref=manifest.manifest_id,
                harness_ir_ref=ir.ir_id,
                event_id=event_id,
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = ConstitutionalValidationReceipt.create(
                command_id=command.command_id,
                run_id=run.run_id,
                report=report,
                authority_identity=command.actor_id,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            receipt.validate(report)
            self._repository.commit_constitutional_validation(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                report=report,
                receipt=receipt,
            )
            for event_name in (
                "ST-03.05:ConstitutionalValidationCompleted",
                "ST-03.05:CrossArtifactCompletenessValidated",
                "ST-03.05:ConstitutionalPrecedenceValidated",
                "ST-03.05:OutcomeVerified",
            ):
                self._emit(
                    event_name=event_name,
                    outcome="PASS",
                    command=command,
                    run=final_run,
                    ir=ir,
                    manifest=manifest,
                    policy=policy,
                    report=report,
                    receipt=receipt,
                    findings=(),
                    failure_context={},
                )
            return receipt
        except Exception as error:
            self._reject(
                command,
                run=run,
                ir=ir,
                manifest=manifest,
                policy=policy,
                report=report,
                error=error,
            )
            raise

    def get_active(self, run_id: str) -> ConstitutionalValidationReport:
        run = self._repository.load_run(run_id)
        if (
            not run.constitutional_validation_ref
            or run.constitutional_validation_invalidation_ref is not None
            or self._repository.is_constitutional_validation_invalidated(
                run.constitutional_validation_ref
            )
        ):
            raise ConstitutionalValidationInvalidatedError(
                "No active constitutional validation report is available.", run_id=run_id
            )
        report = self._repository.get_constitutional_validation_report(
            run.constitutional_validation_ref
        )
        if report is None or report.report_hash != run.constitutional_validation_hash:
            raise ConstitutionalValidationInvalidatedError(
                "The active constitutional validation reference is unavailable or drifted."
            )
        report.validate()
        self._policies.load(report.policy_path, report.policy_hash)
        return report

    def get_historical(self, report_id: str) -> ConstitutionalValidationReport:
        report = self._repository.get_constitutional_validation_report(report_id)
        if report is None:
            raise KeyError(report_id)
        report.validate()
        self._policies.load(report.policy_path, report.policy_hash)
        return report

    def _load_active_inputs(self, run: Run) -> tuple[HarnessIR, ArtifactManifest]:
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.harness_ir_ref
            or not run.artifact_set_ref
            or not run.artifact_manifest_ref
            or run.boundary_invalidation_ref is not None
            or run.harness_ir_invalidation_ref is not None
            or run.artifact_set_invalidation_ref is not None
            or run.constitutional_validation_ref is not None
            or self._repository.is_harness_ir_invalidated(run.harness_ir_ref)
            or self._repository.is_artifact_set_invalidated(run.artifact_set_ref)
        ):
            raise ConstitutionalCommandRejected(
                "Constitutional validation requires one active ST-03.04 artifact set.",
                lifecycle_state=run.lifecycle_state.value,
            )
        ir = self._repository.get_harness_ir(run.harness_ir_ref)
        manifest = self._repository.get_artifact_manifest(run.artifact_manifest_ref)
        if ir is None or manifest is None:
            raise ConstitutionalCommandRejected(
                "Harness IR or artifact manifest is unavailable."
            )
        ir.validate()
        manifest.validate(ir, _manifest_config(manifest))
        if (
            manifest.run_id != run.run_id
            or manifest.artifact_set_id != run.artifact_set_ref
            or manifest.manifest_hash != run.artifact_manifest_hash
            or manifest.ir_id != ir.ir_id
            or manifest.ir_hash != ir.ir_hash
            or manifest.source_lock_ref != run.source_lock_ref
        ):
            raise ConstitutionalCommandRejected(
                "Run, Harness IR, and artifact-manifest lineage differ."
            )
        return ir, manifest

    def _findings(
        self, ir: HarnessIR, manifest: ArtifactManifest
    ) -> tuple[ArtifactConsistencyFinding, ...]:
        findings: list[ArtifactConsistencyFinding] = []
        stored = self._repository.artifacts_for_manifest(manifest.manifest_id)
        expected = render_artifacts(ir, _manifest_config(manifest))
        stored_by_path = {item.path: item for item in stored}
        expected_by_path = {item.path: item for item in expected}
        if tuple(sorted(stored_by_path)) != ARTIFACT_PATHS or len(stored) != len(
            stored_by_path
        ):
            findings.append(
                _finding(
                    "ARTIFACT_INVENTORY_MISMATCH",
                    "Stored artifact inventory is missing, duplicated, or expanded.",
                )
            )
        manifest_by_path = {item.path: item for item in manifest.artifacts}
        for path in ARTIFACT_PATHS:
            actual = stored_by_path.get(path)
            declared = manifest_by_path.get(path)
            wanted = expected_by_path[path]
            node_paths = wanted.source_node_paths
            if actual is None or declared is None:
                findings.append(
                    _finding(
                        "ARTIFACT_MISSING",
                        "A required generated view is absent.",
                        artifact_path=path,
                        ir_node_paths=node_paths,
                    )
                )
                continue
            if actual != declared:
                findings.append(
                    _finding(
                        "MANIFEST_ARTIFACT_BINDING_MISMATCH",
                        "Stored bytes or metadata differ from the immutable manifest.",
                        artifact_path=path,
                        ir_node_paths=node_paths,
                    )
                )
            if actual != wanted:
                findings.append(
                    _finding(
                        "PROJECTED_SEMANTIC_DRIFT",
                        "The generated view is not the deterministic projection of Harness IR.",
                        artifact_path=path,
                        ir_node_paths=node_paths,
                    )
                )
            if (
                actual.authority_class != ARTIFACT_AUTHORITY_CLASS
                or actual.source_ir_id != ir.ir_id
                or actual.source_ir_hash != ir.ir_hash
            ):
                findings.append(
                    _finding(
                        "LOWER_AUTHORITY_OVERRIDE",
                        "A generated view escalated authority or lost its Harness IR source.",
                        artifact_path=path,
                        ir_node_paths=node_paths,
                    )
                )
        ir_paths = {item.path for item in ir.material_values}
        unresolved = tuple(
            sorted(
                {
                    node
                    for artifact in (*manifest.artifacts, *stored)
                    for node in artifact.source_node_paths
                    if node not in ir_paths
                }
            )
        )
        if unresolved:
            findings.append(
                _finding(
                    "UNRESOLVED_HARNESS_IR_REFERENCE",
                    "One or more projected nodes do not exist in active Harness IR.",
                    ir_node_paths=unresolved,
                )
            )
        if ir.constitution_ref != CONSTITUTION_REF:
            findings.append(
                _finding(
                    "CONSTITUTION_REFERENCE_DRIFT",
                    "Harness IR does not reference Constitution V1.1.",
                    ir_node_paths=("references.constitution",),
                )
            )
        for path in ACTIVATIVE_LINEAGE_PATHS:
            try:
                value = ir.value(path)
            except KeyError:
                findings.append(
                    _finding(
                        "RICH_LINEAGE_KEY_MISSING",
                        "A required Activative lineage key is absent.",
                        ir_node_paths=(path,),
                    )
                )
                continue
            if (
                value.value is not None
                or value.knowledge_status != "NOT_APPLICABLE"
                or value.authority_status != "NOT_APPLICABLE"
                or value.disposition
                != "NOT_APPLICABLE_FOR_CATEGORY_NEUTRAL_SYNTHETIC_PROOF"
            ):
                findings.append(
                    _finding(
                        "APPLICABILITY_SEMANTICS_LOST",
                        "Synthetic rich lineage must remain explicit NOT_APPLICABLE.",
                        ir_node_paths=(path,),
                    )
                )
        return tuple(
            sorted(
                findings,
                key=lambda item: (
                    item.code,
                    item.artifact_path or "",
                    item.ir_node_paths,
                ),
            )
        )

    @staticmethod
    def _validate_command(command: ValidateConstitutionalPrecedenceCommand) -> None:
        if not all(
            value.strip()
            for value in (
                command.command_id,
                command.run_id,
                command.actor_id,
                command.correlation_id,
                command.causation_id,
                command.policy_path,
                command.policy_sha256,
                command.constitution_sha256,
                command.builder_prd_amendment_sha256,
            )
        ):
            raise ConstitutionalCommandRejected(
                "Constitutional validation command identity is incomplete."
            )
        if (
            command.policy_path != POLICY_PATH
            or command.policy_sha256 != POLICY_SHA256
        ):
            raise ConstitutionalPolicyInvalid(
                "An arbitrary or unpinned policy is prohibited."
            )

    def _duplicate(
        self, command_id: str, payload_hash: str
    ) -> ConstitutionalValidationReceipt | None:
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if record.payload_hash != payload_hash:
            raise IdempotencyPayloadMismatch(
                "Command identity was reused with a different payload.",
                command_id=command_id,
            )
        if not isinstance(record.result, ConstitutionalValidationReceipt):
            raise IdempotencyPayloadMismatch(
                "Command identity belongs to a different result contract.",
                command_id=command_id,
            )
        return record.result

    def _emit_replay(
        self,
        command: ValidateConstitutionalPrecedenceCommand,
        receipt: ConstitutionalValidationReceipt,
    ) -> None:
        run = self._repository.load_run(command.run_id)
        report = self._repository.get_constitutional_validation_report(
            receipt.report_id
        )
        if report is None:
            raise ConstitutionalCommandRejected("Replay report is unavailable.")
        manifest = self._repository.get_artifact_manifest(report.manifest_id)
        ir = self._repository.get_harness_ir(report.ir_id)
        policy = self._policies.load(report.policy_path, report.policy_hash)
        if manifest is None or ir is None:
            raise ConstitutionalCommandRejected("Replay lineage is unavailable.")
        self._emit(
            event_name="ST-03.05:ValidationReplayReturned",
            outcome="PASS",
            command=command,
            run=run,
            ir=ir,
            manifest=manifest,
            policy=policy,
            report=report,
            receipt=receipt,
            findings=(),
            failure_context={},
        )

    def _reject(
        self,
        command: ValidateConstitutionalPrecedenceCommand,
        *,
        run: Run | None,
        ir: HarnessIR | None,
        manifest: ArtifactManifest | None,
        policy: ConstitutionalPrecedencePolicy | None,
        report: ConstitutionalValidationReport | None,
        error: Exception,
    ) -> None:
        findings = (
            error.findings if isinstance(error, ConstitutionalConflict) else ()
        )
        context = {
            "code": str(getattr(error, "code", type(error).__name__)),
            "message": str(error),
            **dict(getattr(error, "context", {})),
        }
        if findings:
            self._emit(
                event_name="ST-03.05:ConstitutionalConflictDetected",
                outcome="FAIL",
                command=command,
                run=run,
                ir=ir,
                manifest=manifest,
                policy=policy,
                report=report,
                receipt=None,
                findings=findings,
                failure_context=context,
            )
        self._emit(
            event_name="ST-03.05:OutcomeRejected",
            outcome="FAIL",
            command=command,
            run=run,
            ir=ir,
            manifest=manifest,
            policy=policy,
            report=report,
            receipt=None,
            findings=findings,
            failure_context=context,
        )

    def _emit(
        self,
        *,
        event_name: str,
        outcome: str,
        command: ValidateConstitutionalPrecedenceCommand,
        run: Run | None,
        ir: HarnessIR | None,
        manifest: ArtifactManifest | None,
        policy: ConstitutionalPrecedencePolicy | None,
        report: ConstitutionalValidationReport | None,
        receipt: ConstitutionalValidationReceipt | None,
        findings: tuple[ArtifactConsistencyFinding, ...],
        failure_context: dict[str, object],
    ) -> None:
        profile = run.target_profile if run else None
        self._observations.emit(
            Observation(
                event_name=event_name,
                run_id=command.run_id,
                story_id=self.STORY_ID,
                artifact_identity=(report.report_id if report else "unassigned"),
                authority_identity=command.actor_id,
                version=self.CONTRACT_VERSION,
                provenance=(manifest.manifest_hash if manifest else "unassigned"),
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
                activative_lineage_disposition=(
                    "EXPLICIT_NOT_APPLICABLE_SEPARATE_KEYS"
                    if ir
                    else "unassigned"
                ),
                artifact_set_id=(manifest.artifact_set_id if manifest else "unassigned"),
                artifact_manifest_id=(manifest.manifest_id if manifest else "unassigned"),
                artifact_manifest_hash=(manifest.manifest_hash if manifest else "unassigned"),
                artifact_count=(manifest.artifact_count if manifest else 0),
                constitutional_policy_path=(policy.source_path if policy else command.policy_path),
                constitutional_policy_hash=(policy.source_hash if policy else command.policy_sha256),
                constitution_hash=(policy.constitution_hash if policy else command.constitution_sha256),
                builder_prd_amendment_hash=(
                    policy.builder_prd_amendment_hash
                    if policy
                    else command.builder_prd_amendment_sha256
                ),
                constitutional_report_id=(report.report_id if report else "unassigned"),
                constitutional_report_hash=(report.report_hash if report else "unassigned"),
                constitutional_receipt_id=(receipt.receipt_id if receipt else "unassigned"),
                constitutional_receipt_hash=(receipt.receipt_hash if receipt else "unassigned"),
                constitutional_finding_codes=tuple(item.code for item in findings),
                constitutional_artifact_paths=tuple(
                    sorted({item.artifact_path for item in findings if item.artifact_path})
                ),
                constitutional_ir_node_paths=tuple(
                    sorted({path for item in findings for path in item.ir_node_paths})
                ),
                constitutional_coverage_count=(len(report.coverage) if report else 0),
                constitutional_precedence_disposition=(
                    "PASS_HIGHER_AUTHORITY_PRESERVED"
                    if outcome == "PASS"
                    else "BLOCKED_FAIL_CLOSED"
                ),
            )
        )


def _manifest_config(manifest: ArtifactManifest) -> ReproducibleBuildConfig:
    return ReproducibleBuildConfig(
        compiler_id=manifest.compiler_id,
        compiler_version=manifest.compiler_version,
        config_version=manifest.config_version,
        generation_timestamp=manifest.generation_timestamp,
    )


def _finding(
    code: str,
    message: str,
    *,
    artifact_path: str | None = None,
    ir_node_paths: tuple[str, ...] = (),
) -> ArtifactConsistencyFinding:
    return ArtifactConsistencyFinding(
        code=code,
        severity="ERROR",
        message=message,
        artifact_path=artifact_path,
        ir_node_paths=tuple(sorted(set(ir_node_paths))),
    )


def _command_hash(command: object) -> str:
    payload = _canonical_value(asdict(command))
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return f"sha256:{sha256(encoded).hexdigest()}"


def _canonical_value(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): _canonical_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_canonical_value(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value
