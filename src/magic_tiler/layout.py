from typing import Dict

from magic_tiler import interfaces


class Layout(object):
    def __init__(self, config: interfaces.ConfigReader) -> None:
        pass

    @property
    def windows(self) -> Dict:
        return {
            0: {"command": "alacritty --title medium-window"},
            1: {"command": "alacritty --title tiny-window"},
            2: {"command": "alacritty --title middle-panel"},
            3: {"command": "alacritty --title right-panel"},
        }
