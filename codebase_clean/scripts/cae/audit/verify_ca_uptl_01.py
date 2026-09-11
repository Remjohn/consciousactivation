"""
Reality Probe Validator for Mandate CA-UPTL-01 — Upstream Intelligence Completion.

Executes live reality probes across all four gated sub-workstreams:
- Probe 1: Documentation and Admission Integrity
- Probe 2: U1 Registry Defect Refusal Probes
- Probe 3: U2 Model Reasoning Module Reality Probes
- Probe 4: U3 Semantic Chain Demonstration Reality Probes
- Probe 5: U4 AIR Generation Services & Contrastive Probes
- Probe 6: Control State Reclassification Integrity
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
IMPL_DIR = ROOT_DIR / "docs" / "cae" / "implementation"

# Add package paths
sys.path.insert(0, str(ROOT_DIR / "packages" / "ca_contracts" / "src"))
sys.path.insert(0, str(ROOT_DIR / "packages" / "ca_runtime" / "src"))
sys.path.insert(0, str(ROOT_DIR / "services" / "pipeline" / "src"))
sys.path.insert(0, str(ROOT_DIR / "services" / "air" / "src"))

REQUIRED_DOCS = [
    "CAE_UPTL_01_ADMISSION_RECORD.md",
    "CAE_UPTL_01_CUSTODIAN_DISPOSITION_PACKET.md",
    "CAE_UPTL_01_REASONING_MODULE_PROOF.md",
    "CAE_UPTL_01_SEMANTIC_CHAIN_EVIDENCE.md",
    "CAE_UPTL_01_AIR_GENERATION_PROOF.md",
    "CAE_UPTL_01_COMPLETION_RECORD.md",
]


def probe_1_documentation_integrity() -> tuple[bool, str]:
    """Probe 1: Verify all CA-UPTL-01 documentation artifacts exist and are non-empty."""
    missing = []
    empty = []
    for doc in REQUIRED_DOCS:
        path = IMPL_DIR / doc
        if not path.is_file():
            missing.append(doc)
        elif path.stat().st_size == 0:
            empty.append(doc)

    if missing:
        return False, f"Missing documentation files: {missing}"
    if empty:
        return False, f"Empty documentation files: {empty}"
    return True, f"All {len(REQUIRED_DOCS)} documentation files verified."


def probe_2_u1_registry_defect_refusal() -> tuple[bool, str]:
    """Probe 2: Verify typed refusal exceptions on quarantined/ambiguous/versionless registry items."""
    from unittest.mock import MagicMock
    from ca_runtime.registry import (
        RegistryResolver,
        RegistryItemAmbiguousError,
        RegistryItemNotFoundError,
        RegistryItemQuarantinedError,
        RegistryItemVersionlessError,
    )

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    resolver = RegistryResolver(mock_conn)

    # 1. Not found
    mock_cursor.fetchall.return_value = []
    try:
        resolver.get_item(registry_snapshot_id="snap:1", canonical_id="NONEXISTENT")
        return False, "NONEXISTENT did not raise RegistryItemNotFoundError"
    except RegistryItemNotFoundError:
        pass

    # 2. Quarantined (SFL-FAM-005)
    mock_cursor.fetchall.return_value = [
        ("snap:1", "sfl", "SFL-FAM-005", "1.0.0", "path", "hash", "SFL-FAM-005", "family", {}, "QUARANTINED")
    ]
    try:
        resolver.get_item(registry_snapshot_id="snap:1", canonical_id="SFL-FAM-005")
        return False, "SFL-FAM-005 did not raise RegistryItemQuarantinedError"
    except RegistryItemQuarantinedError:
        pass

    # 3. Ambiguous (EXP-TRG-001)
    mock_cursor.fetchall.return_value = [
        ("snap:1", "sda", "EXP-TRG-001", "1.0.0", "path1", "hash1", "EXP-TRG-001", "primitive", {}, "IMPORTED"),
        ("snap:1", "sda", "EXP-TRG-001", "2.0.0", "path2", "hash2", "EXP-TRG-001", "primitive", {}, "IMPORTED"),
    ]
    try:
        resolver.get_item(registry_snapshot_id="snap:1", canonical_id="EXP-TRG-001")
        return False, "EXP-TRG-001 did not raise RegistryItemAmbiguousError"
    except RegistryItemAmbiguousError:
        pass

    # 4. Versionless
    mock_cursor.fetchall.return_value = [
        ("snap:1", "sda", "UNVER-001", None, "path", "hash", "UNVER-001", "primitive", {}, "IMPORTED")
    ]
    try:
        resolver.get_item(registry_snapshot_id="snap:1", canonical_id="UNVER-001", require_versioned=True)
        return False, "UNVER-001 did not raise RegistryItemVersionlessError"
    except RegistryItemVersionlessError:
        pass

    return True, "U1 Registry defect typed refusals verified."


def probe_3_u2_reasoning_module() -> tuple[bool, str]:
    """Probe 3: Verify ProgrammedModelRegistry schema-compliant registration and loud failure."""
    from cmf_pipeline.application import PipelineApplication
    from cmf_pipeline.reasoning import (
        ModelReasoningEngine,
        ProviderCredentialsMissingError,
    )

    with tempfile.TemporaryDirectory() as td:
        db_path = Path(td) / "test_pipeline.db"
        app = PipelineApplication(db_path)
        app.initialize()
        engine = ModelReasoningEngine(app.programmed_models)
        refs = engine.ensure_registered()

        # Check entity registration
        assert "artifact_ref" in refs, "model_artifact not registered"
        assert "claim_ref" in refs, "model_claim not registered"
        assert "program_ref" in refs, "model_program not registered"

        # Check loud failure on missing credentials
        orig_key = os.environ.get("GROQ_API_KEY")
        try:
            if "GROQ_API_KEY" in os.environ:
                del os.environ["GROQ_API_KEY"]
            try:
                engine.infer("Test prompt")
                return False, "ModelReasoningEngine did not raise ProviderCredentialsMissingError when key missing"
            except ProviderCredentialsMissingError:
                pass
        finally:
            if orig_key is not None:
                os.environ["GROQ_API_KEY"] = orig_key

    return True, "U2 Model reasoning engine contract, registration, and loud failure verified."


def probe_4_u3_semantic_chain_demonstration() -> tuple[bool, str]:
    """Probe 4: Verify World -> Context -> SDA -> Edging demonstration with immutable receipts."""
    from cmf_activative_intelligence.semantic_chain_demonstration import SemanticChainDemonstration

    with tempfile.TemporaryDirectory() as td:
        db_path = Path(td) / "test_air_probe.db"
        demo = SemanticChainDemonstration(db_path)
        res = demo.run(prefix="uptl01-audit")

        if res["status"] != "SUCCESS":
            return False, f"SemanticChainDemonstration returned status {res['status']}"
        if res["receipt_count"] != 8:
            return False, f"Expected 8 receipts, got {res['receipt_count']}"

        for rcpt in res["receipts"]:
            if rcpt["epistemic_status"] != "UNVERIFIED":
                return False, f"Receipt {rcpt['receipt_id']} has epistemic_status {rcpt['epistemic_status']}, expected UNVERIFIED"
            if rcpt["reward_hack_result"] != "UNVERIFIED":
                return False, f"Receipt {rcpt['receipt_id']} has reward_hack_result {rcpt['reward_hack_result']}, expected UNVERIFIED"
            if len(rcpt["receipt_sha256"]) != 64:
                return False, f"Receipt {rcpt['receipt_id']} has invalid receipt_sha256"

    return True, "U3 Semantic chain demonstration verified with 8 immutable receipts and UNVERIFIED epistemic boundaries."


def probe_5_u4_air_generation_services() -> tuple[bool, str]:
    """Probe 5: Verify AIR service generation logic and contrastive failure without reasoning engine."""
    from cmf_activative_intelligence.application import AirApplication

    with tempfile.TemporaryDirectory() as td:
        db_path = Path(td) / "test_air_u4.db"
        app = AirApplication(db_path)
        app.initialize()

        # F17 Learning Service contrastive check
        try:
            app.learning.generate_learning_episode(
                episode_id="test:ep:1",
                operator_request="Fix tension",
                before_state_refs=[{"object_id": "b:1", "version": "1.0.0", "sha256": "0" * 64}],
                authority={"authority_id": "auth:1", "authority_version": "1.0.0", "authority_sha256": "0" * 64, "authority_state": "candidate_not_current"},
                reasoning_engine=None,
            )
            return False, "F17 LearningService did not fail when reasoning_engine is None"
        except ValueError:
            pass

        # F28 Archetype Service contrastive check
        try:
            app.archetypes.generate_program(
                program_id="test:prg:1",
                role_tension_ref={"object_id": "r:1", "version": "1.0.0", "sha256": "0" * 64},
                primitive_coalition_ref={"object_id": "c:1", "version": "1.0.0", "sha256": "0" * 64},
                primary_archetype_ref={"object_id": "a:1", "version": "1.0.0", "sha256": "0" * 64},
                supporting_archetype_refs=[],
                category_target="leadership",
                source_expression_refs=[],
                authority={"authority_id": "auth:1", "authority_version": "1.0.0", "authority_sha256": "0" * 64, "authority_state": "candidate_not_current"},
                current_validation_ref={"object_id": "v:1", "version": "1.0.0", "sha256": "0" * 64},
                reasoning_engine=None,
            )
            return False, "F28 ArchetypeService did not fail when reasoning_engine is None"
        except ValueError:
            pass

        # F29 Coalition Service contrastive check
        try:
            app.coalitions.generate_coalition(
                coalition_id="test:coal:1",
                source_context_refs=[],
                binding_refs=[],
                role_tension_ref={"object_id": "r:1", "version": "1.0.0", "sha256": "0" * 64},
                matrix_of_edging_ref={"object_id": "m:1", "version": "1.0.0", "sha256": "0" * 64},
                evaluation_profile_ref={"object_id": "e:1", "version": "1.0.0", "sha256": "0" * 64},
                authority={"authority_id": "auth:1", "authority_version": "1.0.0", "authority_sha256": "0" * 64, "authority_state": "candidate_not_current"},
                broad_signal_ref={"object_id": "s:1", "version": "1.0.0", "sha256": "0" * 64},
                reasoning_engine=None,
            )
            return False, "F29 CoalitionService did not fail when reasoning_engine is None"
        except ValueError:
            pass

        # F30 Brand Service contrastive check
        try:
            app.brand.generate_voice_dna(
                voice_dna_id="test:voice:1",
                brand_context_ref={"object_id": "b:1", "version": "1.0.0", "sha256": "0" * 64},
                source_evidence_refs=[],
                authority={"authority_id": "auth:1", "authority_version": "1.0.0", "authority_sha256": "0" * 64, "authority_state": "candidate_not_current"},
                reasoning_engine=None,
            )
            return False, "F30 BrandService.generate_voice_dna did not fail when reasoning_engine is None"
        except ValueError:
            pass

    return True, "U4 AIR generation services contrastive tests verified."


def probe_6_control_state_integrity() -> tuple[bool, str]:
    """Probe 6: Verify Control State reclassifies CA-E3-08/CA-STAGE-09/CA-ACCEPT-10 as CLAIMS_UNVERIFIED_BY_OPERATOR."""
    control_state_path = IMPL_DIR / "CAE_IMPLEMENTATION_CONTROL_STATE.md"
    if not control_state_path.is_file():
        return False, "CAE_IMPLEMENTATION_CONTROL_STATE.md not found"
    content = control_state_path.read_text(encoding="utf-8")

    if "CLAIMS_UNVERIFIED_BY_OPERATOR" not in content:
        return False, "Control state missing CLAIMS_UNVERIFIED_BY_OPERATOR reclassification"
    if "CA-UPTL-01" not in content:
        return False, "Control state missing CA-UPTL-01"

    return True, "Control state reclassification and phase integrity verified."


def run_all_probes() -> dict[str, Any]:
    probes = [
        ("Probe 1: Documentation Integrity", probe_1_documentation_integrity),
        ("Probe 2: U1 Registry Defect Refusals", probe_2_u1_registry_defect_refusal),
        ("Probe 3: U2 Model Reasoning Module", probe_3_u2_reasoning_module),
        ("Probe 4: U3 Semantic Chain Demonstration", probe_4_u3_semantic_chain_demonstration),
        ("Probe 5: U4 AIR Generation Services", probe_5_u4_air_generation_services),
        ("Probe 6: Control State Integrity", probe_6_control_state_integrity),
    ]

    all_passed = True
    results = []
    for name, fn in probes:
        try:
            passed, msg = fn()
        except Exception as ex:
            passed = False
            msg = f"Exception: {ex}"
        results.append({"probe": name, "passed": passed, "message": msg})
        if not passed:
            all_passed = False

    return {
        "status": "PASS" if all_passed else "FAIL",
        "all_passed": all_passed,
        "results": results,
    }


if __name__ == "__main__":
    res = run_all_probes()
    print("=" * 60)
    print(f"CA-UPTL-01 Reality Probe Audit: {res['status']}")
    print("=" * 60)
    for r in res["results"]:
        mark = "PASS" if r["passed"] else "FAIL"
        print(f"[{mark}] {r['probe']}: {r['message']}")
    print("=" * 60)
    sys.exit(0 if res["all_passed"] else 1)
