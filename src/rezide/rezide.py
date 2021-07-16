import logging
import sys
from typing import Any, Dict

import click

import rezide
from rezide.utils import config_parser
from rezide.utils import config_readers
from rezide.utils import dtos
from rezide.utils import filestore
from rezide.utils import layouts
from rezide.utils import sway
from rezide.utils import tree

# maps from verbosity level to log levels
VERBOSITY_LOG_LEVELS = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
}


# TODO: is it possible to do a dry-run where we just log info but don't
# open windows or run commands? maybe a fake supbrocess runner?


@click.group()
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
@click.pass_context
@click.version_option(version=rezide.__version__)
def main(
    context: click.Context,
    verbosity_level: int,
    xdg_config_home_dir: str,
    user_home_dir: str,
) -> None:
    """todo: write me"""
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called outside of
    # the python entrypoint)
    context.ensure_object(dict)
    # cast the object to Dict and then ignore the error that tells us we can't
    # cast to Dict. We totally can! We just don't control the `click` source code,
    # so `context.obj` will always be typed as Optional[Any] even if we make sure that
    # it's a Dict :(
    context.obj: Dict[str, Any]  # type: ignore[misc]

    log_level = VERBOSITY_LOG_LEVELS[verbosity_level]
    logging.basicConfig(level=log_level)
    logging.info(f"Log level set to {log_level}")
    sys.tracebacklimit = verbosity_level
    env = dtos.Env(home=user_home_dir, xdg_config_home=xdg_config_home_dir)
    context.obj["config_reader"] = config_readers.TomlReader(
        filestore.LocalFilestore(), env=env
    )
    context.obj["env"] = env


@main.command()
@click.argument("layout_name")
@click.pass_context
def open(context: click.Context, layout_name: str) -> None:
    """Open the IDE of your choice"""
    context.obj: Dict[str, Any]  # type: ignore[misc]
    parser = config_parser.ConfigParser(
        context.obj["config_reader"], tree.TreeFactory()
    )
    window_manager = sway.Sway()
    layout = layouts.LayoutManager(parser, window_manager)
    application = Rezide(context.obj["env"], layout)
    application.run(layout_name)


# I want to handle this with an "eager option", but we wouldn't be able to retrieve the
# context from the environment variables without writing a lot more custom code
# so it makes more sense just to use groups and subcommands
#
# https://click.palletsprojects.com/en/8.0.x/options/?highlight=eager#callbacks-and-eager-options
@main.command()
@click.pass_context
def list_layouts(context: click.Context) -> None:
    """List all available layouts"""
    context.obj: Dict[str, Any]  # type: ignore[misc]
    logging.debug(f'env: {context.obj["env"]}')
    for entry, details in context.obj["config_reader"].read().items():
        if "is_layout" in details:
            click.secho(entry, fg="blue")


class Rezide(object):
    """Manages the application's state and calls the appropriate functions"""

    def __init__(
        self,
        env: dtos.Env,
        layout: layouts.LayoutManager,
    ) -> None:
        self._layout = layout
        logging.debug(f"Env is {env}")

    def run(self, layout_name: str) -> None:
        self._layout.select(layout_name)
        self._layout.spawn_windows()
