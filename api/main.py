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
    pipeline.configure_visual_delegation(config.ca_delegation_root)
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

    # Campaigns
    from api.services.campaign_repository import CampaignRepository
    campaign_db_path = db_path / "campaigns" / "campaigns.sqlite3"
    campaign_repository = CampaignRepository(campaign_db_path)
    campaign_repository.initialize()
    app.state.campaign_repository = campaign_repository
    logger.info("campaigns service initialised: %s", campaign_db_path)

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

    # Studio bridge (TS-APP-API-006). A per-call Node subprocess bridge to the
    # built services/studio/dist/rpc.js entrypoint. The bridge object is cheap
    # to construct (no process is spawned until `call()` is invoked); it is held
    # on app.state purely so the dependency can return a shared instance.
    from api.services.studio_bridge import StudioBridge
    app.state.studio_bridge = StudioBridge(rpc_entrypoint=config.ca_studio_rpc_entrypoint)
    logger.info(
        "studio bridge initialised: %s", config.ca_studio_rpc_entrypoint
    )

    # Interview Composer (TS-APP-COMPOSER-001)
    from conscious_activations_interview_composer.application import InterviewComposerApplication
    composer = InterviewComposerApplication(database_path=db_path / "interview_composer.db")
    composer.initialize()
    app.state.composer = composer
    logger.info("interview composer service initialised: %s", db_path / "interview_composer.db")

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
from api.routers import campaigns; app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])
from api.websockets import pipeline_status; app.include_router(pipeline_status.router, prefix="/api", tags=["pipeline-status"])  # noqa: E702
# Wave 3 (TS-APP-API-006): Revision and ship routers
from api.routers import revisions; app.include_router(revisions.router, prefix="/api", tags=["revisions"])  # noqa: E702
from api.routers import ship; app.include_router(ship.router, prefix="/api", tags=["ship"])  # noqa: E702
# Wave 4 (TS-APP-COMPOSER-001): Interview Composer router
from api.routers import interview_composer; app.include_router(interview_composer.router, prefix="/api/interviews/compose", tags=["interview-composer"])  # noqa: E702
# CAE (TS-CAE-TEN-001): Versioned Tenancy and Workspace router
from api.routers import v1_tenancy; app.include_router(v1_tenancy.router, prefix="/api", tags=["tenancy-v1"])  # noqa: E702
# CAE (TS-CAE-PROG-001 / Mandate M14): Program Package Discovery and Registry router
from api.routers import programs; app.include_router(programs.router, prefix="/api/programs", tags=["programs"])  # noqa: E702
# CAE (Phase 4 Mandate M44 / F15): VAE Delegation and Visual Asset Runtime router
from api.routers import vae; app.include_router(vae.router, prefix="/api/vae", tags=["vae"])  # noqa: E702
# CAE (Phase 4 Mandate M45): Release / Ship / Outcome Runtime router
from api.routers import release_ship; app.include_router(release_ship.router, prefix="/api/release", tags=["release-ship"])  # noqa: E702


