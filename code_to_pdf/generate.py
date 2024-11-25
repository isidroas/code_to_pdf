import sys
from pathlib import Path
from typing import NamedTuple

import pygments
from jinja2.loaders import PackageLoader
from latex.jinja2 import make_env
from pygments.lexers import get_lexer_for_filename


def filter_path(path):
    return not path.name == ".git"


def walk(root: Path):
    yield root
    if root.is_dir():
        for child in filter(filter_path, root.iterdir()):
            yield from walk(child)


class Code(NamedTuple):
    abs: str
    rel: str
    lang: str


class TocEntry(NamedTuple):
    depth: str
    name: str
    path: str
    is_file: bool


def main():
    codes = []
    toc_entries = []
    root = Path(sys.argv[1])
    for path in walk(root):
        print(path, file=sys.stderr)
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

    sys.stdout.write(generated)


if __name__ == "__main__":
    main()
