from pathlib import Path

from ccp_studio.contracts.capability_preflight import PipelineId, PreflightPassStatus
from ccp_studio.contracts.golden_path_orchestrator import GoldenPathStatus
from ccp_studio.services.capability_preflight_service import CapabilityPreflightService
from ccp_studio.services.format02_golden_path_orchestrator_service import Format02GoldenPathOrchestratorService


FIXTURES_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "golden_path"


def test_format02_golden_path_preflight_allows_fake_runtime_without_provider_calls():
    report = CapabilityPreflightService().run_preflight(
        pipeline_id=PipelineId.FORMAT02_GOLDEN_PATH,
        artifact_store_configured=True,
        artifact_store_available=True,
    )

    assert report.pipeline_status.pass_status in {PreflightPassStatus.PASS, PreflightPassStatus.DEGRADED}
    assert report.provider_calls_executed is False
    assert report.runtime_calls_executed is False

    run = Format02GoldenPathOrchestratorService().run_fixture(fixtures_dir=FIXTURES_DIR)
    assert run.status == GoldenPathStatus.PASS
    assert run.output.fake_render_only is True
