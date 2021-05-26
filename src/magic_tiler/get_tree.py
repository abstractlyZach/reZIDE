import click
import i3ipc


@click.command()
def main() -> None:
    i3 = i3ipc.Connection()
    current_workspace = i3.get_tree().find_focused().workspace()
    for node in current_workspace.descendants():
        print(node.name)
        print(f"x, y: ({node.rect.x}, {node.rect.y})")
        print(f"width, height: ({node.rect.width}, {node.rect.height})")
        print(f"gaps: {node.gaps}")
        print()
