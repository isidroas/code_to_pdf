# coding: utf-8
import logging
import re

import pygments
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename

REGEX_PATTERN = "#\n#..-+\n#...Gurux.Ltd(\n.*){30}"

REGEX_SUB = """
<h3>
<span class="c1">
# {}
</span>
</h3>
"""


def code_to_html(input_code: str, name_in_header: str):
    with open(input_code) as file:
        file_str = file.read()

    # Remove copyright and add header
    license_match = re.search(REGEX_PATTERN, file_str)

    starting_line = 1

    if license_match:
        if license_match.start() == 0:
            starting_line = len(re.findall("\n", license_match[0])) + 2
            file_str = re.sub(REGEX_PATTERN, "", file_str)

    formater = HtmlFormatter(
        full=True,
        style="colorful",
        linenos=True,
        # if a line is too long, it adds a linebreak
        wrapcode=True,
        linesparator=True,
        linenostart=starting_line,
    )
    try:
        lexer = get_lexer_for_filename(input_code)
    except pygments.util.ClassNotFound:
        logging.warning(
            "Unable to guess lexer for file {}, using python".format(input_code)
        )
        lexer = get_lexer_by_name("python")
    output_str = highlight(file_str, lexer, formater)

    new_header = REGEX_SUB.format(name_in_header)
    index = output_str.find("<body>") + len("<body>")
    output_str_header = output_str[:index] + new_header + output_str[index:]

    return output_str_header


if __name__ == "__main__":
    res = code_to_html(__file__, "this file")
    with open("res.html", "wt") as file:
        file.write(res)
