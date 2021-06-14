from typing import Dict, List, NamedTuple

import pytest

from magic_tiler import magic_tiler
from magic_tiler.utils import dtos
from tests import fakes


@pytest.fixture
def mock_window_manager(mocker):
    return mocker.patch("magic_tiler.utils.sway.Sway")


@pytest.fixture
def mock_run_magic_tiler(mocker):
    mock = mocker.patch("magic_tiler.magic_tiler.MagicTiler")
    return mock


@pytest.fixture
def mock_config(mocker):
    mock = mocker.patch("magic_tiler.utils.configs.TomlConfig")
    return mock


@pytest.fixture
def mock_layout(mocker):
    mock = mocker.patch("magic_tiler.utils.layouts.Layout")
    return mock


# how do we even run an end-to-end test?? a sandboxed vm that runs a window manager?
@pytest.mark.e2e
@pytest.mark.skip
def test_magic_tiler_script(click_runner):
    result = click_runner.invoke(magic_tiler.main)
    assert result.exit_code == 0


class ClickTestParams(NamedTuple):
    cli_args: List[str]
    shell_env: Dict
    expected_env: dtos.Env


test_params = [
    ClickTestParams(
        cli_args=["my_ide"],
        shell_env={"HOME": "abc", "XDG_CONFIG_HOME": "def"},
        expected_env=dtos.Env(home="abc", xdg_config_home="def"),
    ),
    # can we override CLI env variables?
    ClickTestParams(
        cli_args=[
            "my_ide",
            "--user-home-dir",
            "different_home",
            "--xdg-config-home-dir",
            "different_xdg",
        ],
        shell_env={"HOME": "abc", "XDG_CONFIG_HOME": "def"},
        expected_env=dtos.Env(home="different_home", xdg_config_home="different_xdg"),
    ),
]


# I don't like mocking so many things, but I'm not sure how to do DI
# when we're using Click
@pytest.mark.parametrize("test_parameters", test_params)
def test_successful_script(
    click_runner,
    mock_window_manager,
    mock_run_magic_tiler,
    mock_config,
    test_parameters,
):
    result = click_runner.invoke(
        magic_tiler.main, test_parameters.cli_args, env=test_parameters.shell_env
    )
    assert result.exit_code == 0, result.exception
    assert "" == result.output, result.exception
    mock_run_magic_tiler.assert_called_once_with(
        test_parameters.expected_env, mock_window_manager(), mock_config(), 0
    )
    mock_run_magic_tiler.return_value.run.assert_called_once_with("my_ide")


def test_fails_if_too_many_windows_open():
    window_manager = fakes.FakeWindowManager(num_workspace_windows=20)
    env = dtos.Env(home="abc", xdg_config_home="def")
    application = magic_tiler.MagicTiler(env, window_manager, fakes.FakeConfig({}), 0)
    with pytest.raises(RuntimeError):
        application.run("my_ide")


def test_happy_path(mock_layout):
    window_manager = fakes.FakeWindowManager()
    config = fakes.FakeConfig({})
    env = dtos.Env(home="abc", xdg_config_home="def")
    application = magic_tiler.MagicTiler(env, window_manager, config, 0)
    application.run("my_ide")
    mock_layout.assert_called_once_with(config, window_manager)
    mock_layout.return_value.spawn_windows.assert_called_once_with("my_ide")
