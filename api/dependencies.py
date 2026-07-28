from __future__ import annotations
from fastapi import Request, WebSocket
from cmf_pipeline.application import PipelineApplication
from cmf_activative_intelligence.application import AirApplication
from cmf_vae.application import VAEApplication
from conscious_activations_interview_expression.application import InterviewExpressionApplication
from cmf_builder.application.productization_service import BuilderProductizationService
from cmf_builder.adapters.sqlite_productization_repository import SQLiteProductizationRepository

# Forward reference for type annotation only; import is deferred to lifespan()
from api.services.campaign_repository import CampaignRepository


def get_pipeline(request: Request) -> PipelineApplication:
    return request.app.state.pipeline


def get_pipeline_ws(websocket: WebSocket) -> PipelineApplication:
    return websocket.app.state.pipeline


def get_air(request: Request) -> AirApplication:
    return request.app.state.air


def get_vae(request: Request) -> VAEApplication:
    return request.app.state.vae


def get_interview(request: Request) -> InterviewExpressionApplication:
    return request.app.state.interview


def get_builder(request: Request) -> BuilderProductizationService:
    return request.app.state.builder


def get_builder_repository(request: Request) -> SQLiteProductizationRepository:
    """Builder has no `.status()`/`.health()` method of its own (unlike the other
    four services). The gateway keeps a direct handle on its repository so the
    health router can assemble a status snapshot without reaching into
    BuilderProductizationService's private attributes. See api/routers/health.py.
    """
    return request.app.state.builder_repository


def get_campaign_repository(request: Request) -> CampaignRepository:
    return request.app.state.campaign_repository


def get_studio_bridge(request: Request) -> "StudioBridge":
    """Return the shared StudioBridge bound at app startup (TS-APP-API-006).

    The import is local-only to avoid importing the studio_bridge module at
    module load — its only annotation use is the forward-quoted return type,
    keeping `api.dependencies` importable in environments where Node is not
    on PATH (e.g. unit-test shells that never call the bridge).
    """
    return request.app.state.studio_bridge


# Forward reference for the get_studio_bridge return type only; imported here
# (not at the top) so the dependency file stays importable without Node.
from api.services.studio_bridge import StudioBridge  # noqa: E402
