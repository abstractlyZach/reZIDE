from typing import Dict, Set

from magic_tiler import interfaces


class Layout(object):
    """Convert a configuration into a collection of Tiles"""

    def __init__(
        self, config_reader: interfaces.ConfigReader, layout_name: str
    ) -> None:
        self._windows: Dict[int, Dict] = dict()
        self._parse_config(config_reader.to_dict()[layout_name])

    def _parse_config(self, layout_dict: Dict) -> None:
        self._reserved_ids: Set = set()
        self._next_window_id: int = 0
        self._get_reserved_ids(layout_dict)
        self._parse_node(layout_dict)

    def _get_reserved_ids(self, node: Dict) -> None:
        """Recursively parse a node and its children using depth-first traversal
        to get the user-defined IDs and reserve them.
        """
        if "children" in node:
            for child_node in node["children"]:
                self._get_reserved_ids(child_node)
        else:  # process the node if it's a leaf
            if "id" in node:  # custom user-defined id
                if node["id"] in self._reserved_ids:
                    raise KeyError(
                        "There are multiple windows with the same ID in your config"
                    )
                self._reserved_ids.add(node["id"])

    def _parse_node(self, node: Dict) -> None:
        """Recursively process a node and its children using depth-first traversal"""
        if "children" in node:
            for child_node in node["children"]:
                self._parse_node(child_node)
        else:  # process the node if it's a leaf
            if "id" in node:  # custom user-defined id
                self._windows[node["id"]] = {"command": node["command"]}
            else:
                while self._next_window_id in self._reserved_ids:
                    self._next_window_id += 1
                self._windows[self._next_window_id] = {"command": node["command"]}
                self._next_window_id += 1

    @property
    def windows(self) -> Dict:
        return self._windows
