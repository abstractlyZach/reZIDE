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
]


@pytest.mark.parametrize("test_case", layout_test_cases)
def test_layout(test_case):
    mylayout = layout.Layout(FakeConfig(test_case.config), "screen")
    assert mylayout.windows == test_case.expected_windows
