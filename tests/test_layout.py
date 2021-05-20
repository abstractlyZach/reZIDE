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


LayoutTestCase = collections.namedtuple(
    "LayoutTestCase", ["config", "expected_windows"]
)


layout_test_cases = [
    LayoutTestCase(
        config={
            "screen": {
                "children": [
                    {
                        "children": [
                            {"size": 60, "command": "alacritty --title medium-window"},
                            {"size": 40, "command": "alacritty --title tiny-window"},
                        ],
                        "split": "vertical",
                        "size": 25,
                    },
                    {"size": 50, "command": "alacritty --title middle-panel"},
                    {"size": 25, "command": "alacritty --title right-panel"},
                ],
                "split": "horizontal",
            }
        },
        expected_windows={
            0: {"command": "alacritty --title medium-window"},
            1: {"command": "alacritty --title tiny-window"},
            2: {"command": "alacritty --title middle-panel"},
            3: {"command": "alacritty --title right-panel"},
        },
    ),
    LayoutTestCase(
        config={
            "screen": {
                "children": [
                    {"size": 25, "command": "alacritty --title left-panel"},
                    {"size": 50, "command": "alacritty --title middle-panel"},
                    {"size": 25, "command": "alacritty --title right-panel"},
                ],
                "split": "horizontal",
            }
        },
        expected_windows={
            0: {"command": "alacritty --title left-panel"},
            1: {"command": "alacritty --title middle-panel"},
            2: {"command": "alacritty --title right-panel"},
        },
    ),
    # Automatically assign IDs only to windows that don't have their own IDs
    LayoutTestCase(
        config={
            "screen": {
                "children": [
                    {"size": 25, "command": "alacritty --title left-panel", "id": 50},
                    {"size": 50, "command": "alacritty --title middle-panel"},
                    {"size": 25, "command": "alacritty --title right-panel"},
                ],
                "split": "horizontal",
            }
        },
        expected_windows={
            50: {"command": "alacritty --title left-panel"},
            0: {"command": "alacritty --title middle-panel"},
            1: {"command": "alacritty --title right-panel"},
        },
    ),
    # automatically assigned IDs shouldn't collide with user-defined IDs
    # so we shouldn't tag the first window with ID 0
    LayoutTestCase(
        config={
            "screen": {
                "children": [
                    {"size": 25, "command": "alacritty --title left-panel"},
                    {
                        "size": 50,
                        "command": "alacritty --title middle-left-panel",
                        "id": 0,
                    },
                    {"size": 50, "command": "alacritty --title middle-right-panel"},
                    {"size": 25, "command": "alacritty --title right-panel"},
                ],
                "split": "horizontal",
            }
        },
        expected_windows={
            1: {"command": "alacritty --title left-panel"},
            0: {"command": "alacritty --title middle-left-panel"},
            2: {"command": "alacritty --title middle-right-panel"},
            3: {"command": "alacritty --title right-panel"},
        },
    ),
]


@pytest.mark.parametrize("test_case", layout_test_cases)
def test_layout(test_case):
    mylayout = layout.Layout(FakeConfig(test_case.config), "screen")
    assert mylayout.windows == test_case.expected_windows


def test_duplicate_ids_raise_exception():
    config = {
        "screen": {
            "children": [
                {"size": 25, "command": "alacritty --title left-panel", "id": 17},
                {
                    "size": 50,
                    "command": "alacritty --title middle-left-panel",
                    "id": 17,
                },
                {"size": 50, "command": "alacritty --title middle-right-panel"},
                {"size": 25, "command": "alacritty --title right-panel"},
            ],
            "split": "horizontal",
        }
    }
    with pytest.raises(KeyError):
        layout.Layout(FakeConfig(config), "screen")
