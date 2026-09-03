#!/usr/bin/env python3
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
mandates = sorted((ROOT/"gemini_execution/mandates").glob("M*.md"))
prompts = sorted((ROOT/"gemini_execution/prompts").glob("GEMINI_M*_ACTIVATION_PROMPT.md"))
gates = sorted((ROOT/"gemini_execution/gates").glob("OPERATOR_GATE_M*.md"))
agents = sorted((ROOT/"gemini_execution/agents").glob("cae-*.md"))

errors=[]
if len(mandates) != 12: errors.append(f"expected 12 mandates, found {len(mandates)}")
if len(prompts) != 12: errors.append(f"expected 12 activation prompts, found {len(prompts)}")
if len(gates) != 12: errors.append(f"expected 12 operator gates, found {len(gates)}")
if len(agents) < 19: errors.append(f"expected >=19 agents, found {len(agents)}")

required_sections = [
    "## 1. Assignment",
    "## 2. Authority",
    "## 3. Mandatory reading",
    "## 4. Scope",
    "## 6. Required execution pattern",
    "## 7. Evidence and fidelity",
    "## 8. False-proof defenses",
    "## 9. Error taxonomy",
    "## 10. Completion criteria",
    "## 11. Rollback",
    "## 12. Operator gate",
    "## 13. Activation prompt",
]
for p in mandates:
    s=p.read_text(encoding="utf-8")
    for sec in required_sections:
        if sec not in s:
            errors.append(f"{p.name}: missing {sec}")
    if len(s.split()) < 900:
        errors.append(f"{p.name}: only {len(s.split())} words")

for p in prompts:
    if len(p.read_text(encoding="utf-8").split()) < 180:
        errors.append(f"{p.name}: activation prompt too short")

if errors:
    print("FAIL")
    print("\n".join(errors))
    sys.exit(1)

print("PASS")
print(f"mandates={len(mandates)} prompts={len(prompts)} gates={len(gates)} agents={len(agents)}")
