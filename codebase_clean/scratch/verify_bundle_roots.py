import os

epoch_dir = 'Mandates implementation/epoch_01'
bundles = sorted(os.listdir(epoch_dir))

for b in bundles:
    bpath = os.path.join(epoch_dir, b)
    if not os.path.isdir(bpath):
        continue
    nested = os.path.join(bpath, b)
    if os.path.isdir(nested):
        root_dir = nested
    else:
        root_dir = bpath
    
    files = []
    for r, d, fs in os.walk(root_dir):
        for f in fs:
            if f != 'AGENT_HANDOFF.md' and not f.endswith('.pyc'):
                files.append(os.path.relpath(os.path.join(r, f), root_dir))
    print(f'{b}: using root {root_dir} -> {len(files)} files')
