"""DSPy-style Matrix of Edging compiler for TS-CMF-025."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

from ccp_studio.contracts.context import AudienceRealityBrief, ContextPremise, GuestDossier
from ccp_studio.contracts.matrix import (
    BroadPrimarySignal,
    CoalitionSignature,
    EdgeProduct,
    MatrixBriefStatus,
    MatrixEvaluationScores,
    MatrixFailurePoint,
    MatrixOfEdgingBrief,
    MatrixPass,
    PrimitiveCandidatePacket,
    PrimitiveCandidateStatus,
    TensionSite,
    matrix_context_hash,
    new_pass_output,
)
from ccp_studio.contracts.orchestration import utc_now


@dataclass(frozen=True)
class MatrixOfEdgingCompiler:
    compiler_version: str = "matrix-of-edging-v1"

    def predict(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        research_field_id: UUID,
        guest_dossier: GuestDossier,
        audience_reality_brief: AudienceRealityBrief,
        context_premise: ContextPremise,
        trigger_map_id: UUID | None,
        created_by_actor_id: UUID,
        primitive_refs: list[str] | None = None,
        speculative_tension_statement: str | None = None,
        force_generic: bool = False,
    ) -> MatrixOfEdgingBrief:
        now = utc_now()
        input_ids = {
            "guest_dossier_id": guest_dossier.guest_dossier_id,
            "audience_reality_brief_id": audience_reality_brief.audience_reality_brief_id,
            "context_premise_id": context_premise.context_premise_id,
        }
        if trigger_map_id is not None:
            input_ids["trigger_map_id"] = trigger_map_id
        evidence_ids = list(dict.fromkeys([*context_premise.evidence_ids]))
        guest_signal = guest_dossier.identity_facts[0].statement if guest_dossier.identity_facts else "guest truth"
        audience_signal = (
            audience_reality_brief.current_anxieties[0].statement
            if audience_reality_brief.current_anxieties
            else "audience reality"
        )
        broad_statement = (
            "Generic hook about being more authentic."
            if force_generic
            else f"Pressure lives where {guest_signal} meets {audience_signal}."
        )
        broad_signal = BroadPrimarySignal(
            schema_version="cmf.broad_primary_signal.v1",
            broad_primary_signal_id=uuid4(),
            statement=broad_statement,
            evidence_ids=evidence_ids[:2] or evidence_ids,
            magnitude_score=0.9 if not force_generic else 0.32,
        )
        supported_tension = TensionSite(
            schema_version="cmf.tension_site.v1",
            tension_site_id=uuid4(),
            statement=(
                "Public competence collides with private exposure risk."
                if not force_generic
                else "People want better content."
            ),
            evidence_ids=evidence_ids,
            collision_type="identity_behavior_divergence",
            magnitude_score=0.88 if not force_generic else 0.25,
            speculative=False,
            can_anchor_question=True,
        )
        tension_sites = [supported_tension]
        if speculative_tension_statement:
            tension_sites.append(
                TensionSite(
                    schema_version="cmf.tension_site.v1",
                    tension_site_id=uuid4(),
                    statement=speculative_tension_statement,
                    evidence_ids=[],
                    collision_type="unsupported_inference",
                    magnitude_score=0.2,
                    speculative=True,
                    can_anchor_question=False,
                )
            )
        primitive_candidates = self._primitive_candidates(
            evidence_ids=evidence_ids,
            primitive_refs=primitive_refs or [
                "TRG:What-Is / What-Could-Be",
                "PSY:Vulnerable Specificity",
            ],
            force_generic=force_generic,
        )
        coalition = CoalitionSignature(
            schema_version="cmf.coalition_signature.v1",
            coalition_signature_id=uuid4(),
            primitive_candidate_ids=[item.primitive_candidate_id for item in primitive_candidates[:2]],
            family_ratios=self._family_ratios(primitive_candidates[:2]),
            interaction_rationale="The coalition compresses trigger structure and vulnerable specificity into one routeable pressure geometry.",
            route_implications=["interview_asset_contract:origin_scene", "matrix_route:recognition_edge"],
        )
        edge = EdgeProduct(
            schema_version="cmf.edge_product.v1",
            edge_product_id=uuid4(),
            name="recognition-exposure edge" if not force_generic else "generic motivation edge",
            tension_site_ids=[supported_tension.tension_site_id],
            coalition_signature_id=coalition.coalition_signature_id,
            anti_centroid_pressure="Force the opening into the lived contradiction before abstract advice.",
            expected_expression_state=["specific recollection", "truthful pressure", "method earned by scene"],
            route_implications=coalition.route_implications,
        )
        failure_points = [
            MatrixFailurePoint(
                schema_version="cmf.matrix_failure_point.v1",
                failure_point_id=uuid4(),
                statement="The Operator asks for a framework before the guest lands the lived scene.",
                avoidance_guidance="Start with the contradiction and ask what it cost, then let method language arrive later.",
                severity="high",
            ),
            MatrixFailurePoint(
                schema_version="cmf.matrix_failure_point.v1",
                failure_point_id=uuid4(),
                statement="A speculative tension is treated as a source-backed question anchor.",
                avoidance_guidance="Use speculative sites only as review prompts until evidence is attached.",
                severity="high",
            ),
        ]
        pass_outputs = [
            new_pass_output(pass_name=MatrixPass.research, summary=broad_signal.statement, evidence_ids=evidence_ids),
            new_pass_output(pass_name=MatrixPass.provocation, summary="Design a question that makes the pressure speak without coercion.", evidence_ids=evidence_ids),
            new_pass_output(pass_name=MatrixPass.authentication, summary="Validate whether the answer lands in lived detail or performed explanation.", evidence_ids=evidence_ids),
            new_pass_output(pass_name=MatrixPass.primitive, summary="Preserve primitive candidates as upstream operators, not finished content.", evidence_ids=evidence_ids),
            new_pass_output(pass_name=MatrixPass.coalition, summary=coalition.interaction_rationale, evidence_ids=evidence_ids),
            new_pass_output(pass_name=MatrixPass.edge, summary=edge.name, evidence_ids=evidence_ids),
            new_pass_output(pass_name=MatrixPass.routing, summary="Route through recognition edge before derivative packaging.", evidence_ids=evidence_ids),
            new_pass_output(pass_name=MatrixPass.benchmark, summary="Record coalition fatality if pressure dies during execution.", evidence_ids=evidence_ids),
        ]
        return MatrixOfEdgingBrief(
            schema_version="cmf.matrix_of_edging_brief.v1",
            matrix_brief_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=research_field_id,
            guest_dossier_id=guest_dossier.guest_dossier_id,
            audience_reality_brief_id=audience_reality_brief.audience_reality_brief_id,
            context_premise_id=context_premise.context_premise_id,
            trigger_map_id=trigger_map_id,
            status=MatrixBriefStatus.draft,
            pass_outputs=pass_outputs,
            broad_primary_signals=[broad_signal],
            tension_sites=tension_sites,
            primitive_candidates=primitive_candidates,
            coalition_signatures=[coalition],
            edge_products=[edge],
            likely_failure_points=failure_points,
            route_implications=edge.route_implications,
            input_context_hash=matrix_context_hash(input_ids=input_ids, route_seed=edge.name),
            created_by_actor_id=created_by_actor_id,
            created_at=now,
            updated_at=now,
        )

    @staticmethod
    def _primitive_candidates(
        *,
        evidence_ids: list[UUID],
        primitive_refs: list[str],
        force_generic: bool,
    ) -> list[PrimitiveCandidatePacket]:
        candidates: list[PrimitiveCandidatePacket] = []
        for primitive_ref in primitive_refs:
            if ":" in primitive_ref:
                primitive_family, ref = primitive_ref.split(":", 1)
            else:
                primitive_family, ref = "TRG", primitive_ref
            status = PrimitiveCandidateStatus.latent
            weakness = "Needs JIT completion from live guest language."
            if primitive_ref.startswith("unresolved:"):
                status = PrimitiveCandidateStatus.unresolved_registry_ref
                primitive_family = "UNRESOLVED"
                ref = primitive_ref
                weakness = "Primitive registry reference has not been migrated."
            elif force_generic:
                status = PrimitiveCandidateStatus.unsupported
                weakness = "Generic candidate lacks source pressure."
            elif "Vulnerable" in ref:
                status = PrimitiveCandidateStatus.native
                weakness = None
            candidates.append(
                PrimitiveCandidatePacket(
                    schema_version="cmf.primitive_candidate_packet.v1",
                    primitive_candidate_id=uuid4(),
                    primitive_family=primitive_family,
                    primitive_ref=ref,
                    evidence_ids=evidence_ids,
                    status=status,
                    survival_rationale="Survives through evidence fidelity, emotional charge, recognizability, and execution potential.",
                    weakness=weakness,
                )
            )
        return candidates

    @staticmethod
    def _family_ratios(candidates: list[PrimitiveCandidatePacket]) -> dict[str, float]:
        total = len(candidates) or 1
        ratios: dict[str, float] = {}
        for candidate in candidates:
            ratios[candidate.primitive_family] = ratios.get(candidate.primitive_family, 0) + (1 / total)
        return ratios


@dataclass(frozen=True)
class MatrixRSCSEvaluator:
    def evaluate(self, brief: MatrixOfEdgingBrief) -> tuple[MatrixEvaluationScores, list[str], bool]:
        pass_names = {item.pass_name for item in brief.pass_outputs}
        pass_completeness_score = 1.0 if pass_names == set(MatrixPass) else len(pass_names) / len(MatrixPass)
        evidence_ids = {
            evidence_id
            for tension in brief.tension_sites
            for evidence_id in tension.evidence_ids
        }
        saturation_score = 0.9 if len(evidence_ids) >= 2 else 0.45
        anchored = [site for site in brief.tension_sites if site.can_anchor_question and site.evidence_ids]
        collision_strength = max([site.magnitude_score for site in anchored] or [0])
        generic_terms = ["generic", "hook", "better content", "content pillars", "persona"]
        joined = " ".join(
            [
                *[signal.statement for signal in brief.broad_primary_signals],
                *[site.statement for site in brief.tension_sites],
                *brief.route_implications,
            ]
        ).lower()
        specificity_score = 0.35 if any(term in joined for term in generic_terms) else 0.9
        anti_centroid_risk_score = 0.8 if specificity_score < 0.7 or not brief.likely_failure_points else 0.2
        routeability_score = (
            0.9
            if brief.edge_products and brief.coalition_signatures and brief.route_implications
            else 0.35
        )
        scores = MatrixEvaluationScores(
            schema_version="cmf.matrix_evaluation_scores.v1",
            pass_completeness_score=pass_completeness_score,
            saturation_score=saturation_score,
            collision_strength_score=collision_strength,
            specificity_score=specificity_score,
            anti_centroid_risk_score=anti_centroid_risk_score,
            routeability_score=routeability_score,
        )
        failures: list[str] = []
        if pass_completeness_score < 1:
            failures.append("MATRIX_PASS_INCOMPLETE")
        if saturation_score < 0.7:
            failures.append("RSCS_SATURATION_TOO_THIN")
        if collision_strength < 0.7:
            failures.append("COLLISION_STRENGTH_TOO_WEAK")
        if specificity_score < 0.7:
            failures.append("RSCS_SPECIFICITY_FAILED")
        if anti_centroid_risk_score > 0.35:
            failures.append("ANTI_CENTROID_RISK_HIGH")
        if routeability_score < 0.7:
            failures.append("ROUTEABILITY_FAILED")
        if any(site.speculative and site.can_anchor_question for site in brief.tension_sites):
            failures.append("SPECULATIVE_TENSION_CANNOT_ANCHOR")
        passed = not failures
        return scores, failures, passed
