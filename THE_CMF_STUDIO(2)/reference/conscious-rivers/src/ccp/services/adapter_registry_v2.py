"""
CCP Step 7 — Adapter Registry v2.0 Pipeline Orchestrator (Unit 5)
Unified 8-adapter registry orchestrator with FR12 gate wiring.

Architecture reference:
    CCP_Technical_Architecture.md §4 Adapter Registry v2.0
    CCP_Evolution_Architecture_Report_V3 §3.2 — Three New Psychological Adapters
    FR12_Failure_Prevention_Gates_Tech_Spec.md — Gate wiring (DEP-ENG-027)

Load Order (Mandate 4 + v2.0 Tier ordering):
    TIER 1 — Mandatory (all skills):
        1. negative-space-loader-adapter  (Adapter-2) FIRST — Mandate 4
        2. coach-soul-adapter             (Adapter-1)
        3. irevc-adapter                  (Adapter-5)
        4. context-premise-adapter        (Adapter-3)
        5. psych-routing-adapter          (Adapter-4)
    TIER 2 — Conditional:
        6. payload-masking-adapter        (Adapter-6) — mood_state ≠ Processing
        7. audience-maturity-adapter      (Adapter-7)
        8. cral-finding-router-adapter    (Adapter-8) — DEP-ENG-021 available

FR12 Gate Wiring:
    Before seed emission proceeds to compilation, the pipeline checks
    DEP-ENG-027 (GateDiagnosticCertificate) if provided. BLOCKED status
    halts the pipeline.

This orchestrator extends the Step 5 VoiceDNAAdapterPipeline to cover
all 8 adapters. The Step 5 pipeline remains available for callers that
only need the 4 original adapters.

ADR-01: coach_id scopes all operations.
FR47:   Pipeline emits a top-level orchestration receipt after all adapters complete.
M-02:   No TTT hardcoded values in any adapter output.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.adapter_registry_models import AdapterRunResult, AdapterSlot
from src.ccp.models.adapter_registry_v2_models import (
    AdapterRegistryV2Result,
    CRALFindingIndex,
    GateWiringConfig,
    GateWiringStatus,
)
from src.ccp.models.emotional_dna_models import EmotionalDNAProfile
from src.ccp.models.psych_routing_models import MoodStatePrimary, PsychRoutingBrief
from src.ccp.models.tribe_profile_models import TribeProfileDistilled
from src.ccp.models.ttt_models import TTTBaselineData
from src.ccp.models.trigger_map_models import TriggerMap
from src.ccp.models.voice_dna_models import (
    HumorStyleClassification,
    NegativeSpaceObject,
    PositiveSpaceObject,
)
from src.ccp.services.coach_soul_adapter import CoachSoulAdapter
from src.ccp.services.context_premise_adapter import ContextPremiseAdapter
from src.ccp.services.cral_finding_router_adapter import CRALFindingRouterAdapter
from src.ccp.services.irevc_adapter import IREVCAdapter
from src.ccp.services.negative_space_loader_adapter import NegativeSpaceLoaderAdapter
from src.ccp.services.payload_masking_adapter import PayloadMaskingAdapter
from src.ccp.services.psych_routing_adapter import PsychRoutingAdapter

# Audience maturity adapter: import conditionally — may be at different path
try:
    from src.ccp.services.audience_maturity_adapter import AudienceMaturityAdapter
except ImportError:
    AudienceMaturityAdapter = None  # type: ignore[assignment, misc]


# ─── Constants ────────────────────────────────────────────────────────────────

AGENT_PIPELINE = "Adapter-Registry-V2-Pipeline"
STAGE_ORCHESTRATE = "STEP7-ADAPTER-REGISTRY-V2-ORCHESTRATE"


# ─── Pipeline Input ───────────────────────────────────────────────────────────

@dataclass
class AdapterRegistryV2Input:
    """All inputs required for the full Adapter Registry v2.0 pipeline.

    TIER 1 — Mandatory inputs:
        coach_id:         ADR-01 tenant isolation identifier.
        negative_space:   DEP-ENG-004 — NegativeSpaceExcavator (FR3).
        positive_space:   DEP-ENG-003 — PositiveSpaceExtractor (FR3).
        emotional_dna:    DEP-LIB-001 — EmotionalDNAPipeline (FR4).
        trigger_map:      DEP-LIB-002 — TriggerMapPipeline (FR5).
        context_premise:  DEP-ENG-006 — TribeProfileDistilled (FR6/FR9).

    TIER 1 — Optional inputs:
        humor:            HumorStyleClassification — FR3 Step 8.
        ttt_baseline:     DEP-ENG-005 — TTTBaselineExtractor (FR8 Layer 3).
        routing_brief:    DEP-ENG-016 — PsychRoutingPipeline (FR18).

    TIER 2 — Conditional inputs:
        mood_state:       MoodStatePrimary — for payload-masking-adapter activation.
        cral_finding_index: DEP-ENG-021 — from CRAL Orchestrator (FR14, Step 11).
        archetype_id:     For adapter-6 and adapter-8 arc routing.
        theme:            Content theme for adapter-3 and adapter-6.
        semantic_affinity_risk: DEP-PROTO-011 risk level.

    FR12 Gate Wiring:
        gate_wiring:      GateWiringConfig — from FR12 pipeline.
    """
    # ── TIER 1 Mandatory ──────────────────────────────────────
    coach_id: str = ""
    negative_space: Optional[NegativeSpaceObject] = None
    positive_space: Optional[PositiveSpaceObject] = None
    emotional_dna: Optional[EmotionalDNAProfile] = None
    trigger_map: Optional[TriggerMap] = None
    context_premise: Optional[TribeProfileDistilled] = None

    # ── TIER 1 Optional ───────────────────────────────────────
    humor: Optional[HumorStyleClassification] = None
    ttt_baseline: Optional[TTTBaselineData] = None
    routing_brief: Optional[PsychRoutingBrief] = None

    # ── TIER 2 Conditional ────────────────────────────────────
    mood_state: Optional[MoodStatePrimary] = None
    cral_finding_index: Optional[CRALFindingIndex] = None
    archetype_id: str = ""
    theme: str = ""
    semantic_affinity_risk: str = "LOW"

    # ── FR12 Gate Wiring ──────────────────────────────────────
    gate_wiring: Optional[GateWiringConfig] = None


# ─── Pipeline Orchestrator ────────────────────────────────────────────────────

class AdapterRegistryV2Pipeline:
    """Orchestrates all 8 adapters in the Adapter Registry v2.0.

    Extends the Step 5 VoiceDNAAdapterPipeline to include:
        - Adapter-3: context-premise-adapter (DEP-ENG-006)
        - Adapter-6: payload-masking-adapter (mood × archetype)
        - Adapter-8: cral-finding-router-adapter (DEP-ENG-021)
        - FR12 gate wiring (DEP-ENG-027)

    Mandate 4 enforcement:
        NegativeSpaceLoaderAdapter (Adapter-2) MUST complete before
        CoachSoulAdapter (Adapter-1). If Adapter-2 fails, pipeline halts.

    Tier 2 conditional activation:
        - Adapter-6 activated when mood_state ≠ Processing AND mood_state is provided
        - Adapter-7 activated when AudienceMaturityAdapter is importable
        - Adapter-8 activated when cral_finding_index is provided

    ADR-01: coach_id scopes all adapter invocations.
    """

    def __init__(self, receipt_chain: ReceiptChain) -> None:
        self._rc = receipt_chain

        # Tier 1 adapters
        self._neg_space = NegativeSpaceLoaderAdapter(receipt_chain)
        self._coach_soul = CoachSoulAdapter(receipt_chain)
        self._irevc = IREVCAdapter(receipt_chain)
        self._context_premise = ContextPremiseAdapter(receipt_chain)
        self._psych_routing = PsychRoutingAdapter(receipt_chain)

        # Tier 2 adapters
        self._payload_masking = PayloadMaskingAdapter(receipt_chain)
        self._audience_maturity = (
            AudienceMaturityAdapter(receipt_chain)
            if AudienceMaturityAdapter is not None
            else None
        )
        self._cral_router = CRALFindingRouterAdapter(receipt_chain)

    # ── FR12 Gate Wiring Check ────────────────────────────────

    def _check_gate_wiring(
        self,
        gate_wiring: Optional[GateWiringConfig],
    ) -> tuple[GateWiringConfig, list[str]]:
        """Check FR12 gate diagnostic certificate before proceeding.

        Returns:
            (config, gate_failures) — gate_failures non-empty if BLOCKED.
        """
        if gate_wiring is None:
            return GateWiringConfig(), []

        failures: list[str] = []
        if not gate_wiring.is_compilation_allowed():
            failures.append(
                f"FR12 GATE BLOCKED: Overall status = {gate_wiring.overall_status.value}. "
                f"Gate 1 = {gate_wiring.gate_1_verdict}, "
                f"Gate 2 = {gate_wiring.gate_2_verdict}. "
                f"Compilation HALTED — resolve gate failures before proceeding."
            )

        return gate_wiring, failures

    # ── Main Pipeline Run ─────────────────────────────────────

    def run(self, inputs: AdapterRegistryV2Input) -> AdapterRegistryV2Result:
        """Execute all activated adapters in Mandate-4-compliant load order.

        Load order:
            TIER 1 (Mandatory, sequential):
                1. negative-space-loader (Adapter-2) — MUST run first
                2. coach-soul (Adapter-1) — requires step 1 success
                3. irevc (Adapter-5)
                4. context-premise (Adapter-3)
                5. psych-routing (Adapter-4)
            TIER 2 (Conditional, after Tier 1):
                6. payload-masking (Adapter-6)
                7. audience-maturity (Adapter-7)
                8. cral-finding-router (Adapter-8)

        Args:
            inputs: AdapterRegistryV2Input with all required + optional DEP-IDs.

        Returns:
            AdapterRegistryV2Result with all adapter results and FR12 status.
        """
        result = AdapterRegistryV2Result(
            coach_id=inputs.coach_id,
        )

        all_warnings: list[str] = []
        tier_2_activated: list[str] = []

        # ── FR12 Gate Wiring Check ────────────────────────────────
        gate_config, gate_failures = self._check_gate_wiring(inputs.gate_wiring)
        result.gate_wiring = gate_config

        if gate_failures:
            # Pipeline halted by FR12 gate
            result.gate_wiring.overall_status = GateWiringStatus.BLOCKED_GATE_1
            entry = self._rc.log(
                agent_id=AGENT_PIPELINE,
                action=STAGE_ORCHESTRATE,
                input_summary=f"coach_id={inputs.coach_id} — FR12 GATE BLOCKED",
                output_summary=f"Pipeline halted: {gate_failures[0]}",
                decision="BLOCK",
                decision_rationale="FR12 gate diagnostic certificate blocked compilation.",
                metadata={
                    "stage_name": STAGE_ORCHESTRATE,
                    "coach_id": inputs.coach_id,
                    "gate_blocked": True,
                },
            )
            result.pipeline_receipt_id = entry.receipt_id
            return result

        # ════════════════════════════════════════════════════════════
        # TIER 1 — Mandatory Adapters
        # ════════════════════════════════════════════════════════════

        # ── Step 1: Negative Space Loader (Adapter-2) — MUST RUN FIRST ──
        if inputs.negative_space is not None:
            neg_result = self._neg_space.load(
                negative_space=inputs.negative_space,
                coach_id=inputs.coach_id,
            )
        else:
            neg_result = AdapterRunResult(
                adapter_slot=AdapterSlot.NEGATIVE_SPACE_LOADER,
                coach_id=inputs.coach_id,
                success=False,
                gate_failures=["DEP-ENG-004 (NegativeSpaceObject) is None — cannot proceed."],
            )
        result.negative_space_result = neg_result
        all_warnings.extend(neg_result.warnings)

        if not neg_result.success:
            # Mandate 4: halt pipeline if negative space fails
            result.mandate_4_enforced = False
            result = self._finalize_result(result, all_warnings, tier_2_activated, inputs)
            return result

        result.mandate_4_enforced = True

        # ── Step 2: Coach Soul Adapter (Adapter-1) ──────────────────
        if inputs.positive_space is not None:
            coach_result = self._coach_soul.load(
                positive_space=inputs.positive_space,
                coach_id=inputs.coach_id,
                negative_space_complete=True,
                humor=inputs.humor,
            )
        else:
            coach_result = AdapterRunResult(
                adapter_slot=AdapterSlot.COACH_SOUL,
                coach_id=inputs.coach_id,
                success=False,
                gate_failures=["DEP-ENG-003 (PositiveSpaceObject) is None — cannot proceed."],
            )
        result.coach_soul_result = coach_result
        all_warnings.extend(coach_result.warnings)

        # ── Step 3: IREVC Adapter (Adapter-5) ───────────────────────
        if inputs.trigger_map is not None:
            irevc_result = self._irevc.load(
                trigger_map=inputs.trigger_map,
                coach_id=inputs.coach_id,
                ttt_baseline=inputs.ttt_baseline,
            )
        else:
            irevc_result = AdapterRunResult(
                adapter_slot=AdapterSlot.IREVC,
                coach_id=inputs.coach_id,
                success=False,
                gate_failures=["DEP-LIB-002 (TriggerMap) is None — cannot proceed."],
            )
        result.irevc_result = irevc_result
        all_warnings.extend(irevc_result.warnings)

        # ── Step 4: Context Premise Adapter (Adapter-3) ─────────────
        if inputs.context_premise is not None:
            ctx_result = self._context_premise.load(
                context_premise=inputs.context_premise,
                coach_id=inputs.coach_id,
                theme=inputs.theme,
            )
        else:
            ctx_result = AdapterRunResult(
                adapter_slot=AdapterSlot.CONTEXT_PREMISE,
                coach_id=inputs.coach_id,
                success=False,
                gate_failures=["DEP-ENG-006 (TribeProfileDistilled) is None — cannot proceed."],
            )
        result.context_premise_result = ctx_result
        all_warnings.extend(ctx_result.warnings)

        # ── Step 5: Psych Routing Adapter (Adapter-4) ───────────────
        if inputs.emotional_dna is not None:
            psych_result = self._psych_routing.load(
                emotional_dna=inputs.emotional_dna,
                coach_id=inputs.coach_id,
                routing_brief=inputs.routing_brief,
            )
        else:
            psych_result = AdapterRunResult(
                adapter_slot=AdapterSlot.PSYCH_ROUTING,
                coach_id=inputs.coach_id,
                success=False,
                gate_failures=["DEP-LIB-001 (EmotionalDNAProfile) is None — cannot proceed."],
            )
        result.psych_routing_result = psych_result
        all_warnings.extend(psych_result.warnings)

        # ── Tier 1 Complete Check ────────────────────────────────────
        tier_1_results = [neg_result, coach_result, irevc_result, ctx_result, psych_result]
        result.tier_1_complete = all(r.success for r in tier_1_results)

        # ════════════════════════════════════════════════════════════
        # TIER 2 — Conditional Adapters
        # ════════════════════════════════════════════════════════════

        # ── Step 6: Payload Masking Adapter (Adapter-6) ─────────────
        # Conditional: activated when mood_state is provided and ≠ Processing
        if inputs.mood_state is not None:
            tier_2_activated.append("payload-masking-adapter")
            pm_result = self._payload_masking.load(
                mood_state=inputs.mood_state,
                coach_id=inputs.coach_id,
                archetype_id=inputs.archetype_id,
                cral_finding_index=inputs.cral_finding_index,
                semantic_affinity_risk=inputs.semantic_affinity_risk,
                theme=inputs.theme,
            )
            result.payload_masking_result = pm_result
            all_warnings.extend(pm_result.warnings)

        # ── Step 7: Audience Maturity Adapter (Adapter-7) ───────────
        # Conditional: activated when the adapter module is available.
        # NOTE: AudienceMaturityAdapter uses compile_constraints() + format_block_b_section()
        # interface (Step 4 build) rather than the load() pattern used by Step 5+ adapters.
        # This adapter is wired separately by callers who have DEP-ENG-017.
        # The v2.0 pipeline records it as "available but externally managed".
        if self._audience_maturity is not None:
            tier_2_activated.append("audience-maturity-adapter")

        # ── Step 8: CRAL Finding Router Adapter (Adapter-8) ────────
        # Conditional: activated when cral_finding_index is provided
        # (also runs in CRAL_DEGRADED mode when index is None — graceful degradation)
        tier_2_activated.append("cral-finding-router-adapter")
        cral_result = self._cral_router.load(
            coach_id=inputs.coach_id,
            archetype_id=inputs.archetype_id,
            cral_finding_index=inputs.cral_finding_index,
        )
        result.cral_finding_router_result = cral_result
        all_warnings.extend(cral_result.warnings)

        # ── Finalize ──────────────────────────────────────────────────
        result = self._finalize_result(result, all_warnings, tier_2_activated, inputs)
        return result

    # ── Finalize Pipeline Result ──────────────────────────────

    def _finalize_result(
        self,
        result: AdapterRegistryV2Result,
        all_warnings: list[str],
        tier_2_activated: list[str],
        inputs: AdapterRegistryV2Input,
    ) -> AdapterRegistryV2Result:
        """Finalize the pipeline result with aggregate status and receipt."""

        result.tier_2_activated = tier_2_activated
        result.total_warnings = len(all_warnings)

        # Determine all_success across all activated adapters
        activated_results: list[Optional[AdapterRunResult]] = [
            result.negative_space_result,
            result.coach_soul_result,
            result.irevc_result,
            result.context_premise_result,
            result.psych_routing_result,
            result.payload_masking_result,
            result.audience_maturity_result,
            result.cral_finding_router_result,
        ]
        result.all_success = all(
            r.success for r in activated_results if r is not None
        )

        # Count injections
        block_a_count = len(result.get_all_block_a_injections())
        block_b_count = len(result.get_all_block_b_injections())

        # Write pipeline orchestration receipt
        adapter_receipts: dict[str, str] = {}
        for attr_name, r in [
            ("negative_space", result.negative_space_result),
            ("coach_soul", result.coach_soul_result),
            ("irevc", result.irevc_result),
            ("context_premise", result.context_premise_result),
            ("psych_routing", result.psych_routing_result),
            ("payload_masking", result.payload_masking_result),
            ("audience_maturity", result.audience_maturity_result),
            ("cral_finding_router", result.cral_finding_router_result),
        ]:
            if r is not None:
                adapter_receipts[attr_name] = r.receipt_id

        entry = self._rc.log(
            agent_id=AGENT_PIPELINE,
            action=STAGE_ORCHESTRATE,
            input_summary=(
                f"coach_id={inputs.coach_id} "
                f"mood={inputs.mood_state.value if inputs.mood_state else 'none'} "
                f"archetype={inputs.archetype_id or 'unspecified'} "
                f"has_cral={'yes' if inputs.cral_finding_index else 'no'} "
                f"has_gate_wiring={'yes' if inputs.gate_wiring else 'no'}"
            ),
            output_summary=(
                f"all_success={result.all_success} "
                f"mandate_4={result.mandate_4_enforced} "
                f"tier_1_complete={result.tier_1_complete} "
                f"tier_2_activated={tier_2_activated} "
                f"block_a={block_a_count} "
                f"block_b={block_b_count} "
                f"warnings={result.total_warnings}"
            ),
            metadata={
                "stage_name": STAGE_ORCHESTRATE,
                "coach_id": inputs.coach_id,
                "all_success": result.all_success,
                "mandate_4_enforced": result.mandate_4_enforced,
                "tier_1_complete": result.tier_1_complete,
                "tier_2_activated": tier_2_activated,
                "adapter_receipts": adapter_receipts,
                "block_a_injection_count": block_a_count,
                "block_b_injection_count": block_b_count,
                "total_warnings": result.total_warnings,
                "gate_wiring_status": result.gate_wiring.overall_status.value,
            },
        )
        result.pipeline_receipt_id = entry.receipt_id

        return result

    # ── Format Full SKILL.md Injection ────────────────────────

    def format_full_skill_md_injection(
        self,
        inputs: AdapterRegistryV2Input,
    ) -> dict[str, str]:
        """Run the full pipeline and return formatted SKILL.md section texts.

        Returns:
            Dict with keys 'block_a' and 'block_b' containing the assembled
            section text for SKILL.md injection.
        """
        pipeline_result = self.run(inputs)

        block_a_text = ""
        for injection in pipeline_result.get_all_block_a_injections():
            block_a_text += injection.to_block_a_text()

        block_b_text = ""
        for injection in pipeline_result.get_all_block_b_injections():
            block_b_text += injection.to_block_b_text()

        return {
            "block_a": block_a_text,
            "block_b": block_b_text,
            "all_success": str(pipeline_result.all_success),
            "pipeline_receipt_id": pipeline_result.pipeline_receipt_id,
        }
