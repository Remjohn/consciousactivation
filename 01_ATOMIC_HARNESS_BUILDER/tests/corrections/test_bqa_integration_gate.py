from __future__ import annotations

from pathlib import Path

from tests.stories.st_07_04 import build_context, validation_command


def test_corrected_validation_remains_synthetic_portable_and_non_certifying() -> None:
    service, _, _, repository, _, run_id, _, definition = build_context(
        seed="BQA-integration"
    )
    receipt = service.validate(validation_command(run_id))
    report = repository.get_atomic_content_harness_validation_report(
        receipt.report_id
    )

    assert report is not None
    assert report.production_eligible is False
    assert report.certified is False
    assert report.synthetic_not_certifiable is True
    assert report.external_target_compatibility == "NOT_EVALUATED_EXTERNAL_TARGET_BRANCH"
    portable = definition.canonical_bytes() + report.canonical_bytes()
    assert b"D:/" not in portable
    assert b"D:\\" not in portable


def test_bounded_correction_adds_no_production_source_module() -> None:
    root = Path(__file__).resolve().parents[2]
    source_files = {
        path.relative_to(root).as_posix()
        for path in (root / "src/cmf_builder").rglob("*.py")
    }
    assert not any("correction" in path for path in source_files)
