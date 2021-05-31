import pytest

from magic_tiler.utils import configs
from magic_tiler.utils import dtos
from magic_tiler.utils import tree
from tests import fakes

example_trees = []
single_node = tree.TreeNode("A")
example_trees.append(single_node)
simple_tree = tree.TreeNode("horizontal")
tree.TreeNode(dtos.WindowDetails(command="hi", mark="hi"), parent=simple_tree)
tree.TreeNode(dtos.WindowDetails(command="bye", mark="bye"), parent=simple_tree)
example_trees.append(simple_tree)

toml_contents = """
[screen]
split = "horizontal"

[[screen.children]]
size = 25
split = "vertical"

[[screen.children.children]]
command = "alacritty --title medium-window -e sh -c 'cowsay $(fortune); zsh -i'"
size = 60
mark = "medium-window"

[[screen.children.children]]
command = "alacritty --title tiny-window -e sh -c 'neofetch; zsh'"
size = 40
mark = "tiny-window"

[[screen.children]]
command = "alacritty --title middle-panel -e sh -c 'kak ~/internet.txt'"
size = 50
mark = "middle-panel"

[[screen.children]]
command = "alacritty --title right-panel -e sh -c 'broot'"
size = 25
mark = "right-panel"
"""
expected_toml_dict = {
    "screen": {
        "children": [
            {
                "children": [
                    {
                        "size": 60,
                        "command": "alacritty --title medium-window -e sh "
                        + "-c 'cowsay $(fortune); zsh -i'",
                        "mark": "medium-window",
                    },
                    {
                        "size": 40,
                        "command": "alacritty --title tiny-window -e sh -c 'neofetch; zsh'",
                        "mark": "tiny-window",
                    },
                ],
                "split": "vertical",
                "size": 25,
            },
            {
                "size": 50,
                "command": "alacritty --title middle-panel -e sh -c 'kak ~/internet.txt'",
                "mark": "middle-panel",
            },
            {
                "size": 25,
                "command": "alacritty --title right-panel -e sh -c 'broot'",
                "mark": "right-panel",
            },
        ],
        "split": "horizontal",
    }
}


def test_toml_reading():
    config_reader = configs.TomlConfig(
        fakes.FakeFilestore(files={"any": toml_contents}), dtos.Env("", "")
    )
    assert config_reader.to_dict() == expected_toml_dict


def test_reader_uses_xdg_config_first():
    base_dir = "/home/abc/.config"
    filestore = fakes.FakeFilestore(
        {
            base_dir + "/magic_tiler/config.toml": toml_contents,
            "abc": "def",
            "hjk": "lmno",
        }
    )
    env = dtos.Env(home="/home/magic", xdg_config_home=base_dir)
    config = configs.TomlConfig(filestore, env)
    assert config.to_dict() == expected_toml_dict


def test_reader_uses_home_dir_if_no_xdg():
    home_dir = "/home/def"
    filestore = fakes.FakeFilestore({home_dir + "/.magic_tiler.toml": toml_contents})
    env = dtos.Env(home=home_dir, xdg_config_home="")
    config = configs.TomlConfig(filestore, env)
    assert config.to_dict() == expected_toml_dict


def test_throws_error_if_cant_find_config_in_home():
    home_dir = "/home/def"
    filestore = fakes.FakeFilestore(dict())
    env = dtos.Env(home=home_dir, xdg_config_home="")
    with pytest.raises(RuntimeError):
        configs.TomlConfig(filestore, env)
