import argparse
import logging
import os

import yaml

from code_to_pdf.html_generator import code_to_html
from code_to_pdf.pdf_generator import PDFCreator
from code_to_pdf.toc_generator import TocGenerator

# from code_to_pdf.tree_generator import TreeGenerator
from code_to_pdf.tree_generator import walk_tree

logging.basicConfig(level=logging.DEBUG)

DEFAULT_EXCLUDE_LIST = [
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


class Parameters:
    def __init__(
        self,
        source_folder,
        exclude_list=DEFAULT_EXCLUDE_LIST,
        copyright_regex="MIT.* MERCHANTABILITY,",
        title=None,
        max_pages_per_volume=0,
        output_file="",
    ):
        self.source_folder = source_folder

        self.exclude_list = exclude_list
        self.copyright_regex = copyright_regex
        self.max_pages_per_volume = max_pages_per_volume

        self.title = (
            title if title else os.path.basename(self.source_folder)
        )  # TODO: this fails if not end by '/'

        self.output_file = output_file if output_file else self.title + ".pdf"


def argument_parser(raw_args):
    parser = argparse.ArgumentParser(description="Code to PDF generator")
    parser.add_argument("source_folder", type=str, help="Source code folder")
    parser.add_argument("--title", type=str, help="Title of the document")
    parser.add_argument(
        "--output-file", type=str, help="Path where pdf will be generated"
    )
    parser.add_argument(
        "--max-pages-per-volume",
        type=int,
        help="If given, it will generate more than one pdf when the total pages are greater than the given number",
    )
    parser.add_argument("--config-file", type=str, help="Yaml file for configuration")
    args_obj = parser.parse_args(raw_args)

    args = {}
    args["source_folder"] = os.path.abspath(args_obj.source_folder)
    if args_obj.title:
        args["title"] = args_obj.title
    if args_obj.output_file:
        args["output_file"] = args_obj.output_file
    if args_obj.max_pages_per_volume:
        args["max_pages_per_volume"] = args_obj.max_pages_per_volume

    args["config_file"] = args_obj.config_file if args_obj.config_file else None

    return args


def config_parser(args: dict) -> Parameters:

    config_file = args.pop("config_file")

    if config_file:
        with open(config_file) as file:
            file_dict = yaml.load(file.read(), Loader=yaml.Loader)
            # merge dicts
            # arguments will overwrite file options
        args = {**file_dict, **args}

    params = Parameters(**args)
    return params


def main(raw_args=None):
    args = argument_parser(raw_args)
    params = config_parser(args)

    toc = TocGenerator()
    pdf_creator = PDFCreator()

    for (path_str, file_name, is_dir, depth, tree_string, path_rel) in walk_tree(
        params.source_folder, excluded_files=params.exclude_list
    ):

        toc.add_entry(
            file_name, depth + 1, pdf_creator.page_number, tree_string, is_dir=is_dir
        )

        if not is_dir:
            output_html = code_to_html(
                path_str, path_rel, regex_pattern=params.copyright_regex
            )
            pdf_creator.add_html(output_html)

    if params.max_pages_per_volume:
        toc.generate_volumes(
            params.title,
            params.output_file,
            pdf_creator.full_pdf,
            params.max_pages_per_volume,
            version_control_folder=params.source_folder,
        )
    else:
        toc_pdf = toc.render_toc(params.title, params.source_folder)
        # toc + pdf_creator => output_file
        PDFCreator.merge_pdfs([toc_pdf, pdf_creator.full_pdf], params.output_file)

    logging.info("Success!")
    logging.info(f"File written in {params.output_file}")


if __name__ == "__main__":
    main()
