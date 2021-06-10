import click.testing
import pytest


@pytest.fixture(scope="session")
def click_runner():
    return click.testing.CliRunner()
