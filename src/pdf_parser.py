"""Race results PDF parser."""
import os

import re

from datetime import date, timedelta

from PyPDF2 import PdfFileReader


ROOT_DIR = os.path.abspath('./..')


def pdf_parser():
    """Parse PDFs fpr race result data."""
