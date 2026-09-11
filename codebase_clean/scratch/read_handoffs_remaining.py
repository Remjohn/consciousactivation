import os, glob, sys
sys.stdout.reconfigure(encoding='utf-8')

epoch_dir = 'Mandates implementation/epoch_01'
bundles = ['CA-M001_BUNDLE', 'CA-M004_BUNDLE', 'CA-M010_BUNDLE', 'CA-M012_BUNDLE']

for b in bundles:
    bpath = os.path.join(epoch_dir, b)
    handoffs = glob.glob(os.path.join(bpath, '**', 'AGENT_HANDOFF*.md'), recursive=True)
    if handoffs:
        print('====================================================')
        print('HANDOFF FOR:', b)
        print('====================================================')
        lines = open(handoffs[0], encoding='utf-8').readlines()
        print(''.join(lines[:45]))
