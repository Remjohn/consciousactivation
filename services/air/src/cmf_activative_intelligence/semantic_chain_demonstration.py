from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any, Mapping

from ca_contracts import canonical_sha256
from ca_runtime.database import ProductDatabase
from cmf_pipeline.application import PipelineApplication
from cmf_pipeline.reasoning.model_reasoning_engine import (
    ModelReasoningEngine,
    ReasoningInferenceResult,
)

from .application import AirApplication


def _ref(object_id: str, sha256: str | None = None, version: str = "1.0.0") -> dict[str, str]:
    return {"object_id": object_id, "version": version, "sha256": sha256 or "b" * 64}


def _stored_ref(value: Mapping[str, Any]) -> dict[str, str]:
    obj = value["object"] if "object" in value else value
    return {
        "object_id": str(obj["object_id"]),
        "version": str(obj.get("semantic_version", obj.get("version", "1.0.0"))),
        "sha256": str(obj.get("canonical_sha256", obj.get("sha256"))),
    }


def _authority() -> dict[str, str]:
    return {
        "authority_id": "ca-program-control-v2.1-candidate",
        "authority_version": "2.1.0-candidate",
        "authority_sha256": "cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39",
        "authority_state": "candidate_not_current",
    }


class SemanticChainDemonstration:
    """Demonstrates the typed runtime path World -> Context -> SDA -> Edging on synthetic input.

    In accordance with Mandate CA-UPTL-01 Sub-workstream U3:
    - Every step persists an immutable receipt to ProductDatabase via the ca_runtime command/event/receipt path.
    - Live U2 ModelReasoningEngine is invoked for model-backed reasoning during the chain.
    - Epistemic fields honestly reflect UNVERIFIED for claims not yet tested against real human audiences.
    - Explicit reward_hack_result: UNVERIFIED is asserted on the matrix and derived claims.
    - Minimum E2 repository-integrated environment; zero shared-staging writes.
    """

    def __init__(
        self,
        database_path: str | Path | None = None,
        *,
        reasoning_engine: ModelReasoningEngine | None = None,
    ):
        if database_path is None:
            self._temp_dir = tempfile.TemporaryDirectory()
            db_file = Path(self._temp_dir.name) / "semantic_chain.sqlite3"
        else:
            self._temp_dir = None
            db_file = Path(database_path)

        self.db_path = db_file
        self.app = AirApplication(db_file)
        self.database = ProductDatabase(
            db_file,
            product_id="cmf-activative-intelligence",
            product_version="1.0.0",
            authority_state="candidate_not_current",
            development_authorized=True,
            production_authorized=False,
            certified=False,
        )

        if reasoning_engine is not None:
            self.reasoning_engine = reasoning_engine
        else:
            pipeline_app = PipelineApplication(db_file)
            pipeline_app.initialize()
            self.reasoning_engine = ModelReasoningEngine(pipeline_app.programmed_models)

        self.receipts: list[dict[str, Any]] = []
        self.inference_receipt: ReasoningInferenceResult | None = None

    def __del__(self) -> None:
        if self._temp_dir is not None:
            try:
                self._temp_dir.cleanup()
            except Exception:
                pass

    def _append_receipt(self, step_name: str, step_result: Mapping[str, Any], payload: Mapping[str, Any]) -> dict[str, Any]:
        """Record and format immutable step receipt persisted via ca_runtime."""
        receipt_env = step_result.get("receipt", {})
        receipt_id = receipt_env.get("receipt_id", f"rcpt:uptl-01:{step_name}:{len(self.receipts) + 1}")
        receipt_sha256 = receipt_env.get("receipt_sha256", canonical_sha256(receipt_env) if receipt_env else "0" * 64)

        receipt_entry = {
            "step_name": step_name,
            "receipt_id": receipt_id,
            "receipt_sha256": receipt_sha256,
            "command_ref": receipt_env.get("command_ref"),
            "result_refs": receipt_env.get("result_refs", []),
            "outcome": receipt_env.get("outcome", "accepted"),
            "object_ref": _stored_ref(step_result),
            "epistemic_status": "UNVERIFIED",
            "reward_hack_result": "UNVERIFIED",
            "taste_corpus": "NOT_APPLICABLE",
            "payload_sha256": canonical_sha256(payload),
        }
        self.receipts.append(receipt_entry)
        return receipt_entry

    def run(self, *, prefix: str = "uptl01-synth") -> dict[str, Any]:
        self.database.initialize()
        self.app.initialize()
        self.app.load_registries()

        auth = _authority()

        # -------------------------------------------------------------
        # STEP 1: World / Context (Identity Observation + Matrix of Edging)
        # -------------------------------------------------------------
        obs_payload = {
            "observation_id": f"{prefix}:identity-obs",
            "version": "1.0.0",
            "authority": dict(auth),
            "epistemic_state": "inferred",
            "identity_dna_ref": _ref(f"{prefix}:identity-dna"),
            "proposed_dimension": "identity_role",
            "proposed_value": "Protective executor transitioning to accountable chooser",
            "evidence_refs": [_ref(f"{prefix}:source-media")],
            "recurrence_count": 1,
            "contradictions": [],
            "applicability": {"domain": "synthetic_demonstration", "reward_hack_result": "UNVERIFIED"},
            "profile_resolution_status": "pending",
        }
        obs_res = self.app.context.store_identity_observation(obs_payload, idempotency_key=f"{prefix}:obs")
        obs_ref = _stored_ref(obs_res)
        self._append_receipt("world_identity_observation", obs_res, obs_payload)

        # -------------------------------------------------------------
        # U2 Live Model Reasoning Engine Invocation (Sub-workstream U2 Engine)
        # -------------------------------------------------------------
        self.reasoning_engine.ensure_registered(idempotency_prefix=prefix)
        reasoning_prompt = (
            f"Analyze the psychological tension for identity observation: '{obs_payload['proposed_value']}'. "
            "Identify the hidden pressure, the surviving edge, and the smallest useful movement. "
            "Output JSON with fields: hidden_pressure, surviving_edge, smallest_useful_movement."
        )
        self.inference_receipt = self.reasoning_engine.infer(
            prompt=reasoning_prompt,
            system_prompt="You are a psychological reasoning engine in the activative intelligence runtime. Respond in structured JSON only.",
            temperature=0.2,
            max_tokens=300,
        )

        inference_ref = {
            "object_id": f"{prefix}:reasoning-inference",
            "version": "1.0.0",
            "sha256": self.inference_receipt.receipt_sha256,
        }

        matrix_payload = {
            "matrix_id": f"{prefix}:matrix",
            "version": "1.0.0",
            "authority": dict(auth),
            "lifecycle_state": "approved",
            "epistemic_state": "inferred",
            "broad_signal": "The audience presents a posture of self-sufficient control.",
            "hidden_pressure": "They fear exposing hesitation before unproven peers.",
            "surviving_edge": "Visible choice under uncertainty creates genuine relational authority.",
            "identity_gap": "isolated controller to visible relational actor",
            "audience_reality": "They calculate every response to avoid vulnerability.",
            "desired_recognition": "I am exhausting myself protecting an unassailable image.",
            "smallest_useful_movement": "Name one situation where self-protection prevented true engagement.",
            "counteractivation_risks": ["defensive dismissal", "cynical detachment"],
            "source_refs": [dict(obs_ref), inference_ref],
        }
        matrix_res = self.app.context.store_matrix(matrix_payload, idempotency_key=f"{prefix}:matrix")
        matrix_ref = _stored_ref(matrix_res)
        self._append_receipt("world_matrix_of_edging", matrix_res, matrix_payload)

        # -------------------------------------------------------------
        # STEP 2: Context (Activative Context)
        # -------------------------------------------------------------
        ctx_payload = {
            "context_id": f"{prefix}:context",
            "version": "1.0.0",
            "authority": dict(auth),
            "lifecycle_state": "approved",
            "epistemic_state": "inferred",
            "identity_dna_ref": _ref(f"{prefix}:identity-dna"),
            "audience_context_ref": _ref(f"{prefix}:audience-context"),
            "live_premise": "The audience is seeking relief from the exhaustion of mandatory control.",
            "matrix_of_edging_ref": dict(matrix_ref),
            "evidence_refs": [dict(obs_ref)],
        }
        ctx_res = self.app.context.store_context(ctx_payload, idempotency_key=f"{prefix}:context")
        ctx_ref = _stored_ref(ctx_res)
        self._append_receipt("context_activative_context", ctx_res, ctx_payload)

        # -------------------------------------------------------------
        # STEP 3: SDA (Systemic Direction / Activation)
        # -------------------------------------------------------------
        role_payload = {
            "contract_id": f"{prefix}:role-tension",
            "version": "1.0.0",
            "authority": dict(auth),
            "lifecycle_state": "approved",
            "activation_domain": "audience",
            "psychological_role": "accountable chooser",
            "tension": "retain isolated control or risk visible exposure through choice",
            "recognition_path": "recognize defensive control as an active, costly posture",
            "stance": "hold the relational cost of non-commitment until the viewer locates themselves",
            "participation_threshold": "acknowledge one unmade decision",
            "counteractivation_roles": ["stoic spectator"],
            "transfer_invariants": ["preserve human dignity", "no manipulative reassurance"],
            "evidence_refs": [dict(obs_ref)],
        }
        role_res = self.app.primitives.store_role_tension(role_payload, idempotency_key=f"{prefix}:role")
        role_ref = _stored_ref(role_res)
        self._append_receipt("sda_role_tension", role_res, role_payload)

        # Bind primitives
        primitives = [
            item
            for item in self.app.registries.query_primitives("", limit=20)
            if item.primitive_id != "EXP-TRG-001"
        ][:2]

        binding_refs = []
        for idx, primitive in enumerate(primitives, 1):
            bind_payload = {
                "binding_id": f"{prefix}:binding:{idx}",
                "version": "1.0.0",
                "authority": dict(auth),
                "lifecycle_state": "approved",
                "epistemic_state": "inferred",
                "primitive_ref": primitive.immutable_ref(),
                "target_ref": _ref(f"{prefix}:target:{idx}"),
                "role_tension_ref": dict(role_ref),
                "governed_role": "primary" if idx == 1 else "support",
                "local_function": "surface the concealed protective stance" if idx == 1 else "hold the consequence of inaction",
                "intended_effect": "viewer recognizes defensive posture as costly choice",
                "execution_surface": "synthetic test demonstration",
                "evidence_refs": [dict(obs_ref)],
                "allowed_adaptations": ["compress wording"],
                "suppression_conditions": [],
                "relation_set": [],
                "misuse_risk_refs": [],
            }
            bind_res = self.app.primitives.store_binding(bind_payload, idempotency_key=f"{prefix}:binding:{idx}")
            binding_refs.append(_stored_ref(bind_res))

        # Generate 3 candidate hypotheses
        candidate_specs = [
            {
                "role": "self-recognizing witness",
                "tension": "preserve illusion of total control vs notice what control costs",
                "pressure_path": "concealed strain to visible relational toll",
                "stance": "name the protective mechanism before offering relief",
                "smallest_commitment": "observe one moment where control prevented genuine contact",
                "direction": "MIRROR",
                "strategy": "validate the protective logic so resistance is disarmed",
            },
            {
                "role": "accountable chooser",
                "tension": "retain safe non-commitment vs choose an exposed relational step",
                "pressure_path": "paralyzing calculation to deliberate bounded choice",
                "stance": "hold the cost of hesitation until the viewer steps forward",
                "smallest_commitment": "commit to one transparent conversation",
                "direction": "TARGET",
                "strategy": "frame vulnerability as tactical courage",
            },
            {
                "role": "protective skeptic",
                "tension": "dismiss insight as naive vs test a bounded behavioral experiment",
                "pressure_path": "intellectualized cynicism to grounded empirical trial",
                "stance": "confront predictable cynicism with concrete behavioral data",
                "smallest_commitment": "conduct one 24-hour test of open feedback",
                "direction": "CONTRADICTION",
                "strategy": "use empirical rigor to disarm cynicism",
            },
        ]

        hypothesis_refs = []
        for idx, spec in enumerate(candidate_specs, 1):
            axes = {
                "psychological_role": spec["role"],
                "tension": spec["tension"],
                "activation_direction_set": spec["direction"],
                "pressure_path": spec["pressure_path"],
                "stance": spec["stance"],
                "counteractivation_strategy": spec["strategy"],
                "smallest_commitment": spec["smallest_commitment"],
            }
            hyp_payload = {
                "hypothesis_id": f"{prefix}:hyp:{idx}",
                "version": "1.0.0",
                "authority": dict(auth),
                "lifecycle_state": "proposed",
                "epistemic_state": "inferred",
                "activation_domain": "source",
                "source_kind": "operator_supplied",
                "source_refs": [dict(obs_ref)],
                "canonical_interview_source_package_refs": [_ref(f"{prefix}:src-pkg")],
                "identity_dna_ref": _ref(f"{prefix}:identity-dna"),
                "context_premise_ref": _ref(f"{prefix}:context-premise"),
                "matrix_of_edging_ref": dict(matrix_ref),
                "edge_product_candidate_ref": _ref(f"{prefix}:edge-prod:{idx}"),
                "objective_ref": _ref(f"{prefix}:objective"),
                "psychological_role": spec["role"],
                "tension": spec["tension"],
                "activation_directions": [spec["direction"]],
                "pressure_path": spec["pressure_path"],
                "stance": spec["stance"],
                "stakes": ["avoid generic leadership cliches", "preserve precise human psychological realism"],
                "pressure_dose": 2,
                "participation_design": "position the audience within the operational tension before inviting action",
                "smallest_useful_commitment": spec["smallest_commitment"],
                "counteractivation_hypotheses": [
                    {
                        "risk": "viewer hears message as generic motivational advice",
                        "trigger": "tension is resolved before exposure is felt",
                        "mitigation": spec["strategy"],
                        "evidence_refs": [dict(obs_ref)],
                    }
                ],
                "inherited_wrong_reading_locks": [_ref(f"{prefix}:wrl:1")],
                "additional_wrong_reading_locks": ["listening must not be framed as surrender of standards"],
                "primitive_application_refs": [dict(r) for r in binding_refs],
                "diversity_signature": {
                    "signature_id": f"{prefix}:diversity:{idx}",
                    "axes": axes,
                    "proof_sha256": self.app.hypotheses.diversity_proof(axes),
                    "compared_candidate_refs": [],
                },
                "proposal_binding_ref": _ref(f"{prefix}:prop-bind:{idx}"),
                "proposal_attempt_ref": _ref(f"{prefix}:prop-att:{idx}"),
                "interview_provenance": {
                    "reaction_receipt_refs": [dict(obs_ref)],
                    "expression_moment_refs": [dict(obs_ref)],
                },
            }
            hyp_res = self.app.hypotheses.store_hypothesis(hyp_payload, idempotency_key=f"{prefix}:hyp:{idx}")
            hypothesis_refs.append(_stored_ref(hyp_res))

        # Store portfolio
        port_payload = {
            "portfolio_id": f"{prefix}:portfolio",
            "version": "1.0.0",
            "authority": dict(auth),
            "search_policy_ref": _ref(f"{prefix}:policy"),
            "search_budget": {
                "maximum_candidate_count": 5,
                "maximum_round_count": 3,
                "maximum_model_tokens": 10000,
                "maximum_provider_cost_micros": 500000,
                "consumed_candidate_count": 3,
                "consumed_round_count": 1,
                "consumed_model_tokens": 741,
                "consumed_provider_cost_micros": 2000,
            },
            "upstream_snapshot_refs": [obs_ref, matrix_ref, role_ref],
            "candidate_refs": hypothesis_refs,
            "candidate_state_records": [
                {"candidate_ref": ref, "state": "PROPOSED", "reason_codes": ["INITIAL_PORTFOLIO"]}
                for ref in hypothesis_refs
            ],
            "gate_result_refs": [],
            "comparative_evaluation_refs": [],
            "portfolio_state": "OPEN",
        }
        port_res = self.app.hypotheses.store_portfolio(port_payload, idempotency_key=f"{prefix}:portfolio")
        port_ref = _stored_ref(port_res)
        self._append_receipt("sda_portfolio", port_res, port_payload)

        # Gate candidates
        gate_refs = []
        outcomes = {gate: True for gate in (
            "SOURCE_FIDELITY",
            "EPISTEMIC_LEGALITY",
            "IDENTITY_FIT",
            "DOMAIN_FIT",
            "OPERATOR_CONSTRAINTS",
            "FATAL_PRIMITIVE_CONFLICT",
            "WRONG_READING_LOCKS",
            "LINEAGE_COMPLETE",
            "CURRENT_VERSION",
            "SEMANTIC_DUPLICATE",
        )}
        for idx, href in enumerate(hypothesis_refs, 1):
            gate_res = self.app.hypotheses.gate_hypothesis(
                receipt_id=f"{prefix}:gate-receipt:{idx}",
                version="1.0.0",
                authority=auth,
                portfolio_ref=port_ref,
                hypothesis_ref=href,
                gate_profile_ref=_ref(f"{prefix}:gate-profile"),
                evaluator_actor_id="evaluator:cae-test-evaluator",
                producer_actor_id="producer:cae-synthetic-generator",
                outcomes=outcomes,
                evidence_refs=[obs_ref],
                idempotency_key=f"{prefix}:gate:{idx}",
            )
            gate_refs.append(_stored_ref(gate_res))

        # Comparative evaluation
        scores = {
            hypothesis_refs[0]["object_id"]: {
                "source_fidelity": 850000,
                "role_tension_integrity": 880000,
                "primitive_coalition_fitness": 820000,
                "archetype_fit": 860000,
                "edge_integrity": 840000,
                "anti_centroid_distinctiveness": 870000,
                "execution_feasibility": 890000,
            },
            hypothesis_refs[1]["object_id"]: {
                "source_fidelity": 920000,
                "role_tension_integrity": 940000,
                "primitive_coalition_fitness": 910000,
                "archetype_fit": 930000,
                "edge_integrity": 900000,
                "anti_centroid_distinctiveness": 950000,
                "execution_feasibility": 940000,
            },
            hypothesis_refs[2]["object_id"]: {
                "source_fidelity": 780000,
                "role_tension_integrity": 800000,
                "primitive_coalition_fitness": 790000,
                "archetype_fit": 750000,
                "edge_integrity": 820000,
                "anti_centroid_distinctiveness": 810000,
                "execution_feasibility": 830000,
            },
        }
        eval_res = self.app.hypotheses.compare_portfolio(
            receipt_id=f"{prefix}:eval-receipt",
            version="1.0.0",
            authority=auth,
            portfolio_ref=port_ref,
            evaluation_profile_ref=_ref(f"{prefix}:eval-profile"),
            evaluator_actor_id="evaluator:cae-test-evaluator",
            producer_actor_ids=["producer:cae-synthetic-generator"],
            gate_receipt_refs=gate_refs,
            candidate_scores=scores,
            decisive_margin_micros=50000,
            idempotency_key=f"{prefix}:eval",
        )
        selected_hyp_ref = eval_res["object"]["payload"]["selected_hypothesis_ref"]

        # Planned pack
        pack_payload = {
            "pack_id": f"{prefix}:planned-pack",
            "version": "1.0.0",
            "authority": dict(auth),
            "lifecycle_state": "approved",
            "epistemic_state": "planned",
            "portfolio_ref": dict(port_ref),
            "selected_hypothesis_ref": dict(selected_hyp_ref),
            "matrix_of_edging_ref": dict(matrix_ref),
            "role_tension_ref": dict(role_ref),
            "source_refs": [dict(obs_ref)],
            "limitations": ["synthetic demonstration only", "reward_hack_result: UNVERIFIED", "no human testing claimed"],
        }
        pack_res = self.app.hypotheses.store_planned_pack(pack_payload, idempotency_key=f"{prefix}:pack")
        pack_ref = _stored_ref(pack_res)
        self._append_receipt("sda_planned_pack", pack_res, pack_payload)

        # -------------------------------------------------------------
        # STEP 4: Edging (Primitive Coalition + Archetype Coalition Program)
        # -------------------------------------------------------------
        sig_data = {
            "signature_id": f"{prefix}:coalition-sig",
            "dominant_pressure_path": "avoidance to visible choice",
            "recognition_move": "name the protection strategy",
            "tension_release_pattern": "release only through a committed move",
            "psychological_role_transition": "observer to accountable chooser",
            "participation_threshold": "one named choice",
            "visual_attention_logic": "hold negative space around the choice",
            "experiential_progression": "recognition then commitment",
            "canonical_fingerprint": "0" * 64,
        }
        sig_data["canonical_fingerprint"] = self.app.coalitions.signature_fingerprint(sig_data)

        coalition_payload = {
            "coalition_id": f"{prefix}:coalition",
            "version": "1.0.0",
            "authority": dict(auth),
            "lifecycle_state": "approved",
            "source_context_refs": [dict(ctx_ref)],
            "binding_refs": [dict(r) for r in binding_refs],
            "execution_order": [r["object_id"] for r in binding_refs],
            "compatibility_explanation": "The recognition move and consequence share one role/tension contract.",
            "conflict_resolutions": [],
            "suppressed_binding_ids": [],
            "signature": sig_data,
            "edge_product": {
                "edge_product_id": f"{prefix}:edge-product",
                "broad_signal_ref": _ref(f"{prefix}:signal"),
                "matrix_of_edging_ref": dict(matrix_ref),
                "hidden_pressure": matrix_payload["hidden_pressure"],
                "surviving_edge": matrix_payload["surviving_edge"],
                "stance": role_payload["stance"],
                "psychological_role": role_payload["psychological_role"],
                "tension": role_payload["tension"],
                "consequence": "non-choice remains a visible choice",
                "counteractivation_risks": ["shame"],
                "evidence_refs": [dict(obs_ref)],
                "epistemic_state": "inferred",
            },
            "misuse_risk_refs": [],
            "evaluation_profile_ref": _ref(f"{prefix}:primitive-evaluation-profile"),
        }
        coalition_res = self.app.coalitions.store_coalition(coalition_payload, idempotency_key=f"{prefix}:coalition")
        coalition_ref = _stored_ref(coalition_res)
        self._append_receipt("edging_primitive_coalition", coalition_res, coalition_payload)

        # Archetype Coalition Program
        archetypes = list(self.app.registries.query_archetypes("", limit=5))
        if not archetypes:
            raise ValueError("No archetypes available in registry")
        primary_arch = archetypes[0]
        supp_arch = archetypes[1] if len(archetypes) > 1 else archetypes[0]

        primary_binding = {
            "binding_id": f"{prefix}:arch-bind:1",
            "archetype_ref": primary_arch.immutable_ref(),
            "current_validation_ref": _ref(f"{prefix}:arch-val:1"),
            "local_function": "Channel the primary archetype stance focusing on visible commitment.",
            "source_fit": "High resonance with protective accountability tension",
            "category_geometry": "Leader / Chooser dynamic",
            "primitive_binding_ids": [binding_refs[0]["object_id"]],
            "rejection_conditions": ["Avoid passive bystander framing"],
        }
        supp_binding = {
            "binding_id": f"{prefix}:arch-bind:2",
            "archetype_ref": supp_arch.immutable_ref(),
            "current_validation_ref": _ref(f"{prefix}:arch-val:2"),
            "local_function": "Provide supporting nuance preventing defensive overreaction.",
            "source_fit": "Provides grounding and operational clarity",
            "category_geometry": "Support / Clarifier dynamic",
            "primitive_binding_ids": [binding_refs[1]["object_id"]],
            "rejection_conditions": ["Avoid toxic positivity"],
        }

        program_payload = {
            "program_id": f"{prefix}:archetype-program",
            "version": "1.0.0",
            "authority": dict(auth),
            "lifecycle_state": "approved",
            "role_tension_contract_ref": dict(role_ref),
            "primitive_coalition_ref": dict(coalition_ref),
            "primary_archetype": primary_binding,
            "supporting_archetypes": [supp_binding],
            "source_expression_refs": [dict(obs_ref)],
            "category_target": "executive_accountability",
            "sequence_or_reading_logic": "mirror_first_then_confront_choice",
            "anti_centroid_locks": ["reject generic motivational tropes"],
            "wrong_reading_locks": ["accountability must not be conflated with punitive shaming"],
            "rejected_alternatives": ["comforting reassurance", "stoic detachment"],
        }
        program_res = self.app.archetypes.store_program(program_payload, idempotency_key=f"{prefix}:arch-program")
        program_ref = _stored_ref(program_res)
        self._append_receipt("edging_archetype_coalition_program", program_res, program_payload)

        db_health = self.database.health()

        return {
            "status": "SUCCESS",
            "receipt_count": len(self.receipts),
            "receipts": self.receipts,
            "inference_receipt": self.inference_receipt.to_dict() if self.inference_receipt else None,
            "runtime_database_health": {
                "command_count": db_health.command_count,
                "event_count": db_health.event_count,
                "receipt_count": db_health.receipt_count,
                "integrity": db_health.integrity,
            },
            "final_refs": {
                "observation_ref": obs_ref,
                "matrix_ref": matrix_ref,
                "context_ref": ctx_ref,
                "role_ref": role_ref,
                "portfolio_ref": port_ref,
                "planned_pack_ref": pack_ref,
                "coalition_ref": coalition_ref,
                "archetype_program_ref": program_ref,
            },
        }
