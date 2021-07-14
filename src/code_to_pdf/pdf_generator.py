import pdfkit
import PyPDF2
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


PDFKIT_OPTIONS = {
    "quiet": "",
    "page-size": "A4",
    "margin-top": "0.45in",
    "margin-right": "0.3in",
    "margin-bottom": "0.5in",
    "margin-left": "0.3in",
    "encoding": "UTF-8",
    "custom-header": [("Accept-Encoding", "gzip")],
    "outline": None,
}


def html_to_numerized_pdf(input_html: str, output_pdf: str, start_page: int, header_name: str):
    """Generate numerized pdf pages from a html file

    :param input_html: Path to input html
    :param output: Path where output pdf will be generated
    :param start_page: number written in the first page of the PDF
    :type start_page: int
    :return: last page number written + 1
    :rtype: int
    """
    # remove .html exension and change it to .pdf
    input_pdf = input_html[:-5] + "_tmp.pdf"
    pdfkit.from_file(input_html, input_pdf, options=PDFKIT_OPTIONS)

    pdf_reader = PyPDF2.PdfFileReader(input_pdf)
    pdf_writer = PyPDF2.PdfFileWriter()

    n_pages = pdf_reader.getNumPages()

    for n_page in range(n_pages):
        page = pdf_reader.getPage(n_page)

        ## Create
#        temp_file = get_temp_file()
        #with tempfile.NamedTemporaryFile(suffix="pdf") as temp_file:
        #with open(input_html[:-5] + "_canvas.pdf",'+') as temp_file:
        temp_file = input_html[:-5] + "_canvas.pdf"
        c = canvas.Canvas(temp_file)
        width, height = A4
        y = height * 0.03
        absolute_page = n_page + start_page
        x = width * 0.92
        c.drawString(x, y, str(absolute_page))
        # Print file header for the first page
        if n_page==0:
            # TODO: add this header in html. This is not mantenible because 
            # the positions depends on the margins

            textobject = c.beginText(width*0.075, height*0.97)
            textobject.setFillGray(0.8)
            c.setFont("Helvetica", 10)
            textobject.textLine("#")
            textobject.textLine('# ' + header_name)
            textobject.textLine("#")
            c.drawText(textobject) 

        c.showPage()
        c.save()

        pdf_text_reader = PyPDF2.PdfFileReader(temp_file)
        page_text_reader = pdf_text_reader.getPage(0)
        page.mergePage(page_text_reader)

        pdf_writer.addPage(page)

    with open(output_pdf, "wb") as file:
        pdf_writer.write(file)
    return absolute_page + 1


def merge_pdfs(pdf_list, output_pdf):
    """Join various pdf files.

    :param pdf_list: List of PDF paths
    :param output_pdf: Path of generated pdf
    :type output_pdf: str"""

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
    """ Get number of pages of a PDF """
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    return pdf_reader.getNumPages()
