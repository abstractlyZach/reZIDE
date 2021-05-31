from typing import Dict

from magic_tiler.utils import interfaces
from magic_tiler.utils import tree


class FakeFilestore(interfaces.FileStore):
    def __init__(self, files: Dict[str, str]):
        """Add a key called "any" when you don't care about the specific file path
        and just want the file to exist with contents for all inputs
        """
        self._files = files

    def path_exists(self, path: str) -> bool:
        if "any" in self._files:
            return True
        return path in self._files

    def read_file(self, path: str) -> str:
        if "any" in self._files:
            return self._files["any"]
        return self._files[path]


class FakeTreeFactory(interfaces.TreeFactoryInterface):
    def __init__(self, tree_root: tree.TreeNode):
        self._tree = tree_root

    def build_tree(self, root_node: Dict) -> tree.TreeNode:
        return self._tree


class FakeConfig(interfaces.ConfigReader):
    def __init__(self, config_dict: Dict) -> None:
        self._config_dict = config_dict

    def to_dict(self) -> Dict:
        return self._config_dict
