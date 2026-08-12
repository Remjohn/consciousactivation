from cmf_builder.stage1.report import build_taxonomy_summary, build_validation_summary, build_operator_review_stub, assemble_contract_report

def test_build_taxonomy_summary():
    analyses = [
        {"resolutions": [{"status": "canonical"}, {"status": "novel_candidate"}]},
        {"resolutions": [{"status": "unknown"}]}
    ]
    summary = build_taxonomy_summary(analyses)
    assert summary["canonical_count"] == 1
    assert summary["variant_count"] == 0
    assert summary["novel_candidate_count"] == 1
    assert summary["unknown_count"] == 1
    assert len(summary["novel_candidates"]) == 1

def test_build_validation_summary():
    sem = {"technical_status": "PASS", "findings": [{"type": "sem"}]}
    ev = {"technical_status": "FAIL", "findings": [{"type": "ev"}]}
    summary = build_validation_summary(sem, ev)
    assert summary["semantic_status"] == "PASS"
    assert summary["evidence_status"] == "FAIL"
    assert len(summary["findings"]) == 2

def test_operator_review_stub():
    stub = build_operator_review_stub("h1", "PASS")
    assert stub["disposition"] is None

def test_assemble_contract_report():
    report = assemble_contract_report(
        "h1", {}, ["cp1"], {}, {}, {}
    )
    assert report["stage1_complete"] is False
    assert report["compiler_ready"] is False
    assert report["checkpoints_completed"] == ["cp1"]
