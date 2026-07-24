from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from ca_contracts import canonical_sha256, utc_now_rfc3339
from ca_delegation_rc4 import ContractSet

from .capabilities import CapabilityRegistry, WorkcellCompiler, default_registry
from .comfyui import ComfyUIGraphCompiler
from .evaluation import RepairPlanner, TechnicalEvaluator
from .memory import control_tower_projection, project_okf
from .planning import DemandAdmissionService, ProductionPlanCompiler
from .providers import ReferenceProviders
from .repository import VAERepository
from .storage import ContentAddressedStore
from .validation import semantic_id


class VAEApplication:
    def __init__(self, database_path: str | Path, storage_root: str | Path, delegation_root: str | Path):
        self.repository=VAERepository(database_path)
        self.store=ContentAddressedStore(storage_root)
        self.contracts=ContractSet(delegation_root)
        self.admission=DemandAdmissionService(self.repository,self.contracts)
        self.plans=ProductionPlanCompiler(self.repository)
        self.capabilities: CapabilityRegistry=default_registry()
        self.workcells=WorkcellCompiler(self.capabilities)
        self.comfyui=ComfyUIGraphCompiler()
        self.providers=ReferenceProviders(self.store)
        self.evaluator=TechnicalEvaluator(self.store)
        self.repairs=RepairPlanner()

    def initialize(self) -> dict[str,Any]:
        return {"database":self.repository.initialize(),"delegation":self.contracts.verify_release(),"capabilities":self.capabilities.all()}

    def build_result(self, *, demand: Mapping[str,Any], plan: Mapping[str,Any], artifact_record: Mapping[str,Any], evaluation: Mapping[str,Any], attempts_consumed: int) -> dict[str,Any]:
        demand_sha=canonical_sha256(demand)
        demand_ref={"request_id":demand["request_id"],"version":demand["version"],"payload_hash":"sha256:"+demand_sha,"canonical_ref":f"cmf-contract://demands/{demand['request_id']}/{demand['version']}"}
        plan_ref={"resource_id":plan["plan_id"],"version":plan["plan_version"],"payload_hash":"sha256:"+canonical_sha256(plan),"canonical_ref":f"cmf-contract://resources/{plan['plan_id']}/{plan['plan_version']}"}
        result_id=f"result-{canonical_sha256({'demand':demand_ref,'artifact':artifact_record['resource_ref']})[:24]}"
        result={
            "result_id":result_id,"version":1,
            "execution":{"execution_id":f"execution-{demand['request_id']}","demand":demand_ref,"plan_ref":plan_ref},
            "demand":demand_ref,"artifact_ref":artifact_record["resource_ref"],"artifact_media_type":artifact_record["media_type"],"artifact_width_px":demand["delivery"]["width_px"],"artifact_height_px":demand["delivery"]["height_px"],"completion_status":"COMPLETE","unresolved_roles":[],"provenance_refs":[plan_ref],"evaluation_findings":[{"code":"TECHNICAL_REFERENCE_PASS","verdict":"PASS" if evaluation["hard_gate_result"]=="PASS" else "FAIL","evidence_refs":[artifact_record["resource_ref"]],"note":"Independent certified VLM evaluation was not executed."}],"cost_consumed":{"currency":"EUR","minor_units":0},"attempts_consumed":attempts_consumed,"declared_at":utc_now_rfc3339(),
        }
        self.contracts.validate("asset-result-contract",result)
        return result

    def run_reference_job(self, *, demand: Mapping[str,Any], producer_actor_id: str, evaluator_actor_id: str, worker_id: str, now_ms: int = 1_000_000) -> dict[str,Any]:
        admission=self.admission.admit(demand,idempotency_key=f"admit:{demand['request_id']}:{demand['version']}")
        plan_stored=self.plans.compile(demand,admission["demand_ref"],idempotency_key=f"plan:{demand['request_id']}",include_geometry_reference=True)
        plan=plan_stored["payload"]
        workcell=self.workcells.compile(plan,producer_actor_id=producer_actor_id,evaluator_actor_id=evaluator_actor_id)
        workcell_stored=self.repository.store_object("dynamic_workcell",workcell,object_id=workcell["workcell_id"],version="1.0.0",lifecycle_state="COMPILED",idempotency_key=f"workcell:{demand['request_id']}")
        self.repository.add_edge(plan["plan_id"],workcell["workcell_id"],"resolved_into")
        self.repository.register_worker(worker_id,[item["capability_id"] for item in self.capabilities.all()],canonical_sha256({"worker_id":worker_id,"profiles":self.capabilities.all()}))
        job=self.repository.submit_job({"demand_ref":admission["demand_ref"],"plan_ref":{"object_id":plan["plan_id"],"version":plan["plan_version"],"sha256":canonical_sha256(plan)},"workcell_ref":{"object_id":workcell["workcell_id"],"version":workcell["workcell_version"],"sha256":canonical_sha256(workcell)}},[item["capability_id"] for item in workcell["stage_bindings"]],idempotency_key=f"job:{demand['request_id']}",maximum_attempts=demand["evaluation_policy"]["maximum_rounds"])
        leased=self.repository.lease_next(worker_id,now_ms=now_ms)
        assert leased is not None
        width=demand["delivery"]["width_px"]; height=demand["delivery"]["height_px"]
        segment=self.providers.segmentation(width=width,height=height,logical_uri=f"vae/{demand['request_id']}/mask.png",demand_id=demand["request_id"])
        matting=self.providers.matting(width=width,height=height,logical_uri=f"vae/{demand['request_id']}/cutout.png",demand_id=demand["request_id"])
        gnm=self.providers.gnm_geometry(demand_id=demand["request_id"],purpose="GEOMETRY_REFERENCE",head_pose={"yaw_milliradians":50,"pitch_milliradians":0,"roll_milliradians":0},gaze={"x_basis_points":1500,"y_basis_points":0},logical_uri=f"vae/{demand['request_id']}/gnm-reference.json")
        graph=self.comfyui.compile(plan=plan,workcell=workcell,input_refs=[matting["artifact"]["resource_ref"],segment["artifact"]["resource_ref"]]); self.comfyui.validate(graph)
        checkpoint={"completed_stage_ids":["stage:segmentation","stage:matting","stage:geometry-reference"],"artifact_refs":[segment["artifact"]["resource_ref"],matting["artifact"]["resource_ref"],gnm["artifact"]["resource_ref"]],"comfyui_graph_sha256":graph["graph_sha256"],"quality_round":0}
        self.repository.checkpoint(job["job_id"],worker_id,leased["fencing_token"],checkpoint,now_ms=now_ms+100)
        materialized=self.providers.materialize(width=width,height=height,logical_uri=f"vae/{demand['request_id']}/candidate.png",demand_id=demand["request_id"],wrong_reading_locks=demand["wrong_reading_locks"])
        evaluation=self.evaluator.evaluate(artifact_record=materialized["artifact"],demand=demand,geometry=segment["geometry"],producer_actor_id=producer_actor_id,evaluator_actor_id=evaluator_actor_id)
        result=self.build_result(demand=demand,plan=plan,artifact_record=materialized["artifact"],evaluation=evaluation,attempts_consumed=leased["attempt_number"])
        final_job=self.repository.complete_job(job["job_id"],worker_id,leased["fencing_token"],result,now_ms=now_ms+200)
        result_ref={"result_id":result["result_id"],"version":result["version"],"payload_hash":"sha256:"+canonical_sha256(result),"canonical_ref":f"cmf-contract://results/{result['result_id']}/{result['version']}"}
        stored_result=self.repository.store_object("asset_result_contract",result,object_id=result["result_id"],version="1.0.0",lifecycle_state="RESULT_READY",idempotency_key=f"result:{result['result_id']}")
        self.repository.add_edge(plan["plan_id"],result["result_id"],"produced_result")
        okf=project_okf(plan=plan,result=result,evaluation=evaluation)
        tower=control_tower_projection(admission=admission,plan=plan,workcell=workcell,job=final_job,events=self.repository.list_job_events(job["job_id"]),evaluation=evaluation,result=result)
        return {"admission":admission,"plan":plan,"workcell":workcell,"job":final_job,"segmentation":segment,"matting":matting,"gnm":gnm,"comfyui_graph":graph,"artifact":materialized["artifact"],"evaluation":evaluation,"result":result,"result_ref":result_ref,"okf":okf,"control_tower":tower,"claim_ceiling":"PHASE_08_DELEGATION_VAE_INTEGRATION_DEVELOPMENT_EVIDENCE"}

    def status(self) -> dict[str,Any]:
        return {**self.repository.health(),"lifecycle_state":"phase_08_delegation_vae_integration","delegation_release":self.contracts.version,"delegation_release_digest":self.contracts.digest,"capability_count":len(self.capabilities.all()),"stage5_started":False,"production_authorized":False,"certified":False,"format02_activated":False,"claim_ceiling":"PHASE_08_DELEGATION_VAE_INTEGRATION_DEVELOPMENT_EVIDENCE"}
