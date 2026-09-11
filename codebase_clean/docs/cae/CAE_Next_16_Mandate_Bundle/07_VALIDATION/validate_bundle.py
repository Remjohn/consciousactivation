from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
mandates = sorted(ROOT.rglob('M[0-9][0-9]_*.md'))
mandates = [p for p in mandates if 'ACTIVATION_PROMPT' not in p.name]
assert len(mandates) == 16, len(mandates)
for p in mandates:
    text = p.read_text(encoding='utf-8')
    for marker in [
        '## 1. Decision / Objective',
        '## 2. Governing doctrine and authority',
        '## 3. Mandatory reading before action',
        '## 4. Exact scope',
        '## 5. Required implementation behavior',
        '## 6. Verification and evidence',
        '## 7. Completion / stop condition',
        '## 8. Rollback / recovery',
        '## 9. Operator decision',
        '## 10. False-proof / reward-hacking defense',
    ]:
        assert marker in text, f'{p}: missing {marker}'

prompts = sorted(ROOT.rglob('M[0-9][0-9]_ACTIVATION_PROMPT.md'))
assert len(prompts) == 16, len(prompts)

for p in prompts:
    text=p.read_text(encoding='utf-8')
    assert 'STOP' in text
    assert 'CURRENT.md' in text

for p in [ROOT/'06_OPERATOR_GATES/PHASE_5_GATE.md', ROOT/'06_OPERATOR_GATES/PHASE_6_GATE.md', ROOT/'06_OPERATOR_GATES/PHASE_7_GATE.md', ROOT/'06_OPERATOR_GATES/PHASE_8_GATE.md']:
    assert p.exists()

print(f'VALID: {len(mandates)} mandates, {len(prompts)} activation prompts, 4 phase gates')
