# The config file
## Rules
* the number of sizes in a container must match the number of children
* a container must have > 1 child
* these fields and only these fields must be defined
* each child that is named must exist
* marks must be unique

## Window
A Window is the basic object that defines a window on your computer.
* command: the command that spawns the window
* mark: the mark that is used to identify the window

```toml
['medium window']
# make a cow say moo, then run zsh
command = "alacritty -e sh -c 'cowsay moo; zsh'"
mark = "medium-window"

['tiny window']
# show computer specs, then run zsh
command = "alacritty -e sh -c 'neofetch; zsh'"
mark = "tiny-window"
```

## Container
A container is an object that contains other Containers or Windows.
* split: its split orientation (horizontal or vertical)
* children: a list of its children's names
* sizes: a list of its children's sizes

Here are two Container definitions in TOML:
```toml
[screen]
split = "horizontal"
children = ['left', 'middle', 'right']
sizes = [25, 50, 25]

[left]
split = "vertical"
children = ['medium window', 'tiny window']
sizes = [60, 40]
```
