import os
from html_generator import code_to_html
from pdf_generator import html_to_numerized_pdf, merge_pdfs
from toc_generator import render_toc, get_entry
from temporal import get_temp_folder, get_temp_file

PROYECT_FOLDER = "gurux_black"
# exclude containg the following in path name
EXCLUDE_LIST = [".git"]
EXCLUDE_FOLDER = [".git"]

temp_folder = get_temp_folder()


def is_excluded(exclude_list, path):
    for exclude in exclude_list:
        if exclude in path:
            return True
    return False


page_number = 1
pdf_list = []
entries = ""
for root, subdirs, files in os.walk(PROYECT_FOLDER):
    path_list = root.split(os.sep)
    depth = len(path_list)
    folder = path_list[-1]
    if is_excluded(EXCLUDE_FOLDER, root):
        continue
    print(depth * "   " + "Folder: {}".format(folder))
    entries = entries + get_entry(folder, depth, page_number, is_dir=True)
    for file in files:
        file_path = os.path.join(root, file)
        if is_excluded(EXCLUDE_LIST, file_path):
            continue
        output_html = os.path.join(temp_folder, file_path + ".html")
        output_pdf = os.path.join(temp_folder, file_path + ".pdf")
        output_folder = os.path.join(temp_folder, root)
        os.makedirs(output_folder, exist_ok=True)
        code_to_html(file_path, output_html)

        print((depth + 1) * "   " + "File: {}: {}".format(file, page_number))
        entries = entries + get_entry(file, depth + 1, page_number)
        page_number = html_to_numerized_pdf(output_html, output_pdf, page_number)
        pdf_list.append(output_pdf)
        # print("Generated {} pages".format(page_number))

all_contents_pdf = os.path.join(temp_folder, "all_contents.pdf")
merge_pdfs(pdf_list, all_contents_pdf)

output_toc_pdf = os.path.join(temp_folder, "output_toc.pdf")
render_toc(entries, output_toc_pdf)
merge_pdfs([output_toc_pdf, all_contents_pdf], "final_output.pdf")

print("Success!")
print(f"Temporal files written in {temp_folder}")
