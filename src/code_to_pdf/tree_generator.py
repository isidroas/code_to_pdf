# author: https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
import logging
from fnmatch import fnmatchcase
from pathlib import Path
from typing import List

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
    if not path.is_dir():
        # detect if it is a binary file, instead of text file
        try:
            with open(path, "r") as file:
                str_ = file.read()
                if not str_:
                    logging.warn("Skipping empty file %s" % str(path))
                    return False

        except UnicodeDecodeError:
            logging.warn("Decode error for file %s" % str(path))
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
    for i in walk_tree("../../"):
        print(i)
        # pass
