from typing import Dict

from magic_tiler import dtos
from magic_tiler import interfaces


class Layout(object):
    """Convert a configuration into a collection of Tiles"""

    def __init__(
        self,
        config_reader: interfaces.ConfigReader,
        layout_name: str,
        tile_factory: interfaces.TileFactoryInterface,
    ) -> None:
        self._windows: Dict[str, dtos.WindowDetails] = dict()
        try:
            root_node = config_reader.to_dict()[layout_name]
        except KeyError:
            raise KeyError(f'Could not find layout "{layout_name}" in config')
        self._parse_node(root_node)

    def _parse_node(self, node: Dict) -> None:
        """Recursively process a node and its children using depth-first traversal"""
        if "children" in node:
            for child_node in node["children"]:
                self._parse_node(child_node)
        else:  # process the node if it's a leaf
            mark = node["mark"]
            self._windows[mark] = dtos.WindowDetails(
                mark=node["mark"], command=node["command"]
            )

    @property
    def windows(self) -> Dict:
        return self._windows
