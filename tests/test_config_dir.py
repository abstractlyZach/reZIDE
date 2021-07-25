import pytest

from rezide.utils import config_dir
from rezide.utils import dtos
from tests import fakes


@pytest.fixture
def test_env():
    return dtos.Env(home="/home/test/", xdg_config_home="/home/test/.config/")


specified_dir_tests = [
    ({"/abc/alpha.toml": "", "/abc/beta.toml": ""}, {"alpha", "beta"}),
    ({"/abc/hello.toml": "", "/abc/world.toml": ""}, {"hello", "world"}),
]


@pytest.mark.parametrize("test_case", specified_dir_tests)
def test_lists_layouts_from_specified_dir(test_case, test_env):
    """If a dir is specified, give that highest priority"""
    filestore = fakes.FakeFilestore(test_case[0])
    dir = config_dir.ConfigDir(filestore, test_env, "/abc/")
    assert dir.list_layouts() == test_case[1]


@pytest.mark.parametrize("test_case", specified_dir_tests)
def test_throws_error_if_specified_dir_doesnt_exist(test_case, test_env):
    """If the specified dir doesn't exist, throw an error"""
    filestore = fakes.FakeFilestore(test_case[0])
    with pytest.raises(RuntimeError):
        config_dir.ConfigDir(filestore, test_env, "/woopsies/")


xdg_dir_tests = [
    (
        {
            "/home/test/.config/rezide/alpha.toml": "",
            "/home/test/.config/rezide/beta.toml": "",
        },
        {"alpha", "beta"},
    ),
    (
        {
            "/home/test/.config/rezide/hello.toml": "",
            "/home/test/.config/rezide/world.toml": "",
        },
        {"hello", "world"},
    ),
]


@pytest.mark.parametrize("test_case", xdg_dir_tests)
def test_lists_layouts_from_xdg_config_home(test_case, test_env):
    """Look in $XDG_CONFIG_HOME first if there's no specified dir"""
    filestore = fakes.FakeFilestore(test_case[0])
    dir = config_dir.ConfigDir(filestore, test_env)
    assert dir.list_layouts() == test_case[1]


home_dir_tests = [
    (
        {"/home/test/.rezide/alpha.toml": "", "/home/test/.rezide/beta.toml": ""},
        {"alpha", "beta"},
    ),
    (
        {"/home/test/.rezide/hello.toml": "", "/home/test/.rezide/world.toml": ""},
        {"hello", "world"},
    ),
]


@pytest.mark.parametrize("test_case", home_dir_tests)
def test_lists_layouts_from_home_when_xdg_config_dir_is_empty(test_case, test_env):
    """Fall back on $HOME/.rezide/ if there's no config dir path specified and
    $XDG_CONFIG_HOME is empty
    """
    filestore = fakes.FakeFilestore(test_case[0])
    env = dtos.Env(home="/home/test/", xdg_config_home="")
    dir = config_dir.ConfigDir(filestore, env)
    assert dir.list_layouts() == test_case[1]


@pytest.mark.parametrize("test_case", home_dir_tests)
def test_lists_layouts_from_home_when_xdg_config_dir_doesnt_exist(test_case, test_env):
    """Fall back on $HOME/.rezide/ if there's no config dir path specified and
    xdg_config_dir is specified, but doesn't exist
    """
    filestore = fakes.FakeFilestore(test_case[0])
    dir = config_dir.ConfigDir(filestore, test_env)
    assert dir.list_layouts() == test_case[1]


def test_throws_error_if_unspecified_and_env_vars_fail(test_env):
    """Throw an error if there is no specified dir and the directories in the environment
    variables are not valid
    """
    filestore = fakes.FakeFilestore(dict())
    with pytest.raises(RuntimeError):
        config_dir.ConfigDir(filestore, test_env)


layout_file_path_tests = [
    (
        {
            "/home/test/.config/rezide/alpha.toml": "",
            "/home/test/.config/rezide/beta.toml": "",
        },
        "alpha",
        "/home/test/.config/rezide/alpha.toml",
    ),
    (
        {
            "/home/test/.config/rezide/alpha.toml": "",
            "/home/test/.config/rezide/beta.toml": "",
        },
        "beta",
        "/home/test/.config/rezide/beta.toml",
    ),
    (
        {
            "/home/test/.rezide/yay.toml": "",
        },
        "yay",
        "/home/test/.rezide/yay.toml",
    ),
]


@pytest.mark.parametrize("test_case", layout_file_path_tests)
def test_get_layout_file_path(test_case, test_env):
    """Convert layout names into absolute paths within the config dir"""
    filestore = fakes.FakeFilestore(test_case[0])
    dir = config_dir.ConfigDir(filestore, test_env)
    assert dir.get_layout_file_path(test_case[1]) == test_case[2]


def test_cant_find_layout(test_env):
    """Raise an error if the layout can't be found in the config dir"""
    filestore = fakes.FakeFilestore({"/home/test/.config/rezide/abc.toml": ""})
    dir = config_dir.ConfigDir(filestore, test_env)
    with pytest.raises(RuntimeError):
        dir.get_layout_file_path("def")
