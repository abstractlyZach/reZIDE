import logging
import os
from typing import Optional, Set

from rezide.utils import dtos
from rezide.utils import interfaces


class ConfigDir(interfaces.ConfigDir):
    def __init__(
        self,
        filestore: interfaces.FileStore,
        env: dtos.Env,
        specified_dir: Optional[str] = None,
    ) -> None:
        self._filestore = filestore
        xdg_config_dir = os.path.join(env.xdg_config_home + "rezide")
        home_config_dir = os.path.join(env.home + ".rezide")
        if specified_dir:
            if not filestore.exists_as_dir(specified_dir):
                raise RuntimeError(f"{specified_dir} does not exist")
            self._dir = specified_dir
        elif filestore.exists_as_dir(xdg_config_dir):
            self._dir = xdg_config_dir
        elif filestore.exists_as_dir(home_config_dir):
            self._dir = home_config_dir
        else:
            raise RuntimeError(
                f"Failed to find config dir at {env.xdg_config_home} and {home_config_dir}"
            )
        logging.info(f"reading from '{self._dir}' as config dir")

    def list_layouts(self) -> Set[str]:
        files_in_directory = self._filestore.list_directory_contents(self._dir)
        filenames_without_extensions = {
            os.path.splitext(filename)[0] for filename in files_in_directory
        }
        return filenames_without_extensions

    def get_layout_file_path(self, layout_name: str) -> str:
        pass
