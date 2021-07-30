from typing import Dict, List, NamedTuple, Optional, Set, Type

from pyfakefs import fake_filesystem

from rezide.utils import dtos
from rezide.utils import interfaces
from rezide.utils import tree


class FakeFilestore(interfaces.FileStore):
    def __init__(self, files: Dict[str, str]):
        """Initialize a fake filestore with a mapping from filenames to file contents"""
        self._filesystem = fake_filesystem.FakeFilesystem()
        self._os_module = fake_filesystem.FakeOsModule(self._filesystem)
        self._open = fake_filesystem.FakeFileOpen(self._filesystem)
        for file_path, contents in files.items():
            self._filesystem.create_file(file_path, contents=contents)

    def path_exists(self, path: str) -> bool:
        return self._os_module.path.exists(path)

    def read_file(self, path: str) -> str:
        with self._open(path) as infile:
            return infile.read()

    def exists_as_dir(self, path: str) -> bool:
        return self.path_exists(path) and self._os_module.path.isdir(path)

    def exists_as_file(self, path: str) -> bool:
        return self.path_exists(path) and self._os_module.path.isfile(path)

    def list_directory_contents(self, path: str) -> Set[str]:
        return set(self._os_module.listdir(path))


class FakeTreeFactory(interfaces.TreeFactoryInterface):
    def __init__(self, tree_root: tree.TreeNode):
        self._tree = tree_root

    def create_tree(self, root_node: Dict) -> tree.TreeNode:
        return self._tree


class FakeConfig(interfaces.ConfigReader):
    def __init__(self, config_dict: Dict) -> None:
        self._config_dict = config_dict

    def read(self, path: str) -> Dict:
        return self._config_dict


class FakeConfigParser(interfaces.ConfigParserInterface):
    def __init__(
        self, config_dict: Dict, validation_error: Optional[Type[Exception]] = None
    ) -> None:
        self._tree_factory = tree.TreeFactory()
        self._config_dict = config_dict
        self._validation_error = validation_error

    def validate(self) -> None:
        if self._validation_error is not None:
            raise self._validation_error

    def get_tree(self) -> interfaces.TreeNodeInterface:
        return self._tree_factory.create_tree(self._config_dict)


class FakeRect(NamedTuple):
    x: int
    y: int
    width: int
    height: int


class FakeNode(NamedTuple):
    name: str
    rect: FakeRect
    gaps: Optional[str]
    marks: List


class FakeWindowManager(interfaces.TilingWindowManager):
    def __init__(
        self,
        tree: Optional[List[FakeNode]] = None,
        window_sizes: Optional[Dict] = None,
        num_workspace_windows: int = 0,
    ):
        if tree:
            self._tree = tree
        if window_sizes:
            self._window_sizes = window_sizes
        self._num_workspace_windows = num_workspace_windows

    def make_window(self, window_details: dtos.WindowDetails) -> None:
        pass

    def resize_width(
        self, target_window: dtos.WindowDetails, section_percentage: int
    ) -> None:
        pass

    def resize_height(
        self, target_window: dtos.WindowDetails, section_percentage: int
    ) -> None:
        pass

    def focus(self, target_window: dtos.WindowDetails) -> None:
        pass

    def split_and_mark_parent(self, split_type: str, mark: str) -> None:
        pass

    @property
    def num_workspace_windows(self) -> int:
        """Count the windows on the current workspace"""
        return self._num_workspace_windows

    def get_tree(self) -> List[FakeNode]:
        return self._tree

    def get_window_sizes(self):
        return self._window_sizes


class SpyWindowManager(FakeWindowManager):
    """Gets passed into LayoutManagers using dependency injection and spies on their
    calls so we can make sure that we're making the right window commands
    """

    def __init__(self, **kwargs):
        self._calls: List[dtos.WindowManagerCall] = []
        super().__init__(**kwargs)

    @property
    def calls(self):
        return self._calls

    def make_window(
        self,
        window_details: dtos.WindowDetails,
    ) -> None:
        self._calls.append(dtos.WindowManagerCall(command="make", arg=window_details))

    def resize_width(
        self, target_window: dtos.WindowDetails, section_percentage: int
    ) -> None:
        pass

    def resize_height(
        self, target_window: dtos.WindowDetails, section_percentage: int
    ) -> None:
        pass

    def focus(self, target_window: dtos.WindowDetails) -> None:
        self._calls.append(dtos.WindowManagerCall("focus", arg=target_window))

    # todo: add the mark to the call
    def split_and_mark_parent(self, split_type: str, mark: str) -> None:
        self._calls.append(dtos.WindowManagerCall("split", arg=split_type))
