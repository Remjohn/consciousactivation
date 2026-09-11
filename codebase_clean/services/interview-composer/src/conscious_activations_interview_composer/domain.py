from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .canonical import (
    exact_keys,
    require_ref,
    require_string,
    require_url,
    semantic_id,
    sorted_unique_strings,
)
from .errors import ValidationError

MATRIX_SEED_FIELDS = (
    "psychological_role", "tension", "activation_direction_set",
    "pressure_path", "stance", "counteractivation_strategy", "smallest_commitment",
)  # matches TS-APP-COMPOSER-001 §6 MatrixOfEdgingSeed vocabulary

BLOCKED_REASON = (
    "planned_activative_intelligence_pack requires real, "
    "cross-validated activation_hypothesis_portfolio / "
    "activation_hypothesis / matrix_of_edging / "
    "psychological_role_tension_contract objects "
    "(HypothesisService.store_planned_pack, AIR). See "
    "SPEC_GAP_LEDGER.md GAP-007."
)


def make_guest_research_package(*, workspace_id: str, project_id: str,
                                guest_name: str, source_urls: list[str],
                                uploaded_documents: list[Mapping[str, Any]],
                                composer_authority: Mapping[str, str]) -> dict[str, Any]:
    core = {
        "workspace_id": require_string(workspace_id, "workspace_id"),
        "project_id": require_string(project_id, "project_id"),
        "guest_name": require_string(guest_name, "guest_name"),
        "source_urls": sorted_unique_strings(
            [require_url(u, "source_urls[]") for u in source_urls],
            "source_urls",
        ) if source_urls else [],
        "uploaded_documents": list(uploaded_documents),
        "composer_authority": dict(composer_authority),
    }
    core["research_package_id"] = semantic_id("ic:research", core)
    return core


def make_activative_interview_brief(*, research_package_ref: Mapping[str, str],
                                    brand_context_ref: Mapping[str, str] | None,
                                    voice_dna_ref: Mapping[str, str] | None,
                                    guest_name: str, tension_hypothesis: str,
                                    matrix_of_edging_seed: Mapping[str, str],
                                    planned_questions: list[Mapping[str, Any]],
                                    expression_targets: list[str],
                                    composer_authority: Mapping[str, str]) -> dict[str, Any]:
    seed = {}
    for f in MATRIX_SEED_FIELDS:
        val = matrix_of_edging_seed.get(f)
        if f == "activation_direction_set":
            # activation_direction_set is a list[str] — accept as-is or split
            if isinstance(val, list):
                seed[f] = [require_string(v, f"matrix_of_edging_seed.{f}[]") for v in val]
            elif isinstance(val, str):
                seed[f] = [require_string(v.strip(), f"matrix_of_edging_seed.{f}[]")
                           for v in val.split(",") if v.strip()]
            else:
                raise ValidationError(f"matrix_of_edging_seed.{f} must be a list of strings or a comma-separated string")
        else:
            seed[f] = require_string(val, f"matrix_of_edging_seed.{f}")
    exact_keys(matrix_of_edging_seed, set(MATRIX_SEED_FIELDS), "matrix_of_edging_seed")
    questions = []
    for i, q in enumerate(planned_questions):
        questions.append({
            "question_text": require_string(q.get("question_text"), f"planned_questions[{i}].question_text"),
            "activation_direction": require_string(q.get("activation_direction"), f"planned_questions[{i}].activation_direction"),
            "psychological_role": require_string(q.get("psychological_role"), f"planned_questions[{i}].psychological_role"),
        })
    if not questions:
        raise ValidationError("planned_questions must contain at least one question")
    core = {
        "research_package_ref": require_ref(research_package_ref, "research_package_ref"),
        "brand_context_ref": require_ref(brand_context_ref, "brand_context_ref") if brand_context_ref else None,
        "voice_dna_ref": require_ref(voice_dna_ref, "voice_dna_ref") if voice_dna_ref else None,
        "guest_name": require_string(guest_name, "guest_name"),
        "content_origin": "operator_supplied",
        "tension_hypothesis": require_string(tension_hypothesis, "tension_hypothesis"),
        "matrix_of_edging_seed": seed,
        "planned_questions": questions,
        "expression_targets": [require_string(t, "expression_targets[]") for t in expression_targets],
        "hypothesis_pipeline_status": {
            "status": "BLOCKED_PENDING_GAP_007",
            "iac_ref": None, "planned_aip_ref": None, "arm_receipt_ref": None,
            "blocked_reason": BLOCKED_REASON,
        },
        "composer_authority": dict(composer_authority),
    }
    core["brief_id"] = semantic_id("ic:brief", core)
    return core


def make_composer_session(*, brief_ref: Mapping[str, str],
                          relationship_state_ref: Mapping[str, str],
                          progression_ref: Mapping[str, str],
                          recording_date: str | None,
                          composer_authority: Mapping[str, str]) -> dict[str, Any]:
    core = {
        "brief_ref": require_ref(brief_ref, "brief_ref"),
        "relationship_state_ref": require_ref(relationship_state_ref, "relationship_state_ref"),
        "progression_ref": require_ref(progression_ref, "progression_ref"),
        "stage": "ENGAGED",
        "recording_date": recording_date,
        "composer_authority": dict(composer_authority),
    }
    core["session_id"] = semantic_id("ic:session", core)
    return core
