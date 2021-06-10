from typing import Dict, List, NamedTuple, Optional

from magic_tiler.utils import dtos
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


class FakeRect(NamedTuple):
    x: int
    y: int
    width: int
    height: int


class FakeNode(NamedTuple):
    name: str
    rect: FakeRect
    gaps: Optional[str]
    marks: List


class FakeWindowManager(interfaces.TilingWindowManager):
    def __init__(self, tree: Optional[List[FakeNode]] = None):
        if tree:
            self._tree = tree

    def make_window(self, window_details: dtos.WindowDetails) -> None:
        pass

    def resize_width(
        self, target_window: dtos.WindowDetails, container_percentage: int
    ) -> None:
        pass

    def resize_height(
        self, target_window: dtos.WindowDetails, container_percentage: int
    ) -> None:
        pass

    def focus(self, target_window: dtos.WindowDetails) -> None:
        pass

    def split(self, split_type: str) -> None:
        pass

    @property
    def num_workspace_windows(self) -> int:
        """Count the windows on the current workspace"""
        pass

    def get_tree(self) -> List[FakeNode]:
        return self._tree
