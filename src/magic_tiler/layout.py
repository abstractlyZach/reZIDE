from typing import Dict

from magic_tiler import interfaces


class Layout(object):
    def __init__(
        self, config_reader: interfaces.ConfigReader, layout_name: str
    ) -> None:
        self._config = config_reader.to_dict()
        self._windows: Dict[int, Dict] = dict()
        self._next_window_id: int = 0
        self._parse_node(self._config[layout_name])

    def _parse_node(self, node: Dict) -> None:
        """Recursively process a node and its children using depth-first traversal"""
        if "children" in node:
            for child_node in node["children"]:
                self._parse_node(child_node)
        else:  # process the node if it's a leaf
            self._windows[self._next_window_id] = {"command": node["command"]}
            self._next_window_id += 1

    @property
    def windows(self) -> Dict:
        return self._windows
