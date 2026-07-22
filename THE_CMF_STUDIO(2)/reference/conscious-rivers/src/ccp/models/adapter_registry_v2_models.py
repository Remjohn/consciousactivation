"""
CCP Step 7 — Adapter Registry v2.0 Models (Unit 1)
Extended Pydantic v2 models for the three new adapters and the unified
8-adapter pipeline orchestrator.

Architecture reference:
    CCP_Technical_Architecture.md §4 Adapter Registry v2.0
    CCP_Evolution_Architecture_Report_V3 §3.2 — Three New Psychological Adapters
    CCP_Evolution_Architecture_Report_V4 §3.3 — cral-finding-router-adapter

New adapters built in Step 7:
    Adapter-3: context-premise-adapter    (DEP-ENG-006 → Block B)
    Adapter-6: payload-masking-adapter    (mood × archetype → Block B)
    Adapter-8: cral-finding-router-adapter (DEP-ENG-021 → Block B arc phase)

FR12 gate wiring:
    DEP-ENG-027 (GateDiagnosticCertificate) consumed by the registry
    to gate seed emission before compilation proceeds.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field

from src.ccp.models.adapter_registry_models import AdapterRunResult


# ══════════════════════════════════════════════════════════════
# CRAL Finding Index Models (DEP-ENG-021)
# ══════════════════════════════════════════════════════════════

class CRALMomentKey(str, Enum):
    """The 7 CRAL research moment keys from FR14.
    Each moment produces one finding routed by cral-finding-router-adapter."""
    M1_TIMELY = "M1_TIMELY"
    M2_BELIEVABLE = "M2_BELIEVABLE"
    M3_UNDENIABLE = "M3_UNDENIABLE"
    M4_RESONANT = "M4_RESONANT"
    M5_SURPRISING = "M5_SURPRISING"
    M6_IRREFUTABLE = "M6_IRREFUTABLE"
    M7_RELATABLE = "M7_RELATABLE"


class CRALFinding(BaseModel):
    """A single CRAL finding from DEP-ENG-021.
    Each finding is routed to a specific arc phase by the adapter."""
    moment_key: CRALMomentKey = Field(
        description="Which research moment produced this finding."
    )
    finding_text: str = Field(
        description="The compiled finding text ready for injection."
    )
    source_quality: str = Field(
        default="verified",
        description="Quality tier: verified, partial, degraded."
    )
    human_evidence_count: int = Field(
        default=0,
        description="Number of named human evidence instances (FR16 gate: ≥3)."
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional finding metadata from the research pipeline."
    )


class CRALFindingIndex(BaseModel):
    """DEP-ENG-021 — CRAL Finding Index.
    Contains all 7 moment findings for a specific content compilation.
    Produced by CRAL Orchestrator (FR14). Consumed by cral-finding-router-adapter."""
    dep_id: str = Field(default="DEP-ENG-021")
    coach_id: str = Field(description="ADR-01 tenant isolation.")
    theme: str = Field(description="Content theme this index was researched for.")
    archetype_id: str = Field(description="Archetype family this compilation targets.")
    findings: dict[str, CRALFinding] = Field(
        default_factory=dict,
        description=(
            "Keyed by CRALMomentKey value. Missing keys indicate CRAL_DEGRADED "
            "for that moment — adapter must handle gracefully."
        ),
    )
    coverage_status: str = Field(
        default="COMPLETE",
        description="COMPLETE if all 7 moments present, DEGRADED if any missing."
    )

    def get_finding(self, moment: CRALMomentKey) -> Optional[CRALFinding]:
        """Retrieve a finding by moment key, or None if degraded."""
        return self.findings.get(moment.value)

    def missing_moments(self) -> list[CRALMomentKey]:
        """Return list of moments that have no finding."""
        return [m for m in CRALMomentKey if m.value not in self.findings]


# ══════════════════════════════════════════════════════════════
# Arc Phase Routing Map
# ══════════════════════════════════════════════════════════════

class ArcPhase(str, Enum):
    """Standard arc phases for storytelling archetype family.
    CCP_Evolution_Architecture_Report_V4 §3.3 Routing Map."""
    STAKES = "Stakes"
    MECHANISM = "Mechanism"
    TURN = "Turn"
    RESULT = "Result"
    IMPLICATION = "Implication"


# Default routing map from CCP_Evolution_Architecture_Report_V4 §3.3
# Maps each arc phase to the CRAL moments injected at that phase.
STORYTELLING_ARC_PHASE_ROUTING: dict[ArcPhase, list[CRALMomentKey]] = {
    ArcPhase.STAKES: [CRALMomentKey.M2_BELIEVABLE, CRALMomentKey.M3_UNDENIABLE],
    ArcPhase.MECHANISM: [CRALMomentKey.M4_RESONANT],
    ArcPhase.TURN: [CRALMomentKey.M5_SURPRISING],
    ArcPhase.RESULT: [CRALMomentKey.M6_IRREFUTABLE],
    ArcPhase.IMPLICATION: [CRALMomentKey.M7_RELATABLE],
}

# M1_TIMELY is a pre-condition check, not injected into an arc phase.
# It validates the topic's relevance window before compilation begins.


# ══════════════════════════════════════════════════════════════
# Context Premise Adapter Models (Adapter-3)
# ══════════════════════════════════════════════════════════════

class ContextPremiseAdapterOutput(BaseModel):
    """Output from the context-premise-adapter (Adapter-3).
    Extracts audience L3 coordinates from DEP-ENG-006 for Block B injection."""
    coach_id: str = Field(description="ADR-01 tenant isolation.")
    theme: str = Field(
        default="",
        description="Content theme for which context premise is loaded."
    )
    l3_pain_domains: list[str] = Field(
        default_factory=list,
        description="L3 depth pain domains extracted from the Context Premise Map."
    )
    tribal_terms: list[str] = Field(
        default_factory=list,
        description="Verified tribal language terms from the Context Premise Map."
    )
    segment_count: int = Field(
        default=0,
        description="Number of audience segments in the Context Premise Map."
    )
    depth_distribution: dict[str, float] = Field(
        default_factory=dict,
        description="L1/L2/L3 percentages from the Context Premise Map."
    )
    enemy_typology: list[str] = Field(
        default_factory=list,
        description="Shared enemy labels from the enemies dimension."
    )
    hidden_belief_summaries: list[str] = Field(
        default_factory=list,
        description="Hidden belief summaries for generation agent awareness."
    )
    constraint_strings: list[str] = Field(
        default_factory=list,
        description="Formatted constraint strings ready for Block B injection."
    )


# ══════════════════════════════════════════════════════════════
# Payload Masking Adapter Models (Adapter-6)
# ══════════════════════════════════════════════════════════════

class PayloadMaskingAdapterOutput(BaseModel):
    """Output from the payload-masking-adapter (Adapter-6).
    Generates Trojan Horse construction instruction per archetype × mood.
    CCP_Evolution_Architecture_Report_V3 §3.2."""
    coach_id: str = Field(description="ADR-01 tenant isolation.")
    mood_state: str = Field(description="MoodStatePrimary value driving this masking.")
    archetype_id: str = Field(
        default="",
        description="Archetype ID for archetype-specific masking variations."
    )
    masking_instruction: str = Field(
        description=(
            "The literal Trojan Horse instruction string for Emilio prompt injection. "
            "Operationalises Excitation Transfer per mood state."
        ),
    )
    m3_subversion_instruction: Optional[str] = Field(
        default=None,
        description=(
            "When DEP-ENG-021[M3_UNDENIABLE] is available: explicit instruction to "
            "subvert the audience's wrong prediction. FR22 Stage 2 Level 2."
        ),
    )
    semantic_affinity_cleared: bool = Field(
        default=False,
        description=(
            "True when Semantic Affinity Guard (DEP-PROTO-011) has cleared this "
            "mood × theme combination. Required before Escape mode masking."
        ),
    )
    constraint_strings: list[str] = Field(
        default_factory=list,
        description="Formatted constraint strings ready for Block B injection."
    )


# ══════════════════════════════════════════════════════════════
# CRAL Finding Router Adapter Models (Adapter-8)
# ══════════════════════════════════════════════════════════════

class ArcPhaseInjection(BaseModel):
    """A single CRAL finding injection targeted at a specific arc phase."""
    arc_phase: ArcPhase = Field(description="Which arc phase receives this injection.")
    moment_key: CRALMomentKey = Field(description="Which CRAL moment is injected.")
    injection_text: str = Field(
        description="The formatted finding text for Block B injection at this phase."
    )
    quality: str = Field(
        default="verified",
        description="verified | partial | degraded — from the source finding."
    )


class CRALFindingRouterOutput(BaseModel):
    """Output from the cral-finding-router-adapter (Adapter-8).
    Routes DEP-ENG-021 findings to correct arc phases."""
    coach_id: str = Field(description="ADR-01 tenant isolation.")
    archetype_id: str = Field(description="Archetype determining the routing map.")
    phase_injections: list[ArcPhaseInjection] = Field(
        default_factory=list,
        description="Ordered list of arc-phase-targeted CRAL injections."
    )
    degraded_phases: list[str] = Field(
        default_factory=list,
        description="Arc phases where the CRAL finding was missing (CRAL_DEGRADED)."
    )
    coverage_status: str = Field(
        default="COMPLETE",
        description="COMPLETE if all phases have findings, DEGRADED if any missing."
    )
    constraint_strings: list[str] = Field(
        default_factory=list,
        description="Formatted constraint strings ready for Block B injection."
    )


# ══════════════════════════════════════════════════════════════
# FR12 Gate Wiring Configuration
# ══════════════════════════════════════════════════════════════

class GateWiringStatus(str, Enum):
    """Status of FR12 gate diagnostic certificate wiring."""
    CLEARED = "CLEARED"
    BLOCKED_GATE_1 = "BLOCKED_GATE_1"
    BLOCKED_GATE_2 = "BLOCKED_GATE_2"
    PROVISIONAL = "PROVISIONAL"
    AWAITING_GATE_3 = "AWAITING_GATE_3"
    NOT_EVALUATED = "NOT_EVALUATED"


class GateWiringConfig(BaseModel):
    """FR12 gate diagnostic certificate consumption by the registry.
    When a seed has been evaluated by FR12, its GateDiagnosticCertificate
    determines whether compilation should proceed."""
    gate_certificate_id: Optional[str] = Field(
        default=None,
        description="DEP-ENG-027 certificate ID from FR12 pipeline."
    )
    gate_1_verdict: str = Field(
        default="NOT_EVALUATED",
        description="Gate 1 structural congruence verdict: PASS | PROVISIONAL | FAIL."
    )
    gate_2_verdict: str = Field(
        default="NOT_EVALUATED",
        description="Gate 2 language drift verdict: PASS | PROVISIONAL | FAIL."
    )
    gate_3_status: str = Field(
        default="AWAITING_TELEGRAM_PAYLOAD",
        description="Gate 3 async authenticity status."
    )
    overall_status: GateWiringStatus = Field(
        default=GateWiringStatus.NOT_EVALUATED,
        description="Computed overall wiring status."
    )
    language_drift_warning: bool = Field(
        default=False,
        description="True if Gate 2 returned PROVISIONAL with drift warning."
    )

    def is_compilation_allowed(self) -> bool:
        """Check if the gate wiring allows compilation to proceed.
        CLEARED or PROVISIONAL (with warning) allow compilation.
        AWAITING_GATE_3 allows compilation (Gate 3 is async post-recording).
        All BLOCKED states halt compilation."""
        return self.overall_status in (
            GateWiringStatus.CLEARED,
            GateWiringStatus.PROVISIONAL,
            GateWiringStatus.AWAITING_GATE_3,
        )


# ══════════════════════════════════════════════════════════════
# Adapter Registry v2.0 Pipeline Result
# ══════════════════════════════════════════════════════════════

class AdapterRegistryV2Result(BaseModel):
    """Composite result from the full Adapter Registry v2.0 pipeline.

    Collects all 8 adapter results and the FR12 gate wiring status.
    Extends the Step 5 VoiceDNAAdapterPipelineResult with the 3 new adapters.

    Load order (Mandate 4 + v2.0 ordering):
        TIER 1 — Mandatory (all skills):
            1. negative-space-loader-adapter  (Adapter-2) FIRST — Mandate 4
            2. coach-soul-adapter             (Adapter-1)
            3. irevc-adapter                  (Adapter-5)
            4. context-premise-adapter        (Adapter-3)
            5. psych-routing-adapter          (Adapter-4)
        TIER 2 — Conditional:
            6. payload-masking-adapter        (Adapter-6) — mood_state ≠ Processing
            7. audience-maturity-adapter      (Adapter-7)
            8. cral-finding-router-adapter    (Adapter-8) — v1.2 templates only
    """
    coach_id: str = Field(description="ADR-01 tenant isolation.")
    pipeline_receipt_id: str = Field(
        default="",
        description="Top-level orchestration receipt ID."
    )

    # ── Tier 1 Mandatory Results ──────────────────────────────
    negative_space_result: Optional[AdapterRunResult] = Field(default=None)
    coach_soul_result: Optional[AdapterRunResult] = Field(default=None)
    irevc_result: Optional[AdapterRunResult] = Field(default=None)
    context_premise_result: Optional[AdapterRunResult] = Field(default=None)
    psych_routing_result: Optional[AdapterRunResult] = Field(default=None)

    # ── Tier 2 Conditional Results ────────────────────────────
    payload_masking_result: Optional[AdapterRunResult] = Field(default=None)
    audience_maturity_result: Optional[AdapterRunResult] = Field(default=None)
    cral_finding_router_result: Optional[AdapterRunResult] = Field(default=None)

    # ── FR12 Gate Wiring ──────────────────────────────────────
    gate_wiring: GateWiringConfig = Field(
        default_factory=GateWiringConfig,
        description="FR12 gate diagnostic certificate wiring status."
    )

    # ── Aggregate Status ──────────────────────────────────────
    all_success: bool = Field(
        default=False,
        description="True if all activated adapters completed without gate failures."
    )
    mandate_4_enforced: bool = Field(
        default=False,
        description="True when negative-space-loader completed before coach-soul-adapter."
    )
    tier_1_complete: bool = Field(
        default=False,
        description="True when all 5 mandatory adapters completed successfully."
    )
    tier_2_activated: list[str] = Field(
        default_factory=list,
        description="List of Tier 2 adapter slot names that were activated."
    )
    total_warnings: int = Field(
        default=0,
        description="Total advisory warnings across all adapters."
    )

    def get_all_block_a_injections(self) -> list:
        """Return all Block A injections in Mandate-4-compliant load order."""
        from src.ccp.models.adapter_registry_models import BlockAInjection
        results: list[BlockAInjection] = []
        for result in [
            self.negative_space_result,
            self.coach_soul_result,
            self.irevc_result,
        ]:
            if result and result.success and result.block_a:
                results.append(result.block_a)
        return results

    def get_all_block_b_injections(self) -> list:
        """Return all Block B injections in execution order."""
        from src.ccp.models.adapter_registry_models import BlockBInjection
        results: list[BlockBInjection] = []
        for result in [
            self.context_premise_result,
            self.psych_routing_result,
            self.payload_masking_result,
            self.audience_maturity_result,
            self.cral_finding_router_result,
        ]:
            if result and result.success and result.block_b:
                results.append(result.block_b)
        return results
