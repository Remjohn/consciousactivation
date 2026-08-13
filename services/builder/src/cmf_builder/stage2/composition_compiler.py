"""
Composition Compiler for Stage 2 Visual Syntax Composition Compiler.
Transforms governed input payloads into VisualSyntaxCompositionSpec artifacts.
"""

from typing import Dict, Any, List, Optional, Tuple
from hashlib import sha256
import json

from .spec_validator import (
    validate_input_payload,
    validate_composition_spec,
    SpecificationValidationError
)


# Standard Zone Configurations by Slide Role
STANDARD_ROLE_ZONES: Dict[str, List[Dict[str, Any]]] = {
    "cover": [
        {"zone_type": "full_bleed", "layout_mode": "fill", "height_min": 100.0, "height_max": 100.0, "required": True, "accepts": ["image_region"]},
        {"zone_type": "overlay_zone", "layout_mode": "absolute", "height_min": 30.0, "height_max": 60.0, "required": True, "accepts": ["caption_plate", "text_block", "badge"]}
    ],
    "numbered_item": [
        {"zone_type": "header_zone", "layout_mode": "vertical_stack", "height_min": 15.0, "height_max": 30.0, "required": True, "accepts": ["number_label", "text_block"]},
        {"zone_type": "hero_zone", "layout_mode": "overlay", "height_min": 40.0, "height_max": 65.0, "required": True, "accepts": ["image_region", "grid_cluster", "text_block", "caption_plate"]},
        {"zone_type": "footer_zone", "layout_mode": "horizontal_row", "height_min": 10.0, "height_max": 20.0, "required": True, "accepts": ["badge", "icon_row", "text_block"]}
    ],
    "comparison_beat": [
        {"zone_type": "header_zone", "layout_mode": "vertical_stack", "height_min": 15.0, "height_max": 25.0, "required": False, "accepts": ["text_block"]},
        {"zone_type": "hero_zone", "layout_mode": "grid", "height_min": 50.0, "height_max": 75.0, "required": True, "accepts": ["comparison_pair", "image_region", "text_block"]},
        {"zone_type": "footer_zone", "layout_mode": "horizontal_row", "height_min": 10.0, "height_max": 20.0, "required": True, "accepts": ["badge", "text_block"]}
    ],
    "refrain_beat": [
        {"zone_type": "hero_zone", "layout_mode": "vertical_stack", "height_min": 60.0, "height_max": 85.0, "required": True, "accepts": ["text_block", "caption_plate"]},
        {"zone_type": "footer_zone", "layout_mode": "horizontal_row", "height_min": 10.0, "height_max": 20.0, "required": True, "accepts": ["badge"]}
    ],
    "photo_beat": [
        {"zone_type": "full_bleed", "layout_mode": "fill", "height_min": 100.0, "height_max": 100.0, "required": True, "accepts": ["image_region"]},
        {"zone_type": "overlay_zone", "layout_mode": "absolute", "height_min": 20.0, "height_max": 40.0, "required": True, "accepts": ["caption_plate", "text_block"]}
    ],
    "grid_collage": [
        {"zone_type": "header_zone", "layout_mode": "vertical_stack", "height_min": 15.0, "height_max": 25.0, "required": False, "accepts": ["text_block"]},
        {"zone_type": "hero_zone", "layout_mode": "grid", "height_min": 55.0, "height_max": 75.0, "required": True, "accepts": ["grid_cluster", "image_region"]},
        {"zone_type": "footer_zone", "layout_mode": "horizontal_row", "height_min": 10.0, "height_max": 20.0, "required": True, "accepts": ["badge"]}
    ],
    "closing_question": [
        {"zone_type": "hero_zone", "layout_mode": "vertical_stack", "height_min": 60.0, "height_max": 80.0, "required": True, "accepts": ["text_block"]},
        {"zone_type": "footer_zone", "layout_mode": "horizontal_row", "height_min": 10.0, "height_max": 20.0, "required": True, "accepts": ["badge", "icon_row"]}
    ],
    "closing_cta": [
        {"zone_type": "hero_zone", "layout_mode": "vertical_stack", "height_min": 50.0, "height_max": 75.0, "required": True, "accepts": ["text_block", "caption_plate"]},
        {"zone_type": "footer_zone", "layout_mode": "horizontal_row", "height_min": 15.0, "height_max": 25.0, "required": True, "accepts": ["badge", "icon_row"]}
    ],
    "single_frame": [
        {"zone_type": "header_zone", "layout_mode": "vertical_stack", "height_min": 15.0, "height_max": 30.0, "required": True, "accepts": ["text_block", "number_label"]},
        {"zone_type": "hero_zone", "layout_mode": "overlay", "height_min": 45.0, "height_max": 70.0, "required": True, "accepts": ["image_region", "grid_cluster", "text_block", "caption_plate"]},
        {"zone_type": "footer_zone", "layout_mode": "horizontal_row", "height_min": 10.0, "height_max": 20.0, "required": True, "accepts": ["badge", "icon_row", "text_block"]}
    ]
}


class CompositionCompiler:
    """
    Core Stage 2 Composition Compiler.
    Translates input evidence and wrong-reading locks into a VisualSyntaxCompositionSpec.
    """
    def __init__(self, skill_ref: str = "visual_syntax_composition_compiler@1.0.0"):
        self.skill_ref = skill_ref

    def compile(self, input_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes 9-step active compilation procedure.
        """
        # Step 1: Input Validation
        validate_input_payload(input_payload)

        # Step 2: Grammar Family Resolution
        category_id = input_payload["category_id"]
        grammar_family = input_payload["grammar_family"]

        if category_id not in ("carousels", "supervisuals"):
            harness_id = input_payload["harness_definition_id"]
            raw_lineage = input_payload["activative_input_refs"]
            return {
                "spec_id": f"visual_syntax_spec_{harness_id}_not_applicable",
                "spec_version": "1.0.0",
                "harness_definition_id": harness_id,
                "category_id": category_id,
                "grammar_family": grammar_family,
                "applicability": "NOT_APPLICABLE",
                "reason": f"Category '{category_id}' is not in scope for visual_syntax_composition_compiler",
                "slide_sequence": [],
                "cross_slide_anchors": [],
                "wrong_reading_lock_constraints": [],
                "deduplication_hash": f"sha256:{'0' * 64}",
                "lineage": {
                    "source_premise_ref": raw_lineage["source_premise_ref"],
                    "identity_dna_ref": raw_lineage["identity_dna_ref"],
                    "evidence_provenance_refs": raw_lineage["evidence_provenance_refs"],
                    "skill_ref": self.skill_ref
                }
            }

        expected_family = "SUPERVISUAL_STATIC_HIERARCHY" if category_id == "supervisuals" else "CAROUSEL_SWIPE_PROGRESSION"
        if grammar_family != expected_family:
            raise SpecificationValidationError(
                f"Grammar family mismatch for category '{category_id}': expected '{expected_family}', got '{grammar_family}'"
            )

        # Step 3: Slide Role Sequence Assembly
        slide_evidence = input_payload["slide_evidence"]
        sorted_evidence = sorted(slide_evidence, key=lambda x: x["slide_index"])
        
        if category_id == "supervisuals":
            if len(sorted_evidence) != 1 or sorted_evidence[0]["slide_role"] != "single_frame":
                raise SpecificationValidationError("Supervisuals category requires exactly one slide with role 'single_frame'")
        else:
            first_role = sorted_evidence[0]["slide_role"]
            if first_role not in ("cover", "single_frame"):
                sorted_evidence[0]["slide_role"] = "cover"

        # Step 4: Zone Configuration & Step 5: Attribute Range Computation
        slide_sequence = []
        cross_slide_candidates = {}

        for slide in sorted_evidence:
            s_idx = slide["slide_index"]
            s_role = slide["slide_role"]
            obs_prims = slide.get("observed_primitives", [])
            
            # Lookup standard zone configuration
            base_zones = STANDARD_ROLE_ZONES.get(s_role, STANDARD_ROLE_ZONES["numbered_item"])
            compiled_zones = []

            for z_config in base_zones:
                z_type = z_config["zone_type"]
                layout_mode = z_config["layout_mode"]
                accepts = z_config["accepts"]
                
                # Filter observed primitives matching zone or assignable
                matched_prims = []
                for p_idx, p in enumerate(obs_prims):
                    p_zone = p.get("zone")
                    p_type = p["primitive_type"]
                    
                    if p_zone == z_type or (p_zone is None and p_type in accepts):
                        # Step 5: Compute Attribute Ranges with tolerance
                        h_obs = float(p.get("observed_height_pct", 20.0))
                        w_obs = float(p.get("observed_width_pct", 80.0))
                        y_obs = float(p.get("observed_y_anchor_pct", 10.0))
                        font_obs = p.get("observed_font_size_px")

                        # Add tolerance margins (+/- 5% height/width, +/- 4px font)
                        h_min = max(5.0, round(h_obs - 5.0, 1))
                        h_max = min(100.0, round(h_obs + 5.0, 1))
                        w_min = max(10.0, round(w_obs - 5.0, 1))
                        w_max = min(100.0, round(w_obs + 5.0, 1))

                        is_anchor = p.get("cross_slide_stable", False) or (p_type == "badge")
                        anchor_mode = "cross_slide_locked" if is_anchor else ("static" if category_id == "supervisuals" else "per_slide_variable")
                        
                        prim_id = f"prim_{s_idx}_{z_type}_{p_idx}_{p_type}"
                        
                        attr_ranges = {
                            "height_pct": {"min": h_min, "max": h_max},
                            "width_pct": {"min": w_min, "max": w_max},
                            "z_index_range": {"min": 1 if p_type == "caption_plate" else (2 if p_type == "text_block" else 3), "max": 10},
                            "padding_px": {"min": 4, "max": 16},
                            "overlap_allowed": p.get("overlap_observed", False),
                            "color_constraint": "contrast_ratio_min_4.5:1"
                        }
                        
                        if font_obs is not None:
                            font_int = int(font_obs)
                            attr_ranges["font_size_px"] = {
                                "min": max(12, font_int - 4),
                                "max": font_int + 4
                            }
                            attr_ranges["font_weight"] = ["regular", "medium", "bold"] if font_int >= 28 else ["regular", "medium"]
                            attr_ranges["alignment"] = ["center", "left"] if font_int >= 32 else ["left"]

                        matched_prim_obj = {
                            "primitive_id": prim_id,
                            "primitive_type": p_type,
                            "semantic_role": p.get("semantic_role", f"{p_type}_element"),
                            "syntax_role": f"{z_type}:{p_type}",
                            "attribute_ranges": attr_ranges,
                            "anchor_mode": anchor_mode,
                            "why": f"Derived from specimen analysis frame {s_idx} observation for {p_type}",
                            "protected_properties": ["primitive_type", "anchor_mode"]
                        }
                        matched_prims.append(matched_prim_obj)

                        if is_anchor:
                            if p_type not in cross_slide_candidates:
                                cross_slide_candidates[p_type] = {
                                    "primitive_id": prim_id,
                                    "locked_properties": ["height_pct", "width_pct", "z_index_range", "color_constraint"],
                                    "slides": []
                                }
                            cross_slide_candidates[p_type]["slides"].append(s_idx)

                # Assemble zone if required or has primitives
                if matched_prims or z_config["required"]:
                    if not matched_prims:
                        # Add fallback primitive to satisfy schema
                        matched_prims.append({
                            "primitive_id": f"prim_{s_idx}_{z_type}_default",
                            "primitive_type": "text_block" if z_type != "full_bleed" else "image_region",
                            "semantic_role": "zone_placeholder",
                            "syntax_role": f"{z_type}:placeholder",
                            "attribute_ranges": {
                                "height_pct": {"min": z_config["height_min"], "max": z_config["height_max"]},
                                "width_pct": {"min": 20.0, "max": 100.0},
                                "z_index_range": {"min": 1, "max": 5},
                                "padding_px": {"min": 8, "max": 16},
                                "overlap_allowed": False
                            },
                            "anchor_mode": "static" if category_id == "supervisuals" else "per_slide_variable",
                            "why": f"Standard container primitive for {z_type}",
                            "protected_properties": ["primitive_type"]
                        })

                    compiled_zones.append({
                        "zone_type": z_type,
                        "layout_mode": layout_mode,
                        "height_range_pct": {"min": z_config["height_min"], "max": z_config["height_max"]},
                        "y_anchor_range_pct": {"min": 0.0, "max": 90.0},
                        "required": z_config["required"],
                        "max_children": 5,
                        "primitives": matched_prims
                    })

            slide_sequence.append({
                "slide_index": s_idx,
                "slide_role": s_role,
                "zones": compiled_zones
            })

        # Step 6: Wrong-Reading Lock Translation
        lock_constraints = []
        raw_locks = input_payload["wrong_reading_locks"]

        for lock_str in raw_locks:
            spatial_rules = []
            lowered_lock = lock_str.lower()

            if "badge" in lowered_lock or "creator" in lowered_lock or "attribution" in lowered_lock:
                spatial_rules.append({
                    "constraint_type": "anchor_lock",
                    "target_primitive": "badge",
                    "rule": "Creator badge anchor position and scale must remain locked across slides"
                })
            
            if "contrast" in lowered_lock or "legible" in lowered_lock or "obscure" in lowered_lock:
                spatial_rules.append({
                    "constraint_type": "contrast_ratio",
                    "target_primitive": "text_block",
                    "rule": "Text overlay contrast ratio must be >= 4.5:1 against background"
                })
                spatial_rules.append({
                    "constraint_type": "z_index_order",
                    "target_primitive": "caption_plate",
                    "rule": "caption_plate z-index must be below text_block and above hero_zone image"
                })
            
            if "pair" in lowered_lock or "wrong/right" in lowered_lock or "before/after" in lowered_lock:
                spatial_rules.append({
                    "constraint_type": "pairing_required",
                    "target_primitive": "comparison_pair",
                    "rule": "Comparison elements must maintain side-by-side or paired boundary"
                })

            # Default fallback rule for generic locks
            if not spatial_rules:
                spatial_rules.append({
                    "constraint_type": "presence_required",
                    "target_primitive": "text_block",
                    "rule": f"Governed structural lock: {lock_str}"
                })

            lock_constraints.append({
                "lock_text": lock_str,
                "spatial_constraints": spatial_rules
            })

        # Step 7: Cross-Slide Anchor Verification
        cross_slide_anchors = []
        total_slides = len(slide_sequence)

        for p_type, anchor_info in cross_slide_candidates.items():
            slides_covered = anchor_info["slides"]
            applies_mode = "all" if len(slides_covered) == total_slides else ("custom" if len(slides_covered) < total_slides else "all")
            
            anchor_entry = {
                "primitive_id": anchor_info["primitive_id"],
                "locked_properties": anchor_info["locked_properties"],
                "applies_to_slides": applies_mode
            }
            if applies_mode == "custom":
                anchor_entry["custom_slide_indices"] = slides_covered
                
            cross_slide_anchors.append(anchor_entry)

        # Step 8: Deduplication Hash Computation
        hash_payload = {
            "grammar_family": grammar_family,
            "slide_roles": [s["slide_role"] for s in slide_sequence],
            "zones": [
                [z["zone_type"] for z in s["zones"]] for s in slide_sequence
            ],
            "primitive_types": [
                [
                    [p["primitive_type"] for p in z["primitives"]]
                    for z in s["zones"]
                ]
                for s in slide_sequence
            ],
            "wrong_reading_locks": raw_locks
        }
        canonical_json = json.dumps(hash_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        dedup_digest = sha256(canonical_json).hexdigest()
        deduplication_hash = f"sha256:{dedup_digest}"

        # Step 9: Output Assembly
        harness_id = input_payload["harness_definition_id"]
        spec_id = f"visual_syntax_spec_{harness_id}_{dedup_digest[:16]}"
        
        raw_lineage = input_payload["activative_input_refs"]
        lineage = {
            "source_premise_ref": raw_lineage["source_premise_ref"],
            "identity_dna_ref": raw_lineage["identity_dna_ref"],
            "evidence_provenance_refs": raw_lineage["evidence_provenance_refs"],
            "skill_ref": self.skill_ref
        }

        spec = {
            "spec_id": spec_id,
            "spec_version": "1.0.0",
            "harness_definition_id": harness_id,
            "category_id": category_id,
            "grammar_family": grammar_family,
            "slide_sequence": slide_sequence,
            "cross_slide_anchors": cross_slide_anchors,
            "wrong_reading_lock_constraints": lock_constraints,
            "deduplication_hash": deduplication_hash,
            "lineage": lineage
        }

        # Validate against output schema
        is_valid, findings = validate_composition_spec(spec)
        if not is_valid:
            raise SpecificationValidationError("Compiled specification failed validation", findings)

        return spec
