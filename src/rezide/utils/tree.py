# https://stackoverflow.com/questions/36286894/name-not-defined-in-type-annotation
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from rezide.utils import dtos
from rezide.utils import interfaces


class TreeFactory(interfaces.TreeFactoryInterface):
    def create_tree(self, tree_dict: Dict) -> interfaces.TreeNodeInterface:
        return self._create_subtree(tree_dict)

    def _create_subtree(self, node: Dict, parent: Optional[Section] = None) -> TreeNode:
        """Recursively create the subtree of the current node and everything below it"""
        current_node: TreeNode
        if "command" in node:
            current_node = Window(
                dtos.WindowDetails(mark=node["mark"], command=node["command"]),
                parent=parent,
            )
        elif "children" in node:
            current_node = Section(node["split"], node["sizes"], parent=parent)
            if len(node["children"]) <= 1:
                raise RuntimeError("each parent needs at least 2 children")
            for child in node["children"]:
                self._create_subtree(child, parent=current_node)
        else:
            logging.error(node)
            raise RuntimeError("invalid config file")
        return current_node


class TreeNode(interfaces.TreeNodeInterface):
    def __eq__(self, other: object) -> bool:  # pragma: nocover
        raise NotImplementedError("Can't compare base TreeNodes!")


class Section(TreeNode):
    def __init__(
        self,
        split_orientation: str,
        child_sizes: List[int],
        parent: Optional[Section] = None,
    ) -> None:
        self._split_orientation = split_orientation
        self._child_sizes = child_sizes
        self._children: List[interfaces.TreeNodeInterface] = []
        if parent:
            parent.add_child(self)

    def get_leftmost_descendant(self) -> interfaces.TreeNodeInterface:
        return self.children[0].get_leftmost_descendant()

    def add_child(self, node: interfaces.TreeNodeInterface) -> None:
        self._children.append(node)

    @property
    def is_parent(self) -> bool:
        return len(self._children) > 0

    @property
    def children(self) -> List[interfaces.TreeNodeInterface]:
        return self._children

    # probably should add coverage here eventually
    @property
    def child_sizes(self) -> List[int]:  # pragma: nocover
        return self._child_sizes

    @property
    def data(self) -> str:
        return self._split_orientation

    def __str__(self) -> str:
        return f"Section({self._children})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Section):
            return False
        if len(self.children) != len(other.children):
            return False
        for my_child, other_child in zip(self.children, other.children):
            if my_child != other_child:
                return False
        return self.data == other.data


class Window(TreeNode):
    def __init__(
        self, window_details: dtos.WindowDetails, parent: Optional[Section] = None
    ) -> None:
        self._window_details = window_details
        if parent:
            parent.add_child(self)

    def get_leftmost_descendant(self) -> interfaces.TreeNodeInterface:
        return self

    @property
    def children(self) -> List[interfaces.TreeNodeInterface]:  # pragma: no cover
        return []

    @property
    def is_parent(self) -> bool:
        return False

    @property
    def data(self) -> dtos.WindowDetails:
        return self._window_details

    def add_child(self, node: interfaces.TreeNodeInterface) -> None:
        raise RuntimeError(f"{self} is a Window. It should not have any children")

    def __str__(self) -> str:
        return f'Window("{self.data.mark}")'

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Window):
            return False
        return self.data == other.data
