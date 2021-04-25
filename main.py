import os
import argparse
from html_generator import code_to_html
from pdf_generator import html_to_numerized_pdf, merge_pdfs
from toc_generator import render_toc, get_entry
from temporal import get_temp_folder, get_temp_file
from tree_generator import DisplayablePath
from pathlib import Path


def argument_parser():
    parser = argparse.ArgumentParser(description="Code to PDF generator")
    parser.add_argument("source", type=str, help="Source code folder")
    parser.add_argument("--project-name", type=str, help="Title of the document")
    args_obj = parser.parse_args()
    args = {}
    args["source_code"] = args_obj.source

    args["project_name"] = (
        args_obj.project_name
        if args_obj.project_name
        else os.path.dirname(args_obj.source) # TODO: this fails if not end by '/'
    )
    return args


def main():
    page_number = 1
    pdf_list = []
    entries = ""

    temp_folder = get_temp_folder()

    args = argument_parser()

    for path_object in DisplayablePath.make_tree(Path(args["source_code"])):
        path_str = str(path_object.path)
        file_name = path_object.displayname
        is_dir = path_object.path.is_dir()
        depth = path_object.depth
        parent = path_object.parent
        current_folder = str(parent.path) if parent else "."
        tree_string = path_object.displayable()

        entries = entries + get_entry(
            file_name, depth + 1, page_number, tree_string, is_dir=is_dir
        )

        if is_dir:
            print(depth * "   " + "Folder: {}".format(file_name))
        else:
            output_html = os.path.join(temp_folder, path_str + ".html")
            output_pdf = os.path.join(temp_folder, path_str + ".pdf")
            output_folder = os.path.join(temp_folder, current_folder)
            os.makedirs(output_folder, exist_ok=True)
            code_to_html(path_str, output_html)

            print((depth + 1) * "   " + "File: {}: {}".format(file_name, page_number))
            page_number = html_to_numerized_pdf(output_html, output_pdf, page_number)
            pdf_list.append(output_pdf)

    all_contents_pdf = os.path.join(temp_folder, "all_contents.pdf")
    merge_pdfs(pdf_list, all_contents_pdf)

    output_toc_pdf = os.path.join(temp_folder, "output_toc.pdf")
    render_toc(entries, output_toc_pdf, args["project_name"])
    merge_pdfs([output_toc_pdf, all_contents_pdf], "final_output.pdf")

    print("Success!")
    print(f"Temporal files written in {temp_folder}")


if __name__ == "__main__":
    main()
