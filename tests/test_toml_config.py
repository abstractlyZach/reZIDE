from magic_tiler import toml_config


def test_toml():
    config_reader = toml_config.TomlConfig()
    config = config_reader.read("examples/centered_big.toml")
    assert config == {
        "children": [
            {"size": 25, "command": "alacritty --title left-panel"},
            {"size": 50, "command": "alacritty --title middle-panel"},
            {"size": 25, "command": "alacritty --title right-panel"},
        ]
    }
