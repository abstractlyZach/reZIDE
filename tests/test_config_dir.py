import pytest

from rezide.utils import config_dir
from rezide.utils import dtos
from tests import fakes

specified_dir_tests = [
    ({"/abc/alpha.toml": "", "/abc/beta.toml": ""}, {"alpha", "beta"}),
    ({"/abc/hello.toml": "", "/abc/world.toml": ""}, {"hello", "world"}),
]


@pytest.mark.parametrize("test_case", specified_dir_tests)
def test_lists_layouts_from_specified_dir(test_case):
    filestore = fakes.FakeFilestore(test_case[0])
    env = dtos.Env(home="/home/test/", xdg_config_home="/home/test/.config/")
    dir = config_dir.ConfigDir(filestore, env, "/abc/")
    assert dir.list_layouts() == test_case[1]
