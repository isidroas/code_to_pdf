# coding: utf-8
import re
import pygments
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, get_lexer_by_name
from pygments.formatters import HtmlFormatter

REGEX_PATTERN = "#\n#..-+\n#...Gurux.Ltd(\n.*){30}"
REGEX_SUB = """
#######################################################################
# File {}
#######################################################################
"""


def code_to_html(intput_code, output_html):
    with open(intput_code) as file:
        file_str = file.read()

    # Remove copyright and add header
    sub_str = re.sub(REGEX_PATTERN, "", file_str)
    new_header = REGEX_SUB.format(intput_code)
    sub_str = new_header + sub_str

    formater = HtmlFormatter(
        full=True, style="colorful", linenos=True, wrapcode=True, linesparator=True
    )
    try:
        lexer = get_lexer_for_filename(intput_code)
    except pygments.util.ClassNotFound:
        lexer = get_lexer_by_name("python")
    output_str = highlight(sub_str, lexer, formater)

    with open(output_html, "w") as output_file:
        output_file.write(output_str)
