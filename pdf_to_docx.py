from pdf2docx import parse
from typing import Tuple


def convert_pdf2docx(input_file: str, pages: Tuple = None):
    """Converts pdf to docx"""
    input_pdf = input_file + ".pdf"
    output_file = input_file + ".docx"
    if pages:
        pages = [int(i) for i in list(pages) if i.isnumeric()]
    result = parse(pdf_file=input_pdf,
                   docx_with_path=output_file, pages=pages)
    return output_file