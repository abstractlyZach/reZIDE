import click

from rezide.utils import interfaces
from rezide.utils import sway


def print_tree(window_manager: interfaces.TilingWindowManager) -> None:
    for node in window_manager.get_tree():
        click.echo(click.style(node.name, fg="green", bold=True))
        click.echo(f"x, y: ({node.rect.x}, {node.rect.y})")
        click.echo(f"width, height: ({node.rect.width}, {node.rect.height})")
        click.echo(f"gaps: {node.gaps}")
        click.echo("marks: ", nl=False)
        click.echo(click.style(f"{node.marks}", fg="cyan"))
        click.echo()


@click.command()
def main() -> None:
    window_manager = sway.Sway()
    print_tree(window_manager)
