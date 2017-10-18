"""Python script to parse horse race pdfs and extract winners and odds."""

import os
import re
from PyPDF2 import PdfFileReader


races = []
directory = "/Users/gabrielmeringolo/Python/day_at_the_races/race_results/arlington/2016"


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
                horse_number = re.search(f'(?<=WinPlaceShow\\n).[^{winner}]*', pdf_text)
                print(f'Race: {i + 1}, Number: {horse_number.group(0)}')
            elif 'WinPlace' in pdf_text:
                horse_number = re.search(f'(?<=WinPlace\\n).[^{winner}]*', pdf_text)
                print(f'Race: {i + 1}, Number: {horse_number.group(0)}')


# # This will parse a race pdf and find the winner of the race.
# with open(directory, 'rb') as pdfFileObj:
#     reader = PdfFileReader(pdfFileObj)
#     if reader.isEncrypted:
#         reader.decrypt('')
#     # This is iterating over the pages.
#     content = reader.getPage(0)
#     pdf_text = content.extractText()
#     race_day_location = re.search(".*(?=-Race1)", pdf_text)
#     print(race_day_location.group(0))
#     for i in range(reader.getNumPages()):
#         content = reader.getPage(i)
#         pdf_text = content.extractText()
#         # Extracting the winning horse's name with regex.
#         winner = re.search('(?<=Winner:\\n).[^,]*', pdf_text)
#         # Extracting the winning horse's number with regex.
#         if 'WinPlaceShow' in pdf_text:
#             horse_number = re.search(f'(?<=WinPlaceShow\\n).[^{winner}]*', pdf_text)
#             print(f'Race number {i + 1}, Winning horse: {winner.group(0)}, Number: {horse_number.group(0)}')
#         elif 'WinPlace' in pdf_text:
#             horse_number = re.search(f'(?<=WinPlace\\n).[^{winner}]*', pdf_text)
#             print(f'Race number {i + 1}, Winning horse: {winner.group(0)}, Number: {horse_number.group(0)}')

        # print(type(horse_number))
        # races.append(winner.group(0))
        # races.append(pdf_text)
        # print(number.group(0))
        # print(f'page number {i}:\n{type(pdf_text)}\n\n')


# print(races)
