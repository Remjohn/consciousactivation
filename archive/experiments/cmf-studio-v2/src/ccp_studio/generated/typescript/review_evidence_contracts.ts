// Generated consumer-facing review evidence contracts for TS-CMF-012.

export type ApprovalBlockerCode =
  | "missing_source_reference"
  | "consent_incompatible"
  | "provenance_missing"
  | "voice_classification_missing"
  | "voice_eligibility_failed"
  | "evaluation_receipt_missing"
  | "evaluation_hard_failure"
  | "pwa_review_required";

export interface SourceReference {
  schema_version: "cmf.source_reference.v1";
  source_reference_id: string;
  source_artifact_id: string;
  transcript_revision_id?: string | null;
  start_seconds?: number | null;
  end_seconds?: number | null;
  claim_ref?: string | null;
}

export interface ApprovalBlocker {
  schema_version: "cmf.approval_blocker.v1";
  blocker_code: ApprovalBlockerCode;
  message: string;
  evidence_refs: string[];
  repair_action: string;
}

export interface ApprovalEvidenceView {
  schema_version: "cmf.approval_evidence_view.v1";
  approval_evidence_view_id: string;
  organization_id: string;
  brand_id: string;
  object_type: string;
  object_id: string;
  consent_record_version_id: string;
  source_references: SourceReference[];
  transcript_revision_ids: string[];
  evaluation_receipt_ids: string[];
  audio_mix_manifest_id?: string | null;
  file_provenance_refs: string[];
  blockers: ApprovalBlocker[];
  generated_at: string;
}
