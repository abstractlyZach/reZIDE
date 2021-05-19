from typing import Dict

import toml

from magic_tiler import interfaces


class TomlConfig(interfaces.ConfigReader):
    def read(self, filename: str) -> Dict:
        with open(filename, "r") as infile:
            return dict(toml.load(infile))
