import logging

import click

import magic_tiler
from magic_tiler.utils import config_parser
from magic_tiler.utils import configs
from magic_tiler.utils import dtos
from magic_tiler.utils import filestore
from magic_tiler.utils import layouts
from magic_tiler.utils import sway
from magic_tiler.utils import tree

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
@click.option(
    "-c",
    "--xdg-config-home-dir",
    envvar="XDG_CONFIG_HOME",
    help="The directory for your XDG config files. Reads from the XDG_CONFIG_HOME"
    + " environment variable by default.",
)
@click.option(
    "--user-home-dir",
    envvar="HOME",
    help="The current user's home directory. Reads from the HOME environment variable"
    + " by default.",
)
@click.argument("layout_name")
@click.version_option(version=magic_tiler.__version__)
def main(
    verbosity_level: int, xdg_config_home_dir: str, user_home_dir: str, layout_name: str
) -> None:
    """Create the IDE registered at LAYOUT_NAME in the configuration file."""
    log_level = VERBOSITY_LOG_LEVELS[verbosity_level]
    logging.basicConfig(level=log_level)
    logging.info(f"Log level set to {log_level}")
    env = dtos.Env(home=user_home_dir, xdg_config_home=xdg_config_home_dir)
    config_reader = configs.TomlConfig(filestore.LocalFilestore(), env=env)
    parser = config_parser.ConfigParser(config_reader, tree.TreeFactory())
    window_manager = sway.Sway()
    layout = layouts.LayoutManager(parser, window_manager)
    application = MagicTiler(env, layout, verbosity_level)
    application.run(layout_name)


class MagicTiler(object):
    """Manages the application's state and calls the appropriate functions"""

    def __init__(
        self,
        env: dtos.Env,
        layout: layouts.LayoutManager,
        verbosity_level: int,
    ) -> None:
        self._layout = layout
        logging.debug(f"Env is {env}")

    def run(self, layout_name: str) -> None:
        self._layout.select(layout_name)
        self._layout.spawn_windows()
