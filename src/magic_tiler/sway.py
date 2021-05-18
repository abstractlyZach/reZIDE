import logging
import shlex
import subprocess  # noqa: S404

import i3ipc

from magic_tiler import interfaces  # pragma: nocover


class Sway(interfaces.TilingWindowManager):  # pragma: nocover
    def __init__(self) -> None:
        self._sway = i3ipc.Connection()

    def make_horizontal_sibling(self, window_title_regex: str, command: str) -> None:
        pass

    def make_vertical_sibling(self, window_title_regex: str, command: str) -> None:
        pass

    def resize_width(self, window_title_regex: str, container_percentage: int) -> None:
        pass

    def resize_height(self, window_title_regex: str, container_percentage: int) -> None:
        pass

    def _focus_window(self, window_title_regex: str) -> None:
        tree = self._sway.get_tree()
        windows = tree.find_named(window_title_regex)
        logging.debug(f"windows are {windows}")
        if len(windows) > 1:
            raise RuntimeError(
                f'There is more than 1 window that matches the regex "{window_title_regex}"'
            )
        if len(windows) < 1:
            raise RuntimeError(
                f'There are no windows that matches the regex "{window_title_regex}"'
            )
        windows[0].command("focus")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    a = Sway()
    a._focus_window("Alacritty:v")
    args = shlex.split("alacritty -e sh -c zsh")
    logging.info(f"Running command: {args}")
    subprocess.Popen(args)  # noqa: S603
