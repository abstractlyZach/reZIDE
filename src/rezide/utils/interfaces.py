# https://stackoverflow.com/questions/36286894/name-not-defined-in-type-annotation
from __future__ import annotations

import abc
from typing import Any, Dict, List

from rezide.utils import dtos


class TilingWindowManager(object):
    @abc.abstractmethod
    def make_window(self, window_details: dtos.WindowDetails) -> None:
        pass

    @abc.abstractmethod
    def resize_width(
        self, target_window: dtos.WindowDetails, section_percentage: int
    ) -> None:
        pass

    @abc.abstractmethod
    def resize_height(
        self, target_window: dtos.WindowDetails, section_percentage: int
    ) -> None:
        pass

    @abc.abstractmethod
    def focus(self, target_window: dtos.WindowDetails) -> None:
        pass

    @abc.abstractmethod
    def split_and_mark_parent(self, split_type: str, mark: str) -> None:
        pass

    @property
    @abc.abstractmethod
    def num_workspace_windows(self) -> int:
        """Count the windows on the current workspace"""
        pass

    @abc.abstractmethod
    def get_tree(self) -> List:
        pass

    @abc.abstractmethod
    def get_window_sizes(self) -> Dict:
        pass


class ConfigReader(object):
    @abc.abstractmethod
    def read(self) -> Dict:
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


class TreeNodeInterface(object):
    @abc.abstractmethod
    def add_child(self, node: TreeNodeInterface) -> None:
        pass

    @abc.abstractmethod
    def get_leftmost_descendant(self) -> TreeNodeInterface:
        pass

    @property
    @abc.abstractmethod
    def is_parent(self) -> bool:
        pass

    @property
    @abc.abstractmethod
    def children(self) -> List[TreeNodeInterface]:
        pass

    @property
    @abc.abstractmethod
    def data(self) -> Any:
        pass


class TreeFactoryInterface(object):
    @abc.abstractmethod
    def create_tree(self, root_node: Dict) -> TreeNodeInterface:
        pass


class ConfigParserInterface(object):
    @abc.abstractmethod
    def validate(self) -> None:
        pass

    @abc.abstractmethod
    def get_tree(self, layout_name: str) -> TreeNodeInterface:
        pass
