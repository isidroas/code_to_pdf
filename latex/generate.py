# TODO: convert template.tex to generated.tex
from jinja2.loaders import FileSystemLoader

from latex import build_pdf
from latex.jinja2 import make_env

codes = [  # section; label; absolute_path
    (
        "code_to_pdf/run.py",
        "sec:code-to-pdf:run.py",
        "/home/isidro/mp/code_to_pdf/src/code_to_pdf/run.py",
    ),
    (
        r"code_to_pdf/template.html",
        "sec:code-to-pdf:template.html",
        "/home/isidro/mp/code_to_pdf/src/code_to_pdf/template.html",
    ),
]

nodes = [
    (1, "run.py", "sec:code-to-pdf:run.py"),
    (2, "template.html", "sec:code-to-pdf:template.html"),
]

env = make_env(loader=FileSystemLoader("."))
tpl = env.get_template("doc.tex")

generated = tpl.render(codes=codes, nodes=nodes)


pdf = build_pdf(generated)
pdf.save_to("generated.pdf")
