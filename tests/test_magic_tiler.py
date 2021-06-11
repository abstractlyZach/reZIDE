import pytest

from magic_tiler import magic_tiler
from magic_tiler.utils import dtos
from tests import fakes


@pytest.fixture
def mock_window_manager(mocker):
    return mocker.patch("magic_tiler.utils.sway.Sway")


@pytest.fixture
def mock_run_magic_tiler(mocker):
    mock = mocker.patch("magic_tiler.magic_tiler.run_magic_tiler")
    return mock


@pytest.fixture
def mock_config(mocker):
    mock = mocker.patch("magic_tiler.utils.configs.TomlConfig")
    return mock


@pytest.fixture
def mock_layout(mocker):
    mock = mocker.patch("magic_tiler.utils.layout.Layout")
    return mock


# how do we even run an end-to-end test?? a sandboxed vm that runs a window manager?
@pytest.mark.e2e
@pytest.mark.skip
def test_magic_tiler_script(click_runner):
    result = click_runner.invoke(magic_tiler.main)
    assert result.exit_code == 0


def test_click_handles_options(
    click_runner, mock_window_manager, mock_run_magic_tiler, mock_config
):
    fake_config = fakes.FakeConfig({"my_ide": {}})
    mock_config.return_value = fake_config
    expected_env = dtos.Env(home="abc", xdg_config_home="def")
    result = click_runner.invoke(
        magic_tiler.main, ["my_ide"], env={"HOME": "abc", "XDG_CONFIG_HOME": "def"}
    )
    assert result.exit_code == 0, result.exception
    assert "" == result.output, result.exception
    mock_run_magic_tiler.assert_called_once_with(
        expected_env, mock_window_manager(), "my_ide", fake_config
    )


def test_can_override_env_variables(
    click_runner, mock_window_manager, mock_run_magic_tiler, mock_config
):
    expected_env = dtos.Env(home="different_home", xdg_config_home="different_xdg")
    result = click_runner.invoke(
        magic_tiler.main,
        [
            "my_ide",
            "--user-home-dir",
            "different_home",
            "--xdg-config-home-dir",
            "different_xdg",
        ],
        env={"HOME": "abc", "XDG_CONFIG_HOME": "def"},
    )
    assert result.exit_code == 0, result.exception
    assert "" == result.output, result.exception
    mock_run_magic_tiler.assert_called_once_with(
        expected_env, mock_window_manager(), "my_ide", mock_config()
    )


def test_fails_if_too_many_windows_open():
    window_manager = fakes.FakeWindowManager(num_workspace_windows=20)
    env = dtos.Env(home="abc", xdg_config_home="def")
    with pytest.raises(RuntimeError):
        magic_tiler.run_magic_tiler(env, window_manager, "my_ide", fakes.FakeConfig({}))


def test_happy_path(mock_layout):
    window_manager = fakes.FakeWindowManager()
    config = fakes.FakeConfig({})
    env = dtos.Env(home="abc", xdg_config_home="def")
    magic_tiler.run_magic_tiler(env, window_manager, "my_ide", config)
    mock_layout.assert_called_once_with(config, "my_ide", window_manager)
