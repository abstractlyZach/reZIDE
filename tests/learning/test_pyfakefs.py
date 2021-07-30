"""Tests for learning how pyfakefs works"""

import os

from pyfakefs import fake_filesystem
import pytest


@pytest.fixture
def filesystem():
    return fake_filesystem.FakeFilesystem()


@pytest.fixture
def os_module(filesystem):
    return fake_filesystem.FakeOsModule(filesystem)


def test_basic_file_creation(filesystem, os_module):
    directory = "/home/test/.config/rezide/python/"
    filename = "config.toml"
    file_path = os.path.join(directory, filename)
    filesystem.create_file(file_path)
    assert os_module.path.exists(file_path)
    assert os_module.path.isfile(file_path)
    assert os_module.path.isdir(directory)


def test_directory_listing_files(filesystem, os_module):
    directory = "/home/test/.config/rezide/python/"
    filenames = ["config.toml", "abc.txt", "readme.pdf"]
    for filename in filenames:
        file_path = os.path.join(directory, filename)
        filesystem.create_file(file_path)
    assert os_module.listdir(directory) == filenames


def test_directory_listing_directories(filesystem, os_module):
    config_directory = "/home/test/.config/rezide/"
    config_packages = ["rezide-ide", "python", "documentation"]
    for package in config_packages:
        file_path = os.path.join(config_directory, package, "config.toml")
        filesystem.create_file(file_path)
    assert os_module.listdir(config_directory) == config_packages
