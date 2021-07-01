import pytest

from magic_tiler.utils import dtos
from magic_tiler.utils import tree


def test_tree_creation():
    tree_dict = {
        "split": "horizontal",
        "sizes": [50, 50],
        "children": [
            {
                "mark": "hi",
                "command": "echo hi",
            },
            {
                "mark": "moo",
                "command": "cowsay moo",
            },
        ],
    }
    actual_tree = tree.TreeFactory().create_tree(tree_dict)
    expected_tree = tree.Section("horizontal", [50, 50])
    tree.Window(dtos.WindowDetails(mark="hi", command="echo hi"), parent=expected_tree)
    tree.Window(
        dtos.WindowDetails(mark="moo", command="cowsay moo"), parent=expected_tree
    )
    assert actual_tree == expected_tree


def test_complicated_tree_creation():
    """It's a lot of code, but I figure we need one complex test, and we can't
    do much besides handwrite it.
    """
    config = {
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
    }
    actual_tree = tree.TreeFactory().create_tree(config)
    expected_tree = tree.Section("horizontal", [50, 50])
    left_side = tree.Section("vertical", [33, 33, 34], parent=expected_tree)
    top_left = tree.Section("horizontal", [50, 50], parent=left_side)
    tree.Window(dtos.WindowDetails(mark="A", command="alacritty"), parent=top_left)
    tree.Window(dtos.WindowDetails(mark="B", command="alacritty"), parent=top_left)
    middle_left = tree.Section("horizontal", [20, 80], parent=left_side)
    tree.Window(dtos.WindowDetails(mark="F", command="alacritty"), parent=middle_left)
    tree.Window(dtos.WindowDetails(mark="G", command="alacritty"), parent=middle_left)
    tree.Window(dtos.WindowDetails(mark="I", command="alacritty"), parent=left_side)
    right_side = tree.Section("vertical", [50, 50], parent=expected_tree)
    top_right = tree.Section("horizontal", [70, 30], parent=right_side)
    tree.Window(dtos.WindowDetails(mark="C", command="alacritty"), parent=top_right)
    top_right_corner = tree.Section("vertical", [50, 50], parent=top_right)
    tree.Window(
        dtos.WindowDetails(mark="D", command="alacritty"), parent=top_right_corner
    )
    tree.Window(
        dtos.WindowDetails(mark="E", command="alacritty"), parent=top_right_corner
    )
    tree.Window(dtos.WindowDetails(mark="H", command="alacritty"), parent=right_side)
    assert actual_tree == expected_tree


def test_window_unequal_data():
    assert tree.Window(
        dtos.WindowDetails(mark="D", command="alacritty")
    ) != tree.Window(dtos.WindowDetails(mark="E", command="brave"))


def test_section_num_children_unequal():
    tree_1 = tree.Section("a", [])
    tree.Window(dtos.WindowDetails(mark="hi", command="echo hi"), parent=tree_1)
    tree_2 = tree.Section("a", [])
    assert tree_1 != tree_2


def test_tree_node_children_values_unequal():
    tree_1 = tree.Section("a", [])
    tree.Window(dtos.WindowDetails(mark="hi", command="echo hi"), parent=tree_1)
    tree_2 = tree.Section("a", [])
    tree.Window(dtos.WindowDetails(mark="bye", command="echo bye"), parent=tree_2)
    assert tree_1 != tree_2


def test_section_not_equal_to_non_section():
    tree_1 = tree.Section("a", [])
    assert tree_1 != "a"
    assert tree_1 != 1


def test_window_not_equal_to_non_window():
    my_tree = tree.Window(dtos.WindowDetails(mark="hi", command="echo hi"))
    assert my_tree != "hi"
    assert my_tree != 1


def test_windows_can_have_different_parents_and_still_be_equal():
    """A window should be characterized by its mark and command, not its position
    in the tree
    """
    tree_1 = tree.Section("a", [])
    tree_2 = tree.Section("b", [])
    window_1 = tree.Window(
        dtos.WindowDetails(mark="hi", command="echo hi"), parent=tree_1
    )
    window_2 = tree.Window(
        dtos.WindowDetails(mark="hi", command="echo hi"), parent=tree_2
    )
    assert window_1 == window_2


def test_window_cant_add_child():
    window_1 = tree.Window(dtos.WindowDetails(mark="hi", command="echo hi"))
    window_2 = tree.Window(dtos.WindowDetails(mark="hi", command="echo hi"))
    with pytest.raises(RuntimeError):
        window_2.add_child(window_1)
