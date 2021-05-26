import pprint

import click

from magic_tiler import sway
from magic_tiler.utils import subprocess_runner


@click.command()
def main() -> None:
    runner = subprocess_runner.SubprocessRunner()
    window_manager = sway.Sway(runner)
    pprint.pprint(window_manager.get_window_sizes())
