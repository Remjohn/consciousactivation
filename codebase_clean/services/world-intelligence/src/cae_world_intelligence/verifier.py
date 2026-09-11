"""
verifier.py
-----------
Gating and verification logic for ResearchSignals (CAE-M01).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from .domain import ResearchSignal
from .errors import (
    DuplicateSourceInflationError,
    EvidenceError,
    ProvenanceError,
    StaleObservationError,
)


class ResearchSignalVerifier:
    """Enforces constitutional hard gates and anti-reward-hacking checks on ResearchSignals."""

    DEFAULT_MAX_AGE_DAYS = 30

    @classmethod
    def verify(
        cls,
        signal: ResearchSignal,
        *,
        max_age_days: int = DEFAULT_MAX_AGE_DAYS,
        current_time: Optional[datetime] = None,
    ) -> bool:
        """
        Validate a ResearchSignal. Raises specific WorldIntelligenceError on any violation.
        Returns True if fully valid.
        """
        now = current_time or datetime.now(timezone.utc)

        # 1. Provenance Integrity Gate
        if not signal.primary_provenance:
            raise ProvenanceError("Missing primary provenance record.")

        p = signal.primary_provenance
        if not p.origin_url or not p.origin_url.startswith(("http://", "https://", "feed://", "file://")):
            raise ProvenanceError(f"Invalid provenance URL: {p.origin_url}")

        if not p.observed_at:
            raise ProvenanceError("Provenance missing observation timestamp.")

        if not p.content_hash_sha256 or len(p.content_hash_sha256) != 64:
            raise ProvenanceError("Provenance missing valid SHA-256 content hash.")

        # 2. Evidence Excerpt Verification
        if not signal.evidence_excerpt or len(signal.evidence_excerpt.strip()) < 10:
            raise EvidenceError("Evidence excerpt is missing or too short to constitute verifiable evidence.")

        computed_hash = p.compute_content_hash(signal.evidence_excerpt)
        if computed_hash != p.content_hash_sha256:
            raise EvidenceError("Evidence excerpt does not match declared provenance content hash (Fabrication check failed).")

        # 3. Freshness / TTL Gate
        if signal.observation_time > now + timedelta(hours=1):
            raise StaleObservationError(f"Observation time {signal.observation_time} is in the future relative to {now}.")

        age_delta = now - signal.observation_time
        if age_delta > timedelta(days=max_age_days):
            # Check if explicitly allowed in metadata as archival baseline
            if not signal.metadata.get("is_archival_baseline", False):
                raise StaleObservationError(
                    f"Observation age ({age_delta.days} days) exceeds maximum freshness TTL of {max_age_days} days."
                )

        # 4. Multiplicity & Anti-Inflation Gate
        m = signal.source_multiplicity
        if m.independent_source_count > m.unique_root_domain_count:
            raise DuplicateSourceInflationError(
                f"Independent source count ({m.independent_source_count}) cannot exceed unique root domains ({m.unique_root_domain_count})."
            )

        # High confidence check requires real independent corroboration
        if signal.confidence_score > 0.85 and m.independent_source_count < 2:
            raise DuplicateSourceInflationError(
                f"High confidence ({signal.confidence_score:.2f}) requires at least 2 independent sources, but found {m.independent_source_count}."
            )

        return True
