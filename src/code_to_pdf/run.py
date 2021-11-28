import argparse
import logging
import os

from code_to_pdf.html_generator import code_to_html
from code_to_pdf.pdf_generator import PDFCreator
from code_to_pdf.toc_generator import TocGenerator

# from code_to_pdf.tree_generator import TreeGenerator
from code_to_pdf.tree_generator import walk_tree

logging.basicConfig(level=logging.DEBUG)


class Parameters:
    # def __init__(self, exclude_list: List[str] = [], copyright_regex: str = None):
    #    self.exclude_list = exclude_list
    #    self.copyright_regex = copyright_regex

    def __init__(self):
        self.exclude_list = [
            "__pycache__/",
            "*.swp",
            "*.pdf",
            "*.pyc",
            "/*.html",
            "/*.pdf",
            "*.egg-info",
            ".coverage",
            "venv",
            ".mypy_cache",
            ".git",
            "*~",
            "*.svg",
            "tags",
        ]
        self.copyright_regex = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def argument_parser(raw_args):
    parser = argparse.ArgumentParser(description="Code to PDF generator")
    parser.add_argument("source", type=str, help="Source code folder")
    parser.add_argument("--project-name", type=str, help="Title of the document")
    parser.add_argument(
        "--output-pdf", type=str, help="Path where pdf will be generated"
    )
    parser.add_argument(
        "--max-pages-per-volume",
        type=int,
        help="If given, it will generate more than one pdf when the total pages are greater than the given number",
    )
    args_obj = parser.parse_args(raw_args)

    args = {}
    args["source_code"] = os.path.abspath(args_obj.source)
    args["project_name"] = (
        args_obj.project_name
        if args_obj.project_name
        else os.path.basename(args["source_code"])  # TODO: this fails if not end by '/'
    )
    args["output_pdf"] = (
        args_obj.output_pdf if args_obj.output_pdf else args["project_name"] + ".pdf"
    )
    args["max_pages_per_volume"] = args_obj.max_pages_per_volume
    return args


def main(raw_args=None):
    toc = TocGenerator()
    pdf_creator = PDFCreator()
    args = argument_parser(raw_args)

    params = Parameters()

    for (path_str, file_name, is_dir, depth, tree_string, path_rel) in walk_tree(
        args["source_code"], excluded_files=params.exclude_list
    ):

        toc.add_entry(
            file_name, depth + 1, pdf_creator.page_number, tree_string, is_dir=is_dir
        )

        if not is_dir:
            output_html = code_to_html(path_str, path_rel)
            pdf_creator.add_html(output_html)

    if args["max_pages_per_volume"]:
        toc.generate_volumes(
            args["project_name"],
            args["output_pdf"],
            pdf_creator.full_pdf,
            args["max_pages_per_volume"],
            version_control_folder=args["source_code"],
        )
    else:
        toc_pdf = toc.render_toc(args["project_name"], args["source_code"])
        # toc + pdf_creator => output_pdf
        PDFCreator.merge_pdfs([toc_pdf, pdf_creator.full_pdf], args["output_pdf"])

    logging.info("Success!")
    logging.info(f"File written in {args['output_pdf']}")


if __name__ == "__main__":
    main()
