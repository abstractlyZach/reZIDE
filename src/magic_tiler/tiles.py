import math
from typing import NamedTuple

from magic_tiler import interfaces
from magic_tiler import windows


class ScreenDimensions(NamedTuple):
    width: int
    height: int


class Tile(NamedTuple):
    """A class that represents the area covered by a window and its gaps.

    If you combine all tiles in a layout, it should cover the entire screen
    (excluding the status bar???)

    A tile's main job is to store a Window class and the dimensions of the tile
    """

    width: int
    height: int
    window: windows.Window


class TileFactory(object):
    def __init__(self, screen_dimensions: ScreenDimensions) -> None:
        self._screen_dimensions = screen_dimensions

    def make_tile(
        self,
        relative_width: float,
        relative_height: float,
        window_details: interfaces.WindowDetails,
    ) -> Tile:
        # calculate the pixel width and height of the window and tile
        absolute_width = math.floor(relative_width * self._screen_dimensions.width)
        absolute_height = math.floor(relative_height * self._screen_dimensions.height)
        window = windows.Window(
            command=window_details.command,
            width=absolute_width,
            height=absolute_height,
            mark=window_details.mark,
        )
        return Tile(width=absolute_width, height=absolute_height, window=window)
