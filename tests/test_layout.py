from magic_tiler import interfaces
from magic_tiler import layout


class FakeConfig(interfaces.ConfigReader):
    def to_dict(self):
        return {
            "screen": [
                {
                    "children": [
                        {"size": 60, "command": "alacritty --title medium-window"},
                        {"size": 40, "command": "alacritty --title tiny-window"},
                    ],
                    "split": "vertical",
                    "size": 25,
                },
                {"size": 50, "command": "alacritty --title middle-panel"},
                {"size": 25, "command": "alacritty --title right-panel"},
            ],
            "split": "horizontal",
        }


def test_layout():
    mylayout = layout.Layout(FakeConfig())
    # can we assign them window ids?
    assert mylayout.windows == {
        0: {"command": "alacritty --title medium-window"},
        1: {"command": "alacritty --title tiny-window"},
        2: {"command": "alacritty --title middle-panel"},
        3: {"command": "alacritty --title right-panel"},
    }
