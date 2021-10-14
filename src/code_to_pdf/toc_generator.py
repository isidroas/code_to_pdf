import logging
import os
import re
import tempfile
from collections import namedtuple
from typing import List

import pdfkit
from art import text2art
from git import Repo
from git.exc import InvalidGitRepositoryError
from jinja2 import Template

from code_to_pdf.pdf_generator import PDFKIT_OPTIONS, PDFCreator

GitInfo = namedtuple("GitInfo", "commit datetime branch")


class Entry:
    ENTRY_DIR = """<div class=row>{{ 157*'.' }}<span class="row_text"> {{tree}}<span class="dir">{{ name }} </span>&nbsp</span><span class="right">{{ page }}</div>"""
    ENTRY_FILE = """<div class=row>{{ 157*'.' }}<span class="row_text">{{tree}} <span class="file">{{ name }}&nbsp</span></span><span class="right">{{ page }}</div>"""

    def __init__(self, name="", depth=0, page=0, tree="", is_dir=False):
        self.name = name
        self.depth = depth
        self.page = depth

        tree = re.sub(" ", "&nbsp;&nbsp;", tree)
        self.tree = tree

        self.is_dir = is_dir

    def render_html(self) -> str:
        if self.is_dir:
            template = Template(self.ENTRY_DIR)
        else:
            template = Template(self.ENTRY_FILE)
        return template.render(
            name=self.name, depth=self.depth, page=self.page, tree=self.tree
        )


class TocGenerator:
    def __init__(self, max_pages_per_volume=300):
        self.entries = ""
        self.max_pages_per_volume = max_pages_per_volume
        self.entries_list: List[Entry] = []

    def add_entry(self, name, depth, page, tree, is_dir=False):
        if is_dir:
            logging.info(depth * "   " + "Folder: {}".format(name))
        else:
            logging.info((depth + 1) * "   " + "File: {}: {}".format(name, page))
        self.entries_list.append(
            Entry(name=name, depth=depth, page=page, tree=tree, is_dir=is_dir)
        )

    @staticmethod
    def _get_git_info(path):
        try:
            repo = Repo(path)
        except InvalidGitRepositoryError:
            return None

        is_dirty = repo.is_dirty()
        commit = str(repo.head.commit)[:9]
        commit += "*" if is_dirty else ""
        datetime = repo.head.commit.committed_datetime.strftime("%Y-%m-%d %H:%M:%S")
        branch = repo.active_branch.name
        return GitInfo(commit, datetime, branch)

    def render_toc(self, project_name, version_control_folder: str = None):
        folder, _ = os.path.split(__file__)
        template_path = os.path.join(folder, "template.html")
        with open(template_path, "r") as html_temp:
            template = Template(html_temp.read())

        ascii_title = text2art(project_name)

        output_pdf = tempfile.NamedTemporaryFile(suffix=".pdf").name

        git_info = (
            self._get_git_info(version_control_folder)
            if version_control_folder
            else None
        )

        entries = ""
        for it in self.entries_list:
            entries += it.render_html() + "\n"

        output_html = template.render(
            entries=entries,
            page_number_pos=800,
            ascii_title=ascii_title,
            git_info=git_info,
        )

        pdfkit.from_string(output_html, output_pdf, options=PDFKIT_OPTIONS)

        if PDFCreator.number_of_pages(output_pdf) % 2:
            PDFCreator.add_blank_page(output_pdf)

        return output_pdf

    def generate_volumes(output_path: str):
        pass
