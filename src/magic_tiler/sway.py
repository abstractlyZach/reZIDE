import logging
import time
from typing import Dict, List

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
        window = self._get_window(window_title_regex)
        window.command("focus")
        window.command("split horizontal")
        self.make_window(command)

    def make_vertical_sibling(self, window_title_regex: str, command: str) -> None:
        window = self._get_window(window_title_regex)
        window.command("focus")
        window.command("split vertical")
        self.make_window(command)

    def make_window(self, command: str) -> None:
        self._runner.run_and_disown(command)
        time.sleep(0.25)

    def resize_width(self, window_title_regex: str, container_percentage: int) -> None:
        window = self._get_window(window_title_regex)
        window.command("focus")
        logging.debug(f"current window percentage is {window.percent}")

    def resize_height(self, window_title_regex: str, container_percentage: int) -> None:
        pass

    def get_window_sizes(self) -> Dict[str, Dict[str, float]]:
        return {
            window.name: {
                "width": window.window_rect.width,
                "height": window.window_rect.height,
            }
            for window in self._get_windows_in_current_workspace()
        }

    def _get_window(self, window_title_regex: str) -> i3ipc.Con:
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
        return windows[0]

    def _get_windows_in_current_workspace(self) -> List[i3ipc.Con]:
        workspaces = self._sway.get_workspaces()
        for workspace in workspaces:
            if workspace.focused:
                if workspace.num == -1:
                    raise RuntimeError("The current workspace is a named workspace")
                current_workspace_num = workspace.num
                break
        else:
            raise RuntimeError("There is no current workspace")
        windows_in_current_workspace = []
        for container in self._sway.get_tree().leaves():
            logging.debug(
                f'"{container.name}" is in workspace {container.workspace().num}'
            )
            if container.workspace().num == current_workspace_num:
                windows_in_current_workspace.append(container)
        return windows_in_current_workspace

    @property
    def num_workspace_windows(self) -> int:
        """Get the number of windows open on the current workspace

        The current workspace must not be a "named workspace"
        https://i3ipc-python.readthedocs.io/en/latest/replies.html#i3ipc.WorkspaceReply
        """
        return len(self._get_windows_in_current_workspace())
