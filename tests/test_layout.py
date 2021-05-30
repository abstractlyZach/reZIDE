from typing import Any, Dict, List, NamedTuple

import pytest

from magic_tiler.utils import dtos
from magic_tiler.utils import interfaces
from magic_tiler.utils import layout


class FakeConfig(interfaces.ConfigReader):
    def __init__(self, config_dict: Dict) -> None:
        self._config_dict = config_dict

    def to_dict(self) -> Dict:
        return self._config_dict


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
    layout.Layout(
        FakeConfig(test_case.config), test_case.layout_name, spy_window_manager
    )
    assert spy_window_manager.calls == test_case.expected_call_args


def test_cant_find_layout():
    with pytest.raises(KeyError):
        layout.Layout(
            FakeConfig(layout_test_cases[0].config), "nonexistent", SpyWindowManager()
        )


def test_size_shouldnt_be_defined_in_root_node():
    with pytest.raises(RuntimeError):
        layout.Layout(FakeConfig({"a": {"size": 9000}}), "a", SpyWindowManager())


def test_no_invalid_split_orientation():
    with pytest.raises(RuntimeError):
        layout.Layout(
            FakeConfig({"a": {"split": "laskdjflaskdjf"}}), "a", SpyWindowManager()
        )


def test_throws_error_if_not_enough_children():
    with pytest.raises(RuntimeError):
        layout.Layout(
            FakeConfig({"a": {"split": "horizontal", "children": []}}),
            "a",
            SpyWindowManager(),
        )
    with pytest.raises(RuntimeError):
        layout.Layout(
            FakeConfig(
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
            "a",
            SpyWindowManager(),
        )
    # no exception raised with same config but 2 children
    layout.Layout(
        FakeConfig(
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
        "a",
        SpyWindowManager(),
    )


def test_tree():
    config = {
        "split": "horizontal",
        "children": [
            {
                "mark": "hi",
                "size": 10,
                "command": "echo hi",
            },
            {
                "mark": "moo",
                "size": 50,
                "command": "cowsay moo",
            },
        ],
    }
    actual_tree = layout.create_tree(config)
    expected_tree = layout.TreeNode("horizontal")
    layout.TreeNode(
        dtos.WindowDetails(mark="hi", command="echo hi"), parent=expected_tree
    )
    layout.TreeNode(
        dtos.WindowDetails(mark="moo", command="cowsay moo"), parent=expected_tree
    )
    assert actual_tree == expected_tree


def test_complicated_tree():
    """It's a lot of code, but I figure we need one complex test, and we can't
    do much besides handwrite it.
    """
    config = {
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
    actual_tree = layout.create_tree(config)
    expected_tree = layout.TreeNode("horizontal")
    left_side = layout.TreeNode("vertical", parent=expected_tree)
    top_left = layout.TreeNode("horizontal", parent=left_side)
    layout.TreeNode(dtos.WindowDetails(mark="A", command="alacritty"), parent=top_left)
    layout.TreeNode(dtos.WindowDetails(mark="B", command="alacritty"), parent=top_left)
    middle_left = layout.TreeNode("horizontal", parent=left_side)
    layout.TreeNode(
        dtos.WindowDetails(mark="F", command="alacritty"), parent=middle_left
    )
    layout.TreeNode(
        dtos.WindowDetails(mark="G", command="alacritty"), parent=middle_left
    )
    layout.TreeNode(dtos.WindowDetails(mark="I", command="alacritty"), parent=left_side)
    right_side = layout.TreeNode("vertical", parent=expected_tree)
    top_right = layout.TreeNode("horizontal", parent=right_side)
    layout.TreeNode(dtos.WindowDetails(mark="C", command="alacritty"), parent=top_right)
    top_right_corner = layout.TreeNode("vertical", parent=top_right)
    layout.TreeNode(
        dtos.WindowDetails(mark="D", command="alacritty"), parent=top_right_corner
    )
    layout.TreeNode(
        dtos.WindowDetails(mark="E", command="alacritty"), parent=top_right_corner
    )
    layout.TreeNode(
        dtos.WindowDetails(mark="H", command="alacritty"), parent=right_side
    )
    assert actual_tree == expected_tree


def test_tree_node_unequal_data():
    assert layout.TreeNode("a") != layout.TreeNode("b")


def test_tree_node_num_children_unequal():
    tree_1 = layout.TreeNode("a")
    layout.TreeNode(dtos.WindowDetails(mark="hi", command="echo hi"), parent=tree_1)
    tree_2 = layout.TreeNode("a")
    assert tree_1 != tree_2


def test_tree_node_children_values_unequal():
    tree_1 = layout.TreeNode("a")
    layout.TreeNode(dtos.WindowDetails(mark="hi", command="echo hi"), parent=tree_1)
    tree_2 = layout.TreeNode("a")
    layout.TreeNode(dtos.WindowDetails(mark="bye", command="echo bye"), parent=tree_2)
    assert tree_1 != tree_2


def test_tree_node_not_equal_to_non_tree_nodes():
    tree_1 = layout.TreeNode("a")
    assert tree_1 != "a"
    assert tree_1 != 1
