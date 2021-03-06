from typing import Dict, List, NamedTuple

import pytest

from rezide.utils import dtos
from rezide.utils import layouts
from tests import fakes


class LayoutManagerTestCase(NamedTuple):
    config: Dict
    expected_call_args: List[dtos.WindowManagerCall]
    layout_name: str


layout_test_cases = [
    LayoutManagerTestCase(
        config={
            "sizes": [25, 50, 25],
            "children": [
                {
                    "sizes": [60, 40],
                    "children": [
                        {
                            "mark": "medium",
                            "command": "alacritty",
                        },
                        {
                            "mark": "small",
                            "command": "alacritty",
                        },
                    ],
                    "split": "vertical",
                },
                {
                    "mark": "big",
                    "command": "alacritty",
                },
                {
                    "mark": "right",
                    "command": "alacritty",
                },
            ],
            "split": "horizontal",
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
            "sizes": [25, 50, 25],
            "children": [
                {
                    "mark": "left",
                    "command": "alacritty",
                },
                {
                    "mark": "center",
                    "command": "alacritty",
                },
                {
                    "mark": "right",
                    "command": "alacritty",
                },
            ],
            "split": "horizontal",
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
    LayoutManagerTestCase(
        config={
            "split": "horizontal",
            "sizes": [50, 50],
            "children": [
                {
                    "split": "vertical",
                    "sizes": [33, 33, 34],
                    "children": [
                        {
                            "split": "horizontal",
                            "sizes": [50, 50],
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
                            "sizes": [20, 80],
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
                    "sizes": [50, 50],
                    "children": [
                        {
                            "split": "horizontal",
                            "sizes": [70, 30],
                            "children": [
                                {
                                    "mark": "C",
                                    "command": "alacritty",
                                },
                                {
                                    "split": "vertical",
                                    "sizes": [50, 50],
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
        fakes.FakeConfigParser(test_case.config), spy_window_manager
    )
    layout.spawn_windows()
    assert spy_window_manager.calls == test_case.expected_call_args


@pytest.mark.parametrize("num_children", [2, 5, 20])
def test_doesnt_raise_exception_when_2_or_more_children(num_children):
    """no exception raised with same config as above, but multiple children"""
    layout_manager = layouts.LayoutManager(
        fakes.FakeConfigParser(
            {
                "split": "horizontal",
                "sizes": [10 for i in range(num_children)],
                "children": [
                    {"command": "echo hi", "mark": f"mark {i}"}
                    for i in range(num_children)
                ],
            }
        ),
        fakes.FakeWindowManager(),
    )
    layout_manager.spawn_windows()


@pytest.mark.parametrize("num_open_windows", [2, 20, 100])
def test_fails_if_too_many_windows_open(num_open_windows):
    layout = layouts.LayoutManager(
        fakes.FakeConfigParser(
            {
                "mark": "mymark",
                "command": "alacritty",
            }
        ),
        fakes.FakeWindowManager(num_workspace_windows=num_open_windows),
    )
    with pytest.raises(RuntimeError):
        layout.spawn_windows()
