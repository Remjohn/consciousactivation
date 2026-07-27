from __future__ import annotations

SCHEMA_NAMES = [
    "canonical-interview-source-package", "transcript-alignment", "packed-phrase-transcript",
    "source-visual-structure-index", "tag-assertion", "anchor-hit", "expression-moment",
    "reaction-observation", "reaction-receipt", "live-activative-session", "asset-package-spec",
    "observed-expression-evidence-pack",
]

def schema_for(name: str) -> dict[str, object]:
    id_field={
        "canonical-interview-source-package":"package_id","transcript-alignment":"alignment_id","packed-phrase-transcript":"phrase_pack_id","source-visual-structure-index":"visual_index_id","tag-assertion":"tag_assertion_id","anchor-hit":"anchor_hit_id","expression-moment":"expression_moment_id","reaction-observation":"observation_id","reaction-receipt":"reaction_receipt_id","live-activative-session":"session_id","asset-package-spec":"asset_package_spec_id","observed-expression-evidence-pack":"observed_evidence_pack_id",
    }[name]
    return {"$schema":"https://json-schema.org/draft/2020-12/schema","$id":f"https://conscious-activations.local/schemas/interview-expression/{name}/1.0.0","title":name,"type":"object","required":[id_field,"version"],"properties":{id_field:{"type":"string","minLength":1},"version":{"type":"string","const":"1.0.0"}},"additionalProperties":True,"x-ca-closed-runtime-validation":True}
