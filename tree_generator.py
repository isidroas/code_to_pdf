# author: https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python


from pathlib import Path


class DisplayablePath(object):
    display_filename_prefix_middle = "├──"
    display_filename_prefix_last = "└──"
    display_parent_prefix_middle = "    "
    display_parent_prefix_last = "│   "

    def __init__(self, path, parent_path, is_last):
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

        #children = sorted(
        #    list(path for path in root.iterdir() if criteria(path)),
        #    key=lambda s: str(s).lower() if not s.is_dir() else 'z' + str(s).lower()
        #)
        
        children = sorted(
            list(path for path in root.iterdir() if criteria(path)),
            key=cls._sorter
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
        return (
            True
            if path.name
            not in (
                ".git",
                "__pycache__",
                ".gitattributes",
                "gurux_dlms.pyproj",
                "gurux_dlms.sln",
                ".pylintrc",
                "LICENSE",
                "requirements.txt",
            )
            else False
        )

    @classmethod
    def _sorter(cls, path):
        if path.is_dir():
            return  'z' + str(path).lower()
        else:
            return  str(path).lower()

    def displayable(self):
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


# Usage example
# paths = DisplayablePath.make_tree(Path('doc'))
# for path in paths:
#    print(path.displayable())
