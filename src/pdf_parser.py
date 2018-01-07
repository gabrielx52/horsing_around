"""Race results PDF parser."""
import os

from PyPDF2 import PdfFileReader

TRACKS = ['AQU', 'BEL', 'KD', 'SA', 'SAR']

RES_DIR = os.path.abspath('./../results')


test_pdf = '/Users/gabrielmeringolo/Python/day_at_the_races/results/OP/2016-01-15.pdf'


def pdf_parser(test_pdf):
    """Parse PDFs fpr race result data."""
    with open(test_pdf, 'rb') as f:
        reader = PdfFileReader(f, strict=False)
        # import pdb; pdb.set_trace()
        if reader.isEncrypted:
            reader.decrypt('')
        for i in range(reader.getNumPages()):
            content = reader.getPage(i)
            pdf_text = content.extractText()
            input('\n' + pdf_text)


# def pdf_parser(track_code):
#     """Parse PDFs fpr race result data."""
#     t_dir = RES_DIR + '/{}'.format(track_code)
#     for pdf in os.listdir(t_dir):
#         with open(t_dir + '/{}'.format(pdf), 'rb') as f:
#             reader = PdfFileReader(f, strict=False)
#             if reader.isEncrypted:
#                 reader.decrypt('')
#             content = reader.getPage(0)
#             pdf_text = content.extractText()
#             return pdf_text
