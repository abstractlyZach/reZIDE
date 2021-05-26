import shlex
import subprocess  # noqa: S404

from magic_tiler.utils import interfaces


class SubprocessRunner(interfaces.Runner):
    def run_and_disown(self, command: str) -> None:
        """Run a command without waiting for it to exit"""
        # split a command into tokens for the shell
        args = shlex.split(command)
        subprocess.Popen(args)  # noqa: S603
