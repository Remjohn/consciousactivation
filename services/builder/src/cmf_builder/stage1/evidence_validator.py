from .semantic_validator import ValidationResult, Finding

class EvidenceValidator:
    def validate(self, syntax_analyses: list[dict], observations: list[dict]) -> ValidationResult:
        findings = []
        observation_ids = {obs.get("object_id") for obs in observations if "object_id" in obs}
        
        for slide in syntax_analyses:
            evidence_refs = slide.get("evidence_refs", [])
            if not evidence_refs:
                findings.append(Finding("INSUFFICIENT_EVIDENCE", "FAIL", "Slide syntax analysis has empty evidence_refs."))
            else:
                for ref in evidence_refs:
                    if ref not in observation_ids:
                        findings.append(Finding("DANGLING_EVIDENCE_REF", "FAIL", f"Dangling evidence_ref: {ref}"))
                        
            primitives = slide.get("primitives", [])
            for p in primitives:
                p_evidence = p.get("evidence_refs", [])
                if not p_evidence:
                    findings.append(Finding("INSUFFICIENT_EVIDENCE", "FAIL", "Primitive has empty evidence_refs."))
                else:
                    for ref in p_evidence:
                        if ref not in observation_ids:
                            findings.append(Finding("DANGLING_EVIDENCE_REF", "FAIL", f"Dangling evidence_ref: {ref}"))
                            
            anchors = slide.get("anchor_elements", [])
            for a in anchors:
                a_evidence = a.get("evidence_refs", [])
                if not a_evidence:
                    findings.append(Finding("UNSUPPORTED_ANCHOR_CLAIM", "FAIL", "Anchor element has empty evidence_refs."))
                else:
                    for ref in a_evidence:
                        if ref not in observation_ids:
                            findings.append(Finding("DANGLING_EVIDENCE_REF", "FAIL", f"Dangling evidence_ref: {ref}"))
                            
        has_fail = any(f.severity == "FAIL" for f in findings)
        status = "FAIL" if has_fail else "PASS"
        return ValidationResult(technical_status=status, findings=findings)
