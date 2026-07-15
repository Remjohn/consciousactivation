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
    MinimumContextRepository,
    Observation,
    ObservationSink,
)
from cmf_builder.domain.context_manifest import (
    GOVERNED_PRIORITY_ORDER,
    MANIFEST_CATEGORIES,
    MINIMUM_CONTEXT_GRAPH_SCHEMA_ID,
    MINIMUM_CONTEXT_GRAPH_SCHEMA_VERSION,
    MINIMUM_CONTEXT_INPUT_PATH,
    MINIMUM_CONTEXT_INPUT_SCHEMA,
    MINIMUM_CONTEXT_INPUT_SHA256,
    MINIMUM_CONTEXT_SCOPE,
    PHASE_HANDOFF_CONTRACT,
    BudgetLimit,
    ContextAuthorityInvalid,
    ContextBudgetPolicy,
    ContextCompilationReceipt,
    ContextContractInvalid,
    ContextDisposition,
    ContextInputInvalid,
    ContextInvalidatedError,
    ContextLineageInvalid,
    ContextStateInvalid,
    MinimumCompleteContextGraph,
    PhaseContextManifest,
    ReferenceDeclaration,
    ResolvedContextItem,
)
from cmf_builder.domain.handoff import (
    InternalHandoff,
    InternalHandoffDecision,
    InternalHandoffDecisionAction,
    PhaseHandoffGraph,
)
from cmf_builder.domain.harness_ir import HarnessIRAuthorityRejected
from cmf_builder.domain.phase_graph import PhaseGraph
from cmf_builder.domain.run import LifecycleState, Run


class ContextCommandRejected(Exception):
    code = "ContextCommandRejected"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


@dataclass(frozen=True, slots=True)
class CompileMinimumContextCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    context_input_path: str = MINIMUM_CONTEXT_INPUT_PATH
    context_input_sha256: str = MINIMUM_CONTEXT_INPUT_SHA256


class MinimumContextCommandService:
    STORY_ID = "ST-04.05"
    CONTRACT_VERSION = (
        f"{MINIMUM_CONTEXT_GRAPH_SCHEMA_ID}@{MINIMUM_CONTEXT_GRAPH_SCHEMA_VERSION}"
    )

    def __init__(
        self,
        *,
        root: Path,
        repository: MinimumContextRepository,
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

    def compile(self, command: CompileMinimumContextCommand) -> ContextCompilationReceipt:
        run: Run | None = None
        handoff_graph: PhaseHandoffGraph | None = None
        phase_graph: PhaseGraph | None = None
        handoff: InternalHandoff | None = None
        decision: InternalHandoffDecision | None = None
        graph: MinimumCompleteContextGraph | None = None
        try:
            payload_hash = _command_hash(command)
            duplicate = self._duplicate(command.command_id, payload_hash)
            if duplicate is not None:
                self._emit_replay(command, duplicate)
                return duplicate
            self._validate_common(command)
            if (
                command.context_input_path != MINIMUM_CONTEXT_INPUT_PATH
                or command.context_input_sha256 != MINIMUM_CONTEXT_INPUT_SHA256
            ):
                raise ContextInputInvalid("The governed minimum-context input pin is invalid.")
            run = self._repository.load_run(command.run_id)
            self._require_version(command.expected_version, run)
            self._authorize_code(command.actor_id, command.run_id)
            handoff_graph, phase_graph, handoff, decision = self._load_active_parent(run)
            references, policies = self._load_input(command, handoff_graph, phase_graph)
            resolved = self._resolve_references(
                handoff_graph=handoff_graph,
                phase_graph=phase_graph,
                handoff=handoff,
                references=references,
            )
            manifests = self._compile_manifests(
                phase_graph=phase_graph,
                references=references,
                policies=policies,
                resolved=resolved,
            )
            graph = MinimumCompleteContextGraph.create(
                handoff_graph=handoff_graph,
                phase_graph=phase_graph,
                handoff=handoff,
                decision=decision,
                references=references,
                policies=policies,
                manifests=manifests,
                authority_identity=command.actor_id,
            )
            event_id = self._ids.new_id("event")
            final_run, event = run.attach_minimum_context(
                graph_ref=graph.graph_id,
                graph_hash=graph.graph_hash,
                handoff_graph_ref=handoff_graph.graph_id,
                accepted_handoff_ref=handoff.handoff_id,
                acceptance_decision_ref=decision.decision_id,
                manifest_count=len(graph.manifests),
                reference_count=len(graph.references),
                event_id=event_id,
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = ContextCompilationReceipt.create(
                command_id=command.command_id,
                graph=graph,
                authority_identity=command.actor_id,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            self._repository.commit_minimum_context(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                graph=graph,
                receipt=receipt,
            )
            for event_name in (
                "ST-04.05:MinimumCompleteContextCompiled",
                "ST-04.05:ReferenceRegistryValidated",
                "ST-04.05:ContextCompletenessValidated",
                "ST-04.05:ContextMinimalityValidated",
                "ST-04.05:BudgetsAndNoTruncationValidated",
                "ST-04.05:OutcomeVerified",
            ):
                self._emit(
                    event_name=event_name,
                    outcome="PASS",
                    command=command,
                    run=final_run,
                    handoff_graph=handoff_graph,
                    phase_graph=phase_graph,
                    handoff=handoff,
                    decision=decision,
                    graph=graph,
                    receipt=receipt,
                    failure_context={},
                )
            return receipt
        except Exception as error:
            self._emit(
                event_name=(
                    "ST-04.05:RequiredContextOverflowBlocked"
                    if getattr(error, "code", "") == "ContextBudgetOverflow"
                    else "ST-04.05:OutcomeRejected"
                ),
                outcome="FAIL",
                command=command,
                run=run,
                handoff_graph=handoff_graph,
                phase_graph=phase_graph,
                handoff=handoff,
                decision=decision,
                graph=graph,
                receipt=None,
                failure_context={
                    "code": str(getattr(error, "code", type(error).__name__)),
                    "message": str(error),
                    **dict(getattr(error, "context", {})),
                },
            )
            raise

    def get_active(self, run_id: str) -> MinimumCompleteContextGraph:
        run = self._repository.load_run(run_id)
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.minimum_context_ref
            or run.minimum_context_invalidation_ref is not None
            or self._repository.is_minimum_context_invalidated(run.minimum_context_ref)
        ):
            raise ContextInvalidatedError("No active Minimum Complete Context is available.")
        graph = self._repository.get_minimum_context_graph(run.minimum_context_ref)
        if graph is None or graph.graph_hash != run.minimum_context_hash:
            raise ContextInvalidatedError("The active Minimum Complete Context is missing or altered.")
        parent_graph = self._repository.get_phase_handoff_graph(graph.handoff_graph_id)
        phase_graph = self._repository.get_phase_graph(graph.phase_graph_id)
        handoff = self._repository.get_internal_handoff(graph.accepted_handoff_id)
        decision = self._repository.get_internal_handoff_decision(graph.accepted_handoff_id)
        if parent_graph is None or phase_graph is None or handoff is None or decision is None:
            raise ContextLineageInvalid("Minimum context lineage is unavailable.")
        graph.validate(parent_graph, phase_graph, handoff, decision)
        return graph

    def get_historical(self, graph_id: str) -> MinimumCompleteContextGraph:
        graph = self._repository.get_minimum_context_graph(graph_id)
        if graph is None:
            raise KeyError(graph_id)
        parent_graph = self._repository.get_phase_handoff_graph(graph.handoff_graph_id)
        phase_graph = self._repository.get_phase_graph(graph.phase_graph_id)
        handoff = self._repository.get_internal_handoff(graph.accepted_handoff_id)
        decision = self._repository.get_internal_handoff_decision(graph.accepted_handoff_id)
        if parent_graph is None or phase_graph is None or handoff is None or decision is None:
            raise KeyError(graph.handoff_graph_id)
        graph.validate(parent_graph, phase_graph, handoff, decision)
        return graph

    def _load_active_parent(
        self, run: Run
    ) -> tuple[PhaseHandoffGraph, PhaseGraph, InternalHandoff, InternalHandoffDecision]:
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.phase_handoff_ref
            or not run.phase_graph_ref
            or run.minimum_context_ref is not None
            or run.boundary_invalidation_ref is not None
            or run.phase_graph_invalidation_ref is not None
            or run.phase_handoff_invalidation_ref is not None
            or run.minimum_context_invalidation_ref is not None
            or self._repository.is_phase_handoff_invalidated(run.phase_handoff_ref)
        ):
            raise ContextInvalidatedError(
                "Minimum context compilation requires the exact active internal handoff graph."
            )
        handoff_graph = self._repository.get_phase_handoff_graph(run.phase_handoff_ref)
        phase_graph = self._repository.get_phase_graph(run.phase_graph_ref)
        handoffs = self._repository.internal_handoffs(run.run_id)
        if handoff_graph is None or phase_graph is None or len(handoffs) != 1:
            raise ContextLineageInvalid("The internal handoff parent or its exact handoff is unavailable.")
        handoff = handoffs[0]
        decision = self._repository.get_internal_handoff_decision(handoff.handoff_id)
        receiver = next(
            (item for item in phase_graph.phases if item.phase_id == handoff.receiver_phase),
            None,
        )
        if (
            decision is None
            or receiver is None
            or decision.action is not InternalHandoffDecisionAction.ACCEPTED
            or handoff_graph.graph_hash != run.phase_handoff_hash
            or handoff.handoff_graph_id != handoff_graph.graph_id
        ):
            raise ContextStateInvalid("Only the exact accepted Builder-internal handoff may supply context.")
        handoff_graph.validate(phase_graph)
        handoff.validate(handoff_graph, phase_graph)
        decision.validate(handoff, receiver.failure_owner)
        return handoff_graph, phase_graph, handoff, decision

    def _load_input(
        self,
        command: CompileMinimumContextCommand,
        handoff_graph: PhaseHandoffGraph,
        phase_graph: PhaseGraph,
    ) -> tuple[tuple[ReferenceDeclaration, ...], tuple[ContextBudgetPolicy, ...]]:
        path = self._verified_file(command.context_input_path, command.context_input_sha256)
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ContextInputInvalid("Minimum-context input is not canonical UTF-8 JSON.") from error
        root_keys = {
            "schema_version",
            "scope",
            "source_contract",
            "target_profile_ref",
            "conversation_history_allowed",
            "silent_truncation_allowed",
            "runtime_loading_allowed",
            "priority_order",
            "references",
            "phase_policies",
            "manifest_categories",
            "production_eligible",
            "certified",
        }
        if (
            not isinstance(value, dict)
            or set(value) != root_keys
            or value["schema_version"] != MINIMUM_CONTEXT_INPUT_SCHEMA
            or value["scope"] != MINIMUM_CONTEXT_SCOPE
            or value["source_contract"] != PHASE_HANDOFF_CONTRACT
            or value["target_profile_ref"] != handoff_graph.target_profile_ref
            or value["conversation_history_allowed"] is not False
            or value["silent_truncation_allowed"] is not False
            or value["runtime_loading_allowed"] is not False
            or value["priority_order"] != list(GOVERNED_PRIORITY_ORDER)
            or value["manifest_categories"] != list(MANIFEST_CATEGORIES)
            or value["production_eligible"] is not False
            or value["certified"] is not False
            or not isinstance(value["references"], list)
            or not isinstance(value["phase_policies"], list)
        ):
            raise ContextInputInvalid("Minimum-context input root contract is incomplete or broadened.")
        references = tuple(
            sorted(
                (self._parse_reference(item) for item in value["references"]),
                key=lambda item: item.reference_id,
            )
        )
        policies = tuple(
            sorted(
                (self._parse_policy(item) for item in value["phase_policies"]),
                key=lambda item: item.phase_ref,
            )
        )
        reference_ids = tuple(item.reference_id for item in references)
        if (
            len(references) != 6
            or len(set(reference_ids)) != 6
            or tuple(item.phase_ref for item in policies) != tuple(sorted(phase_graph.phase_ids))
            or any(set(policy.declared_references) != set(reference_ids) for policy in policies)
        ):
            raise ContextInputInvalid("Reference registry or phase-policy coverage is incomplete.")
        return references, policies

    @staticmethod
    def _parse_reference(raw: object) -> ReferenceDeclaration:
        required_keys = {
            "reference_id",
            "version",
            "integrity_source",
            "owner",
            "authority",
            "content_role",
            "loading_mode",
            "allowed_phases",
            "may_influence",
            "must_not_influence",
        }
        optional_keys = {"progressive_disclosure_pointer", "semantic_status"}
        if (
            not isinstance(raw, dict)
            or not required_keys <= set(raw)
            or set(raw) - required_keys - optional_keys
            or any(
                not isinstance(raw[key], list)
                for key in ("allowed_phases", "may_influence", "must_not_influence")
            )
        ):
            raise ContextInputInvalid("A reference declaration has unknown or missing fields.")
        return ReferenceDeclaration(
            reference_id=str(raw["reference_id"]),
            version=str(raw["version"]),
            integrity_source=str(raw["integrity_source"]),
            owner=str(raw["owner"]),
            authority=str(raw["authority"]),
            content_role=str(raw["content_role"]),
            loading_mode=str(raw["loading_mode"]),
            allowed_phases=tuple(str(item) for item in raw["allowed_phases"]),
            may_influence=tuple(str(item) for item in raw["may_influence"]),
            must_not_influence=tuple(str(item) for item in raw["must_not_influence"]),
            progressive_disclosure_pointer=(
                str(raw["progressive_disclosure_pointer"])
                if "progressive_disclosure_pointer" in raw
                else None
            ),
            semantic_status=str(raw.get("semantic_status", "APPLICABLE")),
        )

    @staticmethod
    def _parse_policy(raw: object) -> ContextBudgetPolicy:
        keys = {
            "phase_ref",
            "required_references",
            "optional_references",
            "excluded_references",
            "hard_budget",
            "soft_budget",
            "governed_token_contributions",
            "compression_permissions",
            "retrieval_policy",
            "overflow_behavior",
        }
        budget_keys = {"tokens", "latency_ms", "cost_microunits"}
        list_keys = {
            "required_references",
            "optional_references",
            "excluded_references",
            "compression_permissions",
        }
        if (
            not isinstance(raw, dict)
            or set(raw) != keys
            or any(not isinstance(raw[key], list) for key in list_keys)
            or any(
                not isinstance(raw[name], dict) or set(raw[name]) != budget_keys
                for name in ("hard_budget", "soft_budget")
            )
            or not isinstance(raw["governed_token_contributions"], dict)
            or any(not isinstance(value, int) for value in raw["governed_token_contributions"].values())
        ):
            raise ContextInputInvalid("A context budget policy has unknown, missing, or untyped fields.")
        def budget(name: str) -> BudgetLimit:
            item = raw[name]
            assert isinstance(item, dict)
            return BudgetLimit(
                tokens=int(item["tokens"]),
                latency_ms=int(item["latency_ms"]),
                cost_microunits=int(item["cost_microunits"]),
            )
        contributions = raw["governed_token_contributions"]
        assert isinstance(contributions, dict)
        return ContextBudgetPolicy(
            phase_ref=str(raw["phase_ref"]),
            required_references=tuple(str(item) for item in raw["required_references"]),
            optional_references=tuple(str(item) for item in raw["optional_references"]),
            excluded_references=tuple(str(item) for item in raw["excluded_references"]),
            hard_budget=budget("hard_budget"),
            soft_budget=budget("soft_budget"),
            governed_token_contributions=tuple(
                sorted((str(key), int(value)) for key, value in contributions.items())
            ),
            compression_permissions=tuple(str(item) for item in raw["compression_permissions"]),
            retrieval_policy=str(raw["retrieval_policy"]),
            overflow_behavior=str(raw["overflow_behavior"]),
        )

    def _resolve_references(
        self,
        *,
        handoff_graph: PhaseHandoffGraph,
        phase_graph: PhaseGraph,
        handoff: InternalHandoff,
        references: tuple[ReferenceDeclaration, ...],
    ) -> dict[str, tuple[str, str, tuple[str, ...]]]:
        source_lock = self._repository.get_source_lock(handoff_graph.source_lock_ref)
        ratification = self._repository.get_atomicity_ratification(handoff_graph.ratification_ref)
        report = self._repository.get_constitutional_validation_report(
            handoff_graph.constitutional_report_id
        )
        if source_lock is None or ratification is None or report is None:
            raise ContextLineageInvalid("A required authoritative context source is unavailable.")
        if (
            source_lock.run_id != handoff_graph.run_id
            or source_lock.lock_id != handoff_graph.source_lock_ref
            or ratification.source_lock_ref != source_lock.lock_id
            or ratification.boundary_ref != handoff_graph.boundary_ref
            or report.report_hash != handoff_graph.constitutional_report_hash
            or self._repository.is_boundary_invalidated(handoff_graph.boundary_ref)
            or self._repository.is_constitutional_validation_invalidated(report.report_id)
        ):
            raise ContextLineageInvalid("Authoritative context source identity, hash, or active state drifted.")
        artifacts = {item.field: item for item in handoff.artifacts}
        boundary = artifacts.get("frozen_atomic_boundary_ref")
        boundary_receipt = artifacts.get("boundary_validation_receipt_ref")
        if boundary is None or boundary_receipt is None:
            raise ContextLineageInvalid("Accepted handoff omitted required boundary artifacts.")
        report.validate()
        resolved = {
            "source_lock_ref_v1": (
                source_lock.lock_id,
                source_lock.aggregate_hash,
                (source_lock.lock_id, source_lock.aggregate_hash, handoff_graph.graph_id),
            ),
            "human_ratification_ref_v1": (
                ratification.ratification_id,
                _normalized_sha256(ratification.ratification_hash),
                (
                    source_lock.lock_id,
                    ratification.boundary_ref,
                    ratification.ratification_id,
                    _normalized_sha256(ratification.ratification_hash),
                ),
            ),
            "frozen_atomic_boundary_ref_v1": (
                boundary.artifact_id,
                boundary.artifact_hash,
                (*boundary.lineage_refs, handoff.handoff_id),
            ),
            "boundary_validation_receipt_ref_v1": (
                boundary_receipt.artifact_id,
                boundary_receipt.artifact_hash,
                (*boundary_receipt.lineage_refs, handoff.handoff_id),
            ),
            "constitutional_authority_pointer_v1": (
                "canonical_authority_ref",
                _normalized_sha256(report.constitution_hash),
                (report.report_id, report.report_hash, report.policy_path, report.policy_hash),
            ),
            "synthetic_spr_v1": (
                "synthetic_spr_v1",
                "sha256:3f699f67d7246530b211ab63cdce4f91a65af1940dcad51f9b102da752f439d2",
                ("repository_owned_synthetic_fixture", MINIMUM_CONTEXT_INPUT_PATH),
            ),
        }
        declared = {item.reference_id: item for item in references}
        if set(resolved) != set(declared):
            raise ContextContractInvalid("Every governed reference must resolve exactly once.")
        for reference_id, (_, artifact_hash, _) in resolved.items():
            declaration = declared[reference_id]
            expected_literal = declaration.integrity_source.removeprefix("literal_sha256:")
            if declaration.integrity_source.startswith("literal_sha256:") and artifact_hash != f"sha256:{expected_literal}":
                raise ContextLineageInvalid("Literal reference hash does not match its declaration.")
        return resolved

    def _compile_manifests(
        self,
        *,
        phase_graph: PhaseGraph,
        references: tuple[ReferenceDeclaration, ...],
        policies: tuple[ContextBudgetPolicy, ...],
        resolved: dict[str, tuple[str, str, tuple[str, ...]]],
    ) -> tuple[PhaseContextManifest, ...]:
        reference_by_id = {item.reference_id: item for item in references}
        phase_by_id = {item.phase_id: item for item in phase_graph.phases}
        manifests: list[PhaseContextManifest] = []
        for policy in policies:
            phase = phase_by_id[policy.phase_ref]
            if len(phase.module_refs) != 1:
                raise ContextLineageInvalid("Minimum context requires one exact module per phase.")
            included: list[ResolvedContextItem] = []
            excluded: list[ResolvedContextItem] = []
            for reference_id in policy.declared_references:
                declaration = reference_by_id[reference_id]
                if reference_id in policy.required_references:
                    if phase.phase_id not in declaration.allowed_phases:
                        raise ContextContractInvalid(
                            "A required context reference is not allowlisted for its consuming phase.",
                            reference_id=reference_id,
                            phase_ref=phase.phase_id,
                        )
                    disposition = ContextDisposition.REQUIRED
                    reason = f"REQUIRED_BY_GOVERNED_PHASE_POLICY:{phase.phase_id}"
                    target = included
                    tokens = policy.token_contributions[reference_id]
                elif reference_id in policy.optional_references:
                    if phase.phase_id not in declaration.allowed_phases:
                        raise ContextContractInvalid("Optional context cannot bypass its phase allowlist.")
                    disposition = ContextDisposition.OPTIONAL
                    reason = f"OPTIONAL_AND_ALLOWLISTED_BY_GOVERNED_PHASE_POLICY:{phase.phase_id}"
                    target = included
                    tokens = policy.token_contributions[reference_id]
                else:
                    disposition = (
                        ContextDisposition.NOT_APPLICABLE
                        if declaration.semantic_status == "NOT_APPLICABLE"
                        else ContextDisposition.UNAVAILABLE_NON_REQUIRED
                    )
                    reason = (
                        "NOT_APPLICABLE_TO_CATEGORY_NEUTRAL_SYNTHETIC_PROOF"
                        if disposition is ContextDisposition.NOT_APPLICABLE
                        else f"EXPLICITLY_EXCLUDED_AND_NOT_REQUIRED_FOR_PHASE:{phase.phase_id}"
                    )
                    target = excluded
                    tokens = 0
                artifact_id, artifact_hash, provenance = resolved[reference_id]
                target.append(
                    ResolvedContextItem(
                        reference_id=reference_id,
                        version=declaration.version,
                        artifact_id=artifact_id,
                        artifact_hash=artifact_hash,
                        integrity_source=declaration.integrity_source,
                        authoritative_source=declaration.owner,
                        provenance=provenance,
                        owning_responsibility=declaration.owner,
                        consuming_module=phase.module_refs[0],
                        consuming_phase=phase.phase_id,
                        inclusion_reason=reason,
                        authority_boundary=declaration.authority,
                        content_role=declaration.content_role,
                        loading_mode=declaration.loading_mode,
                        may_influence=declaration.may_influence,
                        must_not_influence=declaration.must_not_influence,
                        disposition=disposition,
                        governed_tokens=tokens,
                        pointer_target=declaration.progressive_disclosure_pointer,
                    )
                )
            manifests.append(
                PhaseContextManifest.create(
                    phase_ref=phase.phase_id,
                    module_ref=phase.module_refs[0],
                    responsibility=phase.responsibility,
                    policy=policy,
                    included=tuple(included),
                    excluded=tuple(excluded),
                )
            )
        return tuple(sorted(manifests, key=lambda item: item.phase_ref))

    def _verified_file(self, relative_path: str, expected_sha256: str) -> Path:
        path = (self._root / relative_path).resolve()
        try:
            path.relative_to(self._root)
            observed = sha256(path.read_bytes()).hexdigest()
        except (ValueError, OSError) as error:
            raise ContextInputInvalid(
                "Governed minimum-context input is unavailable or escapes the repository."
            ) from error
        if observed != expected_sha256:
            raise ContextInputInvalid(
                "Governed minimum-context input hash does not match.",
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
                "Only deterministic Builder code may compile minimum-complete context."
            )

    @staticmethod
    def _validate_common(command: CompileMinimumContextCommand) -> None:
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
        ):
            raise ContextInputInvalid("Minimum-context command identity is incomplete.")

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
    ) -> ContextCompilationReceipt | None:
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if record.payload_hash != payload_hash or not isinstance(record.result, ContextCompilationReceipt):
            raise IdempotencyPayloadMismatch(
                "Command identity was reused with a different payload or result contract.",
                command_id=command_id,
            )
        return record.result

    def _emit_replay(
        self, command: CompileMinimumContextCommand, receipt: ContextCompilationReceipt
    ) -> None:
        graph = self._repository.get_minimum_context_graph(receipt.graph_id)
        run = self._repository.load_run(command.run_id)
        if graph is None:
            raise ContextStateInvalid("Replayed context receipt graph is unavailable.")
        handoff_graph = self._repository.get_phase_handoff_graph(graph.handoff_graph_id)
        phase_graph = self._repository.get_phase_graph(graph.phase_graph_id)
        handoff = self._repository.get_internal_handoff(graph.accepted_handoff_id)
        decision = self._repository.get_internal_handoff_decision(graph.accepted_handoff_id)
        self._emit(
            event_name="ST-04.05:CommandReplayReturned",
            outcome="PASS",
            command=command,
            run=run,
            handoff_graph=handoff_graph,
            phase_graph=phase_graph,
            handoff=handoff,
            decision=decision,
            graph=graph,
            receipt=receipt,
            failure_context={},
        )

    def _emit(
        self,
        *,
        event_name: str,
        outcome: str,
        command: CompileMinimumContextCommand,
        run: Run | None,
        handoff_graph: PhaseHandoffGraph | None,
        phase_graph: PhaseGraph | None,
        handoff: InternalHandoff | None,
        decision: InternalHandoffDecision | None,
        graph: MinimumCompleteContextGraph | None,
        receipt: ContextCompilationReceipt | None,
        failure_context: dict[str, object],
    ) -> None:
        profile = run.target_profile if run else None
        manifests = graph.manifests if graph else ()
        self._observations.emit(
            Observation(
                event_name=event_name,
                run_id=command.run_id,
                story_id=self.STORY_ID,
                artifact_identity=(graph.graph_id if graph else "unassigned"),
                authority_identity=command.actor_id,
                version=self.CONTRACT_VERSION,
                provenance=(graph.graph_hash if graph else "unassigned"),
                outcome=outcome,
                failure_context=failure_context,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                command_id=command.command_id,
                target_id=(profile.target_id if profile else "unassigned"),
                category_id=(profile.category_id if profile else "unassigned"),
                profile_id=(profile.profile_id if profile else "unassigned"),
                stream_version=(run.stream_version if run else command.expected_version),
                source_lock_id=(handoff_graph.source_lock_ref if handoff_graph else "unassigned"),
                boundary_id=(handoff_graph.boundary_ref if handoff_graph else "unassigned"),
                model_id=(handoff_graph.model_ref if handoff_graph else "unassigned"),
                decision_receipt_id=(receipt.receipt_id if receipt else "unassigned"),
                decision_receipt_hash=(receipt.receipt_hash if receipt else "unassigned"),
                harness_ir_id=(handoff_graph.ir_id if handoff_graph else "unassigned"),
                harness_ir_hash=(handoff_graph.ir_hash if handoff_graph else "unassigned"),
                artifact_set_id=(handoff_graph.artifact_set_id if handoff_graph else "unassigned"),
                constitutional_report_id=(handoff_graph.constitutional_report_id if handoff_graph else "unassigned"),
                constitutional_report_hash=(handoff_graph.constitutional_report_hash if handoff_graph else "unassigned"),
                capability_graph_id=(handoff_graph.capability_graph_id if handoff_graph else "unassigned"),
                capability_graph_hash=(handoff_graph.capability_graph_hash if handoff_graph else "unassigned"),
                module_graph_id=(handoff_graph.module_graph_id if handoff_graph else "unassigned"),
                module_graph_hash=(handoff_graph.module_graph_hash if handoff_graph else "unassigned"),
                phase_graph_id=(phase_graph.graph_id if phase_graph else "unassigned"),
                phase_graph_hash=(phase_graph.graph_hash if phase_graph else "unassigned"),
                phase_count=(len(phase_graph.phases) if phase_graph else 0),
                handoff_graph_id=(handoff_graph.graph_id if handoff_graph else "unassigned"),
                handoff_graph_hash=(handoff_graph.graph_hash if handoff_graph else "unassigned"),
                internal_handoff_id=(handoff.handoff_id if handoff else "unassigned"),
                internal_handoff_hash=(handoff.handoff_hash if handoff else "unassigned"),
                handoff_status=(decision.action.value if decision else "unassigned"),
                handoff_decision_id=(decision.decision_id if decision else "unassigned"),
                handoff_decision_hash=(decision.decision_hash if decision else "unassigned"),
                minimum_context_graph_id=(graph.graph_id if graph else "unassigned"),
                minimum_context_graph_hash=(graph.graph_hash if graph else "unassigned"),
                context_compilation_receipt_id=(receipt.receipt_id if receipt else "unassigned"),
                context_compilation_receipt_hash=(receipt.receipt_hash if receipt else "unassigned"),
                context_manifest_count=len(manifests),
                context_reference_count=(len(graph.references) if graph else 0),
                context_required_count=sum(len(item.required) for item in manifests),
                context_conditional_count=sum(len(item.conditionally_required) for item in manifests),
                context_optional_count=sum(len(item.optional) for item in manifests),
                context_forbidden_count=sum(len(item.forbidden) for item in manifests),
                context_unavailable_count=sum(len(item.unavailable_non_required) for item in manifests),
                context_not_applicable_count=sum(len(item.not_applicable) for item in manifests),
                context_included_count=sum(len(item.included) for item in manifests),
                context_excluded_count=sum(len(item.excluded) for item in manifests),
                context_summarized_count=sum(len(item.summarized) for item in manifests),
                context_retrieved_count=sum(len(item.retrieved) for item in manifests),
                context_compressed_count=sum(len(item.compressed) for item in manifests),
                context_overflow_count=(1 if failure_context.get("code") == "ContextBudgetOverflow" else 0),
                context_manifest_ids=tuple(item.manifest_id for item in manifests),
                context_manifest_hashes=tuple(item.manifest_hash for item in manifests),
                context_reference_ids=(
                    tuple(item.reference_id for item in graph.references) if graph else ()
                ),
                context_loading_modes=(
                    tuple((item.reference_id, item.loading_mode) for item in graph.references)
                    if graph else ()
                ),
                context_hard_token_budgets=tuple(
                    (item.phase_ref, item.hard_budget.tokens) for item in manifests
                ),
                context_soft_token_budgets=tuple(
                    (item.phase_ref, item.soft_budget.tokens) for item in manifests
                ),
            )
        )


def _command_hash(command: object) -> str:
    payload = _canonical_value(asdict(command))
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return f"sha256:{sha256(encoded).hexdigest()}"


def _normalized_sha256(value: str) -> str:
    return value if value.startswith("sha256:") else f"sha256:{value}"


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
