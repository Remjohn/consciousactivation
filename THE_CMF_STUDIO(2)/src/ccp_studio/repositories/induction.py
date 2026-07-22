"""Induction rationale repositories for TS-CMF-028."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.induction import (
    CRALFinding,
    EmotionalDNAProfile,
    InductionRationale,
    InductionRationaleReceipt,
    VoiceDNAProfile,
)


@dataclass
class InMemoryInductionRepository:
    cral_findings: dict[UUID, CRALFinding] = field(default_factory=dict)
    emotional_dna_profiles: dict[UUID, EmotionalDNAProfile] = field(default_factory=dict)
    voice_dna_profiles: dict[UUID, VoiceDNAProfile] = field(default_factory=dict)
    rationales: dict[UUID, InductionRationale] = field(default_factory=dict)
    receipts: dict[UUID, InductionRationaleReceipt] = field(default_factory=dict)

    def put_cral_finding(self, finding: CRALFinding) -> CRALFinding:
        self.cral_findings[finding.cral_finding_id] = finding
        return finding

    def put_emotional_dna_profile(self, profile: EmotionalDNAProfile) -> EmotionalDNAProfile:
        self.emotional_dna_profiles[profile.emotional_dna_profile_id] = profile
        return profile

    def put_voice_dna_profile(self, profile: VoiceDNAProfile) -> VoiceDNAProfile:
        self.voice_dna_profiles[profile.voice_dna_profile_id] = profile
        return profile

    def put_rationale(self, rationale: InductionRationale) -> InductionRationale:
        self.rationales[rationale.rationale_id] = rationale
        return rationale

    def put_receipt(self, receipt: InductionRationaleReceipt) -> InductionRationaleReceipt:
        self.receipts[receipt.induction_rationale_receipt_id] = receipt
        return receipt
