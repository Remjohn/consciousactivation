from __future__ import annotations

from pathlib import Path
import shutil

import pytest

from cmf_builder.application.activative_skill_commands import (
    ActivativeSkillCommandError,
    ActivativeSkillCommandService,
    CompileActivativeSkillCommand,
    _validate_development_evaluation,
)
from cmf_builder.skills.portable_package import PortableSkillPackage
from tests.skills.activative_semantics.test_contracts import make_input


ROOT = Path(__file__).resolve().parents[3]


def command(**changes: object) -> CompileActivativeSkillCommand:
    values: dict[str, object] = {
        "command_id": "skill-command-1",
        "run_id": "activative-development-run-1",
        "actor_id": "analyst-1",
        "compiler_input": make_input(),
    }
    values.update(changes)
    return CompileActivativeSkillCommand(**values)  # type: ignore[arg-type]


def test_vertical_compile_binds_pack_package_necessity_and_evaluation() -> None:
    service = ActivativeSkillCommandService(root=ROOT, authorized_actor_ids=("analyst-1",))
    receipt = service.compile(command())
    pack = service.get_pack(receipt.pack_id)
    assert receipt.story_id == "ST-05.03"
    assert receipt.package_hash == "sha256:6e9fbf9925a3ccaedf2bc053f4a349e69e3bff80500443c2d22b52ca40c789c6"
    assert receipt.evaluation_status == "development_validated"
    assert receipt.production_eligible is False and receipt.certified is False
    assert pack.human_truth_generated is False
    assert pack.human_reaction_generated is False
    assert pack.issued_receipt_kinds == ()
    assert service.observations[-1].outcome == "PASS"


def test_evaluation_receipt_binds_14_governed_cases_at_development_ceiling() -> None:
    package = PortableSkillPackage.load(
        ROOT / "skill-packages/activative_intelligence_pack_compiler/1.0.0"
    )
    receipt = _validate_development_evaluation(ROOT, package)
    assert receipt.case_count == 14
    assert receipt.development_validated_count == 3
    assert receipt.insufficient_evidence_count == 11
    assert receipt.status == "development_validated"
    assert receipt.production_eligible is False and receipt.certified is False


def test_repeat_is_idempotent_and_conflicting_payload_fails_closed() -> None:
    service = ActivativeSkillCommandService(root=ROOT, authorized_actor_ids=("analyst-1",))
    first = service.compile(command())
    assert service.compile(command()) == first
    with pytest.raises(ActivativeSkillCommandError, match="payload changed"):
        service.compile(command(run_id="changed"))


def test_authority_and_atomic_failure_leave_no_active_pack() -> None:
    service = ActivativeSkillCommandService(root=ROOT, authorized_actor_ids=("analyst-1",))
    with pytest.raises(ActivativeSkillCommandError, match="authority"):
        service.compile(command(actor_id="intruder"))
    with pytest.raises(ActivativeSkillCommandError, match="Injected"):
        service.compile(command(command_id="atomic-fail"), inject_failure=True)
    with pytest.raises(KeyError):
        service.get_pack("activative-intelligence-pack_missing")
    assert [item.outcome for item in service.observations] == ["FAIL", "FAIL"]


def test_altered_evaluation_asset_fails_before_semantic_commit(tmp_path: Path) -> None:
    shutil.copytree(
        ROOT / "skill-packages",
        tmp_path / "skill-packages",
    )
    shutil.copytree(
        ROOT / "evaluation",
        tmp_path / "evaluation",
    )
    rubric = tmp_path / "evaluation/skills/activative_intelligence_pack_compiler/RUBRIC.yaml"
    rubric.write_bytes(rubric.read_bytes() + b"\n")
    service = ActivativeSkillCommandService(root=tmp_path, authorized_actor_ids=("analyst-1",))
    with pytest.raises(ActivativeSkillCommandError, match="hash mismatch"):
        service.compile(command())
    assert service.observations[-1].outcome == "FAIL"
