import pytest

from cmf_builder.application.operator_shell import OutputMode, ShellCommand, ShellError, execute_shell_request, parse_shell_command, shell_help


def test_shell_parses_supported_commands_with_stable_identity_and_modes():
    request = parse_shell_command("run inspect run-001 --json", operator_identity="operator:dev", authority_identity="authority:od-am-005")
    repeat = parse_shell_command("run inspect run-001 --json", operator_identity="operator:dev", authority_identity="authority:od-am-005")

    assert request.command is ShellCommand.RUN_INSPECT
    assert request.subject == "run-001"
    assert request.output_mode is OutputMode.MACHINE
    assert request.command_identity == repeat.command_identity


def test_shell_help_is_accessible_and_deterministic():
    help_payload = shell_help()

    assert "no_color_required" in help_payload["accessibility"]
    assert help_payload["commands"] == sorted(help_payload["commands"], key=lambda item: item["command"])
    assert help_payload["production_ready"] is False
    assert help_payload["certified"] is False


def test_shell_rejects_missing_authority_subject_absolute_paths_and_unknown_commands():
    with pytest.raises(ShellError) as authority:
        parse_shell_command("run list", operator_identity="", authority_identity="authority:od-am-005")
    assert authority.value.code == "SHELL_AUTHORITY_REQUIRED"

    with pytest.raises(ShellError) as subject:
        parse_shell_command("run inspect", operator_identity="operator:dev", authority_identity="authority:od-am-005")
    assert subject.value.code == "SHELL_SUBJECT_REQUIRED"

    with pytest.raises(ShellError) as path:
        parse_shell_command("receipt export C:/secret", operator_identity="operator:dev", authority_identity="authority:od-am-005")
    assert path.value.code == "PORTABLE_PATH_REQUIRED"

    with pytest.raises(ShellError) as unknown:
        parse_shell_command("mutate prod", operator_identity="operator:dev", authority_identity="authority:od-am-005")
    assert unknown.value.code == "UNKNOWN_SHELL_COMMAND"


def test_shell_outputs_structured_rejections_without_secret_leakage_or_mutation():
    request = parse_shell_command("evidence export bundle-001 --human", operator_identity="operator:dev", authority_identity="authority:od-am-005")

    response = execute_shell_request(request, {"safe": True})
    assert response.exit_code == 0
    assert response.output_mode is OutputMode.HUMAN

    denied = execute_shell_request(request, {"safe": True}, authority_granted=False)
    assert denied.status == "REJECTED"
    assert denied.exit_code == 13

    secret = execute_shell_request(request, {"secret": "redacted"})
    assert secret.payload == {"reason": "SECRET_EXCLUDED"}

    hidden = execute_shell_request(request, {"hidden_mutation": True})
    assert hidden.payload == {"reason": "HIDDEN_MUTATION_REJECTED"}
