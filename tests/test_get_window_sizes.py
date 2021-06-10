import pytest

from magic_tiler import get_window_sizes
from tests import fakes


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
    click_runner.invoke(get_window_sizes.main)
    mock_print_window_sizes.assert_called_once_with(mock_window_manager())


def test_print_window_sizes_run():
    window_sizes = {("gutter",): {"height": 500, "weight": 400}}
    window_manager = fakes.FakeWindowManager(window_sizes=window_sizes)
    get_window_sizes.print_window_sizes(window_manager)
