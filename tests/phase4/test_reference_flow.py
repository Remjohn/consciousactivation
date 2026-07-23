from _support import *
from conscious_activations_interview_expression.demo import run_demo

def test_deterministic_reference_flow(tmp_path):
 result=run_demo(tmp_path/'demo.sqlite3')
 assert result['source_package']['payload']['derivative_eligible'] is True
 assert result['health']['integrity']=='ok'
 assert result['production_authorized'] is False
 assert result['format02_activated'] is False

def test_schema_export(tmp_path):
 from conscious_activations_interview_expression.schema_export import export_schemas
 files=export_schemas(tmp_path/'schemas')
 assert len(files)==13
