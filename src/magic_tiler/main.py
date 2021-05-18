import logging

import click

import magic_tiler
from magic_tiler import subprocess_runner
from magic_tiler import sway


@click.command()
@click.version_option(version=magic_tiler.__version__)
def main() -> None:
    logging.basicConfig(level=logging.INFO)
    swaywm = sway.Sway(subprocess_runner.SubprocessRunner())
    swaywm.make_horizontal_sibling("Alacritty:v", 'alacritty -e sh -c "ls | fzf"')
    # how do we make alacritty hang around after running the initial command?
    swaywm.make_horizontal_sibling("Alacritty:poetry", 'alacritty -e zsh -c "ls"')


def woops() -> None:
    """Thowaway function to satisfy testing requirements since this project doesn't have
    any testable functions quite yet"""
    pass
