from typing import List, NamedTuple

import pytest

from magic_tiler import interfaces
from magic_tiler import tiles
from magic_tiler import windows


class TileTestCase(NamedTuple):
    screen_dimensions: tiles.ScreenDimensions
    expected_tile: interfaces.Tile
    tile_args: List


tile_test_cases: List[TileTestCase] = [
    TileTestCase(
        screen_dimensions=tiles.ScreenDimensions(100, 100),
        tile_args=[0.2, 0.5, interfaces.WindowDetails(command="echo hi", mark="hi")],
        expected_tile=interfaces.Tile(
            width=20,
            height=50,
            window=windows.Window(command="echo hi", width=20, height=50, mark="hi"),
        ),
    ),
    TileTestCase(
        screen_dimensions=tiles.ScreenDimensions(100, 100),
        tile_args=[
            0.33,
            0.66,
            interfaces.WindowDetails(command="echo bye", mark="bye"),
        ],
        expected_tile=interfaces.Tile(
            width=33,
            height=66,
            window=windows.Window(command="echo bye", width=33, height=66, mark="bye"),
        ),
    ),
    TileTestCase(
        screen_dimensions=tiles.ScreenDimensions(1000, 1000),
        tile_args=[
            0.33,
            0.554,
            interfaces.WindowDetails(command="cowsay moo", mark="moo"),
        ],
        expected_tile=interfaces.Tile(
            width=330,
            height=554,
            window=windows.Window(
                command="cowsay moo", width=330, height=554, mark="moo"
            ),
        ),
    ),
]


@pytest.mark.parametrize("test_case", tile_test_cases)
def test_tile_factory_no_gap(test_case):
    factory = tiles.TileFactory(test_case.screen_dimensions)
    tile = factory.make_tile(*test_case.tile_args)
    assert tile == test_case.expected_tile
