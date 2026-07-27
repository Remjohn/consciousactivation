"""
src/ccp/services/eval_registry_service.py
=========================================
Canonical evaluation registry lookup, validation, scoring, and normalization service.
"""

from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional

from src.ccp.models.eval_registry_models import (
    MetricScale,
    VisibleFamilyKey,
    HiddenClusterKey,
    EvalDefinition,
    EvalCluster,
    VisibleScoreFamily,
    HiddenSupportCluster,
    EvalMeasurement,
    EvalPenaltyRule,
    EvalScoreProjection
)


class EvalRegistryService:
    """Manages the canonical scoring taxonomy dictionary, rules, and mathematical projection models."""

    def __init__(self):
        # 1. Initialize Visible Families
        self.visible_families: Dict[VisibleFamilyKey, VisibleScoreFamily] = {
            VisibleFamilyKey.HUMANITY: VisibleScoreFamily(
                family_key=VisibleFamilyKey.HUMANITY,
                primary_question="does this feel like a real person with lived experience?",
                base_color_hex="#EC4899"
            ),
            VisibleFamilyKey.PRESENCE: VisibleScoreFamily(
                family_key=VisibleFamilyKey.PRESENCE,
                primary_question="does this person feel worth paying attention to?",
                base_color_hex="#8B5CF6"
            ),
            VisibleFamilyKey.TRUST: VisibleScoreFamily(
                family_key=VisibleFamilyKey.TRUST,
                primary_question="do I believe this signal and does it feel earned?",
                base_color_hex="#3B82F6"
            ),
            VisibleFamilyKey.MEMORABILITY: VisibleScoreFamily(
                family_key=VisibleFamilyKey.MEMORABILITY,
                primary_question="will this survive beyond the scroll?",
                base_color_hex="#F59E0B"
            ),
            VisibleFamilyKey.RESONANCE: VisibleScoreFamily(
                family_key=VisibleFamilyKey.RESONANCE,
                primary_question="did this emotionally and symbolically land?",
                base_color_hex="#10B981"
            ),
            VisibleFamilyKey.SIGNAL: VisibleScoreFamily(
                family_key=VisibleFamilyKey.SIGNAL,
                primary_question="does this cut through noise with sharp identity and non-generic specificity?",
                base_color_hex="#EF4444"
            ),
            VisibleFamilyKey.AI_SLOP_RISK: VisibleScoreFamily(
                family_key=VisibleFamilyKey.AI_SLOP_RISK,
                primary_question="how strongly does this feel flattened, over-smoothed, generic, or statistically familiar?",
                base_color_hex="#6B7280",
                is_penalty_indicator=True
            ),
        }

        # 2. Initialize Internal Metrics mapping to Clusters
        self.clusters: Dict[VisibleFamilyKey, EvalCluster] = {
            VisibleFamilyKey.HUMANITY: EvalCluster(
                cluster_id="CLU-HUMANITY",
                name="Humanity Cluster",
                target_family=VisibleFamilyKey.HUMANITY,
                cluster_description="Measures authentic human markers, transparency, and raw lived-experience density.",
                metrics=[
                    EvalDefinition(metric_id="MET-LIVEXP", name="Lived Experience Density", description="Density of direct evidence from direct real life actions.", scale=MetricScale.PROBABILITY, default_weight=0.3),
                    EvalDefinition(metric_id="MET-PROCTR", name="Process Transparency", description="How transparent and open the speaking process is.", scale=MetricScale.PROBABILITY, default_weight=0.2),
                    EvalDefinition(metric_id="MET-EMOTSP", name="Emotional Specificity", description="Specificity and texture of emotional markers.", scale=MetricScale.PROBABILITY, default_weight=0.2),
                    EvalDefinition(metric_id="MET-HUMTXT", name="Human Texture", description="Natural variations in delivery and conversational flow.", scale=MetricScale.PROBABILITY, default_weight=0.3)
                ]
            ),
            VisibleFamilyKey.PRESENCE: EvalCluster(
                cluster_id="CLU-PRESENCE",
                name="Presence Cluster",
                target_family=VisibleFamilyKey.PRESENCE,
                cluster_description="Measures authority projection, conviction, energetic stability, and charismatic draw.",
                metrics=[
                    EvalDefinition(metric_id="MET-CONVDN", name="Conviction Density", description="Force, pace stability, and belief transparency.", scale=MetricScale.PROBABILITY, default_weight=0.4),
                    EvalDefinition(metric_id="MET-AURAIT", name="Aura Intensity", description="Energetic aura density and command of attention.", scale=MetricScale.PROBABILITY, default_weight=0.3),
                    EvalDefinition(metric_id="MET-DELMAG", name="Delivery Magnetism", description="Magnetic cadence rhythm and acoustic clarity.", scale=MetricScale.PROBABILITY, default_weight=0.3)
                ]
            ),
            VisibleFamilyKey.TRUST: EvalCluster(
                cluster_id="CLU-TRUST",
                name="Trust Cluster",
                target_family=VisibleFamilyKey.TRUST,
                cluster_description="Measures credibility anchors, congruent arguments, and preservation of user dignity.",
                metrics=[
                    EvalDefinition(metric_id="MET-PROFDN", name="Proof Density", description="Explicit verifiable references and concrete proof density.", scale=MetricScale.PROBABILITY, default_weight=0.4),
                    EvalDefinition(metric_id="MET-VISANC", name="Visible Reality Anchors", description="Photographic, document, or frame evidence anchoring.", scale=MetricScale.PROBABILITY, default_weight=0.3),
                    EvalDefinition(metric_id="MET-CRECON", name="Credibility Congruence", description="Harmonic alignment with established worldview invariants.", scale=MetricScale.PROBABILITY, default_weight=0.3)
                ]
            ),
            VisibleFamilyKey.MEMORABILITY: EvalCluster(
                cluster_id="CLU-MEMORAB",
                name="Memorability Cluster",
                target_family=VisibleFamilyKey.MEMORABILITY,
                cluster_description="Measures symbolic compression, phrase density, and hook retention strength.",
                metrics=[
                    EvalDefinition(metric_id="MET-PHRCOM", name="Phrase Compression", description="Aphoristic sharpness and density of high-contrast phrasing.", scale=MetricScale.PROBABILITY, default_weight=0.4),
                    EvalDefinition(metric_id="MET-SYMREC", name="Symbolic Recall", description="Use of sticky analogies, visual models, or narrative tokens.", scale=MetricScale.PROBABILITY, default_weight=0.3),
                    EvalDefinition(metric_id="MET-HKPERS", name="Hook Persistence", description="Initial hook power and persistence through target scroll.", scale=MetricScale.PROBABILITY, default_weight=0.3)
                ]
            ),
            VisibleFamilyKey.RESONANCE: EvalCluster(
                cluster_id="CLU-RESONAN",
                name="Resonance Cluster",
                target_family=VisibleFamilyKey.RESONANCE,
                cluster_description="Measures atmospheric weight, subtextual depth, and emotional relevance mapping.",
                metrics=[
                    EvalDefinition(metric_id="MET-EMOCHG", name="Emotional Charge", description="Direct gut-level felt vulnerability and tension projection.", scale=MetricScale.PROBABILITY, default_weight=0.4),
                    EvalDefinition(metric_id="MET-SUBDEP", name="Subtext Depth", description="Layered complexity that prevents flat surface reading.", scale=MetricScale.PROBABILITY, default_weight=0.3),
                    EvalDefinition(metric_id="MET-FLTREL", name="Felt Relevance", description="Direct alignment with tribal worldview core tensions.", scale=MetricScale.PROBABILITY, default_weight=0.3)
                ]
            ),
            VisibleFamilyKey.SIGNAL: EvalCluster(
                cluster_id="CLU-SIGNAL",
                name="Signal Cluster",
                target_family=VisibleFamilyKey.SIGNAL,
                cluster_description="Measures anti-genericity, opinion sharpness, and niche specificity.",
                metrics=[
                    EvalDefinition(metric_id="MET-ANTGEN", name="Anti-Genericity", description="Negative distance to standard AI writing centroids.", scale=MetricScale.PROBABILITY, default_weight=0.4),
                    EvalDefinition(metric_id="MET-OPSHRP", name="Opinion Sharpness", description="Polarizing authority display without cheap aggression.", scale=MetricScale.PROBABILITY, default_weight=0.3),
                    EvalDefinition(metric_id="MET-NICSPC", name="Niche Specificity", description="Granularity of domain-specific references.", scale=MetricScale.PROBABILITY, default_weight=0.3)
                ]
            ),
            VisibleFamilyKey.AI_SLOP_RISK: EvalCluster(
                cluster_id="CLU-AISLOP",
                name="AI Slop Risk Cluster",
                target_family=VisibleFamilyKey.AI_SLOP_RISK,
                cluster_description="Quantifies synthetic patterns, over-smoothed phrasing, and template dependence.",
                metrics=[
                    EvalDefinition(metric_id="MET-DEDPOL", name="Dead Polish", description="Excessive clinical syntax and fake-deep vocabulary.", scale=MetricScale.PROBABILITY, default_weight=0.4),
                    EvalDefinition(metric_id="MET-OVSMTH", name="Over-smoothing", description="Flattened, highly generic statistical sentence pacing.", scale=MetricScale.PROBABILITY, default_weight=0.3),
                    EvalDefinition(metric_id="MET-STAFTY", name="Statistical Familiarity", description="Similarity to high-frequency Internet template centroids.", scale=MetricScale.PROBABILITY, default_weight=0.3)
                ]
            )
        }

        # 3. Initialize Hidden Support Clusters
        self.hidden_support: Dict[HiddenClusterKey, HiddenSupportCluster] = {
            HiddenClusterKey.STRUCTURE: HiddenSupportCluster(
                cluster_key=HiddenClusterKey.STRUCTURE,
                description="Influences flow stability across carousels and explainer formats.",
                influence_mappings={
                    VisibleFamilyKey.MEMORABILITY: 0.3,
                    VisibleFamilyKey.RESONANCE: 0.2,
                    VisibleFamilyKey.TRUST: 0.2
                }
            ),
            HiddenClusterKey.ACTIONABILITY: HiddenSupportCluster(
                cluster_key=HiddenClusterKey.ACTIONABILITY,
                description="Influences conversion willingness and felt competence transfer.",
                influence_mappings={
                    VisibleFamilyKey.TRUST: 0.4,
                    VisibleFamilyKey.PRESENCE: 0.2,
                    VisibleFamilyKey.SIGNAL: 0.2
                }
            )
        }

        # 4. Initialize Penalty and Cap Rules
        self.penalty_rules: List[EvalPenaltyRule] = [
            EvalPenaltyRule(
                rule_id="RUL-SLOP-CAP",
                trigger_metric=VisibleFamilyKey.AI_SLOP_RISK,
                threshold_value=40,
                cap_limit=59,
                description="If AI Slop Risk exceeds 40, overall score is penalized aggressively and capped at 59."
            ),
            EvalPenaltyRule(
                rule_id="RUL-TRUST-CAP",
                trigger_metric=VisibleFamilyKey.TRUST,
                threshold_value=40,
                cap_limit=59,
                description="If Trust is critically low (below 40), the overall score cannot exceed 59."
            ),
            EvalPenaltyRule(
                rule_id="RUL-HUMAN-CAP",
                trigger_metric=VisibleFamilyKey.HUMANITY,
                threshold_value=40,
                cap_limit=59,
                description="If Humanity is critically low (below 40), the overall score cannot exceed 59."
            )
        ]

    def query_metric(self, metric_id: str) -> Optional[EvalDefinition]:
        """Looks up a metric definition in the registry manifest."""
        for cluster in self.clusters.values():
            for metric in cluster.metrics:
                if metric.metric_id == metric_id:
                    return metric
        return None

    def normalize_value(self, raw_value: float, scale: MetricScale) -> int:
        """Applies mathematical normalization laws to force standard 0-99 output."""
        if scale == MetricScale.PROBABILITY:
            # Bounds checking for raw probability [0.0, 1.0]
            val = max(0.0, min(1.0, raw_value))
            return int(val * 99)
        elif scale == MetricScale.PERCENTAGE:
            val = max(0.0, min(100.0, raw_value))
            return int((val / 100.0) * 99)
        elif scale == MetricScale.COUNT:
            # Count values ceiling-cap at 10 to protect bounds
            val = max(0, min(10, int(raw_value)))
            return int((val / 10) * 99)
        else:
            # Fallback direct projection bounded at 0-99
            return max(0, min(99, int(raw_value)))

    def calculate_projection(
        self,
        raw_measurements: Dict[str, float],
        is_qa_reviewed: bool = False,
        operator_id: Optional[str] = None
    ) -> EvalScoreProjection:
        """
        Executes taxonomic calculations, maps metrics to visible families,
        processes non-linear slop penalties, validates boundaries, and encapsulates the QA gate state.
        """
        measurements: List[EvalMeasurement] = []
        visible_scores: Dict[VisibleFamilyKey, int] = {}

        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        # 1. Compute cluster visible score family averages
        for family_key, cluster in self.clusters.items():
            cluster_weighted_sum = 0.0
            for metric in cluster.metrics:
                # Retrieve raw measurement or default to 0.70 baseline
                raw_val = raw_measurements.get(metric.metric_id, 0.70)
                norm_score = self.normalize_value(raw_val, metric.scale)
                
                measurements.append(
                    EvalMeasurement(
                        metric_id=metric.metric_id,
                        raw_value=raw_val,
                        normalized_score=norm_score,
                        captured_at=now_str
                    )
                )
                cluster_weighted_sum += norm_score * metric.default_weight

            visible_scores[family_key] = max(0, min(99, int(cluster_weighted_sum)))

        # 2. Naive weighted overall score baseline
        weights = {
            VisibleFamilyKey.HUMANITY: 0.20,
            VisibleFamilyKey.PRESENCE: 0.15,
            VisibleFamilyKey.TRUST: 0.25,
            VisibleFamilyKey.MEMORABILITY: 0.15,
            VisibleFamilyKey.RESONANCE: 0.10,
            VisibleFamilyKey.SIGNAL: 0.15
        }

        weighted_sum = 0.0
        for fk, w in weights.items():
            weighted_sum += visible_scores[fk] * w

        overall_score = int(weighted_sum)

        # 3. Apply Penalty & Cap rules
        # AI Slop Risk Penalty: Slop score above 40 penalizes overall score aggressively
        slop_val = visible_scores[VisibleFamilyKey.AI_SLOP_RISK]
        if slop_val > 40:
            slop_penalty = (slop_val - 40) * 0.6
            overall_score = max(0, int(overall_score - slop_penalty))

        # Hard bounds caps (RUL-SLOP-CAP, RUL-TRUST-CAP, RUL-HUMAN-CAP)
        for rule in self.penalty_rules:
            curr_val = visible_scores[rule.trigger_metric]
            if rule.trigger_metric == VisibleFamilyKey.AI_SLOP_RISK:
                if curr_val > rule.threshold_value:
                    overall_score = min(overall_score, rule.cap_limit)
            else:
                if curr_val < rule.threshold_value:
                    overall_score = min(overall_score, rule.cap_limit)

        # Ensure final boundary limits [0, 99]
        overall_score = max(0, min(99, overall_score))

        # 4. Handle internal-first gating operator signature
        qa_signature = None
        is_approved = False
        if is_qa_reviewed and operator_id:
            is_approved = True
            qa_signature = f"QA-SIG-{uuid.uuid4().hex[:8].upper()}-{operator_id.upper()}"

        return EvalScoreProjection(
            measurements=measurements,
            visible_scores=visible_scores,
            overall_score=overall_score,
            is_internally_approved=is_approved,
            qa_signature=qa_signature
        )
