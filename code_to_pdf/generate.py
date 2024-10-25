import sys
import argparse
from pathlib import Path

import pygments
from jinja2.loaders import PackageLoader
from pygments.lexers import get_lexer_for_filename
from walkfind import walkfind, Sort

from latex.jinja2 import make_env


class StdinIter:

    # TODO: use fileinput.FileInput and inherit
    def __next__(self):
        path = next(sys.stdin)
        path = path.strip()  # remove trailing newline
        path = Path(path)
        assert path.exists()
        return Path(path)

    def __iter__(self):
        return self


def get_codes_and_nodes(iter, root):
    codes = []
    nodes = []

    for path in iter:
        relative = path.relative_to(root)
        if path.is_file():
            try:
                lang = get_lexer_for_filename(path.name).aliases[0]
            except pygments.util.ClassNotFound:
                lang = "text"

            codes.append({"abs": str(path), "rel": str(relative), "lang": lang})
        node = dict(
            depth=len(relative.parts) + 1,
            name=path.name,
            path=str(path),
            is_file=path.is_file(),
        )
        nodes.append(node)

    return codes, nodes


def main():
    paths = StdinIter()
    root = next(paths)
    codes, nodes = get_codes_and_nodes(paths, root)

    env = make_env(loader=PackageLoader("code_to_pdf", "templates"))
    template = env.get_template("doc.tex")

    generated = template.render(
        codes=codes,
        nodes=nodes,
        title=root.name,
        monofont="SauceCodePro Nerd Font",
        mainfont="SauceCodePro Nerd Font Mono",
    )  # monofont='Hack Nerd Font Mono', mainfont='Hack Nerd Font')

    sys.stdout.write(generated)


if __name__ == "__main__":
    main()
