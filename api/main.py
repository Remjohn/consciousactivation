from __future__ import annotations
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.config import load_config
from api.errors import not_found_handler, http_exception_handler, internal_error_handler
from api.routers import health

logger = logging.getLogger("conscious_activations.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    config = load_config()
    app.state.config = config

    db_path = config.ca_data_root

    # Pipeline
    from cmf_pipeline.application import PipelineApplication
    pipeline = PipelineApplication(database_path=db_path / "pipeline.db")
    pipeline.initialize()
    pipeline.load_default_development_candidates()
    app.state.pipeline = pipeline
    logger.info("pipeline service initialised: %s", db_path / "pipeline.db")

    # AIR
    from cmf_activative_intelligence.application import AirApplication
    air = AirApplication(database_path=db_path / "air.db")
    air.initialize()
    air.load_registries()
    app.state.air = air
    logger.info("air service initialised: %s", db_path / "air.db")

    # VAE
    from cmf_vae.application import VAEApplication
    vae = VAEApplication(
        database_path=db_path / "vae.db",
        storage_root=config.ca_media_root,
        delegation_root=config.ca_delegation_root,
    )
    vae.initialize()
    app.state.vae = vae
    logger.info("vae service initialised: %s", db_path / "vae.db")

    # Interview Expression
    from conscious_activations_interview_expression.application import InterviewExpressionApplication
    interview = InterviewExpressionApplication(database_path=db_path / "interview.db")
    interview.initialize()
    app.state.interview = interview
    logger.info("interview service initialised: %s", db_path / "interview.db")

    # Builder
    # TS-APP-API-001's Stage 3 sample code calls BuilderProductizationService()
    # with no arguments. The real class (services/builder/src/cmf_builder/
    # application/productization_service.py) takes keyword-only `repository`,
    # `compiler`, and `exporter` -- it has no default constructor. The correct
    # construction is the one cmf_builder's own CLI bootstrap uses
    # (cmf_builder/cli/bootstrap.py:build_local_service). The repository handle
    # is also kept on app.state so the health router can query it directly,
    # since BuilderProductizationService itself exposes no .status()/.health().
    from cmf_builder.adapters.sqlite_productization_repository import SQLiteProductizationRepository
    from cmf_builder.application.export_service import (
        DeterministicPortableExportService,
        PortableAtomicHarnessCompiler,
    )
    from cmf_builder.application.productization_service import BuilderProductizationService
    builder_repository = SQLiteProductizationRepository(db_path / "builder.db")
    builder = BuilderProductizationService(
        repository=builder_repository,
        compiler=PortableAtomicHarnessCompiler(),
        exporter=DeterministicPortableExportService(builder_repository),
    )
    app.state.builder = builder
    app.state.builder_repository = builder_repository
    logger.info("builder service initialised: %s", db_path / "builder.db")

    yield  # server runs here

    # --- shutdown ---
    logger.info("Conscious Activations API shutting down")
    # SQLite connections in these services are opened per-call (closing() context
    # managers), not held open for the process lifetime, so there is nothing to
    # explicitly close here.


app = FastAPI(
    title="Conscious Activations",
    version="0.1.0",
    description="One product. Interview to content batch.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)

app.add_exception_handler(404, not_found_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(500, internal_error_handler)

app.include_router(health.router, prefix="/api")
app.include_router(__import__("api.routers.air", fromlist=["router"]).router, prefix="/api/air", tags=["air"])
# Wave 2 routers registered here as each spec is implemented:
from api.routers import harnesses; app.include_router(harnesses.router, prefix="/api/harnesses", tags=["harnesses"])
from api.routers import interviews; app.include_router(interviews.router, prefix="/api/interviews", tags=["interviews"])  # noqa: E702
# app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])
# app.include_router(revisions.router, prefix="/api/revisions", tags=["revisions"])
# app.include_router(ship.router, prefix="/api/ship", tags=["ship"])
