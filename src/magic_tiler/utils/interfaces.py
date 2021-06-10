import abc
from typing import Dict, List

from magic_tiler.utils import dtos
from magic_tiler.utils import tree


class TilingWindowManager(object):
    @abc.abstractmethod
    def make_window(self, window_details: dtos.WindowDetails) -> None:
        pass

    @abc.abstractmethod
    def resize_width(
        self, target_window: dtos.WindowDetails, container_percentage: int
    ) -> None:
        pass

    @abc.abstractmethod
    def resize_height(
        self, target_window: dtos.WindowDetails, container_percentage: int
    ) -> None:
        pass

    @abc.abstractmethod
    def focus(self, target_window: dtos.WindowDetails) -> None:
        pass

    @abc.abstractmethod
    def split(self, split_type: str) -> None:
        pass

    @property
    @abc.abstractmethod
    def num_workspace_windows(self) -> int:
        """Count the windows on the current workspace"""
        pass

    @abc.abstractmethod
    def get_tree(self) -> List:
        pass


class ConfigReader(object):
    @abc.abstractmethod
    def to_dict(self) -> Dict:
        pass


class TileFactoryInterface(object):
    @abc.abstractmethod
    def make_tile(
        self,
        relative_width: float,
        relative_height: float,
        window_details: dtos.WindowDetails,
    ) -> dtos.Tile:
        pass


class FileStore(object):
    """Any system that could store files, like a local filesystem"""

    @abc.abstractmethod
    def path_exists(self, path: str) -> bool:
        pass

    @abc.abstractmethod
    def read_file(self, path: str) -> str:
        pass


class TreeFactoryInterface(object):
    def build_tree(self, root_node: Dict) -> tree.TreeNode:
        pass
