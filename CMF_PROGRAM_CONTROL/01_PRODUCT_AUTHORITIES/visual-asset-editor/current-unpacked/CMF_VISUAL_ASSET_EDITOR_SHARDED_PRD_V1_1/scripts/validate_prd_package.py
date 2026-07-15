from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)

def main() -> int:
    errors: list[str] = []
    req = yaml.safe_load((ROOT / "governance/REQUIREMENTS_REGISTRY.yaml").read_text(encoding="utf-8"))
    dec = json.loads((ROOT / "governance/DECISION_REGISTER.json").read_text(encoding="utf-8"))
    pres = yaml.safe_load((ROOT / "governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml").read_text(encoding="utf-8"))

    frs = req["functional_requirements"]
    nfrs = req["non_functional_requirements"]
    add(errors, len(frs) == 176, f"Expected 176 FRs, found {len(frs)}")
    add(errors, len(nfrs) == 70, f"Expected 70 NFRs, found {len(nfrs)}")
    all_ids = [r["id"] for r in frs] + [r["id"] for r in nfrs]
    add(errors, len(all_ids) == len(set(all_ids)), "Duplicate requirement IDs")

    feature_files = sorted((ROOT / "prd/05-features").glob("F[0-9][0-9]-*.md"))
    add(errors, len(feature_files) == 22, f"Expected 22 feature shards, found {len(feature_files)}")
    fr_re = re.compile(r"^### (FR-[0-9]{3}) —", re.MULTILINE)
    shard_frs: list[str] = []
    for path in feature_files:
        text = path.read_text(encoding="utf-8")
        ids = fr_re.findall(text)
        add(errors, len(ids) == 8, f"{path.name} should contain 8 FRs, found {len(ids)}")
        add(errors, text.count("**Consequences (testable):") == len(ids), f"{path.name} consequence blocks mismatch")
        shard_frs.extend(ids)
    registry_frs = [r["id"] for r in frs]
    add(errors, shard_frs == registry_frs, "Feature-shard FR order/content does not match registry")
    add(errors, registry_frs == [f"FR-{i:03d}" for i in range(1, 177)], "FR IDs are not contiguous FR-001..FR-176")

    nfr_text = (ROOT / "prd/06-cross-cutting-nfrs.md").read_text(encoding="utf-8")
    nfr_re = re.compile(r"^### (NFR-[A-Z]+-[0-9]{3}) —", re.MULTILINE)
    shard_nfrs = nfr_re.findall(nfr_text)
    registry_nfrs = [r["id"] for r in nfrs]
    add(errors, len(shard_nfrs) == 70, f"Expected 70 NFR headings, found {len(shard_nfrs)}")
    add(errors, set(shard_nfrs) == set(registry_nfrs), "NFR shard does not match registry")

    add(errors, len(dec["decisions"]) == 28, f"Expected 28 decisions, found {len(dec['decisions'])}")
    valid_decisions = {d["id"] for d in dec["decisions"]}
    covered_decisions = {d for r in frs for d in r.get("decisions", [])}
    add(errors, not (valid_decisions - covered_decisions), f"Decisions without FR coverage: {sorted(valid_decisions - covered_decisions)}")

    valid_journeys = {f"UJ-{i:02d}" for i in range(1, 17)}
    covered_journeys = {j for r in frs for j in r.get("journeys", [])}
    add(errors, not (valid_journeys - covered_journeys), f"Journeys without FR coverage: {sorted(valid_journeys - covered_journeys)}")

    valid_nfrs = set(registry_nfrs)
    for r in frs:
        add(errors, len(r.get("testable_consequences", [])) >= 2, f"{r['id']} has fewer than 2 consequences")
        unknown = set(r.get("cross_cutting_nfrs", [])) - valid_nfrs
        add(errors, not unknown, f"{r['id']} references unknown NFRs {sorted(unknown)}")

    schema_files = sorted((ROOT / "contracts/schemas").glob("*.schema.yaml"))
    add(errors, len(schema_files) == 13, f"Expected 13 contract schemas, found {len(schema_files)}")
    for path in schema_files:
        try:
            s = yaml.safe_load(path.read_text(encoding="utf-8"))
            for key in ("$schema", "title", "type", "required", "properties"):
                add(errors, key in s, f"{path.name} missing {key}")
            add(errors, s.get("type") == "object", f"{path.name} root type is not object")
        except Exception as exc:
            errors.append(f"Schema parse failed {path.name}: {exc}")

    add(errors, len(pres.get("preserved_architecture", [])) >= 18, "Architecture Preservation Contract is incomplete")

    canonical = list((ROOT / "prd").rglob("*.md")) + list((ROOT / "governance").glob("*.md")) + list((ROOT / "handoff").glob("*.md"))
    for path in canonical:
        text = path.read_text(encoding="utf-8")
        for token in ("{{", "TBD", "TODO", "[placeholder]"):
            if token in text:
                errors.append(f"Placeholder token {token!r} in {path.relative_to(ROOT)}")

    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    broken = []
    links_checked = 0
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in link_re.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:", "asset://", "visual-memory://", "benchmark://", "registry://")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            links_checked += 1
            if not (path.parent / target).resolve().exists():
                broken.append(f"{path.relative_to(ROOT)} -> {target}")
    add(errors, not broken, f"Broken relative links: {broken[:20]}")

    source = json.loads((ROOT / "governance/SOURCE_REGISTER.json").read_text(encoding="utf-8"))
    source_errors = []
    for item in source["sources"]:
        if item["type"] != "local_file":
            continue
        path = Path(item["path"])
        if not path.exists():
            source_errors.append(f"missing {item['id']}: {path}")
            continue
        h = hashlib.sha256(path.read_bytes()).hexdigest()
        if h != item["sha256"]:
            source_errors.append(f"hash mismatch {item['id']}")
    add(errors, not source_errors, f"Source integrity errors: {source_errors}")

    manifest_path = ROOT / "MANIFEST.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_errors = []
        for item in manifest.get("files", []):
            path = ROOT / item["path"]
            if not path.exists():
                manifest_errors.append(f"missing {item['path']}")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
                manifest_errors.append(f"hash mismatch {item['path']}")
        add(errors, not manifest_errors, f"Manifest integrity errors: {manifest_errors[:20]}")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "counts": {
            "features": len(feature_files),
            "functional_requirements": len(frs),
            "non_functional_requirements": len(nfrs),
            "decisions": len(dec["decisions"]),
            "journeys": len(valid_journeys),
            "contract_schemas": len(schema_files),
            "links_checked": links_checked,
        }
    }
    print(json.dumps(result, indent=2))
    (ROOT / "validation/EMBEDDED_VALIDATOR_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
