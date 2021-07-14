import collections
import logging
from typing import Iterable, Set

from rezide.utils import interfaces

# We use depth-first traversal to create each leaf node in the tree. We
# create the leftmost descendant of each parent first so that it can reserve
# space for its other siblings.


class LayoutManager(object):
    def __init__(
        self,
        config_parser: interfaces.ConfigParserInterface,
        window_manager: interfaces.TilingWindowManager,
    ) -> None:
        self._window_manager = window_manager
        self._config_parser = config_parser
        # make sure that our configuration is valid
        self._config_parser.validate()
        self._layout_has_been_selected = False

    def select(self, layout_name: str) -> None:
        selected_tree = self._config_parser.get_tree(layout_name)
        self._layout_has_been_selected = True
        self._selected_layout = Layout(selected_tree)

    def spawn_windows(self) -> None:
        if not self._layout_has_been_selected:
            raise RuntimeError("No layout selected")
        logging.debug(
            f"{self._window_manager.num_workspace_windows} windows"
            + " are open in the current workspace"
        )
        if self._window_manager.num_workspace_windows > 1:
            raise RuntimeError(
                "There are multiple windows open in the current workspace."
            )
        self._created_windows: Set[str] = set()
        for window in self._selected_layout.zachstras_traversal():
            if window.is_parent:
                self._window_manager.split_and_mark_parent(window.data, "abc")
            elif window.data.mark in self._created_windows:
                self._window_manager.focus(window.data)
            else:
                self._window_manager.make_window(window.data)
                self._created_windows.add(window.data.mark)


class Layout(object):
    def __init__(self, tree_: interfaces.TreeNodeInterface) -> None:
        self._tree = tree_

    def zachstras_traversal(self) -> Iterable[interfaces.TreeNodeInterface]:
        node_queue = collections.deque([self._tree])
        while len(node_queue) >= 1:
            current_node = node_queue.popleft()
            logging.debug(f"dequeuing {current_node}")
            if current_node.is_parent:
                yield current_node.children[0].get_leftmost_descendant()
                yield current_node
                for child in current_node.children[1:]:
                    yield child.get_leftmost_descendant()
                for child in current_node.children:
                    node_queue.append(child)
