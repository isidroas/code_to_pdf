# coding: utf-8
import re
import pygments
import logging
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, get_lexer_by_name
from pygments.formatters import HtmlFormatter

REGEX_PATTERN = "#\n#..-+\n#...Gurux.Ltd(\n.*){30}"
REGEX_SUB = """
#######################################################################
# File {}
#######################################################################
"""


def code_to_html(input_code: str):
    with open(input_code) as file:
        file_str = file.read()

    # Remove copyright and add header
    license_match = re.search(REGEX_PATTERN, file_str)

    new_header = REGEX_SUB.format(input_code)
#    sub_str = new_header + sub_str
    starting_line = 1

    if license_match:
        if license_match.start() == 0:
            starting_line = len(re.findall('\n', license_match[0]))
            file_str = re.sub(REGEX_PATTERN,'', file_str)

    formater = HtmlFormatter(
        full=True, style="colorful", linenos=True, wrapcode=True, linesparator=True, linenostart=starting_line
    )
    try:
        lexer = get_lexer_for_filename(input_code)
    except pygments.util.ClassNotFound:
        logging.warning('Unable to guess lexer for file {}, using python'.format(input_code) )
        lexer = get_lexer_by_name("python")
    output_str = highlight(file_str, lexer, formater)

    return output_str
