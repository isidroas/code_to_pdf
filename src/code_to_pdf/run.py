import argparse
import logging
import os

from code_to_pdf.html_generator import code_to_html
from code_to_pdf.pdf_generator import PDFCreator
from code_to_pdf.toc_generator import TocGenerator
from code_to_pdf.tree_generator import TreeGenerator

logging.basicConfig(level=logging.DEBUG)


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

    for (
        path_str,
        file_name,
        is_dir,
        depth,
        tree_string,
        path_rel,
    ) in TreeGenerator.get_iterable(args["source_code"]):

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
