import collections
from typing import Dict

import pytest

from magic_tiler import interfaces
from magic_tiler import layout


class FakeConfig(interfaces.ConfigReader):
    def __init__(self, config_dict: Dict) -> None:
        self._config_dict = config_dict

    def to_dict(self) -> Dict:
        return self._config_dict


class FakeTileFactory(interfaces.TileFactoryInterface):
    def make_tile(
        self,
        relative_width: float,
        relative_height: float,
        window_details: interfaces.WindowDetails,
    ) -> interfaces.Tile:
        pass


LayoutTestCase = collections.namedtuple(
    "LayoutTestCase", ["config", "expected_windows", "layout_name"]
)


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
        expected_windows={
            "medium": interfaces.WindowDetails(command="alacritty", mark="medium"),
            "small": interfaces.WindowDetails(command="alacritty", mark="small"),
            "big": interfaces.WindowDetails(command="alacritty", mark="big"),
            "right": interfaces.WindowDetails(command="alacritty", mark="right"),
        },
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
        expected_windows={
            "left": interfaces.WindowDetails(command="alacritty", mark="left"),
            "center": interfaces.WindowDetails(command="alacritty", mark="center"),
            "right": interfaces.WindowDetails(command="alacritty", mark="right"),
        },
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
        expected_windows={
            "linter": interfaces.WindowDetails(command="alacritty", mark="linter"),
            "terminal": interfaces.WindowDetails(command="alacritty", mark="terminal"),
            "jumbo": interfaces.WindowDetails(command="alacritty", mark="jumbo"),
        },
        layout_name="dev-ide",
    ),
]


@pytest.mark.parametrize("test_case", layout_test_cases)
def test_layout(test_case):
    mylayout = layout.Layout(
        FakeConfig(test_case.config), test_case.layout_name, FakeTileFactory()
    )
    assert mylayout.windows == test_case.expected_windows


def test_cant_find_layout():
    with pytest.raises(KeyError):
        layout.Layout(
            FakeConfig(layout_test_cases[0].config), "nonexistent", FakeTileFactory()
        )
