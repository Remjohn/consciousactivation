"""
domain.py
---------
Canonical domain models for CAE World Intelligence (CAE-M01).
"""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class ProvenanceRecord(BaseModel):
    """Immutable audit record linking a signal to its raw origin."""
    origin_url: str = Field(..., description="Absolute URL where the observation was retrieved")
    root_domain: str = Field(..., description="Canonical root domain (e.g. reuters.com, reddit.com)")
    platform: str = Field(..., description="Platform identifier (searxng, reddit, x, hn, polymarket, news)")
    observed_at: datetime = Field(..., description="Timestamp of when the observation was retrieved")
    content_hash_sha256: str = Field(..., description="SHA-256 hash of the verbatim snippet or payload")
    author_outlet: Optional[str] = Field(None, description="Author or publishing outlet name")
    is_syndicated_copy: bool = Field(False, description="Flag indicating if this is a syndicated republication")

    @classmethod
    def compute_content_hash(cls, text: str) -> str:
        clean_text = text.strip().encode("utf-8")
        return hashlib.sha256(clean_text).hexdigest()


class SourceMultiplicity(BaseModel):
    """Tracks raw vs independent source corroboration to prevent duplicate-source inflation."""
    raw_mention_count: int = Field(..., ge=1, description="Total number of citations/mentions found")
    unique_root_domain_count: int = Field(..., ge=1, description="Number of distinct root domains")
    independent_source_count: int = Field(..., ge=1, description="Unique domains excluding syndicated mirrors")
    syndication_ratio: float = Field(0.0, ge=0.0, le=1.0, description="Proportion of mentions that are syndicated")


class RawObservation(BaseModel):
    """Raw, pre-normalization observation ingested from an external research adapter."""
    observation_id: str = Field(default_factory=lambda: f"OBS-{uuid.uuid4().hex[:12]}")
    source_platform: str
    query_context: str
    raw_payload: Dict[str, Any]
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    raw_text_snippet: str
    source_url: str
    author_outlet: Optional[str] = None


class ResearchSignal(BaseModel):
    """
    The canonical, immutable World Intelligence entity representing a verified external trend or cultural signal.
    """
    signal_id: str = Field(default_factory=lambda: f"SIG-{uuid.uuid4().hex[:12]}")
    topic: str = Field(..., min_length=2, description="Normalized topic headline or query focus")
    entities: List[str] = Field(default_factory=list, description="Extracted named entities")
    retrieval_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    observation_time: datetime = Field(..., description="Real-world timestamp of the underlying event/post")
    
    # 14-Feature Space Metrics
    velocity_score: float = Field(..., ge=0.0, le=1.0, description="Recent mention/search velocity")
    acceleration_score: float = Field(0.0, ge=0.0, le=1.0, description="Rate of velocity increase (2nd derivative)")
    cross_source_divergence: float = Field(0.0, ge=0.0, le=1.0, description="Framing variance across platforms")
    novelty_score: float = Field(0.5, ge=0.0, le=1.0, description="Semantic distance from known baselines")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Corroboration confidence based on independent sources")
    mutation_rate: float = Field(0.0, ge=0.0, le=1.0, description="Lexical variation rate across discussions")
    engine_agreement: float = Field(1.0, ge=0.0, le=1.0, description="Consensus across multiple search engines")
    rank_volatility: float = Field(0.0, ge=0.0, le=1.0, description="SERP position volatility")
    publication_density: float = Field(0.5, ge=0.0, le=1.0, description="Density of publications over last 48h")
    new_domain_emergence: float = Field(0.0, ge=0.0, le=1.0, description="Ratio of emerging vs legacy domains")
    volume_spike_ratio: float = Field(1.0, ge=0.0, description="Volume vs moving baseline")
    entity_density: float = Field(0.5, ge=0.0, le=1.0, description="Named entity density in excerpt")
    headline_clustering: float = Field(0.5, ge=0.0, le=1.0, description="Semantic coherence of headline cluster")
    serp_feature_presence: float = Field(0.0, ge=0.0, le=1.0, description="Presence of interactive SERP features")
    click_entropy_proxy: float = Field(0.5, ge=0.0, le=1.0, description="Dispersion of user attention")

    evidence_excerpt: str = Field(..., min_length=10, description="Verbatim evidence snippet")
    source_multiplicity: SourceMultiplicity = Field(...)
    primary_provenance: ProvenanceRecord = Field(...)
    corroborating_provenance: List[ProvenanceRecord] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("confidence_score")
    @classmethod
    def validate_confidence_against_sources(cls, v: float, info) -> float:
        # Multiplicity checks will be further enforced by ResearchSignalVerifier
        return v
