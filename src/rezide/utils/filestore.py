import os

from rezide.utils import interfaces


class LocalFilestore(interfaces.FileStore):
    def path_exists(self, path: str) -> bool:
        return os.path.exists(path)

    def read_file(self, path: str) -> str:
        with open(path, "r") as infile:
            return infile.read()
