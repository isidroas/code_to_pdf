class PDFCreator:
    def add_html(self, html, relative_path):
        pass

    def get_pages(self):
        return 0


class TOC:
    def add_entry(self, relative_path, n_page):
        pass


def code_to_html(file):
    return ""


def main(path_to_code, output_pdf):
    pdf_creator = PDFCreator()
    toc = TOC()

    for file, relative_path in os.walk(path_to_code):

        html = code_to_html(file)

        pdf_creator.add_html(html, relative_path)

        toc.add_entry(relative_path, pdf_creator.get_pages())

    # toc + pdf_creator => output_pdf
    #    join_PDFs(pdf_creator.full_output, toc.render_page(), output_pdf)
    toc.generate_volumes(max_pages_per_volume=max_pages_per_volume)
