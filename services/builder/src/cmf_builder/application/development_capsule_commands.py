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
    DevelopmentCapsuleRepository,
    IdempotencyPayloadMismatch,
    IdProvider,
    Observation,
    ObservationSink,
)
from cmf_builder.domain.atomic_harness_definition import AtomicHarnessDefinition
from cmf_builder.domain.development_capsule import (
    CAPSULE_INPUT_PATH,
    CAPSULE_INPUT_SHA256,
    CAPSULE_MODE,
    CAPSULE_OUTCOME,
    CAPSULE_PROFILE_ID,
    DIRECT_DEPENDENCIES,
    OWNED_OBLIGATIONS,
    REQUIRED_CAPSULE_SECTIONS,
    DevelopmentCapsuleAuthorityInvalid,
    DevelopmentCapsuleInputInvalid,
    DevelopmentCapsuleInvalidatedError,
    DevelopmentCapsuleReceipt,
    DevelopmentCapsuleScopeInvalid,
    DevelopmentCapsuleTraceInvalid,
    VersionedTraceableDevelopmentCapsule,
)
from cmf_builder.domain.run import LifecycleState, Run
from cmf_builder.domain.target_package_validation import (
    EXTERNAL_TARGET_COMPATIBILITY,
    AtomicContentHarnessValidationReport,
)


@dataclass(frozen=True, slots=True)
class GenerateDevelopmentCapsuleCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    capsule_input_path: str = CAPSULE_INPUT_PATH
    capsule_input_sha256: str = CAPSULE_INPUT_SHA256
    requested_operation: str = "generate_versioned_traceable_development_capsule"
    requested_mode: str = CAPSULE_MODE
    requested_profile_id: str = CAPSULE_PROFILE_ID
    requested_sections: tuple[str, ...] = REQUIRED_CAPSULE_SECTIONS
    requested_obligations: tuple[str, ...] = OWNED_OBLIGATIONS
    requested_dependencies: tuple[str, ...] = DIRECT_DEPENDENCIES
    requested_external_target_compatibility: str = EXTERNAL_TARGET_COMPATIBILITY
    requested_production_eligible: bool = False
    requested_certified: bool = False
    requested_generated_product_implementation: bool = False
    requested_external_runtime_ids: tuple[str, ...] = ()
    requested_external_skill_ids: tuple[str, ...] = ()
    reference_overrides: tuple[tuple[str, str], ...] = ()
    scaffolding_overrides: tuple[tuple[str, str], ...] = ()


class DevelopmentCapsuleCommandService:
    STORY_ID = "ST-11.01"
    CONTRACT_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        root: Path,
        repository: DevelopmentCapsuleRepository,
        authority: AuthorityService,
        ids: IdProvider,
        clock: Clock,
        observations: ObservationSink,
    ) -> None:
        self._root = root.resolve()
        self._repository = repository
        self._authority = authority
        self._ids = ids
        self._clock = clock
        self._observations = observations

    def generate(
        self, command: GenerateDevelopmentCapsuleCommand
    ) -> DevelopmentCapsuleReceipt:
        run: Run | None = None
        definition: AtomicHarnessDefinition | None = None
        validation: AtomicContentHarnessValidationReport | None = None
        capsule: VersionedTraceableDevelopmentCapsule | None = None
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
            capsule_input = self._load_input(command)
            definition, validation = self._load_active_parents(run)
            capsule = VersionedTraceableDevelopmentCapsule.create(
                definition=definition,
                validation=validation,
                capsule_input=capsule_input,
                authority_identity=command.actor_id,
            )
            event_id = self._ids.new_id("event")
            final_run, event = run.attach_development_capsule(
                capsule_ref=capsule.capsule_id,
                capsule_hash=capsule.capsule_hash,
                validation_ref=capsule.validation_id,
                validation_hash=capsule.validation_hash,
                section_count=len(capsule.sections),
                reference_count=len(capsule.references),
                obligation_count=len(capsule.obligation_ids),
                production_eligible=capsule.production_eligible,
                certified=capsule.certified,
                synthetic_not_certifiable=(
                    capsule.certification_state == "synthetic_not_certifiable"
                ),
                event_id=event_id,
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = DevelopmentCapsuleReceipt.create(
                command_id=command.command_id,
                capsule=capsule,
                authority_identity=command.actor_id,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            self._repository.commit_development_capsule(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                capsule=capsule,
                receipt=receipt,
            )
            self._emit(
                event_name="development_capsule_generation_started",
                outcome="PASS",
                command=command,
                run=final_run,
                definition=definition,
                validation=validation,
                capsule=capsule,
                receipt=receipt,
                replay_status="NEW_COMMIT",
                failure_context={},
            )
            for section in capsule.sections:
                self._emit(
                    event_name=f"development_capsule_section_{section.section_id}",
                    outcome="PASS",
                    command=command,
                    run=final_run,
                    definition=definition,
                    validation=validation,
                    capsule=capsule,
                    receipt=receipt,
                    replay_status="NEW_COMMIT",
                    failure_context={"section": section.section_id},
                )
            self._emit(
                event_name="development_capsule_generation_committed",
                outcome="PASS",
                command=command,
                run=final_run,
                definition=definition,
                validation=validation,
                capsule=capsule,
                receipt=receipt,
                replay_status="NEW_COMMIT",
                failure_context={},
            )
            return receipt
        except Exception as error:
            if not isinstance(error, AtomicCommitFailed):
                self._emit(
                    event_name="development_capsule_generation_rejected",
                    outcome="FAIL",
                    command=command,
                    run=run,
                    definition=definition,
                    validation=validation,
                    capsule=capsule,
                    receipt=None,
                    replay_status="NOT_COMMITTED",
                    failure_context={
                        "code": str(getattr(error, "code", type(error).__name__)),
                        "message": str(error),
                        **dict(getattr(error, "context", {})),
                    },
                )
            raise

    def get_active(self, run_id: str) -> VersionedTraceableDevelopmentCapsule:
        run = self._repository.load_run(run_id)
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.development_capsule_ref
            or run.development_capsule_invalidation_ref is not None
            or self._repository.is_development_capsule_invalidated(
                run.development_capsule_ref
            )
        ):
            raise DevelopmentCapsuleInvalidatedError(
                "No active generated Development Capsule is available."
            )
        capsule = self._repository.get_development_capsule(run.development_capsule_ref)
        definition, validation = self._load_active_parents(
            run, allow_existing_capsule=True
        )
        if capsule is None or capsule.capsule_hash != run.development_capsule_hash:
            raise DevelopmentCapsuleInvalidatedError(
                "The active Development Capsule is missing or altered."
            )
        capsule.validate(definition, validation)
        return capsule

    def get_historical(
        self, capsule_id: str
    ) -> VersionedTraceableDevelopmentCapsule:
        capsule = self._repository.get_development_capsule(capsule_id)
        if capsule is None:
            raise KeyError(capsule_id)
        definition = self._repository.get_atomic_harness_definition(
            capsule.definition_id
        )
        validation = self._repository.get_atomic_content_harness_validation_report(
            capsule.validation_id
        )
        if definition is None or validation is None:
            raise DevelopmentCapsuleTraceInvalid(
                "Historical capsule parents are unavailable."
            )
        capsule.validate(definition, validation)
        return capsule

    def _load_active_parents(
        self, run: Run, *, allow_existing_capsule: bool = False
    ) -> tuple[AtomicHarnessDefinition, AtomicContentHarnessValidationReport]:
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.atomic_harness_definition_ref
            or not run.atomic_content_harness_validation_ref
            or not run.atomic_harness_definition_hash
            or not run.atomic_content_harness_validation_hash
            or run.atomic_harness_definition_invalidation_ref is not None
            or run.atomic_content_harness_validation_invalidation_ref is not None
            or (run.development_capsule_ref is not None and not allow_existing_capsule)
            or run.development_capsule_invalidation_ref is not None
            or self._repository.is_atomic_harness_definition_invalidated(
                run.atomic_harness_definition_ref
            )
            or self._repository.is_atomic_content_harness_validation_invalidated(
                run.atomic_content_harness_validation_ref
            )
        ):
            raise DevelopmentCapsuleInvalidatedError(
                "Capsule generation requires one active validated Harness Definition."
            )
        definition = self._repository.get_atomic_harness_definition(
            run.atomic_harness_definition_ref
        )
        validation = self._repository.get_atomic_content_harness_validation_report(
            run.atomic_content_harness_validation_ref
        )
        if definition is None or validation is None:
            raise DevelopmentCapsuleTraceInvalid(
                "The active definition or validation report is unavailable."
            )
        if (
            definition.definition_hash != run.atomic_harness_definition_hash
            or validation.report_hash != run.atomic_content_harness_validation_hash
            or validation.definition_id != definition.definition_id
            or validation.definition_hash != definition.definition_hash
        ):
            raise DevelopmentCapsuleTraceInvalid(
                "The active definition and validation lineage is altered."
            )
        validation.validate(definition)
        return definition, validation

    def _load_input(
        self, command: GenerateDevelopmentCapsuleCommand
    ) -> Mapping[str, object]:
        if (
            command.capsule_input_path != CAPSULE_INPUT_PATH
            or command.capsule_input_sha256 != CAPSULE_INPUT_SHA256
        ):
            raise DevelopmentCapsuleInputInvalid(
                "Development Capsule input pin differs from capsule authority."
            )
        path = self._safe_path(command.capsule_input_path)
        try:
            raw = path.read_bytes()
            observed = sha256(raw).hexdigest()
            value = json.loads(raw.decode("utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise DevelopmentCapsuleInputInvalid(
                "Development Capsule input is missing, unreadable or invalid."
            ) from error
        if observed != CAPSULE_INPUT_SHA256 or not isinstance(value, Mapping):
            raise DevelopmentCapsuleInputInvalid(
                "Development Capsule input bytes do not match the immutable pin."
            )
        self._verify_referenced_files(value)
        return value

    def _verify_referenced_files(self, value: Mapping[str, object]) -> None:
        groups = (
            "authority_references",
            "requirement_references",
            "technical_spec_references",
            "accepted_adr_references",
            "dependency_receipts",
            "examples_and_fixtures",
        )
        for group in groups:
            items = value.get(group)
            if not isinstance(items, list) or not items:
                raise DevelopmentCapsuleInputInvalid(
                    "A required capsule reference group is missing.", group=group
                )
            for item in items:
                if not isinstance(item, Mapping):
                    raise DevelopmentCapsuleInputInvalid(
                        "Capsule reference entries must be mappings.", group=group
                    )
                path = str(item.get("path", ""))
                expected = str(item.get("sha256", ""))
                if not path or len(expected) != 64:
                    raise DevelopmentCapsuleInputInvalid(
                        "Capsule references require a path and SHA-256.", group=group
                    )
                try:
                    observed = sha256(self._safe_path(path).read_bytes()).hexdigest()
                except OSError as error:
                    raise DevelopmentCapsuleInputInvalid(
                        "A hash-pinned capsule reference is unavailable.", path=path
                    ) from error
                if observed != expected:
                    raise DevelopmentCapsuleTraceInvalid(
                        "A hash-pinned capsule reference has drifted.",
                        path=path,
                        expected=expected,
                        observed=observed,
                    )

    def _safe_path(self, relative: str) -> Path:
        path = (self._root / relative).resolve()
        try:
            path.relative_to(self._root)
        except ValueError as error:
            raise DevelopmentCapsuleScopeInvalid(
                "Capsule references must remain inside the Builder repository.",
                path=relative,
            ) from error
        return path

    def _validate_command(self, command: GenerateDevelopmentCapsuleCommand) -> None:
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
            != "generate_versioned_traceable_development_capsule"
            or command.requested_mode != CAPSULE_MODE
            or command.requested_profile_id != CAPSULE_PROFILE_ID
            or command.requested_sections != REQUIRED_CAPSULE_SECTIONS
            or command.requested_obligations != OWNED_OBLIGATIONS
            or command.requested_dependencies != DIRECT_DEPENDENCIES
            or command.requested_external_target_compatibility
            != EXTERNAL_TARGET_COMPATIBILITY
        ):
            raise DevelopmentCapsuleInputInvalid(
                "Development Capsule command identity or contract is invalid."
            )
        if command.requested_production_eligible or command.requested_certified:
            raise DevelopmentCapsuleAuthorityInvalid(
                "The synthetic capsule cannot claim production or certification."
            )
        if command.requested_generated_product_implementation:
            raise DevelopmentCapsuleScopeInvalid(
                "ST-11.01 generates the capsule and cannot implement its product."
            )
        if command.requested_external_runtime_ids or command.requested_external_skill_ids:
            raise DevelopmentCapsuleScopeInvalid(
                "The synthetic capsule cannot introduce external skills or runtimes."
            )
        if command.reference_overrides or command.scaffolding_overrides:
            raise DevelopmentCapsuleTraceInvalid(
                "Command-supplied references or scaffolding are not authoritative."
            )

    def _authorize_code(self, actor_id: str, run_id: str) -> None:
        actor = self._authority.authorize(
            actor_id=actor_id,
            action=Action.TRANSITION_RUN,
            resource_id=run_id,
            now=self._clock.now(),
        )
        if actor.kind is not ActorKind.CODE:
            raise DevelopmentCapsuleAuthorityInvalid(
                "Only deterministic Builder code may generate the capsule."
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
    ) -> DevelopmentCapsuleReceipt | None:
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if (
            record.payload_hash != payload_hash
            or not isinstance(record.result, DevelopmentCapsuleReceipt)
        ):
            raise IdempotencyPayloadMismatch(
                "Command identity was reused with a different payload or result contract.",
                command_id=command_id,
            )
        return record.result

    def _emit_replay(
        self,
        command: GenerateDevelopmentCapsuleCommand,
        receipt: DevelopmentCapsuleReceipt,
    ) -> None:
        run = self._repository.load_run(command.run_id)
        capsule = self._repository.get_development_capsule(receipt.capsule_id)
        definition = self._repository.get_atomic_harness_definition(
            receipt.definition_id
        )
        validation = self._repository.get_atomic_content_harness_validation_report(
            receipt.validation_id
        )
        if capsule is None or definition is None or validation is None:
            raise DevelopmentCapsuleTraceInvalid(
                "Replayed Development Capsule evidence is unavailable."
            )
        self._emit(
            event_name="development_capsule_generation_replayed",
            outcome="PASS",
            command=command,
            run=run,
            definition=definition,
            validation=validation,
            capsule=capsule,
            receipt=receipt,
            replay_status="ORIGINAL_RECEIPT_RETURNED",
            failure_context={},
        )

    def _emit(
        self,
        *,
        event_name: str,
        outcome: str,
        command: GenerateDevelopmentCapsuleCommand,
        run: Run | None,
        definition: AtomicHarnessDefinition | None,
        validation: AtomicContentHarnessValidationReport | None,
        capsule: VersionedTraceableDevelopmentCapsule | None,
        receipt: DevelopmentCapsuleReceipt | None,
        replay_status: str,
        failure_context: dict[str, object],
    ) -> None:
        self._observations.emit(
            Observation(
                event_name=event_name,
                run_id=command.run_id,
                story_id=self.STORY_ID,
                artifact_identity=(capsule.capsule_id if capsule else "unassigned"),
                authority_identity=command.actor_id,
                version=self.CONTRACT_VERSION,
                provenance=(capsule.capsule_hash if capsule else "unassigned"),
                outcome=outcome,
                failure_context=failure_context,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                command_id=command.command_id,
                target_id=(
                    run.target_profile.target_id if run else command.requested_profile_id
                ),
                category_id=(run.target_profile.category_id if run else "none"),
                profile_id=(
                    run.target_profile.profile_id if run else command.requested_profile_id
                ),
                stream_version=(run.stream_version if run else command.expected_version),
                atomic_harness_definition_id=(
                    definition.definition_id if definition else "unassigned"
                ),
                atomic_harness_definition_hash=(
                    definition.definition_hash if definition else "unassigned"
                ),
                atomic_content_harness_validation_id=(
                    validation.report_id if validation else "unassigned"
                ),
                atomic_content_harness_validation_hash=(
                    validation.report_hash if validation else "unassigned"
                ),
                development_capsule_id=(
                    capsule.capsule_id if capsule else "unassigned"
                ),
                development_capsule_hash=(
                    capsule.capsule_hash if capsule else "unassigned"
                ),
                development_capsule_receipt_id=(
                    receipt.receipt_id if receipt else "unassigned"
                ),
                development_capsule_receipt_hash=(
                    receipt.receipt_hash if receipt else "unassigned"
                ),
                development_capsule_section_count=(
                    len(capsule.sections) if capsule else 0
                ),
                development_capsule_reference_count=(
                    len(capsule.references) if capsule else 0
                ),
                development_capsule_obligation_count=(
                    len(capsule.obligation_ids) if capsule else 0
                ),
                development_capsule_compatibility=(
                    capsule.internal_compatibility if capsule else "unassigned"
                ),
                development_capsule_certification=(
                    capsule.certification_state if capsule else "unassigned"
                ),
                development_capsule_replay_status=replay_status,
            )
        )


def _command_hash(command: GenerateDevelopmentCapsuleCommand) -> str:
    value = json.dumps(
        asdict(command),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return f"sha256:{sha256(value).hexdigest()}"
