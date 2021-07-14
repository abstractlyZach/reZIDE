import logging
import time
from typing import Dict, List, Tuple

import i3ipc

from rezide.utils import dtos
from rezide.utils import interfaces

"""We need to sleep for a short time since processes take time to start.
If we don't sleep, then we may be focusing on a different window by the
time that the current window is spawning, which would put it in the wrong
split.
"""

# WINDOW_MARK_EVENT = i3ipc.Event.WINDOW_MARK
# WINDOW_FOCUS_EVENT = i3ipc.Event.WINDOW_FOCUS
NEW_WINDOW_EVENT = i3ipc.Event.WINDOW_NEW

# marking and focusing are such quick actions that we can't just fire and wait.
# python isn't fast enough to catch up to them!
# TODO: set up something to expect an event and wait instead of manually waiting
MARK_SLEEP_TIME = 0
FOCUS_SLEEP_TIME = 0

# there doesn't seem to be either of these events
RESIZE_SLEEP_TIME = 0.25
SPLIT_SLEEP_TIME = 0.25

# TODO: add logging for commands


class Sway(interfaces.TilingWindowManager):
    def __init__(self) -> None:
        self._sway = i3ipc.Connection()

    def sleep_until_event(self, event: i3ipc.events.IpcBaseEvent) -> None:
        """Sleep until a certain IPC event is detected"""

        def wake_up(
            connection: i3ipc.connection.Connection, event: i3ipc.events.IpcBaseEvent
        ) -> None:
            """Callback function that ends the sleep"""
            logging.debug(f"detected {event.change} event")
            connection.main_quit()

        # set up the wakeup callback
        self._sway.on(event, wake_up)
        logging.debug(f"waiting for {event} event")
        # start the main loop, effectively sleeping until the wakeup callback is triggered
        self._sway.main()
        # unsubscribe the handler so we don't have anything hanging around
        self._sway.off(wake_up)

    def make_window(self, window_details: dtos.WindowDetails) -> None:
        """Create a window then mark it"""
        logging.debug(f"creating window with command {window_details.command}")
        self._sway.command(f"exec {window_details.command}")
        self.sleep_until_event(NEW_WINDOW_EVENT)
        logging.debug(f"marking window with mark {window_details.mark}")
        self._get_focused_window().command(f"mark {window_details.mark}")
        time.sleep(MARK_SLEEP_TIME)

    def focus(self, target_window: dtos.WindowDetails) -> i3ipc.Con:
        logging.debug(f"focusing window with mark {target_window.mark}")
        window = self._get_window(target_window.mark)
        window.command("focus")
        time.sleep(FOCUS_SLEEP_TIME)
        return window

    def split_and_mark_parent(self, split_type: str, mark: str) -> None:
        logging.debug(
            f"splitting the parent of the focused node and marking the container with {mark}"
        )
        focused = self._get_focused_window()
        if split_type == "vertical":
            focused.command("split vertical")
        elif split_type == "horizontal":
            focused.command("split horizontal")
        else:
            raise RuntimeError(f"invalid split type: {split_type}")
        time.sleep(SPLIT_SLEEP_TIME)
        focused.command("focus parent")
        time.sleep(FOCUS_SLEEP_TIME)
        parent = self._get_focused_window()
        parent.command(f"mark {mark}")
        time.sleep(MARK_SLEEP_TIME)
        # need to give focus back to the window that we just focused
        focused.command("focus")
        time.sleep(FOCUS_SLEEP_TIME)

    def resize_width(
        self, target_window: dtos.WindowDetails, section_percentage: int
    ) -> None:
        window = self.focus(target_window)
        time.sleep(FOCUS_SLEEP_TIME)
        window.command(f"resize set width {section_percentage} ppt")

    def resize_height(
        self, target_window: dtos.WindowDetails, section_percentage: int
    ) -> None:
        window = self.focus(target_window)
        time.sleep(FOCUS_SLEEP_TIME)
        window.command(f"resize set height {section_percentage} ppt")

    def get_window_sizes(self) -> Dict[Tuple, Dict[str, float]]:
        return {
            tuple(window.marks): {
                "width": window.window_rect.width,
                "height": window.window_rect.height,
            }
            for window in self._get_windows_in_current_workspace()
        }

    def get_tree(self) -> List:
        current_workspace = self._get_focused_window().workspace()
        return current_workspace.descendants()

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
        current_workspace_num = self._get_current_workspace_num()
        windows_in_current_workspace = []
        for section in self._sway.get_tree().leaves():
            logging.debug(
                f'"{section.name}" is in workspace {section.workspace().num} with '
                + f'marks "{section.marks}"'
            )
            if section.workspace().num == current_workspace_num:
                windows_in_current_workspace.append(section)
        return windows_in_current_workspace

    def _get_current_workspace_num(self) -> i3ipc.Con:
        workspaces = self._sway.get_workspaces()
        for workspace in workspaces:
            if workspace.focused:
                if workspace.num == -1:
                    raise RuntimeError("The current workspace is a named workspace")
                return workspace.num
        else:
            raise RuntimeError("There is no current workspace")

    @property
    def num_workspace_windows(self) -> int:
        """Get the number of windows open on the current workspace

        The current workspace must not be a "named workspace"
        https://i3ipc-python.readthedocs.io/en/latest/replies.html#i3ipc.WorkspaceReply
        """
        return len(self._get_windows_in_current_workspace())
