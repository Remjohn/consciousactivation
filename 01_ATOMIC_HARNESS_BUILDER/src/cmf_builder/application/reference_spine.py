"""Development-uncertified reference complete-spine proof for OD-AM-005 / ST-12.03."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any


def sha256_of(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


class Format02SpineError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


REQUIRED_STEPS = (
    "source_admission",
    "syntax_observations",
    "provisional_grammar",
    "atomic_boundary",
    "harness_ir",
    "category_binding",
    "format02_profile",
    "category_native_syntax",
    "activative_sequencing",
    "capability_and_skill_decision",
    "recipe_and_jit_capsule",
    "target_compilation",
    "builder_owned_handoff_mapping",
    "evaluation",
    "diagnosis_and_selective_repair",
    "workflow_execution",
    "evidence_projections",
    "governed_receipt_export",
)


@dataclass(frozen=True)
class Format02SpineProof:
    proof_identity_seed: str
    admitted_corpus_refs: tuple[str, ...]
    excluded_corpus_refs_used: tuple[str, ...]
    category_identity: str
    profile_identity: str
    character_performance_requirements: tuple[str, ...]
    wrong_reading_locks: tuple[str, ...]
    lineage_refs: tuple[str, ...]
    executed_steps: tuple[str, ...]
    external_vae_execution: str = "NOT_PERFORMED"
    external_delegation_execution: str = "NOT_PERFORMED"
    bd_008_status: str = "OPEN"
    production_ready: bool = False
    certified: bool = False

    def __post_init__(self) -> None:
        if self.excluded_corpus_refs_used:
            raise Format02SpineError("EXCLUDED_CORPUS_USED", "Format 02 spine may not use excluded corpus members")
        if self.category_identity != "2D_CHARACTER_ANIMATION":
            raise Format02SpineError("FORMAT02_CATEGORY_MISMATCH", "Format 02 must bind to 2D Character Animation")
        if self.profile_identity != "FORMAT_02":
            raise Format02SpineError("FORMAT02_PROFILE_REQUIRED", "Format 02 profile identity is required")
        if len(set(self.character_performance_requirements)) != 13:
            raise Format02SpineError("THIRTEEN_CHARACTER_REQUIREMENTS_REQUIRED", "all 13 character-performance requirements are required")
        if not self.wrong_reading_locks:
            raise Format02SpineError("WRONG_READING_LOCKS_REQUIRED", "wrong-reading locks are required")
        missing = set(REQUIRED_STEPS) - set(self.executed_steps)
        if missing:
            raise Format02SpineError("SPINE_STEP_MISSING", "complete spine step missing", missing=sorted(missing))
        if self.external_vae_execution != "NOT_PERFORMED" or self.external_delegation_execution != "NOT_PERFORMED":
            raise Format02SpineError("EXTERNAL_PRODUCT_EXECUTION_PROHIBITED", "VAE and Delegation execution are not performed")
        if self.production_ready or self.certified:
            raise Format02SpineError("FORMAT02_CERTIFICATION_PROHIBITED", "development spine cannot claim production or certification")

    @property
    def proof_identity(self) -> str:
        return sha256_of(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "mode": "FORMAT02_SPINE_DEVELOPMENT_UNCERTIFIED",
            "proof_identity_seed": self.proof_identity_seed,
            "admitted_corpus_refs": list(self.admitted_corpus_refs),
            "category_identity": self.category_identity,
            "profile_identity": self.profile_identity,
            "character_performance_requirements": list(self.character_performance_requirements),
            "wrong_reading_locks": list(self.wrong_reading_locks),
            "lineage_refs": list(self.lineage_refs),
            "executed_steps": list(self.executed_steps),
            "format02_spine": "DEVELOPMENT_UNCERTIFIED",
            "bd_008": self.bd_008_status,
            "external_vae_execution": self.external_vae_execution,
            "external_delegation_execution": self.external_delegation_execution,
            "production_ready": False,
            "certified": False,
        }
