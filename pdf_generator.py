import pdfkit
import PyPDF2
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def _get_temp_file():
    with tempfile.NamedTemporaryFile(suffix=".pdf") as file:
        return file.name


def numerize_pdf(input_html, output_pdf, start_page):

    input_pdf = _get_temp_file()
    pdfkit.from_file(input_html, input_pdf)

    pdf_reader = PyPDF2.PdfFileReader(input_pdf)
    pdf_writer = PyPDF2.PdfFileWriter()

    n_pages = pdf_reader.getNumPages()

    for n_page in range(n_pages):
        page = pdf_reader.getPage(n_page)

        ## Create
        temp_file = _get_temp_file()
        c = canvas.Canvas(temp_file)
        width, height = A4
        y = height * 0.03
        absolute_page = n_page + start_page
        if absolute_page % 2:
            x = width * 0.05
        else:
            x = width * 0.92
        c.drawString(x, y, str(absolute_page))
        c.showPage()
        c.save()

        pdf_text = open(temp_file, "rb")
        pdf_text_reader = PyPDF2.PdfFileReader(temp_file)
        page_text_reader = pdf_text_reader.getPage(0)
        page.mergePage(page_text_reader)

        pdf_writer.addPage(page)

    with open(output_pdf, "wb") as file:
        pdf_writer.write(file)
    return absolute_page


input_html = "output.html"
input_pdf = "input.pdf"
output_pdf = "output.pdf"


numerize_pdf(input_html, output_pdf, 250)
