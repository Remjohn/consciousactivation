from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from cmf_builder.domain.constitutional_validation import (
    AUTHORITY_ORDER,
    BUILDER_PRD_AMENDMENT_PATH,
    BUILDER_PRD_AMENDMENT_SHA256,
    CONSTITUTION_PATH,
    CONSTITUTION_SHA256,
    FORBIDDEN_BEHAVIORS,
    HARD_GATES,
    POLICY_PATH,
    POLICY_SHA256,
    RICH_LINEAGE_KEYS,
    ConstitutionalPolicyInvalid,
    ConstitutionalPrecedencePolicy,
)


_REQUIRED_POLICY_FRAGMENTS = (
    "schema_version: cmf-builder-constitutional-precedence/v1",
    "status: ACCEPTED_CORRECTED_V1_2_OVERLAY",
    "version: 1.1.0",
    f"path: {CONSTITUTION_PATH}",
    f"sha256: {CONSTITUTION_SHA256}",
    f"amendment: {BUILDER_PRD_AMENDMENT_PATH}",
    f"amendment_sha256: {BUILDER_PRD_AMENDMENT_SHA256}",
    "action: BLOCK_AND_EMIT_DECISION_REQUEST",
    "hard_gates: [HG-001, HG-004, HG-005, HG-015]",
    "law: Visual Syntax First",
    "law: Activation First",
    "rich_object_references_required: true",
    "frozen_versions_required: true",
    "required_rich_refs: [identity_dna_ref, context_premise_ref, resonance_ref, matrix_of_edging_ref, activative_intelligence_pack_ref]",
    "builder: [compile, validate, preserve_lineage, emit_capsule_and_handoff]",
    "builder_exclusions: [interview_execution, visual_asset_editor_runtime, delegation_protocol_runtime, identity_dna_merge]",
)


class FileConstitutionalPolicyRepository:
    """Read the one closed policy and verify its referenced canonical authorities."""

    def __init__(self, root: Path) -> None:
        self._root = root.resolve()

    def load(
        self, relative_path: str, expected_sha256: str
    ) -> ConstitutionalPrecedencePolicy:
        if relative_path != POLICY_PATH or expected_sha256 != POLICY_SHA256:
            raise ConstitutionalPolicyInvalid(
                "Only the governed hash-pinned precedence policy may be loaded.",
                relative_path=relative_path,
                expected_sha256=expected_sha256,
            )
        text = self._read_verified(relative_path, expected_sha256).decode("utf-8")
        missing = tuple(
            fragment for fragment in _REQUIRED_POLICY_FRAGMENTS if fragment not in text
        )
        order_positions = tuple(text.find(f"- {item}") for item in AUTHORITY_ORDER)
        if missing or any(position < 0 for position in order_positions) or order_positions != tuple(
            sorted(order_positions)
        ):
            raise ConstitutionalPolicyInvalid(
                "The pinned policy cannot be projected into the accepted typed contract.",
                missing_fragments=missing,
            )
        self._read_verified(CONSTITUTION_PATH, CONSTITUTION_SHA256)
        self._read_verified(
            BUILDER_PRD_AMENDMENT_PATH, BUILDER_PRD_AMENDMENT_SHA256
        )
        policy = ConstitutionalPrecedencePolicy(
            source_path=POLICY_PATH,
            source_hash=POLICY_SHA256,
            constitution_path=CONSTITUTION_PATH,
            constitution_version="1.1.0",
            constitution_hash=CONSTITUTION_SHA256,
            builder_prd_amendment_path=BUILDER_PRD_AMENDMENT_PATH,
            builder_prd_version="1.2",
            builder_prd_amendment_hash=BUILDER_PRD_AMENDMENT_SHA256,
            authority_order=AUTHORITY_ORDER,
            conflict_action="BLOCK_AND_EMIT_DECISION_REQUEST",
            hard_gates=HARD_GATES,
            forbidden_behaviors=FORBIDDEN_BEHAVIORS,
            harness_development_law="Visual Syntax First",
            runtime_law="Activation First",
            rich_lineage_keys=RICH_LINEAGE_KEYS,
            builder_ownership=(
                "compile",
                "validate",
                "preserve_lineage",
                "emit_capsule_and_handoff",
            ),
            builder_exclusions=(
                "interview_execution",
                "visual_asset_editor_runtime",
                "delegation_protocol_runtime",
                "identity_dna_merge",
            ),
        )
        policy.validate()
        return policy

    def _read_verified(self, relative_path: str, expected_sha256: str) -> bytes:
        if not relative_path or Path(relative_path).is_absolute():
            raise ConstitutionalPolicyInvalid("Authority path must be repository-relative.")
        candidate = (self._root / relative_path).resolve()
        try:
            candidate.relative_to(self._root)
        except ValueError as error:
            raise ConstitutionalPolicyInvalid(
                "Authority path escapes the repository root.", relative_path=relative_path
            ) from error
        try:
            content = candidate.read_bytes()
        except OSError as error:
            raise ConstitutionalPolicyInvalid(
                "A canonical authority source is unavailable.", relative_path=relative_path
            ) from error
        observed = sha256(content).hexdigest()
        if observed != expected_sha256:
            raise ConstitutionalPolicyInvalid(
                "A canonical authority source hash drifted.",
                relative_path=relative_path,
                expected_sha256=expected_sha256,
                observed_sha256=observed,
            )
        return content
