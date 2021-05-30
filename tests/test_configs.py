from typing import Dict, List

from magic_tiler.utils import configs
from magic_tiler.utils import interfaces
from magic_tiler.utils import tree


class FakeFilestore(interfaces.FileStore):
    def __init__(self, exists: List[str], file_contents: str = ""):
        self._existing_paths = exists
        self._file_contents = file_contents

    def path_exists(self, path: str) -> bool:
        return path in self._existing_paths

    def read_file(self, path: str) -> str:
        return self._file_contents


class FakeTreeFactory(interfaces.TreeFactoryInterface):
    def build_tree(self, root_node: Dict) -> tree.TreeNode:
        return tree.TreeNode("a")


def test_toml():
    config_reader = configs.TomlConfig("examples/centered_big.toml")
    assert config_reader.to_dict() == {
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


def test_config_uses_xdg_base_first():
    base_dir = "/home/abc/.config"
    filestore = FakeFilestore(exists=[base_dir + "magic_tiler/config"])
    tree_factory = FakeTreeFactory()
    config = configs.Config(filestore, tree_factory, xdg_base_dir=base_dir)
    assert config.tree == tree.TreeNode("a")
