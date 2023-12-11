# TODO: convert template.tex to generated.tex
from jinja2.loaders import FileSystemLoader

from latex import build_pdf
from latex.jinja2 import make_env

env = make_env(loader=FileSystemLoader("."))
tpl = env.get_template("doc.tex")

generated = tpl.render(name="Alice")


pdf = build_pdf(generated)
pdf.save_to("generated.pdf")
