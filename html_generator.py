# coding: utf-8
import re
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

REGEX_PATTERN = "#\n#..-+\n#...Gurux.Ltd(\n.*){31}"
REGEX_SUB = """
############################################
# File {}
############################################"""
file_path = "gurux/Gurux.DLMS.python/setup.py"


def code_to_html(file_path, output_html):
    with open(file_path) as file:
        file_str = file.read()

    # Remove copyright and add header
    sub_str = re.sub(REGEX_PATTERN, REGEX_SUB.format(file_path), file_str)

    formater = HtmlFormatter(full=True, style="colorful", linenos=True)
    output_str = highlight(sub_str, PythonLexer(), formater)

    with open(output_html, "w") as output_file:
        output_file.write(output_str)


code_to_html(file_path, "output.html")
