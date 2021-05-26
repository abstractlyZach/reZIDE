import pprint

import click

from magic_tiler.utils import sway


@click.command()
def main() -> None:
    window_manager = sway.Sway()
    pprint.pprint(window_manager.get_window_sizes())
