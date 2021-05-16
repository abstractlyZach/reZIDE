import abc


class TilingWindowManager(object):
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
