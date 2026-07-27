from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _support import ref  # type: ignore
from cmf_pipeline import PipelineApplication
from cmf_pipeline.domain.errors import PipelineValidationError
from cmf_pipeline.domain.validation import semantic_identity


def authority_snapshot() -> dict[str, object]:
    core = {
        "schema_id": "authority-snapshot",
        "schema_version": "1.0.0",
        "constitution_id": "ca-constitution-v2.1-candidate",
        "constitution_version": "2.1.0-candidate",
        "constitution_sha256": "c" * 64,
        "product_authorities": [
            {"authority_id": "authority:ahp", "authority_version": "1.0.0", "authority_sha256": "a" * 64, "authority_state": "current"},
            {"authority_id": "authority:air", "authority_version": "1.0.0", "authority_sha256": "b" * 64, "authority_state": "current"},
        ],
        "candidate_authorities": [
            {"authority_id": "authority:v2.1-candidate", "authority_version": "2.1.0-candidate", "authority_sha256": "c" * 64, "authority_state": "candidate_not_current"}
        ],
        "canonical_program_status_id": "status:program-control",
        "issued_by": "program-control",
    }
    return {"snapshot_id": semantic_identity("authority-snapshot", core), **core}


def status(product_id: str, *, canonical: bool, production: bool = False) -> dict[str, object]:
    return {
        "projection_id": f"status:{product_id}",
        "product_id": product_id,
        "product_version": "1.0.0",
        "canonical": canonical,
        "implementation_coverage": "development_only",
        "story_completion": "open",
        "evidence_closure": "open",
        "external_proof_complete": False,
        "production_authorized": production,
        "certified": False,
        "source_sha256": "d" * 64,
    }


class AuthorityBatchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.app = PipelineApplication(Path(self.temp.name) / "pipeline.sqlite3")
        self.app.initialize()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_program_control_status_wins_and_claim_dimensions_stay_separate(self) -> None:
        result = self.app.authority.reconcile_program_state(
            authority_snapshot(),
            [status("program-control", canonical=True), status("legacy-product", canonical=False, production=True)],
            idempotency_key="reconcile",
        )["object"]["payload"]
        self.assertTrue(result["claim_dimensions_separate"])
        self.assertEqual(result["canonical_program_status"]["product_id"], "program-control")
        self.assertEqual(result["conflicts"][0]["resolution"], "CANONICAL_PROGRAM_CONTROL_WINS")

    def test_candidate_authority_denies_build_claim(self) -> None:
        auth = authority_snapshot()
        canonical = status("program-control", canonical=True)
        request_core = {
            "binding_id": "binding:1",
            "binding_version": "1.0.0",
            "binding_sha256": "e" * 64,
            "atomic_harness_definition_ref": ref("harness:def"),
            "authority_snapshot_id": auth["snapshot_id"],
            "program_status_id": canonical["projection_id"],
            "source_record_ids": [],
            "contract_refs": [],
            "category_id": "short_form_edited_video",
            "profile_id": "format07_direct_coaching_a_roll",
            "requested_claim": "ACCEPTED_FOR_BUILD",
        }
        request = {"request_id": semantic_identity("binding-admission-request", request_core), **request_core}
        result = self.app.authority.evaluate_binding_admission(
            request,
            authority_snapshot=auth,
            canonical_program_status=canonical,
            idempotency_key="admit",
        )["object"]["payload"]
        self.assertEqual(result["decision"], "DENIED")
        self.assertIn("CANDIDATE_AUTHORITY_NOT_RATIFIED", result["blockers"])

    def test_source_backed_batch_preserves_exact_lineage_and_animation_derivative(self) -> None:
        source_ref = ref("interview:source-package")
        request = {
            "source_package_ref": source_ref,
            "observed_activative_pack_ref": ref("air:observed-pack"),
            "harness_binding_ref": ref("ahp:binding"),
            "brand_context_ref": ref("air:brand-context"),
            "shared_analysis_refs": [ref("analysis:shot-map")],
            "campaign_id": "campaign:reference",
            "routes": [
                {
                    "route_id": "route:animation",
                    "derivative_type": "ANIMATION_SCENE_PACKAGE",
                    "semantic_program_ref": ref("air:semantic-animation"),
                    "final_script_ref": ref("air:final-script"),
                    "archetype_coalition_ref": ref("air:archetype"),
                    "primitive_coalition_ref": ref("air:coalition"),
                    "activation_transfer_contract_ref": ref("air:transfer"),
                    "source_spans": [{"source_id": source_ref["object_id"], "source_version": source_ref["version"], "source_sha256": source_ref["sha256"], "start_ms": 1000, "end_ms": 3000, "speaker_id": "speaker:guest"}],
                    "animation_scene_package_ref": ref("air:animation-scenes"),
                    "priority": 1,
                    "not_applicable_reason": "NOT_APPLICABLE",
                },
                {
                    "route_id": "route:short",
                    "derivative_type": "SOURCE_LED_SHORT",
                    "semantic_program_ref": ref("air:semantic-short"),
                    "final_script_ref": ref("air:final-script"),
                    "archetype_coalition_ref": ref("air:archetype"),
                    "primitive_coalition_ref": ref("air:coalition"),
                    "activation_transfer_contract_ref": ref("air:transfer"),
                    "source_spans": [{"source_id": source_ref["object_id"], "source_version": source_ref["version"], "source_sha256": source_ref["sha256"], "start_ms": 1000, "end_ms": 6000, "speaker_id": "speaker:guest"}],
                    "animation_scene_package_ref": ref("air:animation-scenes"),
                    "priority": 2,
                    "not_applicable_reason": "NOT_APPLICABLE",
                },
            ],
        }
        result = self.app.batches.compile_batch(request, idempotency_key="batch")["object"]["payload"]
        self.assertEqual(len(result["jobs"]), 2)
        self.assertFalse(result["semantic_values_owned_by_pipeline"])
        self.assertEqual(result["source_package_ref"], source_ref)
        self.assertEqual({item["derivative_type"] for item in result["jobs"]}, {"ANIMATION_SCENE_PACKAGE", "SOURCE_LED_SHORT"})

    def test_batch_rejects_format02(self) -> None:
        source_ref = ref("interview:source-package")
        request = {
            "source_package_ref": source_ref,
            "observed_activative_pack_ref": ref("air:observed-pack"),
            "harness_binding_ref": ref("ahp:binding"),
            "brand_context_ref": ref("air:brand-context"),
            "shared_analysis_refs": [],
            "campaign_id": "campaign:reference",
            "routes": [{
                "route_id": "format02:bad",
                "derivative_type": "ANIMATION_SHORT",
                "semantic_program_ref": ref("air:semantic"),
                "final_script_ref": ref("air:final-script"),
                "archetype_coalition_ref": ref("air:archetype"),
                "primitive_coalition_ref": ref("air:coalition"),
                "activation_transfer_contract_ref": ref("air:transfer"),
                "source_spans": [{"source_id": source_ref["object_id"], "source_version": source_ref["version"], "source_sha256": source_ref["sha256"], "start_ms": 0, "end_ms": 1, "speaker_id": "guest"}],
                "animation_scene_package_ref": ref("air:animation-scenes"),
                "priority": 1,
                "not_applicable_reason": "NOT_APPLICABLE",
            }],
        }
        with self.assertRaises(PipelineValidationError):
            self.app.batches.compile_batch(request, idempotency_key="bad")



if __name__ == "__main__":
    unittest.main()
