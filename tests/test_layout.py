from typing import Dict, List, NamedTuple

import pytest

from magic_tiler import dtos
from magic_tiler.utils import interfaces
from magic_tiler.utils import layout


class FakeConfig(interfaces.ConfigReader):
    def __init__(self, config_dict: Dict) -> None:
        self._config_dict = config_dict

    def to_dict(self) -> Dict:
        return self._config_dict


class MakeTileArgs(NamedTuple):
    """A DTO for testing call args to TileFactory.make_tile()"""

    relative_width: float
    relative_height: float
    window_details: dtos.WindowDetails


def make_dummy_tile() -> dtos.Tile:
    return dtos.Tile(
        height=0,
        width=0,
        window=dtos.Window(command="", width=0, height=0, mark=""),
    )


class SpyTileFactory(interfaces.TileFactoryInterface):
    """Gets passed into Layouts using dependency injection
    and spys on their calls so we can make sure that we're doing
    the tile math correctly
    """

    def __init__(self):
        self._calls: List[MakeTileArgs] = []

    def make_tile(
        self,
        relative_width: float,
        relative_height: float,
        window_details: dtos.WindowDetails,
    ) -> dtos.Tile:
        self._calls.append(
            MakeTileArgs(
                relative_width=relative_width,
                relative_height=relative_height,
                window_details=window_details,
            )
        )
        return make_dummy_tile()

    @property
    def calls(self):
        return self._calls


class LayoutTestCase(NamedTuple):
    config: Dict
    expected_call_args: List[MakeTileArgs]
    layout_name: str


layout_test_cases = [
    LayoutTestCase(
        config={
            "screen": {
                "children": [
                    {
                        "children": [
                            {
                                "mark": "medium",
                                "size": 60,
                                "command": "alacritty",
                            },
                            {
                                "mark": "small",
                                "size": 40,
                                "command": "alacritty",
                            },
                        ],
                        "split": "vertical",
                        "size": 25,
                    },
                    {
                        "mark": "big",
                        "size": 50,
                        "command": "alacritty",
                    },
                    {
                        "mark": "right",
                        "size": 25,
                        "command": "alacritty",
                    },
                ],
                "split": "horizontal",
            }
        },
        expected_call_args=[
            MakeTileArgs(
                relative_height=1.0,
                relative_width=0.5,
                window_details=dtos.WindowDetails(mark="big", command="alacritty"),
            ),
            MakeTileArgs(
                relative_height=1.0,
                relative_width=0.25,
                window_details=dtos.WindowDetails(mark="right", command="alacritty"),
            ),
            MakeTileArgs(
                relative_height=0.6,
                relative_width=0.25,
                window_details=dtos.WindowDetails(mark="medium", command="alacritty"),
            ),
            MakeTileArgs(
                relative_height=0.4,
                relative_width=0.25,
                window_details=dtos.WindowDetails(mark="small", command="alacritty"),
            ),
        ],
        layout_name="screen",
    ),
    LayoutTestCase(
        config={
            "screen": {
                "children": [
                    {
                        "mark": "left",
                        "size": 25,
                        "command": "alacritty",
                    },
                    {
                        "mark": "center",
                        "size": 50,
                        "command": "alacritty",
                    },
                    {
                        "mark": "right",
                        "size": 25,
                        "command": "alacritty",
                    },
                ],
                "split": "horizontal",
            }
        },
        expected_call_args=[
            MakeTileArgs(
                relative_height=1.0,
                relative_width=0.25,
                window_details=dtos.WindowDetails(mark="left", command="alacritty"),
            ),
            MakeTileArgs(
                relative_height=1.0,
                relative_width=0.5,
                window_details=dtos.WindowDetails(mark="center", command="alacritty"),
            ),
            MakeTileArgs(
                relative_height=1.0,
                relative_width=0.25,
                window_details=dtos.WindowDetails(mark="right", command="alacritty"),
            ),
        ],
        layout_name="screen",
    ),
    # allow configs to define multiple layouts
    LayoutTestCase(
        config={
            "screen": {
                "children": [
                    {
                        "mark": "mymark",
                        "size": 100,
                        "command": "alacritty",
                    },
                ],
                "split": "horizontal",
            },
            "dev-ide": {
                "children": [
                    {
                        "children": [
                            {
                                "mark": "linter",
                                "size": 60,
                                "command": "alacritty",
                            },
                            {
                                "mark": "terminal",
                                "size": 40,
                                "command": "alacritty",
                            },
                        ],
                        "split": "vertical",
                        "size": 25,
                    },
                    {
                        "mark": "jumbo",
                        "size": 75,
                        "command": "alacritty",
                    },
                ],
                "split": "horizontal",
            },
        },
        expected_call_args=[
            MakeTileArgs(
                relative_height=1.0,
                relative_width=0.75,
                window_details=dtos.WindowDetails(mark="jumbo", command="alacritty"),
            ),
            MakeTileArgs(
                relative_height=0.6,
                relative_width=0.25,
                window_details=dtos.WindowDetails(mark="linter", command="alacritty"),
            ),
            MakeTileArgs(
                relative_height=0.4,
                relative_width=0.25,
                window_details=dtos.WindowDetails(mark="terminal", command="alacritty"),
            ),
        ],
        layout_name="dev-ide",
    ),
]


@pytest.mark.parametrize("test_case", layout_test_cases)
def test_layout_calls_tile_factory(test_case):
    """Make sure we're calling the tile factory correctly"""
    spy_tile_factory = SpyTileFactory()
    layout.Layout(FakeConfig(test_case.config), test_case.layout_name, spy_tile_factory)
    assert spy_tile_factory.calls == test_case.expected_call_args


def test_use_tile_factory_output():
    """Make sure we're using whatever output we get from the tile factory"""
    fake_tile_factory = SpyTileFactory()
    mylayout = layout.Layout(
        FakeConfig(
            {
                "screen": {
                    "children": [
                        {
                            "children": [
                                {
                                    "mark": "medium",
                                    "size": 60,
                                    "command": "alacritty",
                                },
                                {
                                    "mark": "small",
                                    "size": 40,
                                    "command": "alacritty",
                                },
                            ],
                            "split": "vertical",
                            "size": 25,
                        },
                        {
                            "mark": "big",
                            "size": 50,
                            "command": "alacritty",
                        },
                        {
                            "mark": "right",
                            "size": 25,
                            "command": "alacritty",
                        },
                    ],
                    "split": "horizontal",
                }
            }
        ),
        "screen",
        fake_tile_factory,
    )
    assert mylayout.tiles == [make_dummy_tile() for i in range(4)]


def test_cant_find_layout():
    with pytest.raises(KeyError):
        layout.Layout(
            FakeConfig(layout_test_cases[0].config), "nonexistent", SpyTileFactory()
        )


def test_size_shouldnt_be_defined_in_root_node():
    with pytest.raises(RuntimeError):
        layout.Layout(FakeConfig({"a": {"size": 9000}}), "a", SpyTileFactory())


def test_no_invalid_split_orientation():
    with pytest.raises(RuntimeError):
        layout.Layout(
            FakeConfig({"a": {"split": "laskdjflaskdjf"}}), "a", SpyTileFactory()
        )
