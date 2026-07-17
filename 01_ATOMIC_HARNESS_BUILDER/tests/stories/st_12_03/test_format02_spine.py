import pytest

from cmf_builder.application.reference_spine import REQUIRED_STEPS, Format02SpineError, Format02SpineProof


def proof(**overrides):
    values = {
        "proof_identity_seed": "proof:format02",
        "admitted_corpus_refs": ("admitted:format02:1",),
        "excluded_corpus_refs_used": (),
        "category_identity": "2D_CHARACTER_ANIMATION",
        "profile_identity": "FORMAT_02",
        "character_performance_requirements": tuple(f"character:req:{i}" for i in range(13)),
        "wrong_reading_locks": ("not edited video", "not conversational timeline"),
        "lineage_refs": ("source", "ir", "target"),
        "executed_steps": REQUIRED_STEPS,
    }
    values.update(overrides)
    return Format02SpineProof(**values)


def test_format02_spine_records_complete_development_uncertified_chain():
    result = proof()

    assert result.as_dict()["format02_spine"] == "DEVELOPMENT_UNCERTIFIED"
    assert result.as_dict()["bd_008"] == "OPEN"
    assert result.as_dict()["external_vae_execution"] == "NOT_PERFORMED"
    assert result.as_dict()["production_ready"] is False


def test_format02_spine_rejects_excluded_corpus_flattening_missing_steps_and_certification():
    with pytest.raises(Format02SpineError) as corpus:
        proof(excluded_corpus_refs_used=("excluded:1",))
    assert corpus.value.code == "EXCLUDED_CORPUS_USED"

    with pytest.raises(Format02SpineError) as category:
        proof(category_identity="SHORT_FORM_EDITED_VIDEO")
    assert category.value.code == "FORMAT02_CATEGORY_MISMATCH"

    with pytest.raises(Format02SpineError) as requirements:
        proof(character_performance_requirements=("only-one",))
    assert requirements.value.code == "THIRTEEN_CHARACTER_REQUIREMENTS_REQUIRED"

    with pytest.raises(Format02SpineError) as step:
        proof(executed_steps=REQUIRED_STEPS[:-1])
    assert step.value.code == "SPINE_STEP_MISSING"

    with pytest.raises(Format02SpineError) as cert:
        proof(certified=True)
    assert cert.value.code == "FORMAT02_CERTIFICATION_PROHIBITED"
