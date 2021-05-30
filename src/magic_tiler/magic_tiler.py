import logging
import pprint

import click

import magic_tiler
from magic_tiler.utils import layout
from magic_tiler.utils import sway
from magic_tiler.utils import toml_config

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
    log_level = VERBOSITY_LOG_LEVELS[verbosity_level]
    logging.basicConfig(level=log_level)
    logging.info(f"Log level set to {log_level}")
    window_manager = sway.Sway()
    logging.debug(
        f"{window_manager.num_workspace_windows} windows are open in the current workspace"
    )
    if window_manager.num_workspace_windows > 1:
        raise RuntimeError("There are multiple windows open in the current workspace.")

    config = toml_config.TomlConfig("examples/centered_big.toml")
    pprint.pprint(config.to_dict())
    layout.Layout(config, "screen", window_manager)
