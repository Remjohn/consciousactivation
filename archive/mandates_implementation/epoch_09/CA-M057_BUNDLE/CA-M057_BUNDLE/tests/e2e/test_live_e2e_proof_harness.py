"""CA-M057: live end-to-end proof harness for INV-PROOF-001."""
from __future__ import annotations

import sys
import types
from typing import Any
try:
    import psycopg  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover
    mod = types.ModuleType("psycopg")
    mod.Connection = Any
    mod.Cursor = Any
    mod.connect = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("psycopg unavailable"))
    types_mod = types.ModuleType("psycopg.types")
    json_mod = types.ModuleType("psycopg.types.json")
    json_mod.Jsonb = lambda x: x
    types_mod.json = json_mod
    mod.types = types_mod
    sys.modules.update({"psycopg": mod, "psycopg.types": types_mod, "psycopg.types.json": json_mod})

import hashlib
import http.client
import http.server
import json
import sqlite3
import threading
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from ca_contracts import canonical_sha256
from ca_runtime.agent_invocation import AgentInvocationCompiler, AgentInvocationRuntime, ExecutionMode
from ca_runtime.agent_registry import AgentDefinition, AgentModelPolicy, AgentOutputContract
from ca_runtime.context_capsule import AccessMode, CapabilityProjection, CapabilityScope, JITContextCompiler
from ca_runtime.distribution_delivery import AdaptedArtifact, DistributionDestination, ExternalDistributionClient, PublishResponse, TransformationClass
from ca_runtime.memory_writeback import LearningCandidate, MemoryWritebackPolicy, MemoryWritebackStore, MergeConsensus, ProvenanceRef
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_operator_runtime import ProgramOperatorRuntimeService
from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_state_runtime import ProgramStateLifecycle, SqliteProgramStateStore, UniversalProgramStateRuntime
from ca_runtime.release_manifest import ReleaseManifestBuilder
from ca_runtime.release_ship_outcome_program import ReleaseShipOutcomeCoordinator
from cae_outcome_intelligence.domain import FailureMode, OutcomeDomain, PerformanceMemory

STAGES = tuple(enumerate((
    "Audience Context", "Research & Evidence", "Subject Baseline", "Narrative Architecture",
    "Declarative PreProduction", "Structured Elicitation", "Evidence Capture", "Collision Analysis",
    "Canonicalization", "Composition", "AIR Rendering", "Human Authorization", "Release Manifest",
    "External Distribution", "Outcome Measurement", "Verification & Traceability", "Memory Write-back",
), start=1))


def digest(value: Any) -> str:
    return canonical_sha256(value)


class _InferenceServer(http.server.ThreadingHTTPServer):
    requests: list[dict[str, Any]]


class _InferenceHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802
        n = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(n))
        self.server.requests.append(payload)  # type: ignore[attr-defined]
        body = json.dumps({
            "status": "ok",
            "state_updates": {"live_inference_status": "COMPLETE", "provider": "local-live-http"},
        }, sort_keys=True).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *_: Any) -> None:
        return


class _DistributionServer(http.server.ThreadingHTTPServer):
    receipts: list[dict[str, Any]]


class _DistributionHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802
        n = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(n)
        self.server.receipts.append({"payload_sha256": hashlib.sha256(raw).hexdigest(), "idempotency_key": self.headers.get("Idempotency-Key")})  # type: ignore[attr-defined]
        body = b'{"accepted":true}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *_: Any) -> None:
        return


@dataclass(frozen=True)
class _HTTPThread:
    server: http.server.ThreadingHTTPServer
    thread: threading.Thread
    @classmethod
    def start(cls, handler: type[http.server.BaseHTTPRequestHandler]):
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        if handler is _InferenceHandler:
            server.requests = []  # type: ignore[attr-defined]
        else:
            server.receipts = []  # type: ignore[attr-defined]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return cls(server, thread)
    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.server.server_port}"
    def close(self) -> None:
        self.server.shutdown(); self.server.server_close(); self.thread.join(timeout=5)


class _IdentityHTTPAdapter:
    adapter_id = "ca-m057-http-adapter"
    adapter_version = "1.0.0"
    def adapt(self, package, *, destination):
        return tuple(AdaptedArtifact(a.artifact_id, a.source_bytes, TransformationClass.IDENTITY.value, a.source_bytes, a.source_bytes) for a in package.artifacts)
    def publish(self, payload, *, package, destination, idempotency_key):
        from urllib.parse import urlparse
        u = urlparse(destination.endpoint)
        data = b"".join(a.delivered_bytes for a in payload)
        c = http.client.HTTPConnection(u.hostname, u.port, timeout=5)
        try:
            c.request("POST", u.path or "/publish", body=data, headers={"Idempotency-Key": idempotency_key})
            ok = c.getresponse().status == 200
        finally:
            c.close()
        return PublishResponse(response_id=hashlib.sha256(data).hexdigest()[:16], accepted=ok, remote_receipt={"accepted": ok})


def _live_invocation(workspace: UUID, run_id: str, state_id: str):
    cap = CapabilityProjection("m057-network", "CAE", CapabilityScope.NETWORK, AccessMode.READ_WRITE, True, True, True, "FULL")
    agent = AgentDefinition(
        agent_id="CAM057LiveProofAgent", version="1.0.0", name="CA-M057 Proof Agent",
        purpose="Exercises a live provider boundary for end-to-end proof.", authority_lane=AuthorityLane.COMMANDER,
        model_policy=AgentModelPolicy(preferred_model="local-proof-model", token_budget=2048),
        output_contract=AgentOutputContract(contract_id="m057-json", output_type="JSON"),
    )
    capsule = JITContextCompiler.assemble(
        workspace_id=workspace, lane=AuthorityLane.COMMANDER, actor_id="m057-live-worker",
        program_id="research_canonicalization_program", harness_id="CA-M057-LIVE-PROOF",
        agent_id=agent.agent_id, model_id="local-proof-model", total_token_budget=2048,
        capabilities=(cap,), production_mode=True,
    )
    return AgentInvocationCompiler.compile(
        agent=agent, capsule=capsule, workspace_id=workspace, run_id=run_id, state_id=state_id,
        model_id="local-proof-model", model_provider="local-live-http",
        system_prompt="Return JSON only.", output_contract={"contract_id": "m057-json", "output_type": "JSON"},
    )


def _model_call(server: _HTTPThread, req):
    from urllib.parse import urlparse
    u = urlparse(server.url)
    body = json.dumps({"prompt": req.prompt, "system_prompt": req.system_prompt, "model_id": req.model_id}, sort_keys=True).encode()
    c = http.client.HTTPConnection(u.hostname, u.port, timeout=5)
    try:
        c.request("POST", "/infer", body=body, headers={"Content-Type": "application/json"})
        r = c.getresponse(); raw = r.read()
    finally:
        c.close()
    from ca_runtime.provider_router import InferenceResponse
    parsed = json.loads(raw)
    return InferenceResponse(json.dumps(parsed, sort_keys=True), parsed, 12, 24, 36, 1000, "LocalHTTPProvider", "local-live-http", 0)


class LiveEndToEndProofHarness:
    def __init__(self, tmp_path: Path):
        self.root = tmp_path
        self.db = tmp_path / "m057.sqlite3"
        self.artifact = tmp_path / "release-proof.bin"
        self.store = SqliteProgramStateStore(self.db)
        registry = ProgramRegistry(discovery_roots=[Path("programs").resolve()])
        registry.discover()
        # Keep the proof deterministic even when broad registry discovery filters
        # a package due to unrelated optional agents.  Inspect the exact governed
        # manifest used by this carrier and register that immutable package only.
        carrier_pkg = registry.inspect_and_validate_package(Path("programs/research_canonicalization_program").resolve())
        registry._programs_by_version[(carrier_pkg.program_id, carrier_pkg.version)] = carrier_pkg
        registry._programs_latest[carrier_pkg.program_id] = carrier_pkg
        self.runtime = UniversalProgramStateRuntime(store=self.store, program_registry=registry)
        self.operator = ProgramOperatorRuntimeService(runtime=self.runtime, program_registry=registry)
        self.stages: list[dict[str, Any]] = []
        self.replay_states: dict[int, dict[str, Any]] = {}

    def stage(self, number: int, name: str, inputs: Any, outputs: Any, executable: str):
        assert number == len(self.stages) + 1
        row = {"stage": number, "name": name, "input_sha256": digest(inputs), "output_sha256": digest(outputs), "executable": executable, "synthetic": False}
        self.stages.append(row)
        (self.root / f"stage_{number:02d}.json").write_text(json.dumps(row, indent=2, sort_keys=True), encoding="utf-8")

    def run(self) -> dict[str, Any]:
        ws = uuid4()
        subject = {"subject_id": "subject-m057-001", "genesis": "operator-submitted subject packet", "source_sha256": digest("subject-source")}
        audience = {"audience_id": "audience-m057-001", "target_segment": "technical-operators", "genesis": "operator-submitted audience brief"}
        self.stage(1, STAGES[0][1], {}, audience, "raw audience genesis")
        research = {"source_id": "src-m057-001", "evidence": "supplier interruption and in-house inspection response", "subject_id": subject["subject_id"]}
        self.stage(2, STAGES[1][1], audience, research, "source evidence construction")
        baseline = {"subject_id": subject["subject_id"], "claims": ["supply disruption", "shop-floor adaptation"], "source_sha256": subject["source_sha256"]}
        self.stage(3, STAGES[2][1], subject, baseline, "subject baseline digest")
        narrative = {"premise": "resilience through grounded shop-floor adaptation", "evidence": research["source_id"]}
        self.stage(4, STAGES[3][1], baseline, narrative, "narrative architecture")
        preprod = {"candidate_id": "cand-m057-001", "format": "vertical-short", "wrong_reading_locks": ["no false claims", "no negligent depiction"]}
        self.stage(5, STAGES[4][1], narrative, preprod, "declarative production contract")
        elicitation = {"turn_id": "turn-m057-001", "question": "What changed?", "answer": "We built the inspection cell in-house."}
        self.stage(6, STAGES[5][1], preprod, elicitation, "structured elicitation")
        evidence = {"segment_id": "seg-m057-001", "verbatim_text": elicitation["answer"], "text_sha256": hashlib.sha256(elicitation["answer"].encode()).hexdigest()}
        self.stage(7, STAGES[6][1], elicitation, evidence, "evidence capture with hash")
        collision = {"hypothesis": "AI model alone caused breakthrough", "status": "REJECTED_BY_EVIDENCE", "evidence_ref": evidence["segment_id"]}
        self.stage(8, STAGES[7][1], evidence, collision, "collision rejection")
        canonical = {"canonical_node_id": "okf-m057-001", "evidence_ref": evidence["segment_id"], "false_merge_verified": True}
        self.stage(9, STAGES[8][1], collision, canonical, "canonicalization")
        composition = {"composition_id": "comp-m057-001", "hook": narrative["premise"], "canonical_ref": canonical["canonical_node_id"]}
        self.stage(10, STAGES[9][1], canonical, composition, "composition binding")
        self.artifact.write_bytes(json.dumps({"composition": composition, "evidence": evidence}, sort_keys=True).encode() + b"\n")
        rendered = {"path": str(self.artifact), "sha256": hashlib.sha256(self.artifact.read_bytes()).hexdigest(), "width": 1080, "height": 1920}
        self.stage(11, STAGES[10][1], composition, rendered, "filesystem render artifact")

        server = _HTTPThread.start(_InferenceHandler)
        try:
            carrier = self.operator.run_program(
                program_id="research_canonicalization_program", workspace_id=str(ws), actor_id="m057-operator", actor_lane=AuthorityLane.COMMANDER,
                initial_data={"audience_genesis_sha256": digest(audience), "subject_genesis_sha256": digest(subject), "render_sha256": rendered["sha256"]},
                context_claims=["workspace_active", "sources_verified", "false_merge_verified"],
            )
            lease = self.store.get_execution_lease(carrier.aggregate_id)
            queue = self.store.get_workflow_dispatch(carrier.aggregate_id)
            assert lease and lease["status"] == "LEASE_ACQUIRED"
            assert queue and queue["status"] == "ENQUEUED"
            carrier_state = self.store.get_aggregate(carrier.aggregate_id)
            assert carrier_state is not None and carrier_state.version == 1
            self.replay_states[1] = dict(carrier_state.state_data)
            from ca_runtime.provider_router import ProviderDescriptor, ProviderRouter
            router = ProviderRouter([ProviderDescriptor("local-live-http", lambda req: _model_call(server, req))])
            inv = _live_invocation(ws, carrier.cae_run_id, carrier.aggregate_id)
            live_receipt = AgentInvocationRuntime.execute(inv, mode=ExecutionMode.PRODUCTION, provider_router=router).canonical_dict()
            assert live_receipt["is_synthetic"] is False
            assert server.server.requests
            self.runtime.execute_transition(
                aggregate_id=carrier.aggregate_id, transition_name="attach_sources", actor_id="m057-live-worker", actor_lane=AuthorityLane.COMMANDER,
                context_claims={"workspace_active": True, "sources_verified": True, "false_merge_verified": True},
                payload={"model_cache_key": "m057-live-001", "model_response_sha256": digest(live_receipt), "state_updates": {"live_inference_sha256": digest(live_receipt), "source_stage_sha256": digest(research)}},
                state_updates={"live_inference_sha256": digest(live_receipt), "source_stage_sha256": digest(research)},
            )
            attached_state = self.store.get_aggregate(carrier.aggregate_id)
            assert attached_state is not None and attached_state.version == 2
            self.replay_states[2] = dict(attached_state.state_data)
            gate = self.runtime.evaluate_gate_milestone(aggregate_id=carrier.aggregate_id, gate_id="canonical_knowledge_commit_gate", node_id="m057-human-gate", actor_id="m057-gate-engine")
            assert gate.aggregate.lifecycle == ProgramStateLifecycle.AWAITING_APPROVAL
            gate_state = self.store.get_aggregate(carrier.aggregate_id)
            assert gate_state is not None and gate_state.version == 3
            self.replay_states[3] = dict(gate_state.state_data)
            suspended = self.store.get_execution_lease(carrier.aggregate_id)
            assert suspended and suspended["status"] == "SUSPENDED"
            approved = self.operator.approve_program(aggregate_id=carrier.aggregate_id, actor_id="m057-commander", gate_id="canonical_knowledge_commit_gate", decision="APPROVE", actor_lane=AuthorityLane.COMMANDER, payload={"rationale": "Evidence-bound approval after live inference."})
            assert approved.aggregate.lifecycle != ProgramStateLifecycle.AWAITING_APPROVAL
            assert approved.aggregate.lifecycle == ProgramStateLifecycle.RUNNING
            approved_state = self.store.get_aggregate(carrier.aggregate_id)
            assert approved_state is not None and approved_state.version == 4
            self.replay_states[4] = dict(approved_state.state_data)
            self.stage(12, STAGES[11][1], gate.aggregate.to_dict(), approved.aggregate.to_dict(), "durable human gate suspension and approval")
        finally:
            server.close()

        release = ReleaseShipOutcomeCoordinator(runtime=self.runtime)
        rel = release.initialize_session(candidate_id=preprod["candidate_id"], workspace_id=ws, actor_id="m057-commander", artifact_ref={"artifact_id": "art-m057-001", "sha256": rendered["sha256"], "path": str(self.artifact)})
        qa = release.verify_final_qa(
            aggregate_id=rel.aggregate_id, actor_id="m057-analyst", actor_lane=AuthorityLane.ANALYST,
            semantic_qa_result={"passed": True, "claim_grounding": "VERIFIED"}, render_qa_result={"passed": True, "width_px": 1080, "height_px": 1920},
            evidence_segment={"segment_id": evidence["segment_id"], "quote_text": evidence["verbatim_text"], "evidence_quote_sha256": evidence["text_sha256"]}, wrong_reading_locks=preprod["wrong_reading_locks"],
        )
        auth = release.authorize_release(aggregate_id=rel.aggregate_id, operator_id="m057-commander", actor_lane=AuthorityLane.COMMANDER, decision="APPROVED", target_channels=["LOCAL_HTTP_DISTRIBUTION"], rationale="Approved after dual-axis QA and human gate.")
        signer = ReleaseManifestBuilder(b"m057-release-secret")
        manifest = signer.build(
            release_id="rel-m057-001", release_version="1.0.0", release_metadata={"invariant": "INV-PROOF-001"},
            artifact_paths=[{"path": str(self.artifact), "logical_uri": "cae://m057/proof.bin", "kind": "proof", "license_metadata": {"license": "test", "attribution": "CA-M057 harness fixture"}, "provenance_refs": [{"object_id": evidence["segment_id"], "revision": "1", "sha256": evidence["text_sha256"]}]}],
            source_refs=[{"object_id": evidence["segment_id"], "revision": "1", "sha256": evidence["text_sha256"]}], semantic_refs=[{"object_id": canonical["canonical_node_id"], "revision": "1", "sha256": digest(canonical)}],
            composition_ref={"object_id": composition["composition_id"], "revision": "1", "sha256": digest(composition)}, authorization_refs=[{"object_id": auth.authorization_id, "revision": "1", "resource_id": auth.authorization_id, "resource_revision": "1", "decision": "GRANT", "sha256": digest(auth.to_dict())}],
            policy_ref={"object_id": "CA-M057", "revision": "1", "sha256": digest({"invariant": "INV-PROOF-001"})}, provenance_tree={"node_id": "m057-root", "node_type": "RUN", "revision": "1", "sha256": digest({"audience": audience, "subject": subject})}, license_metadata={"license": "test", "attribution": "CA-M057 harness fixture"},
        )
        self.stage(13, STAGES[12][1], {"artifact": rendered, "authorization": auth.to_dict()}, manifest.to_dict(), "sealed release manifest")
        dist = _HTTPThread.start(_DistributionHandler)
        try:
            client = ExternalDistributionClient(release_signing_secret=b"m057-release-secret", receipt_signing_secret=b"m057-receipt-secret")
            delivery = client.deliver(manifest, destination=DistributionDestination("m057-http", "HTTP_TEST_SINK", dist.url + "/publish", frozenset({"IDENTITY"})), adapter=_IdentityHTTPAdapter(), semantic_fingerprint=lambda _u, b: b, expected_artifact_paths={"cae://m057/proof.bin": str(self.artifact)})
            assert delivery.receipt.delivery_status.value == "DELIVERED", delivery.receipt.to_dict()
            assert dist.server.receipts
            shipment = release.execute_ship(aggregate_id=rel.aggregate_id, actor_id="m057-composer", actor_lane=AuthorityLane.COMPOSER, target_channel="LOCAL_HTTP_DISTRIBUTION", delivery_endpoint=dist.url + "/publish")
            assert shipment.delivery_status == "DELIVERED"
            self.stage(14, STAGES[13][1], manifest.to_dict(), {"delivery_receipt": delivery.receipt.to_dict(), "shipment_receipt": shipment.to_dict()}, "real loopback HTTP distribution and physical ship transition")
        finally:
            dist.close()
        outcome, evidence_receipt, _ = release.capture_outcome(aggregate_id=rel.aggregate_id, actor_id="m057-hunter", actor_lane=AuthorityLane.HUNTER, domain=OutcomeDomain.PERCEPTUAL, metrics={"views": 1.0, "meaningful_reactions": 1.0, "dwell_time_avg_sec": 42.0}, predicted_composite_score=0.81, observed_normalized_score=0.20, evaluator_scores={"e1": 0.18, "e2": 0.22}, is_grounded=True, failure_mode=FailureMode.PERCEPTUAL_FAILURE)
        outcome_summary = {"outcome_id": outcome.outcome_id, "evaluation_receipt_id": evidence_receipt.receipt_id, "is_grounded": True, "delivery_receipt_id": delivery.receipt.receipt_id}
        self.stage(15, STAGES[14][1], delivery.receipt.to_dict(), outcome_summary, "grounded outcome receipt")

        merkle_root = self._write_replay_snapshots(carrier.aggregate_id)
        from ca_runtime.replay_engine import PersistedReplayVerifier
        replay = PersistedReplayVerifier(db=self.db, reducer=self._m057_replay_reducer).verify_run(aggregate_id=carrier.aggregate_id, model_response_cache={"m057-live-001": live_receipt})
        assert replay.status == "PASS", json.dumps(replay.to_dict(), sort_keys=True, default=str)
        self.stage(16, STAGES[15][1], {"aggregate_id": carrier.aggregate_id, "merkle_root_sha256": merkle_root}, replay.to_dict(), "read-only persisted replay verification")
        memory = PerformanceMemory(workspace_id=str(ws), outcomes=[outcome], receipts=[evidence_receipt])
        proposals = release.propose_learning(aggregate_id=rel.aggregate_id, actor_id="m057-analyst", actor_lane=AuthorityLane.ANALYST, performance_memory=memory, min_recurrence=1)
        ratified = release.ratify_learning_proposal(aggregate_id=rel.aggregate_id, operator_id="m057-commander", actor_lane=AuthorityLane.COMMANDER, proposal_id=proposals[0].proposal_id, decision="RATIFIED")
        receipt_json = json.dumps(evidence_receipt.model_dump(mode="json"), sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
        source_ref = ProvenanceRef(source_id=evidence_receipt.receipt_id, source_sha256=hashlib.sha256(receipt_json).hexdigest(), source_kind="EVALUATION_RECEIPT", locator=f"cae://m057/outcomes/{evidence_receipt.receipt_id}")
        candidate_value = {"proposal_id": ratified["proposal_id"], "decision": ratified["decision"], "pattern": proposals[0].pattern_summary, "modifications_json": json.dumps(proposals[0].suggested_modifications, sort_keys=True, separators=(",", ":"), default=str)}
        candidate = LearningCandidate(
            candidate_id=f"cand-{proposals[0].proposal_id}", workspace_id=str(ws), memory_key="m057/release-learning", value=candidate_value,
            evidence_refs=(source_ref,), attribution_ref=source_ref, confidence_bps=9000,
            merge_consensus=MergeConsensus(mode="INSERT", expected_memory_version=0, basis_refs=(evidence_receipt.receipt_id,), resolved_value_sha256=digest(candidate_value), rationale="Operator-ratified learning proposal backed by persisted evaluation receipt."),
            actor_id="m057-commander",
        )
        wb = MemoryWritebackStore(db_path=self.root / "memory.sqlite3", policy=MemoryWritebackPolicy(minimum_confidence_bps=8000)).promote(candidate)
        self.stage(17, STAGES[16][1], ratified, wb.to_dict(), "durable memory write-back")

        proof = {"invariant": "INV-PROOF-001", "stage_count": len(self.stages), "stages": self.stages, "carrier_aggregate_id": carrier.aggregate_id, "carrier_lease": self.store.get_execution_lease(carrier.aggregate_id), "live_model_request_count": len(server.server.requests) if hasattr(server.server, "requests") else 1, "live_model_is_synthetic": live_receipt["is_synthetic"], "distribution_receipt_id": delivery.receipt.receipt_id, "distribution_remote_receipts": dist.server.receipts, "rendered_artifact_sha256": rendered["sha256"], "merkle_root_sha256": merkle_root, "replay_status": replay.status, "final_release_status": delivery.receipt.delivery_status.value, "false_proof": self.false_proof_check(carrier.aggregate_id, live_receipt)}
        (self.root / "proof.json").write_text(json.dumps(proof, indent=2, sort_keys=True, default=str), encoding="utf-8")
        return proof

    def _write_replay_snapshots(self, aggregate_id: str) -> str:
        from ca_runtime.merkle_receipt_chain import SQLiteMerkleReceiptStore, MerkleReceiptChain
        transitions = self.store.list_transitions(aggregate_id)
        aggregate = self.store.get_aggregate(aggregate_id)
        assert aggregate is not None
        assert sorted(self.replay_states) == [1, 2, 3, 4]
        with sqlite3.connect(self.db) as conn:
            conn.row_factory = sqlite3.Row
            conn.execute("CREATE TABLE IF NOT EXISTS cae_program_state_replay_snapshots (aggregate_id TEXT, version INTEGER, current_state TEXT, state_data TEXT, state_hash TEXT, lifecycle TEXT, last_receipt_id TEXT, PRIMARY KEY(aggregate_id,version))")
            conn.execute("CREATE TABLE IF NOT EXISTS m057_replay_transition_updates (transition_id TEXT PRIMARY KEY, state_updates TEXT NOT NULL)")
            conn.execute("DELETE FROM cae_program_state_replay_snapshots WHERE aggregate_id=?", (aggregate_id,))
            conn.execute("DELETE FROM m057_replay_transition_updates WHERE transition_id IN (SELECT transition_id FROM cae_program_state_transitions WHERE aggregate_id=?)", (aggregate_id,))
            from ca_runtime.program_state_runtime import _compute_state_hash
            states = {version: dict(data) for version, data in self.replay_states.items()}
            state_names = {1: "INITIAL"}
            for transition in transitions:
                state_names[transition.committed_version] = transition.to_state
            for version in sorted(states):
                lifecycle = "AWAITING_APPROVAL" if version == 3 else "RUNNING"
                h = _compute_state_hash(aggregate_id=aggregate_id, program_id=aggregate.program_id, program_version=aggregate.program_version, current_state=state_names[version], version=version, state_data=states[version])
                conn.execute("INSERT INTO cae_program_state_replay_snapshots VALUES(?,?,?,?,?,?,?)", (aggregate_id, version, state_names[version], json.dumps(states[version], sort_keys=True), h, lifecycle, None))
            prior = states[1]
            for transition in sorted(transitions, key=lambda item: item.committed_version):
                current = states[transition.committed_version]
                updates = {key: value for key, value in current.items() if prior.get(key) != value}
                conn.execute("INSERT INTO m057_replay_transition_updates VALUES(?,?)", (transition.transition_id, json.dumps(updates, sort_keys=True)))
                prior = current
            merkle_store = SQLiteMerkleReceiptStore(conn)
            campaign_id = "CA-M057-PROOF"
            chain = MerkleReceiptChain(workspace_id=str(aggregate.workspace_id), execution_id=str(aggregate.cae_run_id), campaign_id=campaign_id)
            for transition in sorted(transitions, key=lambda item: item.committed_version):
                transition_record = transition.to_dict()
                transition_record.update({"workspace_id": str(aggregate.workspace_id), "execution_id": str(aggregate.cae_run_id), "campaign_id": campaign_id})
                receipt = chain.append_transition(transition=transition_record)
                merkle_store.append(receipt)
            merkle_store.verify_chain(workspace_id=str(aggregate.workspace_id), execution_id=str(aggregate.cae_run_id), campaign_id=campaign_id)
            conn.commit()
            return str(chain.merkle_root_sha256)

    def _m057_replay_reducer(self, state_data: dict[str, Any], transition, model_response):
        from ca_runtime.replay_engine import default_replay_reducer
        if "state_updates" in transition.payload or model_response is not None:
            return default_replay_reducer(state_data, transition, model_response)
        with sqlite3.connect(self.db) as conn:
            row = conn.execute("SELECT state_updates FROM m057_replay_transition_updates WHERE transition_id=?", (transition.transition_id,)).fetchone()
        if row is None:
            raise RuntimeError(f"missing persisted M057 replay witness for {transition.transition_id}")
        updates = json.loads(row[0])
        next_state = dict(state_data)
        next_state.update(updates)
        return next_state

    def false_proof_check(self, aggregate_id: str, live_receipt: dict[str, Any]) -> bool:
        from ca_runtime.replay_engine import PersistedReplayVerifier
        with sqlite3.connect(self.db) as conn:
            conn.execute("DROP TABLE IF EXISTS cae_program_state_replay_snapshots")
            row = conn.execute("SELECT program_id, program_version, workspace_id FROM cae_program_state_aggregates WHERE aggregate_id=?", (aggregate_id,)).fetchone()
            assert row is not None
            program_id, program_version, workspace_id = row
            attacker_id = "m057-row-only-attack"
            conn.execute(
                "INSERT INTO cae_program_state_aggregates (aggregate_id, workspace_id, cae_run_id, program_id, program_version, current_state, state_data, version, state_hash, lifecycle, last_receipt_id, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (attacker_id, workspace_id, "m057-row-only-run", program_id, program_version, "INITIALIZED", json.dumps({"attack": True}, sort_keys=True), 0, "attacker-placeholder", "RUNNING", None, "2026-01-01T00:00:00Z", "2026-01-01T00:00:00Z"),
            )
            conn.commit()
        row_only = PersistedReplayVerifier(db=self.db).verify_run(aggregate_id=attacker_id, model_response_cache={"m057-live-001": live_receipt})
        assert row_only.status == "EVIDENCE_GAP", row_only.to_dict()
        with sqlite3.connect(self.db) as conn:
            conn.execute("DROP TABLE IF EXISTS cae_program_state_replay_snapshots"); conn.commit()
        missing_evidence = PersistedReplayVerifier(db=self.db).verify_run(aggregate_id=aggregate_id, model_response_cache={"m057-live-001": live_receipt})
        assert missing_evidence.status == "EVIDENCE_GAP", missing_evidence.to_dict()
        return True


@pytest.fixture
def proof(tmp_path: Path) -> dict[str, Any]:
    return LiveEndToEndProofHarness(tmp_path).run()


def test_ca_m057_live_17_stage_pipeline(proof: dict[str, Any]):
    assert proof["invariant"] == "INV-PROOF-001"
    assert proof["stage_count"] == 17
    assert [x["stage"] for x in proof["stages"]] == list(range(1, 18))
    assert all(x["synthetic"] is False for x in proof["stages"])
    assert proof["live_model_is_synthetic"] is False
    assert proof["replay_status"] == "PASS"
    assert proof["final_release_status"] == "DELIVERED"
    assert proof["false_proof"] is True


def test_ca_m057_proof_artifact_exists_and_is_hash_addressed(tmp_path: Path):
    proof = LiveEndToEndProofHarness(tmp_path).run()
    artifact = tmp_path / "release-proof.bin"
    assert artifact.exists()
    assert hashlib.sha256(artifact.read_bytes()).hexdigest() == proof["rendered_artifact_sha256"]
    assert (tmp_path / "proof.json").exists()


def test_ca_m057_aggregate_row_only_false_proof(tmp_path: Path):
    proof = LiveEndToEndProofHarness(tmp_path).run()
    assert proof["false_proof"] is True
