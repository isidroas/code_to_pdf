from pathlib import Path

from jinja2.loaders import FileSystemLoader
from walkfind import walkfind

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
            "tree_generator.py",
            "*.pyc",
            "*.pdf",
            "tree.py",
            ".coverage",
            "output.html",
        ],
        exclude_dirs=["venv", "build", ".git", "*.egg-info"],
    ):
        relative = path.relative_to(root)
        if path.is_file():
            codes.append({"abs": str(path), "rel": str(relative)})
        node = (
            len(relative.parts) + 1,
            path.name,
            str(path) if path.is_file() else None,
        )
        nodes.append(node)
    return codes, nodes


if __name__ == "__main__":
    codes, nodes = get_codes_and_nodes(Path("/home/isidro/mp/code_to_pdf/"))

    env = make_env(loader=FileSystemLoader("."))
    tpl = env.get_template("doc.tex")

    generated = tpl.render(codes=codes, nodes=nodes)

    # for debugging
    with open("/tmp/out.tex", "wt") as file:
        file.write(generated)

    pdf = build_pdf(generated)
    pdf.save_to("generated.pdf")
