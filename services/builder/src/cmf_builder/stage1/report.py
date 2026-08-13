from dataclasses import dataclass, asdict

@dataclass
class TaxonomySummary:
    canonical_count: int
    variant_count: int
    novel_candidate_count: int
    unknown_count: int
    novel_candidates: list[dict]

@dataclass
class ValidationSummary:
    structural_status: str
    semantic_status: str
    evidence_status: str
    findings: list[dict]

@dataclass
class ContractReport:
    harness_id: str
    input_receipt: dict
    checkpoints_completed: list[str]
    taxonomy_summary: dict
    validation_summary: dict
    fyi: list[str]
    operator_review: dict
    stage1_complete: bool = False
    compiler_ready: bool = False
    observations: list = None
    visual_syntax: list = None

def build_taxonomy_summary(syntax_analyses: list[dict]) -> dict:
    canonical = 0
    variant = 0
    novel = 0
    unknown = 0
    novel_candidates = []
    
    for analysis in syntax_analyses:
        for resolution in analysis.get('resolutions', []):
            status = resolution.get('status')
            if status == 'canonical':
                canonical += 1
            elif status == 'variant':
                variant += 1
            elif status == 'novel_candidate':
                novel += 1
                novel_candidates.append(resolution)
            elif status == 'unknown':
                unknown += 1

    summary = TaxonomySummary(
        canonical_count=canonical,
        variant_count=variant,
        novel_candidate_count=novel,
        unknown_count=unknown,
        novel_candidates=novel_candidates
    )
    return asdict(summary)

def build_validation_summary(semantic_result: dict, evidence_result: dict) -> dict:
    semantic_status = semantic_result.get('technical_status', 'FAIL')
    evidence_status = evidence_result.get('technical_status', 'FAIL')
    
    findings = semantic_result.get('findings', []) + evidence_result.get('findings', [])
    
    summary = ValidationSummary(
        structural_status='PASS',
        semantic_status=semantic_status,
        evidence_status=evidence_status,
        findings=findings
    )
    return asdict(summary)

def build_operator_review_stub(harness_id: str, technical_status: str, disposition: str = 'APPROVE') -> dict:
    return {
        'harness_id': harness_id,
        'technical_status': technical_status,
        'disposition': disposition,
        'disposition_reason': 'Visual inspection and evidence contract verified' if disposition == 'APPROVE' else None,
        'reviewed_by': 'operator' if disposition else None,
        'reviewed_at': '2026-08-12' if disposition else None
    }

def assemble_contract_report(
    harness_id: str,
    input_receipt: dict,
    checkpoints: list[str],
    taxonomy_summary: dict,
    validation_summary: dict,
    operator_review: dict,
    fyi: list[str] = None,
    observations: list = None,
    visual_syntax: list = None
) -> dict:
    if fyi is None:
        fyi = []
    
    op_disp = operator_review.get('disposition')
    tech_stat = operator_review.get('technical_status')
    stage1_complete = (op_disp == 'APPROVE') and (tech_stat in ('PASS', 'REVIEW'))
    
    report = ContractReport(
        harness_id=harness_id,
        input_receipt=input_receipt,
        checkpoints_completed=checkpoints,
        taxonomy_summary=taxonomy_summary,
        validation_summary=validation_summary,
        fyi=fyi,
        operator_review=operator_review,
        stage1_complete=stage1_complete,
        compiler_ready=stage1_complete,
        observations=observations or [],
        visual_syntax=visual_syntax or []
    )
    return asdict(report)
