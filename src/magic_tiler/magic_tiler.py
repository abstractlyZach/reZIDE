import logging

import click

import magic_tiler
from magic_tiler.utils import configs
from magic_tiler.utils import dtos
from magic_tiler.utils import filestore
from magic_tiler.utils import interfaces
from magic_tiler.utils import layouts
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
@click.option("-c", "--xdg-config-home-dir", envvar="XDG_CONFIG_HOME")
@click.option("--user-home-dir", envvar="HOME")
@click.argument("layout_name")
@click.version_option(version=magic_tiler.__version__)
def main(
    verbosity_level: int, xdg_config_home_dir: str, user_home_dir: str, layout_name: str
) -> None:
    env = dtos.Env(home=user_home_dir, xdg_config_home=xdg_config_home_dir)
    config = configs.TomlConfig(filestore.LocalFilestore(), env=env)
    window_manager = sway.Sway()
    application = MagicTiler(env, window_manager, config, verbosity_level)
    application.run(layout_name)


class MagicTiler(object):
    """Manages the application's state and calls the appropriate functions"""

    def __init__(
        self,
        env: dtos.Env,
        window_manager: interfaces.TilingWindowManager,
        config: interfaces.ConfigReader,
        verbosity_level: int,
    ) -> None:
        self._window_manager = window_manager
        self._layout = layouts.Layout(config, window_manager)
        log_level = VERBOSITY_LOG_LEVELS[verbosity_level]
        logging.basicConfig(level=log_level)
        logging.info(f"Log level set to {log_level}")
        logging.debug(f"Env is {env}")

    def run(self, layout_name: str) -> None:
        logging.debug(
            f"{self._window_manager.num_workspace_windows} windows"
            + " are open in the current workspace"
        )
        if self._window_manager.num_workspace_windows > 1:
            raise RuntimeError(
                "There are multiple windows open in the current workspace."
            )
        self._layout.spawn_windows(layout_name)
