import pprint

import click

from magic_tiler import subprocess_runner
from magic_tiler import sway


@click.command()
def main() -> None:
    runner = subprocess_runner.SubprocessRunner()
    window_manager = sway.Sway(runner)
    pprint.pprint(window_manager.get_window_sizes())
