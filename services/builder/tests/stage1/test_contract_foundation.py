import pytest
import json
from pathlib import Path

from cmf_builder.stage1.semantic_validator import SemanticValidator
from cmf_builder.stage1.evidence_validator import EvidenceValidator
from cmf_builder.stage1.lifecycle import derive_stage1_complete, derive_compiler_ready
from cmf_builder.stage1.canonicalizer import compute_syntax_hash

def test_case1_primitive_type_leakage():
    validator = SemanticValidator()
    
    # Path to legacy fixtures
    congofash_path = Path(r"d:\Work\consciousactivation\tools\vision_analysis_output\CAR-JUX-Congofash-4-5-12_VISUAL_SYNTAX_ANALYSIS.json")
    viralpost_path = Path(r"d:\Work\consciousactivation\tools\vision_analysis_output\CAR-LST-Viralpost-3-4-8_VISUAL_SYNTAX_ANALYSIS.json")
    
    with open(congofash_path, "r", encoding="utf-8") as f:
        congofash_data = json.load(f)
    with open(viralpost_path, "r", encoding="utf-8") as f:
        viralpost_data = json.load(f)
        
    res_congo = validator.validate(congofash_data)
    assert res_congo.technical_status == "FAIL"
    assert any(f.error_code == "ROLE_PRIMITIVE_TYPE_MISMATCH" for f in res_congo.findings)

    res_viral = validator.validate(viralpost_data)
    assert res_viral.technical_status == "FAIL"
    assert any(f.error_code == "ROLE_PRIMITIVE_TYPE_MISMATCH" for f in res_viral.findings)

def test_case2_novel_role_allowed():
    validator = SemanticValidator()
    data = {
        "visual_observations": [{"object_id": "obs1"}],
        "all_slide_analyses": [
            {
                "candidate_slide_role": "some_novel_role",
                "taxonomy_state": "NOVEL_CANDIDATE",
                "evidence_refs": ["obs1"],
                "syntax_hash": compute_syntax_hash("some_novel_role", [], [], [])
            }
        ],
        "deduplication_summary": {
            "unique_slide_roles": [{"slide_role": "some_novel_role"}]
        }
    }
    res = validator.validate(data)
    assert res.technical_status == "REVIEW"
    assert not any(f.severity == "FAIL" for f in res.findings)
    assert any(f.error_code == "NOVEL_CANDIDATE" for f in res.findings)

def test_case3_novel_candidate_not_silently_canonical():
    validator = SemanticValidator()
    data = {
        "visual_observations": [{"object_id": "obs1"}],
        "all_slide_analyses": [
            {
                "candidate_slide_role": "some_novel_role",
                "taxonomy_state": "CANONICAL",
                "evidence_refs": ["obs1"],
                "syntax_hash": compute_syntax_hash("some_novel_role", [], [], [])
            }
        ],
        "deduplication_summary": {
            "unique_slide_roles": [{"slide_role": "some_novel_role"}]
        }
    }
    res = validator.validate(data)
    assert res.technical_status == "FAIL"
    assert any(f.error_code == "INVALID_CANDIDATE_PROMOTION" for f in res.findings)

def test_case4_duplicate_counts_must_agree():
    validator = SemanticValidator()
    hash1 = compute_syntax_hash("cover", [], [], [])
    hash2 = compute_syntax_hash("numbered_item", [], [], [])
    
    data = {
        "visual_observations": [{"object_id": "obs1"}],
        "all_slide_analyses": [
            {
                "candidate_slide_role": "cover",
                "taxonomy_state": "CANONICAL",
                "evidence_refs": ["obs1"],
                "syntax_hash": hash1
            },
            {
                "candidate_slide_role": "numbered_item",
                "taxonomy_state": "CANONICAL",
                "evidence_refs": ["obs1"],
                "syntax_hash": hash2
            }
        ],
        "deduplication_summary": {
            # Only one entry, but there are 2 distinct hashes
            "unique_slide_roles": [{"slide_role": "cover"}]
        }
    }
    res = validator.validate(data)
    assert res.technical_status == "FAIL"
    assert any(f.error_code == "DEDUP_COUNT_INCONSISTENT" for f in res.findings)

def test_case5_zone_primitive_incompatible():
    validator = SemanticValidator()
    hash_val = compute_syntax_hash("cover", [], [{"primitive_type": "text_block", "zone": "invalid_zone", "evidence_refs": ["obs1"]}], [])
    data = {
        "visual_observations": [{"object_id": "obs1"}],
        "all_slide_analyses": [
            {
                "candidate_slide_role": "cover",
                "taxonomy_state": "CANONICAL",
                "evidence_refs": ["obs1"],
                "primitives": [
                    {
                        "primitive_type": "text_block",
                        "zone": "invalid_zone",
                        "evidence_refs": ["obs1"]
                    }
                ],
                "syntax_hash": hash_val
            }
        ],
        "deduplication_summary": {
            "unique_slide_roles": [{"slide_role": "cover"}]
        }
    }
    res = validator.validate(data)
    assert res.technical_status == "FAIL"
    assert any(f.error_code == "ZONE_PRIMITIVE_INCOMPATIBLE" for f in res.findings)

def test_case6_anchor_claims_require_evidence():
    validator = SemanticValidator()
    hash_val = compute_syntax_hash("cover", [], [], [{"label": "logo"}])
    data = {
        "visual_observations": [{"object_id": "obs1"}],
        "all_slide_analyses": [
            {
                "candidate_slide_role": "cover",
                "taxonomy_state": "CANONICAL",
                "evidence_refs": ["obs1"],
                "anchor_elements": [
                    {
                        "label": "logo",
                        "evidence_refs": []
                    }
                ],
                "syntax_hash": hash_val
            }
        ],
        "deduplication_summary": {
            "unique_slide_roles": [{"slide_role": "cover"}]
        }
    }
    res = validator.validate(data)
    # The requirement: technical_status = REVIEW or FAIL
    assert res.technical_status in ("REVIEW", "FAIL")
    assert any(f.error_code == "UNSUPPORTED_ANCHOR_CLAIM" for f in res.findings)

def test_case7_unsupported_visual_claims():
    validator = SemanticValidator()
    hash_val = compute_syntax_hash("cover", [], [], [])
    data = {
        "visual_observations": [{"object_id": "obs1"}],
        "all_slide_analyses": [
            {
                "candidate_slide_role": "cover",
                "taxonomy_state": "CANONICAL",
                "evidence_refs": [], # missing evidence
                "syntax_hash": hash_val
            }
        ],
        "deduplication_summary": {
            "unique_slide_roles": [{"slide_role": "cover"}]
        }
    }
    res = validator.validate(data)
    assert res.technical_status != "PASS"
    assert any(f.error_code == "INSUFFICIENT_EVIDENCE" for f in res.findings)

def test_case8_valid_taxonomy_extension():
    validator = SemanticValidator()
    data = {
        "visual_observations": [{"object_id": "obs1"}],
        "all_slide_analyses": [
            {
                "candidate_slide_role": "brand_new_role",
                "taxonomy_state": "NOVEL_CANDIDATE",
                "evidence_refs": ["obs1"],
                "syntax_hash": compute_syntax_hash("brand_new_role", [], [], [])
            }
        ],
        "deduplication_summary": {
            "unique_slide_roles": [{"slide_role": "brand_new_role"}]
        }
    }
    res = validator.validate(data)
    assert res.technical_status == "REVIEW"
    
    # lifecycle allows STAGE1_COMPLETE on APPROVE
    assert derive_stage1_complete(res.technical_status, "APPROVE") is True

def test_case9_structurally_valid_json_with_inadequate_evidence():
    ev_validator = EvidenceValidator()
    syntax_analyses = [
        {
            "candidate_slide_role": "cover",
            "evidence_refs": ["bad_obs"],
        }
    ]
    observations = [{"object_id": "obs1"}]
    res = ev_validator.validate(syntax_analyses, observations)
    assert res.technical_status == "FAIL"
    assert any(f.error_code in ("INSUFFICIENT_EVIDENCE", "DANGLING_EVIDENCE_REF") for f in res.findings)

def test_case10_stage1_complete_gates():
    assert not derive_stage1_complete("PASS", "HOLD")
    assert not derive_stage1_complete("BLOCKED", "APPROVE")
    assert not derive_stage1_complete("FAIL", "APPROVE")
    assert derive_stage1_complete("REVIEW", "APPROVE")
    assert derive_stage1_complete("PASS", "APPROVE")

def test_case11_data_integrity_mismatch():
    validator = SemanticValidator()
    data = {
        "receipt": {
            "source_zip_sha256_recorded": "hashA",
            "source_zip_sha256_observed_now": "hashB"
        }
    }
    res = validator.validate(data)
    assert res.technical_status == "BLOCKED"
    assert any(f.error_code == "SOURCE_INTEGRITY_MISMATCH" for f in res.findings)

def test_case12_undocumented_pipeline_deviation():
    validator = SemanticValidator()
    data = {
        "receipt": {
            "deviation_from_documented_pipeline": True
        }
    }
    res = validator.validate(data)
    # The requirement: technical_status not affected (PASS if no other issues)
    assert res.technical_status == "PASS"
    assert any(f.error_code == "UNDOCUMENTED_PIPELINE_DEVIATION" and f.severity == "INFO" for f in res.findings)

