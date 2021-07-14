from typing import List, NamedTuple

import pytest

from rezide.utils import dtos
from rezide.utils import tiles


class TileTestCase(NamedTuple):
    screen_dimensions: dtos.ScreenDimensions
    expected_tile: dtos.Tile
    tile_args: List


tile_test_cases: List[TileTestCase] = [
    TileTestCase(
        screen_dimensions=dtos.ScreenDimensions(100, 100),
        tile_args=[0.2, 0.5, dtos.WindowDetails(command="echo hi", mark="hi")],
        expected_tile=dtos.Tile(
            width=20,
            height=50,
            window=dtos.Window(command="echo hi", width=20, height=50, mark="hi"),
        ),
    ),
    TileTestCase(
        screen_dimensions=dtos.ScreenDimensions(100, 100),
        tile_args=[
            0.33,
            0.66,
            dtos.WindowDetails(command="echo bye", mark="bye"),
        ],
        expected_tile=dtos.Tile(
            width=33,
            height=66,
            window=dtos.Window(command="echo bye", width=33, height=66, mark="bye"),
        ),
    ),
    TileTestCase(
        screen_dimensions=dtos.ScreenDimensions(1000, 1000),
        tile_args=[
            0.33,
            0.554,
            dtos.WindowDetails(command="cowsay moo", mark="moo"),
        ],
        expected_tile=dtos.Tile(
            width=330,
            height=554,
            window=dtos.Window(command="cowsay moo", width=330, height=554, mark="moo"),
        ),
    ),
]


@pytest.mark.parametrize("test_case", tile_test_cases)
def test_tile_factory_no_gap(test_case):
    factory = tiles.TileFactory(test_case.screen_dimensions)
    tile = factory.make_tile(*test_case.tile_args)
    assert tile == test_case.expected_tile
