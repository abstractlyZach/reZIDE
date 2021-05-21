from typing import Dict

from magic_tiler import interfaces


class Layout(object):
    """Convert a configuration into a collection of Tiles"""

    def __init__(
        self, config_reader: interfaces.ConfigReader, layout_name: str
    ) -> None:
        self._windows: Dict[str, interfaces.WindowDetails] = dict()
        try:
            config = config_reader.to_dict()[layout_name]
        except KeyError:
            raise KeyError(f'Could not find layout "{layout_name}" in config')
        self._parse_config(config)

    def _parse_config(self, layout_dict: Dict) -> None:
        self._parse_node(layout_dict)

    def _parse_node(self, node: Dict) -> None:
        """Recursively process a node and its children using depth-first traversal"""
        if "children" in node:
            for child_node in node["children"]:
                self._parse_node(child_node)
        else:  # process the node if it's a leaf
            mark = node["mark"]
            self._windows[mark] = interfaces.WindowDetails(
                mark=node["mark"], command=node["command"]
            )

    @property
    def windows(self) -> Dict:
        return self._windows
