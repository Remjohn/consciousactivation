#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REG = ROOT / "docs/cae/CAE_Visual_Production_External_Adoption_M0073_v1/M0073_EXTERNAL_REPOSITORY_ADOPTION_REGISTRY.json"
REQUIRED = {
    "id","name","url","classification","boundary_type","license","source_ref","source_commit_sha",
    "source_paths","adopted_behavior","excluded_behavior","cae_destination","process_boundary",
    "integration_owner","status","evidence_class","verification_note"
}
CLASSES={"behavioral_reference","isolated_upstream_dependency","embedded_primitive","runtime","visual_intelligence_engine"}
STATUSES={"LOCALLY_VERIFIED_SNAPSHOT","TAG_VERIFIED_SHA_UNAVAILABLE","PARTIALLY_VERIFIED_BLOCKED","LOCALLY_ALIGNED_EXTERNALLY_BLOCKED"}
BLOCKED={"PARTIALLY_VERIFIED_BLOCKED","TAG_VERIFIED_SHA_UNAVAILABLE","LOCALLY_ALIGNED_EXTERNALLY_BLOCKED"}

def load():
    data=json.loads(REG.read_text(encoding="utf-8"))
    assert data["mandate_id"]=="M0073"
    assert len(data["external_registry"])==16
    return data

def validate(data, require_complete=False):
    problems=[]
    ids=set()
    for e in data["external_registry"]:
        missing=REQUIRED-set(e)
        if missing: problems.append(f"{e.get('name','?')}: missing {sorted(missing)}")
        if e.get("id") in ids: problems.append(f"duplicate id: {e.get('id')}")
        ids.add(e.get("id"))
        if e.get("classification") not in CLASSES: problems.append(f"{e.get('name')}: invalid classification")
        if not e.get("source_paths"): problems.append(f"{e.get('name')}: no source paths")
        if not e.get("adopted_behavior") or not e.get("excluded_behavior"): problems.append(f"{e.get('name')}: behavior boundary incomplete")
        if e.get("source_commit_sha") is None and e.get("status") not in BLOCKED:
            problems.append(f"{e.get('name')}: exact source SHA absent without blocking status")
        if require_complete and e.get("source_commit_sha") is None:
            problems.append(f"{e.get('name')}: completion requires exact source SHA")
    return problems

def self_test():
    data=load()
    p=validate(data)
    assert not p, "\n".join(p)
    # Contrastive false-proof: a good-looking registry row with omitted exclusion must fail.
    bad=json.loads(json.dumps(data))
    bad["external_registry"][0]["excluded_behavior"]=""
    p=validate(bad)
    assert any("behavior boundary incomplete" in x for x in p), p
    # Completion gate: unresolved external refs must not claim completeness.
    p=validate(data, require_complete=True)
    assert p, "incomplete external refs incorrectly accepted as complete"
    return True

if __name__=="__main__":
    data=load()
    if "--self-test" in sys.argv:
        self_test()
        print("M0073 registry self-test: PASS")
    else:
        problems=validate(data)
        if problems:
            for p in problems: print("ERROR:",p)
            raise SystemExit(1)
        print("M0073 registry structural validation: PASS")
