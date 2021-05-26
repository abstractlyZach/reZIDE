import logging
import pprint

import click

import magic_tiler
from magic_tiler.utils import dtos
from magic_tiler.utils import subprocess_runner
from magic_tiler.utils import sway

# maps from verbosity level to log levels
VERBOSITY_LOG_LEVELS = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
}


# TODO: is it possible to do a dry-run where we just log info but don't
# open windows or run commands? maybe a fake supbrocess runner?


@click.command()
@click.option(
    "-v",
    "--verbose",
    "verbosity_level",
    default=0,
    count=True,
    help="Set verbosity. Add more v's to increase verbosity. For example, -v is "
    + "verbosity level 1 and -vv is verbosity level 2",
)
@click.version_option(version=magic_tiler.__version__)
def main(verbosity_level: int) -> None:
    logging.basicConfig(level=VERBOSITY_LOG_LEVELS[verbosity_level])
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
