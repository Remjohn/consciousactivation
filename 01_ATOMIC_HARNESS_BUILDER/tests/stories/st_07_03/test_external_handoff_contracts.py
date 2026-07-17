from __future__ import annotations

from dataclasses import replace
from hashlib import sha256

import pytest

from cmf_builder.domain.category_syntax import GovernedRef
from cmf_builder.domain.external_handoff_contracts import (
    DELEGATION_TARGET,
    DELEGATION_VERSION,
    EXTERNAL_VALIDATION_PENDING,
    VAE_TARGET,
    ExternalHandoffInput,
    HandoffContractRejected,
    HandoffAuthorityRejected,
    SourceProvenance,
    SourceProvenanceRejected,
    WrongReadingLock,
    WrongReadingLockRejected,
    compile_external_handoff,
    ST_07_02_COMPLETION_RECEIPT_SHA256,
    SYNTHETIC_DEFINITION_ID,
    SYNTHETIC_DEFINITION_SHA256,
    SYNTHETIC_DEFINITION_RECEIPT_ID,
    SYNTHETIC_DEFINITION_RECEIPT_SHA256,
    structural_lineage_fixture_ref,
    interview_structural_placeholder_ref,
    OD_STRUCTURAL_LINEAGE_MANIFEST_HASH,
    STRUCTURAL_LINEAGE_CLASSIFICATION,
    INTERVIEW_PLACEHOLDER_CLASSIFICATION,
)


ROLES = (
    "activative_intelligence_pack",
    "identity_dna",
    "context_premise",
    "resonance_map",
    "matrix_edge_product",
    "activative_call",
    "activation_contract",
    "visual_semantic_pack",
    "visual_narrative_program",
    "feature_contract",
    "somatic_route",
    "composition_intent",
)


def ref(role: str, suffix: str = "v1", *, authority: str = "handoff-code") -> GovernedRef:
    return GovernedRef(
        object_id=f"{role}-{suffix}",
        version="1.0.0",
        sha256=sha256(f"{role}:{suffix}:{authority}".encode()).hexdigest(),
        authority=authority,
        lineage_role=role,
    )


def lock(lock_id: str = "preserve-human-truth", *, level: int = 2, scopes=("/meaning",)) -> WrongReadingLock:
    return WrongReadingLock(
        lock_id=lock_id,
        statement="Do not invent or weaken human-owned truth.",
        meaning_hash=f"sha256:{sha256(lock_id.encode()).hexdigest()}",
        scope_paths=tuple(scopes),
        enforcement_level=level,
    )


def handoff_input(
    target_id: str = VAE_TARGET,
    *,
    builder_source: str = "Public Comment",
    lineage=None,
    locks=None,
    parent_locks=(),
) -> ExternalHandoffInput:
    return ExternalHandoffInput(
        request_id=f"request-{target_id}",
        request_version="1.0.0",
        target_id=target_id,
        run_ref=ref("builder_run"),
        atomic_harness_definition_ref=GovernedRef(
            object_id=SYNTHETIC_DEFINITION_ID,
            version="1.0.0",
            sha256=SYNTHETIC_DEFINITION_SHA256,
            authority="Atomic Harness Builder",
            lineage_role="atomic_harness_definition",
        ),
        atomic_harness_definition_receipt_ref=GovernedRef(
            object_id=SYNTHETIC_DEFINITION_RECEIPT_ID,
            version="1.0.0",
            sha256=SYNTHETIC_DEFINITION_RECEIPT_SHA256,
            authority="Atomic Harness Builder",
            lineage_role="atomic_harness_definition_receipt",
        ),
        st_07_02_completion_receipt_sha256=ST_07_02_COMPLETION_RECEIPT_SHA256,
        source=SourceProvenance(builder_source, ref("source_provenance")),
        semantic_lineage=(
            tuple(structural_lineage_fixture_ref(role) for role in ROLES)
            if lineage is None
            else tuple(lineage)
        ),
        wrong_reading_locks=(lock(),) if locks is None else tuple(locks),
        inherited_parent_locks=tuple(parent_locks),
        authority_ref=ref("handoff_authority"),
        local_contract_pin=(
            "builder-local-vae-interface/v1" if target_id == VAE_TARGET else DELEGATION_VERSION
        ),
    )


@pytest.mark.parametrize("target_id", (VAE_TARGET, DELEGATION_TARGET))
def test_distinct_external_target_requests_are_deterministic_and_uncertified(target_id: str) -> None:
    first = compile_external_handoff(handoff_input(target_id))
    second = compile_external_handoff(handoff_input(target_id))
    assert first.canonical_bytes == second.canonical_bytes
    assert first.request_hash == second.request_hash
    assert first.target_id == target_id
    assert first.external_compatibility == EXTERNAL_VALIDATION_PENDING
    assert first.production_ready is False and first.certified is False


def test_all_required_activative_lineage_remains_structured() -> None:
    result = compile_external_handoff(handoff_input())
    assert set(ROLES).issubset({item.lineage_role for item in result.semantic_lineage})
    assert not {"notes", "generic_notes"}.intersection(
        item.lineage_role for item in result.semantic_lineage
    )
    assert result.structural_lineage_manifest_hash == OD_STRUCTURAL_LINEAGE_MANIFEST_HASH
    assert result.structural_lineage_classification == STRUCTURAL_LINEAGE_CLASSIFICATION
    with pytest.raises(HandoffContractRejected, match="Missing required structured lineage"):
        compile_external_handoff(
            handoff_input(lineage=tuple(structural_lineage_fixture_ref(role) for role in ROLES[:-1]))
        )


def test_interview_expression_requires_reaction_and_expression_provenance() -> None:
    with pytest.raises(HandoffContractRejected, match="Reaction Receipt"):
        compile_external_handoff(handoff_input(builder_source="Interview Expression"))
    lineage = tuple(structural_lineage_fixture_ref(role) for role in ROLES) + (
        interview_structural_placeholder_ref("reaction_receipt"),
        interview_structural_placeholder_ref("expression_moment"),
    )
    result = compile_external_handoff(
        handoff_input(builder_source="Interview Expression", lineage=lineage)
    )
    assert result.source_kind == "interview_expression"
    assert result.interview_provenance_classification == INTERVIEW_PLACEHOLDER_CLASSIFICATION


def test_wrong_reading_locks_are_nonempty_and_monotonic() -> None:
    with pytest.raises(WrongReadingLockRejected, match="requires wrong-reading locks"):
        compile_external_handoff(handoff_input(locks=()))
    parent = lock(level=2, scopes=("/meaning", "/identity"))
    stronger = lock(level=3, scopes=("/meaning", "/identity", "/audience"))
    result = compile_external_handoff(handoff_input(locks=(stronger,), parent_locks=(parent,)))
    assert result.wrong_reading_locks[0].enforcement_level == 3
    with pytest.raises(WrongReadingLockRejected):
        compile_external_handoff(handoff_input(locks=(lock(level=1),), parent_locks=(parent,)))


def test_compiled_request_rejects_forged_bytes_hash_or_claims() -> None:
    result = compile_external_handoff(handoff_input(DELEGATION_TARGET))
    with pytest.raises(HandoffContractRejected):
        replace(result, request_hash="sha256:" + "0" * 64)
    with pytest.raises(HandoffContractRejected):
        replace(result, canonical_bytes=b"{}\n")
    with pytest.raises(HandoffContractRejected):
        replace(result, certified=True)
    with pytest.raises(SourceProvenanceRejected):
        replace(result, source_kind="guessed_source_kind")
    with pytest.raises(HandoffContractRejected):
        replace(result, semantic_lineage=result.semantic_lineage[:-1])
    with pytest.raises(WrongReadingLockRejected):
        replace(result, wrong_reading_locks=())
    with pytest.raises(HandoffContractRejected, match="exact frozen ST-07.02"):
        replace(result, st_07_02_completion_receipt_sha256="0" * 64)
    with pytest.raises(HandoffContractRejected, match="exact frozen ST-07.02"):
        replace(
            result,
            atomic_harness_definition_ref=replace(
                result.atomic_harness_definition_ref,
                version="999.0.0",
            ),
        )
    with pytest.raises(HandoffContractRejected, match="exact frozen ST-07.02"):
        replace(
            result,
            atomic_harness_definition_receipt_ref=replace(
                result.atomic_harness_definition_receipt_ref,
                authority="fake-parent-authority",
            ),
        )

    forged_input = handoff_input(DELEGATION_TARGET)
    with pytest.raises(HandoffContractRejected, match="exact governed ST-07.02 parent tuple"):
        compile_external_handoff(
            replace(
                forged_input,
                atomic_harness_definition_ref=replace(
                    forged_input.atomic_harness_definition_ref,
                    authority="fake-parent-authority",
                ),
                atomic_harness_definition_receipt_ref=replace(
                    forged_input.atomic_harness_definition_receipt_ref,
                    version="999.0.0",
                ),
            )
        )


def test_boolean_enforcement_level_is_rejected() -> None:
    with pytest.raises(WrongReadingLockRejected, match="positive level"):
        WrongReadingLock(
            lock_id="bool-is-not-an-int-policy",
            statement="Boolean coercion must not weaken lock enforcement.",
            meaning_hash=f"sha256:{sha256(b'bool').hexdigest()}",
            scope_paths=("/meaning",),
            enforcement_level=True,
        )


def test_interview_truth_refs_cannot_be_builder_owned() -> None:
    lineage = tuple(structural_lineage_fixture_ref(role) for role in ROLES) + (
        ref("reaction_receipt", authority="fake-human-authority"),
        ref("expression_moment", authority="fake-human-authority"),
    )
    with pytest.raises(HandoffAuthorityRejected, match="non-personal structural placeholders"):
        compile_external_handoff(
            handoff_input(builder_source="Interview Expression", lineage=lineage)
        )


def test_unrelated_role_correct_refs_are_not_admitted_as_structural_lineage() -> None:
    unrelated = tuple(ref(role, suffix="unrelated") for role in ROLES)
    with pytest.raises(HandoffContractRejected, match="exact OD structural fixture identity"):
        compile_external_handoff(handoff_input(lineage=unrelated))
    with pytest.raises(HandoffContractRejected, match="Unsupported structural lineage roles"):
        compile_external_handoff(
            handoff_input(
                lineage=tuple(structural_lineage_fixture_ref(role) for role in ROLES)
                + (ref("invented_human_truth"),)
            )
        )
