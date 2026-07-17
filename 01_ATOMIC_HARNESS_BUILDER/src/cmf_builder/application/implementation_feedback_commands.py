from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping

from cmf_builder.application.authority import Action, ActorKind, AuthorityService
from cmf_builder.application.ports import (
    AmendmentProposalRepository,
    AtomicCommitFailed,
    Clock,
    CommandRecord,
    ConcurrencyConflict,
    IdempotencyPayloadMismatch,
    Observation,
    ObservationSink,
)
from cmf_builder.domain.implementation_feedback import (
    DIRECT_DEPENDENCIES,
    FEEDBACK_INPUT_PATH,
    FEEDBACK_INPUT_SHA256,
    FEEDBACK_MODE,
    FEEDBACK_OUTCOME,
    FEEDBACK_PROFILE_ID,
    OWNED_OBLIGATIONS,
    PROPOSAL_STATUS,
    AmendmentProposalReceipt,
    AuthorityAmendmentProposal,
    ImplementationFeedbackAuthorityInvalid,
    ImplementationFeedbackInputInvalid,
    ImplementationFeedbackInvalidatedError,
    ImplementationFeedbackScopeInvalid,
    ImplementationFeedbackTraceInvalid,
)
from cmf_builder.domain.implementation_plan import VerticalImplementationPlan
from cmf_builder.domain.run import LifecycleState, Run


@dataclass(frozen=True, slots=True)
class GovernImplementationFeedbackCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    feedback_input_path: str = FEEDBACK_INPUT_PATH
    feedback_input_sha256: str = FEEDBACK_INPUT_SHA256
    requested_operation: str = "govern_implementation_feedback_as_proposal"
    requested_mode: str = FEEDBACK_MODE
    requested_profile_id: str = FEEDBACK_PROFILE_ID
    requested_obligations: tuple[str, ...] = OWNED_OBLIGATIONS
    requested_dependencies: tuple[str, ...] = DIRECT_DEPENDENCIES
    requested_proposal_status: str = PROPOSAL_STATUS
    requested_apply_proposal: bool = False
    requested_ratified: bool = False
    requested_authority_mutation: bool = False
    requested_production_eligible: bool = False
    requested_certified: bool = False
    feedback_overrides: tuple[tuple[str, str], ...] = ()


class ImplementationFeedbackCommandService:
    STORY_ID = "ST-11.03"
    CONTRACT_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        root: Path,
        repository: AmendmentProposalRepository,
        authority: AuthorityService,
        clock: Clock,
        observations: ObservationSink,
    ) -> None:
        self._root = root.resolve()
        self._repository = repository
        self._authority = authority
        self._clock = clock
        self._observations = observations

    def govern(
        self, command: GovernImplementationFeedbackCommand
    ) -> AmendmentProposalReceipt:
        run: Run | None = None
        plan: VerticalImplementationPlan | None = None
        proposal: AuthorityAmendmentProposal | None = None
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
            self._authorize_code(command.actor_id, command.run_id)
            plan = self._load_active_plan(run)
            feedback_input = self._load_input(command)
            proposal = AuthorityAmendmentProposal.create(
                plan=plan,
                feedback_input=feedback_input,
                authority_identity=command.actor_id,
            )
            receipt = AmendmentProposalReceipt.create(
                command_id=command.command_id,
                proposal=proposal,
                stream_version=run.stream_version,
            )
            self._repository.commit_amendment_proposal(
                run_id=run.run_id,
                expected_version=command.expected_version,
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                proposal=proposal,
                receipt=receipt,
            )
            self._emit("implementation_feedback_ingestion_started", "PASS", command, run, plan, proposal, receipt, "NEW_COMMIT", {})
            for item in proposal.feedback_items:
                self._emit("implementation_feedback_item_governed", "PASS", command, run, plan, proposal, receipt, "NEW_COMMIT", {"feedback_id": item.feedback_id, "feedback_kind": item.feedback_kind})
            self._emit("implementation_feedback_proposal_committed", "PASS", command, run, plan, proposal, receipt, "NEW_COMMIT", {})
            return receipt
        except Exception as error:
            if not isinstance(error, AtomicCommitFailed):
                self._emit(
                    "implementation_feedback_ingestion_rejected", "FAIL", command,
                    run, plan, proposal, None, "NOT_COMMITTED",
                    {"code": str(getattr(error, "code", type(error).__name__)), "message": str(error), **dict(getattr(error, "context", {}))},
                )
            raise

    def get_active(self, run_id: str) -> AuthorityAmendmentProposal:
        run = self._repository.load_run(run_id)
        plan = self._load_active_plan(run)
        proposals = self._repository.amendment_proposals(run_id)
        if len(proposals) != 1:
            raise ImplementationFeedbackInvalidatedError("No single active amendment proposal is available.")
        proposal = proposals[0]
        if self._repository.is_amendment_proposal_invalidated(proposal.proposal_id):
            raise ImplementationFeedbackInvalidatedError("The amendment proposal parent is invalidated.")
        proposal.validate(plan)
        return proposal

    def get_historical(self, proposal_id: str) -> AuthorityAmendmentProposal:
        proposal = self._repository.get_amendment_proposal(proposal_id)
        if proposal is None:
            raise KeyError(proposal_id)
        plan = self._repository.get_implementation_plan(proposal.plan_id)
        if plan is None:
            raise ImplementationFeedbackTraceInvalid("Historical proposal parent is unavailable.")
        proposal.validate(plan)
        return proposal

    def _load_active_plan(self, run: Run) -> VerticalImplementationPlan:
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or run.development_capsule_invalidation_ref is not None
        ):
            raise ImplementationFeedbackInvalidatedError("Feedback intake requires an active synthetic handoff chain.")
        plans = self._repository.implementation_plans(run.run_id)
        receipts = self._repository.implementation_plan_receipts(run.run_id)
        if len(plans) != 1 or len(receipts) != 1:
            raise ImplementationFeedbackTraceInvalid("Feedback intake requires one exact implementation plan and receipt.")
        plan = plans[0]
        capsule = self._repository.get_development_capsule(plan.capsule_id)
        if capsule is None or self._repository.is_implementation_plan_invalidated(plan.plan_id):
            raise ImplementationFeedbackInvalidatedError("The implementation plan is stale or invalidated.")
        plan.validate(capsule)
        receipts[0].validate(plan)
        return plan

    def _load_input(self, command: GovernImplementationFeedbackCommand) -> Mapping[str, object]:
        if command.feedback_input_path != FEEDBACK_INPUT_PATH or command.feedback_input_sha256 != FEEDBACK_INPUT_SHA256:
            raise ImplementationFeedbackInputInvalid("Feedback input pin differs from capsule authority.")
        path = (self._root / command.feedback_input_path).resolve()
        try:
            path.relative_to(self._root)
        except ValueError as error:
            raise ImplementationFeedbackScopeInvalid("Feedback input must remain inside the Builder repository.") from error
        try:
            raw = path.read_bytes()
            observed = sha256(raw).hexdigest()
            value = json.loads(raw.decode("utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ImplementationFeedbackInputInvalid("Feedback input is missing, unreadable or invalid.") from error
        if observed != FEEDBACK_INPUT_SHA256 or not isinstance(value, Mapping):
            raise ImplementationFeedbackInputInvalid("Feedback input bytes do not match the immutable pin.")
        self._verify_evidence(value)
        return value

    def _verify_evidence(self, value: Mapping[str, object]) -> None:
        items = value.get("feedback_items")
        if not isinstance(items, list):
            raise ImplementationFeedbackInputInvalid("Feedback items are missing.")
        for item in items:
            if not isinstance(item, Mapping):
                raise ImplementationFeedbackInputInvalid("Feedback item is not a mapping.")
            refs, hashes = item.get("evidence_refs"), item.get("evidence_hashes")
            if not isinstance(refs, list) or not isinstance(hashes, list) or len(refs) != len(hashes):
                raise ImplementationFeedbackInputInvalid("Feedback evidence references are incomplete.")
            for relative, expected in zip(refs, hashes, strict=True):
                if not isinstance(relative, str) or not isinstance(expected, str):
                    raise ImplementationFeedbackInputInvalid("Feedback evidence identity is invalid.")
                evidence_path = (self._root / relative).resolve()
                try:
                    evidence_path.relative_to(self._root)
                except ValueError as error:
                    raise ImplementationFeedbackScopeInvalid("Feedback evidence escaped the Builder repository.") from error
                observed = sha256(evidence_path.read_bytes()).hexdigest()
                if expected != f"sha256:{observed}":
                    raise ImplementationFeedbackTraceInvalid("Hash-pinned feedback evidence has drifted.", path=relative, expected=expected, observed=f"sha256:{observed}")

    def _validate_command(self, command: GovernImplementationFeedbackCommand) -> None:
        if (
            not all(value.strip() for value in (command.command_id, command.run_id, command.actor_id, command.correlation_id, command.causation_id))
            or command.expected_version < 1
            or command.requested_operation != "govern_implementation_feedback_as_proposal"
            or command.requested_mode != FEEDBACK_MODE
            or command.requested_profile_id != FEEDBACK_PROFILE_ID
            or command.requested_obligations != OWNED_OBLIGATIONS
            or command.requested_dependencies != DIRECT_DEPENDENCIES
            or command.requested_proposal_status != PROPOSAL_STATUS
        ):
            raise ImplementationFeedbackInputInvalid("Feedback command identity or contract is invalid.")
        if command.requested_apply_proposal or command.requested_ratified or command.requested_authority_mutation:
            raise ImplementationFeedbackAuthorityInvalid("ST-11.03 may propose but cannot apply, ratify or mutate authority.")
        if command.requested_production_eligible or command.requested_certified:
            raise ImplementationFeedbackAuthorityInvalid("Synthetic feedback cannot grant production or certification.")
        if command.feedback_overrides:
            raise ImplementationFeedbackTraceInvalid("Command-supplied feedback overrides are not authoritative.")

    def _authorize_code(self, actor_id: str, run_id: str) -> None:
        actor = self._authority.authorize(actor_id=actor_id, action=Action.TRANSITION_RUN, resource_id=run_id, now=self._clock.now())
        if actor.kind is not ActorKind.CODE:
            raise ImplementationFeedbackAuthorityInvalid("Only deterministic Builder code may compile the proposal.")

    def _duplicate(self, command_id: str, payload_hash: str) -> AmendmentProposalReceipt | None:
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if record.payload_hash != payload_hash or not isinstance(record.result, AmendmentProposalReceipt):
            raise IdempotencyPayloadMismatch("Command identity was reused with a different payload or result contract.", command_id=command_id)
        return record.result

    def _emit_replay(self, command: GovernImplementationFeedbackCommand, receipt: AmendmentProposalReceipt) -> None:
        run = self._repository.load_run(command.run_id)
        proposal = self._repository.get_amendment_proposal(receipt.proposal_id)
        plan = self._repository.get_implementation_plan(receipt.plan_id)
        if proposal is None or plan is None:
            raise ImplementationFeedbackTraceInvalid("Replayed proposal evidence is unavailable.")
        self._emit("implementation_feedback_ingestion_replayed", "PASS", command, run, plan, proposal, receipt, "ORIGINAL_RECEIPT_RETURNED", {})

    def _emit(
        self, event_name: str, outcome: str, command: GovernImplementationFeedbackCommand,
        run: Run | None, plan: VerticalImplementationPlan | None,
        proposal: AuthorityAmendmentProposal | None, receipt: AmendmentProposalReceipt | None,
        replay_status: str, failure_context: dict[str, object],
    ) -> None:
        context = dict(failure_context)
        context.update({
            "proposal_id": proposal.proposal_id if proposal else "unassigned",
            "proposal_hash": proposal.proposal_hash if proposal else "unassigned",
            "proposal_receipt_id": receipt.receipt_id if receipt else "unassigned",
            "plan_id": plan.plan_id if plan else "unassigned",
            "proposal_status": PROPOSAL_STATUS,
            "authority_mutated": False,
            "replay_status": replay_status,
        })
        self._observations.emit(Observation(
            event_name=event_name, run_id=command.run_id, story_id=self.STORY_ID,
            artifact_identity=proposal.proposal_id if proposal else "unassigned",
            authority_identity=command.actor_id, version=self.CONTRACT_VERSION,
            provenance=proposal.proposal_hash if proposal else plan.plan_hash if plan else "unassigned",
            outcome=outcome, failure_context=context,
            correlation_id=command.correlation_id, causation_id=command.causation_id,
            command_id=command.command_id,
            target_id=run.target_profile.target_id if run else FEEDBACK_PROFILE_ID,
            category_id=run.target_profile.category_id if run else "none",
            profile_id=run.target_profile.profile_id if run else FEEDBACK_PROFILE_ID,
            stream_version=run.stream_version if run else command.expected_version,
            development_capsule_id=plan.capsule_id if plan else "unassigned",
            development_capsule_hash=plan.capsule_hash if plan else "unassigned",
        ))


def _command_hash(command: GovernImplementationFeedbackCommand) -> str:
    value = json.dumps(asdict(command), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return f"sha256:{sha256(value).hexdigest()}"
