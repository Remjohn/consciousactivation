import pytest
from cmf_builder.stage2.spec_validator import (
    validate_input_payload,
    validate_composition_spec,
    SpecificationValidationError
)


def test_validate_input_payload_valid():
    payload = {
        "harness_definition_id": "format02_c01",
        "category_id": "carousels",
        "grammar_family": "CAROUSEL_SWIPE_PROGRESSION",
        "wrong_reading_locks": ["Badge must remain locked"],
        "slide_evidence": [
            {
                "slide_index": 0,
                "slide_role": "cover",
                "specimen_ref": "ref_0",
                "observed_primitives": [
                    {
                        "primitive_type": "text_block",
                        "semantic_role": "headline",
                        "zone": "header_zone"
                    }
                ]
            }
        ],
        "canvas_dimensions": {"width_px": 1080, "height_px": 1080},
        "activative_input_refs": {
            "source_premise_ref": "sp_1",
            "identity_dna_ref": "dna_1",
            "evidence_provenance_refs": ["prov_1"]
        }
    }
    assert validate_input_payload(payload) is True


def test_validate_input_payload_invalid_category():
    payload = {
        "harness_definition_id": "h1",
        "category_id": "invalid_cat",
        "grammar_family": "CAROUSEL_SWIPE_PROGRESSION",
        "wrong_reading_locks": ["lock1"],
        "slide_evidence": [{"slide_index": 0, "slide_role": "cover", "specimen_ref": "ref"}],
        "canvas_dimensions": {"width_px": 1080, "height_px": 1080},
        "activative_input_refs": {"source_premise_ref": "a", "identity_dna_ref": "b", "evidence_provenance_refs": ["c"]}
    }
    with pytest.raises(SpecificationValidationError, match="Invalid category_id"):
        validate_input_payload(payload)


def test_validate_composition_spec_valid():
    spec = {
        "spec_id": "spec_1",
        "spec_version": "1.0.0",
        "harness_definition_id": "format02_c01",
        "category_id": "carousels",
        "grammar_family": "CAROUSEL_SWIPE_PROGRESSION",
        "slide_sequence": [
            {
                "slide_index": 0,
                "slide_role": "cover",
                "zones": [
                    {
                        "zone_type": "header_zone",
                        "layout_mode": "vertical_stack",
                        "height_range_pct": {"min": 10.0, "max": 30.0},
                        "required": True,
                        "primitives": [
                            {
                                "primitive_id": "p1",
                                "primitive_type": "text_block",
                                "semantic_role": "headline",
                                "syntax_role": "header_zone:text_block",
                                "attribute_ranges": {
                                    "height_pct": {"min": 10.0, "max": 25.0},
                                    "width_pct": {"min": 20.0, "max": 80.0}
                                },
                                "anchor_mode": "static"
                            }
                        ]
                    }
                ]
            }
        ],
        "cross_slide_anchors": [],
        "wrong_reading_lock_constraints": [
            {
                "lock_text": "lock1",
                "spatial_constraints": [
                    {"constraint_type": "presence_required", "target_primitive": "text_block", "rule": "rule1"}
                ]
            }
        ],
        "deduplication_hash": "sha256:" + "a" * 64,
        "lineage": {
            "source_premise_ref": "sp",
            "identity_dna_ref": "dna",
            "evidence_provenance_refs": ["p1"],
            "skill_ref": "skill@1.0.0"
        }
    }
    is_valid, findings = validate_composition_spec(spec)
    assert is_valid is True
    assert len(findings) == 0
