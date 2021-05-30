from magic_tiler.utils import toml_config


def test_toml():
    config_reader = toml_config.TomlConfig("examples/centered_big.toml")
    assert config_reader.to_dict() == {
        "screen": {
            "children": [
                {
                    "children": [
                        {
                            "size": 60,
                            "command": "alacritty --title medium-window -e sh "
                            + "-c 'cowsay $(fortune); zsh -i'",
                            "mark": "medium-window",
                        },
                        {
                            "size": 40,
                            "command": "alacritty --title tiny-window -e sh -c 'neofetch; zsh'",
                            "mark": "tiny-window",
                        },
                    ],
                    "split": "vertical",
                    "size": 25,
                },
                {
                    "size": 50,
                    "command": "alacritty --title middle-panel -e sh -c 'kak ~/internet.txt'",
                    "mark": "middle-panel",
                },
                {
                    "size": 25,
                    "command": "alacritty --title right-panel -e sh -c 'broot'",
                    "mark": "right-panel",
                },
            ],
            "split": "horizontal",
        }
    }
