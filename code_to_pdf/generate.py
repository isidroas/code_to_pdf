import sys
import argparse
from pathlib import Path

import pygments
from jinja2.loaders import FileSystemLoader, PackageLoader
from pygments.lexers import get_lexer_for_filename
from walkfind import walkfind, Sort

from latex import build_pdf
from latex.jinja2 import make_env


def get_codes_and_nodes(root):
    codes = []
    nodes = []

    for path in walkfind(
        root,
        # git_tracked=True,
        also_dirs=True,
        exclude_files=[
            "*.pdf",
            ".coverage",
            "output.html",
            "LICENSE",
            "*.svg",
        ],
        exclude_dirs=["venv", "build", ".git", "*.egg-info", "HTML", "docs"],
        binary=False,
        sort=[Sort.FILES_FIRST, Sort.ALPHA]
    ):
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

def get_arguments():
    parser = argparse.ArgumentParser(description="Code to PDF generator")
    parser.add_argument("source_folder", help="Source code folder", type=Path)
    parser.add_argument("--title", type=str, help="Title of the document")
    parser.add_argument(
        "--output-folder", type=str, help="Path where pdf will be generated"
    )
    return parser.parse_args()

def main():
    args = get_arguments()
    path = args.source_folder
    codes, nodes = get_codes_and_nodes(path)

    env = make_env(loader=PackageLoader("code_to_pdf", 'templates'))
    tpl = env.get_template("doc.tex")

    generated = tpl.render(codes=codes, nodes=nodes, title=path.name,monofont = 'SauceCodePro Nerd Font', mainfont = 'SauceCodePro Nerd Font Mono')# monofont='Hack Nerd Font Mono', mainfont='Hack Nerd Font')

    # for debugging
    with open("/tmp/out.tex", "wt") as file:
        file.write(generated)

    # quit()
    pdf = build_pdf(generated, builder = 'xelatexmk')
    pdf.save_to("generated.pdf")

if __name__ == "__main__":
    main()
