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
    logging.debug(
        f"{swaywm.num_workspace_windows} windows are open in the current workspace"
    )
    if swaywm.num_workspace_windows > 1:
        raise RuntimeError("There are multiple windows open in the current workspace.")
    swaywm.make_window('alacritty --title "first window"')
    swaywm.make_horizontal_sibling("^first window$", 'alacritty --title "big boy"')
    swaywm.resize_width("first window", 25)
    swaywm.make_horizontal_sibling("^big boy$", 'alacritty --title "side window"')
    swaywm.resize_width("side window", 33)
    window_sizes = swaywm.get_window_sizes()
    logging.info(pprint.pformat(window_sizes))


def woops() -> None:
    """Thowaway function to satisfy testing requirements since this project doesn't have
    any testable functions quite yet"""
    pass
