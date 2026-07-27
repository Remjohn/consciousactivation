from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json

from cmf_builder.application.authority import Action, AuthorityDenied, AuthorityService
from cmf_builder.domain.conversational_feedback import (
    ConversationalFeedbackChain,
    ConversationalFeedbackError,
    ConversationalFeedbackInput,
    FeedbackTransition,
    compile_structural_feedback_chain,
    transition_feedback_chain,
)
from cmf_builder.domain.category_syntax import GovernedRef


ST_06_04_IMPLEMENTATION_RECEIPT_SHA256 = (
    "c5b67fbd0a2c7a1cc98e1e8d03f9ea6c10ea14369c9f2b61d399cce88cf35021"
)


class ConversationalCommandRejected(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class CompileConversationalFeedbackCommand:
    command_id: str
    source: ConversationalFeedbackInput
    actor_id: str
    now: datetime
    correlation_id: str
    causation_id: str


@dataclass(frozen=True, slots=True)
class TransitionConversationalFeedbackCommand:
    command_id: str
    chain_id: str
    expected_parent_hash: str
    event: str
    new_version: str
    authority_ref: GovernedRef
    actor_id: str
    now: datetime
    correlation_id: str
    causation_id: str
    reaction_receipt_ref: GovernedRef | None = None
    expression_moment_ref: GovernedRef | None = None
    reason: str = "governed structural transition"


@dataclass(frozen=True, slots=True)
class ConversationalFeedbackReceipt:
    receipt_id: str
    receipt_hash: str
    command_id: str
    command_payload_hash: str
    chain_id: str
    chain_version: str
    chain_hash: str
    state: str
    implementation_status: str
    human_policy_status: str
    production_ready: bool
    certified: bool


@dataclass(frozen=True, slots=True)
class ConversationalFeedbackObservation:
    event_name: str
    outcome: str
    story_id: str
    command_id: str
    chain_id: str
    chain_version: str
    profile_id: str | None
    authority_identity: str
    provenance: tuple[str, ...]
    correlation_id: str
    causation_id: str
    failure_context: str | None


class InMemoryConversationalObservationSink:
    def __init__(self) -> None:
        self._items: list[ConversationalFeedbackObservation] = []

    @property
    def items(self) -> tuple[ConversationalFeedbackObservation, ...]:
        return tuple(self._items)

    def emit(self, item: ConversationalFeedbackObservation) -> None:
        self._items.append(item)


class InMemoryConversationalFeedbackRepository:
    def __init__(self) -> None:
        self._chains: dict[str, ConversationalFeedbackChain] = {}
        self._active_versions: dict[str, str] = {}
        self._payload_hashes: dict[str, str] = {}
        self._receipts: dict[str, ConversationalFeedbackReceipt] = {}
        self._fail_before_commit = False

    @property
    def chain_version_count(self) -> int:
        return len(self._chains)

    @property
    def receipt_count(self) -> int:
        return len(self._receipts)

    @property
    def command_count(self) -> int:
        return len(self._payload_hashes)

    def inject_failure_before_commit(self) -> None:
        self._fail_before_commit = True

    def command_state(
        self, command_id: str
    ) -> tuple[str, ConversationalFeedbackReceipt] | None:
        if command_id not in self._receipts:
            return None
        return self._payload_hashes[command_id], self._receipts[command_id]

    def active_chain(self, chain_id: str) -> ConversationalFeedbackChain:
        try:
            version = self._active_versions[chain_id]
            return self._chains[f"{chain_id}@{version}"]
        except KeyError as error:
            raise ConversationalCommandRejected("Active feedback chain does not exist.") from error

    def historical_chain(self, chain_id: str, version: str) -> ConversationalFeedbackChain:
        try:
            return self._chains[f"{chain_id}@{version}"]
        except KeyError as error:
            raise ConversationalCommandRejected("Historical feedback chain does not exist.") from error

    def commit(
        self,
        *,
        command_id: str,
        payload_hash: str,
        chain: ConversationalFeedbackChain,
        receipt: ConversationalFeedbackReceipt,
    ) -> None:
        if self._fail_before_commit:
            self._fail_before_commit = False
            raise ConversationalCommandRejected("Injected atomic feedback-chain failure.")
        key = f"{chain.chain_id}@{chain.chain_version}"
        existing = self._chains.get(key)
        if existing is not None and existing.chain_hash != chain.chain_hash:
            raise ConversationalCommandRejected(
                "An immutable feedback-chain version already has different content."
            )
        self._chains[key] = chain
        self._active_versions[chain.chain_id] = chain.chain_version
        self._payload_hashes[command_id] = payload_hash
        self._receipts[command_id] = receipt


class ConversationalFeedbackService:
    def __init__(
        self,
        authority: AuthorityService,
        repository: InMemoryConversationalFeedbackRepository,
        observations: InMemoryConversationalObservationSink,
    ) -> None:
        self._authority = authority
        self._repository = repository
        self._observations = observations

    def compile(
        self, command: CompileConversationalFeedbackCommand
    ) -> ConversationalFeedbackReceipt:
        payload_hash = _compile_payload_hash(command)
        prior = self._replay(command.command_id, payload_hash)
        if prior is not None:
            self._observe_compile(command, "ST-06.05:FeedbackChainReplayReturned", "PASS", None)
            return prior
        try:
            self._authorize(command.actor_id, command.source.chain_id, command.now)
            chain = compile_structural_feedback_chain(command.source)
            receipt = _receipt(command.command_id, payload_hash, chain)
            self._repository.commit(
                command_id=command.command_id,
                payload_hash=payload_hash,
                chain=chain,
                receipt=receipt,
            )
        except (AuthorityDenied, ConversationalFeedbackError, ConversationalCommandRejected) as error:
            self._observe_compile(command, "ST-06.05:FeedbackChainRejected", "FAIL", str(error))
            raise ConversationalCommandRejected(str(error)) from error
        self._observe_compile(command, "ST-06.05:FeedbackChainCompiled", "PASS", None)
        return receipt

    def transition(
        self, command: TransitionConversationalFeedbackCommand
    ) -> ConversationalFeedbackReceipt:
        payload_hash = _transition_payload_hash(command)
        active: ConversationalFeedbackChain | None = None
        try:
            prior = self._replay(command.command_id, payload_hash)
            if prior is not None:
                active = self._repository.active_chain(command.chain_id)
                self._observe_transition(
                    command,
                    active,
                    "ST-06.05:FeedbackTransitionReplayReturned",
                    "PASS",
                    None,
                )
                return prior
            active = self._repository.active_chain(command.chain_id)
            if active.chain_hash != command.expected_parent_hash:
                raise ConversationalCommandRejected(
                    "Transition parent is stale, superseded, or not the active chain."
                )
            action = (
                Action.WITHDRAW_CONVERSATIONAL_FEEDBACK_CONSENT
                if command.event == "WITHDRAW_CONSENT"
                else Action.COMPILE_CONVERSATIONAL_FEEDBACK
            )
            self._authorize(
                command.actor_id, command.chain_id, command.now, action=action
            )
            self._bind_actor_to_transition_authority(
                command.actor_id, command.authority_ref
            )
            transition = FeedbackTransition(
                event=command.event,
                new_version=command.new_version,
                authority_ref=command.authority_ref,
                reaction_receipt_ref=command.reaction_receipt_ref,
                expression_moment_ref=command.expression_moment_ref,
                reason=command.reason,
            )
            chain = transition_feedback_chain(active, transition)
            receipt = _receipt(command.command_id, payload_hash, chain)
            self._repository.commit(
                command_id=command.command_id,
                payload_hash=payload_hash,
                chain=chain,
                receipt=receipt,
            )
        except (AuthorityDenied, ConversationalFeedbackError, ConversationalCommandRejected) as error:
            self._observe_transition(
                command, active, "ST-06.05:FeedbackTransitionRejected", "FAIL", str(error)
            )
            raise ConversationalCommandRejected(str(error)) from error
        self._observe_transition(
            command, chain, "ST-06.05:FeedbackTransitionCommitted", "PASS", None
        )
        return receipt

    def resume(self, chain_id: str) -> ConversationalFeedbackChain:
        return self._repository.active_chain(chain_id)

    def _authorize(
        self,
        actor_id: str,
        resource_id: str,
        now: datetime,
        *,
        action: Action = Action.COMPILE_CONVERSATIONAL_FEEDBACK,
    ) -> None:
        self._authority.authorize(
            actor_id=actor_id,
            action=action,
            resource_id=resource_id,
            now=now,
        )

    @staticmethod
    def _bind_actor_to_transition_authority(
        actor_id: str, authority_ref: GovernedRef
    ) -> None:
        try:
            authority_ref.validate()
        except ValueError as error:
            raise AuthorityDenied(
                "Transition authority evidence is invalid.", actor_id=actor_id
            ) from error
        if authority_ref.authority != actor_id:
            raise AuthorityDenied(
                "Transition authority evidence does not identify the acting actor.",
                actor_id=actor_id,
                authority_identity=authority_ref.authority,
            )

    def _replay(
        self, command_id: str, payload_hash: str
    ) -> ConversationalFeedbackReceipt | None:
        prior = self._repository.command_state(command_id)
        if prior is None:
            return None
        prior_hash, prior_receipt = prior
        if prior_hash != payload_hash:
            raise ConversationalCommandRejected(
                "Command identity was reused with a different payload."
            )
        return prior_receipt

    def _observe_compile(
        self,
        command: CompileConversationalFeedbackCommand,
        event: str,
        outcome: str,
        failure: str | None,
    ) -> None:
        self._observations.emit(
            ConversationalFeedbackObservation(
                event_name=event,
                outcome=outcome,
                story_id="ST-06.05",
                command_id=command.command_id,
                chain_id=command.source.chain_id,
                chain_version=command.source.chain_version,
                profile_id=command.source.category_policy.profile_id,
                authority_identity=command.actor_id,
                provenance=(
                    f"ST-06.04:{ST_06_04_IMPLEMENTATION_RECEIPT_SHA256}",
                    f"policy:{command.source.category_policy.ruleset_hash}",
                ),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                failure_context=failure,
            )
        )

    def _observe_transition(
        self,
        command: TransitionConversationalFeedbackCommand,
        chain: ConversationalFeedbackChain | None,
        event: str,
        outcome: str,
        failure: str | None,
    ) -> None:
        self._observations.emit(
            ConversationalFeedbackObservation(
                event_name=event,
                outcome=outcome,
                story_id="ST-06.05",
                command_id=command.command_id,
                chain_id=command.chain_id,
                chain_version=command.new_version,
                profile_id=None if chain is None else chain.profile_id,
                authority_identity=command.actor_id,
                provenance=(
                    f"parent:{command.expected_parent_hash}",
                    "transition-authority:"
                    f"{command.authority_ref.authority}:"
                    f"{command.authority_ref.object_id}@{command.authority_ref.version}:"
                    f"{command.authority_ref.sha256}",
                ),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                failure_context=failure,
            )
        )


def _compile_payload_hash(command: CompileConversationalFeedbackCommand) -> str:
    content = {
        "kind": "compile",
        "command_id": command.command_id,
        "source": command.source.canonical_dict(),
        "actor_id": command.actor_id,
        "now": command.now.isoformat(),
        "correlation_id": command.correlation_id,
        "causation_id": command.causation_id,
        "st_06_04_receipt_sha256": ST_06_04_IMPLEMENTATION_RECEIPT_SHA256,
    }
    return f"sha256:{sha256(_canonical_json(content)).hexdigest()}"


def _transition_payload_hash(command: TransitionConversationalFeedbackCommand) -> str:
    content = {
        "kind": "transition",
        "command_id": command.command_id,
        "chain_id": command.chain_id,
        "expected_parent_hash": command.expected_parent_hash,
        "event": command.event,
        "new_version": command.new_version,
        "authority_ref": command.authority_ref.canonical_dict(),
        "reaction_receipt_ref": _optional_ref(command.reaction_receipt_ref),
        "expression_moment_ref": _optional_ref(command.expression_moment_ref),
        "reason": command.reason,
        "actor_id": command.actor_id,
        "now": command.now.isoformat(),
        "correlation_id": command.correlation_id,
        "causation_id": command.causation_id,
    }
    return f"sha256:{sha256(_canonical_json(content)).hexdigest()}"


def _receipt(
    command_id: str,
    payload_hash: str,
    chain: ConversationalFeedbackChain,
) -> ConversationalFeedbackReceipt:
    content = {
        "schema_version": "cmf-builder-conversational-feedback-receipt/v1",
        "command_id": command_id,
        "command_payload_hash": payload_hash,
        "chain_id": chain.chain_id,
        "chain_version": chain.chain_version,
        "chain_hash": chain.chain_hash,
        "state": chain.state,
        "implementation_status": "IMPLEMENTED_DEVELOPMENT_PASS",
        "human_policy_status": "HD-006_PENDING;HD-007_CERTIFICATION_PENDING",
        "production_ready": False,
        "certified": False,
    }
    digest = sha256(_canonical_json(content)).hexdigest()
    return ConversationalFeedbackReceipt(
        receipt_id=f"conversational-feedback-receipt_{digest}",
        receipt_hash=f"sha256:{digest}",
        command_id=command_id,
        command_payload_hash=payload_hash,
        chain_id=chain.chain_id,
        chain_version=chain.chain_version,
        chain_hash=chain.chain_hash,
        state=chain.state,
        implementation_status="IMPLEMENTED_DEVELOPMENT_PASS",
        human_policy_status="HD-006_PENDING;HD-007_CERTIFICATION_PENDING",
        production_ready=False,
        certified=False,
    )


def _optional_ref(ref: GovernedRef | None) -> dict[str, str] | None:
    return None if ref is None else ref.canonical_dict()


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
