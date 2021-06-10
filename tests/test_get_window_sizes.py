from unittest import mock

import pytest

from magic_tiler import get_window_sizes


@pytest.fixture
def mock_window_manager(mocker):
    return mocker.patch("magic_tiler.utils.sway.Sway")


@pytest.fixture
def mock_print_window_sizes(mocker):
    return mocker.patch("magic_tiler.get_window_sizes.print_window_sizes")


@pytest.mark.e2e
def test_get_window_sizes(click_runner):
    result = click_runner.invoke(get_window_sizes.main)
    assert result.exit_code == 0


def test_click_handles_options(
    click_runner, mock_window_manager, mock_print_window_sizes
):
    """Click should handle the user's input and specified flags to pass in the right
    details to the print_window_sizes function
    """
    click_runner.invoke(get_window_sizes.main)
    mock_print_window_sizes.assert_called_once_with(mock_window_manager())


def test_calls_window_manager():
    window_manager = mock.MagicMock()
    get_window_sizes.print_window_sizes(window_manager)
    window_manager.get_window_sizes.assert_called_once_with()
