from magic_tiler.utils import dtos
from magic_tiler.utils import tree


def test_tree_creation():
    tree_dict = {
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
    actual_tree = tree.TreeFactory().create_tree(tree_dict)
    expected_tree = tree.Container("horizontal")
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
    actual_tree = tree.TreeFactory().create_tree(config)
    expected_tree = tree.Container("horizontal")
    left_side = tree.Container("vertical", parent=expected_tree)
    top_left = tree.Container("horizontal", parent=left_side)
    tree.Window(dtos.WindowDetails(mark="A", command="alacritty"), parent=top_left)
    tree.Window(dtos.WindowDetails(mark="B", command="alacritty"), parent=top_left)
    middle_left = tree.Container("horizontal", parent=left_side)
    tree.Window(dtos.WindowDetails(mark="F", command="alacritty"), parent=middle_left)
    tree.Window(dtos.WindowDetails(mark="G", command="alacritty"), parent=middle_left)
    tree.Window(dtos.WindowDetails(mark="I", command="alacritty"), parent=left_side)
    right_side = tree.Container("vertical", parent=expected_tree)
    top_right = tree.Container("horizontal", parent=right_side)
    tree.Window(dtos.WindowDetails(mark="C", command="alacritty"), parent=top_right)
    top_right_corner = tree.Container("vertical", parent=top_right)
    tree.Window(
        dtos.WindowDetails(mark="D", command="alacritty"), parent=top_right_corner
    )
    tree.Window(
        dtos.WindowDetails(mark="E", command="alacritty"), parent=top_right_corner
    )
    tree.Window(dtos.WindowDetails(mark="H", command="alacritty"), parent=right_side)
    assert actual_tree == expected_tree


def test_window_unequal_data():
    assert tree.Window("a") != tree.Window("b")


def test_container_num_children_unequal():
    tree_1 = tree.Container("a")
    tree.Window(dtos.WindowDetails(mark="hi", command="echo hi"), parent=tree_1)
    tree_2 = tree.Container("a")
    assert tree_1 != tree_2


def test_tree_node_children_values_unequal():
    tree_1 = tree.Container("a")
    tree.Window(dtos.WindowDetails(mark="hi", command="echo hi"), parent=tree_1)
    tree_2 = tree.Container("a")
    tree.Window(dtos.WindowDetails(mark="bye", command="echo bye"), parent=tree_2)
    assert tree_1 != tree_2


def test_container_not_equal_to_non_container():
    tree_1 = tree.Container("a")
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
    tree_1 = tree.Container("a")
    tree_2 = tree.Container("b")
    window_1 = tree.Window(
        dtos.WindowDetails(mark="hi", command="echo hi"), parent=tree_1
    )
    window_2 = tree.Window(
        dtos.WindowDetails(mark="hi", command="echo hi"), parent=tree_2
    )
    assert window_1 == window_2
