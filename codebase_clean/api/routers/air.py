from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from ca_contracts import utc_now_rfc3339

from api.dependencies import get_air
from api.errors import ErrorResponse
from api.schemas import air as schemas
from api.services import air_adapter, air_projection
from cmf_activative_intelligence.domain import AirValidationError
from cmf_activative_intelligence.repositories.air_repository import ObjectVersionConflict

router = APIRouter()


def _error(code: str, message: str, status: int) -> HTTPException:
    return HTTPException(status_code=status, detail=ErrorResponse(error_code=code, message=message, timestamp=utc_now_rfc3339()).model_dump())


@router.get("/hypotheses/{portfolio_id}", response_model=schemas.HypothesisPortfolioDetail)
def get_hypothesis_portfolio(portfolio_id: str, air=Depends(get_air)):
    try:
        portfolio = air_adapter.get_portfolio(air, portfolio_id)
    except air_adapter.PortfolioNotFound:
        raise _error("PORTFOLIO_NOT_FOUND", f"no activation_hypothesis_portfolio with id '{portfolio_id}'", 404)
    return air_projection.project_portfolio_detail(air, portfolio)


@router.post("/hypotheses/{portfolio_id}/select", response_model=schemas.HypothesisSelectionResponse)
def select_hypothesis(portfolio_id: str, body: schemas.HypothesisSelectionRequest, air=Depends(get_air)):
    try:
        result = air_adapter.select_hypothesis(air, portfolio_id, body.model_dump())
    except air_adapter.PortfolioNotFound:
        raise _error("PORTFOLIO_NOT_FOUND", f"no activation_hypothesis_portfolio with id '{portfolio_id}'", 404)
    except air_adapter.PortfolioNotOpen as exc:
        raise _error("PORTFOLIO_NOT_OPEN", f"portfolio_state is '{exc}', expected 'OPEN'", 409)
    except air_adapter.CandidateJudgmentsIncomplete as exc:
        raise _error("CANDIDATE_JUDGMENTS_INCOMPLETE", f"missing={sorted(exc.missing)} extra={sorted(exc.extra)}", 422)
    except air_adapter.UnknownCandidate as exc:
        raise _error("UNKNOWN_CANDIDATE", f"'{exc}' is not a candidate in this portfolio", 404)
    except air_adapter.SelectionNotSupportedByScores as exc:
        raise _error("SELECTION_NOT_SUPPORTED_BY_SCORES", f"comparison decided {exc.decision}, not a decisive win for '{body.selected_hypothesis_id}'; no writes were made past compare_portfolio", 409)
    except ObjectVersionConflict:
        raise _error("CONFLICT", "portfolio was modified concurrently; re-fetch and retry", 409)
    except AirValidationError as exc:
        raise _error("VALIDATION_ERROR", str(exc), 422)
    return {
        "portfolio": air_projection.project_portfolio_detail(air, air_adapter.get_portfolio(air, portfolio_id)),
        "decision": result["decision"],
        "stop_reason": result["stop_reason"],
        "selected_hypothesis_ref": result["selected_hypothesis_ref"],
        "comparison_ref": result["comparison_ref"],
        "stopping_receipt_ref": result["stopping_receipt_ref"],
        "planned_pack_ref": result["planned_pack_ref"],
        "promotion_ref": result["promotion_ref"],
    }


@router.get("/scripts/{script_id}", response_model=schemas.FinalScriptDetail)
def get_script(script_id: str, air=Depends(get_air)):
    try:
        script = air_adapter.get_script(air, script_id)
    except air_adapter.ScriptNotFound:
        raise _error("SCRIPT_NOT_FOUND", f"no final_script_package with id '{script_id}'", 404)
    return air_projection.project_script_detail(air, script)


@router.post("/scripts/{script_id}/approve", response_model=schemas.ScriptApprovalResponse)
def approve_script(script_id: str, body: schemas.ScriptApprovalRequest, air=Depends(get_air)):
    try:
        result = air_adapter.approve_script(air, script_id, body.model_dump())
    except air_adapter.ScriptNotFound:
        raise _error("SCRIPT_NOT_FOUND", f"no final_script_package with id '{script_id}'", 404)
    except air_adapter.ScriptAlreadyApproved:
        raise _error("ALREADY_APPROVED", f"'{script_id}' is already operator_approved; retry with the same idempotency_key if this was meant to be a replay", 409)
    except AirValidationError as exc:
        raise _error("VALIDATION_ERROR", str(exc), 422)
    return {
        "approval_ref": {k: result["approval"][k2] for k, k2 in (("object_id", "object_id"), ("version", "semantic_version"), ("sha256", "canonical_sha256"))},
        "decision": "APPROVE",
        "script": air_projection.project_script_detail(air, result["script"]),
    }


@router.post("/scripts/{script_id}/transfer-contract", response_model=schemas.TransferContractResponse)
def create_transfer_contract(script_id: str, body: schemas.TransferContractRequest, air=Depends(get_air)):
    try:
        contract = air_adapter.create_transfer_contract(air, script_id, body.model_dump())
    except air_adapter.ScriptNotFound:
        raise _error("SCRIPT_NOT_FOUND", f"no final_script_package with id '{script_id}'", 404)
    except air_adapter.ScriptNotApproved:
        raise _error("SCRIPT_NOT_APPROVED", f"final_script_package '{script_id}' has operator_approved=false; a transfer contract cannot be created until FR-APP-032 approval is recorded", 409)
    except AirValidationError as exc:
        raise _error("VALIDATION_ERROR", str(exc), 422)
    return {
        "contract_ref": {"object_id": contract["object_id"], "version": contract["semantic_version"], "sha256": contract["canonical_sha256"]},
        "final_script_ref": contract["payload"]["final_script_ref"],
    }


# ============================================================================
# Brand Genesis, Voice DNA, Visual DNA, Distillation, Semantic Territory (M27)
# ============================================================================

@router.post("/brand/context", response_model=schemas.BrandContextResponse)
def create_brand_context(body: schemas.BrandContextCreateRequest, air=Depends(get_air)):
    try:
        payload = {
            "brand_context_id": body.brand_context_id,
            "version": "1.0.0",
            "authority": body.authority.model_dump(),
            "lifecycle_state": "proposed",
            "epistemic_state": "operator_confirmed",
            "brand_genesis_session_ref": body.brand_genesis_session_ref.model_dump(),
            "identity_truths": body.identity_truths,
            "audience_relationship": body.audience_relationship,
            "positioning_tension": body.positioning_tension,
            "source_refs": [r.model_dump() for r in body.source_refs],
        }
        res = air.brand.store_brand_context(
            payload,
            idempotency_key=body.idempotency_key,
        )
        obj = res["object"]
        return {
            "brand_context_ref": {"object_id": obj["object_id"], "version": obj["semantic_version"], "sha256": obj["canonical_sha256"]},
            "brand_context_id": obj["payload"]["brand_context_id"],
            "lifecycle_state": obj["lifecycle_state"],
            "epistemic_state": obj["epistemic_state"],
            "identity_truths": obj["payload"]["identity_truths"],
            "audience_relationship": obj["payload"]["audience_relationship"],
            "positioning_tension": obj["payload"]["positioning_tension"],
            "source_refs": obj["payload"]["source_refs"],
        }
    except ObjectVersionConflict:
        raise _error("CONFLICT", "brand context was modified concurrently", 409)
    except (AirValidationError, ValueError) as exc:
        raise _error("VALIDATION_ERROR", str(exc), 422)


@router.get("/brand/context/{brand_id}", response_model=schemas.BrandContextResponse)
def get_brand_context(brand_id: str, air=Depends(get_air)):
    try:
        obj = air.brand.get_brand_context(brand_id)
        return {
            "brand_context_ref": {"object_id": obj.object_id, "version": obj.semantic_version, "sha256": obj.canonical_sha256},
            "brand_context_id": obj.payload.get("brand_context_id", obj.object_id),
            "lifecycle_state": obj.lifecycle_state,
            "epistemic_state": obj.epistemic_state,
            "identity_truths": obj.payload.get("identity_truths", []),
            "audience_relationship": obj.payload.get("audience_relationship", ""),
            "positioning_tension": obj.payload.get("positioning_tension", ""),
            "source_refs": obj.payload.get("source_refs", []),
        }
    except Exception:
        raise _error("BRAND_CONTEXT_NOT_FOUND", f"no brand_context_version with id '{brand_id}'", 404)


@router.post("/brand/voice-dna", response_model=schemas.VoiceDnaResponse)
def create_voice_dna(body: schemas.VoiceDnaCreateRequest, air=Depends(get_air)):
    try:
        payload = {
            "voice_dna_id": body.voice_dna_id,
            "version": "1.0.0",
            "authority": body.authority.model_dump(),
            "lifecycle_state": "proposed",
            "epistemic_state": "operator_confirmed",
            "brand_context_ref": body.brand_context_ref.model_dump(),
            "vocabulary_patterns": body.vocabulary_patterns,
            "rhythm_patterns": body.rhythm_patterns,
            "sentence_pressure_patterns": body.sentence_pressure_patterns,
            "stance_patterns": body.stance_patterns,
            "specificity_patterns": body.specificity_patterns,
            "metaphor_range": body.metaphor_range,
            "emotional_distance": body.emotional_distance,
            "prohibited_centroid_patterns": body.prohibited_centroid_patterns,
            "source_evidence_refs": [r.model_dump() for r in body.source_evidence_refs],
        }
        res = air.brand.store_voice_dna(
            payload,
            idempotency_key=body.idempotency_key,
        )
        obj = res["object"]
        return {
            "voice_dna_ref": {"object_id": obj["object_id"], "version": obj["semantic_version"], "sha256": obj["canonical_sha256"]},
            "voice_dna_id": obj["payload"]["voice_dna_id"],
            "brand_context_ref": obj["payload"]["brand_context_ref"],
            "lifecycle_state": obj["lifecycle_state"],
            "epistemic_state": obj["epistemic_state"],
            "vocabulary_patterns": obj["payload"]["vocabulary_patterns"],
            "rhythm_patterns": obj["payload"]["rhythm_patterns"],
            "sentence_pressure_patterns": obj["payload"]["sentence_pressure_patterns"],
            "stance_patterns": obj["payload"]["stance_patterns"],
            "specificity_patterns": obj["payload"]["specificity_patterns"],
            "metaphor_range": obj["payload"]["metaphor_range"],
            "emotional_distance": obj["payload"]["emotional_distance"],
            "prohibited_centroid_patterns": obj["payload"]["prohibited_centroid_patterns"],
            "source_evidence_refs": obj["payload"]["source_evidence_refs"],
        }
    except ObjectVersionConflict:
        raise _error("CONFLICT", "voice DNA was modified concurrently", 409)
    except (AirValidationError, ValueError) as exc:
        raise _error("VALIDATION_ERROR", str(exc), 422)


@router.get("/brand/voice-dna/{voice_id}", response_model=schemas.VoiceDnaResponse)
def get_voice_dna(voice_id: str, air=Depends(get_air)):
    try:
        obj = air.brand.get_voice_dna(voice_id)
        return {
            "voice_dna_ref": {"object_id": obj.object_id, "version": obj.semantic_version, "sha256": obj.canonical_sha256},
            "voice_dna_id": obj.payload.get("voice_dna_id", obj.object_id),
            "brand_context_ref": obj.payload.get("brand_context_ref", {}),
            "lifecycle_state": obj.lifecycle_state,
            "epistemic_state": obj.epistemic_state,
            "vocabulary_patterns": obj.payload.get("vocabulary_patterns", []),
            "rhythm_patterns": obj.payload.get("rhythm_patterns", []),
            "sentence_pressure_patterns": obj.payload.get("sentence_pressure_patterns", []),
            "stance_patterns": obj.payload.get("stance_patterns", []),
            "specificity_patterns": obj.payload.get("specificity_patterns", []),
            "metaphor_range": obj.payload.get("metaphor_range", []),
            "emotional_distance": obj.payload.get("emotional_distance", ""),
            "prohibited_centroid_patterns": obj.payload.get("prohibited_centroid_patterns", []),
            "source_evidence_refs": obj.payload.get("source_evidence_refs", []),
        }
    except Exception:
        raise _error("VOICE_DNA_NOT_FOUND", f"no voice_dna with id '{voice_id}'", 404)


@router.post("/brand/visual-dna", response_model=schemas.VisualDnaResponse)
def create_visual_dna(body: schemas.VisualDnaCreateRequest, air=Depends(get_air)):
    try:
        payload = {
            "visual_dna_id": body.visual_dna_id,
            "version": "1.0.0",
            "authority": body.authority.model_dump(),
            "lifecycle_state": "proposed",
            "epistemic_state": "operator_confirmed",
            "brand_context_ref": body.brand_context_ref.model_dump(),
            "real_life_reference_refs": [r.model_dump() for r in body.real_life_reference_refs],
            "subject_treatment": body.subject_treatment,
            "visual_temperature": body.visual_temperature,
            "materiality": body.materiality,
            "composition_tendencies": body.composition_tendencies,
            "negative_space_functions": body.negative_space_functions,
            "edge_behaviors": body.edge_behaviors,
            "typographic_posture": body.typographic_posture,
            "motion_character": body.motion_character,
            "prohibited_centroid_defaults": body.prohibited_centroid_defaults,
        }
        res = air.brand.store_visual_dna(
            payload,
            idempotency_key=body.idempotency_key,
        )
        obj = res["object"]
        return {
            "visual_dna_ref": {"object_id": obj["object_id"], "version": obj["semantic_version"], "sha256": obj["canonical_sha256"]},
            "visual_dna_id": obj["payload"]["visual_dna_id"],
            "brand_context_ref": obj["payload"]["brand_context_ref"],
            "real_life_reference_refs": obj["payload"]["real_life_reference_refs"],
            "subject_treatment": obj["payload"]["subject_treatment"],
            "visual_temperature": obj["payload"]["visual_temperature"],
            "materiality": obj["payload"]["materiality"],
            "composition_tendencies": obj["payload"]["composition_tendencies"],
            "negative_space_functions": obj["payload"]["negative_space_functions"],
            "edge_behaviors": obj["payload"]["edge_behaviors"],
            "typographic_posture": obj["payload"]["typographic_posture"],
            "motion_character": obj["payload"]["motion_character"],
            "prohibited_centroid_defaults": obj["payload"]["prohibited_centroid_defaults"],
        }
    except ObjectVersionConflict:
        raise _error("CONFLICT", "visual DNA was modified concurrently", 409)
    except (AirValidationError, ValueError) as exc:
        raise _error("VALIDATION_ERROR", str(exc), 422)


@router.get("/brand/visual-dna/{visual_id}", response_model=schemas.VisualDnaResponse)
def get_visual_dna(visual_id: str, air=Depends(get_air)):
    try:
        obj = air.brand.get_visual_dna(visual_id)
        return {
            "visual_dna_ref": {"object_id": obj.object_id, "version": obj.semantic_version, "sha256": obj.canonical_sha256},
            "visual_dna_id": obj.payload.get("visual_dna_id", obj.object_id),
            "brand_context_ref": obj.payload.get("brand_context_ref", {}),
            "real_life_reference_refs": obj.payload.get("real_life_reference_refs", []),
            "subject_treatment": obj.payload.get("subject_treatment", []),
            "visual_temperature": obj.payload.get("visual_temperature", []),
            "materiality": obj.payload.get("materiality", []),
            "composition_tendencies": obj.payload.get("composition_tendencies", []),
            "negative_space_functions": obj.payload.get("negative_space_functions", []),
            "edge_behaviors": obj.payload.get("edge_behaviors", []),
            "typographic_posture": obj.payload.get("typographic_posture", []),
            "motion_character": obj.payload.get("motion_character", []),
            "prohibited_centroid_defaults": obj.payload.get("prohibited_centroid_defaults", []),
        }
    except Exception:
        raise _error("VISUAL_DNA_NOT_FOUND", f"no visual_dna with id '{visual_id}'", 404)


@router.post("/brand/distillation", response_model=schemas.DistillationReceiptResponse)
def create_distillation_receipt(body: schemas.DistillationReceiptCreateRequest, air=Depends(get_air)):
    try:
        payload = {
            "receipt_id": body.receipt_id,
            "version": "1.0.0",
            "authority": body.authority.model_dump(),
            "lifecycle_state": "validated",
            "epistemic_state": "operator_confirmed",
            "layer": body.layer,
            "brand_context_ref": body.brand_context_ref.model_dump() if hasattr(body, "brand_context_ref") and body.brand_context_ref else None,
            "voice_dna_ref": body.voice_dna_ref.model_dump() if hasattr(body, "voice_dna_ref") and body.voice_dna_ref else None,
            "input_refs": [r.model_dump() for r in body.input_refs],
            "output_refs": [r.model_dump() for r in body.output_refs],
            "decisions": body.decisions,
            "edge_product_preserved": body.edge_product_preserved,
            "role_tension_preserved": body.role_tension_preserved,
            "voice_dna_preserved": body.voice_dna_preserved,
            "visual_dna_preserved": body.visual_dna_preserved,
            "rejection_refs": [r.model_dump() for r in body.rejection_refs],
        }
        # Filter None
        payload = {k: v for k, v in payload.items() if v is not None}
        res = air.brand.store_distillation_receipt(
            payload,
            idempotency_key=body.idempotency_key,
        )
        obj = res["object"]
        return {
            "receipt_ref": {"object_id": obj["object_id"], "version": obj["semantic_version"], "sha256": obj["canonical_sha256"]},
            "receipt_id": obj["payload"]["receipt_id"],
            "layer": obj["payload"]["layer"],
            "edge_product_preserved": obj["payload"]["edge_product_preserved"],
            "role_tension_preserved": obj["payload"]["role_tension_preserved"],
        }
    except ObjectVersionConflict:
        raise _error("CONFLICT", "distillation receipt was modified concurrently", 409)
    except (AirValidationError, ValueError) as exc:
        raise _error("VALIDATION_ERROR", str(exc), 422)


@router.post("/brand/distillation/synthesize", response_model=list[schemas.DistillationReceiptResponse])
def synthesize_distillation_receipts(body: schemas.DistillationSynthesizeRequest, air=Depends(get_air)):
    try:
        results = air.brand.synthesize_distillation_layers(
            receipt_id_prefix=body.receipt_id_prefix,
            brand_context_ref=body.brand_context_ref.model_dump(),
            voice_dna_ref=body.voice_dna_ref.model_dump(),
            input_evidence_refs=[r.model_dump() for r in body.input_evidence_refs],
            authority=body.authority.model_dump(),
            idempotency_prefix=body.idempotency_prefix,
        )
        responses = []
        for res in results:
            obj = res["object"]
            responses.append({
                "receipt_ref": {"object_id": obj["object_id"], "version": obj["semantic_version"], "sha256": obj["canonical_sha256"]},
                "receipt_id": obj["payload"]["receipt_id"],
                "layer": obj["payload"]["layer"],
                "edge_product_preserved": obj["payload"]["edge_product_preserved"],
                "role_tension_preserved": obj["payload"]["role_tension_preserved"],
            })
        return responses
    except ObjectVersionConflict:
        raise _error("CONFLICT", "distillation receipt was modified concurrently", 409)
    except (AirValidationError, ValueError) as exc:
        raise _error("VALIDATION_ERROR", str(exc), 422)


@router.post("/brand/semantic-territory", response_model=schemas.SemanticTerritoryResponse)
def derive_semantic_territory_endpoint(body: schemas.SemanticTerritoryRequest, air=Depends(get_air)):
    try:
        territory = air.brand.derive_semantic_territory(
            brand_context_ref=body.brand_context_ref.model_dump(),
            voice_dna_ref=body.voice_dna_ref.model_dump(),
            protected_source_refs=[r.model_dump() for r in body.protected_source_refs],
            wrong_reading_locks=body.wrong_reading_locks,
            prohibited_centroid_patterns=body.prohibited_centroid_patterns,
            authority=body.authority.model_dump(),
        )
        return territory
    except (AirValidationError, ValueError) as exc:
        raise _error("VALIDATION_ERROR", str(exc), 422)

