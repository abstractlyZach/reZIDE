import abc
from typing import Dict

from magic_tiler.utils import dtos


class TilingWindowManager(object):
    @abc.abstractmethod
    def make_window(self, window_details: dtos.WindowDetails) -> None:
        pass

    @abc.abstractmethod
    def make_horizontal_sibling(
        self, target_window: dtos.WindowDetails, new_window: dtos.WindowDetails
    ) -> None:
        pass

    @abc.abstractmethod
    def make_vertical_sibling(
        self, target_window: dtos.WindowDetails, new_window: dtos.WindowDetails
    ) -> None:
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

    @property
    @abc.abstractmethod
    def num_workspace_windows(self) -> int:
        """Count the windows on the current workspace"""
        pass


class Runner(object):
    @abc.abstractmethod
    def run_and_disown(self, command: str) -> None:
        """Run a command and don't wait for it to finish"""
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
