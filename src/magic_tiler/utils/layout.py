import collections
import logging
import pprint
from typing import Dict, List, NamedTuple

from magic_tiler import dtos
from magic_tiler.utils import interfaces


class Node(NamedTuple):
    node: Dict
    parent_relative_width: float
    parent_relative_height: float
    parent_split_orientation: str


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
        logging.debug(pprint.pformat(root_node))
        if "size" in root_node:
            raise RuntimeError("root node shouldn't have a size. size is implied 100")
        root_node["size"] = 100
        self._parse_tree(root_node)

    def _parse_tree(self, root_node: Dict) -> None:
        """Process a node and its children using breadth-first traversal"""
        node_queue = collections.deque(
            [
                Node(
                    node=root_node,
                    parent_relative_width=1.0,
                    parent_relative_height=1.0,
                    parent_split_orientation=root_node["split"],
                )
            ]
        )
        while len(node_queue) > 0:
            current_node = node_queue.popleft()
            if current_node.parent_split_orientation == "vertical":
                relative_height = (
                    current_node.parent_relative_height
                    * current_node.node["size"]
                    / 100
                )
                relative_width = current_node.parent_relative_width
            elif current_node.parent_split_orientation == "horizontal":
                relative_height = current_node.parent_relative_height
                relative_width = (
                    current_node.parent_relative_width * current_node.node["size"] / 100
                )
            else:
                raise RuntimeError("not a valid split orientation!")
            if "children" in current_node.node:
                for child_dict in current_node.node["children"]:
                    node_queue.append(
                        Node(
                            node=child_dict,
                            parent_relative_width=relative_width,
                            parent_relative_height=relative_height,
                            parent_split_orientation=current_node.node["split"],
                        )
                    )
            else:  # process the node if it's a leaf
                logging.debug(current_node.node)
                new_tile = self._tile_factory.make_tile(
                    relative_width,
                    relative_height,
                    dtos.WindowDetails(
                        mark=current_node.node["mark"],
                        command=current_node.node["command"],
                    ),
                )
                self._tiles.append(new_tile)

    @property
    def tiles(self) -> List[dtos.Tile]:
        return self._tiles
