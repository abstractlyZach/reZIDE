# https://stackoverflow.com/questions/36286894/name-not-defined-in-type-annotation
from __future__ import annotations

from typing import Any, Dict, List, Optional

from magic_tiler.utils import dtos


class TreeFactory:
    def create_tree(self, tree_dict: Dict) -> TreeNode:
        return self._create_subtree(tree_dict)

    def _create_subtree(
        self, node: Dict, parent: Optional[TreeNode] = None
    ) -> TreeNode:
        """Recursively create the subtree of the current node and everything below it"""
        if "mark" in node:
            current_node = TreeNode(
                dtos.WindowDetails(mark=node["mark"], command=node["command"]),
                parent=parent,
            )
        elif "children" in node:
            current_node = TreeNode(node["split"], parent=parent)
            if len(node["children"]) <= 1:
                raise RuntimeError("each parent needs at least 2 children")
            for child in node["children"]:
                self._create_subtree(child, current_node)
        else:
            raise RuntimeError("invalid config file")
        return current_node


class TreeNode(object):
    def __init__(self, data: Any, parent: TreeNode = None) -> None:
        self._data = data
        self._children: List[TreeNode] = []
        if parent:
            parent.add_child(self)

    def add_child(self, node: TreeNode) -> None:
        self._children.append(node)

    def get_leftmost_descendant(self) -> TreeNode:
        if self.is_parent:
            return self.children[0].get_leftmost_descendant()
        else:
            return self

    @property
    def is_parent(self) -> bool:
        return len(self._children) > 0

    @property
    def children(self) -> List[TreeNode]:
        return self._children

    @property
    def data(self) -> Any:
        return self._data

    def __str__(self) -> str:
        return f"{self.data}: {self._children}"

    def __repr__(self) -> str:
        return f"TreeNode<{len(self.children)}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TreeNode):
            return False
        if len(self.children) != len(other.children):
            return False
        for my_child, other_child in zip(self.children, other.children):
            if my_child != other_child:
                return False
        return self.data == other.data
