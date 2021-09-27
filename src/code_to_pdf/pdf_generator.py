import pdfkit
import PyPDF2
import os
import shutil
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




class PDFCreator:
    def __init__(self):
        self.page_number=1
        self.full_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False).name
        print(self.full_pdf)

    
    def add_html(self, input_html: str,  header_name: str):
        """Generate numerized pdf pages from a html file

        :param input_html: html in string
        :param start_page: number written in the first page of the PDF
        """
        input_pdf = tempfile.NamedTemporaryFile()
        pdfkit.from_string(input_html, input_pdf.name, options=PDFKIT_OPTIONS)

        pdf_reader = PyPDF2.PdfFileReader(input_pdf)
        pdf_writer = PyPDF2.PdfFileWriter()

        
        if os.path.isfile(self.full_pdf) and os.path.getsize(self.full_pdf)>0:
            # It is a non empty file

            pdf_reader_full = PyPDF2.PdfFileReader(self.full_pdf)
            pdf_writer.appendPagesFromReader(pdf_reader_full)

        n_pages = pdf_reader.getNumPages()

        for n_page in range(n_pages):
            page = pdf_reader.getPage(n_page)

            ## Create
            temp_file =  tempfile.NamedTemporaryFile(suffix="pdf", delete=False)
            c = canvas.Canvas(temp_file.name)
            width, height = A4
            y = height * 0.03
            self.page_number += n_page
            x = width * 0.92
            c.drawString(x, y, str(self.page_number))

            if n_page==0:
                # Print file header for the first page
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

            # temp_file + pdf_text_reader => pdf_writer
            pdf_text_reader = PyPDF2.PdfFileReader(temp_file.name)
            page_text_reader = pdf_text_reader.getPage(0)
            page.mergePage(page_text_reader)

            pdf_writer.addPage(page)

            self.page_number +=1



        with open(self.full_pdf, 'wb') as file:
            pdf_writer.write(file)








    def save_in_path(self, path:str):
        shutil.copyfile(self.full_pdf, path)

    @staticmethod
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


    @staticmethod
    def add_blank_page(pdf_file):
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pdf_writer = PyPDF2.PdfFileWriter()
        n_pages = pdf_reader.getNumPages()

        pdf_writer.appendPagesFromReader(pdf_reader)
        pdf_writer.addBlankPage()

        with open(pdf_file, "wb") as file:
            pdf_writer.write(file)


    @staticmethod
    def number_of_pages(pdf_file):
        """ Get number of pages of a PDF """
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        return pdf_reader.getNumPages()


if __name__=="__main__":
    pdfcreator = PDFCreator()
    html_1 = """
<html>
<body>
    this is page 1
</body>
</html>
"""
    html_2 = """
<html>
<body>
    this is page 2
</body>
</html>
"""
    html_3 = """
<html>
<body>
    this is page 3
</body>
</html>
"""
    pdfcreator.add_html(html_1, 'HTML 1')
    pdfcreator.add_html(html_2, 'HTML 2')
    pdfcreator.add_html(html_3, 'HTML 3')
    pdfcreator.save_in_path('./pruebapdf.pdf')
