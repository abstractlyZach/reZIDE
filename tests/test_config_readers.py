import pytest

from rezide.utils import config_readers
from tests import fakes


@pytest.fixture
def MockTomlLibrary(mocker):
    return mocker.patch("rezide.utils.config_readers.toml")


toml_contents = """
[screen]
split = "horizontal"
children = ['left', 'middle', 'right']
sizes = [25, 50, 25]

[left]
split = "vertical"
children = ['medium window', 'tiny window']
sizes = [60, 40]

['medium window']
command = "alacritty --title medium-window -e sh -c 'cowsay $(fortune); zsh -i'"
mark = "medium-window"

['tiny window']
command = "alacritty --title tiny-window -e sh -c 'neofetch; zsh'"
mark = "tiny-window"

[middle]
command = "alacritty --title middle-panel -e sh -c 'kak ~/internet.txt'"
mark = "middle-panel"

[right]
command = "alacritty --title right-panel -e sh -c 'broot'"
mark = "right-panel"
"""

expected_toml_dict = {
    "screen": {
        "children": ["left", "middle", "right"],
        "split": "horizontal",
        "sizes": [25, 50, 25],
    },
    "left": {
        "children": ["medium window", "tiny window"],
        "split": "vertical",
        "sizes": [60, 40],
    },
    "tiny window": {
        "command": "alacritty --title tiny-window -e sh -c 'neofetch; zsh'",
        "mark": "tiny-window",
    },
    "medium window": {
        "command": "alacritty --title medium-window -e sh -c 'cowsay $(fortune); zsh -i'",
        "mark": "medium-window",
    },
    "middle": {
        "command": "alacritty --title middle-panel -e sh -c 'kak ~/internet.txt'",
        "mark": "middle-panel",
    },
    "right": {
        "command": "alacritty --title right-panel -e sh -c 'broot'",
        "mark": "right-panel",
    },
}


def test_toml_integration():
    config_reader = config_readers.TomlReader(
        fakes.FakeFilestore(files={"any": toml_contents}),
    )
    assert (
        config_reader.read("/home/test/.config/rezide/abc/config.toml")
        == expected_toml_dict
    )


def test_toml_reader_makes_correct_call(MockTomlLibrary):
    config_reader = config_readers.TomlReader(
        fakes.FakeFilestore(files={"any": toml_contents}),
    )
    config_reader.read("abclkajsdlfkasjdlfkj")
    MockTomlLibrary.loads.assert_called_once_with(toml_contents)
