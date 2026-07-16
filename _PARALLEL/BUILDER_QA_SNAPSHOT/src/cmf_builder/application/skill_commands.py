from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from pathlib import Path

from cmf_builder.application.authority import Action, ActorKind, AuthorityService
from cmf_builder.application.ports import (
    Clock,
    CommandRecord,
    ConcurrencyConflict,
    IdProvider,
    IdempotencyPayloadMismatch,
    Observation,
    ObservationSink,
    SkillNecessityRepository,
    SkillRegistryRepository,
)
from cmf_builder.domain.context_manifest import MinimumCompleteContextGraph
from cmf_builder.domain.harness_ir import HarnessIRAuthorityRejected
from cmf_builder.domain.run import LifecycleState, Run
from cmf_builder.domain.skill_registry import (
    ALLOWED_OPERATIONS,
    AUTHORITY_LANES,
    CAPABILITY_IDS,
    MATURITY_STATES,
    MINIMUM_CONTEXT_CONTRACT,
    PLASTICITY_STATES,
    PROHIBITED_OPERATIONS,
    REGISTRY_FIXTURE_PATH,
    REGISTRY_FIXTURE_SHA256,
    REGISTRY_ID,
    REGISTRY_POLICY_ID,
    REGISTRY_POLICY_PATH,
    REGISTRY_POLICY_SHA256,
    REGISTRY_POLICY_VERSION,
    REGISTRY_REF,
    REGISTRY_SCHEMA_PATH,
    REGISTRY_SCHEMA_SHA256,
    REGISTRY_VALIDATION_RECEIPT_ID,
    REGISTRY_VALIDATION_RECEIPT_PATH,
    REGISTRY_VALIDATION_RECEIPT_SHA256,
    REGISTRY_VERSION,
    SKILL_REGISTRY_INPUT_PATH,
    SKILL_REGISTRY_INPUT_SCHEMA,
    SKILL_REGISTRY_INPUT_SHA256,
    SKILL_REGISTRY_SCOPE,
    SKILL_REGISTRY_SNAPSHOT_SCHEMA_ID,
    SKILL_REGISTRY_SNAPSHOT_SCHEMA_VERSION,
    GOVERNED_ALTERNATIVE_ORDER,
    SKILL_NECESSITY_ALLOWED_OPERATIONS,
    SKILL_NECESSITY_DECISION_SCHEMA_ID,
    SKILL_NECESSITY_DECISION_SCHEMA_VERSION,
    SKILL_NECESSITY_INPUT_PATH,
    SKILL_NECESSITY_INPUT_SCHEMA,
    SKILL_NECESSITY_INPUT_SHA256,
    SKILL_NECESSITY_PROHIBITED_OPERATIONS,
    SKILL_NECESSITY_SCOPE,
    CapabilityGapEvidence,
    CapabilityClassification,
    CapabilityDeclaration,
    GovernedAlternativeAssessment,
    MissingRequiredSkill,
    SkillDesignBriefDisposition,
    SkillNecessityAuthorityInvalid,
    SkillNecessityDecision,
    SkillNecessityEvidenceInvalid,
    SkillNecessityInvalidatedError,
    SkillNecessityReceipt,
    SkillNecessityVerdict,
    SkillClassificationTaxonomy,
    SkillRegistryAuthorityInvalid,
    SkillRegistryConsumptionReceipt,
    SkillRegistryContractInvalid,
    SkillRegistryInputInvalid,
    SkillRegistryInvalidatedError,
    SkillRegistryLineageInvalid,
    SkillRegistryStateInvalid,
    SyntheticSkillRegistrySnapshot,
    UndeclaredSkillRequirement,
)


@dataclass(frozen=True, slots=True)
class CompileSyntheticSkillRegistryCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    registry_input_path: str = SKILL_REGISTRY_INPUT_PATH
    registry_input_sha256: str = SKILL_REGISTRY_INPUT_SHA256
    registry_fixture_path: str = REGISTRY_FIXTURE_PATH
    registry_fixture_sha256: str = REGISTRY_FIXTURE_SHA256
    policy_path: str = REGISTRY_POLICY_PATH
    policy_sha256: str = REGISTRY_POLICY_SHA256
    schema_path: str = REGISTRY_SCHEMA_PATH
    schema_sha256: str = REGISTRY_SCHEMA_SHA256
    validation_receipt_path: str = REGISTRY_VALIDATION_RECEIPT_PATH
    validation_receipt_sha256: str = REGISTRY_VALIDATION_RECEIPT_SHA256
    registry_ref: str = REGISTRY_REF
    requested_operation: str = "consume_exact_registry"
    declared_external_skill_ids: tuple[str, ...] = ()
    capability_overrides: tuple[tuple[str, str], ...] = ()
    relation_edges: tuple[tuple[str, str], ...] = ()
    evaluator_receipt_ids: tuple[str, ...] = ()
    active_maturity_claims: tuple[tuple[str, str], ...] = ()


class SyntheticSkillRegistryCommandService:
    STORY_ID = "ST-05.01"
    CONTRACT_VERSION = (
        f"{SKILL_REGISTRY_SNAPSHOT_SCHEMA_ID}@{SKILL_REGISTRY_SNAPSHOT_SCHEMA_VERSION}"
    )

    def __init__(
        self,
        *,
        root: Path,
        repository: SkillRegistryRepository,
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

    def compile(
        self, command: CompileSyntheticSkillRegistryCommand
    ) -> SkillRegistryConsumptionReceipt:
        run: Run | None = None
        context: MinimumCompleteContextGraph | None = None
        snapshot: SyntheticSkillRegistrySnapshot | None = None
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
            context = self._load_active_context(run)
            self._validate_governance(command)
            self._load_and_validate_input(command)
            declarations = self._classify_capabilities(context)
            taxonomy = SkillClassificationTaxonomy(
                authority_lanes=AUTHORITY_LANES,
                maturity_states=MATURITY_STATES,
                plasticity_states=PLASTICITY_STATES,
                canonical_skills=(),
                harness_local_adaptations=(),
                experimental_capabilities=(),
                recipes=(),
                jit_capsules=(),
            )
            snapshot = SyntheticSkillRegistrySnapshot.create(
                context=context,
                authority_identity=command.actor_id,
                capability_classifications=declarations,
                taxonomy=taxonomy,
            )
            event_id = self._ids.new_id("event")
            final_run, event = run.attach_skill_registry_snapshot(
                snapshot_ref=snapshot.snapshot_id,
                snapshot_hash=snapshot.snapshot_hash,
                registry_ref=snapshot.registry_ref,
                registry_hash=snapshot.registry_hash,
                minimum_context_ref=context.graph_id,
                capability_count=len(snapshot.capability_classifications),
                registered_skill_count=snapshot.registry_skill_count,
                required_external_skill_count=snapshot.required_external_skill_count,
                event_id=event_id,
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = SkillRegistryConsumptionReceipt.create(
                command_id=command.command_id,
                snapshot=snapshot,
                authority_identity=command.actor_id,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            self._repository.commit_skill_registry_snapshot(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                snapshot=snapshot,
                receipt=receipt,
            )
            for event_name in (
                "synthetic_skill_registry_compilation_started",
                "synthetic_skill_registry_validated",
                "synthetic_skill_registry_snapshot_committed",
            ):
                self._emit(
                    event_name=event_name,
                    outcome="PASS",
                    command=command,
                    run=final_run,
                    context=context,
                    snapshot=snapshot,
                    receipt=receipt,
                    replay_status="NEW_COMMIT",
                    failure_context={},
                )
            return receipt
        except Exception as error:
            self._emit(
                event_name="synthetic_skill_registry_rejected",
                outcome="FAIL",
                command=command,
                run=run,
                context=context,
                snapshot=snapshot,
                receipt=None,
                replay_status="NOT_COMMITTED",
                failure_context={
                    "code": str(getattr(error, "code", type(error).__name__)),
                    "message": str(error),
                    **dict(getattr(error, "context", {})),
                },
            )
            raise

    def get_active(self, run_id: str) -> SyntheticSkillRegistrySnapshot:
        run = self._repository.load_run(run_id)
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.skill_registry_snapshot_ref
            or run.skill_registry_snapshot_invalidation_ref is not None
            or self._repository.is_skill_registry_snapshot_invalidated(
                run.skill_registry_snapshot_ref
            )
        ):
            raise SkillRegistryInvalidatedError(
                "No active synthetic skill-registry snapshot is available."
            )
        snapshot = self._repository.get_skill_registry_snapshot(
            run.skill_registry_snapshot_ref
        )
        context = self._repository.get_minimum_context_graph(
            run.minimum_context_ref or ""
        )
        if (
            snapshot is None
            or context is None
            or snapshot.snapshot_hash != run.skill_registry_snapshot_hash
        ):
            raise SkillRegistryInvalidatedError(
                "The active skill-registry snapshot is missing or altered."
            )
        snapshot.validate(context)
        return snapshot

    def get_historical(self, snapshot_id: str) -> SyntheticSkillRegistrySnapshot:
        snapshot = self._repository.get_skill_registry_snapshot(snapshot_id)
        if snapshot is None:
            raise KeyError(snapshot_id)
        context = self._repository.get_minimum_context_graph(
            snapshot.minimum_context_graph_id
        )
        if context is None:
            raise KeyError(snapshot.minimum_context_graph_id)
        snapshot.validate(context)
        return snapshot

    def _load_active_context(self, run: Run) -> MinimumCompleteContextGraph:
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.minimum_context_ref
            or run.minimum_context_invalidation_ref is not None
            or run.skill_registry_snapshot_ref is not None
            or run.skill_registry_snapshot_invalidation_ref is not None
            or self._repository.is_minimum_context_invalidated(
                run.minimum_context_ref
            )
        ):
            raise SkillRegistryInvalidatedError(
                "Skill snapshot compilation requires the exact active Minimum Complete Context."
            )
        context = self._repository.get_minimum_context_graph(run.minimum_context_ref)
        if context is None or context.graph_hash != run.minimum_context_hash:
            raise SkillRegistryLineageInvalid(
                "Minimum Complete Context identity or hash is unavailable."
            )
        handoff_graph = self._repository.get_phase_handoff_graph(context.handoff_graph_id)
        phase_graph = self._repository.get_phase_graph(context.phase_graph_id)
        handoff = self._repository.get_internal_handoff(context.accepted_handoff_id)
        decision = self._repository.get_internal_handoff_decision(
            context.accepted_handoff_id
        )
        if handoff_graph is None or phase_graph is None or handoff is None or decision is None:
            raise SkillRegistryLineageInvalid(
                "Minimum Complete Context parent lineage is unavailable."
            )
        context.validate(handoff_graph, phase_graph, handoff, decision)
        return context

    def _validate_governance(
        self, command: CompileSyntheticSkillRegistryCommand
    ) -> None:
        fixture = self._verified_file(
            command.registry_fixture_path,
            command.registry_fixture_sha256,
            REGISTRY_FIXTURE_PATH,
            REGISTRY_FIXTURE_SHA256,
        )
        policy = self._verified_file(
            command.policy_path,
            command.policy_sha256,
            REGISTRY_POLICY_PATH,
            REGISTRY_POLICY_SHA256,
        )
        schema_path = self._verified_file(
            command.schema_path,
            command.schema_sha256,
            REGISTRY_SCHEMA_PATH,
            REGISTRY_SCHEMA_SHA256,
        )
        receipt_path = self._verified_file(
            command.validation_receipt_path,
            command.validation_receipt_sha256,
            REGISTRY_VALIDATION_RECEIPT_PATH,
            REGISTRY_VALIDATION_RECEIPT_SHA256,
        )
        try:
            fixture_text = fixture.read_text(encoding="utf-8")
            policy_text = policy.read_text(encoding="utf-8")
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise SkillRegistryInputInvalid(
                "Governed empty-registry artifacts are unreadable or non-canonical."
            ) from error
        required_fixture_tokens = (
            f"registry_id: {REGISTRY_ID}",
            f"version: {REGISTRY_VERSION}",
            "status: ACTIVE_SYNTHETIC_PROOF_ONLY",
            "skills: []",
            "external_skills_required: false",
            "dynamic_skill_discovery_allowed: false",
            "undeclared_skill_use: FAIL_CLOSED",
            "production_inference: PROHIBITED",
            *tuple(f"capability_id: {item}" for item in CAPABILITY_IDS),
        )
        if any(token not in fixture_text for token in required_fixture_tokens):
            raise SkillRegistryContractInvalid(
                "The governed empty registry is semantically incomplete."
            )
        if (
            f"policy_id: {REGISTRY_POLICY_ID}" not in policy_text
            or f"version: {REGISTRY_POLICY_VERSION}" not in policy_text
            or "required_capability_ownership: builder_code" not in policy_text
            or "production_inference: PROHIBITED" not in policy_text
        ):
            raise SkillRegistryContractInvalid(
                "The governed empty-registry policy is semantically incomplete."
            )
        if (
            not isinstance(schema, dict)
            or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
            or schema.get("additionalProperties") is not False
            or not isinstance(receipt, dict)
            or receipt.get("receipt_id") != REGISTRY_VALIDATION_RECEIPT_ID
            or receipt.get("verdict") != "PASS"
            or receipt.get("artifacts", {}).get("fixture", {}).get("sha256")
            != REGISTRY_FIXTURE_SHA256
            or receipt.get("artifacts", {}).get("policy", {}).get("sha256")
            != REGISTRY_POLICY_SHA256
            or receipt.get("artifacts", {}).get("schema", {}).get("sha256")
            != REGISTRY_SCHEMA_SHA256
            or receipt.get("validation", {}).get("skills_array_empty") != "PASS"
            or receipt.get("validation", {}).get(
                "all_capabilities_builder_code_owned"
            ) != "PASS_5_OF_5"
        ):
            raise SkillRegistryContractInvalid(
                "Schema or validation receipt does not prove the pinned zero-skill registry."
            )

    def _load_and_validate_input(
        self, command: CompileSyntheticSkillRegistryCommand
    ) -> None:
        path = self._verified_file(
            command.registry_input_path,
            command.registry_input_sha256,
            SKILL_REGISTRY_INPUT_PATH,
            SKILL_REGISTRY_INPUT_SHA256,
        )
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise SkillRegistryInputInvalid(
                "Skill-registry consumption input is not canonical UTF-8 JSON."
            ) from error
        registry = value.get("registry", {}) if isinstance(value, dict) else {}
        contract = value.get("classification_contract", {}) if isinstance(value, dict) else {}
        declarations = value.get("declarations", {}) if isinstance(value, dict) else {}
        capabilities = value.get("expected_capabilities", []) if isinstance(value, dict) else []
        observed = tuple(
            sorted(
                item.get("capability_id", "")
                for item in capabilities
                if isinstance(item, dict)
            )
        )
        if (
            not isinstance(value, dict)
            or value.get("schema_version") != SKILL_REGISTRY_INPUT_SCHEMA
            or value.get("scope") != SKILL_REGISTRY_SCOPE
            or value.get("source_contract") != MINIMUM_CONTEXT_CONTRACT
            or registry.get("registry_ref") != REGISTRY_REF
            or registry.get("fixture_path") != REGISTRY_FIXTURE_PATH
            or registry.get("fixture_sha256") != REGISTRY_FIXTURE_SHA256
            or registry.get("policy_path") != REGISTRY_POLICY_PATH
            or registry.get("policy_sha256") != REGISTRY_POLICY_SHA256
            or registry.get("schema_path") != REGISTRY_SCHEMA_PATH
            or registry.get("schema_sha256") != REGISTRY_SCHEMA_SHA256
            or registry.get("validation_receipt_path")
            != REGISTRY_VALIDATION_RECEIPT_PATH
            or registry.get("validation_receipt_sha256")
            != REGISTRY_VALIDATION_RECEIPT_SHA256
            or observed != CAPABILITY_IDS
            or any(
                item.get("owner_kind") != "builder_code"
                or item.get("skill_required") is not False
                or item.get("determinism") != "deterministic"
                for item in capabilities
            )
            or tuple(contract.get("authority_lanes", ())) != AUTHORITY_LANES
            or tuple(contract.get("maturity_states", ())) != MATURITY_STATES
            or tuple(contract.get("plasticity_states", ())) != PLASTICITY_STATES
            or any(contract.get(name) != [] for name in (
                "canonical_skills",
                "harness_local_adaptations",
                "experimental_capabilities",
            ))
            or tuple(sorted(value.get("allowed_operations", ()))) != ALLOWED_OPERATIONS
            or tuple(sorted(value.get("prohibited_operations", ()))) != PROHIBITED_OPERATIONS
            or declarations != {
                "external_skills_required": False,
                "dynamic_skill_discovery_allowed": False,
                "undeclared_skill_use": "FAIL_CLOSED",
                "later_external_skill_effect": "NEW_IMMUTABLE_HARNESS_VERSION_REQUIRED",
                "production_inference": "PROHIBITED",
            }
            or value.get("real_profile_registry_subscope")
            != "DEFERRED_BLOCKED_BY_EXISTING_GATES"
            or value.get("production_eligible") is not False
            or value.get("certified") is not False
        ):
            raise SkillRegistryInputInvalid(
                "Skill-registry consumption input is incomplete, altered, or broadened."
            )

    def _classify_capabilities(
        self, context: MinimumCompleteContextGraph
    ) -> tuple[CapabilityDeclaration, ...]:
        manifests = tuple(sorted(item.manifest_id for item in context.manifests))
        modules = tuple(sorted(item.module_ref for item in context.manifests))
        phases = tuple(sorted(item.phase_ref for item in context.manifests))
        common_evidence = tuple(sorted((
            context.graph_id,
            context.graph_hash,
            context.capability_graph_id,
            context.module_graph_id,
            context.phase_graph_id,
            context.accepted_handoff_id,
            context.acceptance_decision_id,
        )))
        declarations = tuple(
            CapabilityDeclaration(
                capability_id=capability_id,
                classification=CapabilityClassification.BUILDER_OWNED_CODE,
                owner_kind="builder_code",
                owner_id=f"cmf_builder.{capability_id}",
                authority_boundary="builder_code_validation",
                module_refs=modules,
                phase_refs=phases,
                context_manifest_refs=manifests,
                evidence_refs=common_evidence,
                determinism="deterministic",
                skill_required=False,
                external_skill_required=False,
            )
            for capability_id in CAPABILITY_IDS
        )
        for declaration in declarations:
            declaration.validate()
        return declarations

    def _validate_command(
        self, command: CompileSyntheticSkillRegistryCommand
    ) -> None:
        if (
            not all(value.strip() for value in (
                command.command_id,
                command.run_id,
                command.actor_id,
                command.correlation_id,
                command.causation_id,
            ))
            or command.expected_version < 1
            or command.registry_ref != REGISTRY_REF
        ):
            raise SkillRegistryInputInvalid(
                "Skill-registry command identity or registry version is invalid."
            )
        if command.requested_operation not in ALLOWED_OPERATIONS:
            raise SkillRegistryAuthorityInvalid(
                "The requested skill operation is outside ST-05.01 authority.",
                requested_operation=command.requested_operation,
            )
        if command.requested_operation in PROHIBITED_OPERATIONS:
            raise SkillRegistryAuthorityInvalid(
                "The requested skill operation is explicitly prohibited."
            )
        if command.declared_external_skill_ids:
            raise UndeclaredSkillRequirement(
                "The synthetic proof cannot declare or consume an external skill.",
                skill_ids=command.declared_external_skill_ids,
                required_remediation="NEW_IMMUTABLE_HARNESS_VERSION_REQUIRED",
            )
        if command.capability_overrides:
            raise SkillRegistryContractInvalid(
                "Capability ownership may not silently default or be overridden."
            )
        if command.relation_edges:
            raise SkillRegistryContractInvalid(
                "The governed empty registry authorizes no skill dependency relations."
            )
        if command.evaluator_receipt_ids or command.active_maturity_claims:
            raise SkillRegistryContractInvalid(
                "No evaluated maturity claim exists in the synthetic empty registry."
            )

    def _verified_file(
        self,
        relative_path: str,
        expected_sha256: str,
        canonical_path: str,
        canonical_sha256: str,
    ) -> Path:
        if relative_path != canonical_path or expected_sha256 != canonical_sha256:
            raise SkillRegistryInputInvalid(
                "A governed skill-registry file pin differs from capsule authority.",
                expected_path=canonical_path,
            )
        path = (self._root / relative_path).resolve()
        try:
            path.relative_to(self._root)
            observed = sha256(path.read_bytes()).hexdigest()
        except (ValueError, OSError) as error:
            raise SkillRegistryInputInvalid(
                "A governed skill-registry file is missing, unreadable, or escapes the repository.",
                path=relative_path,
            ) from error
        if observed != expected_sha256:
            raise SkillRegistryInputInvalid(
                "A governed skill-registry file hash does not match.",
                path=relative_path,
                expected_sha256=expected_sha256,
                observed_sha256=observed,
            )
        return path

    def _authorize_code(self, actor_id: str, run_id: str) -> None:
        actor = self._authority.authorize(
            actor_id=actor_id,
            action=Action.TRANSITION_RUN,
            resource_id=run_id,
            now=self._clock.now(),
        )
        if actor.kind is not ActorKind.CODE:
            raise HarnessIRAuthorityRejected(
                "Only deterministic Builder code may compile the synthetic skill snapshot."
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
    ) -> SkillRegistryConsumptionReceipt | None:
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if (
            record.payload_hash != payload_hash
            or not isinstance(record.result, SkillRegistryConsumptionReceipt)
        ):
            raise IdempotencyPayloadMismatch(
                "Command identity was reused with a different payload or result contract.",
                command_id=command_id,
            )
        return record.result

    def _emit_replay(
        self,
        command: CompileSyntheticSkillRegistryCommand,
        receipt: SkillRegistryConsumptionReceipt,
    ) -> None:
        snapshot = self._repository.get_skill_registry_snapshot(receipt.snapshot_id)
        run = self._repository.load_run(command.run_id)
        context = (
            self._repository.get_minimum_context_graph(
                snapshot.minimum_context_graph_id
            )
            if snapshot
            else None
        )
        if snapshot is None or context is None:
            raise SkillRegistryStateInvalid(
                "Replayed skill-registry receipt snapshot is unavailable."
            )
        self._emit(
            event_name="synthetic_skill_registry_replayed",
            outcome="PASS",
            command=command,
            run=run,
            context=context,
            snapshot=snapshot,
            receipt=receipt,
            replay_status="ORIGINAL_RECEIPT_RETURNED",
            failure_context={},
        )

    def _emit(
        self,
        *,
        event_name: str,
        outcome: str,
        command: CompileSyntheticSkillRegistryCommand,
        run: Run | None,
        context: MinimumCompleteContextGraph | None,
        snapshot: SyntheticSkillRegistrySnapshot | None,
        receipt: SkillRegistryConsumptionReceipt | None,
        replay_status: str,
        failure_context: dict[str, object],
    ) -> None:
        profile = run.target_profile if run else None
        self._observations.emit(Observation(
            event_name=event_name,
            run_id=command.run_id,
            story_id=self.STORY_ID,
            artifact_identity=(snapshot.snapshot_id if snapshot else "unassigned"),
            authority_identity=command.actor_id,
            version=self.CONTRACT_VERSION,
            provenance=(snapshot.snapshot_hash if snapshot else "unassigned"),
            outcome=outcome,
            failure_context=failure_context,
            correlation_id=command.correlation_id,
            causation_id=command.causation_id,
            command_id=command.command_id,
            target_id=(profile.target_id if profile else "unassigned"),
            category_id=(profile.category_id if profile else "unassigned"),
            profile_id=(profile.profile_id if profile else "unassigned"),
            stream_version=(run.stream_version if run else command.expected_version),
            source_lock_id=(context.source_lock_ref if context else "unassigned"),
            boundary_id=(context.boundary_ref if context else "unassigned"),
            model_id=(context.model_ref if context else "unassigned"),
            harness_ir_id=(context.ir_id if context else "unassigned"),
            harness_ir_hash=(context.ir_hash if context else "unassigned"),
            artifact_set_id=(context.artifact_set_id if context else "unassigned"),
            constitutional_report_id=(
                context.constitutional_report_id if context else "unassigned"
            ),
            constitutional_report_hash=(
                context.constitutional_report_hash if context else "unassigned"
            ),
            capability_graph_id=(
                context.capability_graph_id if context else "unassigned"
            ),
            capability_graph_hash=(
                context.capability_graph_hash if context else "unassigned"
            ),
            module_graph_id=(context.module_graph_id if context else "unassigned"),
            module_graph_hash=(context.module_graph_hash if context else "unassigned"),
            phase_graph_id=(context.phase_graph_id if context else "unassigned"),
            phase_graph_hash=(context.phase_graph_hash if context else "unassigned"),
            handoff_graph_id=(context.handoff_graph_id if context else "unassigned"),
            handoff_graph_hash=(context.handoff_graph_hash if context else "unassigned"),
            minimum_context_graph_id=(context.graph_id if context else "unassigned"),
            minimum_context_graph_hash=(context.graph_hash if context else "unassigned"),
            skill_snapshot_id=(snapshot.snapshot_id if snapshot else "unassigned"),
            skill_snapshot_hash=(snapshot.snapshot_hash if snapshot else "unassigned"),
            skill_registry_id=(snapshot.registry_id if snapshot else REGISTRY_ID),
            skill_registry_version=(snapshot.registry_version if snapshot else REGISTRY_VERSION),
            skill_registry_hash=(
                snapshot.registry_hash if snapshot else f"sha256:{REGISTRY_FIXTURE_SHA256}"
            ),
            skill_policy_id=(snapshot.policy_id if snapshot else REGISTRY_POLICY_ID),
            skill_policy_hash=(
                snapshot.policy_hash if snapshot else f"sha256:{REGISTRY_POLICY_SHA256}"
            ),
            skill_schema_hash=(
                snapshot.schema_hash if snapshot else f"sha256:{REGISTRY_SCHEMA_SHA256}"
            ),
            skill_validation_receipt_id=(
                snapshot.validation_receipt_id
                if snapshot else REGISTRY_VALIDATION_RECEIPT_ID
            ),
            skill_validation_receipt_hash=(
                snapshot.validation_receipt_hash
                if snapshot else f"sha256:{REGISTRY_VALIDATION_RECEIPT_SHA256}"
            ),
            skill_consumption_receipt_id=(
                receipt.receipt_id if receipt else "unassigned"
            ),
            skill_consumption_receipt_hash=(
                receipt.receipt_hash if receipt else "unassigned"
            ),
            skill_capability_count=(
                len(snapshot.capability_classifications) if snapshot else 0
            ),
            registered_skill_count=(snapshot.registry_skill_count if snapshot else 0),
            required_external_skill_count=(
                snapshot.required_external_skill_count if snapshot else 0
            ),
            skill_adaptation_count=(
                len(snapshot.taxonomy.harness_local_adaptations) if snapshot else 0
            ),
            experimental_capability_count=(
                len(snapshot.taxonomy.experimental_capabilities) if snapshot else 0
            ),
            skill_replay_status=replay_status,
        ))


@dataclass(frozen=True, slots=True)
class RunSkillNecessityTestCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    snapshot_id: str
    snapshot_hash: str
    necessity_input_path: str = SKILL_NECESSITY_INPUT_PATH
    necessity_input_sha256: str = SKILL_NECESSITY_INPUT_SHA256
    requested_operation: str = "evaluate_skill_necessity"
    capability_evidence_overrides: tuple[tuple[str, str, str], ...] = ()
    declared_skill_ids: tuple[str, ...] = ()
    requested_skill_artifacts: tuple[str, ...] = ()
    human_authority_receipt_id: str | None = None


class SyntheticSkillNecessityCommandService:
    STORY_ID = "ST-05.02"
    CONTRACT_VERSION = (
        f"{SKILL_NECESSITY_DECISION_SCHEMA_ID}@"
        f"{SKILL_NECESSITY_DECISION_SCHEMA_VERSION}"
    )

    def __init__(
        self,
        *,
        root: Path,
        repository: SkillNecessityRepository,
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

    def evaluate(
        self, command: RunSkillNecessityTestCommand
    ) -> SkillNecessityReceipt:
        run: Run | None = None
        context: MinimumCompleteContextGraph | None = None
        snapshot: SyntheticSkillRegistrySnapshot | None = None
        decision: SkillNecessityDecision | None = None
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
            snapshot, context = self._load_active_inputs(run, command)
            value = self._load_and_validate_input(command)
            self._validate_override_evidence(command)
            evidence = self._compile_capability_evidence(
                snapshot=snapshot,
                context=context,
                value=value,
            )
            decision = SkillNecessityDecision.create(
                snapshot=snapshot,
                context=context,
                authority_identity=command.actor_id,
                capability_evidence=evidence,
            )
            event_id = self._ids.new_id("event")
            final_run, event = run.attach_skill_necessity_decision(
                decision_ref=decision.decision_id,
                decision_hash=decision.decision_hash,
                snapshot_ref=snapshot.snapshot_id,
                snapshot_hash=snapshot.snapshot_hash,
                capability_count=len(decision.capability_evidence),
                external_skills_required_count=decision.external_skills_required_count,
                adaptations_required_count=decision.adaptations_required_count,
                experiments_required_count=decision.experiments_required_count,
                jit_capsules_required_count=decision.jit_capsules_required_count,
                outcome=decision.outcome,
                event_id=event_id,
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = SkillNecessityReceipt.create(
                command_id=command.command_id,
                decision=decision,
                authority_identity=command.actor_id,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            self._repository.commit_skill_necessity(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                decision=decision,
                receipt=receipt,
            )
            for event_name in (
                "synthetic_skill_necessity_started",
                "synthetic_skill_alternatives_assessed",
                "synthetic_no_skill_decision_committed",
            ):
                self._emit(
                    event_name=event_name,
                    outcome="PASS",
                    command=command,
                    run=final_run,
                    context=context,
                    snapshot=snapshot,
                    decision=decision,
                    receipt=receipt,
                    replay_status="NEW_COMMIT",
                    failure_context={},
                )
            return receipt
        except Exception as error:
            self._emit(
                event_name="synthetic_skill_necessity_rejected",
                outcome="FAIL",
                command=command,
                run=run,
                context=context,
                snapshot=snapshot,
                decision=decision,
                receipt=None,
                replay_status="NOT_COMMITTED",
                failure_context={
                    "code": str(getattr(error, "code", type(error).__name__)),
                    "message": str(error),
                    **dict(getattr(error, "context", {})),
                },
            )
            raise

    def get_active(self, run_id: str) -> SkillNecessityDecision:
        run = self._repository.load_run(run_id)
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.skill_necessity_ref
            or run.skill_necessity_invalidation_ref is not None
            or self._repository.is_skill_necessity_invalidated(run.skill_necessity_ref)
        ):
            raise SkillNecessityInvalidatedError(
                "No active synthetic skill necessity decision is available."
            )
        decision = self._repository.get_skill_necessity_decision(run.skill_necessity_ref)
        snapshot = self._repository.get_skill_registry_snapshot(
            run.skill_registry_snapshot_ref or ""
        )
        context = self._repository.get_minimum_context_graph(
            run.minimum_context_ref or ""
        )
        if (
            decision is None
            or snapshot is None
            or context is None
            or decision.decision_hash != run.skill_necessity_hash
        ):
            raise SkillNecessityInvalidatedError(
                "The active necessity decision is missing or altered."
            )
        decision.validate(snapshot, context)
        return decision

    def get_historical(self, decision_id: str) -> SkillNecessityDecision:
        decision = self._repository.get_skill_necessity_decision(decision_id)
        if decision is None:
            raise KeyError(decision_id)
        snapshot = self._repository.get_skill_registry_snapshot(decision.snapshot_id)
        context = self._repository.get_minimum_context_graph(
            decision.minimum_context_graph_id
        )
        if snapshot is None or context is None:
            raise KeyError(decision.snapshot_id)
        decision.validate(snapshot, context)
        return decision

    def _load_active_inputs(
        self,
        run: Run,
        command: RunSkillNecessityTestCommand,
    ) -> tuple[SyntheticSkillRegistrySnapshot, MinimumCompleteContextGraph]:
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.skill_registry_snapshot_ref
            or not run.minimum_context_ref
            or run.skill_registry_snapshot_invalidation_ref is not None
            or run.minimum_context_invalidation_ref is not None
            or run.skill_necessity_ref is not None
            or run.skill_necessity_invalidation_ref is not None
            or run.skill_registry_snapshot_ref != command.snapshot_id
            or run.skill_registry_snapshot_hash != command.snapshot_hash
            or self._repository.is_skill_registry_snapshot_invalidated(
                run.skill_registry_snapshot_ref
            )
            or self._repository.is_minimum_context_invalidated(run.minimum_context_ref)
        ):
            raise SkillNecessityInvalidatedError(
                "Necessity evaluation requires the exact active snapshot and context."
            )
        snapshot = self._repository.get_skill_registry_snapshot(
            run.skill_registry_snapshot_ref
        )
        context = self._repository.get_minimum_context_graph(run.minimum_context_ref)
        if snapshot is None or context is None:
            raise SkillNecessityEvidenceInvalid(
                "The active skill snapshot or context cannot be reproduced."
            )
        snapshot.validate(context)
        return snapshot, context

    def _load_and_validate_input(
        self, command: RunSkillNecessityTestCommand
    ) -> dict[str, object]:
        path = self._verified_file(
            command.necessity_input_path,
            command.necessity_input_sha256,
            SKILL_NECESSITY_INPUT_PATH,
            SKILL_NECESSITY_INPUT_SHA256,
        )
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise SkillNecessityEvidenceInvalid(
                "Skill necessity input is not canonical UTF-8 JSON."
            ) from error
        requirements = value.get("capability_requirements", []) if isinstance(value, dict) else []
        observed = tuple(
            sorted(
                item.get("capability_id", "")
                for item in requirements
                if isinstance(item, dict)
            )
        )
        policy = value.get("decision_policy", {}) if isinstance(value, dict) else {}
        if (
            not isinstance(value, dict)
            or value.get("schema_version") != SKILL_NECESSITY_INPUT_SCHEMA
            or value.get("scope") != SKILL_NECESSITY_SCOPE
            or value.get("source_contract")
            != f"{SKILL_REGISTRY_SNAPSHOT_SCHEMA_ID}@{SKILL_REGISTRY_SNAPSHOT_SCHEMA_VERSION}"
            or value.get("required_snapshot_state", {}).get("registry_ref") != REGISTRY_REF
            or value.get("required_snapshot_state", {}).get("registered_skill_count") != 0
            or value.get("required_snapshot_state", {}).get("required_external_skill_count") != 0
            or value.get("required_snapshot_state", {}).get("external_skills_required") is not False
            or value.get("required_snapshot_state", {}).get("dynamic_skill_discovery_allowed") is not False
            or observed != CAPABILITY_IDS
            or len(requirements) != len(CAPABILITY_IDS)
            or any(
                item.get("target_failure_observed") is not False
                or item.get("current_owner_kind") != "builder_code"
                or item.get("selected_alternative") != "deterministic_code"
                or item.get("adequacy") != "COMPLETE"
                for item in requirements
            )
            or tuple(value.get("governed_alternative_order", ()))
            != GOVERNED_ALTERNATIVE_ORDER
            or policy != {
                "new_skill_requires_target_failure": True,
                "new_skill_requires_all_prior_alternatives_inadequate": True,
                "new_skill_requires_human_authority": True,
                "material_adaptation_requires_typed_skill_design_brief": True,
                "new_skill_requires_typed_skill_design_brief": True,
                "no_gap_brief_disposition": "NOT_APPLICABLE_NO_GAP",
                "implicit_ownership": "FAIL_CLOSED",
                "hidden_workflow_in_skill": "FAIL_CLOSED",
                "same_version_mutation": "FAIL_CLOSED",
            }
            or value.get("expected_decision") != "NO_NEW_SKILL_REQUIRED"
            or value.get("expected_selected_owner") != "deterministic_builder_code"
            or any(value.get(name) != 0 for name in (
                "expected_new_skill_count",
                "expected_adaptation_count",
                "expected_adapter_count",
                "expected_skill_design_brief_count",
            ))
            or value.get("production_eligible") is not False
            or value.get("certified") is not False
        ):
            raise SkillNecessityEvidenceInvalid(
                "Skill necessity input is incomplete, altered, or assumes its outcome."
            )
        return value

    def _validate_override_evidence(
        self, command: RunSkillNecessityTestCommand
    ) -> None:
        seen: set[tuple[str, str]] = set()
        for capability_id, field, value in command.capability_evidence_overrides:
            key = (capability_id, field)
            if capability_id not in CAPABILITY_IDS or key in seen:
                raise SkillNecessityEvidenceInvalid(
                    "Capability override evidence is unknown or conflicting.",
                    capability_id=capability_id,
                    field=field,
                )
            seen.add(key)
            if field == "target_failure_observed" and value.lower() == "true":
                raise MissingRequiredSkill(
                    "A demonstrated target failure cannot be hidden by the empty registry.",
                    capability_id=capability_id,
                )
            if field == "current_owner_kind" and value != "builder_code":
                raise SkillNecessityEvidenceInvalid(
                    "Capability ownership evidence conflicts with the active ownership graph.",
                    capability_id=capability_id,
                )
            if field == "implementation_evidence" and value in {"", "missing", "unverifiable"}:
                raise SkillNecessityEvidenceInvalid(
                    "Deterministic Builder-code evidence is missing or unverifiable.",
                    capability_id=capability_id,
                )
            if field == "selected_alternative" and value in {
                "harness_local_adaptation",
                "new_canonical_skill",
            }:
                raise SkillNecessityAuthorityInvalid(
                    "Synthetic no-gap mode cannot authorize skill or adaptation work.",
                    capability_id=capability_id,
                )
            if field == "registered_skill_ref":
                raise UndeclaredSkillRequirement(
                    "The empty registry contains no declared reusable skill.",
                    capability_id=capability_id,
                    skill_ref=value,
                )
            raise SkillNecessityEvidenceInvalid(
                "Capability evidence differs from the governed necessity input.",
                capability_id=capability_id,
                field=field,
            )

    def _compile_capability_evidence(
        self,
        *,
        snapshot: SyntheticSkillRegistrySnapshot,
        context: MinimumCompleteContextGraph,
        value: dict[str, object],
    ) -> tuple[CapabilityGapEvidence, ...]:
        capability_graph = self._repository.get_capability_ownership_graph(
            snapshot.capability_graph_id
        )
        module_graph = self._repository.get_responsibility_module_graph(
            snapshot.module_graph_id
        )
        phase_graph = self._repository.get_phase_graph(snapshot.phase_graph_id)
        if capability_graph is None or module_graph is None or phase_graph is None:
            raise SkillNecessityEvidenceInvalid(
                "Capability, module, or phase evidence is unavailable."
            )
        capability_graph.validate()
        module_graph.validate(capability_graph)
        phase_graph.validate(module_graph)
        if (
            capability_graph.graph_hash != snapshot.capability_graph_hash
            or module_graph.graph_hash != snapshot.module_graph_hash
            or phase_graph.graph_hash != snapshot.phase_graph_hash
            or capability_graph.run_id != snapshot.run_id
            or module_graph.run_id != snapshot.run_id
            or phase_graph.run_id != snapshot.run_id
        ):
            raise SkillNecessityEvidenceInvalid(
                "Capability necessity lineage differs from the active snapshot."
            )
        requirements = {
            item["capability_id"]: item
            for item in value["capability_requirements"]
            if isinstance(item, dict)
        }
        declaration_by_id = {
            item.capability_id: item for item in snapshot.capability_classifications
        }
        module_selection = {
            "deterministic_contract_validation": "governed_contract_module",
            "governed_run_lifecycle": "atomic_boundary_module",
            "governed_task_acceptance": "atomic_boundary_module",
            "immutable_receipt_emission": "governed_contract_module",
            "synthetic_target_profile_binding": "atomic_boundary_module",
        }
        result: list[CapabilityGapEvidence] = []
        for capability_id in CAPABILITY_IDS:
            requirement = requirements.get(capability_id)
            declaration = declaration_by_id.get(capability_id)
            modules = tuple(
                item for item in module_graph.modules
                if item.module_id == module_selection[capability_id]
            )
            if requirement is None or declaration is None or len(modules) != 1:
                raise SkillNecessityEvidenceInvalid(
                    "A capability lacks exact requirement, ownership, or module evidence.",
                    capability_id=capability_id,
                )
            module = modules[0]
            phases = tuple(
                item for item in phase_graph.phases if module.module_id in item.module_refs
            )
            if len(phases) != 1:
                raise SkillNecessityEvidenceInvalid(
                    "A capability module lacks one exact owning phase.",
                    capability_id=capability_id,
                )
            phase = phases[0]
            ownership_bytes = json.dumps(
                declaration.canonical_dict(),
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            ).encode("utf-8")
            ownership_hash = f"sha256:{sha256(ownership_bytes).hexdigest()}"
            common_refs = tuple(sorted(set((
                capability_graph.graph_id,
                capability_graph.graph_hash,
                module_graph.graph_id,
                module_graph.graph_hash,
                phase_graph.graph_id,
                phase_graph.graph_hash,
                snapshot.snapshot_id,
                snapshot.snapshot_hash,
                *declaration.evidence_refs,
            ))))
            assessments = tuple(
                GovernedAlternativeAssessment(
                    alternative_id=alternative,
                    order=index + 1,
                    adequacy=(
                        "COMPLETE"
                        if alternative == "deterministic_code"
                        else "NOT_REQUIRED_AFTER_ADEQUATE_PRIOR_ALTERNATIVE"
                    ),
                    selected=alternative == "deterministic_code",
                    evidence_refs=common_refs,
                )
                for index, alternative in enumerate(GOVERNED_ALTERNATIVE_ORDER)
            )
            evidence = CapabilityGapEvidence(
                capability_id=capability_id,
                capability_version_or_hash=ownership_hash,
                owning_module_id=module.module_id,
                owning_phase_id=phase.phase_id,
                required_behavior=module.responsibility,
                implementation_evidence_refs=tuple(sorted(set((
                    declaration.owner_id,
                    module.module_id,
                    phase.phase_id,
                    *declaration.evidence_refs,
                )))),
                reliability_evidence_refs=tuple(sorted(set((
                    *module.invariants,
                    *module.test_seam.contract_tests,
                    *module.test_seam.observable_outputs,
                )))),
                authority_boundary=declaration.authority_boundary,
                context_requirement_refs=declaration.context_manifest_refs,
                failure_responsibility=module.failure_owner,
                target_failure_observed=bool(requirement["target_failure_observed"]),
                current_owner_kind=str(requirement["current_owner_kind"]),
                alternative_assessments=assessments,
                verdict=SkillNecessityVerdict.BUILDER_OWNED_CODE,
                justification=(
                    "No target failure is observed; exact deterministic Builder-code "
                    "ownership, reliability, module, phase, and context evidence is active."
                ),
                policy_ref=(
                    f"{snapshot.policy_id}@{REGISTRY_POLICY_VERSION}:"
                    f"{snapshot.policy_hash}"
                ),
                validation_status="PASS",
            )
            evidence.validate(registry_skill_ids=())
            result.append(evidence)
        return tuple(result)

    def _validate_command(self, command: RunSkillNecessityTestCommand) -> None:
        if command.requested_operation in SKILL_NECESSITY_PROHIBITED_OPERATIONS:
            raise SkillNecessityAuthorityInvalid(
                "The requested operation is prohibited by ST-05.02 authority."
            )
        if (
            not all(value.strip() for value in (
                command.command_id,
                command.run_id,
                command.actor_id,
                command.correlation_id,
                command.causation_id,
                command.snapshot_id,
                command.snapshot_hash,
            ))
            or command.expected_version < 1
            or command.requested_operation not in SKILL_NECESSITY_ALLOWED_OPERATIONS
        ):
            raise SkillNecessityEvidenceInvalid(
                "Skill necessity command identity or operation is invalid."
            )
        if command.declared_skill_ids:
            raise UndeclaredSkillRequirement(
                "No skill may be silently introduced into the empty registry.",
                skill_ids=command.declared_skill_ids,
            )
        if command.requested_skill_artifacts or command.human_authority_receipt_id:
            raise SkillNecessityAuthorityInvalid(
                "The no-gap Story cannot design, adapt, package, or authorize a skill."
            )

    def _verified_file(
        self,
        relative_path: str,
        expected_sha256: str,
        canonical_path: str,
        canonical_sha256: str,
    ) -> Path:
        if relative_path != canonical_path or expected_sha256 != canonical_sha256:
            raise SkillNecessityEvidenceInvalid(
                "The governed necessity input pin differs from capsule authority."
            )
        path = (self._root / relative_path).resolve()
        try:
            path.relative_to(self._root)
            observed = sha256(path.read_bytes()).hexdigest()
        except (ValueError, OSError) as error:
            raise SkillNecessityEvidenceInvalid(
                "The governed necessity input is missing or escapes the repository."
            ) from error
        if observed != expected_sha256:
            raise SkillNecessityEvidenceInvalid(
                "The governed necessity input hash does not match.",
                expected_sha256=expected_sha256,
                observed_sha256=observed,
            )
        return path

    def _authorize_code(self, actor_id: str, run_id: str) -> None:
        actor = self._authority.authorize(
            actor_id=actor_id,
            action=Action.TRANSITION_RUN,
            resource_id=run_id,
            now=self._clock.now(),
        )
        if actor.kind is not ActorKind.CODE:
            raise HarnessIRAuthorityRejected(
                "Only deterministic Builder code may emit the necessity decision."
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
    ) -> SkillNecessityReceipt | None:
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if (
            record.payload_hash != payload_hash
            or not isinstance(record.result, SkillNecessityReceipt)
        ):
            raise IdempotencyPayloadMismatch(
                "Command identity was reused with a different payload or result contract.",
                command_id=command_id,
            )
        return record.result

    def _emit_replay(
        self,
        command: RunSkillNecessityTestCommand,
        receipt: SkillNecessityReceipt,
    ) -> None:
        decision = self._repository.get_skill_necessity_decision(receipt.decision_id)
        snapshot = self._repository.get_skill_registry_snapshot(receipt.snapshot_id)
        run = self._repository.load_run(command.run_id)
        context = (
            self._repository.get_minimum_context_graph(
                decision.minimum_context_graph_id
            )
            if decision
            else None
        )
        if decision is None or snapshot is None or context is None:
            raise SkillNecessityEvidenceInvalid(
                "Replayed necessity decision lineage is unavailable."
            )
        self._emit(
            event_name="synthetic_skill_necessity_replayed",
            outcome="PASS",
            command=command,
            run=run,
            context=context,
            snapshot=snapshot,
            decision=decision,
            receipt=receipt,
            replay_status="ORIGINAL_RECEIPT_RETURNED",
            failure_context={},
        )

    def _emit(
        self,
        *,
        event_name: str,
        outcome: str,
        command: RunSkillNecessityTestCommand,
        run: Run | None,
        context: MinimumCompleteContextGraph | None,
        snapshot: SyntheticSkillRegistrySnapshot | None,
        decision: SkillNecessityDecision | None,
        receipt: SkillNecessityReceipt | None,
        replay_status: str,
        failure_context: dict[str, object],
    ) -> None:
        profile = run.target_profile if run else None
        self._observations.emit(Observation(
            event_name=event_name,
            run_id=command.run_id,
            story_id=self.STORY_ID,
            artifact_identity=(decision.decision_id if decision else "unassigned"),
            authority_identity=command.actor_id,
            version=self.CONTRACT_VERSION,
            provenance=(decision.decision_hash if decision else "unassigned"),
            outcome=outcome,
            failure_context=failure_context,
            correlation_id=command.correlation_id,
            causation_id=command.causation_id,
            command_id=command.command_id,
            target_id=(profile.target_id if profile else "unassigned"),
            category_id=(profile.category_id if profile else "unassigned"),
            profile_id=(profile.profile_id if profile else "unassigned"),
            stream_version=(run.stream_version if run else command.expected_version),
            source_lock_id=(context.source_lock_ref if context else "unassigned"),
            boundary_id=(context.boundary_ref if context else "unassigned"),
            model_id=(context.model_ref if context else "unassigned"),
            harness_ir_id=(context.ir_id if context else "unassigned"),
            harness_ir_hash=(context.ir_hash if context else "unassigned"),
            artifact_set_id=(context.artifact_set_id if context else "unassigned"),
            constitutional_report_id=(
                context.constitutional_report_id if context else "unassigned"
            ),
            constitutional_report_hash=(
                context.constitutional_report_hash if context else "unassigned"
            ),
            capability_graph_id=(
                context.capability_graph_id if context else "unassigned"
            ),
            capability_graph_hash=(
                context.capability_graph_hash if context else "unassigned"
            ),
            module_graph_id=(context.module_graph_id if context else "unassigned"),
            module_graph_hash=(context.module_graph_hash if context else "unassigned"),
            phase_graph_id=(context.phase_graph_id if context else "unassigned"),
            phase_graph_hash=(context.phase_graph_hash if context else "unassigned"),
            handoff_graph_id=(context.handoff_graph_id if context else "unassigned"),
            handoff_graph_hash=(context.handoff_graph_hash if context else "unassigned"),
            minimum_context_graph_id=(context.graph_id if context else "unassigned"),
            minimum_context_graph_hash=(context.graph_hash if context else "unassigned"),
            skill_snapshot_id=(snapshot.snapshot_id if snapshot else command.snapshot_id),
            skill_snapshot_hash=(snapshot.snapshot_hash if snapshot else command.snapshot_hash),
            skill_registry_id=(snapshot.registry_id if snapshot else REGISTRY_ID),
            skill_registry_version=(snapshot.registry_version if snapshot else REGISTRY_VERSION),
            skill_registry_hash=(snapshot.registry_hash if snapshot else "unassigned"),
            skill_policy_id=(snapshot.policy_id if snapshot else REGISTRY_POLICY_ID),
            skill_policy_hash=(snapshot.policy_hash if snapshot else "unassigned"),
            skill_capability_count=(len(snapshot.capability_classifications) if snapshot else 0),
            registered_skill_count=(snapshot.registry_skill_count if snapshot else 0),
            required_external_skill_count=(
                snapshot.required_external_skill_count if snapshot else 0
            ),
            skill_replay_status=replay_status,
            skill_necessity_decision_id=(
                decision.decision_id if decision else "unassigned"
            ),
            skill_necessity_decision_hash=(
                decision.decision_hash if decision else "unassigned"
            ),
            skill_necessity_receipt_id=(receipt.receipt_id if receipt else "unassigned"),
            skill_necessity_receipt_hash=(receipt.receipt_hash if receipt else "unassigned"),
            skill_necessity_outcome=(decision.outcome if decision else "unassigned"),
            skill_necessity_capability_count=(
                len(decision.capability_evidence) if decision else 0
            ),
            skill_target_failure_count=(decision.target_failure_count if decision else 0),
            skill_alternative_assessment_count=(
                decision.alternative_assessment_count if decision else 0
            ),
            skill_missing_required_count=(
                decision.missing_required_skills_count if decision else 0
            ),
            skill_adaptation_count=(
                decision.adaptations_required_count if decision else 0
            ),
            skill_experiment_count=(
                decision.experiments_required_count if decision else 0
            ),
            skill_jit_capsule_count=(
                decision.jit_capsules_required_count if decision else 0
            ),
            skill_design_brief_count=(
                decision.skill_design_brief_count if decision else 0
            ),
            skill_design_brief_disposition=(
                decision.brief_disposition.value if decision else "unassigned"
            ),
        ))


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
