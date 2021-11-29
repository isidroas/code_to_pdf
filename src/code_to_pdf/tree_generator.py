# author: https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python


import os
import re
from fnmatch import fnmatchcase
from pathlib import Path
from typing import List

###


class TreeGenerator(object):
    display_filename_prefix_middle = "├──"
    display_filename_prefix_last = "└──"
    display_parent_prefix_middle = "    "
    display_parent_prefix_last = "│   "

    def __init__(self, path: Path, parent_path, is_last: bool):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        self.depth = self.parent.depth + 1 if self.parent else 0  # type: ignore

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + "/"
        return self.path.name

    @classmethod
    def make_tree(cls, root, parent=None, is_last=False, criteria=None):
        root = Path(str(root))
        criteria = criteria or cls._default_criteria

        displayable_root = cls(root, parent, is_last)
        yield displayable_root

        # children = sorted(
        #    list(path for path in root.iterdir() if criteria(path)),
        #    key=lambda s: str(s).lower() if not s.is_dir() else 'z' + str(s).lower()
        # )

        children = sorted(
            list(path for path in root.iterdir() if criteria(path)), key=cls._sorter
        )

        count = 1
        for path in children:
            is_last = count == len(children)
            if path.is_dir():
                yield from cls.make_tree(
                    path, parent=displayable_root, is_last=is_last, criteria=criteria
                )
            else:
                yield cls(path, displayable_root, is_last)
            count += 1

    @staticmethod
    def _default_criteria(path):
        if path.name in (
            ".git",
            "__pycache__",
            ".gitattributes",
            "gurux_dlms.pyproj",
            "gurux_dlms.sln",
            ".pylintrc",
            "LICENSE",
            "requirements.txt",
            "venv",
        ):
            return False
        if path.name == "__init__.py":
            return False

        if re.search(r".*\.egg-info", path.name):
            return False

        if not path.is_dir():
            # TODO: remove the next condition to support more lenguages
            if not re.search(r".*\.py", path.name):
                return False

            # detect if it is a binary file, instead of text file
            try:
                with open(path, "r") as file:
                    file.read()
            except UnicodeDecodeError:
                return False

        return True

    @classmethod
    def _sorter(cls, path):
        if path.is_dir():
            return "z" + str(path).lower()
        else:
            return str(path).lower()

    def displayable(self) -> str:
        if self.parent is None:
            return ""

        _filename_prefix = (
            self.display_filename_prefix_last
            if self.is_last
            else self.display_filename_prefix_middle
        )

        #        parts = ['{!s} {!s}'.format(_filename_prefix,
        #                                    self.displayname)]
        parts = [_filename_prefix]

        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(
                self.display_parent_prefix_middle
                if parent.is_last
                else self.display_parent_prefix_last
            )
            parent = parent.parent

        return "".join(reversed(parts))

    @classmethod
    def get_iterable(cls, path):
        for path_object in cls.make_tree(path):
            path_str = str(path_object.path)
            file_name = path_object.displayname
            is_dir = path_object.path.is_dir()
            depth = path_object.depth
            # parent = path_object.parent
            # current_folder = str(parent.path) if parent else "."
            tree_string = path_object.displayable()

            path_rel = os.path.relpath(path_str, path)

            yield path_str, file_name, is_dir, depth, tree_string, path_rel


display_filename_prefix_middle = "├──"
display_filename_prefix_last = "└──"
display_parent_prefix_middle = "    "
display_parent_prefix_last = "│   "

BLACK_LIST = [
    "__pycache__/",
    "*.swp",
    "*.pdf",
    "*.pyc",
    "/*.html",
    "/*.pdf",
    "*.egg-info",
    ".coverage",
    "venv",
    ".mypy_cache",
    ".git",
    "*~",
    "*.svg",
    "tags",
]


def _filter(path: Path, excluded_files):
    # TODO: use pathlib.Path.match?
    if path.is_symlink():
        return False
    for i in excluded_files:
        if fnmatchcase(path.name, i):
            return False
    return True


def _sorter_key(key: Path):
    """
    This guarantiees that folders will appear last
    """

    if key.is_dir():
        return "z" + key.name.lower()
    else:
        return key.name.lower()


def _calculate_prefix(parents: List[bool]):
    if not parents:
        return ""

    prefix = ""
    for is_last2 in parents[:-1]:
        prefix += (
            display_parent_prefix_last if not is_last2 else display_parent_prefix_middle
        )

    prefix += (
        display_filename_prefix_last if parents[-1] else display_filename_prefix_middle
    )
    return prefix


def iterate_over_dir(folder: Path, is_last_list: List[bool] = [], excluded_files=[]):
    folder = folder.resolve()

    prefix = _calculate_prefix(is_last_list)

    yield prefix, folder

    if folder.is_dir():
        contents = folder.iterdir()

        # filter
        contents_filtered = iter(it for it in contents if _filter(it, excluded_files))

        # sort
        contents_sorted = sorted(contents_filtered, key=_sorter_key)

        for index, c in enumerate(contents_sorted):
            is_last2 = index == len(contents_sorted) - 1
            is_last_list2 = is_last_list[:]
            is_last_list2.append(is_last2)

            yield from iterate_over_dir(c, is_last_list2, excluded_files=excluded_files)


def walk_tree(path_str: str, excluded_files: List = BLACK_LIST):
    """
    User friendly wrapper for `iterate_over_dir`
    ret: tree_prefix, name,
    """
    path = Path(path_str).resolve()

    for tree_string, path_object in iterate_over_dir(
        path, excluded_files=excluded_files
    ):

        path_str = str(path_object)
        is_dir = path_object.is_dir()
        file_name = path_object.name
        if is_dir:
            file_name += "/"

        depth = len(path_object.parts)

        path_rel = path_object.relative_to(path)

        yield path_str, file_name, is_dir, depth, tree_string, path_rel


if __name__ == "__main__":
    # for i in iterate_over_dir(Path("../../")):
    #    #print(i)
    #    pass

    for i in walk_tree("../../"):
        print(i)
        # pass
