from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parent
mandates = sorted((ROOT / '02_MANDATES').glob('CA-CSR-*.md'))
required = [
    '## 1. Identity and status',
    '## 2. Decision / objective being authorized',
    '## 3. Governing doctrine and authority sources',
    '## 4. Mandatory reading before action',
    '## 5. Exact scope',
    '## 6. Allowed artifacts and file boundary',
    '## 7. Prohibitions and collision procedure',
    '## 8. Required work / implementation behavior',
    '## 9. Verification and evidence standard',
    '## 10. Completion and stop condition',
    '## 11. Rollback / recovery',
    '## 12. Operator decision',
    '## 13. Activation prompt',
]
errors = []
for path in mandates:
    text = path.read_text()
    for heading in required:
        if heading not in text:
            errors.append(f'{path.name}: missing {heading}')
    p = text.split('## 13. Activation prompt', 1)[1]
    words = re.findall(r"\b\w[\w'-]*\b", p)
    if not 200 <= len(words) <= 340:
        errors.append(f'{path.name}: activation prompt word count {len(words)}')
    for token in ['CA-CSR-', '01_CA_MANDATE_AUTHORING_PROTOCOL.md', '02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md', 'stop']:
        if token.lower() not in p.lower():
            errors.append(f'{path.name}: prompt missing {token}')

manifest = json.loads((ROOT/'00_MANIFEST/01_FILE_MANIFEST.json').read_text())
for item in manifest['artifacts']:
    if not (ROOT/item['path']).exists():
        errors.append(f"manifest missing file: {item['path']}")

if errors:
    print('VALIDATION FAILED')
    print('\n'.join(errors))
    sys.exit(1)
print(f'VALIDATION PASS: {len(mandates)} mandates; manifest files present; activation prompts within expected size envelope.')
