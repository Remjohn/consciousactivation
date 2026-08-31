"""Tests for AIR Brand REST API endpoints introduced in CAE Mandate M27."""

from __future__ import annotations

from fastapi.testclient import TestClient


def _client(tmp_path, monkeypatch):
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path))
    from api.main import app
    return TestClient(app)


def test_air_brand_endpoints_lifecycle(tmp_path, monkeypatch):
    with _client(tmp_path, monkeypatch) as client:
        auth = {
            "authority_id": "usr_operator_1",
            "authority_version": "1.0.0",
            "authority_sha256": "0" * 64,
            "authority_state": "current",
        }
        source_ref = {
            "object_id": "ev-src-001",
            "version": "1.0.0",
            "sha256": "1" * 64,
        }
        genesis_ref = {
            "object_id": "ses-gen-001",
            "version": "1.0.0",
            "sha256": "2" * 64,
        }

        # 1. POST /api/air/brand/context
        brand_req = {
            "brand_context_id": "brand-ctx-rest-01",
            "brand_genesis_session_ref": genesis_ref,
            "identity_truths": ["Operational clarity over consensus", "Truth found in friction"],
            "audience_relationship": "Collaborative peer",
            "positioning_tension": "Autonomy requires transparency",
            "source_refs": [source_ref],
            "authority": auth,
            "idempotency_key": "idem-brand-01",
        }
        res = client.post("/api/air/brand/context", json=brand_req)
        assert res.status_code == 200, res.text
        data = res.json()
        assert data["brand_context_id"] == "brand-ctx-rest-01"
        brand_ref = data["brand_context_ref"]

        # GET /api/air/brand/context/{id}
        res_get = client.get("/api/air/brand/context/brand-ctx-rest-01")
        assert res_get.status_code == 200
        assert res_get.json()["brand_context_id"] == "brand-ctx-rest-01"

        # 2. POST /api/air/brand/voice-dna
        voice_req = {
            "voice_dna_id": "voice-dna-rest-01",
            "brand_context_ref": brand_ref,
            "vocabulary_patterns": ["friction-forged", "ruthless precision"],
            "rhythm_patterns": ["deliberate cadences"],
            "sentence_pressure_patterns": ["declarative imperatives"],
            "stance_patterns": ["rigorous partner"],
            "specificity_patterns": ["concrete operational examples"],
            "metaphor_range": ["structural mechanics"],
            "emotional_distance": "measured but committed",
            "prohibited_centroid_patterns": ["synergy", "paradigm shift"],
            "source_evidence_refs": [source_ref],
            "authority": auth,
            "idempotency_key": "idem-voice-01",
        }
        res_voice = client.post("/api/air/brand/voice-dna", json=voice_req)
        assert res_voice.status_code == 200, res_voice.text
        data_voice = res_voice.json()
        assert data_voice["voice_dna_id"] == "voice-dna-rest-01"
        voice_ref = data_voice["voice_dna_ref"]

        # GET /api/air/brand/voice-dna/{id}
        res_voice_get = client.get("/api/air/brand/voice-dna/voice-dna-rest-01")
        assert res_voice_get.status_code == 200
        assert res_voice_get.json()["voice_dna_id"] == "voice-dna-rest-01"

        # 3. POST /api/air/brand/visual-dna
        visual_req = {
            "visual_dna_id": "vis-dna-rest-01",
            "brand_context_ref": brand_ref,
            "subject_treatment": ["candid portraiture"],
            "visual_temperature": ["neutral cool"],
            "materiality": ["textured matte"],
            "composition_tendencies": ["strict asymmetric balance"],
            "negative_space_functions": ["breathing room"],
            "edge_behaviors": ["hard clean cuts"],
            "typographic_posture": ["architectural geometric"],
            "motion_character": ["linear purposeful"],
            "prohibited_centroid_defaults": ["stock handshakes", "blue gradient blobs"],
            "real_life_reference_refs": [source_ref],
            "authority": auth,
            "idempotency_key": "idem-visual-01",
        }
        res_vis = client.post("/api/air/brand/visual-dna", json=visual_req)
        assert res_vis.status_code == 200, res_vis.text
        assert res_vis.json()["visual_dna_id"] == "vis-dna-rest-01"

        # GET /api/air/brand/visual-dna/{id}
        res_vis_get = client.get("/api/air/brand/visual-dna/vis-dna-rest-01")
        assert res_vis_get.status_code == 200
        assert res_vis_get.json()["visual_dna_id"] == "vis-dna-rest-01"

        # 4. POST /api/air/brand/distillation/synthesize
        distill_req = {
            "receipt_id_prefix": "rcpt:dist:rest",
            "brand_context_ref": brand_ref,
            "voice_dna_ref": voice_ref,
            "input_evidence_refs": [source_ref],
            "authority": auth,
            "idempotency_prefix": "idem-dist",
        }
        res_dist = client.post("/api/air/brand/distillation/synthesize", json=distill_req)
        assert res_dist.status_code == 200, res_dist.text
        dist_data = res_dist.json()
        assert len(dist_data) == 5

        # 5. POST /api/air/brand/semantic-territory
        terr_req = {
            "brand_context_ref": brand_ref,
            "voice_dna_ref": voice_ref,
            "protected_source_refs": [source_ref],
            "wrong_reading_locks": ["Never interpret directness as aggression"],
            "prohibited_centroid_patterns": ["synergy", "low hanging fruit"],
            "authority": auth,
        }
        res_terr = client.post("/api/air/brand/semantic-territory", json=terr_req)
        assert res_terr.status_code == 200, res_terr.text
        terr_data = res_terr.json()
        assert terr_data["ratified"] is True
        assert len(terr_data["wrong_reading_locks"]) == 1
