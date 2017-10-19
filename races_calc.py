"""Python script to parse horse race pdfs and extract winners and odds."""

import os
import re
from datetime import timedelta, date
from PyPDF2 import PdfFileReader


races = []
directory = os.path.abspath('./race_results/arlington/2016')


track_codes = {'KD': (9, 10),
               'SAR': (7, 8, 9, 10),
               'BEL': (4, 5, 6, 7, 8),
               'SA': (1, 2, 3, 4, 5, 6, 7, 8),
               'KEE': (4, 5, 10, 11),
               'DMR': (7, 8, 9, 11, 12),
               'CD': (4, 5, 6, 9, 10, 11, 12),
               'AQU': (1, 2, 3, 4, 5, 6),
               'OP': (1, 2, 3, 4, 5, 6)}

# pdf_url = 'http://www.equibase.com/premium/eqbPDFChartPlus.cfm?\
# RACE=A&BorP=P&TID=SA&CTRY=USA&DT=01/15/2016&DAY=D&STYLE=EQB'

pdf_url = 'http://www.equibase.com/premium/eqbPDFChartPlus.cfm?RACE=A&BorP=P&TID=AQU&CTRY=USA&DT=11/08/2015&DAY=D&STYLE=EQB'


def daterange(start_date, end_date):
    """Generate all dates in date range."""
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2010, 1, 1)
end_date = date(2016, 1, 1)
for single_date in daterange(start_date, end_date):
    print(single_date.strftime("%Y-%m-%d"))

# print(pdf_url)

for pdf in os.listdir(directory):
    with open(os.path.join(directory, pdf), 'rb') as pdfFileObj:
        reader = PdfFileReader(pdfFileObj)
        if reader.isEncrypted:
            reader.decrypt('')
        content = reader.getPage(0)
        pdf_text = content.extractText()
        race_day_location = re.search(".*(?=-Race1)", pdf_text)
        print(race_day_location.group(0))
        for i in range(reader.getNumPages()):
            content = reader.getPage(i)
            pdf_text = content.extractText()
            # Extracting the winning horse's name with regex.
            winner = re.search('(?<=Winner:\\n).[^,]*', pdf_text)
            # Extracting the winning horse's number with regex.
            if 'WinPlaceShow' in pdf_text:
                horse_num = re.search(f'(?<=WinPlaceShow\\n).[^{winner}]*', pdf_text)
                print(f'Race: {i + 1}, Number: {horse_num.group(0)}')
            elif 'WinPlace' in pdf_text:
                horse_num = re.search(f'(?<=WinPlace\\n).[^{winner}]*', pdf_text)
                print(f'Race: {i + 1}, Number: {horse_num.group(0)}')
