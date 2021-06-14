import collections
import logging
from typing import Set

from magic_tiler.utils import interfaces
from magic_tiler.utils import tree

# We use depth-first traversal to create each leaf node in the tree. We
# create the leftmost descendant of each parent first so that it can reserve
# space for its other siblings.


class Layout(object):
    def __init__(
        self,
        config_reader: interfaces.ConfigReader,
        window_manager: interfaces.TilingWindowManager,
    ) -> None:
        self._window_manager = window_manager
        self._config_reader = config_reader

    def select(self, layout_name: str) -> None:
        try:
            self._root_node = self._config_reader.to_dict()[layout_name]
        except KeyError:
            raise KeyError(f'Could not find layout "{layout_name}" in config')
        if "size" in self._root_node:
            raise RuntimeError("root node shouldn't have a size. size is implied 100")
        self._root_node["size"] = 100

    def spawn_windows(self) -> None:
        logging.debug(
            f"{self._window_manager.num_workspace_windows} windows"
            + " are open in the current workspace"
        )
        if self._window_manager.num_workspace_windows > 1:
            raise RuntimeError(
                "There are multiple windows open in the current workspace."
            )
        tree_root = tree.create_tree(self._root_node)
        self._parse_tree(tree_root)

    def _parse_tree(self, root_node: tree.TreeNode) -> None:
        node_queue = collections.deque([root_node])
        self._created_windows: Set[str] = set()
        while len(node_queue) >= 1:
            current_node = node_queue.popleft()
            logging.debug(f"dequeuing {current_node}")
            if current_node.is_parent:
                self._attempt_to_create_leftmost_descendant(current_node.children[0])
                self._window_manager.split(current_node.data)
                for child in current_node.children[1:]:
                    self._attempt_to_create_leftmost_descendant(child)
                for child in current_node.children:
                    node_queue.append(child)

    def _attempt_to_create_leftmost_descendant(self, node: tree.TreeNode) -> None:
        logging.debug(f"getting leftmost descendant of {node}")
        leftmost_descendant = node.get_leftmost_descendant()
        if leftmost_descendant.data.mark in self._created_windows:
            self._window_manager.focus(leftmost_descendant.data)
        else:
            self._window_manager.make_window(leftmost_descendant.data)
            self._created_windows.add(leftmost_descendant.data.mark)
