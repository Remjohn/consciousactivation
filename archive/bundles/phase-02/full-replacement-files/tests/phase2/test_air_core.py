from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from _support import AUTHORITY, ROOT, base, ref  # type: ignore
from ca_contracts import canonical_sha256
from cmf_activative_intelligence.application import AirApplication
from cmf_activative_intelligence.domain import (
    ActivationDomain,
    AirValidationError,
    EpistemicState,
    require_epistemic_transition,
    schema_registry,
    supported_object_types,
    validate_air_object,
)
from cmf_activative_intelligence.repositories.air_repository import ObjectVersionConflict
from cmf_activative_intelligence.repositories.registry_repository import AirRepositoryError


class AirDomainTests(unittest.TestCase):
    def test_activation_domains_are_complete(self) -> None:
        self.assertEqual(
            {item.value for item in ActivationDomain},
            {"source", "relationship", "audience", "campaign", "derivative"},
        )

    def test_epistemic_transition_requires_operator_evidence(self) -> None:
        with self.assertRaises(AirValidationError):
            require_epistemic_transition("inferred", "operator_confirmed")
        require_epistemic_transition(
            "inferred",
            "operator_confirmed",
            evidence_refs=[ref("evidence:1")],
            operator_decision_ref=ref("decision:1"),
        )

    def test_planned_cannot_become_observed(self) -> None:
        with self.assertRaises(AirValidationError):
            require_epistemic_transition(
                EpistemicState.PLANNED.value,
                EpistemicState.OBSERVED.value,
                evidence_refs=[ref("evidence:1")],
            )

    def test_schemas_are_closed_and_cover_all_objects(self) -> None:
        schemas = schema_registry()
        self.assertEqual(set(schemas), set(supported_object_types()))
        self.assertTrue(all(item["additionalProperties"] is False for item in schemas.values()))

    def test_role_and_tension_must_be_distinct(self) -> None:
        payload = {
            **base("contract_id", "role:bad", epistemic=False),
            "activation_domain": "audience",
            "psychological_role": "witness",
            "tension": "witness",
            "recognition_path": "recognize the concealed cost",
            "stance": "stand inside the unresolved choice",
            "participation_threshold": "name the smallest move",
            "counteractivation_roles": [],
            "transfer_invariants": ["preserve the unresolved choice"],
            "evidence_refs": [ref("evidence:role")],
        }
        with self.assertRaises(AirValidationError):
            validate_air_object("psychological_role_tension_contract", payload)

    def test_human_resolution_cannot_claim_automatic_promotion(self) -> None:
        payload = {
            **base("episode_id", "resolution:bad"),
            "before_state_refs": [ref("before:1")],
            "operator_request": "move the tension earlier",
            "interpreted_target": "sequence pressure",
            "exact_changes": [{"operation": "move", "target_ref": ref("node:1"), "parameter_changes": {"index": 1}}],
            "tools_invoked": ["studio"],
            "models_or_runtimes": [],
            "context_refs": [],
            "invariants": ["preserve source fidelity"],
            "required_transformations": ["reorder"],
            "creative_freedom": [],
            "wrong_reading_locks": ["do not flatten tension"],
            "result_refs": [],
            "evaluation_refs": [],
            "operator_verdict": "approved",
            "applicability_scope": {"campaign": "reference"},
            "programming_material_dispositions": ["capture_episode"],
            "promotion_status": "promoted",
        }
        with self.assertRaises(AirValidationError):
            validate_air_object("human_resolution_episode", payload)


class AirRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.app = AirApplication(Path(self.temp.name) / "air.sqlite")
        self.app.initialize()
        self.result = self.app.load_registries()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_exact_inventory_counts_and_duplicate_preservation(self) -> None:
        primitive = self.result["primitive_registry"]
        self.assertEqual(primitive["item_count"], 243)
        self.assertEqual(primitive["unique_primitive_id_count"], 242)
        self.assertEqual(primitive["duplicate_primitive_id_count"], 1)
        self.assertEqual(self.result["archetype_registry"]["item_count"], 96)

    def test_duplicate_id_requires_source_hash(self) -> None:
        with self.assertRaises(AirRepositoryError):
            self.app.registries.get_primitive("EXP-TRG-001")
        matches = self.app.registries.query_primitives("EXP-TRG-001", limit=10)
        self.assertEqual(len(matches), 2)
        selected = self.app.registries.get_primitive(
            "EXP-TRG-001", source_sha256=matches[0].source_sha256
        )
        self.assertEqual(selected.source_sha256, matches[0].source_sha256)

    def test_archetypes_remain_historical_evidence(self) -> None:
        status = self.app.registries.status()
        self.assertFalse(status["historical_archetypes_are_current_authority"])
        self.assertEqual(status["archetype_count"], 96)


class AirSemanticFlowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.app = AirApplication(Path(self.temp.name) / "air.sqlite")
        self.app.initialize()
        self.app.load_registries()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _store(self, object_type: str, payload: dict[str, object], key: str) -> dict[str, object]:
        return self.app.store(object_type, payload, idempotency_key=key)

    def test_end_to_end_semantic_core(self) -> None:
        matrix_payload = {
            **base("matrix_id", "matrix:reference"),
            "broad_signal": "The audience says they need more confidence.",
            "hidden_pressure": "They fear choosing publicly and being wrong.",
            "surviving_edge": "Confidence follows a visible committed move.",
            "identity_gap": "observer to accountable chooser",
            "audience_reality": "They already know the options but avoid exposure.",
            "desired_recognition": "I am protecting myself from being seen choosing.",
            "smallest_useful_movement": "Name one choice and its cost.",
            "counteractivation_risks": ["shame", "premature certainty"],
            "source_refs": [ref("source:expression")],
        }
        matrix = self._store("matrix_of_edging", matrix_payload, "matrix-1")["object"]
        matrix_ref = ref(matrix["object_id"], matrix["canonical_sha256"])

        context_payload = {
            **base("context_id", "context:reference"),
            "identity_dna_ref": ref("identity:dna"),
            "audience_context_ref": ref("audience:context"),
            "live_premise": "The person is not confused; they are avoiding exposure.",
            "matrix_of_edging_ref": matrix_ref,
            "evidence_refs": [ref("source:expression")],
        }
        context = self._store("activative_context", context_payload, "context-1")["object"]
        context_ref = ref(context["object_id"], context["canonical_sha256"])

        role_payload = {
            **base("contract_id", "role:reference", epistemic=False),
            "activation_domain": "audience",
            "psychological_role": "accountable chooser",
            "tension": "remain protected or become visible through a choice",
            "recognition_path": "recognize avoidance as a choice",
            "stance": "stand inside the cost of non-choice",
            "participation_threshold": "name one choice",
            "counteractivation_roles": ["judged failure"],
            "transfer_invariants": ["preserve agency", "preserve unresolved cost"],
            "evidence_refs": [ref("source:expression")],
        }
        role = self._store("psychological_role_tension_contract", role_payload, "role-1")["object"]
        role_ref = ref(role["object_id"], role["canonical_sha256"])

        primitives = [item for item in self.app.registries.query_primitives("", limit=20) if item.primitive_id != "EXP-TRG-001"][:2]
        self.assertEqual(len(primitives), 2)
        bindings = []
        for index, primitive in enumerate(primitives, 1):
            binding_payload = {
                **base("binding_id", f"binding:{index}"),
                "primitive_ref": primitive.immutable_ref(),
                "target_ref": ref("derivative:reference"),
                "role_tension_ref": role_ref,
                "governed_role": "primary" if index == 1 else "support",
                "local_function": "surface the concealed choice" if index == 1 else "hold the consequence",
                "intended_effect": "viewer recognizes their position",
                "execution_surface": "semantic production program",
                "evidence_refs": [ref("source:expression")],
                "allowed_adaptations": ["compress wording"],
                "suppression_conditions": [],
                "relation_set": [],
                "misuse_risk_refs": [],
            }
            stored = self._store("primitive_binding", binding_payload, f"binding-{index}")["object"]
            bindings.append(stored)

        signature = {
            "signature_id": "signature:reference",
            "dominant_pressure_path": "avoidance to visible choice",
            "recognition_move": "name the protection strategy",
            "tension_release_pattern": "release only through a committed move",
            "psychological_role_transition": "observer to accountable chooser",
            "participation_threshold": "one named choice",
            "visual_attention_logic": "hold negative space around the choice",
            "experiential_progression": "recognition then commitment",
            "canonical_fingerprint": "0" * 64,
        }
        signature["canonical_fingerprint"] = self.app.coalitions.signature_fingerprint(signature)
        edge_product = {
            "edge_product_id": "edge:reference",
            "broad_signal_ref": ref("signal:confidence"),
            "matrix_of_edging_ref": matrix_ref,
            "hidden_pressure": matrix_payload["hidden_pressure"],
            "surviving_edge": matrix_payload["surviving_edge"],
            "stance": role_payload["stance"],
            "psychological_role": role_payload["psychological_role"],
            "tension": role_payload["tension"],
            "consequence": "non-choice remains a visible choice",
            "counteractivation_risks": ["shame"],
            "evidence_refs": [ref("source:expression")],
            "epistemic_state": "operator_confirmed",
        }
        coalition_payload = {
            **base("coalition_id", "coalition:reference", epistemic=False),
            "source_context_refs": [context_ref],
            "binding_refs": [ref(item["object_id"], item["canonical_sha256"]) for item in bindings],
            "execution_order": [item["object_id"] for item in bindings],
            "compatibility_explanation": "Primary recognition move and support consequence share one role/tension contract.",
            "conflict_resolutions": [],
            "suppressed_binding_ids": [],
            "signature": signature,
            "edge_product": edge_product,
            "misuse_risk_refs": [],
            "evaluation_profile_ref": ref("evaluation:primitive-coalition"),
        }
        coalition = self._store("primitive_coalition_contract", coalition_payload, "coalition-1")["object"]
        coalition_ref = ref(coalition["object_id"], coalition["canonical_sha256"])

        archetype = self.app.registries.query_archetypes("", limit=1)[0]
        archetype_payload = {
            **base("program_id", "archetype-program:reference", epistemic=False),
            "role_tension_contract_ref": role_ref,
            "primitive_coalition_ref": coalition_ref,
            "primary_archetype": {
                "binding_id": "archetype-binding:primary",
                "archetype_ref": archetype.immutable_ref(),
                "current_validation_ref": ref("validation:archetype-current"),
                "local_function": "structure recognition before resolution",
                "source_fit": "matches the expression evidence",
                "category_geometry": "source-led short",
                "primitive_binding_ids": [item["object_id"] for item in bindings],
                "rejection_conditions": ["generic motivational flattening"],
            },
            "supporting_archetypes": [],
            "source_expression_refs": [ref("source:expression")],
            "category_target": "format07_direct_coaching_a_roll",
            "sequence_or_reading_logic": "source expression, recognition, consequence, smallest move",
            "anti_centroid_locks": ["do not average the stance"],
            "wrong_reading_locks": ["not a confidence tip"],
            "rejected_alternatives": ["generic listicle"],
        }
        program = self._store("archetype_coalition_program", archetype_payload, "archetype-1")["object"]
        self.assertEqual(program["object_type"], "archetype_coalition_program")

        brand_payload = {
            **base("brand_context_id", "brand:reference"),
            "brand_genesis_session_ref": ref("brand-genesis:1"),
            "identity_truths": ["activation before advice"],
            "audience_relationship": "credible challenger",
            "positioning_tension": "human truth versus generic content",
            "source_refs": [ref("brand-source:1")],
        }
        brand = self._store("brand_context_version", brand_payload, "brand-1")["object"]
        brand_ref = ref(brand["object_id"], brand["canonical_sha256"])

        voice_payload = {
            **base("voice_dna_id", "voice:reference"),
            "brand_context_ref": brand_ref,
            "vocabulary_patterns": ["concrete pressure language"],
            "rhythm_patterns": ["short assertion then consequence"],
            "sentence_pressure_patterns": ["name the concealed tradeoff"],
            "stance_patterns": ["direct without theatrical certainty"],
            "specificity_patterns": ["name exact source behavior"],
            "metaphor_range": ["bounded lived metaphors"],
            "emotional_distance": "close but not confessional by default",
            "prohibited_centroid_patterns": ["generic inspiration"],
            "source_evidence_refs": [ref("voice-source:1")],
        }
        voice = self._store("voice_dna", voice_payload, "voice-1")["object"]
        self.assertEqual(voice["object_type"], "voice_dna")

        visual_payload = {
            **base("visual_dna_id", "visual:reference"),
            "brand_context_ref": brand_ref,
            "real_life_reference_refs": [ref("visual-reference:1")],
            "subject_treatment": ["human evidence before decoration"],
            "visual_temperature": ["restrained tension"],
            "materiality": ["documentary texture"],
            "composition_tendencies": ["asymmetric pressure"],
            "negative_space_functions": ["hold the unresolved choice"],
            "edge_behaviors": ["preserve edge integrity"],
            "typographic_posture": ["specific and quiet"],
            "motion_character": ["bounded intentional movement"],
            "prohibited_centroid_defaults": ["centered generic card"],
        }
        visual = self._store("visual_dna", visual_payload, "visual-1")["object"]
        self.assertEqual(visual["object_type"], "visual_dna")

        health = self.app.repository.health()
        self.assertEqual(health["integrity"], "ok")
        self.assertGreaterEqual(health["semantic_object_count"], 9)
        self.assertEqual(health["primitive_count"], 243)
        self.assertEqual(health["archetype_count"], 96)

    def test_idempotent_replay_and_revision_conflict(self) -> None:
        payload = {
            **base("matrix_id", "matrix:idempotent"),
            "broad_signal": "signal",
            "hidden_pressure": "pressure",
            "surviving_edge": "edge",
            "identity_gap": "gap",
            "audience_reality": "reality",
            "desired_recognition": "recognition",
            "smallest_useful_movement": "movement",
            "counteractivation_risks": [],
            "source_refs": [ref("source:1")],
        }
        first = self._store("matrix_of_edging", payload, "same-key")
        second = self._store("matrix_of_edging", payload, "same-key")
        self.assertFalse(first["idempotent_replay"])
        self.assertTrue(second["idempotent_replay"])
        changed = dict(payload)
        changed["surviving_edge"] = "new edge"
        changed["supersedes_ref"] = ref(first["object"]["object_id"], first["object"]["canonical_sha256"])
        with self.assertRaises(ObjectVersionConflict):
            self.app.store("matrix_of_edging", changed, idempotency_key="revision", expected_revision=0)

    def test_failure_routing_preserves_product_sovereignty(self) -> None:
        failure_payload = {
            **base("failure_id", "failure:vae", epistemic=False, lifecycle=False),
            "failed_object_ref": ref("artifact:1"),
            "observed_symptom": "visual realization violates composition contract",
            "responsible_layer": "vae.production",
            "owner_product": "visual-asset-editor",
            "evidence_refs": [ref("evaluation:1")],
            "preserved_property_refs": [],
            "invalidated_descendant_refs": [],
            "confidence_bps": 9000,
            "status": "confirmed",
        }
        failure = self._store("failure_attribution", failure_payload, "failure-1")["object"]
        repair_payload = {
            **base("repair_id", "repair:vae", epistemic=False, lifecycle=False),
            "failure_ref": ref(failure["object_id"], failure["canonical_sha256"]),
            "responsible_layer": "vae.production",
            "owner_product": "visual-asset-editor",
            "repair_mode": "owner_referral",
            "target_refs": [ref("artifact:1")],
            "allowed_operations": ["submit typed repair demand"],
            "protected_refs": [],
            "rerun_node_refs": [],
        }
        repair = self._store("repair_program", repair_payload, "repair-1")["object"]
        self.assertEqual(repair["payload"]["repair_mode"], "owner_referral")


class AirCliTests(unittest.TestCase):
    def _env(self, data_root: str) -> dict[str, str]:
        import os
        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join(
            str(path)
            for path in (
                ROOT / "packages" / "ca_contracts" / "src",
                ROOT / "packages" / "ca_runtime" / "src",
                ROOT / "04_ACTIVATIVE_INTELLIGENCE_RUNTIME" / "src",
            )
        )
        env["CA_DATA_ROOT"] = data_root
        return env

    def test_cli_bootstrap_registry_and_status(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env = self._env(temp_dir)
            for command in (
                ["bootstrap", "--json"],
                ["load-registries", "--json"],
                ["registry-status", "--json"],
                ["status", "--json"],
            ):
                completed = subprocess.run(
                    [sys.executable, "-m", "cmf_activative_intelligence", *command],
                    cwd=ROOT,
                    env=env,
                    text=True,
                    capture_output=True,
                    check=True,
                )
                body = json.loads(completed.stdout)
                self.assertIsInstance(body, dict)
            self.assertEqual(body["product_id"], "activative-intelligence-runtime")
            self.assertTrue(body["development_authorized"])
            self.assertFalse(body["format02_activated"])


if __name__ == "__main__":
    unittest.main()
