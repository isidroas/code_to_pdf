import pdfkit
import PyPDF2
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

INPUT_PDF = "input.pdf"
OUTPUT_PDF = "output.pdf"
INPUT_HTML = "output.html"


def _get_temp_file():
    with tempfile.NamedTemporaryFile(suffix=".pdf") as file:
        return file.name


pdfkit.from_file(INPUT_HTML, INPUT_PDF)

pdf_reader = PyPDF2.PdfFileReader(INPUT_PDF)
pdf_writer = PyPDF2.PdfFileWriter()
page = pdf_reader.getPage(0)

## Create
temp_file = _get_temp_file()
c = canvas.Canvas(temp_file)
width, height = A4
x = width * 0.05
y = height * 0.03
c.drawString(x, y, "233")
x = width * 0.92
c.drawString(x, y, "233")
c.showPage()
c.save()

pdf_text = open(temp_file, "rb")
pdf_text_reader = PyPDF2.PdfFileReader(temp_file)
page_text_reader = pdf_text_reader.getPage(0)
page.mergePage(page_text_reader)


pdf_writer.addPage(page)

with open(OUTPUT_PDF, "wb") as file:
    pdf_writer.write(file)
