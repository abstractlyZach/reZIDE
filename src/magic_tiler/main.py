import logging
import pprint

import click

import magic_tiler
from magic_tiler import dtos
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
    first_window = dtos.WindowDetails(mark="first", command='alacritty -e sh -c "fzf"')
    big = dtos.WindowDetails(mark="big", command='alacritty -e sh -c "kak README.md"')
    gutter = dtos.WindowDetails(
        mark="gutter", command='alacritty -e sh -c "neofetch; zsh -i"'
    )
    swaywm.make_window(first_window)
    swaywm.make_horizontal_sibling(first_window, big)
    swaywm.resize_width(first_window, 25)
    swaywm.make_vertical_sibling(big, gutter)
    swaywm.resize_height(gutter, 33)
    window_sizes = swaywm.get_window_sizes()
    logging.info(pprint.pformat(window_sizes))
