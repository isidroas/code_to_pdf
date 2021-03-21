import os
from html_generator import code_to_html
from pdf_generator import html_to_numerized_pdf

PROYECT_FOLDER = "gurux_small"
# exclude containg the following in path name
EXCLUDE_LIST = [".git"]
temp_folder = "tmp"


def is_excluded(exclude_list, path):
    for exclude in exclude_list:
        if exclude in path:
            return True
    return False


page_number = 0
for root, subdirs, files in os.walk(PROYECT_FOLDER):
    for file in files:
        file_path = os.path.join(root, file)
        if is_excluded(EXCLUDE_LIST, file_path):
            continue
        output_html = os.path.join(temp_folder, file_path + ".html")
        output_pdf = os.path.join(temp_folder, file_path + ".pdf")
        output_folder = os.path.join(temp_folder, root)
        os.makedirs(output_folder, exist_ok=True)
        code_to_html(file_path, output_html)

        page_number = html_to_numerized_pdf(output_html, output_pdf, page_number)
        print(page_number)
