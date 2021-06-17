from typing import Dict, List, NamedTuple

import pytest

from magic_tiler.utils import dtos
from magic_tiler.utils import layouts
from tests import fakes


class LayoutManagerTestCase(NamedTuple):
    config: Dict
    expected_call_args: List[dtos.WindowManagerCall]
    layout_name: str


layout_test_cases = [
    LayoutManagerTestCase(
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
            dtos.WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="medium", command="alacritty"),
            ),
            dtos.WindowManagerCall(command="split", arg="horizontal"),
            dtos.WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="big", command="alacritty")
            ),
            dtos.WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="right", command="alacritty"),
            ),
            dtos.WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="medium", command="alacritty"),
            ),
            dtos.WindowManagerCall(command="split", arg="vertical"),
            dtos.WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="small", command="alacritty"),
            ),
        ],
        layout_name="screen",
    ),
    LayoutManagerTestCase(
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
            dtos.WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="left", command="alacritty")
            ),
            dtos.WindowManagerCall(command="split", arg="horizontal"),
            dtos.WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="center", command="alacritty"),
            ),
            dtos.WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="right", command="alacritty"),
            ),
        ],
        layout_name="screen",
    ),
    # allow configs to define multiple layouts
    LayoutManagerTestCase(
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
            dtos.WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="linter", command="alacritty"),
            ),
            dtos.WindowManagerCall(command="split", arg="horizontal"),
            dtos.WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="jumbo", command="alacritty"),
            ),
            dtos.WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="linter", command="alacritty"),
            ),
            dtos.WindowManagerCall(command="split", arg="vertical"),
            dtos.WindowManagerCall(
                command="make",
                arg=dtos.WindowDetails(mark="terminal", command="alacritty"),
            ),
        ],
        layout_name="dev-ide",
    ),
    LayoutManagerTestCase(
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
            dtos.WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="A", command="alacritty")
            ),
            dtos.WindowManagerCall(command="split", arg="horizontal"),
            dtos.WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="C", command="alacritty")
            ),
            dtos.WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="A", command="alacritty"),
            ),
            dtos.WindowManagerCall(command="split", arg="vertical"),
            dtos.WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="F", command="alacritty")
            ),
            dtos.WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="I", command="alacritty")
            ),
            dtos.WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="C", command="alacritty"),
            ),
            dtos.WindowManagerCall(command="split", arg="vertical"),
            dtos.WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="H", command="alacritty")
            ),
            dtos.WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="A", command="alacritty"),
            ),
            dtos.WindowManagerCall(command="split", arg="horizontal"),
            dtos.WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="B", command="alacritty")
            ),
            dtos.WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="F", command="alacritty"),
            ),
            dtos.WindowManagerCall(command="split", arg="horizontal"),
            dtos.WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="G", command="alacritty")
            ),
            dtos.WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="C", command="alacritty"),
            ),
            dtos.WindowManagerCall(command="split", arg="horizontal"),
            dtos.WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="D", command="alacritty")
            ),
            dtos.WindowManagerCall(
                command="focus",
                arg=dtos.WindowDetails(mark="D", command="alacritty"),
            ),
            dtos.WindowManagerCall(command="split", arg="vertical"),
            dtos.WindowManagerCall(
                command="make", arg=dtos.WindowDetails(mark="E", command="alacritty")
            ),
        ],
        layout_name="complicated",
    ),
]


@pytest.mark.parametrize("test_case", layout_test_cases)
def test_layout_calls_window_manager(test_case):
    """Make sure we're calling the window manager correctly"""
    spy_window_manager = fakes.SpyWindowManager()
    layout = layouts.LayoutManager(
        fakes.FakeConfig(test_case.config), spy_window_manager
    )
    layout.select(test_case.layout_name)
    layout.spawn_windows()
    assert spy_window_manager.calls == test_case.expected_call_args


def test_cant_find_layout():
    layout = layouts.LayoutManager(
        fakes.FakeConfig(layout_test_cases[0].config),
        fakes.FakeWindowManager(),
    )
    with pytest.raises(KeyError):
        layout.select("doesn't exist abcdefg")


def test_size_shouldnt_be_defined_in_root_node():
    layout = layouts.LayoutManager(
        fakes.FakeConfig({"a": {"size": 9000}}), fakes.FakeWindowManager()
    )
    with pytest.raises(RuntimeError):
        layout.select("a")


def test_fails_if_invalid_split_orientation():
    layout = layouts.LayoutManager(
        fakes.FakeConfig({"a": {"split": "laskdjflaskdjf"}}),
        fakes.FakeWindowManager(),
    )
    with pytest.raises(RuntimeError):
        layout.select("a")


@pytest.mark.parametrize("num_children", [0, 1])
def test_throws_error_if_not_enough_children(num_children):
    layout_manager = layouts.LayoutManager(
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
                        for i in range(num_children)
                    ],
                }
            }
        ),
        fakes.FakeWindowManager(),
    )
    with pytest.raises(RuntimeError):
        layout_manager.select("a")


@pytest.mark.parametrize("num_children", [2, 5, 20])
def test_doesnt_raise_exception_when_2_or_more_children(num_children):
    """no exception raised with same config as above, but multiple children"""
    layout_manager = layouts.LayoutManager(
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
                        for i in range(num_children)
                    ],
                }
            }
        ),
        fakes.FakeWindowManager(),
    )
    layout_manager.select("a")
    layout_manager.spawn_windows()


@pytest.mark.parametrize("num_open_windows", [2, 20, 100])
def test_fails_if_too_many_windows_open(num_open_windows):
    layout = layouts.LayoutManager(
        fakes.FakeConfig(
            {
                "screen": {
                    "mark": "mymark",
                    "command": "alacritty",
                },
            }
        ),
        fakes.FakeWindowManager(num_workspace_windows=num_open_windows),
    )
    layout.select("screen")
    with pytest.raises(RuntimeError):
        layout.spawn_windows()


def test_raises_exception_if_no_selection():
    layout = layouts.LayoutManager(
        fakes.FakeConfig({}),
        fakes.FakeWindowManager(),
    )
    with pytest.raises(RuntimeError):
        layout.spawn_windows()
