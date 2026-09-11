from __future__ import annotations
from fastapi import Request
from cmf_pipeline.application import PipelineApplication
from cmf_activative_intelligence.application import AirApplication
from cmf_vae.application import VAEApplication
from conscious_activations_interview_expression.application import InterviewExpressionApplication
from cmf_builder.application.productization_service import BuilderProductizationService
from cmf_builder.adapters.sqlite_productization_repository import SQLiteProductizationRepository


def get_pipeline(request: Request) -> PipelineApplication:
    return request.app.state.pipeline


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
