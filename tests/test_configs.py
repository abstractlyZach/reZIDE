import pytest

from rezide.utils import configs
from rezide.utils import dtos
from tests import fakes

toml_contents = """
[screen]
split = "horizontal"
children = ['left', 'middle', 'right']
sizes = [25, 50, 25]

[left]
split = "vertical"
children = ['medium window', 'tiny window']
sizes = [60, 40]

['medium window']
command = "alacritty --title medium-window -e sh -c 'cowsay $(fortune); zsh -i'"
mark = "medium-window"

['tiny window']
command = "alacritty --title tiny-window -e sh -c 'neofetch; zsh'"
mark = "tiny-window"

[middle]
command = "alacritty --title middle-panel -e sh -c 'kak ~/internet.txt'"
mark = "middle-panel"

[right]
command = "alacritty --title right-panel -e sh -c 'broot'"
mark = "right-panel"
"""

expected_toml_dict = {
    "screen": {
        "children": ["left", "middle", "right"],
        "split": "horizontal",
        "sizes": [25, 50, 25],
    },
    "left": {
        "children": ["medium window", "tiny window"],
        "split": "vertical",
        "sizes": [60, 40],
    },
    "tiny window": {
        "command": "alacritty --title tiny-window -e sh -c 'neofetch; zsh'",
        "mark": "tiny-window",
    },
    "medium window": {
        "command": "alacritty --title medium-window -e sh -c 'cowsay $(fortune); zsh -i'",
        "mark": "medium-window",
    },
    "middle": {
        "command": "alacritty --title middle-panel -e sh -c 'kak ~/internet.txt'",
        "mark": "middle-panel",
    },
    "right": {
        "command": "alacritty --title right-panel -e sh -c 'broot'",
        "mark": "right-panel",
    },
}


def test_toml_reading():
    config_reader = configs.TomlReader(
        # ignore the env logic by using the "any" feature of our Fake :)
        fakes.FakeFilestore(files={"any": toml_contents}),
        dtos.Env(home="/home/myhomedir", xdg_config_home="/xdg"),
    )
    assert config_reader.read() == expected_toml_dict


def test_reader_uses_xdg_config_first():
    config_dir = "/home/abc/.config"
    filestore = fakes.FakeFilestore(
        {
            config_dir + "/rezide/config.toml": toml_contents,
            "abc": "def",
            "hjk": "lmno",
        }
    )
    env = dtos.Env(home="/home/magic", xdg_config_home=config_dir)
    config = configs.TomlReader(filestore, env)
    assert config.read() == expected_toml_dict


def test_reader_uses_home_dir_if_no_xdg():
    home_dir = "/home/def"
    filestore = fakes.FakeFilestore({home_dir + "/.rezide.toml": toml_contents})
    env = dtos.Env(home=home_dir, xdg_config_home="")
    config = configs.TomlReader(filestore, env)
    assert config.read() == expected_toml_dict


# TODO: add test to make sure that we check both paths even if xdg is defined


def test_throws_error_if_cant_find_config_in_home():
    filestore = fakes.FakeFilestore(dict())
    env = dtos.Env(home="/home/jkl", xdg_config_home="")
    with pytest.raises(RuntimeError):
        configs.TomlReader(filestore, env)


def test_throws_error_if_cant_find_config_anywhere():
    """Both xdg and home don't have the config"""
    filestore = fakes.FakeFilestore(dict())
    env = dtos.Env(home="/home/abc", xdg_config_home="/home/abc/.config")
    with pytest.raises(RuntimeError):
        configs.TomlReader(filestore, env)
