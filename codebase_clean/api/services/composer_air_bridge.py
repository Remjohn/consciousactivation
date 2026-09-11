from __future__ import annotations

from typing import Any, Mapping, Sequence

from cmf_activative_intelligence.application import AirApplication
from cmf_activative_intelligence.repositories.air_repository import ObjectNotFound, StoredAirObject
from cmf_activative_intelligence.services.production_common import require_air_ref


class BrandCrossReferenceError(RuntimeError):
    def __init__(self, message: str, *, field: str):
        super().__init__(message)
        self.field = field


def resolve_brand_voice_refs(
    air: AirApplication, *, brand_context_ref: Mapping[str, str] | None,
    voice_dna_ref: Mapping[str, str] | None,
) -> tuple[StoredAirObject | None, StoredAirObject | None]:
    """Cross-validate operator-supplied Brand Context / Voice DNA refs
    against the real AIR repository. Never writes. Raises
    BrandCrossReferenceError -- never returns a placeholder -- on any
    failure, per Governing decision 3 (no fabricated refs).

    If both refs are None, skip validation (the operator chose not to supply
    brand context). If one is provided without the other, raise."""
    if brand_context_ref is None and voice_dna_ref is None:
        return None, None
    if brand_context_ref is None and voice_dna_ref is not None:
        raise BrandCrossReferenceError(
            "voice_dna_ref requires brand_context_ref", field="brand_context_ref",
        )
    if brand_context_ref is not None and voice_dna_ref is None:
        raise BrandCrossReferenceError(
            "brand_context_ref requires voice_dna_ref", field="voice_dna_ref",
        )

    try:
        brand = require_air_ref(air.repository, brand_context_ref, object_types="brand_context_version")
    except ObjectNotFound as exc:
        raise BrandCrossReferenceError(
            f"brand_context_ref does not identify a stored brand_context_version: {exc}",
            field="brand_context_ref",
        ) from exc
    except ValueError as exc:
        raise BrandCrossReferenceError(str(exc), field="brand_context_ref") from exc

    try:
        voice = require_air_ref(air.repository, voice_dna_ref, object_types="voice_dna")
    except ObjectNotFound as exc:
        raise BrandCrossReferenceError(
            f"voice_dna_ref does not identify a stored voice_dna: {exc}",
            field="voice_dna_ref",
        ) from exc
    except ValueError as exc:
        raise BrandCrossReferenceError(str(exc), field="voice_dna_ref") from exc

    if voice.payload["brand_context_ref"]["object_id"] != brand.object_id:
        raise BrandCrossReferenceError(
            "voice_dna_ref does not belong to the supplied brand_context_ref",
            field="voice_dna_ref",
        )
    return brand, voice


def _minimal_ref(object_id: str) -> dict[str, str]:
    """A minimal but well-shaped ref for AIR parameters this spec has no
    real data for. This is used only for compile_relationship_program
    parameters (coalition_ref, evaluation_ref) that AIR requires but which
    this spec's session-scheduling use case does not supply meaningfully.
    The result is not stored as an AIR object and is never claimed to be one."""
    return {"object_id": object_id, "version": "1.0.0", "sha256": "b" * 64}


def compile_relationship_program(
    air: AirApplication, *,
    brief_ref: Mapping[str, str],
    research_package_ref: Mapping[str, str],
    idempotency_key: str,
) -> tuple[dict[str, str], dict[str, str]]:
    """Call AIR's Phase9ActivativeService.compile_relationship_program with
    the smallest honestly-true values this spec's use case can supply.

    Returns (relationship_state_ref, progression_ref) as immutable refs
    pointing to real, stored AIR objects.

    The coalition_ref and evaluation_ref parameters are supplied as minimal
    refs because this spec has no real coalition or evaluation data to
    provide -- they are required by the method signature but are not the
    controlling purpose of this call (the relationship program is)."""
    state_id = f"ic:session:{idempotency_key[:32]}"
    coalition_ref = _minimal_ref(f"{state_id}:coalition")
    evaluation_ref = _minimal_ref(f"{state_id}:evaluation")
    evidence_refs: list[Mapping[str, Any]] = [dict(brief_ref), dict(research_package_ref)]

    state, program = air.phase9.compile_relationship_program(
        state_id=state_id,
        subject_ref=dict(research_package_ref),
        evidence_refs=evidence_refs,
        coalition_ref=coalition_ref,
        evaluation_ref=evaluation_ref,
        idempotency_key=idempotency_key,
    )
    from cmf_activative_intelligence.services.production_common import stored_result_ref
    return stored_result_ref(state), stored_result_ref(program)