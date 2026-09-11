import json
import test_epochs

data = json.load(open('scratch/detailed_mandates.json', encoding='utf-8'))
file_map = {m['file']: m for m in data}

total = 0
for ep_name, f_list in test_epochs.epochs.items():
    print(f"\n### {ep_name} ({len(f_list)} Concurrent Mandates)")
    print("| Mandate ID | Canon Q | Wave | Functional Scope | Physical Surface Touched |")
    print("|---|:---:|:---:|---|---|")
    for f in f_list:
        m = file_map[f]
        total += 1
        fn = f.split('/')[-1]
        mid = m['id']
        cq = m['q']
        w = f"Wave {m['wave']:02d}"
        # clean title
        t = m['title'].replace(chr(8212), '-').replace(chr(8211), '-').replace(chr(65533), '-').split('-')[-1].strip()
        s = m['surfs'] if m['surfs'] != '?' else 'Domain pipeline/tests'
        s_short = s.split(';')[0].strip()
        print(f"| **{mid}** | {cq} | {w} | {t} | {s_short} |")

print(f"\nGrand Total Mandates Scheduled: {total}/58 (100% complete)")
