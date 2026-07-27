from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json

from cmf_builder.application.authority import (
    Action,
    AuthorityDenied,
    AuthorityService,
)
from cmf_builder.domain.category_syntax import (
    ActivativeSequenceProgram,
    CategoryNativeSyntax,
    CategorySyntaxError,
    CategorySyntaxInput,
    compile_category_native_syntax,
)


OD_AM_001_RECEIPT_SHA256 = (
    "cb6b1e6b15a6d2bde05ebf5858524c9670306ee382fa4fdc97a44590846bbf44"
)
ST_06_02_RECEIPT_SHA256 = (
    "0224d3866dafbcbce2de7202e96c24f9fd3f4fd95bf217dadb22337f79cee151"
)
BD_004_ADMISSION_RECEIPT_SHA256 = (
    "17f772ce86d8082767991455c2968253ca3dcbc185151b9aff48f73f075ba245"
)
BD_007_DISPOSITION = "EVIDENCE_PENDING"


class SyntaxCommandRejected(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class CompileCategorySyntaxCommand:
    command_id: str
    source: CategorySyntaxInput
    actor_id: str
    now: datetime
    correlation_id: str
    causation_id: str


@dataclass(frozen=True, slots=True)
class CategorySyntaxCompilationReceipt:
    receipt_id: str
    receipt_hash: str
    command_id: str
    command_payload_hash: str
    harness_id: str
    harness_version: str
    syntax_hash: str
    sequence_hash: str
    implementation_status: str
    evidence_status: str
    production_ready: bool
    certified: bool


@dataclass(frozen=True, slots=True)
class CategorySyntaxObservation:
    event_name: str
    outcome: str
    story_id: str
    command_id: str
    harness_id: str
    harness_version: str
    category_id: str | None
    profile_id: str | None
    authority_identity: str
    source_evidence: tuple[str, ...]
    rich_lineage: tuple[str, ...]
    maturity_status: str
    correlation_id: str
    causation_id: str
    failure_context: str | None


class InMemoryCategorySyntaxObservationSink:
    def __init__(self) -> None:
        self._items: list[CategorySyntaxObservation] = []

    @property
    def items(self) -> tuple[CategorySyntaxObservation, ...]:
        return tuple(self._items)

    def emit(self, item: CategorySyntaxObservation) -> None:
        self._items.append(item)


class InMemoryCategorySyntaxRepository:
    def __init__(self) -> None:
        self._artifact_sets: dict[
            str, tuple[CategoryNativeSyntax, ActivativeSequenceProgram]
        ] = {}
        self._receipts: dict[str, CategorySyntaxCompilationReceipt] = {}
        self._payload_hashes: dict[str, str] = {}
        self._fail_before_commit = False

    @property
    def artifact_set_count(self) -> int:
        return len(self._artifact_sets)

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
    ) -> tuple[str, CategorySyntaxCompilationReceipt] | None:
        receipt = self._receipts.get(command_id)
        payload_hash = self._payload_hashes.get(command_id)
        if receipt is None or payload_hash is None:
            return None
        return payload_hash, receipt

    def artifacts(
        self, harness_id: str, harness_version: str
    ) -> tuple[CategoryNativeSyntax, ActivativeSequenceProgram]:
        key = f"{harness_id}@{harness_version}"
        try:
            return self._artifact_sets[key]
        except KeyError as error:
            raise SyntaxCommandRejected("No compiled syntax exists for the Harness.") from error

    def commit(
        self,
        *,
        command: CompileCategorySyntaxCommand,
        payload_hash: str,
        syntax: CategoryNativeSyntax,
        sequence: ActivativeSequenceProgram,
        receipt: CategorySyntaxCompilationReceipt,
    ) -> None:
        if self._fail_before_commit:
            self._fail_before_commit = False
            raise SyntaxCommandRejected("Injected atomic category-syntax commit failure.")
        key = f"{syntax.harness_id}@{syntax.harness_version}"
        existing = self._artifact_sets.get(key)
        if existing is not None and (
            existing[0].syntax_hash != syntax.syntax_hash
            or existing[1].sequence_hash != sequence.sequence_hash
        ):
            raise SyntaxCommandRejected(
                "An immutable Harness version already has different syntax artifacts."
            )
        self._artifact_sets[key] = (syntax, sequence)
        self._payload_hashes[command.command_id] = payload_hash
        self._receipts[command.command_id] = receipt


class CategorySyntaxCompilationService:
    def __init__(
        self,
        authority: AuthorityService,
        repository: InMemoryCategorySyntaxRepository,
        observations: InMemoryCategorySyntaxObservationSink,
    ) -> None:
        self._authority = authority
        self._repository = repository
        self._observations = observations

    def compile(
        self, command: CompileCategorySyntaxCommand
    ) -> CategorySyntaxCompilationReceipt:
        payload_hash = _payload_hash(command)
        prior = self._repository.command_state(command.command_id)
        if prior is not None:
            prior_hash, prior_receipt = prior
            if prior_hash != payload_hash:
                self._reject(
                    command, "Command identity was reused with a different payload."
                )
            self._observe(
                command,
                event_name="ST-06.03:CategoryNativeCompilationReplayReturned",
                outcome="PASS",
                failure=None,
            )
            return prior_receipt
        try:
            self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.COMPILE_CATEGORY_SYNTAX,
                resource_id=command.source.harness_id,
                now=command.now,
            )
            syntax, sequence = compile_category_native_syntax(command.source)
            receipt = _receipt(command, payload_hash, syntax, sequence)
            self._repository.commit(
                command=command,
                payload_hash=payload_hash,
                syntax=syntax,
                sequence=sequence,
                receipt=receipt,
            )
        except (AuthorityDenied, CategorySyntaxError, SyntaxCommandRejected) as error:
            self._reject(command, str(error))
        self._observe(
            command,
            event_name="ST-06.03:CategoryNativeSyntaxCompiled",
            outcome="PASS",
            failure=None,
        )
        return receipt

    def _reject(self, command: CompileCategorySyntaxCommand, detail: str) -> None:
        self._observe(
            command,
            event_name="ST-06.03:CategoryNativeCompilationRejected",
            outcome="FAIL",
            failure=detail,
        )
        raise SyntaxCommandRejected(detail)

    def _observe(
        self,
        command: CompileCategorySyntaxCommand,
        *,
        event_name: str,
        outcome: str,
        failure: str | None,
    ) -> None:
        source = command.source
        self._observations.emit(
            CategorySyntaxObservation(
                event_name=event_name,
                outcome=outcome,
                story_id="ST-06.03",
                command_id=command.command_id,
                harness_id=source.harness_id,
                harness_version=source.harness_version,
                category_id=source.category_id,
                profile_id=source.profile_id,
                authority_identity=command.actor_id,
                source_evidence=tuple(
                    f"{ref.object_id}@{ref.version}#sha256:{ref.sha256}"
                    for ref in source.evidence_refs
                ),
                rich_lineage=tuple(
                    f"{ref.lineage_role}:{ref.object_id}@{ref.version}#sha256:{ref.sha256}"
                    for ref in source.rich_source_object_refs
                ),
                maturity_status="OFFLINE_STRUCTURAL_IMPLEMENTED_EVIDENCE_PENDING",
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                failure_context=failure,
            )
        )


def _payload_hash(command: CompileCategorySyntaxCommand) -> str:
    content = {
        "command_id": command.command_id,
        "source": command.source.canonical_dict(),
        "actor_id": command.actor_id,
        "now": command.now.isoformat(),
        "correlation_id": command.correlation_id,
        "causation_id": command.causation_id,
        "authority": {
            "od_am_001_receipt_sha256": OD_AM_001_RECEIPT_SHA256,
            "st_06_02_receipt_sha256": ST_06_02_RECEIPT_SHA256,
            "bd_004_admission_receipt_sha256": BD_004_ADMISSION_RECEIPT_SHA256,
            "bd_007_disposition": BD_007_DISPOSITION,
        },
    }
    return f"sha256:{sha256(_canonical_json(content)).hexdigest()}"


def _receipt(
    command: CompileCategorySyntaxCommand,
    payload_hash: str,
    syntax: CategoryNativeSyntax,
    sequence: ActivativeSequenceProgram,
) -> CategorySyntaxCompilationReceipt:
    content = {
        "schema_version": "cmf-builder-category-syntax-compilation-receipt/v1",
        "command_id": command.command_id,
        "command_payload_hash": payload_hash,
        "harness_id": syntax.harness_id,
        "harness_version": syntax.harness_version,
        "syntax_hash": syntax.syntax_hash,
        "sequence_hash": sequence.sequence_hash,
        "implementation_status": "IMPLEMENTED_DEVELOPMENT_PASS",
        "evidence_status": BD_007_DISPOSITION,
        "od_am_001_receipt_sha256": OD_AM_001_RECEIPT_SHA256,
        "st_06_02_receipt_sha256": ST_06_02_RECEIPT_SHA256,
        "bd_004_admission_receipt_sha256": BD_004_ADMISSION_RECEIPT_SHA256,
        "production_ready": False,
        "certified": False,
    }
    digest = sha256(_canonical_json(content)).hexdigest()
    return CategorySyntaxCompilationReceipt(
        receipt_id=f"category-syntax-compilation-receipt_{digest}",
        receipt_hash=f"sha256:{digest}",
        command_id=command.command_id,
        command_payload_hash=payload_hash,
        harness_id=syntax.harness_id,
        harness_version=syntax.harness_version,
        syntax_hash=syntax.syntax_hash,
        sequence_hash=sequence.sequence_hash,
        implementation_status="IMPLEMENTED_DEVELOPMENT_PASS",
        evidence_status=BD_007_DISPOSITION,
        production_ready=False,
        certified=False,
    )


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
