import pprint

import click

from magic_tiler.utils import interfaces
from magic_tiler.utils import sway


@click.command()
def main() -> None:
    window_manager = sway.Sway()
    print_window_sizes(window_manager)


def print_window_sizes(window_manager: interfaces.TilingWindowManager) -> None:
    pprint.pprint(window_manager.get_window_sizes())
