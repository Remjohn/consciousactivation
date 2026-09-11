from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
mandates = []
activations = []
for p in ROOT.glob("0[1-7]_*/*.md"):
    m = re.match(r"M(6[5-9]|7[0-2])_", p.name)
    if not m:
        continue
    if "ACTIVATION_PROMPT" in p.name:
        activations.append(p)
    else:
        mandates.append(p)

expected = list(range(65,73))
ids = sorted(int(re.search(r"M(\d+)_", p.name).group(1)) for p in mandates)
aids = sorted(int(re.search(r"M(\d+)_", p.name).group(1)) for p in activations)
errors = []
if ids != expected: errors.append(f"mandates={ids} expected={expected}")
if aids != expected: errors.append(f"activations={aids} expected={expected}")

sections = [
"## 1. Decision / Objective",
"## 2. Governing Doctrine and Authority",
"## 3. Mandatory Reading Before Action",
"## 4. Exact Scope",
"## 5. Required Implementation Behavior",
"## 6. Verification and Evidence",
"## 7. Completion / Stop Condition",
"## 8. Rollback / Recovery",
"## 9. Operator Decision",
"## 10. False-Proof / Reward-Hacking Defense",
"## 11. Out-of-Scope but Recorded",
]
for p in mandates:
    txt = p.read_text(encoding="utf-8")
    for s in sections:
        if s not in txt:
            errors.append(f"{p.name}: missing {s}")
for p in activations:
    txt = p.read_text(encoding="utf-8")
    for s in ("Hard STOP", "brownfield preflight", "Operator decision"):
        if s.lower() not in txt.lower():
            errors.append(f"{p.name}: missing {s}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print(f"VALID: {len(mandates)} mandates + {len(activations)} activation prompts")
