#!/usr/bin/env python3
from pathlib import Path
import re, sys

root = Path(__file__).resolve().parents[1]
required = [
"## Kernel","## Identity & Persona","## Operating Doctrine","## Decision Heuristics",
"## Activation & Context","## Investigation Protocol","## Evidence & Uncertainty",
"## Execution Loop","## Quality Loop","## Boundaries & Escalation",
"## Handoff Protocol","## Capability Menu","## Output Contract"
]
bad=False
for p in sorted((root/"gemini_execution/agents").glob("cae-*.md")):
    text=p.read_text()
    prose=re.sub(r"^#.*$","",text,flags=re.M)
    count=len(re.findall(r"\b[\w’'-]+\b",prose))
    missing=[h for h in required if h not in text]
    print(f"{p.name}: {count} words" + (f"; missing={missing}" if missing else ""))
    if missing or not 500 <= count <= 700: bad=True
sys.exit(1 if bad else 0)
