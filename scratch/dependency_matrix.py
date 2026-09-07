import json, re
from collections import defaultdict

data = json.load(open('scratch/detailed_mandates.json', encoding='utf-8'))

# Map out physical surfaces touched by each mandate
mandate_surfs = {}
for m in data:
    mid = m['id']
    surfs = m['surfs']
    # clean surfaces
    s_list = [s.strip() for s in re.split(r'[;,]', surfs) if s.strip() and s.strip() != '?']
    mandate_surfs[mid] = s_list

# Check which mandates share surfaces
surface_conflicts = defaultdict(list)
for mid1, s1 in mandate_surfs.items():
    for mid2, s2 in mandate_surfs.items():
        if mid1 >= mid2:
            continue
        common = set(s1).intersection(set(s2))
        if common:
            surface_conflicts[(mid1, mid2)] = list(common)

print(f"Total pairs with surface conflicts: {len(surface_conflicts)}")
for (m1, m2), comm in list(surface_conflicts.items())[:20]:
    print(f"{m1} <--> {m2}: {comm}")
