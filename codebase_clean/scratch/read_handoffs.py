import os, glob, sys
sys.stdout.reconfigure(encoding='utf-8')

epoch_dir = 'Mandates implementation/epoch_01'
bundles = sorted(os.listdir(epoch_dir))

for b in bundles:
    bpath = os.path.join(epoch_dir, b)
    if not os.path.isdir(bpath):
        continue
    handoffs = glob.glob(os.path.join(bpath, '**', 'AGENT_HANDOFF*.md'), recursive=True)
    if handoffs:
        print('====================================================')
        print('HANDOFF FOR:', b)
        print('====================================================')
        lines = open(handoffs[0], encoding='utf-8').readlines()
        print(''.join(lines[:45]))
