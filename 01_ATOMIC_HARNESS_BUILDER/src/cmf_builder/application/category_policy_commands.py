from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json

from cmf_builder.application.authority import Action, AuthorityDenied, AuthorityService
from cmf_builder.domain.category_runtime_rules import (
    CategoryOperatingRules,
    CategoryPolicyError,
    CategoryPolicyInput,
    compile_category_operating_rules,
)


ST_06_03_IMPLEMENTATION_RECEIPT_SHA256 = (
    "89d2f10aca87399e25f0f2115562bd4ac2c1bc2bb1f0c4621540a25e0c15569b"
)


class CategoryPolicyCommandRejected(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class CompileCategoryPolicyCommand:
    command_id: str
    source: CategoryPolicyInput
    actor_id: str
    now: datetime
    correlation_id: str
    causation_id: str


@dataclass(frozen=True, slots=True)
class CategoryPolicyCompilationReceipt:
    receipt_id: str
    receipt_hash: str
    command_id: str
    command_payload_hash: str
    ruleset_id: str
    ruleset_hash: str
    category_id: str | None
    implementation_status: str
    evidence_status: str
    production_ready: bool
    certified: bool


@dataclass(frozen=True, slots=True)
class CategoryPolicyObservation:
    event_name: str
    outcome: str
    story_id: str
    command_id: str
    ruleset_identity: str
    category_id: str | None
    profile_id: str | None
    authority_identity: str
    evaluator_owner: str | None
    repair_owner: str | None
    migration_authority: str | None
    version: str
    provenance: tuple[str, ...]
    correlation_id: str
    causation_id: str
    failure_context: str | None


class InMemoryCategoryPolicyObservationSink:
    def __init__(self) -> None:
        self._items: list[CategoryPolicyObservation] = []

    @property
    def items(self) -> tuple[CategoryPolicyObservation, ...]:
        return tuple(self._items)

    def emit(self, item: CategoryPolicyObservation) -> None:
        self._items.append(item)


class InMemoryCategoryPolicyRepository:
    def __init__(self) -> None:
        self._rulesets: dict[str, CategoryOperatingRules] = {}
        self._payload_hashes: dict[str, str] = {}
        self._receipts: dict[str, CategoryPolicyCompilationReceipt] = {}
        self._fail_before_commit = False

    @property
    def ruleset_count(self) -> int:
        return len(self._rulesets)

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
    ) -> tuple[str, CategoryPolicyCompilationReceipt] | None:
        if command_id not in self._receipts:
            return None
        return self._payload_hashes[command_id], self._receipts[command_id]

    def ruleset(self, ruleset_name: str, ruleset_version: str) -> CategoryOperatingRules:
        try:
            return self._rulesets[f"{ruleset_name}@{ruleset_version}"]
        except KeyError as error:
            raise CategoryPolicyCommandRejected("Category ruleset does not exist.") from error

    def commit(
        self,
        *,
        command: CompileCategoryPolicyCommand,
        payload_hash: str,
        ruleset: CategoryOperatingRules,
        receipt: CategoryPolicyCompilationReceipt,
    ) -> None:
        if self._fail_before_commit:
            self._fail_before_commit = False
            raise CategoryPolicyCommandRejected("Injected atomic category-policy failure.")
        key = f"{ruleset.ruleset_name}@{ruleset.ruleset_version}"
        existing = self._rulesets.get(key)
        if existing is not None and existing.ruleset_hash != ruleset.ruleset_hash:
            raise CategoryPolicyCommandRejected(
                "An immutable category ruleset version already has different content."
            )
        self._rulesets[key] = ruleset
        self._payload_hashes[command.command_id] = payload_hash
        self._receipts[command.command_id] = receipt


class CategoryPolicyCompilationService:
    def __init__(
        self,
        authority: AuthorityService,
        repository: InMemoryCategoryPolicyRepository,
        observations: InMemoryCategoryPolicyObservationSink,
    ) -> None:
        self._authority = authority
        self._repository = repository
        self._observations = observations

    def compile(
        self, command: CompileCategoryPolicyCommand
    ) -> CategoryPolicyCompilationReceipt:
        payload_hash = _payload_hash(command)
        prior = self._repository.command_state(command.command_id)
        if prior is not None:
            prior_hash, prior_receipt = prior
            if prior_hash != payload_hash:
                self._reject(command, "Command identity was reused with a different payload.")
            self._observe(
                command,
                event_name="ST-06.04:CategoryPolicyReplayReturned",
                outcome="PASS",
                failure=None,
            )
            return prior_receipt
        try:
            self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.COMPILE_CATEGORY_POLICY,
                resource_id=command.source.ruleset_name,
                now=command.now,
            )
            ruleset = compile_category_operating_rules(command.source)
            receipt = _receipt(command, payload_hash, ruleset)
            self._repository.commit(
                command=command,
                payload_hash=payload_hash,
                ruleset=ruleset,
                receipt=receipt,
            )
        except (
            AuthorityDenied,
            CategoryPolicyError,
            CategoryPolicyCommandRejected,
        ) as error:
            self._reject(command, str(error))
        self._observe(
            command,
            event_name="ST-06.04:CategoryPolicyCompiled",
            outcome="PASS",
            failure=None,
        )
        return receipt

    def _reject(self, command: CompileCategoryPolicyCommand, detail: str) -> None:
        self._observe(
            command,
            event_name="ST-06.04:CategoryPolicyRejected",
            outcome="FAIL",
            failure=detail,
        )
        raise CategoryPolicyCommandRejected(detail)

    def _observe(
        self,
        command: CompileCategoryPolicyCommand,
        *,
        event_name: str,
        outcome: str,
        failure: str | None,
    ) -> None:
        source = command.source
        self._observations.emit(
            CategoryPolicyObservation(
                event_name=event_name,
                outcome=outcome,
                story_id="ST-06.04",
                command_id=command.command_id,
                ruleset_identity=source.ruleset_name,
                category_id=source.syntax.category_id,
                profile_id=source.syntax.profile_id,
                authority_identity=command.actor_id,
                evaluator_owner=_ref_id(source.evaluator_owner_ref),
                repair_owner=_ref_id(source.repair_owner_ref),
                migration_authority=_ref_id(source.migration_authority_ref),
                version=source.ruleset_version,
                provenance=(
                    f"syntax:{source.syntax.syntax_hash}",
                    f"sequence:{source.sequence.sequence_hash}",
                    f"ST-06.03:{ST_06_03_IMPLEMENTATION_RECEIPT_SHA256}",
                ),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                failure_context=failure,
            )
        )


def _payload_hash(command: CompileCategoryPolicyCommand) -> str:
    content = {
        "command_id": command.command_id,
        "source": command.source.canonical_dict(),
        "actor_id": command.actor_id,
        "now": command.now.isoformat(),
        "correlation_id": command.correlation_id,
        "causation_id": command.causation_id,
        "st_06_03_implementation_receipt_sha256": ST_06_03_IMPLEMENTATION_RECEIPT_SHA256,
    }
    return f"sha256:{sha256(_canonical_json(content)).hexdigest()}"


def _receipt(
    command: CompileCategoryPolicyCommand,
    payload_hash: str,
    ruleset: CategoryOperatingRules,
) -> CategoryPolicyCompilationReceipt:
    content = {
        "schema_version": "cmf-builder-category-policy-compilation-receipt/v1",
        "command_id": command.command_id,
        "command_payload_hash": payload_hash,
        "ruleset_id": ruleset.ruleset_id,
        "ruleset_hash": ruleset.ruleset_hash,
        "category_id": ruleset.category_id,
        "implementation_status": "IMPLEMENTED_DEVELOPMENT_PASS",
        "evidence_status": "EXTERNAL_AND_CERTIFICATION_GATES_REMAIN_OPEN",
        "st_06_03_implementation_receipt_sha256": ST_06_03_IMPLEMENTATION_RECEIPT_SHA256,
        "production_ready": False,
        "certified": False,
    }
    digest = sha256(_canonical_json(content)).hexdigest()
    return CategoryPolicyCompilationReceipt(
        receipt_id=f"category-policy-compilation-receipt_{digest}",
        receipt_hash=f"sha256:{digest}",
        command_id=command.command_id,
        command_payload_hash=payload_hash,
        ruleset_id=ruleset.ruleset_id,
        ruleset_hash=ruleset.ruleset_hash,
        category_id=ruleset.category_id,
        implementation_status="IMPLEMENTED_DEVELOPMENT_PASS",
        evidence_status="EXTERNAL_AND_CERTIFICATION_GATES_REMAIN_OPEN",
        production_ready=False,
        certified=False,
    )


def _ref_id(ref) -> str | None:
    return None if ref is None else ref.object_id


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
