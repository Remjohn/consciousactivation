from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PrimitiveFamily(str, Enum):
    STRUCTURAL = "structural"
    TENSION = "tension"
    IDENTITY = "identity"
    COMPRESSION = "compression"
    EMOTIONAL = "emotional"


class PrimitiveCandidate(BaseModel):
    model_config = ConfigDict(strict=True)

    primitive_id: str = Field(..., min_length=11, max_length=15)  # e.g. PRM-STR-008
    primitive_name: str = Field(..., min_length=3, max_length=80)
    family: PrimitiveFamily
    evidence_quote: str = Field(..., min_length=20)       # Must cite real coach speech
    evidence_fidelity: float = Field(..., ge=0.0, le=1.0)
    emotional_charge: float = Field(..., ge=0.0, le=1.0)
    tribal_density: float = Field(..., ge=0.0, le=1.0)
    speakability: float = Field(..., ge=0.0, le=1.0)

    @field_validator('primitive_id')
    @classmethod
    def primitive_id_must_follow_yaml_format(cls, v: str) -> str:
        """ADR-05: Enforce specific YAML IDs (e.g., PRM-STR-008), not family names."""
        parts = v.split("-")
        if len(parts) != 3:
            raise ValueError(f"primitive_id '{v}' must follow PRM-XXX-NNN format (ADR-05).")
        if parts[0] != "PRM":
            raise ValueError(f"primitive_id '{v}' must start with 'PRM' (ADR-05).")
        if not parts[2].isdigit():
            raise ValueError(f"primitive_id '{v}' must end with a numeric segment (ADR-05).")
        return v

    @field_validator('evidence_quote')
    @classmethod
    def evidence_must_not_be_generic(cls, v: str) -> str:
        generic_phrases = ["in general", "most people", "it is said", "studies show"]
        for phrase in generic_phrases:
            if phrase.lower() in v.lower():
                raise ValueError(f"Evidence quote contains generic phrase '{phrase}'. Must cite specific coach speech.")
        return v


class CoalitionSignature(BaseModel):
    model_config = ConfigDict(strict=True)

    coalition_id: str
    primitives: list[PrimitiveCandidate] = Field(..., min_length=2, max_length=5)
    dominant_primitive_id: str  # Must be a specific YAML ID
    combined_force_score: float = Field(..., ge=0.0, le=1.0)
    edge_product_type: str

    @field_validator('dominant_primitive_id')
    @classmethod
    def dominant_must_follow_yaml_format(cls, v: str) -> str:
        parts = v.split("-")
        if len(parts) != 3 or parts[0] != "PRM":
            raise ValueError(f"dominant_primitive_id '{v}' must follow PRM-XXX-NNN format (ADR-05).")
        return v


class EdgeProduct(BaseModel):
    model_config = ConfigDict(strict=True)

    edge_id: str
    coalition_id: str
    tension_object: str = Field(..., min_length=10)
    ccf_routing_target: str                     # Which CCF archetype/format receives this
    cmf_routing_target: str | None = None       # Optional CMF routing
    anti_centroid_score: float = Field(..., ge=0.0, le=1.0)
