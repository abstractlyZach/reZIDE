from typing import Dict, Optional

import toml

from magic_tiler.utils import interfaces
from magic_tiler.utils import tree


class TomlConfig(interfaces.ConfigReader):
    def __init__(self, filename: str) -> None:
        with open(filename, "r") as infile:
            self._dict = dict(toml.load(infile))

    def to_dict(self) -> Dict:
        return self._dict


class Config(object):
    def __init__(
        self,
        filestore: interfaces.FileStore,
        tree_factory: interfaces.TreeFactoryInterface,
        xdg_base_dir: Optional[str] = None,
    ) -> None:
        self._tree = tree.TreeNode("a")

    @property
    def tree(self) -> tree.TreeNode:
        return self._tree
