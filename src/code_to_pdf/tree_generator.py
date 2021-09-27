# author: https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python


from pathlib import Path
import re


class TreeGenerator(object):
    display_filename_prefix_middle = "├──"
    display_filename_prefix_last = "└──"
    display_parent_prefix_middle = "    "
    display_parent_prefix_last = "│   "

    def __init__(self, path: Path, parent_path: Path, is_last: bool):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

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
        ):
            return False
        if path.name == "__init__.py":
            return False

        if re.search(r".*\.egg-info", path.name):
            return False

        if not path.is_dir():
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
            parent = path_object.parent
            current_folder = str(parent.path) if parent else "."
            tree_string = path_object.displayable()

            yield path_str, file_name, is_dir, depth, parent, current_folder, tree_string
