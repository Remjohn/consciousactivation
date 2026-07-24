from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ca_contracts import canonical_json_text, canonical_sha256

from .application import VAEApplication


def _ref(object_id: str, seed: str) -> dict[str,str]: return {"object_id":object_id,"version":"1.0.0","sha256":canonical_sha256({"seed":seed})}


def run_phase8_demo(output_dir: str|Path, delegation_root: str|Path) -> dict[str,Any]:
    from cmf_pipeline.delegation import VisualDelegationService
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    pipeline=VisualDelegationService(delegation_root)
    demand_package=pipeline.compile_demand(
        source_package_ref=_ref("source-package:phase8","source"),
        reaction_receipt_refs=[_ref("reaction-receipt:phase8","reaction")],
        expression_moment_refs=[_ref("expression-moment:phase8","moment")],
        semantic_program_ref=_ref("semantic-program:phase8","semantic"),
        final_script_ref=_ref("final-script:phase8","script"),
        primitive_coalition_ref=_ref("primitive-coalition:phase8","primitive"),
        archetype_coalition_ref=_ref("archetype-coalition:phase8","archetype"),
        activation_transfer_contract_ref=_ref("transfer-contract:phase8","transfer"),
        content_harness_ref=_ref("harness:phase8","harness"),
        category_profile_ref=_ref("category:static-composition","category"),
        format_profile_ref=_ref("format:supervisual","format"),
        width_px=320,height_px=320,
        wrong_reading_locks=["Do not erase source identity.","Preserve negative space for the approved claim."],
    )
    app=VAEApplication(out/"vae.sqlite3",out/"storage",delegation_root); init=app.initialize()
    flow=app.run_reference_job(demand=demand_package["demand"],producer_actor_id="vae-reference-materializer",evaluator_actor_id="vae-independent-technical-evaluator",worker_id="worker:phase8-reference")
    acknowledgement=pipeline.acknowledge(demand=flow["admission"]["demand_ref"],result=flow["result"],decision="ACCEPTED_WITH_CONCERNS",consumption_authorized=False,evidence_ref=flow["artifact"]["resource_ref"])
    artifacts={
        "demand.json":demand_package["demand"],"plan.json":flow["plan"],"workcell.json":flow["workcell"],"comfyui-graph.json":flow["comfyui_graph"],"evaluation.json":flow["evaluation"],"asset-result.json":flow["result"],"result-acknowledgement.json":acknowledgement,"control-tower.json":flow["control_tower"],"okf-projection.json":{k:v for k,v in flow["okf"].items() if k!="markdown"},"demo-receipt.json":{"initialization":init,"claim_ceiling":flow["claim_ceiling"],"real_sam3_executed":False,"real_lucida_executed":False,"real_comfyui_worker_executed":False,"real_google_gnm_executed":False,"production_authorized":False,"certified":False,"format02_activated":False},
    }
    for name,payload in artifacts.items(): (out/name).write_text(canonical_json_text(payload)+"\n",encoding="utf-8")
    (out/"visual-asset-result.md").write_text(flow["okf"]["markdown"],encoding="utf-8")
    data,_=app.store.get(flow["artifact"]["sha256"]); (out/"reference-visual-asset.png").write_bytes(data)
    return {"output_dir":str(out),"files":sorted(path.name for path in out.iterdir() if path.is_file()),"result_id":flow["result"]["result_id"],"acknowledgement_id":acknowledgement["acknowledgement_id"],"artifact_sha256":flow["artifact"]["sha256"],"claim_ceiling":flow["claim_ceiling"]}
