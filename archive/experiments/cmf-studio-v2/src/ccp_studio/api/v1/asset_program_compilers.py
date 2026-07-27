"""FastAPI adapter for Batch 2 asset and program compiler contracts."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.asset_program_compilers import (
    CarouselBuilderProgram,
    CarouselSlideLibrary,
    ContentSequenceProgram,
    InterviewBriefV2Plan,
    SingleImageSkiaScene,
    TwoDCharacterSceneProgram,
    VideoEditProgram,
)
from ccp_studio.services.asset_program_compiler_service import AssetProgramCompilerService


router = APIRouter(prefix="/api/v1/asset-program-compilers", tags=["asset-program-compilers"])
_asset_program_compiler_service = AssetProgramCompilerService()


class CarouselProgramRequest(BaseModel):
    source_context_refs: list[str]
    format_code: str = "CAR-JUX"
    slide_count: int = 5


class SingleImageSceneRequest(BaseModel):
    archetype_ref: str
    format_code: str = "SUPERVISUAL"


class VideoEditProgramRequest(BaseModel):
    interview_asset_contract_ref: str
    transcript_beat_map_ref: str
    content_format_targets: list[str] | None = None


class TwoDCharacterProgramRequest(BaseModel):
    character_ref: str
    brand_genesis_ref: str
    transcript_spans: list[dict]


class InterviewBriefV2Request(BaseModel):
    brand_context_ref: str
    audience_context_ref: str
    research_evidence_refs: list[str]


class ContentSequenceProgramRequest(BaseModel):
    ingredients: list[dict]
    relation_edges: list[dict] = []
    target_compilers: list[str] = []


def set_asset_program_compiler_service(service: AssetProgramCompilerService) -> None:
    global _asset_program_compiler_service
    _asset_program_compiler_service = service


def get_asset_program_compiler_service() -> AssetProgramCompilerService:
    return _asset_program_compiler_service


@router.post("/carousel-program", response_model=CarouselBuilderProgram)
def compile_carousel_program(
    request: CarouselProgramRequest,
    service: AssetProgramCompilerService = Depends(get_asset_program_compiler_service),
) -> CarouselBuilderProgram:
    library = service.compile_carousel_slide_library()
    sequence = service.compile_carousel_sequence(
        library=library,
        source_context_refs=request.source_context_refs,
        format_code=request.format_code,
        slide_count=request.slide_count,
    )
    program, _receipt = service.compile_carousel_builder_program(sequence_plan=sequence, library=library)
    return program


@router.get("/carousel-library", response_model=CarouselSlideLibrary)
def load_carousel_library(
    service: AssetProgramCompilerService = Depends(get_asset_program_compiler_service),
) -> CarouselSlideLibrary:
    return service.compile_carousel_slide_library()


@router.post("/single-image-scene", response_model=SingleImageSkiaScene)
def compile_single_image_scene(
    request: SingleImageSceneRequest,
    service: AssetProgramCompilerService = Depends(get_asset_program_compiler_service),
) -> SingleImageSkiaScene:
    route = service.route_single_image(archetype_ref=request.archetype_ref, format_code=request.format_code)
    service.plan_single_image_provider_job(route_decision=route)
    return service.compile_single_image_skia_scene(route_decision=route)


@router.post("/video-edit-program", response_model=VideoEditProgram)
def compile_video_edit_program(
    request: VideoEditProgramRequest,
    service: AssetProgramCompilerService = Depends(get_asset_program_compiler_service),
) -> VideoEditProgram:
    return service.compile_video_edit_program(
        interview_asset_contract_ref=request.interview_asset_contract_ref,
        transcript_beat_map_ref=request.transcript_beat_map_ref,
        content_format_targets=request.content_format_targets,  # type: ignore[arg-type]
    )


@router.post("/two-d-character-program", response_model=TwoDCharacterSceneProgram)
def compile_two_d_character_program(
    request: TwoDCharacterProgramRequest,
    service: AssetProgramCompilerService = Depends(get_asset_program_compiler_service),
) -> TwoDCharacterSceneProgram:
    _genesis, rig = service.compile_two_d_character_genesis(
        character_ref=request.character_ref,
        brand_genesis_ref=request.brand_genesis_ref,
    )
    return service.compile_two_d_character_scene_program(rig=rig, transcript_spans=request.transcript_spans)


@router.post("/interview-brief-v2", response_model=InterviewBriefV2Plan)
def compile_interview_brief_v2(
    request: InterviewBriefV2Request,
    service: AssetProgramCompilerService = Depends(get_asset_program_compiler_service),
) -> InterviewBriefV2Plan:
    return service.compile_interview_brief_v2(
        brand_context_ref=request.brand_context_ref,
        audience_context_ref=request.audience_context_ref,
        research_evidence_refs=request.research_evidence_refs,
    )


@router.post("/content-sequence-program", response_model=ContentSequenceProgram)
def compile_content_sequence_program(
    request: ContentSequenceProgramRequest,
    service: AssetProgramCompilerService = Depends(get_asset_program_compiler_service),
) -> ContentSequenceProgram:
    kernel = service.create_sequencing_kernel()
    inventory = service.build_expression_inventory(ingredients=request.ingredients, relation_edges=request.relation_edges)
    return service.compile_content_sequence_program(
        kernel=kernel,
        inventory=inventory,
        target_compilers=request.target_compilers or None,
    )
