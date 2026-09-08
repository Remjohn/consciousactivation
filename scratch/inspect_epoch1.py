import os, glob
from collections import defaultdict

epoch_dir = 'Mandates implementation/epoch_01'
bundles = sorted(os.listdir(epoch_dir))

dest_to_bundles = defaultdict(list)

for b in bundles:
    bpath = os.path.join(epoch_dir, b)
    if not os.path.isdir(bpath):
        continue
    # find root inside bundle (handles nested folder like CA-M001_BUNDLE/CA-M001_BUNDLE/...)
    nested = os.path.join(bpath, b)
    root_src = nested if os.path.exists(nested) else bpath
    
    for root, dirs, files in os.walk(root_src):
        for f in files:
            if f == 'AGENT_HANDOFF.md' or f.endswith('.pyc') or f.endswith('.DS_Store'):
                continue
            full_p = os.path.join(root, f)
            rel_p = os.path.relpath(full_p, root_src)
            dest_to_bundles[rel_p.replace('\\', '/')].append(b)

collisions = {k: v for k, v in dest_to_bundles.items() if len(v) > 1}
if collisions:
    print('WARNING: Collisions found!')
    for k, v in collisions.items():
        print(f'  {k} -> {v}')
else:
    print(f'SUCCESS: Zero collisions among all {len(dest_to_bundles)} unique files across the 7 bundles!')

print('\nTotal unique destination files to deploy:', len(dest_to_bundles))
for f, b in sorted(dest_to_bundles.items())[:25]:
    print(f'  [{b[0]}] -> {f}')
if len(dest_to_bundles) > 25:
    print(f'  ... and {len(dest_to_bundles)-25} more')
