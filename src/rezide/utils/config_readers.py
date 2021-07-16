import logging
import os
from typing import Dict

import toml

from rezide.utils import dtos
from rezide.utils import interfaces


class TomlReader(interfaces.ConfigReader):
    def __init__(self, filestore: interfaces.FileStore, env: dtos.Env) -> None:
        paths_to_check = []
        if env.xdg_config_home:
            path = os.path.join(env.xdg_config_home, "rezide", "config.toml")
            paths_to_check.append(path)
        else:
            path = os.path.join(env.home, ".rezide.toml")
            paths_to_check.append(path)
        for path in paths_to_check:
            logging.debug(f"checking {path}")
            if filestore.path_exists(path):
                target_path = path
                logging.debug(f"found config at {path}")
                break
        else:
            raise RuntimeError(
                'Could not find config file at "$XDG_CONFIG_HOME/rezide/config.toml"'
                + 'or "$HOME/.rezide.toml"'
            )
        toml_str = filestore.read_file(target_path)
        self._dict = dict(toml.loads(toml_str))

    def read(self) -> Dict:
        return self._dict
