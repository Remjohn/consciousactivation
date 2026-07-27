from pathlib import Path

from tests.stories.st_03_01 import build_context, open_command


ROOT = Path(__file__).resolve().parents[3]


class FailOnceSink:
    def __init__(self):
        self.failed = False
        self.observations = []

    def emit(self, observation):
        if not self.failed:
            self.failed = True
            raise RuntimeError("injected sink failure")
        self.observations.append(observation)


def test_success_emits_graph_and_question_observations():
    service, repository, sink, run_id = build_context()
    service.open(open_command(repository, run_id))
    names = {item.event_name for item in sink.observations if item.story_id == "ST-03.01"}
    assert names == {"ST-03.01:QuestionPackageCompiled", "ST-03.01:OutcomeVerified"}
    assert all(item.authority_identity == "code-1" for item in sink.observations if item.story_id == "ST-03.01")


def test_story_source_has_no_external_runtime_or_product_imports():
    paths = (
        ROOT / "src/cmf_builder/domain/genesis_questions.py",
        ROOT / "src/cmf_builder/application/genesis_question_commands.py",
    )
    forbidden = ("requests", "httpx", "boto", "delegation", "visual_asset_editor", "comfyui", "gpu")
    text = "\n".join(path.read_text(encoding="utf-8").lower() for path in paths)
    assert all(token not in text for token in forbidden)


def test_package_is_synthetic_nonproduction_and_noncertified():
    service, repository, _, run_id = build_context()
    receipt = service.open(open_command(repository, run_id))
    package = repository.get_genesis_question_package(receipt.package_id)
    assert package.production_eligible is False
    assert package.certified is False


def test_committed_observation_outbox_retries_without_false_uncommitted_result():
    sink = FailOnceSink()
    service, repository, _, run_id = build_context(genesis_observations=sink)
    command = open_command(repository, run_id)
    receipt = service.open(command)
    assert receipt.outcome == "PASS"
    assert len(repository.pending_observations(command.command_id)) == 2
    assert service.open(command) == receipt
    assert repository.pending_observations(command.command_id) == ()
    assert {item.event_name for item in sink.observations} >= {
        "ST-03.01:QuestionPackageCompiled",
        "ST-03.01:OutcomeVerified",
        "ST-03.01:QuestionPackageReplayReturned",
    }
