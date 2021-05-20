from typing import Dict

import toml

from magic_tiler import interfaces


class TomlConfig(interfaces.ConfigReader):
    def __init__(self, filename: str) -> None:
        with open(filename, "r") as infile:
            self._dict = dict(toml.load(infile))

    def to_dict(self) -> Dict:
        return self._dict
