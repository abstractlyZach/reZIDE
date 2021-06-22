# https://stackoverflow.com/questions/36286894/name-not-defined-in-type-annotation
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from magic_tiler.utils import dtos
from magic_tiler.utils import interfaces


class TreeFactory(interfaces.TreeFactoryInterface):
    def create_tree(self, tree_dict: Dict) -> interfaces.TreeNodeInterface:
        return self._create_subtree(tree_dict)

    def _create_subtree(
        self, node: Dict, parent: Optional[Container] = None
    ) -> TreeNode:
        """Recursively create the subtree of the current node and everything below it"""
        current_node: TreeNode
        if "mark" in node:
            current_node = Window(
                dtos.WindowDetails(mark=node["mark"], command=node["command"]),
                parent=parent,
            )
        elif "children" in node:
            current_node = Container(node["split"], parent=parent)
            if len(node["children"]) <= 1:
                raise RuntimeError("each parent needs at least 2 children")
            for child in node["children"]:
                self._create_subtree(child, current_node)
        else:
            logging.error(node)
            raise RuntimeError("invalid config file")
        return current_node


class TreeNode(interfaces.TreeNodeInterface):
    def __eq__(self, other: object) -> bool:  # pragma: nocover
        raise NotImplementedError("Can't compare base TreeNodes!")


class Container(TreeNode):
    def __init__(self, data: Any, parent: Optional[Container] = None) -> None:
        self._data = data
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

    @property
    def data(self) -> Any:
        return self._data

    def __str__(self) -> str:
        return f"Container({self._children})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Container):
            return False
        if len(self.children) != len(other.children):
            return False
        for my_child, other_child in zip(self.children, other.children):
            if my_child != other_child:
                return False
        return self.data == other.data


class Window(TreeNode):
    def __init__(self, data: Any, parent: Optional[Container] = None) -> None:
        self._data = data
        if parent:
            parent.add_child(self)

    def get_leftmost_descendant(self) -> interfaces.TreeNodeInterface:
        return self

    @property
    def is_parent(self) -> bool:
        return False

    @property
    def data(self) -> Any:
        return self._data

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
