import abc
from typing import Dict


class TilingWindowManager(object):
    @abc.abstractmethod
    def make_window(self, command: str) -> None:
        pass

    @abc.abstractmethod
    def make_horizontal_sibling(self, window_title_regex: str, command: str) -> None:
        pass

    @abc.abstractmethod
    def make_vertical_sibling(self, window_title_regex: str, command: str) -> None:
        pass

    @abc.abstractmethod
    def resize_width(self, window_title_regex: str, container_percentage: int) -> None:
        pass

    @abc.abstractmethod
    def resize_height(self, window_title_regex: str, container_percentage: int) -> None:
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
    @abc.abstractmethod
    def to_dict(self) -> Dict:
        pass
