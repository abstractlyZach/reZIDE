import os
from typing import List

from rezide.utils import interfaces


class LocalFilestore(interfaces.FileStore):
    def path_exists(self, path: str) -> bool:
        return os.path.exists(path)

    def read_file(self, path: str) -> str:
        with open(path, "r") as infile:
            return infile.read()

    def exists_as_dir(self, path: str) -> bool:
        return self.path_exists(path) and os.path.isdir(path)

    def exists_as_file(self, path: str) -> bool:
        return self.path_exists(path) and os.path.isfile(path)

    def list_directory_contents(self, path: str) -> List[str]:
        if self.exists_as_dir(path):
            return os.listdir(path)
        raise RuntimeError(f"{path} is not a valid directory")
