import logging
import os
from typing import Optional, Set

from rezide.utils import dtos
from rezide.utils import interfaces


class ConfigDir(interfaces.ConfigDir):
    """Finds and exposes operations for a rezide configuration directory"""

    def __init__(
        self,
        filestore: interfaces.FileStore,
        env: dtos.Env,
        specified_dir: Optional[str] = None,
    ) -> None:
        self._filestore = filestore
        self._select_config_dir(env, specified_dir)

    def _select_config_dir(self, env: dtos.Env, specified_dir: Optional[str]) -> None:
        """Search through options for configuration directories in this order:
        1. directory that has been manually specified by the user
        2. $XDG_CONFIG_HOME/rezide
        3. $HOME/.rezide
        """
        xdg_config_dir = os.path.join(env.xdg_config_home, "rezide")
        home_config_dir = os.path.join(env.home, ".rezide")

        if specified_dir:
            if not self._filestore.exists_as_dir(specified_dir):
                raise RuntimeError(f"{specified_dir} does not exist")
            self._dir = specified_dir
        elif self._filestore.exists_as_dir(xdg_config_dir):
            self._dir = xdg_config_dir
        elif self._filestore.exists_as_dir(home_config_dir):
            self._dir = home_config_dir
        else:
            raise RuntimeError(
                f"Failed to find config dir. looked in '{xdg_config_dir}' and"
                + f" '{home_config_dir}'"
            )
        logging.info(f"reading from '{self._dir}' as config dir")

    def list_layouts(self) -> Set[str]:
        """List all available layouts in the config directory"""
        logging.info(f"listing layouts in {self._dir}")
        layouts = set()
        for file_or_dir in self._filestore.list_directory_contents(self._dir):
            logging.debug(f"examining {file_or_dir} to see if it has a config")
            absolute_path_to_dir = os.path.join(self._dir, file_or_dir)
            absolute_path_to_config_file = os.path.join(
                absolute_path_to_dir, "config.toml"
            )
            is_dir = self._filestore.exists_as_dir(absolute_path_to_dir)
            has_config_file = self._filestore.exists_as_file(
                absolute_path_to_config_file
            )
            if is_dir and has_config_file:
                layouts.add(file_or_dir)
        return layouts

    def get_layout_file_path(self, layout_name: str) -> str:
        """Given a name of a layout, check for a matching toml file in the config directory
        and return its absolute file path if it exists
        """
        file_path = os.path.join(self._dir, layout_name + ".toml")
        if not self._filestore.exists_as_file(file_path):
            raise RuntimeError(f"Layout '{layout_name}' doesn't exist in '{self._dir}'")
        return file_path
