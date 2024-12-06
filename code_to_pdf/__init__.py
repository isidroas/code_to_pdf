import logging
import sys
import re
import fnmatch
from pathlib import Path
from typing import NamedTuple, Callable

import pygments
from jinja2.loaders import PackageLoader
from latex.jinja2 import make_env
from pygments.lexers import get_lexer_for_filename

LOG = logging.getLogger(__name__)


class PathSelector:
    DEFAULT_EXCLUDE = (".git", "venv", "*.pyc")

    # TODO: `include` use case? por ahora no lo he necesitado. En todo caso tendría más sentido sin contar directories?
    # TODO: exclude is acutally: extend_exclude
    def __init__(
        self, exclude=[], include=[], exclude_binary=True, exclude_empty=False
    ):
        self.include = list(re.compile(fnmatch.translate(name)) for name in include)
        self.exclude = list(
            re.compile(fnmatch.translate(name))
            for name in (*self.DEFAULT_EXCLUDE, *exclude)
        )
        self.exclude_empty = exclude_empty
        self.exclude_binary = exclude_binary

    # def select(self, path: Path)-> bool:
    #     if self.include and not any(pattern.match(path.name) for pattern in self.include):
    #         return False
    #     if any(pattern.match(path.name) for pattern in self.exclude):
    #         return False
    #     return True
    def select(self, path: Path) -> bool:
        # TODO: fmt: block
        # fmt: off
        # return (
        #     not self.is_excluded(path)
        #     and (not self.include or self.is_included(path))
        #     and (not self.exclude_binary or not self.is_binary(path))
        #     and (not self.exclude_emtpy or not self.is_empty(path))
        #     # not any(pattern.match(path.name) for pattern in self.exclude)
        #     # and (not self.include or any(pattern.match(path.name) for pattern in self.include))
        # )
        # reverted bool more concise?
        return not (
            self.is_excluded(path)
            or (self.include and not self.is_included(path))
            or (self.exclude_binary and path.is_file() and self.is_binary(path))
            or (self.exclude_empty and self.is_empty(path))
            # or any(pattern.match(path.name) for pattern in self.exclude)
            # or not (self.include or any(pattern.match(path.name) for pattern in self.include))
        )
        # fmt: on

    def is_included(self, path) -> bool:
        return any(pattern.match(path.name) for pattern in self.include)

    def is_excluded(self, path) -> bool:
        return any(pattern.match(path.name) for pattern in self.exclude)

    @staticmethod
    def is_empty(path) -> bool:
        # return (path.is_dir() and len(list(path.iterdir()))==0) or (path.is_file() and path.stat().st_size ==0)
        return (
            len(list(path.iterdir())) == 0
            if path.is_dir()
            else path.stat().st_size == 0
        )

    @staticmethod
    def is_binary(path) -> bool:
        try:
            path.read_text()
        except UnicodeError:
            return True
        return False


default_filter_predicate = PathSelector().select


def walk(root: Path, filter_predicate):
    yield root
    if root.is_dir():
        for child in filter(filter_predicate, root.iterdir()):
            yield from walk(child, filter_predicate)


class Code(NamedTuple):
    # TODO: no usar abreviaciones

    # en realidad no necesita ser absoluto, sino relativo a cwd
    abs: str

    # relative to root
    rel: str

    lang: str


class TocEntry(NamedTuple):
    depth: str
    name: str
    path: str
    is_file: bool


def generate(
    root: Path,
    filter_predicate: Callable[[Path], bool] = default_filter_predicate,
    title=None,
    monofont=None,
    mainfont=None,
):
    """
    if `root` is absolute, the resulting tex file can be moved.
    """
    if not root.exists():
        raise FileNotFoundError(root)
    codes = []
    toc_entries = []
    for path in walk(root, filter_predicate):
        LOG.info(path)
        relative = path.relative_to(root)
        if not path.is_dir():
            try:
                lang = get_lexer_for_filename(path.name).aliases[0]
            except pygments.util.ClassNotFound:
                lang = "text"
            codes.append(Code(abs=str(path), rel=str(relative), lang=lang))
        toc_entries.append(
            TocEntry(
                depth=len(relative.parts) + 1,
                name=path.name,
                path=str(path),
                is_file=path.is_file(),
            )
        )

    env = make_env(loader=PackageLoader("code_to_pdf", "templates"))
    template = env.get_template("doc.tex")

    generated = template.render(
        codes=codes,
        nodes=toc_entries,
        title=title or root.name,
        monofont=monofont,
        mainfont=mainfont,
        filename_in_header=True,
    )  # monofont='Hack Nerd Font Mono', mainfont='Hack Nerd Font'

    return generated
