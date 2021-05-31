import os
from typing import Dict

import toml

from magic_tiler.utils import dtos
from magic_tiler.utils import interfaces


class TomlConfig(interfaces.ConfigReader):
    def __init__(self, filestore: interfaces.FileStore, env: dtos.Env) -> None:
        if env.xdg_config_home:
            target_path = os.path.join(
                env.xdg_config_home, "magic_tiler", "config.toml"
            )
        else:
            target_path = os.path.join(env.home, ".magic_tiler.toml")
        if not filestore.path_exists(target_path):
            raise RuntimeError(
                'Could not find config file at "$XDG_CONFIG_HOME/magic_tiler/config.toml"'
                + 'or "$HOME/.magic_tiler.toml"'
            )
        toml_str = filestore.read_file(target_path)
        self._dict = dict(toml.loads(toml_str))

    def to_dict(self) -> Dict:
        return self._dict


# class Config(object):
#     def __init__(
#         self,
#         config_reader: interfaces.ConfigReader,
#         tree_factory: interfaces.TreeFactoryInterface,
#         xdg_base_dir: Optional[str] = None,
#     ) -> None:
#         self._tree_factory = tree_factory
#         self._config_reader = config_reader

#     def get_tree(self, layout_name: str) -> tree.TreeNode:
#         config = self._config_reader.to_dict()
#         layout = config[layout_name]
#         return self._tree_factory.build_tree(layout)
