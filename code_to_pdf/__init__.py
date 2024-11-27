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
    DEFAULT_EXCLUDE = ('.git', 'venv', '*.pyc')

    def __init__(self, exclude = [], include = [], exclude_binary=False):
        self.include = list(re.compile(fnmatch.translate(name)) for name in include)
        self.exclude = list(re.compile(fnmatch.translate(name)) for name in (*self.DEFAULT_EXCLUDE, *exclude))
        

    def select(self, path: Path)-> bool:
        if self.include and not any(pattern.match(path.name) for pattern in self.include):
            return False
        if any(pattern.match(path.name) for pattern in self.exclude):
            return False
        return True

default_filter_predicate = PathSelector().select


def walk(root: Path, filter_predicate):
    yield root
    if root.is_dir():
        for child in filter(filter_predicate, root.iterdir()):
            yield from walk(child, filter_predicate)


class Code(NamedTuple):
    # TODO: no usar abreviaciones
    abs: str
    rel: str

    lang: str


class TocEntry(NamedTuple):
    depth: str
    name: str
    path: str
    is_file: bool


def generate(root: Path, filter_predicate: Callable[Path, bool] = default_filter_predicate):
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
        title=root.name,
        monofont="SauceCodePro Nerd Font",
        mainfont="SauceCodePro Nerd Font Mono",
        filename_in_header=True,
    )  # monofont='Hack Nerd Font Mono', mainfont='Hack Nerd Font'

    return generated
