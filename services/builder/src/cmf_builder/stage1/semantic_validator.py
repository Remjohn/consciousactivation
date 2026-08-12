from dataclasses import dataclass
from typing import List
from .taxonomy import is_canonical_primitive, is_canonical_slide_role, is_canonical_zone, get_taxonomy_candidate_states
from .canonicalizer import compute_syntax_hash

@dataclass
class Finding:
    error_code: str
    severity: str
    detail: str

@dataclass
class ValidationResult:
    technical_status: str
    findings: List[Finding]

class SemanticValidator:
    def validate(self, analysis_data: dict) -> ValidationResult:
        findings: List[Finding] = []
        
        all_slides = analysis_data.get("all_slide_analyses", [])
        observations = analysis_data.get("visual_observations", [])
        observation_ids = [obs.get("object_id") for obs in observations if "object_id" in obs]
        
        if len(observation_ids) != len(set(observation_ids)):
            findings.append(Finding("DUPLICATE_ID", "FAIL", "Duplicate object_id in visual_observations."))
            
        observation_id_set = set(observation_ids)
        distinct_hashes = set()
        
        for slide in all_slides:
            slide_role = slide.get("candidate_slide_role")
            if slide_role:
                if not is_canonical_slide_role(slide_role) and is_canonical_primitive(slide_role):
                    findings.append(Finding("ROLE_PRIMITIVE_TYPE_MISMATCH", "FAIL", f"slide_role '{slide_role}' is a primitive_type."))
                
                # Check for NOVEL_CANDIDATE
                if not is_canonical_slide_role(slide_role) and not is_canonical_primitive(slide_role):
                    if slide.get("taxonomy_state") == "CANONICAL":
                        findings.append(Finding("INVALID_CANDIDATE_PROMOTION", "FAIL", f"NOVEL_CANDIDATE recorded as CANONICAL for {slide_role}."))
                    elif slide.get("taxonomy_state") == "NOVEL_CANDIDATE":
                        findings.append(Finding("NOVEL_CANDIDATE", "REVIEW", f"Novel candidate {slide_role} requires review."))
                
                evidence_refs = slide.get("evidence_refs", [])
                if not evidence_refs:
                    findings.append(Finding("INSUFFICIENT_EVIDENCE", "FAIL", "Slide inference has empty evidence_refs."))
                else:
                    for ref in evidence_refs:
                        if ref not in observation_id_set:
                            findings.append(Finding("DANGLING_EVIDENCE_REF", "FAIL", f"Dangling evidence_ref: {ref}"))
                            
            primitives = slide.get("primitives", [])
            for p in primitives:
                if isinstance(p, dict):
                    ptype = p.get("primitive_type")
                    if ptype and not is_canonical_primitive(ptype) and is_canonical_slide_role(ptype):
                        findings.append(Finding("PRIMITIVE_ROLE_TYPE_MISMATCH", "FAIL", f"primitive_type '{ptype}' is a slide_role."))
                        
                    zone = p.get("zone")
                    if zone and not is_canonical_zone(zone):
                        findings.append(Finding("ZONE_PRIMITIVE_INCOMPATIBLE", "FAIL", f"Zone '{zone}' not in registry."))
                        
                    p_evidence = p.get("evidence_refs", [])
                    if not p_evidence:
                        findings.append(Finding("INSUFFICIENT_EVIDENCE", "FAIL", "Primitive has empty evidence_refs."))
                    else:
                        for ref in p_evidence:
                            if ref not in observation_id_set:
                                findings.append(Finding("DANGLING_EVIDENCE_REF", "FAIL", f"Dangling evidence_ref: {ref}"))
                            
            anchors = slide.get("anchor_elements", [])
            for a in anchors:
                if isinstance(a, dict):
                    a_evidence = a.get("evidence_refs", [])
                    if not a_evidence:
                        findings.append(Finding("UNSUPPORTED_ANCHOR_CLAIM", "FAIL", "Anchor claim has empty evidence_refs."))
                    else:
                        for ref in a_evidence:
                            if ref not in observation_id_set:
                                findings.append(Finding("DANGLING_EVIDENCE_REF", "FAIL", f"Dangling evidence_ref: {ref}"))

                            
            syntax_hash = slide.get("syntax_hash")
            computed_hash = compute_syntax_hash(
                slide.get("candidate_slide_role", ""),
                slide.get("container_zones", []),
                primitives,
                anchors
            )
            if syntax_hash and syntax_hash != computed_hash:
                findings.append(Finding("SYNTAX_HASH_MISMATCH", "FAIL", "Recorded syntax_hash does not match computed syntax_hash."))
            if syntax_hash:
                distinct_hashes.add(syntax_hash)

        dedup_summary = analysis_data.get("deduplication_summary", {})
        unique_slide_roles = dedup_summary.get("unique_slide_roles", [])
        unique_layout_count = dedup_summary.get("unique_layout_count", len(unique_slide_roles))
        if "deduplication_summary" in analysis_data and dedup_summary:
            if unique_layout_count != len(distinct_hashes):
                findings.append(Finding("DEDUP_COUNT_INCONSISTENT", "FAIL", "Deduplication summary count inconsistent with distinct syntax_hashes."))
                
        for u in unique_slide_roles:
            role = u.get("slide_role")
            if role and not is_canonical_slide_role(role) and is_canonical_primitive(role):
                findings.append(Finding("ROLE_PRIMITIVE_TYPE_MISMATCH", "FAIL", f"Unique slide_role '{role}' is a primitive_type."))

        receipt = analysis_data.get("receipt", {})
        if "source_zip_sha256_recorded" in receipt and "source_zip_sha256_observed_now" in receipt:
            if receipt["source_zip_sha256_recorded"] != receipt["source_zip_sha256_observed_now"]:
                findings.append(Finding("SOURCE_INTEGRITY_MISMATCH", "BLOCKED", "Source zip sha256 mismatch."))
                
        if receipt.get("deviation_from_documented_pipeline") is True:
            findings.append(Finding("UNDOCUMENTED_PIPELINE_DEVIATION", "INFO", "Deviation from documented pipeline."))

        has_fail = any(f.severity == "FAIL" for f in findings)
        has_blocked = any(f.severity == "BLOCKED" for f in findings)
        has_review = any(f.severity == "REVIEW" for f in findings)
        
        if has_fail:
            status = "FAIL"
        elif has_blocked:
            status = "BLOCKED"
        elif has_review:
            status = "REVIEW"
        else:
            status = "PASS"
            
        return ValidationResult(technical_status=status, findings=findings)
