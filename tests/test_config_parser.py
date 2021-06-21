from typing import Dict, NamedTuple, Type
from unittest import mock

import pytest

from magic_tiler.utils import config_parser
from tests import fakes


def test_returns_result_from_tree_factory():
    config_reader = fakes.FakeConfig(
        {
            "ide": {
                "split": "horizontal",
                "children": ["left window", "right window"],
                "sizes": [50, 50],
            },
            "left window": {
                "command": 'alacritty -e sh -c "echo left window!"',
                "mark": "left window",
            },
            "right window": {
                "command": 'alacritty -e sh -c "echo right window!"',
                "mark": "right window",
            },
        }
    )
    tree_stub = mock.MagicMock()
    parser = config_parser.ConfigParser(config_reader, fakes.FakeTreeFactory(tree_stub))
    assert parser.get_tree("ide") == tree_stub


class SuccessfulConfigParserTestCase(NamedTuple):
    config_dict: Dict
    layout_name: str
    expected_tree: Dict


test_cases = [
    SuccessfulConfigParserTestCase(
        config_dict={
            "ide": {
                "split": "horizontal",
                "children": ["left window", "right window"],
                "sizes": [50, 50],
            },
            "left window": {
                "command": 'alacritty -e sh -c "echo left window!"',
                "mark": "left window",
            },
            "right window": {
                "command": 'alacritty -e sh -c "echo right window!"',
                "mark": "right window",
            },
        },
        expected_tree={
            "split": "horizontal",
            "sizes": [50, 50],
            "children": [
                {
                    "command": 'alacritty -e sh -c "echo left window!"',
                    "mark": "left window",
                },
                {
                    "command": 'alacritty -e sh -c "echo right window!"',
                    "mark": "right window",
                },
            ],
        },
        layout_name="ide",
    ),
    SuccessfulConfigParserTestCase(
        config_dict={
            "3 windows": {
                "split": "horizontal",
                "children": ["left side", "right window"],
                "sizes": [50, 50],
            },
            "left side": {
                "split": "vertical",
                "sizes": [40, 60],
                "children": ["top-left window", "bottom-left window"],
            },
            "top-left window": {
                "command": 'alacritty -e sh -c "echo I\'m in the top left!"',
                "mark": "top-left window",
            },
            "bottom-left window": {
                "command": 'alacritty -e sh -c "echo I\'m in the bottom left!"',
                "mark": "bottom-left window",
            },
            "right window": {
                "command": 'alacritty -e sh -c "echo right window!"',
                "mark": "right window",
            },
        },
        expected_tree={
            "split": "horizontal",
            "sizes": [50, 50],
            "children": [
                {
                    "split": "vertical",
                    "sizes": [40, 60],
                    "children": [
                        {
                            "command": 'alacritty -e sh -c "echo I\'m in the top left!"',
                            "mark": "top-left window",
                        },
                        {
                            "command": 'alacritty -e sh -c "echo I\'m in the bottom left!"',
                            "mark": "bottom-left window",
                        },
                    ],
                },
                {
                    "command": 'alacritty -e sh -c "echo right window!"',
                    "mark": "right window",
                },
            ],
        },
        layout_name="3 windows",
    ),
]


@pytest.mark.parametrize("test_case", test_cases)
def test_passes_correct_tree_to_tree_factory(test_case):
    config_reader = fakes.FakeConfig(test_case.config_dict)
    expected_tree = test_case.expected_tree
    spy_tree_factory = mock.MagicMock()
    parser = config_parser.ConfigParser(config_reader, spy_tree_factory)
    parser.get_tree(test_case.layout_name)
    spy_tree_factory.create_tree.assert_called_once_with(expected_tree)


class ConfigParserExceptionTestCase(NamedTuple):
    config_dict: Dict
    expected_error_class: Type[Exception]
    layout_name: str


exception_test_cases = [
    ConfigParserExceptionTestCase(
        config_dict={},
        expected_error_class=KeyError,
        layout_name="",
    ),
    # layout name doesn't exist in config
    ConfigParserExceptionTestCase(
        config_dict={
            "ide": {
                "split": "horizontal",
                "children": ["left window", "right window"],
                "sizes": [50, 50],
            },
            "left window": {
                "command": 'alacritty -e sh -c "echo left window!"',
                "mark": "left window",
            },
            "right window": {
                "command": 'alacritty -e sh -c "echo right window!"',
                "mark": "right window",
            },
        },
        expected_error_class=KeyError,
        layout_name="abc",
    ),
    # children are not defined
    ConfigParserExceptionTestCase(
        config_dict={
            "ide": {
                "split": "horizontal",
                "children": ["left window", "right window"],
                "sizes": [50, 50],
            },
            "left window": {
                "command": 'alacritty -e sh -c "echo left window!"',
                "mark": "left window",
            },
        },
        expected_error_class=RuntimeError,
        layout_name="ide",
    ),
    # missing fields
    ConfigParserExceptionTestCase(
        config_dict={
            "ide": {
                "children": ["left window", "right window"],
            },
            "left window": {
                "command": 'alacritty -e sh -c "echo left window!"',
                "mark": "left window",
            },
            "right window": {
                "command": 'alacritty -e sh -c "echo right window!"',
                "mark": "right window",
            },
        },
        expected_error_class=RuntimeError,
        layout_name="ide",
    ),
    # number of children don't match number of sizes
    ConfigParserExceptionTestCase(
        config_dict={
            "ide": {
                "split": "horizontal",
                "children": ["left window"],
                "sizes": [50, 50],
            },
            "left window": {
                "command": 'alacritty -e sh -c "echo left window!"',
                "mark": "left window",
            },
            "right window": {
                "command": 'alacritty -e sh -c "echo right window!"',
                "mark": "right window",
            },
        },
        expected_error_class=RuntimeError,
        layout_name="ide",
    ),
]


@pytest.mark.parametrize("test_case", exception_test_cases)
def test_config_parser_exceptions(test_case):
    config_reader = fakes.FakeConfig(test_case.config_dict)
    parser = config_parser.ConfigParser(
        config_reader, fakes.FakeTreeFactory(mock.MagicMock())
    )
    with pytest.raises(test_case.expected_error_class):
        parser.get_tree(test_case.layout_name)