import pdfkit
import os
from jinja2 import Template
from pdf_generator import add_blank_page, number_of_pages
from temporal import get_temp_folder


ENTRY_DIR = """<div class=row>{{ 125*'.' }}<span class="d{{ depth }}"> {{ 6*depth*"&nbsp;" }} {{ name }}&nbsp</span><span class="right">{{ page }}</div>"""
# ENTRY_DIR = """<div class=row><span class="d{{ depth }}"> {{ 2*depth*"&nbsp;" }} {{ name }}</span></div></br>"""
ENTRY_FILE = """<div class=row>{{ 125*'.' }}<span class="f{{ depth }}"> {{ 6*depth*"&nbsp;" }} {{ name }}&nbsp</span><span class="right">{{ page }}</div>"""


def get_entry(name, depth, page, is_dir=False):
    n_dots = 60
    if is_dir:
        template = Template(ENTRY_DIR)
    else:
        template = Template(ENTRY_FILE)
    return template.render(name=name, depth=depth, page=page) + "\n"


def render_toc(entries, output_pdf):
    with open("toc_template/template.html", "r") as html_temp:
        template = Template(html_temp.read())

    output_html = template.render(entries=entries)

    temp_file = os.path.join(get_temp_folder(), "toc_output.html")

    with open(temp_file, "w") as output_file:
        output_file.write(output_html)

    options = {"quiet": ""}
    pdfkit.from_file(temp_file, output_pdf, options=options)
    if number_of_pages(output_pdf) % 2:
        add_blank_page(output_pdf)
