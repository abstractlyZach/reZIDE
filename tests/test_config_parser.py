from typing import Dict, NamedTuple, Type
from unittest import mock

import pytest

from rezide.utils import config_parser
from tests import fakes

# TODO: pick better/more-specific errors than RuntimeError lol


def test_returns_result_from_tree_factory():
    config_dict = {
        "root": {
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
    tree_stub = mock.MagicMock()
    parser = config_parser.ConfigParser(config_dict, fakes.FakeTreeFactory(tree_stub))
    assert parser.get_tree() == tree_stub


class SuccessfulConfigParserTestCase(NamedTuple):
    config_dict: Dict
    expected_tree: Dict


test_cases = [
    SuccessfulConfigParserTestCase(
        config_dict={
            "root": {
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
    ),
    SuccessfulConfigParserTestCase(
        config_dict={
            "root": {
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
            },
            "bottom-left window": {
                "command": 'alacritty -e sh -c "echo I\'m in the bottom left!"',
            },
            "right window": {
                "command": 'alacritty -e sh -c "echo right window!"',
            },
        },
        expected_tree={
            "split": "horizontal",
            "sizes": [50, 50],
            "children": [
                {
                    "split": "vertical",
                    "sizes": [40, 60],
                    "mark": "left side",
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
    ),
]


@pytest.mark.parametrize("test_case", test_cases)
def test_passes_correct_tree_to_tree_factory(test_case):
    expected_tree = test_case.expected_tree
    spy_tree_factory = mock.MagicMock()
    parser = config_parser.ConfigParser(test_case.config_dict, spy_tree_factory)
    parser.get_tree()
    spy_tree_factory.create_tree.assert_called_once_with(expected_tree)


class ConfigParserExceptionTestCase(NamedTuple):
    config_dict: Dict
    expected_error_class: Type[Exception]


exception_test_cases = [
    ConfigParserExceptionTestCase(
        config_dict={},
        expected_error_class=KeyError,
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
    ),
]


@pytest.mark.parametrize("test_case", exception_test_cases)
def test_config_parser_exceptions(test_case):
    parser = config_parser.ConfigParser(
        test_case.config_dict, fakes.FakeTreeFactory(mock.MagicMock())
    )
    with pytest.raises(test_case.expected_error_class):
        parser.get_tree()


validation_test_cases = [
    # missing fields
    ConfigParserExceptionTestCase(
        config_dict={"ide": {"split": "horizontal"}},
        expected_error_class=RuntimeError,
    ),
    # invalid field in section
    ConfigParserExceptionTestCase(
        config_dict={
            "ide": {
                "split": "horizontal",
                "children": ["a", "b"],
                "sizes": [1, 1],
                "woops": "idk",
            }
        },
        expected_error_class=RuntimeError,
    ),
    ConfigParserExceptionTestCase(
        config_dict={
            "ide": {
                "split": "horizontal",
                "children": ["left window", "right window"],
                "sizes": [50, 50],
            },
            "left window": {
                "command": 'alacritty -e sh -c "echo left window!"',
            },
            "right window": {
                "command": 'alacritty -e sh -c "echo right window!"',
                "mark": "right window",
            },
        },
        expected_error_class=RuntimeError,
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
    ),
    # number of children don't match number of sizes
    ConfigParserExceptionTestCase(
        config_dict={
            "ide": {
                "split": "horizontal",
                "children": ["left window", "right window", "abc"],
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
            "abc": {
                "command": 'alacritty -e sh -c "echo right window!"',
                "mark": "right window",
            },
            "def": {
                "command": 'alacritty -e sh -c "echo right window!"',
                "mark": "right window",
            },
        },
        expected_error_class=RuntimeError,
    ),
    # less than 2 children
    ConfigParserExceptionTestCase(
        config_dict={
            "ide": {
                "split": "horizontal",
                "children": [],
                "sizes": [],
            },
        },
        expected_error_class=RuntimeError,
    ),
    ConfigParserExceptionTestCase(
        config_dict={
            "ide": {
                "split": "horizontal",
                "children": ["left"],
                "sizes": [100],
            },
            "left": {
                "command": 'alacritty -e sh -c "echo left window!"',
                "mark": "left window",
            },
        },
        expected_error_class=RuntimeError,
    ),
    # extra junk in section
    ConfigParserExceptionTestCase(
        config_dict={
            "ide": {
                "split": "horizontal",
                "children": ["left", "right"],
                "sizes": [45, 55],
                "woops": "abc",
            },
        },
        expected_error_class=RuntimeError,
    ),
    # extra junk in window
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
                "extra": "nice",
            },
        },
        expected_error_class=RuntimeError,
    ),
    ConfigParserExceptionTestCase(
        config_dict={
            "ide": {
                "split": "horizontal",
                "children": ["left window", "left window"],
                "sizes": [50, 50],
            },
            "right window": {
                "command": 'alacritty -e sh -c "echo left window!"',
                "mark": "right window",
            },
            "left window": {
                "command": 'alacritty -e sh -c "echo right window!"',
                "mark": "right window",
            },
        },
        expected_error_class=RuntimeError,
    ),
]


@pytest.mark.parametrize("test_case", validation_test_cases)
def test_parser_validation(test_case):
    parser = config_parser.ConfigParser(
        test_case.config_dict, fakes.FakeTreeFactory(mock.MagicMock())
    )
    with pytest.raises(test_case.expected_error_class):
        parser.validate()


def test_parser_validation_happy_path():
    # perfectly good config
    config_dict = {
        "ide": {
            "split": "horizontal",
            "children": ["left window", "right window"],
            "sizes": [50, 50],
            "is_layout": True,
        },
        "left window": {
            "command": 'alacritty -e sh -c "echo left window!"',
        },
        "right window": {
            "command": 'alacritty -e sh -c "echo right window!"',
        },
    }
    parser = config_parser.ConfigParser(
        config_dict, fakes.FakeTreeFactory(mock.MagicMock())
    )
    # no exception raised
    parser.validate()
