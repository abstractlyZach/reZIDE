import logging
import time
from typing import Dict, List, Tuple

import i3ipc

from magic_tiler.utils import dtos
from magic_tiler.utils import interfaces

"""We need to sleep for a short time since processes take time to start.
If we don't sleep, then we may be focusing on a different window by the
time that the current window is spawning, which would put it in the wrong
split.
"""
SLEEP_TIME = 0.30


class Sway(interfaces.TilingWindowManager):  # pragma: nocover
    def __init__(self) -> None:
        self._sway = i3ipc.Connection()

    def make_horizontal_sibling(
        self,
        target_window: dtos.WindowDetails,
        new_window: dtos.WindowDetails,
    ) -> None:
        window = self._get_window(target_window.mark)
        window.command("focus")
        window.command("split horizontal")
        self.make_window(new_window)

    def make_vertical_sibling(
        self,
        target_window: dtos.WindowDetails,
        new_window: dtos.WindowDetails,
    ) -> None:
        window = self._get_window(target_window.mark)
        window.command("focus")
        window.command("split vertical")
        self.make_window(new_window)

    def make_window(self, window_details: dtos.WindowDetails) -> None:
        """Create a window, sleep to let it start up, then mark it"""
        self._sway.command(f"exec {window_details.command}")
        time.sleep(SLEEP_TIME)
        self._get_focused_window().command(f"mark {window_details.mark}")

    def resize_width(
        self, target_window: dtos.WindowDetails, container_percentage: int
    ) -> None:
        window = self._get_window(target_window.mark)
        window.command("focus")
        window.command(f"resize set width {container_percentage} ppt")

    def resize_height(
        self, target_window: dtos.WindowDetails, container_percentage: int
    ) -> None:
        window = self._get_window(target_window.mark)
        window.command("focus")
        window.command(f"resize set height {container_percentage} ppt")

    def get_window_sizes(self) -> Dict[Tuple, Dict[str, float]]:
        return {
            tuple(window.marks): {
                "width": window.window_rect.width,
                "height": window.window_rect.height,
            }
            for window in self._get_windows_in_current_workspace()
        }

    def _get_focused_window(self) -> i3ipc.Con:
        tree = self._sway.get_tree()
        focused = tree.find_focused()
        if not focused:
            raise RuntimeError("There is no focused window")
        return focused

    def _get_window(self, mark: str) -> i3ipc.Con:
        tree = self._sway.get_tree()
        windows = tree.find_marked(mark)
        logging.debug(f'searching for mark "{mark}"')
        logging.debug(f"windows are {windows}")
        if len(windows) > 1:
            raise RuntimeError(
                f'There is more than 1 window that matches the regex "{mark}"'
            )
        if len(windows) < 1:
            raise RuntimeError(f'There are no windows that matches the regex "{mark}"')
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
                f'"{container.name}" is in workspace {container.workspace().num} with '
                + f'marks "{container.marks}"'
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
