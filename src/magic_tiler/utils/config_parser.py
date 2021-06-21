import logging
from typing import Dict

from magic_tiler.utils import interfaces


class ConfigParser(interfaces.ConfigParserInterface):
    """Parses a config file and creates a Tree out of it."""

    def __init__(
        self,
        config_reader: interfaces.ConfigReader,
        tree_factory: interfaces.TreeFactoryInterface,
    ) -> None:
        self._tree_factory = tree_factory
        self._layout_definitions = config_reader.to_dict()

    def get_tree(self, layout_name: str) -> interfaces.TreeNodeInterface:
        """Parse and validate the layout, stitch together the node definitions, and
        create a tree out of them.
        """
        layout_top_definition = self._layout_definitions[layout_name]
        root_node = self._construct_subtree(layout_top_definition)
        return self._tree_factory.create_tree(root_node)

    def _construct_subtree(self, subtree_dict: Dict) -> Dict:
        if "command" in subtree_dict and "mark" in subtree_dict:
            return subtree_dict.copy()
        elif (
            "split" in subtree_dict
            and "children" in subtree_dict
            and "sizes" in subtree_dict
        ):
            if len(subtree_dict["children"]) != len(subtree_dict["sizes"]):
                raise RuntimeError(
                    "The number of children doesn't match the number of sizes"
                )
            subtree = subtree_dict.copy()
            child_subtrees = []
            for child in subtree["children"]:
                if child in self._layout_definitions:
                    child_definition = self._layout_definitions[child]
                else:
                    raise RuntimeError(f'Definition for "{child}" is not available')
                child_subtrees.append(self._construct_subtree(child_definition))
            subtree["children"] = child_subtrees
            return subtree
        else:
            logging.error(subtree_dict)
            raise RuntimeError("Definition is neither a parent or leaf")
