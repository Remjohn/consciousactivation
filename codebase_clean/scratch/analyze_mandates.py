import glob, os, re, json

files = sorted(glob.glob('docs/cae/CAE_PRD_mandates/**/*.md', recursive=True))
mandates = []
for f in files:
    bn = os.path.basename(f)
    if not re.search(r'MANDATE_\d+', bn):
        continue
    content = open(f, encoding='utf-8').read()
    
    mid = re.search(r'\*\*Mandate ID:\*\*\s*?([^\n]+)?', content)
    cq = re.search(r'\*\*Canonical question:\*\*\s*?([^\n]+)?', content)
    inv = re.search(r'\*\*Primary requirement/invariant:\*\*\s*?([^\n]+)?', content)
    deps = re.search(r'\*\*Dependency set:\*\*\s*([^\n]+)', content)
    surfs = re.search(r'\*\*Primary physical surfaces:\*\*\s*([^\n]+)', content)
    wave = re.search(r'CAE_MANDATE_BUNDLE_WAVE_(\d+)', f)
    
    mandates.append({
        'file': f.replace('\\', '/'),
        'wave': int(wave.group(1)) if wave else 0,
        'id': mid.group(1).strip() if mid else bn,
        'q': cq.group(1).strip() if cq else '?',
        'inv': inv.group(1).strip() if inv else '?',
        'deps': deps.group(1).strip() if deps else '?',
        'surfs': surfs.group(1).strip() if surfs else '?'
    })

print(f"Total mandate files parsed: {len(mandates)}")
with open('scratch/mandates_summary.json', 'w', encoding='utf-8') as out:
    json.dump(mandates, out, indent=2)

for idx, m in enumerate(mandates):
    print(f"[{idx+1:02d}] Wave {m['wave']:02d} | {m['id']} (Q: {m['q']}) | Invariant: {m['inv']}")
