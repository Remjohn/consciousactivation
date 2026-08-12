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
    stage1_complete: bool
    compiler_ready: bool

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

def build_operator_review_stub(harness_id: str, technical_status: str) -> dict:
    return {
        'harness_id': harness_id,
        'technical_status': technical_status,
        'disposition': None,
        'disposition_reason': None,
        'reviewed_by': None,
        'reviewed_at': None
    }

def assemble_contract_report(
    harness_id: str,
    input_receipt: dict,
    checkpoints: list[str],
    taxonomy_summary: dict,
    validation_summary: dict,
    operator_review: dict,
    fyi: list[str] = None
) -> dict:
    if fyi is None:
        fyi = []
    
    report = ContractReport(
        harness_id=harness_id,
        input_receipt=input_receipt,
        checkpoints_completed=checkpoints,
        taxonomy_summary=taxonomy_summary,
        validation_summary=validation_summary,
        fyi=fyi,
        operator_review=operator_review,
        stage1_complete=False,
        compiler_ready=False
    )
    return asdict(report)
