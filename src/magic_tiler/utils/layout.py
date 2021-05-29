# https://stackoverflow.com/questions/36286894/name-not-defined-in-type-annotation
from __future__ import annotations

import collections
from typing import Any, Dict, List, Optional, Set

from magic_tiler.utils import dtos
from magic_tiler.utils import interfaces


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


# we need to use a depth-y breadth-first traversal in order to properly
# open up the sway windows. basically, we need sway to reserve space
# for splits beyond the top-level split, so we need to create a window
# to reserve that space. Therefore we do breadth-first traversal, but we
# promote the first window in each section straight to the front of the queue


class Layout(object):
    """Convert a configuration into a collection of Tiles"""

    def __init__(
        self,
        config_reader: interfaces.ConfigReader,
        layout_name: str,
        window_manager: interfaces.TilingWindowManager,
    ) -> None:
        self._window_manager = window_manager
        self._windows: Dict[str, dtos.WindowDetails] = dict()
        try:
            root_node = config_reader.to_dict()[layout_name]
        except KeyError:
            raise KeyError(f'Could not find layout "{layout_name}" in config')
        if "size" in root_node:
            raise RuntimeError("root node shouldn't have a size. size is implied 100")
        root_node["size"] = 100
        tree = self._create_tree(root_node)
        self._parse_tree(tree)

    def _create_tree(self, node: Dict, parent: Optional[TreeNode] = None) -> TreeNode:
        if "mark" in node:
            current_node = TreeNode(
                dtos.WindowDetails(mark=node["mark"], command=node["command"]),
                parent=parent,
            )
        elif "children" in node:
            current_node = TreeNode(node["split"])
            if len(node["children"]) <= 1:
                raise RuntimeError("each parent needs at least 2 children")
            for child in node["children"]:
                child_node = self._create_tree(child, current_node)
                current_node.add_child(child_node)
        else:
            raise RuntimeError("invalid config file")
        return current_node

    def _parse_tree(self, root_node: TreeNode) -> None:
        node_queue = collections.deque([root_node])
        created_windows: Set[str] = set()
        while len(node_queue) >= 1:
            current_node = node_queue.popleft()
            leftmost_descendant = current_node.get_leftmost_descendant()
            if leftmost_descendant.data.mark in created_windows:
                pass
            else:
                self._window_manager.make_window(leftmost_descendant.data)
                created_windows.add(leftmost_descendant.data.mark)
            if current_node.is_parent:
                for child in current_node.children:
                    node_queue.append(child)
