import glob, os, re, json

files = sorted(glob.glob('docs/cae/CAE_PRD_mandates/**/*.md', recursive=True))
mandates = []
for f in files:
    bn = os.path.basename(f)
    if not re.search(r'MANDATE_\d+', bn):
        continue
    content = open(f, encoding='utf-8').read()
    
    # Extract title
    title_m = re.search(r'^#\s+([^\n]+)', content, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else bn
    
    # Extract section 1
    mid = re.search(r'\*\*Mandate ID:\*\*\s*?([^\n]+)?', content)
    cq = re.search(r'\*\*Canonical question:\*\*\s*?([^\n]+)?', content)
    inv = re.search(r'\*\*(?:Primary requirement/invariant|Primary invariant|Invariant):\*\*\s*?([^\n]+)?', content)
    deps = re.search(r'\*\*Dependency set:\*\*\s*([^\n]+)', content)
    surfs = re.search(r'\*\*Primary physical surfaces:\*\*\s*([^\n]+)', content)
    wave = re.search(r'CAE_MANDATE_BUNDLE_WAVE_(\d+)', f)
    
    # Allowed artifacts (section 6)
    sec6 = re.search(r'## 6\. Allowed artifacts[^\n]*\n+(.*?)(?=## 7|\Z)', content, re.DOTALL)
    allowed = sec6.group(1).strip() if sec6 else ''
    
    # Prohibitions (section 7)
    sec7 = re.search(r'## 7\. Prohibitions[^\n]*\n+(.*?)(?=## 8|\Z)', content, re.DOTALL)
    prohib = sec7.group(1).strip() if sec7 else ''
    
    # Dependencies (from sec 5 or 1)
    mandates.append({
        'file': f.replace('\\', '/'),
        'wave': int(wave.group(1)) if wave else 0,
        'title': title,
        'id': mid.group(1).strip() if mid else bn,
        'q': cq.group(1).strip() if cq else '?',
        'inv': inv.group(1).strip() if inv else '?',
        'deps': deps.group(1).strip() if deps else '?',
        'surfs': surfs.group(1).strip() if surfs else '?',
        'allowed_artifacts': allowed,
        'prohibitions': prohib
    })

print(f"Parsed {len(mandates)} mandates.")
with open('scratch/detailed_mandates.json', 'w', encoding='utf-8') as out:
    json.dump(mandates, out, indent=2)

for m in mandates:
    print(f"W{m['wave']} | {m['id']} | Q: {m['q']} | Title: {m['title'][:55]} | Surfs: {m['surfs'][:50]}")
