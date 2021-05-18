import logging
import time

import i3ipc

from magic_tiler import interfaces  # pragma: nocover

"""We need to sleep for a short time since processes take time to start.
If we don't sleep, then we may be focusing on a different window by the
time that the current window is spawning, which would put it in the wrong
split.
"""
SLEEP_TIME = 0.25


class Sway(interfaces.TilingWindowManager):  # pragma: nocover
    def __init__(self, runner: interfaces.Runner) -> None:
        self._sway = i3ipc.Connection()
        self._runner = runner

    def make_horizontal_sibling(self, window_title_regex: str, command: str) -> None:
        self._focus_window(window_title_regex)
        self._runner.run_and_disown(command)
        time.sleep(0.25)

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
