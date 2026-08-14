"""
Input Adapter for Stage 2 Visual Syntax Composition Compiler.
Converts Stage 1 Contract Reports and precomputed visual frame observations
into governed VisualSyntaxCompositionCompilerInput data structures.
"""

from typing import Dict, Any, List, Optional
from .spec_validator import VALID_PRIMITIVE_TYPES, VALID_ZONES, VALID_SLIDE_ROLES
from .composition_compiler import SpecificationValidationError


def derive_category_and_grammar(harness_id: str) -> tuple[str, str]:
    """Derive category_id and grammar_family from harness_id."""
    lowered = harness_id.lower()
    if "format04" in lowered or "format_04" in lowered:
        return "short_form_edited_video", "SHORT_FORM_EDITED_VIDEO_TIMELINE"
    if "spv" in lowered or "supervisual" in lowered or "super_visual" in lowered:
        return "supervisuals", "SUPERVISUAL_STATIC_HIERARCHY"
    return "carousels", "CAROUSEL_SWIPE_PROGRESSION"


def normalize_primitive_type(prim_type: str) -> str:
    """Ensure primitive_type maps to canonical taxonomy."""
    if prim_type in VALID_PRIMITIVE_TYPES:
        return prim_type
    
    mapping = {
        "text": "text_block",
        "headline": "text_block",
        "caption": "text_block",
        "paragraph": "text_block",
        "title_text": "text_block",
        "body_text": "text_block",
        "image": "image_region",
        "photo": "image_region",
        "picture": "image_region",
        "avatar": "badge",
        "logo": "badge",
        "brand": "badge",
        "number": "number_label",
        "step_number": "number_label",
        "index": "number_label",
        "plate": "caption_plate",
        "container": "caption_plate",
        "icons": "icon_row",
        "arrow": "callout_arrow",
        "diagram": "flow_diagram"
    }
    if prim_type in mapping:
        return mapping[prim_type]
    
    raise SpecificationValidationError(
        f"Unrecognized primitive_type: '{prim_type}'. Value is not in canonical primitive taxonomy or known aliases."
    )


def normalize_zone(zone: str) -> str:
    """Ensure zone maps to canonical container zones."""
    if zone in VALID_ZONES:
        return zone
    mapping = {
        "header": "header_zone",
        "top": "header_zone",
        "top_zone": "header_zone",
        "upper_zone": "header_zone",
        "subheading_zone": "header_zone",
        "logo_zone": "header_zone",
        "upper_left": "header_zone",
        "upper_right": "header_zone",
        "upper_center": "header_zone",
        "upper_photo": "hero_zone",
        "upper_grid": "hero_zone",
        "lower_grid": "hero_zone",
        "upper_illustration": "hero_zone",
        "lower_illustration": "hero_zone",
        "upper_portrait": "hero_zone",
        "lower_portrait": "hero_zone",
        "hero": "hero_zone",
        "hero_zone": "hero_zone",
        "body_zone": "hero_zone",
        "center": "hero_zone",
        "center_zone": "hero_zone",
        "center_left_zone": "hero_zone",
        "center_right_zone": "hero_zone",
        "left_zone": "hero_zone",
        "right_zone": "hero_zone",
        "left_card": "hero_zone",
        "right_card": "hero_zone",
        "left_graphic": "hero_zone",
        "right_graphic": "hero_zone",
        "left_diagram": "hero_zone",
        "right_diagram": "hero_zone",
        "card_zone": "hero_zone",
        "photo_zone": "hero_zone",
        "middle_zone": "hero_zone",
        "lower_photo": "footer_zone",
        "quote_banner": "hero_zone",
        "question_badge": "overlay_zone",
        "footer": "footer_zone",
        "bottom": "footer_zone",
        "bottom_zone": "footer_zone",
        "lower_zone": "footer_zone",
        "lower_center": "footer_zone",
        "lower_left": "footer_zone",
        "lower_right": "footer_zone",
        "lower_left_zone": "footer_zone",
        "lower_right_zone": "footer_zone",
        "overlay": "overlay_zone",
        "background": "full_bleed"
    }
    if zone in mapping:
        return mapping[zone]
    
    raise SpecificationValidationError(
        f"Unrecognized zone: '{zone}'. Value is not in canonical zone taxonomy or known aliases."
    )


def normalize_slide_role(role: str, category_id: str) -> str:
    """Normalize slide role string."""
    if category_id == "supervisuals":
        return "single_frame"
    
    if role in VALID_SLIDE_ROLES:
        return role
    
    mapping = {
        "title": "cover",
        "intro": "cover",
        "header": "cover",
        "item": "numbered_item",
        "step": "numbered_item",
        "body": "numbered_item",
        "content": "numbered_item",
        "cta": "closing_cta",
        "conclusion": "closing_cta",
        "closing": "closing_cta",
        "end": "closing_cta",
        "question": "closing_question",
        "comparison": "comparison_beat",
        "quote": "refrain_beat",
        "recap": "refrain_beat"
    }
    if role in mapping:
        return mapping[role]
    
    raise SpecificationValidationError(
        f"Unrecognized slide_role: '{role}'. Value is not in canonical slide_role taxonomy or known aliases."
    )


def build_compiler_input(
    stage1_report: Dict[str, Any],
    observations: Optional[List[Dict[str, Any]]] = None,
    wrong_reading_locks: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Assembles VisualSyntaxCompositionCompilerInput payload from Stage 1 report data.
    """
    harness_id = stage1_report.get("harness_id", "unknown_harness")
    category_id, grammar_family = derive_category_and_grammar(harness_id)
    
    locks = wrong_reading_locks or stage1_report.get("wrong_reading_locks", [])
    if not locks:
        locks = [
            f"Do not obscure primary visual elements in {harness_id}",
            "Creator badge must remain legible and cross-slide locked",
            "Text overlays must maintain contrast ratio minimum of 4.5:1 against background plates"
        ]
    
    raw_syntax = stage1_report.get("visual_syntax", [])
    raw_obs = observations or stage1_report.get("observations", [])

    obs_by_frame = {}
    for o in raw_obs:
        f_idx = o.get("frame_index", 0)
        obs_by_frame.setdefault(f_idx, []).append(o)

    slide_evidence = []

    if raw_syntax:
        for idx, slide_entry in enumerate(raw_syntax):
            f_idx = slide_entry.get("frame_index", idx)
            role = normalize_slide_role(slide_entry.get("slide_role", "single_frame" if category_id == "supervisuals" else "numbered_item"), category_id)
            
            frame_objects = obs_by_frame.get(f_idx, [])
            observed_prims = []

            if frame_objects:
                for p_idx, o in enumerate(frame_objects):
                    p_type = normalize_primitive_type(o.get("object_type", "text_block"))
                    zone = normalize_zone(o.get("zone_observation", "hero_zone"))
                    bbox = o.get("bbox_normalized", {})

                    height = bbox.get("height", 0.2) * 100.0 if "height" in bbox else 25.0
                    width = bbox.get("width", 0.8) * 100.0 if "width" in bbox else 80.0
                    y_anchor = bbox.get("y", 0.1) * 100.0 if "y" in bbox else 15.0

                    observed_prims.append({
                        "primitive_type": p_type,
                        "semantic_role": f"{p_type}_element",
                        "zone": zone,
                        "observed_height_pct": round(max(1.0, min(100.0, height)), 2),
                        "observed_width_pct": round(max(1.0, min(100.0, width)), 2),
                        "observed_y_anchor_pct": round(max(0.0, min(100.0, y_anchor)), 2),
                        "observed_font_size_px": 32 if p_type == "text_block" else (24 if p_type == "number_label" else 16),
                        "overlap_observed": False,
                        "cross_slide_stable": p_type == "badge"
                    })
            else:
                for p in slide_entry.get("primitives", []):
                    p_type = normalize_primitive_type(p.get("primitive_type", "text_block"))
                    zone = normalize_zone(p.get("zone", "hero_zone"))
                    observed_prims.append({
                        "primitive_type": p_type,
                        "semantic_role": f"{p_type}_element",
                        "zone": zone,
                        "observed_height_pct": 25.0,
                        "observed_width_pct": 80.0,
                        "observed_y_anchor_pct": 15.0,
                        "observed_font_size_px": 32,
                        "overlap_observed": False,
                        "cross_slide_stable": p_type == "badge"
                    })

            slide_evidence.append({
                "slide_index": idx,
                "slide_role": role,
                "specimen_ref": f"specimen:{harness_id}:frame_{f_idx}",
                "observed_primitives": observed_prims
            })
    else:
        # Single frame or default fallback if visual_syntax not populated
        role = "single_frame" if category_id == "supervisuals" else "cover"
        observed_prims = []
        for p_idx, o in enumerate(raw_obs):
            p_type = normalize_primitive_type(o.get("object_type", "text_block"))
            zone = normalize_zone(o.get("zone_observation", "hero_zone"))
            bbox = o.get("bbox_normalized", {})
            height = bbox.get("height", 0.2) * 100.0 if "height" in bbox else 25.0
            width = bbox.get("width", 0.8) * 100.0 if "width" in bbox else 80.0
            y_anchor = bbox.get("y", 0.1) * 100.0 if "y" in bbox else 15.0
            observed_prims.append({
                "primitive_type": p_type,
                "semantic_role": f"{p_type}_element",
                "zone": zone,
                "observed_height_pct": round(max(1.0, min(100.0, height)), 2),
                "observed_width_pct": round(max(1.0, min(100.0, width)), 2),
                "observed_y_anchor_pct": round(max(0.0, min(100.0, y_anchor)), 2),
                "observed_font_size_px": 32 if p_type == "text_block" else 16,
                "overlap_observed": False,
                "cross_slide_stable": p_type == "badge"
            })
            
        slide_evidence.append({
            "slide_index": 0,
            "slide_role": role,
            "specimen_ref": f"specimen:{harness_id}:frame_0",
            "observed_primitives": observed_prims or [
                {
                    "primitive_type": "text_block",
                    "semantic_role": "headline",
                    "zone": "hero_zone",
                    "observed_height_pct": 30.0,
                    "observed_width_pct": 80.0,
                    "observed_y_anchor_pct": 20.0,
                    "observed_font_size_px": 36,
                    "overlap_observed": False,
                    "cross_slide_stable": False
                }
            ]
        })

    if category_id == "supervisuals" and slide_evidence:
        all_prims = []
        seen = set()
        for s in slide_evidence:
            for p in s.get("observed_primitives", []):
                key = (p["primitive_type"], p["zone"])
                if key not in seen:
                    seen.add(key)
                    all_prims.append(p)
        slide_evidence = [
            {
                "slide_index": 0,
                "slide_role": "single_frame",
                "specimen_ref": f"specimen:{harness_id}:single_frame",
                "observed_primitives": all_prims or [
                    {
                        "primitive_type": "text_block",
                        "semantic_role": "headline",
                        "zone": "hero_zone",
                        "observed_height_pct": 30.0,
                        "observed_width_pct": 80.0,
                        "observed_y_anchor_pct": 20.0,
                        "observed_font_size_px": 36,
                        "overlap_observed": False,
                        "cross_slide_stable": False
                    }
                ]
            }
        ]

    input_receipt = stage1_report.get("input_receipt", {})
    source_zip_sha = input_receipt.get("source_zip_sha256_observed_now", input_receipt.get("source_zip_sha256", "0" * 64))

    activative_input_refs = {
        "source_premise_ref": f"source_premise:{harness_id}:v1.0.0",
        "identity_dna_ref": f"identity_dna:{harness_id}:{source_zip_sha[:16]}",
        "evidence_provenance_refs": [
            f"provenance:stage1_report:{harness_id}",
            f"provenance:zip:{source_zip_sha[:32]}"
        ]
    }

    return {
        "harness_definition_id": harness_id,
        "category_id": category_id,
        "grammar_family": grammar_family,
        "wrong_reading_locks": locks,
        "slide_evidence": slide_evidence,
        "canvas_dimensions": {
            "width_px": 1080,
            "height_px": 1080
        },
        "activative_input_refs": activative_input_refs
    }
