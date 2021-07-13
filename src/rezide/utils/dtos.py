from typing import Any, NamedTuple

# data-transfer objects (DTOs)
# objects that don't have much functionality besides storing
# useful collections of information


class ScreenDimensions(NamedTuple):
    width: int
    height: int


class Window(NamedTuple):
    command: str
    width: int
    height: int
    mark: str


class WindowDetails(NamedTuple):
    mark: str
    command: str


# todo: remove tiles now that we don't use them anymore
class Tile(NamedTuple):
    """A class that represents the area covered by a window and its gaps.

    If you combine all tiles in a layout, it should cover the entire screen
    (excluding the status bar???)

    A tile's main job is to store a Window class and the dimensions of the tile
    """

    width: int
    height: int
    window: Window


class Env(NamedTuple):
    """Environment variables"""

    home: str
    xdg_config_home: str


class WindowManagerCall(NamedTuple):
    """Used for verifying calls to a window manager"""

    command: str
    arg: Any
