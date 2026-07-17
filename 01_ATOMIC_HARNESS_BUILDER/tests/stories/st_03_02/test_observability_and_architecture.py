from pathlib import Path

from tests.stories.st_03_02 import build_context, record_command

ROOT = Path(__file__).resolve().parents[3]


def test_success_observations_are_attributable_and_receipt_linked():
    service, repository, sink, run_id, question = build_context()
    receipt = service.record(record_command(repository, run_id, question.package_id))
    items = [item for item in sink.observations if item.story_id == "ST-03.02"]
    assert {item.event_name for item in items} == {"ST-03.02:HumanDecisionRecorded", "ST-03.02:OutcomeVerified"}
    assert all(item.authority_identity == "architect-1" for item in items)
    assert any(item.failure_context.get("receipt_id") == receipt.receipt_id for item in items)


def test_story_sources_have_no_external_runtime_product_or_persistence_imports():
    paths = (ROOT / "src/cmf_builder/domain/genesis_decisions.py", ROOT / "src/cmf_builder/application/genesis_decision_commands.py")
    text = "\n".join(path.read_text(encoding="utf-8").lower() for path in paths)
    assert all(word not in text for word in ("requests", "fastapi", "sqlalchemy", "delegation", "visual_asset_editor", "comfyui", "gpu"))


def test_no_canonical_harness_ir_is_compiled_or_mutated():
    service, repository, _, run_id, question = build_context()
    service.record(record_command(repository, run_id, question.package_id))
    run = repository.load_run(run_id)
    assert run.harness_ir_ref is None
    assert run.genesis_decision_memory_ref is not None
