import logging
from typing import Dict, Set

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

    def validate(self) -> None:
        seen_marks: Set[str] = set()
        for definition_name, definition_body in self._layout_definitions.items():
            if "command" in definition_body and "mark" in definition_body:
                if definition_body["mark"] in seen_marks:
                    raise RuntimeError(
                        f"There are multiple windows with mark \"{definition_body['mark']}\""
                    )
                self._validate_window(definition_name, definition_body)
                seen_marks.add(definition_body["mark"])
            elif (
                "split" in definition_body
                and "children" in definition_body
                and "sizes" in definition_body
            ):
                self._validate_container(definition_name, definition_body)
            else:
                logging.error(definition_body)
                raise RuntimeError("This definition is not a Window or Container")

    def _validate_window(self, definition_name: str, definition_body: Dict) -> None:
        if len(definition_body) != 2:
            raise RuntimeError("Window must only define command and mark")

    def _validate_container(self, definition_name: str, definition_body: Dict) -> None:
        if len(definition_body) != 3:
            raise RuntimeError("Container must only define split, children, and sizes")
        for child in definition_body["children"]:
            if child not in self._layout_definitions:
                raise RuntimeError(
                    f"{child} is a child of {definition_name} but is not defined"
                )
        if len(definition_body["children"]) < 2:
            raise RuntimeError(f"{definition_name} has less than 2 children")
        if len(definition_body["children"]) != len(definition_body["sizes"]):
            raise RuntimeError(
                "The number of children to not match the number of sizes in"
                + f" {definition_name}"
            )

    def get_tree(self, layout_name: str) -> interfaces.TreeNodeInterface:
        """Parse and validate the layout, stitch together the node definitions, and
        create a tree out of them.
        """
        layout_top_definition = self._layout_definitions[layout_name]
        root_node = self._construct_subtree(layout_top_definition)
        return self._tree_factory.create_tree(root_node)

    def _construct_subtree(self, subtree_dict: Dict) -> Dict:
        if "mark" in subtree_dict:
            return subtree_dict.copy()
        else:
            subtree = subtree_dict.copy()
            child_subtrees = []
            for child in subtree["children"]:
                child_definition = self._layout_definitions[child]
                child_subtrees.append(self._construct_subtree(child_definition))
            subtree["children"] = child_subtrees
            return subtree
