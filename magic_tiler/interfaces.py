import abc

class TilingWindowManager(class):
    @abc.abstractmethod
    def make_horizontal_sibling(window_title_regex:str, command) -> None:
        pass

    @abc.abstractmethod
    def make_vertical_sibling(window_title_regex:str, command) -> None:
        pass

    @abc.abstractmethod
    def resize_width(window_title_regex:str, container_percentage:int) -> None:
        pass

    @abc.abstractmethod
    def resize_height(window_title_regex:str, container_percentage:int) -> None:
        pass
