import pytest

from magic_tiler import get_tree
from tests import fakes


@pytest.fixture
def mock_window_manager(mocker):
    return mocker.patch("magic_tiler.utils.sway.Sway")


@pytest.fixture
def mock_print_tree(mocker):
    mock = mocker.patch("magic_tiler.get_tree.print_tree")
    mock.return_value = """
    Alacritty
    x, y: (803, 294)
    width, height: (787, 846)
    gaps: None
    marks: ['tests']
    """
    return mock


@pytest.mark.e2e
def test_get_tree(click_runner):
    result = click_runner.invoke(get_tree.main)
    assert result.exit_code == 0


def test_click_handles_options(click_runner, mock_window_manager, mock_print_tree):
    click_runner.invoke(get_tree.main)
    mock_print_tree.assert_called_once_with(mock_window_manager())


def test_print_tree_runs():
    tree = [
        fakes.FakeNode("alacritty", fakes.FakeRect(0, 0, 100, 200), None, ["editor"]),
        fakes.FakeNode("alacritty", fakes.FakeRect(0, 0, 100, 200), None, ["editor"]),
        fakes.FakeNode("alacritty", fakes.FakeRect(0, 0, 100, 200), None, ["editor"]),
    ]
    window_manager = fakes.FakeWindowManager(tree=tree)
    get_tree.print_tree(window_manager)
