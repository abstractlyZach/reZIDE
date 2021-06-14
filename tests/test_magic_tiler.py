from typing import Dict, List, NamedTuple
from unittest import mock

import pytest

from magic_tiler import magic_tiler
from magic_tiler.utils import dtos


@pytest.fixture
def MockWindowManager(mocker):
    return mocker.patch("magic_tiler.utils.sway.Sway")


@pytest.fixture
def MockMagicTiler(mocker):
    return mocker.patch("magic_tiler.magic_tiler.MagicTiler")


@pytest.fixture
def MockConfig(mocker):
    return mocker.patch("magic_tiler.utils.configs.TomlConfig")


@pytest.fixture
def MockLayout(mocker):
    return mocker.patch("magic_tiler.utils.layouts.Layout")


# how do we even run an end-to-end test?? a sandboxed vm that runs a window manager?
@pytest.mark.skip
@pytest.mark.e2e
def test_magic_tiler_script(click_runner):
    result = click_runner.invoke(magic_tiler.main)
    assert result.exit_code == 0


class ClickTestParams(NamedTuple):
    """Store test parameters in a nice namedtuple"""

    cli_args: List[str]
    shell_env: Dict
    expected_parsed_env: dtos.Env
    expected_verbosity: int


test_params = [
    ClickTestParams(
        cli_args=["my_ide"],
        shell_env={"HOME": "abc", "XDG_CONFIG_HOME": "def"},
        expected_parsed_env=dtos.Env(home="abc", xdg_config_home="def"),
        expected_verbosity=0,
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
        expected_parsed_env=dtos.Env(
            home="different_home", xdg_config_home="different_xdg"
        ),
        expected_verbosity=0,
    ),
    ClickTestParams(
        cli_args=["test_ide", "-v"],
        shell_env={"HOME": "abc", "XDG_CONFIG_HOME": "def"},
        expected_parsed_env=dtos.Env(home="abc", xdg_config_home="def"),
        expected_verbosity=1,
    ),
    ClickTestParams(
        cli_args=["super-verbose", "-vv"],
        shell_env={"HOME": "abc", "XDG_CONFIG_HOME": "def"},
        expected_parsed_env=dtos.Env(home="abc", xdg_config_home="def"),
        expected_verbosity=2,
    ),
]


# I don't like mocking so many things, but I'm not sure how to do DI
# when we're using Click
@pytest.mark.parametrize("test_parameters", test_params)
def test_successful_script(
    click_runner,
    MockWindowManager,
    MockMagicTiler,
    MockConfig,
    MockLayout,
    test_parameters,
):
    """Verify that we're setting up dependencies and calling MagicTiler correctly"""
    result = click_runner.invoke(
        magic_tiler.main, test_parameters.cli_args, env=test_parameters.shell_env
    )
    assert result.exit_code == 0, result.exception
    assert "" == result.output, result.exception
    MockMagicTiler.assert_called_once_with(
        test_parameters.expected_parsed_env,
        MockLayout(),
        test_parameters.expected_verbosity,
    )
    MockMagicTiler.return_value.run.assert_called_once_with(test_parameters.cli_args[0])


def test_run():
    env = dtos.Env(home="abc", xdg_config_home="def")
    layout = mock.MagicMock()
    application = magic_tiler.MagicTiler(env, layout, 0)
    application.run("my_ide")
    layout.spawn_windows.assert_called_once_with("my_ide")
