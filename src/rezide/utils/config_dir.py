import os
from typing import Optional, Set

from rezide.utils import dtos
from rezide.utils import interfaces


class ConfigDir(interfaces.ConfigDir):
    def __init__(
        self,
        filestore: interfaces.FileStore,
        env: dtos.Env,
        specified_dir: Optional[str],
    ) -> None:
        self._filestore = filestore
        if specified_dir:  # and filestore.path_exists(specified_dir):
            self._dir = specified_dir
        else:
            raise Exception("woops")

    def list_layouts(self) -> Set[str]:
        files_in_directory = self._filestore.list_directory_contents(self._dir)
        filenames_without_extensions = {
            os.path.splitext(filename)[0] for filename in files_in_directory
        }
        return filenames_without_extensions

    def get_layout_file_path(self, layout_name: str) -> str:
        pass
