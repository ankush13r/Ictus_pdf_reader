#You must upgrade setuptools and install padfminer librery first.

"""pip install --upgrade setuptools"""
"""pip install pdfminer3K"""

from pdfminer.pdfinterp import PDFResourceManager , process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO


def readPDF(pdf_file):
    resource_maneger = PDFResourceManager()
    ret_string = StringIO()
    laparams = LAParams()
    device = TextConverter(resource_maneger,ret_string, laparams=laparams)
    
    process_pdf(resource_maneger,device,pdf_file)
    device.close()

    content = ret_string.getvalue()
    ret_string.close()
    return content



