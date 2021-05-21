import math
from typing import NamedTuple

from magic_tiler import interfaces


class ScreenDimensions(NamedTuple):
    width: int
    height: int


class TileFactory(interfaces.TileFactoryInterface):
    def __init__(self, screen_dimensions: ScreenDimensions) -> None:
        self._screen_dimensions = screen_dimensions

    def make_tile(
        self,
        relative_width: float,
        relative_height: float,
        window_details: interfaces.WindowDetails,
    ) -> interfaces.Tile:
        # calculate the pixel width and height of the window and tile
        absolute_width = math.floor(relative_width * self._screen_dimensions.width)
        absolute_height = math.floor(relative_height * self._screen_dimensions.height)
        window = interfaces.Window(
            command=window_details.command,
            width=absolute_width,
            height=absolute_height,
            mark=window_details.mark,
        )
        return interfaces.Tile(
            width=absolute_width, height=absolute_height, window=window
        )
