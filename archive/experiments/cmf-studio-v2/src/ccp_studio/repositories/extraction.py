"""Extraction repositories for TS-CMF-031."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.extraction import (
    ExpressionMomentCandidate,
    ExtractionReceipt,
    ExtractionRun,
    SkillExtractionContribution,
    SourceCue,
    TimestampedAnchorHit,
)


@dataclass
class InMemoryExtractionRepository:
    anchor_hits: dict[UUID, TimestampedAnchorHit] = field(default_factory=dict)
    source_cues: dict[UUID, SourceCue] = field(default_factory=dict)
    candidates: dict[UUID, ExpressionMomentCandidate] = field(default_factory=dict)
    skill_contributions: dict[UUID, SkillExtractionContribution] = field(default_factory=dict)
    extraction_runs: dict[UUID, ExtractionRun] = field(default_factory=dict)
    receipts: dict[UUID, ExtractionReceipt] = field(default_factory=dict)

    def put_anchor_hit(self, anchor_hit: TimestampedAnchorHit) -> TimestampedAnchorHit:
        self.anchor_hits[anchor_hit.anchor_hit_id] = anchor_hit
        return anchor_hit

    def put_source_cue(self, cue: SourceCue) -> SourceCue:
        self.source_cues[cue.source_cue_id] = cue
        return cue

    def put_candidate(self, candidate: ExpressionMomentCandidate) -> ExpressionMomentCandidate:
        self.candidates[candidate.candidate_id] = candidate
        return candidate

    def put_skill_contribution(self, contribution: SkillExtractionContribution) -> SkillExtractionContribution:
        self.skill_contributions[contribution.skill_invocation_receipt_id] = contribution
        return contribution

    def put_extraction_run(self, run: ExtractionRun) -> ExtractionRun:
        self.extraction_runs[run.extraction_run_id] = run
        return run

    def put_receipt(self, receipt: ExtractionReceipt) -> ExtractionReceipt:
        self.receipts[receipt.extraction_receipt_id] = receipt
        return receipt
