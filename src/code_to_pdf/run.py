import os
import argparse
import logging
logging.basicConfig(level=logging.DEBUG)
from pathlib import Path
from code_to_pdf.html_generator import code_to_html
from code_to_pdf.pdf_generator import html_to_numerized_pdf, merge_pdfs
from code_to_pdf.toc_generator import TocGenerator
#from code_to_pdf.temporal import get_temp_folder, get_temp_file
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
    page_number = 1
    pdf_list = []
    toc = TocGenerator()

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

        toc.add_entry(file_name, depth + 1, page_number, tree_string, is_dir=is_dir)

        if is_dir:
            logging.info(depth * "   " + "Folder: {}".format(file_name))
        else:
            path_rel = os.path.relpath(path_str, args['source_code']) 
            output_folder = os.path.join(temp_folder, path_rel)
            output_html = os.path.join(temp_folder, path_rel + ".html")
            output_pdf = os.path.join(temp_folder, path_rel + ".pdf")
            os.makedirs(output_folder, exist_ok=True)
            code_to_html(path_str, output_html)

            logging.info((depth + 1) * "   " + "File: {}: {}".format(file_name, page_number))
            page_number = html_to_numerized_pdf(output_html, output_pdf, page_number)
            pdf_list.append(output_pdf)

    all_contents_pdf = os.path.join(temp_folder, "all_contents.pdf")
    merge_pdfs(pdf_list, all_contents_pdf)

    output_toc_pdf = os.path.join(temp_folder, "output_toc.pdf")
    toc.render_toc(output_toc_pdf, args['project_name'])
    merge_pdfs([output_toc_pdf, all_contents_pdf], args['output_pdf'])

    print("Success!")
    print(f"File written in {args['output_pdf']}")


if __name__ == "__main__":
    main()
