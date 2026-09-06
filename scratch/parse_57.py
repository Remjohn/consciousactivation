import re
import json

with open('ChatGPT-Continue Question Eight-20260906-0553.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Lines after 2200 contain the complete, unbroken run of Q1-Q33
lines = text.splitlines()
sub_text = '\n'.join(lines[2210:])

matches = list(re.finditer(r'### Grill Session: Question (\d+) of 33 \| Target: \[PRD\]', sub_text))

data = []
for i, m in enumerate(matches):
    q_num = int(m.group(1))
    start_pos = m.start()
    end_pos = matches[i+1].start() if i+1 < len(matches) else len(sub_text)
    block = sub_text[start_pos:end_pos]
    
    # Precheck
    pre_m = re.search(r'\*\*Zero-waste precheck.*?\*\*:(.*?)(?=\n\n|\n###)', block, re.DOTALL)
    precheck = ' '.join(pre_m.group(1).split()) if pre_m else ''
    
    # Recommendation text
    rscs_m = re.search(r'### RSCS Recommendation.*?\n(.*?)(?=\n###|\n\*\*Question|\n##|\n\*\*Final Question)', block, re.DOTALL)
    rscs = ' '.join(rscs_m.group(1).split()) if rscs_m else ''
    
    # The actual question prompt
    q_prompt_m = re.search(r'(\*\*Question.*?\*\*|\*\*Final Question.*?\*\*|Question:)(.*?)(?=\n\n|\n##)', block, re.DOTALL)
    q_prompt = ' '.join(q_prompt_m.group(2).split()) if q_prompt_m else ''
    
    # Collision primitives
    collisions = re.findall(r'\[(PREDICTION VIOLATION|COSTLY EXPOSURE|LATENT PATTERN ARTICULATION)\]', block)
    
    # Code references
    code_refs = re.findall(r'`([a-zA-Z0-9_\-\.\/]+\.(?:py|yaml|md|json|ts|tsx|sql))`', block)
    code_refs = list(dict.fromkeys(code_refs))
    
    data.append({
        'q_num': q_num,
        'precheck': precheck[:250],
        'rscs_lead': rscs[:300],
        'question': q_prompt[:300],
        'collisions': list(set(collisions)),
        'refs': code_refs[:6]
    })

# Keep the latest occurrence for each question 1..33
final_map = {}
for item in data:
    final_map[item['q_num']] = item

print(f"Total unique questions mapped: {len(final_map)}")
with open('scratch/q1_33_extracted.json', 'w', encoding='utf-8') as out:
    json.dump(final_map, out, indent=2)

for q in sorted(final_map.keys()):
    it = final_map[q]
    safe_lead = it['rscs_lead'][:100].encode('ascii', 'replace').decode('ascii')
    print(f"Q{q:02d}: {safe_lead}... | Collisions: {it['collisions']} | Refs: {it['refs']}")

