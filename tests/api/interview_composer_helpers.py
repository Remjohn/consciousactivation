from __future__ import annotations

from typing import Any

from cmf_activative_intelligence.application import AirApplication

AUTHORITY = {
    "authority_id": "ca-program-control-v2.1-candidate",
    "authority_version": "2.1.0-candidate",
    "authority_sha256": "a" * 64,
    "authority_state": "candidate_not_current",
}


def _ref(object_id: str, sha256: str | None = None, version: str = "1.0.0") -> dict[str, str]:
    return {"object_id": object_id, "version": version, "sha256": sha256 or ("b" * 64)}


def seed_brand_context(air: AirApplication, *, brand_id: str = "brand-ctx-1") -> dict[str, Any]:
    """Seed a minimal brand_context_version into AIR."""
    payload = {
        "brand_context_id": brand_id,
        "version": "1.0.0",
        "authority": dict(AUTHORITY),
        "lifecycle_state": "approved",
        "epistemic_state": "operator_confirmed",
        "brand_genesis_session_ref": _ref("brand-genesis-1"),
        "identity_truths": ["We protect agency through honest pressure."],
        "audience_relationship": "The audience is a capable witness.",
        "positioning_tension": "Control protects but also prevents listening.",
        "source_refs": [_ref("source-1")],
    }
    result = air.brand.store_brand_context(payload, idempotency_key=f"test:{brand_id}")
    return result["object"]


def seed_voice_dna(air: AirApplication, *, brand_context_ref: dict[str, str],
                   voice_id: str = "voice-dna-1") -> dict[str, Any]:
    """Seed a minimal voice_dna into AIR, linked to the given brand context."""
    payload = {
        "voice_dna_id": voice_id,
        "version": "1.0.0",
        "authority": dict(AUTHORITY),
        "lifecycle_state": "approved",
        "epistemic_state": "operator_confirmed",
        "brand_context_ref": dict(brand_context_ref),
        "vocabulary_patterns": ["protective", "listen"],
        "rhythm_patterns": ["short declarative", "pause"],
        "sentence_pressure_patterns": ["low", "medium"],
        "stance_patterns": ["curious", "direct"],
        "specificity_patterns": ["concrete example"],
        "metaphor_range": ["journey", "weight"],
        "emotional_distance": "warm direct",
        "prohibited_centroid_patterns": ["generic advice", "stock empathy"],
        "source_evidence_refs": [_ref("source-evidence-1")],
    }
    result = air.brand.store_voice_dna(payload, idempotency_key=f"test:{voice_id}")
    return result["object"]


def seed_brand_and_voice(air: AirApplication) -> tuple[dict[str, Any], dict[str, Any]]:
    """Seed a brand context and a linked voice DNA, returning (brand, voice) stored objects."""
    brand = seed_brand_context(air)
    brand_ref = {
        "object_id": brand["object_id"],
        "version": brand["semantic_version"],
        "sha256": brand["canonical_sha256"],
    }
    voice = seed_voice_dna(air, brand_context_ref=brand_ref)
    return brand, voice


def stored_ref(obj: dict[str, Any]) -> dict[str, str]:
    return {
        "object_id": str(obj["object_id"]),
        "version": str(obj["semantic_version"]),
        "sha256": str(obj["canonical_sha256"]),
    }