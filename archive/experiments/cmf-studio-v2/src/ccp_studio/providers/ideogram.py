"""Ideogram 4 provider adapter boundary for TS-CMF-038."""

from __future__ import annotations

from uuid import uuid4

from ccp_studio.contracts.composition import CompositionJob, IdeogramCompositionProviderResponse, stable_hash


class Ideogram4Adapter:
    provider_name = "ideogram_4"
    model_version = "ideogram_4"

    def __init__(self, *, analysis_override: dict | None = None):
        self.analysis_override = analysis_override or {}

    def submit_composition_job(self, job: CompositionJob) -> IdeogramCompositionProviderResponse:
        plate_hash = stable_hash(
            {
                "composition_job_id": job.composition_job_id,
                "prompt_hash": job.prompt_hash,
                "constraints": job.constraints.model_dump(mode="json"),
            }
        )
        analysis = {
            "text_space_score": 0.92,
            "identity_drift_score": 0.08,
            "baked_final_text_detected": False,
            "layerability_score": 0.87,
            "style_fit_score": 0.9,
            "visual_flow_score": 0.88,
            "boundary_notes": ["Composition plate leaves downstream final text and identity rebuild boundaries intact."],
        }
        analysis.update(self.analysis_override)
        return IdeogramCompositionProviderResponse(
            schema_version="cmf.ideogram_composition_provider_response.v1",
            provider_correlation_id=f"ideogram_4:{uuid4()}",
            plate_uri=f"object://{job.output_requirements.storage_prefix}/{job.composition_job_id}.png",
            plate_hash=plate_hash,
            model_version=self.model_version,
            response_metadata={"provider_name": self.provider_name, "purpose": job.purpose},
            analysis=analysis,
        )
