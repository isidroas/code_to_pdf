import pdfkit
import os
import re
from jinja2 import Template
from pdf_generator import add_blank_page, number_of_pages
from temporal import get_temp_folder
from pdf_generator import PDFKIT_OPTIONS
from art import text2art


ENTRY_DIR = """<div class=row>{{ 157*'.' }}<span class="row_text"> {{tree}}<span class="dir">{{ name }} </span>&nbsp</span><span class="right">{{ page }}</div>"""
ENTRY_FILE = """<div class=row>{{ 157*'.' }}<span class="row_text">{{tree}} <span class="file">{{ name }}&nbsp</span></span><span class="right">{{ page }}</div>"""


def get_entry(name, depth, page, tree, is_dir=False):
    tree = re.sub(" ", "&nbsp;&nbsp;", tree)
    if is_dir:
        template = Template(ENTRY_DIR)
    else:
        template = Template(ENTRY_FILE)
    return template.render(name=name, depth=depth, page=page, tree=tree) + "\n"


def render_toc(entries, output_pdf, project_name):
    folder, _ = os.path.split(__file__)
    template_path = os.path.join(folder, 'template.html')
    with open(template_path, "r") as html_temp:
        template = Template(html_temp.read())

    ascii_title = text2art(project_name)
    output_html = template.render(
        entries=entries, page_number_pos=800, ascii_title=ascii_title
    )

    temp_file = os.path.join(get_temp_folder(), "toc_output.html")

    with open(temp_file, "w") as output_file:
        output_file.write(output_html)

    options = {"quiet": ""}
    pdfkit.from_file(temp_file, output_pdf, options=PDFKIT_OPTIONS)
    if number_of_pages(output_pdf) % 2:
        add_blank_page(output_pdf)
