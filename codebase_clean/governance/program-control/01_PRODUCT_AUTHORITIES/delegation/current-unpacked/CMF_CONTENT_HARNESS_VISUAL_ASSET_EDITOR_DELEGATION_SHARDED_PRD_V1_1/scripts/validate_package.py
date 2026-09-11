#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, re, sys, zipfile
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "decisions": 16,
    "features": 16,
    "functional_requirements": 128,
    "non_functional_requirements": 60,
    "journeys": 14,
    "schemas": 25,
    "examples": 25,
    "messages": 25,
    "scenarios": 10,
}
errors=[]
checks={}

def fail(msg): errors.append(msg)
def load_yaml(p):
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"YAML parse failed {p.relative_to(ROOT)}: {e}")
        return None
def load_json(p):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"JSON parse failed {p.relative_to(ROOT)}: {e}")
        return None
def sha256(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

# Core registries
dec=load_json(ROOT/"governance/DECISION_REGISTER.json")
req=load_yaml(ROOT/"governance/REQUIREMENTS_REGISTRY.yaml")
msg=load_yaml(ROOT/"governance/MESSAGE_TYPE_REGISTRY.yaml")
life=load_yaml(ROOT/"governance/LIFECYCLE_MACHINE.yaml")
auth=load_yaml(ROOT/"governance/AUTHORITY_MATRIX.yaml")
scn=load_yaml(ROOT/"reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/SCENARIO_MANIFEST.yaml")

if dec and len(dec.get("decisions",[])) != EXPECTED["decisions"]: fail("Decision count mismatch")
if req:
    counts=req.get("counts",{})
    for key in ["features","functional_requirements","non_functional_requirements","decisions","journeys"]:
        if counts.get(key) != EXPECTED[key]: fail(f"Requirements count mismatch for {key}: {counts.get(key)}")
if msg and len(msg.get("messages",[])) != EXPECTED["messages"]: fail("Message registry count mismatch")
if scn and len(scn.get("scenarios",[])) != EXPECTED["scenarios"]: fail("Format 02 scenario count mismatch")
if auth and not auth.get("domains"): fail("Authority matrix has no domains")

# IDs and traceability
if req:
    frs=req.get("functional_requirements",[])
    nfrs=req.get("non_functional_requirements",[])
    fids=[x.get("id") for x in frs]
    nids=[x.get("id") for x in nfrs]
    if len(fids)!=len(set(fids)): fail("Duplicate FR IDs")
    if len(nids)!=len(set(nids)): fail("Duplicate NFR IDs")
    known_nfr=set(nids)
    decisions={x.get("decision_id") for x in dec.get("decisions",[])} if dec else set()
    journeys={x.get("journey_id") for x in req.get("journeys",[])}
    for fr in frs:
        if fr.get("decision_id") not in decisions: fail(f"{fr.get('id')} unknown decision")
        for j in fr.get("journeys",[]): 
            if j not in journeys: fail(f"{fr.get('id')} unknown journey {j}")
        for n in fr.get("nfr_refs",[]):
            if n not in known_nfr: fail(f"{fr.get('id')} unknown NFR {n}")
        if not fr.get("consequences"): fail(f"{fr.get('id')} missing consequences")
    feature_files=list((ROOT/"prd/05-features").glob("F*.md"))
    if len(feature_files)!=EXPECTED["features"]: fail(f"Feature file count {len(feature_files)}")

# Schema/example validation
schema_dir=ROOT/"contracts/schemas"; example_dir=ROOT/"contracts/examples"
schemas=sorted(schema_dir.glob("*.schema.yaml"))
examples=sorted(example_dir.glob("*.example.yaml"))
if len(schemas)!=EXPECTED["schemas"]: fail(f"Schema count {len(schemas)}")
if len(examples)!=EXPECTED["examples"]: fail(f"Example count {len(examples)}")
format_checker=FormatChecker()
for sp in schemas:
    schema=load_yaml(sp)
    if schema is None: continue
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as e:
        fail(f"Invalid JSON Schema {sp.name}: {e}")
        continue
    ep=example_dir/(sp.name.replace(".schema.yaml",".example.yaml"))
    if not ep.exists():
        fail(f"Missing example for {sp.name}")
        continue
    example=load_yaml(ep)
    if example is None: continue
    errs=sorted(Draft202012Validator(schema,format_checker=format_checker).iter_errors(example),key=lambda e:list(e.path))
    for e in errs:
        path=".".join(str(x) for x in e.path)
        fail(f"Example validation {ep.name} at {path or '<root>'}: {e.message}")

# Message registry files
if msg:
    for m in msg.get("messages",[]):
        for field in ("schema","example"):
            p=ROOT/m[field]
            if not p.exists(): fail(f"Message registry missing {field}: {m[field]}")

# Lifecycle
if life:
    states=set(life.get("states",{}))
    if life.get("initial_state") not in states: fail("Invalid lifecycle initial state")
    for t in life.get("transitions",[]):
        if t.get("from") not in states or t.get("to") not in states:
            fail(f"Transition references unknown state: {t}")

# Traceability CSV
trace=ROOT/"governance/TRACEABILITY_MATRIX.csv"
if trace.exists():
    with trace.open(encoding="utf-8",newline="") as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=EXPECTED["functional_requirements"]: fail(f"Traceability row count {len(rows)}")
else: fail("Missing traceability matrix")

# Relative Markdown links
link_re=re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for md in ROOT.rglob("*.md"):
    text=md.read_text(encoding="utf-8")
    for target in link_re.findall(text):
        target=target.strip().split("#",1)[0]
        if not target or target.startswith(("http://","https://","mailto:","asset://","contract://","visual-editor://","diagnostic://","#")):
            continue
        p=(md.parent/target).resolve()
        try: p.relative_to(ROOT.resolve())
        except ValueError:
            fail(f"Markdown link escapes package: {md.relative_to(ROOT)} -> {target}")
            continue
        if not p.exists(): fail(f"Broken link: {md.relative_to(ROOT)} -> {target}")

# Placeholder scan, excluding intentional templates
for p in ROOT.rglob("*"):
    if not p.is_file() or p.suffix.lower() not in {".md",".yaml",".yml",".json",".csv",".py"}: continue
    rel=p.relative_to(ROOT).as_posix()
    if rel.startswith(("templates/","scripts/","validation/")) or rel.endswith("FEATURE_TECH_SPEC_TEMPLATE.md"): continue
    text=p.read_text(encoding="utf-8",errors="ignore")
    for bad in ("{{","TBD","TODO"):
        if bad in text: fail(f"Placeholder {bad!r} in {rel}")

# Manifest integrity
manifest_path=ROOT/"MANIFEST.json"
if manifest_path.exists():
    man=load_json(manifest_path)
    if man:
        for rec in man.get("files",[]):
            p=ROOT/rec["path"]
            if not p.exists(): fail(f"Manifest missing file {rec['path']}")
            elif sha256(p)!=rec["sha256"]: fail(f"Manifest hash mismatch {rec['path']}")
else:
    checks["manifest"]="not_present_during_initial_build"

# ZIP integrity if built
zip_path=ROOT.parent/(ROOT.name+".zip")
if zip_path.exists():
    try:
        with zipfile.ZipFile(zip_path) as z:
            bad=z.testzip()
            if bad: fail(f"ZIP corrupt member {bad}")
    except Exception as e: fail(f"ZIP integrity failed: {e}")
else:
    checks["zip"]="not_present_during_initial_build"

checks.update({
    "decisions": EXPECTED["decisions"],
    "features": EXPECTED["features"],
    "functional_requirements": EXPECTED["functional_requirements"],
    "non_functional_requirements": EXPECTED["non_functional_requirements"],
    "journeys": EXPECTED["journeys"],
    "schemas": len(schemas),
    "examples": len(examples),
    "messages": EXPECTED["messages"],
    "scenarios": EXPECTED["scenarios"],
    "relative_links": "checked",
})

result={"status":"PASS" if not errors else "FAIL","checks":checks,"errors":errors}
print(json.dumps(result,indent=2))
sys.exit(0 if not errors else 1)
