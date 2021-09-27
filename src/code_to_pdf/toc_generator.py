import pdfkit
import os
import re
import logging
from art import text2art
from jinja2 import Template
from code_to_pdf.pdf_generator import PDFCreator
from code_to_pdf.pdf_generator import PDFKIT_OPTIONS


ENTRY_DIR = """<div class=row>{{ 157*'.' }}<span class="row_text"> {{tree}}<span class="dir">{{ name }} </span>&nbsp</span><span class="right">{{ page }}</div>"""
ENTRY_FILE = """<div class=row>{{ 157*'.' }}<span class="row_text">{{tree}} <span class="file">{{ name }}&nbsp</span></span><span class="right">{{ page }}</div>"""


class TocGenerator:
    def __init__(self):
        self.entries = ""

    def add_entry(self, name, depth, page, tree, is_dir=False):
        tree = re.sub(" ", "&nbsp;&nbsp;", tree)
        if is_dir:
            template = Template(ENTRY_DIR)
            logging.info(depth * "   " + "Folder: {}".format(name))
        else:
            logging.info((depth + 1) * "   " + "File: {}: {}".format(name, page))
            template = Template(ENTRY_FILE)
        self.entries = (
            self.entries
            + template.render(name=name, depth=depth, page=page, tree=tree)
            + "\n"
        )

    def render_toc(self, output_pdf, project_name):
        folder, _ = os.path.split(__file__)
        template_path = os.path.join(folder, "template.html")
        with open(template_path, "r") as html_temp:
            template = Template(html_temp.read())

        ascii_title = text2art(project_name)
        output_html = template.render(
            entries=self.entries, page_number_pos=800, ascii_title=ascii_title
        )

        options = {"quiet": ""}
        pdfkit.from_string(output_html, output_pdf, options=PDFKIT_OPTIONS)

        if PDFCreator.number_of_pages(output_pdf) % 2:
            PDFCreator.add_blank_page(output_pdf)
