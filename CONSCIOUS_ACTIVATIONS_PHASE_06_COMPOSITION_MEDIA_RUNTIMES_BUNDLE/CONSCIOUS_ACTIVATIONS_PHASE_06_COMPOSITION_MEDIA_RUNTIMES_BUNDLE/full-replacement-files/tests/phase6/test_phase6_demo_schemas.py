from pathlib import Path
from cmf_pipeline.phase6_demo import run_phase6_demo
from cmf_pipeline.schema_export import export_schemas

def test_phase6_demo(tmp_path):
 result=run_phase6_demo(tmp_path/'db.sqlite3',tmp_path/'artifacts');assert result['claim_ceiling']=='PHASE_06_COMPOSITION_MEDIA_RUNTIME_DEVELOPMENT_EVIDENCE';assert any(x.endswith('.mp4') for x in result['output_files']);assert any(x.endswith('.png') for x in result['output_files']);assert result['video_evaluation']['verdict'].startswith('PASS')
def test_schema_export_contains_phase6(tmp_path):
 result=export_schemas(tmp_path/'schemas');assert result['file_count']>=31;assert (tmp_path/'schemas/video_edit_program.schema.json').is_file();assert (tmp_path/'schemas/composition_ir.schema.json').is_file()
