from typing import Dict, List

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
        self._tile_factory: interfaces.TileFactoryInterface = tile_factory
        self._tiles: List[dtos.Tile] = []
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
            new_tile = self._tile_factory.make_tile(
                0, 0, dtos.WindowDetails(mark=node["mark"], command=node["command"])
            )
            self._tiles.append(new_tile)

    @property
    def tiles(self) -> List[dtos.Tile]:
        return self._tiles
