import logging
import pprint

import click

import magic_tiler
from magic_tiler import interfaces
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
    first_window = interfaces.WindowDetails(
        mark="first", command='alacritty --title "first window"'
    )
    big = interfaces.WindowDetails(mark="big", command='alacritty --title "big boy"')
    side_window = interfaces.WindowDetails(
        mark="side", command='alacritty --title "side window"'
    )
    swaywm.make_window(first_window)
    swaywm.make_horizontal_sibling(first_window, big)
    swaywm.resize_width(first_window, 25)
    swaywm.make_horizontal_sibling(big, side_window)
    swaywm.resize_width(side_window, 33)
    window_sizes = swaywm.get_window_sizes()
    logging.info(pprint.pformat(window_sizes))


def woops() -> None:
    """Thowaway function to satisfy testing requirements since this project doesn't have
    any testable functions quite yet"""
    pass
