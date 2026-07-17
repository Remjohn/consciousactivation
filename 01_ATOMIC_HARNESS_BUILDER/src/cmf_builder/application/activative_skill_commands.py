from __future__ import annotations

from dataclasses import dataclass, fields
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
from types import ModuleType

from cmf_builder.skills.activative_contracts import (
    ActivativeCompilerInput,
    ActivativeIntelligencePack,
)
from cmf_builder.skills.necessity import HarnessSkillMode, determine_skill_requirement
from cmf_builder.skills.portable_package import PortableSkillPackage


class ActivativeSkillCommandError(ValueError):
    """The bounded real-skill command failed before an atomic commit."""


@dataclass(frozen=True, slots=True)
class CompileActivativeSkillCommand:
    command_id: str
    run_id: str
    actor_id: str
    compiler_input: ActivativeCompilerInput


@dataclass(frozen=True, slots=True)
class SkillDevelopmentEvaluationReceipt:
    receipt_id: str
    skill_id: str
    skill_version: str
    package_hash: str
    corpus_manifest_hash: str
    rubric_hash: str
    evaluator_hash: str
    case_count: int
    development_validated_count: int
    insufficient_evidence_count: int
    status: str
    production_eligible: bool
    certified: bool
    receipt_hash: str


@dataclass(frozen=True, slots=True)
class ActivativeSkillCompilationReceipt:
    receipt_id: str
    story_id: str
    command_id: str
    run_id: str
    authority_identity: str
    pack_id: str
    pack_hash: str
    package_manifest_hash: str
    package_hash: str
    package_receipt_hash: str
    necessity_decision_hash: str
    evaluation_receipt_hash: str
    evaluation_status: str
    production_eligible: bool
    certified: bool
    receipt_hash: str


@dataclass(frozen=True, slots=True)
class ActivativeSkillObservation:
    story_id: str
    event_name: str
    run_id: str
    artifact_identity: str | None
    authority_identity: str
    version: str
    provenance: tuple[str, ...]
    outcome: str
    failure_context: dict[str, str]


class ActivativeSkillCommandService:
    STORY_ID = "ST-05.03"
    PACKAGE_RELATIVE = Path("skill-packages/activative_intelligence_pack_compiler/1.0.0")

    def __init__(self, *, root: Path, authorized_actor_ids: tuple[str, ...]) -> None:
        self._root = root.resolve()
        self._authorized = frozenset(authorized_actor_ids)
        self._commands: dict[str, tuple[str, ActivativeSkillCompilationReceipt]] = {}
        self._packs: dict[str, ActivativeIntelligencePack] = {}
        self._receipts: dict[str, ActivativeSkillCompilationReceipt] = {}
        self.observations: list[ActivativeSkillObservation] = []

    def compile(
        self,
        command: CompileActivativeSkillCommand,
        *,
        inject_failure: bool = False,
    ) -> ActivativeSkillCompilationReceipt:
        payload_hash = _command_hash(command)
        duplicate = self._commands.get(command.command_id)
        if duplicate:
            if duplicate[0] != payload_hash:
                self._reject(command, "CONFLICTING_COMMAND", "Command payload changed.")
            self._observe(command, "activative_skill_compilation_replayed", duplicate[1].pack_id, "PASS", {})
            return duplicate[1]
        if command.actor_id not in self._authorized:
            self._reject(command, "UNAUTHORIZED", "Actor lacks Analyst compilation authority.")
        try:
            package = PortableSkillPackage.load(self._root / self.PACKAGE_RELATIVE)
            necessity = determine_skill_requirement(HarnessSkillMode.ACTIVATIVE)
            if necessity.required_skill_id != package.skill_id or necessity.required_skill_version != package.version:
                raise ActivativeSkillCommandError("Necessity evidence and package identity disagree.")
            evaluation = _validate_development_evaluation(self._root, package)
            pack = ActivativeIntelligencePack.compile(command.compiler_input)
            if inject_failure:
                raise ActivativeSkillCommandError("Injected atomic Activative skill failure.")
            receipt = _compilation_receipt(command, pack, package, necessity.decision_hash, evaluation)
            # All state becomes visible only after package, evaluation, semantic, and authority checks pass.
            self._packs[pack.pack_id] = pack
            self._receipts[receipt.receipt_id] = receipt
            self._commands[command.command_id] = (payload_hash, receipt)
            self._observe(command, "activative_skill_compilation_committed", pack.pack_id, "PASS", {})
            return receipt
        except Exception as error:
            self._observe(
                command,
                "activative_skill_compilation_rejected",
                None,
                "FAIL",
                {"code": str(getattr(error, "code", type(error).__name__)), "message": str(error)},
            )
            raise

    def get_pack(self, pack_id: str) -> ActivativeIntelligencePack:
        pack = self._packs.get(pack_id)
        if pack is None:
            raise KeyError(pack_id)
        return pack

    def _reject(self, command: CompileActivativeSkillCommand, code: str, message: str) -> None:
        self._observe(command, "activative_skill_compilation_rejected", None, "FAIL", {"code": code, "message": message})
        raise ActivativeSkillCommandError(message)

    def _observe(self, command: CompileActivativeSkillCommand, event: str, artifact: str | None, outcome: str, failure: dict[str, str]) -> None:
        self.observations.append(
            ActivativeSkillObservation(
                story_id=self.STORY_ID,
                event_name=event,
                run_id=command.run_id,
                artifact_identity=artifact,
                authority_identity=command.actor_id,
                version="1.0.0",
                provenance=command.compiler_input.source_refs,
                outcome=outcome,
                failure_context=failure,
            )
        )


def _validate_development_evaluation(
    root: Path, package: PortableSkillPackage
) -> SkillDevelopmentEvaluationReceipt:
    manifest = json.loads(package.manifest_bytes)
    assets = manifest.get("evaluation_assets")
    if not isinstance(assets, dict):
        raise ActivativeSkillCommandError("The package lacks evaluation asset pins.")
    observed: dict[str, tuple[Path, str]] = {}
    for name in ("corpus_manifest", "rubric", "evaluator"):
        item = assets.get(name)
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            raise ActivativeSkillCommandError("An evaluation asset pin is incomplete.")
        relative = Path(str(item["path"]))
        if relative.is_absolute() or ".." in relative.parts:
            raise ActivativeSkillCommandError("Evaluation assets must use portable repository-relative paths.")
        path = root / relative
        if not path.is_file():
            raise ActivativeSkillCommandError(f"Evaluation asset is missing: {relative.as_posix()}")
        digest = f"sha256:{sha256(path.read_bytes()).hexdigest()}"
        if digest != item["sha256"]:
            raise ActivativeSkillCommandError(f"Evaluation asset hash mismatch: {relative.as_posix()}")
        observed[name] = (path, digest)
    corpus = _read_json(observed["corpus_manifest"][0])
    rubric = _read_json(observed["rubric"][0])
    if (
        corpus.get("protected") is not False
        or corpus.get("production_certification_eligible") is not False
        or corpus.get("campaign_ceiling") != "development_validated"
        or corpus.get("production_thresholds") != "NOT_DEFINED_HUMAN_GOVERNANCE_REQUIRED"
        or rubric.get("campaign_ceiling") != "development_validated"
    ):
        raise ActivativeSkillCommandError("Evaluation evidence exceeds the development-only authority ceiling.")
    module = _load_evaluator(observed["evaluator"][0])
    base_item = corpus.get("base_fixture")
    cases = corpus.get("cases")
    if not isinstance(base_item, dict) or not isinstance(cases, list) or corpus.get("case_count") != len(cases):
        raise ActivativeSkillCommandError("Evaluation corpus manifest is incomplete.")
    evaluation_root = observed["corpus_manifest"][0].parent
    base_path = evaluation_root / str(base_item.get("path"))
    _verify_asset_hash(base_path, str(base_item.get("sha256")))
    counts = {"development_validated": 0, "insufficient_evidence": 0}
    for item in cases:
        if not isinstance(item, dict):
            raise ActivativeSkillCommandError("Evaluation case metadata is invalid.")
        case_path = evaluation_root / str(item.get("path"))
        _verify_asset_hash(case_path, str(item.get("sha256")))
        case = module.load_case(base_path, case_path)
        receipt = module.evaluate_case(case, rubric)
        if receipt.status not in counts:
            raise ActivativeSkillCommandError("Evaluation exceeded the development maturity ceiling.")
        counts[receipt.status] += 1
    if counts != {"development_validated": 3, "insufficient_evidence": 11}:
        raise ActivativeSkillCommandError("The governed development evaluation result set has drifted.")
    unsigned = {
        "skill_id": package.skill_id,
        "skill_version": package.version,
        "package_hash": package.package_hash,
        "corpus_manifest_hash": observed["corpus_manifest"][1],
        "rubric_hash": observed["rubric"][1],
        "evaluator_hash": observed["evaluator"][1],
        "case_count": sum(counts.values()),
        "development_validated_count": counts["development_validated"],
        "insufficient_evidence_count": counts["insufficient_evidence"],
        "status": "development_validated",
        "production_eligible": False,
        "certified": False,
    }
    digest = sha256(_canonical_bytes(unsigned)).hexdigest()
    return SkillDevelopmentEvaluationReceipt(
        receipt_id=f"skill-development-evaluation_{digest}",
        **unsigned,
        receipt_hash=f"sha256:{digest}",
    )


def _load_evaluator(path: Path) -> ModuleType:
    name = "cmf_builder_governed_activative_evaluator"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ActivativeSkillCommandError("The governed evaluator cannot be loaded.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(name, None)
    return module


def _verify_asset_hash(path: Path, expected: str) -> None:
    if not path.is_file() or f"sha256:{sha256(path.read_bytes()).hexdigest()}" != expected:
        raise ActivativeSkillCommandError(f"Evaluation corpus member hash mismatch: {path.name}")


def _read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ActivativeSkillCommandError("Governed evaluation metadata must be a mapping.")
    return value


def _compilation_receipt(
    command: CompileActivativeSkillCommand,
    pack: ActivativeIntelligencePack,
    package: PortableSkillPackage,
    necessity_hash: str,
    evaluation: SkillDevelopmentEvaluationReceipt,
) -> ActivativeSkillCompilationReceipt:
    unsigned = {
        "story_id": "ST-05.03",
        "command_id": command.command_id,
        "run_id": command.run_id,
        "authority_identity": command.actor_id,
        "pack_id": pack.pack_id,
        "pack_hash": pack.pack_hash,
        "package_manifest_hash": package.manifest_hash,
        "package_hash": package.package_hash,
        "package_receipt_hash": package.receipt.receipt_hash,
        "necessity_decision_hash": necessity_hash,
        "evaluation_receipt_hash": evaluation.receipt_hash,
        "evaluation_status": evaluation.status,
        "production_eligible": False,
        "certified": False,
    }
    digest = sha256(_canonical_bytes(unsigned)).hexdigest()
    return ActivativeSkillCompilationReceipt(
        receipt_id=f"ST-05.03:StoryOutcomeReceipt:{digest}",
        **unsigned,
        receipt_hash=f"sha256:{digest}",
    )


def _command_hash(command: CompileActivativeSkillCommand) -> str:
    payload = {
        field.name: (
            command.compiler_input.canonical_dict()
            if field.name == "compiler_input"
            else getattr(command, field.name)
        )
        for field in fields(command)
    }
    return f"sha256:{sha256(_canonical_bytes(payload)).hexdigest()}"


def _canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
