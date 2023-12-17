# TODO: convert template.tex to generated.tex
from pathlib import Path

from jinja2.loaders import FileSystemLoader
from walkfind import walkfind

from latex import build_pdf
from latex.jinja2 import make_env

codes = [  # section; label; absolute_path
    (
        "code_to_pdf/run.py",
        "code-to-pdf:run.py",
        "/home/isidro/mp/code_to_pdf/src/code_to_pdf/run.py",
    ),
    (
        r"code_to_pdf/template.html",
        "code-to-pdf:template.html",
        "/home/isidro/mp/code_to_pdf/src/code_to_pdf/template.html",
    ),
]

nodes = [
    (1, "run.py", "sec:code-to-pdf:run.py"),
    (2, "template.html", "sec:code-to-pdf:template.html"),
]

codes = []
nodes = []

for path in walkfind(
    Path("/home/isidro/mp/code_to_pdf/src"),
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
    print(path)
    if path.is_file():
        code = str(path)
        codes.append(code)
    node = (
        len(path.parts) - 4,
        path.name,
        str(path) if path.is_file() else None,
    )  # TODO: remove hard depth
    # print(node)
    nodes.append(node)
env = make_env(loader=FileSystemLoader("."))
tpl = env.get_template("doc.tex")

generated = tpl.render(codes=codes, nodes=nodes)
with open("/tmp/out.tex", "wt") as file:
    file.write(generated)


pdf = build_pdf(generated)
pdf.save_to("generated.pdf")
