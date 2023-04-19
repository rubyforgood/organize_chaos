import pypdfium2 as pdfium


def get_pdf_content(file: str) -> str:
    """Derive the file contents of pdf"""
    try:
        pdf = pdfium.PdfDocument(file)
        contents = ""
        for i in range(len(pdf)):
            page = pdf[i]
            # Load a text page helper
            textpage = page.get_textpage()
            text_all = textpage.get_text_range()
            contents += text_all

        return contents
    except Exception as e:
        print(f"\n\nCannot parse PDF at '{file}'\n\n")
        raise e
