from typing import Any, Dict, List, NamedTuple

import pytest

from magic_tiler.utils import dtos
from magic_tiler.utils import interfaces
from magic_tiler.utils import layouts
from tests import fakes


class WindowManagerCall(NamedTuple):
    command: str
    arg: Any


class SpyWindowManager(interfaces.TilingWindowManager):
    """Gets passed into Layouts using dependency injection
    and spys on their calls so we can make sure that we're doing
    the tile math correctly
    """

    def __init__(self):
        self._calls: List[WindowManagerCall] = []

    def make_window(
        self,
        window_details: dtos.WindowDetails,
    ) -> None:
        self._calls.append(WindowManagerCall(command="make", arg=window_details))

    @property
    def calls(self):
        return self._calls

    @property
    def num_workspace_windows(self):
        pass

    def resize_width(
        self, target_window: dtos.WindowDetails, container_percentage: int
    ) -> None:
        pass

    def resize_height(
        self, target_window: dtos.WindowDetails, container_percentage: int
    ) -> None:
        pass

    def focus(self, target_window: dtos.WindowDetails) -> None:
        self._calls.append(WindowManagerCall("focus", arg=target_window))

    def split(self, split_type: str) -> None:
        self._calls.append(WindowManagerCall("split", arg=split_type))

    def get_tree(self):
        pass

    def get_window_sizes(self) -> Dict:
        pass


class LayoutTestCase(NamedTuple):
    config: Dict
    expected_call_args: List[WindowManagerCall]
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
            WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="medium", command="alacritty"),
            ),
            WindowManagerCall(command="split", arg="horizontal"),
            WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="big", command="alacritty")
            ),
            WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="right", command="alacritty"),
            ),
            WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="medium", command="alacritty"),
            ),
            WindowManagerCall(command="split", arg="vertical"),
            WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="small", command="alacritty"),
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
            WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="left", command="alacritty")
            ),
            WindowManagerCall(command="split", arg="horizontal"),
            WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="center", command="alacritty"),
            ),
            WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="right", command="alacritty"),
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
            WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="linter", command="alacritty"),
            ),
            WindowManagerCall(command="split", arg="horizontal"),
            WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="jumbo", command="alacritty"),
            ),
            WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="linter", command="alacritty"),
            ),
            WindowManagerCall(command="split", arg="vertical"),
            WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="terminal", command="alacritty"),
            ),
        ],
        layout_name="dev-ide",
    ),
    LayoutTestCase(
        config={
            "complicated": {
                "split": "horizontal",
                "children": [
                    {
                        "split": "vertical",
                        "children": [
                            {
                                "split": "horizontal",
                                "children": [
                                    {
                                        "mark": "A",
                                        "command": "alacritty",
                                    },
                                    {
                                        "mark": "B",
                                        "command": "alacritty",
                                    },
                                ],
                            },
                            {
                                "split": "horizontal",
                                "children": [
                                    {
                                        "mark": "F",
                                        "command": "alacritty",
                                    },
                                    {
                                        "mark": "G",
                                        "command": "alacritty",
                                    },
                                ],
                            },
                            {
                                "mark": "I",
                                "command": "alacritty",
                            },
                        ],
                    },
                    {
                        "split": "vertical",
                        "children": [
                            {
                                "split": "horizontal",
                                "children": [
                                    {
                                        "mark": "C",
                                        "command": "alacritty",
                                    },
                                    {
                                        "split": "vertical",
                                        "children": [
                                            {
                                                "mark": "D",
                                                "command": "alacritty",
                                            },
                                            {
                                                "mark": "E",
                                                "command": "alacritty",
                                            },
                                        ],
                                    },
                                ],
                            },
                            {"mark": "H", "command": "alacritty"},
                        ],
                    },
                ],
            }
        },
        expected_call_args=[
            WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="A", command="alacritty")
            ),
            WindowManagerCall(command="split", arg="horizontal"),
            WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="C", command="alacritty")
            ),
            WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="A", command="alacritty"),
            ),
            WindowManagerCall(command="split", arg="vertical"),
            WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="F", command="alacritty")
            ),
            WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="I", command="alacritty")
            ),
            WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="C", command="alacritty"),
            ),
            WindowManagerCall(command="split", arg="vertical"),
            WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="H", command="alacritty")
            ),
            WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="A", command="alacritty"),
            ),
            WindowManagerCall(command="split", arg="horizontal"),
            WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="B", command="alacritty")
            ),
            WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="F", command="alacritty"),
            ),
            WindowManagerCall(command="split", arg="horizontal"),
            WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="G", command="alacritty")
            ),
            WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="C", command="alacritty"),
            ),
            WindowManagerCall(command="split", arg="horizontal"),
            WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="D", command="alacritty")
            ),
            WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="D", command="alacritty"),
            ),
            WindowManagerCall(command="split", arg="vertical"),
            WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="E", command="alacritty")
            ),
        ],
        layout_name="complicated",
    ),
]


@pytest.mark.parametrize("test_case", layout_test_cases)
def test_layout_calls_tile_factory(test_case):
    """Make sure we're calling the tile factory correctly"""
    spy_window_manager = SpyWindowManager()
    layout = layouts.Layout(
        fakes.FakeConfig(test_case.config),
        spy_window_manager,
    )
    layout.spawn_windows(test_case.layout_name)
    assert spy_window_manager.calls == test_case.expected_call_args


def test_cant_find_layout():
    layout = layouts.Layout(
        fakes.FakeConfig(layout_test_cases[0].config),
        SpyWindowManager(),
    )
    with pytest.raises(KeyError):
        layout.spawn_windows("a")


def test_size_shouldnt_be_defined_in_root_node():
    layout = layouts.Layout(fakes.FakeConfig({"a": {"size": 9000}}), SpyWindowManager())
    with pytest.raises(RuntimeError):
        layout.spawn_windows("a")


def test_no_invalid_split_orientation():
    layout = layouts.Layout(
        fakes.FakeConfig({"a": {"split": "laskdjflaskdjf"}}),
        SpyWindowManager(),
    )
    with pytest.raises(RuntimeError):
        layout.spawn_windows("a")


def test_throws_error_if_not_enough_children():
    failing_layouts = []
    failing_layouts.append(
        layouts.Layout(
            fakes.FakeConfig({"a": {"split": "horizontal", "children": []}}),
            SpyWindowManager(),
        )
    )
    failing_layouts.append(
        layouts.Layout(
            fakes.FakeConfig({"a": {"split": "horizontal", "children": []}}),
            SpyWindowManager(),
        )
    )
    failing_layouts.append(
        layouts.Layout(
            fakes.FakeConfig({"a": {"split": "horizontal", "children": []}}),
            SpyWindowManager(),
        )
    )
    failing_layouts.append(
        layouts.Layout(
            fakes.FakeConfig(
                {
                    "a": {
                        "split": "horizontal",
                        "children": [
                            {
                                "mark": "hi",
                                "size": 10,
                                "command": "echo hi",
                            }
                        ],
                    }
                }
            ),
            SpyWindowManager(),
        )
    )
    for layout in failing_layouts:
        with pytest.raises(RuntimeError):
            layout.spawn_windows("a")

    # no exception raised with same config but 2 children
    layout_5 = layouts.Layout(
        fakes.FakeConfig(
            {
                "a": {
                    "split": "horizontal",
                    "children": [
                        {
                            "mark": "hi",
                            "size": 10,
                            "command": "echo hi",
                        },
                        {
                            "mark": "hi",
                            "size": 10,
                            "command": "echo hi",
                        },
                    ],
                }
            }
        ),
        SpyWindowManager(),
    )
    layout_5.spawn_windows("a")
