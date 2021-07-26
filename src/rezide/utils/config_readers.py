from typing import Dict

import toml

from rezide.utils import interfaces


class TomlReader(interfaces.ConfigReader):
    def __init__(self, filestore: interfaces.FileStore) -> None:
        self._filestore = filestore

    def read(self, path: str) -> Dict:
        """Convert a TOML file at `path` to a python Dict"""
        toml_str = self._filestore.read_file(path)
        return dict(toml.loads(toml_str))
