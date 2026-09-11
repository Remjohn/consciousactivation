from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ResearchBriefError(ValueError):
    """Base error for the structured Research Brief contract."""


class ResearchBriefBlockedError(ResearchBriefError):
    """Raised when a brief cannot cross the governed admission/consumption boundary."""

    def __init__(self, message: str, *, reason_codes: tuple[str, ...]):
        super().__init__(message)
        self.reason_codes = reason_codes


class ResearchBriefNotFoundError(ResearchBriefError):
    """Raised when a requested brief revision does not exist."""


class ResearchBriefStaleError(ResearchBriefError):
    """Raised when a caller attempts to admit/consume a non-current brief revision."""


class ResearchBriefAuthorityError(ResearchBriefError):
    """Raised when the caller uses an unauthorized authority lane."""


class ResearchBriefSourceSubstitutionError(ResearchBriefError):
    """Raised when a pinned source identity no longer matches the source registry."""


AuthorityTier = Annotated[int, Field(ge=1, le=4)]


class ClaimType(str, Enum):
    FACT = "FACT"
    HYPOTHESIS = "HYPOTHESIS"
    INFERENCE = "INFERENCE"


class FalsificationCondition(BaseModel):
    """Explicit condition under which the claim would be disconfirmed."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    condition: str = Field(min_length=10)
    evidence_to_check: str = Field(min_length=10)


class ResearchCitation(BaseModel):
    """Stable citation identity pinned to an exact research-source revision."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    citation_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    source_revision: int = Field(ge=1)
    source_content_sha256: str | None = None
    immutable_locator: str | None = None

    @field_validator("source_content_sha256")
    @classmethod
    def validate_sha256(cls, value: str | None) -> str | None:
        if value is None:
            return value
        normalized = value.lower()
        if len(normalized) != 64 or any(char not in "0123456789abcdef" for char in normalized):
            raise ValueError("source_content_sha256 must be a 64-character lowercase SHA-256 hex digest")
        return normalized

    @model_validator(mode="after")
    def require_verifiable_anchor(self) -> "ResearchCitation":
        if not self.source_content_sha256 and not self.immutable_locator:
            raise ValueError("citation requires source_content_sha256 or immutable_locator")
        return self


class ResearchClaimDraft(BaseModel):
    """Unrevisioned claim authoring shape; the service binds it to a sealed revision."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    claim_id: str = Field(min_length=1)
    claim_type: ClaimType
    authority_tier: AuthorityTier
    claim_text: str = Field(min_length=10)
    citations: tuple[ResearchCitation, ...] = Field(min_length=1)
    falsification_condition: FalsificationCondition

    @field_validator("claim_text")
    @classmethod
    def claim_text_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("claim_text must not be blank")
        return value.strip()


class ResearchClaim(ResearchClaimDraft):
    """Revision-bound claim carried by a sealed Research Brief."""

    brief_revision: int = Field(ge=1)


class ResearchBriefDraft(BaseModel):
    """Input shape for creating a Research Brief revision."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    brief_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    question_id: str = Field(min_length=1)
    owner_id: str = Field(min_length=1)
    claims: tuple[ResearchClaimDraft, ...] = Field(min_length=1)


class ResearchBrief(BaseModel):
    """Sealed, typed, digest-pinned Research Brief consumed downstream."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["ca-m010.research-brief.v1"] = "ca-m010.research-brief.v1"
    brief_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    question_id: str = Field(min_length=1)
    owner_id: str = Field(min_length=1)
    revision: int = Field(ge=1)
    lifecycle_state: Literal["SEALED"] = "SEALED"
    authority_lane: Literal["COMPOSER"] = "COMPOSER"
    claims: tuple[ResearchClaim, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def claims_are_bound_to_parent_revision(self) -> "ResearchBrief":
        mismatched = [claim.claim_id for claim in self.claims if claim.brief_revision != self.revision]
        if mismatched:
            raise ValueError(
                "all claims must bind to the containing Research Brief revision; "
                f"mismatched claim_ids={mismatched}"
            )
        return self


class ResearchBriefInspection(BaseModel):
    """Operator-facing read model for provenance and blocked reasons."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    brief_id: str
    current_revision: int | None
    inspected_revision: int | None
    admission_state: Literal["READY", "BLOCKED", "NOT_FOUND"]
    block_reasons: tuple[str, ...]
    claim_count: int
    source_pins: tuple[dict[str, object], ...]


class ResearchBriefReceipt(BaseModel):
    """Deterministic receipt emitted and persisted for a brief admission."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    receipt_type: Literal["cae_execution_receipt"] = "cae_execution_receipt"
    receipt_id: str
    operation_id: Literal["cae.research_brief.admit@1.0.0"] = "cae.research_brief.admit@1.0.0"
    actor_id: str
    authority_lane: Literal["COMPOSER"] = "COMPOSER"
    workspace_id: str
    aggregate_id: str
    brief_revision: int
    brief_canonical_sha256: str
    input_snapshot_sha256: str
    output_snapshot_sha256: str
    idempotent_replay: bool
    receipt_sha256: str
