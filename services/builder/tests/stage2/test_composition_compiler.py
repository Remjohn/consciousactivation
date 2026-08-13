import pytest
from cmf_builder.stage2.composition_compiler import CompositionCompiler
from cmf_builder.stage2.input_adapter import build_compiler_input


def test_composition_compiler_carousel():
    stage1_report = {
        "harness_id": "format02_c01",
        "stage1_complete": True,
        "input_receipt": {"source_zip_sha256": "1234567890abcdef" * 4},
        "wrong_reading_locks": [
            "Creator badge must remain locked across slides",
            "Headline text contrast ratio must be >= 4.5:1"
        ]
    }
    
    compiler_input = build_compiler_input(stage1_report)
    compiler = CompositionCompiler()
    spec = compiler.compile(compiler_input)
    
    assert spec["harness_definition_id"] == "format02_c01"
    assert spec["category_id"] == "carousels"
    assert spec["grammar_family"] == "CAROUSEL_SWIPE_PROGRESSION"
    assert len(spec["slide_sequence"]) >= 1
    assert spec["deduplication_hash"].startswith("sha256:")
    assert len(spec["wrong_reading_lock_constraints"]) == 2


def test_composition_compiler_supervisual():
    stage1_report = {
        "harness_id": "spv_test_01",
        "stage1_complete": True,
        "input_receipt": {"source_zip_sha256": "abcdef1234567890" * 4},
        "wrong_reading_locks": [
            "Text overlay must not obscure main visual"
        ]
    }
    
    compiler_input = build_compiler_input(stage1_report)
    compiler = CompositionCompiler()
    spec = compiler.compile(compiler_input)
    
    assert spec["harness_definition_id"] == "spv_test_01"
    assert spec["category_id"] == "supervisuals"
    assert spec["grammar_family"] == "SUPERVISUAL_STATIC_HIERARCHY"
    assert len(spec["slide_sequence"]) == 1
    assert spec["slide_sequence"][0]["slide_role"] == "single_frame"


def test_deduplication_hash_consistency():
    stage1_report = {
        "harness_id": "format02_c02",
        "stage1_complete": True,
        "input_receipt": {"source_zip_sha256": "0" * 64}
    }
    
    input1 = build_compiler_input(stage1_report)
    input2 = build_compiler_input(stage1_report)
    
    compiler = CompositionCompiler()
    spec1 = compiler.compile(input1)
    spec2 = compiler.compile(input2)
    
    assert spec1["deduplication_hash"] == spec2["deduplication_hash"]
