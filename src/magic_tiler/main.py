import logging

from magic_tiler import subprocess_runner
from magic_tiler import sway

logging.basicConfig(level=logging.INFO)
swaywm = sway.Sway(subprocess_runner.SubprocessRunner())
swaywm.make_horizontal_sibling("Alacritty:v", 'alacritty -e sh -c "ls | fzf"')
# how do we make alacritty hang around after running the initial command?
swaywm.make_horizontal_sibling("Alacritty:poetry", 'alacritty -e zsh -c "ls"')
