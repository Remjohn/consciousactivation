#!/usr/bin/env python3
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
PRD=ROOT/"prd"
def strip_fm(t):
    if t.startswith("---\n"):
        parts=t.split("---\n",2)
        if len(parts)==3:return parts[2].lstrip()
    return t
feature_files=sorted((PRD/"05-features").glob("F*.md"))
paths=[PRD/x for x in ["00-document-purpose.md","01-vision-product-promise.md","02-users-and-journeys.md","03-product-doctrine.md","04-glossary.md"]]
paths+=feature_files
paths+=[PRD/x for x in ["06-cross-cutting-nfrs.md","07-shared-lifecycle.md","08-success-metrics.md","09-non-goals.md","10-release-scope.md","11-risks.md","12-assumptions-open-questions.md","13-source-register.md"]]
front={"title":"PRD: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol","status":"draft_for_review","version":"0.1.0-draft","updated":"2026-07-13"}
out="---\n"+yaml.safe_dump(front,sort_keys=False,allow_unicode=True)+"---\n\n# PRD: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol\n\n> Combined rendering of the authoritative shards. Do not edit independently.\n"
for p in paths:out+="\n\n---\n\n"+strip_fm(p.read_text(encoding="utf-8"))
(PRD/"PRD_COMBINED.md").write_text(out,encoding="utf-8")
print(PRD/"PRD_COMBINED.md")
