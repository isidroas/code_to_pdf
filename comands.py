# coding: utf-8
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

file = open("gurux/Gurux.DLMS.python/setup.py")
file_str = file.read()

formater = HtmlFormatter(full=True, style="colorful", linenos=True)
output_str = highlight(file_str, PythonLexer(), formater)

output_file = open("output.html", "w")
output_file.write(output_str)
output_file.close()
