from magic_tiler import toml_config


def test_toml():
    config_reader = toml_config.TomlConfig("examples/centered_big.toml")
    assert config_reader.to_dict() == {
        "screen": {
            "children": [
                {
                    "children": [
                        {
                            "size": 60,
                            "command": "alacritty --title medium-window",
                            "name": "medium-window",
                        },
                        {
                            "size": 40,
                            "command": "alacritty --title tiny-window",
                            "name": "tiny-window",
                        },
                    ],
                    "split": "vertical",
                    "size": 25,
                },
                {
                    "size": 50,
                    "command": "alacritty --title middle-panel",
                    "name": "middle-panel",
                },
                {
                    "size": 25,
                    "command": "alacritty --title right-panel",
                    "name": "right-panel",
                },
            ],
            "split": "horizontal",
        }
    }
