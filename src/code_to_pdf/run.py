import os
import argparse
import logging
logging.basicConfig(level=logging.DEBUG)
from pathlib import Path
from code_to_pdf.html_generator import code_to_html
from code_to_pdf.pdf_generator import PDFCreator
from code_to_pdf.toc_generator import TocGenerator
from code_to_pdf.temporal import Temporal
from code_to_pdf.tree_generator import TreeGenerator


def argument_parser(raw_args):
    parser = argparse.ArgumentParser(description="Code to PDF generator")
    parser.add_argument("source", type=str, help="Source code folder")
    parser.add_argument("--project-name", type=str, help="Title of the document")
    parser.add_argument(
        "--output-pdf", type=str, help="Path where pdf will be generated"
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
        args_obj.output_pdf

        if args_obj.output_pdf
        else args["project_name"] + ".pdf"
    )
    return args


def main(raw_args=None):
    toc = TocGenerator()
    pdf_creator = PDFCreator()

    temp = Temporal()
    temp_folder = temp.get_temp_folder()

    args = argument_parser(raw_args)


    for (
        path_str,
        file_name,
        is_dir,
        depth,
        parent,
        current_folder,
        tree_string,
    ) in TreeGenerator.get_iterable(args['source_code']):

        
        toc.add_entry(file_name, depth + 1, pdf_creator.page_number, tree_string, is_dir=is_dir)

        if not is_dir:
            path_rel = os.path.relpath(path_str, args['source_code']) 
            output_html = code_to_html(path_str)
            pdf_creator.add_html(output_html, path_rel)

    output_toc_pdf = os.path.join(temp_folder, "output_toc.pdf")
    toc.render_toc(output_toc_pdf, args['project_name'])

    PDFCreator.merge_pdfs([output_toc_pdf, pdf_creator.full_pdf], args['output_pdf'])

    print("Success!")
    print(f"File written in {args['output_pdf']}")


if __name__ == "__main__":
    main()
