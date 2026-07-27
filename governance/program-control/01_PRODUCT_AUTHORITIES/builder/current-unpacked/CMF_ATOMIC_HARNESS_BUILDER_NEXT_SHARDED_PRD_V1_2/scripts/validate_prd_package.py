from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    req = yaml.safe_load((ROOT / "governance/REQUIREMENTS_REGISTRY.yaml").read_text(encoding="utf-8"))
    dec = json.loads((ROOT / "governance/DECISION_REGISTER.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))

    frs = req["functional_requirements"]
    nfrs = req["non_functional_requirements"]
    ids = [r["id"] for r in frs] + [r["id"] for r in nfrs]
    if len(ids) != len(set(ids)):
        fail("Duplicate requirement IDs", errors)

    # Cross-check the human-readable PRD shards against the machine registry.
    feature_files = sorted((ROOT / "prd/05-features").glob("F[0-9][0-9]-*.md"))
    if len(feature_files) != 18:
        fail(f"Expected 18 feature shards, found {len(feature_files)}", errors)
    fr_heading_re = re.compile(r"^### (FR-[0-9]{3}) —", re.MULTILINE)
    shard_fr_ids: list[str] = []
    for feature_file in feature_files:
        shard_fr_ids.extend(fr_heading_re.findall(feature_file.read_text(encoding="utf-8")))
    registry_fr_ids = [r["id"] for r in frs]
    if len(shard_fr_ids) != len(set(shard_fr_ids)):
        fail("Duplicate FR headings in feature shards", errors)
    if shard_fr_ids != registry_fr_ids:
        fail("Feature-shard FR order/content does not match requirements registry", errors)

    nfr_text = (ROOT / "prd/06-cross-cutting-nfrs.md").read_text(encoding="utf-8")
    nfr_heading_re = re.compile(r"^### (NFR-[A-Z]+-[0-9]{3}) —", re.MULTILINE)
    shard_nfr_ids = nfr_heading_re.findall(nfr_text)
    registry_nfr_ids = [r["id"] for r in nfrs]
    if len(shard_nfr_ids) != len(set(shard_nfr_ids)):
        fail("Duplicate NFR headings in NFR shard", errors)
    if set(shard_nfr_ids) != set(registry_nfr_ids):
        fail("NFR shard content does not match requirements registry", errors)
    if nfr_text.startswith("---\n"):
        end = nfr_text.find("\n---\n", 4)
        nfr_frontmatter = yaml.safe_load(nfr_text[4:end]) if end >= 0 else {}
        if nfr_frontmatter.get("nfr_count") != len(nfrs):
            fail("NFR frontmatter count does not match registry", errors)

    valid_nfrs = set(registry_nfr_ids)
    for r in frs:
        unknown_nfrs = set(r.get("cross_cutting_nfrs", [])) - valid_nfrs
        if unknown_nfrs:
            fail(f"FR references unknown NFRs: {r['id']} -> {sorted(unknown_nfrs)}", errors)
    if len(dec["decisions"]) != 33:
        fail("Decision register does not contain 33 decisions", errors)
    valid_decisions = {d["id"] for d in dec["decisions"]}
    covered = {d for r in frs for d in r.get("decisions", [])}
    missing = valid_decisions - covered
    if missing:
        fail(f"Decisions without FR coverage: {sorted(missing)}", errors)
    for r in frs:
        if not r.get("testable_consequences"):
            fail(f"FR without testable consequences: {r['id']}", errors)
    import hashlib
    for item in manifest["files"]:
        p = ROOT / item["path"]
        if not p.exists():
            fail(f"Manifest file missing: {item['path']}", errors)
            continue
        actual_hash = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual_hash != item.get("sha256"):
            fail(f"Manifest hash mismatch: {item['path']}", errors)
    canonical = list((ROOT / "prd").rglob("*.md")) + list((ROOT / "governance").glob("*.md"))
    bad_tokens = ["{{", "TBD", "TODO", "[placeholder]"]
    for path in canonical:
        text = path.read_text(encoding="utf-8")
        for token in bad_tokens:
            if token in text:
                fail(f"Placeholder token {token!r} in {path.relative_to(ROOT)}", errors)
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in link_re.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            if not (path.parent / target).resolve().exists():
                fail(f"Broken link in {path.relative_to(ROOT)}: {target}", errors)
    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
