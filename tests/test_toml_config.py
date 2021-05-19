from magic_tiler import toml_config


def test_toml():
    config_reader = toml_config.TomlConfig()
    config = config_reader.read("examples/centered_big.toml")
    assert config["left-panel"] == {
        "size": 25,
        "command": "alacritty --title left-panel",
    }
    assert config == {
        "left-panel": {"size": 25, "command": "alacritty --title left-panel"},
        "middle-panel": {"size": 50, "command": "alacritty --title middle-panel"},
        "right-panel": {"size": 25, "command": "alacritty --title right-panel"},
    }
