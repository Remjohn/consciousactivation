"""
normalization.py
----------------
Normalization pipeline, URL canonicalization, and anti-inflation logic for World Intelligence.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import List, Set, Tuple
from urllib.parse import urlparse

from .domain import (
    ProvenanceRecord,
    RawObservation,
    ResearchSignal,
    SourceMultiplicity,
)


class SignalNormalizer:
    """Normalizes heterogeneous raw observations into canonical ResearchSignals."""

    # Common wire/syndication indicators
    WIRE_PATTERNS = [
        r"\(reuters\)",
        r"\(ap\)",
        r"associated press",
        r"pr newswire",
        r"business wire",
        r"syndicated from",
    ]

    @staticmethod
    def extract_root_domain(url: str) -> str:
        """Extract canonical root domain from a URL (e.g., https://sub.reddit.com/r/xyz -> reddit.com)."""
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()
        if not netloc:
            netloc = url.split("/")[0].lower()
            
        # Strip port
        netloc = netloc.split(":")[0]
        
        # Extract base domain
        parts = netloc.split(".")
        if len(parts) >= 2:
            return ".".join(parts[-2:])
        return netloc

    @classmethod
    def is_syndicated_text(cls, text: str) -> bool:
        """Detect if text contains explicit wire/syndication attribution."""
        lower_text = text.lower()
        for pattern in cls.WIRE_PATTERNS:
            if re.search(pattern, lower_text):
                return True
        return False

    @classmethod
    def calculate_multiplicity(
        cls,
        observations: List[RawObservation],
    ) -> Tuple[SourceMultiplicity, List[ProvenanceRecord]]:
        """
        Analyze a cluster of observations to extract independent provenance records
        and detect duplicate-source inflation.
        """
        if not observations:
            raise ValueError("Cannot calculate multiplicity for empty observation set.")

        provenance_list: List[ProvenanceRecord] = []
        seen_hashes: Set[str] = set()
        unique_domains: Set[str] = set()
        independent_domains: Set[str] = set()
        syndicated_count = 0

        for obs in observations:
            root_dom = cls.extract_root_domain(obs.source_url)
            unique_domains.add(root_dom)
            
            content_hash = ProvenanceRecord.compute_content_hash(obs.raw_text_snippet)
            is_dup_hash = content_hash in seen_hashes
            is_wire = cls.is_syndicated_text(obs.raw_text_snippet)
            
            is_syndicated = is_dup_hash or is_wire
            if is_syndicated:
                syndicated_count += 1
            else:
                independent_domains.add(root_dom)
                
            seen_hashes.add(content_hash)
            
            record = ProvenanceRecord(
                origin_url=obs.source_url,
                root_domain=root_dom,
                platform=obs.source_platform,
                observed_at=obs.retrieved_at,
                content_hash_sha256=content_hash,
                author_outlet=obs.author_outlet,
                is_syndicated_copy=is_syndicated,
            )
            provenance_list.append(record)

        total_mentions = len(observations)
        unique_dom_count = len(unique_domains)
        # Independent source count is at least 1, and at most the number of unique non-syndicated domains
        indep_count = max(1, len(independent_domains))
        synd_ratio = syndicated_count / total_mentions if total_mentions > 0 else 0.0

        multiplicity = SourceMultiplicity(
            raw_mention_count=total_mentions,
            unique_root_domain_count=unique_dom_count,
            independent_source_count=indep_count,
            syndication_ratio=synd_ratio,
        )

        return multiplicity, provenance_list

    @classmethod
    def synthesize_signal(
        cls,
        topic: str,
        observations: List[RawObservation],
        *,
        entities: List[str] | None = None,
        velocity_score: float = 0.7,
        acceleration_score: float = 0.5,
        cross_source_divergence: float = 0.3,
        novelty_score: float = 0.6,
        confidence_base: float = 0.8,
        observation_time: datetime | None = None,
    ) -> ResearchSignal:
        """
        Synthesize a list of raw observations into a single verified ResearchSignal.
        """
        if not observations:
            raise ValueError("Observations required to synthesize a ResearchSignal.")

        multiplicity, provenance_records = cls.calculate_multiplicity(observations)
        primary_provenance = provenance_records[0]
        corroborating = provenance_records[1:] if len(provenance_records) > 1 else []

        # Confidence calculation: Penalize if low independent source count despite high raw mentions
        if multiplicity.independent_source_count == 1 and multiplicity.raw_mention_count > 3:
            # Duplicate syndication detected, cap confidence
            calibrated_confidence = min(0.60, confidence_base * 0.7)
        elif multiplicity.independent_source_count >= 2:
            calibrated_confidence = min(1.0, confidence_base)
        else:
            calibrated_confidence = confidence_base * 0.8

        obs_time = observation_time or observations[0].retrieved_at

        return ResearchSignal(
            topic=topic,
            entities=entities or [],
            observation_time=obs_time,
            velocity_score=velocity_score,
            acceleration_score=acceleration_score,
            cross_source_divergence=cross_source_divergence,
            novelty_score=novelty_score,
            confidence_score=calibrated_confidence,
            evidence_excerpt=observations[0].raw_text_snippet,
            source_multiplicity=multiplicity,
            primary_provenance=primary_provenance,
            corroborating_provenance=corroborating,
        )
