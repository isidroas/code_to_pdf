import pdfkit
import PyPDF2
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from temporal import get_temp_file


def html_to_numerized_pdf(input_html, output_pdf, start_page):
    #    input_pdf = _get_temp_file()
    input_pdf = input_html[:-5] + "_tmp.pdf"
    # options = {"quiet": "",
    #          'margin-left': '20000in'}
    options = {
        "quiet": "",
        "page-size": "A4",
        "margin-top": "0.1in",
        "margin-right": "0.3in",
        "margin-bottom": "0.7in",
        "margin-left": "0.3in",
        #        'encoding': "UTF-8",
        #        'custom-header' : [
        #            ('Accept-Encoding', 'gzip')
        #        ],
        #        'cookie': [
        #            ('cookie-name1', 'cookie-value1'),
        #            ('cookie-name2', 'cookie-value2'),
        #        ],
        "outline": None,
    }
    #              'margin-bottom': '0.75in'}
    pdfkit.from_file(input_html, input_pdf, options=options)

    pdf_reader = PyPDF2.PdfFileReader(input_pdf)
    pdf_writer = PyPDF2.PdfFileWriter()

    n_pages = pdf_reader.getNumPages()

    for n_page in range(n_pages):
        page = pdf_reader.getPage(n_page)

        ## Create
        temp_file = get_temp_file()
        c = canvas.Canvas(temp_file)
        width, height = A4
        y = height * 0.03
        absolute_page = n_page + start_page
        if (absolute_page + 1) % 2:
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
    return absolute_page + 1


# input_html = "output.html"
# input_pdf = "input.pdf"
# output_pdf = "output.pdf"


# html_to_numerized_pdf(input_html, output_pdf, 250)
def merge_pdfs(pdf_list, output_pdf):
    pdf_writer = PyPDF2.PdfFileWriter()
    for pdf in pdf_list:
        pdf_reader = PyPDF2.PdfFileReader(pdf)
        n_pages = pdf_reader.getNumPages()
        for n_page in range(n_pages):
            pdf_writer.addPage(pdf_reader.getPage(n_page))

    with open(output_pdf, "wb") as file:
        pdf_writer.write(file)


def add_blank_page(pdf_file):
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    pdf_writer = PyPDF2.PdfFileWriter()
    n_pages = pdf_reader.getNumPages()

    pdf_writer.appendPagesFromReader(pdf_reader)
    pdf_writer.addBlankPage()

    with open(pdf_file, "wb") as file:
        pdf_writer.write(file)


def number_of_pages(pdf_file):
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    return pdf_reader.getNumPages()
