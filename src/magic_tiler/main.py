import logging
import pprint

import click

import magic_tiler
from magic_tiler import subprocess_runner
from magic_tiler import sway


@click.command()
@click.version_option(version=magic_tiler.__version__)
def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    swaywm = sway.Sway(subprocess_runner.SubprocessRunner())
    # swaywm.make_horizontal_sibling("Alacritty:v", 'alacritty -e sh -c "ls | fzf"')
    # how do we make alacritty hang around after running the initial command?
    # swaywm.make_horizontal_sibling("Alacritty:poetry", 'alacritty -e zsh -c "ls"')
    logging.debug(
        f"{swaywm.num_workspace_windows} windows are open in the current workspace"
    )
    if swaywm.num_workspace_windows > 1:
        raise RuntimeError("There are multiple windows open in the current workspace.")
    swaywm.make_window('alacritty --title "first window"')
    swaywm.make_horizontal_sibling(
        "^first window$", 'alacritty --title "second window"'
    )
    swaywm.make_vertical_sibling("^second window$", 'alacritty --title "small window"')
    swaywm.make_vertical_sibling(
        "^first window$", 'alacritty --title "another small window"'
    )
    swaywm.make_horizontal_sibling(
        "^first window$", 'alacritty --title "yet another small window"'
    )
    swaywm.resize_width("first window", 70)
    swaywm.resize_width("second window", 75)
    swaywm.resize_height("yet another small window", 40)
    window_sizes = swaywm.get_window_sizes()
    logging.info(pprint.pformat(window_sizes))


def woops() -> None:
    """Thowaway function to satisfy testing requirements since this project doesn't have
    any testable functions quite yet"""
    pass
