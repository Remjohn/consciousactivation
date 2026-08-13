"""
Specification Validator for Stage 2 Visual Syntax Composition Compiler.
Validates input payloads and output VisualSyntaxCompositionSpec objects against governed JSON schemas.
"""

from typing import Dict, Any, List, Tuple, Optional
import re
import jsonschema


VALID_CATEGORIES = {"carousels", "supervisuals", "short_form_edited_video"}
VALID_GRAMMAR_FAMILIES = {"CAROUSEL_SWIPE_PROGRESSION", "SUPERVISUAL_STATIC_HIERARCHY", "SHORT_FORM_EDITED_VIDEO_TIMELINE"}
VALID_SLIDE_ROLES = {
    "cover", "numbered_item", "comparison_beat", "refrain_beat",
    "photo_beat", "grid_collage", "closing_question", "closing_cta",
    "closing_comparison", "testimonial", "single_frame"
}
VALID_ZONES = {"header_zone", "hero_zone", "footer_zone", "overlay_zone", "full_bleed"}
VALID_LAYOUT_MODES = {"vertical_stack", "horizontal_row", "overlay", "grid", "fill", "absolute"}
VALID_PRIMITIVE_TYPES = {
    "text_block", "image_region", "grid_cluster", "comparison_pair",
    "badge", "number_label", "icon_row", "caption_plate",
    "callout_arrow", "flow_diagram"
}
VALID_CONSTRAINT_TYPES = {
    "z_index_order", "non_overlap", "anchor_lock", "contrast_ratio",
    "presence_required", "absence_required", "pairing_required", "content_separation"
}
DEDUPLICATION_HASH_REGEX = re.compile(r"^sha256:[a-f0-9]{64}$")


class SpecificationValidationError(ValueError):
    """Raised when input or output validation fails structural or semantic rules."""
    def __init__(self, message: str, findings: Optional[List[Dict[str, Any]]] = None):
        super().__init__(message)
        self.findings = findings or []


def validate_input_payload(payload: Dict[str, Any]) -> bool:
    """Validate Stage 2 input payload against schema rules."""
    required = ["harness_definition_id", "category_id", "grammar_family", "wrong_reading_locks", "slide_evidence", "canvas_dimensions", "activative_input_refs"]
    missing = [f for f in required if f not in payload]
    if missing:
        raise SpecificationValidationError(f"Input payload missing required fields: {missing}")

    if payload["category_id"] not in VALID_CATEGORIES:
        raise SpecificationValidationError(f"Invalid category_id: {payload['category_id']}")

    if payload["grammar_family"] not in VALID_GRAMMAR_FAMILIES:
        raise SpecificationValidationError(f"Invalid grammar_family: {payload['grammar_family']}")

    if not isinstance(payload["wrong_reading_locks"], list) or len(payload["wrong_reading_locks"]) == 0:
        raise SpecificationValidationError("wrong_reading_locks must be a non-empty array")

    if not isinstance(payload["slide_evidence"], list) or len(payload["slide_evidence"]) == 0:
        raise SpecificationValidationError("slide_evidence must be a non-empty array")

    for slide in payload["slide_evidence"]:
        if slide.get("slide_role") not in VALID_SLIDE_ROLES:
            raise SpecificationValidationError(f"Invalid slide_role: {slide.get('slide_role')}")
        for p in slide.get("observed_primitives", []):
            if p.get("primitive_type") not in VALID_PRIMITIVE_TYPES:
                raise SpecificationValidationError(f"Invalid primitive_type: {p.get('primitive_type')}")
            if p.get("zone") not in VALID_ZONES:
                raise SpecificationValidationError(f"Invalid zone: {p.get('zone')}")

    return True


def validate_composition_spec(spec: Dict[str, Any]) -> Tuple[bool, List[Dict[str, Any]]]:
    """
    Validates a VisualSyntaxCompositionSpec output dictionary.
    Returns (is_valid, findings_list).
    """
    findings = []
    required_top = [
        "spec_id", "spec_version", "harness_definition_id", "category_id",
        "grammar_family", "slide_sequence", "cross_slide_anchors",
        "wrong_reading_lock_constraints", "deduplication_hash", "lineage"
    ]
    
    for field in required_top:
        if field not in spec:
            findings.append({
                "rule": "REQUIRED_FIELD_MISSING",
                "field": field,
                "severity": "ERROR",
                "message": f"Missing required top-level field '{field}'"
            })
            
    if findings:
        return False, findings

    if spec["category_id"] not in VALID_CATEGORIES:
        findings.append({
            "rule": "INVALID_CATEGORY",
            "severity": "ERROR",
            "message": f"Category '{spec['category_id']}' is not in allowed enum"
        })

    if spec["grammar_family"] not in VALID_GRAMMAR_FAMILIES:
        findings.append({
            "rule": "INVALID_GRAMMAR_FAMILY",
            "severity": "ERROR",
            "message": f"Grammar family '{spec['grammar_family']}' is not in allowed enum"
        })

    # Validate deduplication hash
    hash_val = spec.get("deduplication_hash", "")
    if not DEDUPLICATION_HASH_REGEX.match(hash_val):
        findings.append({
            "rule": "INVALID_DEDUPLICATION_HASH",
            "severity": "ERROR",
            "message": f"Deduplication hash '{hash_val}' does not match pattern sha256:[a-f0-9]{{64}}"
        })

    # Validate slide sequence
    slides = spec.get("slide_sequence", [])
    if not isinstance(slides, list) or len(slides) == 0:
        findings.append({
            "rule": "EMPTY_SLIDE_SEQUENCE",
            "severity": "ERROR",
            "message": "slide_sequence must be a non-empty list"
        })
    else:
        for idx, slide in enumerate(slides):
            role = slide.get("slide_role")
            if role not in VALID_SLIDE_ROLES:
                findings.append({
                    "rule": "INVALID_SLIDE_ROLE",
                    "severity": "ERROR",
                    "message": f"Slide {idx} has invalid role '{role}'"
                })
            
            zones = slide.get("zones", [])
            for z_idx, zone in enumerate(zones):
                z_type = zone.get("zone_type")
                if z_type not in VALID_ZONES:
                    findings.append({
                        "rule": "INVALID_ZONE_TYPE",
                        "severity": "ERROR",
                        "message": f"Slide {idx} zone {z_idx} has invalid zone_type '{z_type}'"
                    })
                
                prims = zone.get("primitives", [])
                for p_idx, p in enumerate(prims):
                    p_type = p.get("primitive_type")
                    if p_type not in VALID_PRIMITIVE_TYPES:
                        findings.append({
                            "rule": "INVALID_PRIMITIVE_TYPE",
                            "severity": "ERROR",
                            "message": f"Primitive '{p_type}' is not canonical"
                        })
                    
                    # Validate attribute ranges min <= max
                    attr_ranges = p.get("attribute_ranges", {})
                    for attr_name in ("height_pct", "width_pct", "font_size_px", "z_index_range"):
                        range_obj = attr_ranges.get(attr_name)
                        if range_obj and isinstance(range_obj, dict):
                            min_val = range_obj.get("min")
                            max_val = range_obj.get("max")
                            if min_val is not None and max_val is not None and min_val > max_val:
                                findings.append({
                                    "rule": "ATTRIBUTE_RANGE_INVERTED",
                                    "severity": "ERROR",
                                    "message": f"Primitive {p.get('primitive_id')} attribute '{attr_name}' has min ({min_val}) > max ({max_val})"
                                })

    # Validate wrong reading lock constraints
    lock_constraints = spec.get("wrong_reading_lock_constraints", [])
    if not isinstance(lock_constraints, list) or len(lock_constraints) == 0:
        findings.append({
            "rule": "EMPTY_LOCK_CONSTRAINTS",
            "severity": "ERROR",
            "message": "wrong_reading_lock_constraints must be a non-empty list"
        })
    else:
        for lock in lock_constraints:
            for c in lock.get("spatial_constraints", []):
                c_type = c.get("constraint_type")
                if c_type not in VALID_CONSTRAINT_TYPES:
                    findings.append({
                        "rule": "INVALID_CONSTRAINT_TYPE",
                        "severity": "ERROR",
                        "message": f"Constraint type '{c_type}' is not recognized"
                    })

    is_valid = len(findings) == 0
    return is_valid, findings
